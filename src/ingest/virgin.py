"""Arrow 41 — virgin ingest Dec 2025 warmup + Jan–May 2026 study. Ingest only."""

from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, time as dtime, timezone
from zoneinfo import ZoneInfo

import polars as pl
from thetadata.errors import NoDataFoundError

from ingest.bars import normalize_ohlc_full, split_sessions
from ingest.calendar import (
    virgin_prior_calendar,
    virgin_sessions,
    virgin_study_sessions,
    virgin_warmup_sessions,
)
from ingest.eligibility import (
    MAX_CLOSE_VIRGIN,
    build_eligibility,
    eod_session_dates,
    with_pdv_10m_flag,
)
from ingest.paths import (
    BARS_DIR,
    FULL_BARS,
    REPORTS,
    SYMBOLS,
    VIRGIN_BARS,
    VIRGIN_ELIGIBILITY,
    VIRGIN_EOD,
    VIRGIN_IWM,
    VIRGIN_MANIFEST,
    VIRGIN_ROOT,
    ensure_virgin_dirs,
    virgin_bar_path,
    virgin_eod_path,
    virgin_iwm_path,
)
from ingest.progress import Progress
from ingest.run import month_groups
from ingest.theta_pool import ThetaLimiter, call_theta
from theta.client import get_shared_client

ET = ZoneInfo("America/New_York")
VENUE = "utp_cta"
INTERVAL = "1m"
START_TIME = dtime(4, 0)
END_TIME = dtime(16, 0)
PRE_CUT = dtime(7, 30)

VIRGIN_EOD_CHUNKS: tuple[tuple[date, date, str], ...] = (
    (date(2025, 12, 16), date(2025, 12, 31), "2025-12"),
    (date(2026, 1, 1), date(2026, 1, 31), "2026-01"),
    (date(2026, 2, 1), date(2026, 2, 28), "2026-02"),
    (date(2026, 3, 1), date(2026, 3, 31), "2026-03"),
    (date(2026, 4, 1), date(2026, 4, 30), "2026-04"),
    (date(2026, 5, 1), date(2026, 5, 29), "2026-05"),
)


def _assert_virgin_tree() -> None:
    root = VIRGIN_ROOT.resolve()
    if FULL_BARS.resolve() == root or BARS_DIR.resolve() == root:
        raise RuntimeError("virgin output collided with data/full or Lab A data/bars")
    if FULL_BARS in (VIRGIN_BARS, VIRGIN_EOD, VIRGIN_IWM):
        raise RuntimeError("virgin paths must not alias data/full")


def sessions_to_pull(symbol: str, dates: list[date], *, force: bool = False) -> list[date]:
    """Resume: skip name-days whose virgin parquet already exists unless force."""
    if force:
        return list(dates)
    return [d for d in dates if not virgin_bar_path(d, symbol).exists()]


def _empty_full_frame(symbol: str, is_warmup: bool) -> pl.DataFrame:
    return normalize_ohlc_full(pl.DataFrame(), symbol, is_warmup)


def _empty_eod(symbol: str) -> pl.DataFrame:
    return pl.DataFrame(
        schema={
            "symbol": pl.String,
            "eod_date": pl.Date,
            "close": pl.Float64,
            "volume": pl.Int64,
        }
    ).with_columns(pl.lit(symbol).alias("symbol"))


def pull_one_eod(
    client,
    limiter: ThetaLimiter,
    symbol: str,
    start: date,
    end: date,
    chunk: str,
    force: bool,
) -> tuple[str, bool, str, str, float]:
    path = virgin_eod_path(symbol, chunk)
    if not force and path.exists():
        return symbol, True, "", "", 0.0
    try:
        df, elapsed = call_theta(
            limiter,
            client.stock_history_eod,
            symbol=symbol,
            start_date=start,
            end_date=end,
        )
        df = df.with_columns(pl.lit(symbol).alias("symbol"))
        df = eod_session_dates(df)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(path)
        return symbol, True, "", "", elapsed
    except NoDataFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        _empty_eod(symbol).write_parquet(path)
        return symbol, True, "", "", 0.0
    except Exception as exc:  # noqa: BLE001
        return symbol, False, type(exc).__name__, str(exc)[:500], 0.0


def _concat_chunk(chunk: str) -> None:
    folder = VIRGIN_EOD / chunk
    if not folder.exists():
        return
    files = [p for p in folder.glob("*.parquet") if not p.name.startswith("_")]
    dest = folder / "_all.parquet"
    if not files:
        return
    with ThreadPoolExecutor(max_workers=8) as pool:
        frames = list(pool.map(pl.read_parquet, files))
    pl.concat(frames, how="diagonal_relaxed").write_parquet(dest)


def pull_eod(
    client,
    limiter: ThetaLimiter,
    symbols: list[str],
    workers: int,
    force: bool,
) -> tuple[pl.DataFrame, list[dict]]:
    failures: list[dict] = []
    for start, end, chunk in VIRGIN_EOD_CHUNKS:
        (VIRGIN_EOD / chunk).mkdir(parents=True, exist_ok=True)
        need = [
            s
            for s in symbols
            if force or not virgin_eod_path(s, chunk).exists()
        ]
        print(
            f"EOD chunk={chunk} {start}..{end} symbols={len(symbols)} need={len(need)}",
            flush=True,
        )
        if need:
            prog = Progress(len(need), f"virgin_eod:{chunk}")
            prog.start_heartbeat()
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futs = [
                    pool.submit(pull_one_eod, client, limiter, sym, start, end, chunk, force)
                    for sym in need
                ]
                for i, fut in enumerate(as_completed(futs), 1):
                    symbol, ok, cls, msg, elapsed = fut.result()
                    prog.mark(symbol, ok=ok, elapsed_s=elapsed)
                    if not ok:
                        failures.append(
                            {
                                "symbol": symbol,
                                "session": f"eod:{chunk}",
                                "error_class": cls,
                                "error_message": msg,
                            }
                        )
                    if i % 250 == 0:
                        prog.heartbeat()
            prog.stop_heartbeat()
            prog.heartbeat()
        print(f"concat EOD chunk={chunk}", flush=True)
        _concat_chunk(chunk)
    eod = load_virgin_eod()
    print(f"EOD loaded rows={eod.height} fails={len(failures)}", flush=True)
    return eod, failures


def load_virgin_eod() -> pl.DataFrame:
    files = sorted(VIRGIN_EOD.glob("*/_all.parquet"))
    if not files:
        files = [p for p in VIRGIN_EOD.rglob("*.parquet") if not p.name.startswith("_")]
    if not files:
        return pl.DataFrame()
    return pl.concat([pl.read_parquet(p) for p in files], how="diagonal_relaxed")


def build_virgin_eligibility(eod: pl.DataFrame, symbols: list[str]) -> pl.DataFrame:
    if eod.height == 0:
        raise FileNotFoundError(f"no virgin EOD under {VIRGIN_EOD}")
    if "eod_date" not in eod.columns:
        eod = eod_session_dates(eod)
    prior_cal = virgin_prior_calendar()
    warm = build_eligibility(
        eod,
        symbols,
        virgin_warmup_sessions(),
        is_warmup=True,
        max_close=MAX_CLOSE_VIRGIN,
        sessions_for_prior=prior_cal,
    )
    study = build_eligibility(
        eod,
        symbols,
        virgin_study_sessions(),
        is_warmup=False,
        max_close=MAX_CLOSE_VIRGIN,
        sessions_for_prior=prior_cal,
    )
    elig = with_pdv_10m_flag(pl.concat([warm, study], how="vertical_relaxed"))
    keep = elig.select(
        "symbol",
        "session_date",
        "prior_close",
        "prior_volume",
        "prior_dollar_volume",
        "eligible",
        "exclude_reason",
        "is_warmup",
        "pdv_ge_10m",
    )
    VIRGIN_ELIGIBILITY.parent.mkdir(parents=True, exist_ok=True)
    keep.write_parquet(VIRGIN_ELIGIBILITY)
    n_ok = keep.filter(pl.col("eligible")).height
    n_sym = keep.filter(pl.col("eligible"))["symbol"].n_unique()
    n_10m = keep.filter(pl.col("eligible") & pl.col("pdv_ge_10m")).height
    n_gt50 = keep.filter(pl.col("eligible") & (pl.col("prior_close") > 50)).height
    print(
        f"virgin eligibility name-days={keep.height} eligible={n_ok} unique={n_sym} "
        f"max_close={MAX_CLOSE_VIRGIN} pdv_ge_10m={n_10m} prior_close_gt_50={n_gt50} "
        f"wrote={VIRGIN_ELIGIBILITY}",
        flush=True,
    )
    return keep


def pull_one_ohlc(
    client,
    limiter: ThetaLimiter,
    symbol: str,
    sessions: list[date],
    force: bool,
    is_warmup: bool,
) -> dict:
    sessions = sorted(sessions)
    need = sessions_to_pull(symbol, sessions, force=force)
    if not need:
        rows = 0
        for d in sessions:
            p = virgin_bar_path(d, symbol)
            rows += pl.read_parquet(p).height if p.exists() else 0
        return {
            "symbol": symbol,
            "ok": True,
            "skipped": True,
            "rows": rows,
            "elapsed_s": 0.0,
            "error_class": "",
            "error_message": "",
        }
    start_d, end_d = need[0], need[-1]
    try:
        kwargs = {
            "symbol": symbol,
            "interval": INTERVAL,
            "start_time": START_TIME,
            "end_time": END_TIME,
            "venue": VENUE,
        }
        if start_d == end_d:
            kwargs["date"] = start_d
        else:
            kwargs["start_date"] = start_d
            kwargs["end_date"] = end_d
        df, elapsed = call_theta(limiter, client.stock_history_ohlc, **kwargs)
        norm = normalize_ohlc_full(df, symbol, is_warmup=is_warmup)
        parts = split_sessions(norm, set(need))
        total = 0
        for d in need:
            part = parts.get(d)
            path = virgin_bar_path(d, symbol)
            path.parent.mkdir(parents=True, exist_ok=True)
            if part is None or part.height == 0:
                _empty_full_frame(symbol, is_warmup).write_parquet(path)
            else:
                part.write_parquet(path)
                total += part.height
        return {
            "symbol": symbol,
            "ok": True,
            "skipped": False,
            "rows": total,
            "elapsed_s": elapsed,
            "error_class": "",
            "error_message": "",
        }
    except NoDataFoundError:
        for d in need:
            path = virgin_bar_path(d, symbol)
            path.parent.mkdir(parents=True, exist_ok=True)
            _empty_full_frame(symbol, is_warmup).write_parquet(path)
        return {
            "symbol": symbol,
            "ok": True,
            "skipped": False,
            "rows": 0,
            "elapsed_s": 0.0,
            "error_class": "",
            "error_message": "",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "symbol": symbol,
            "ok": False,
            "skipped": False,
            "rows": 0,
            "elapsed_s": 0.0,
            "error_class": type(exc).__name__,
            "error_message": str(exc)[:500],
        }


def _jobs_for(elig: pl.DataFrame, target: list[date]) -> list[tuple[str, list[date], bool]]:
    want = set(target)
    warmup = set(virgin_warmup_sessions())
    by_sym: dict[str, list[date]] = {}
    for symbol, session in (
        elig.filter(pl.col("eligible")).select("symbol", "session_date").iter_rows()
    ):
        if session in want:
            by_sym.setdefault(str(symbol), []).append(session)
    jobs: list[tuple[str, list[date], bool]] = []
    for sym, dates in by_sym.items():
        for group in month_groups(dates):
            is_w = all(d in warmup for d in group)
            jobs.append((sym, group, is_w))
    return jobs


def _run_jobs(
    jobs: list[tuple[str, list[date], bool]],
    *,
    client,
    limiter: ThetaLimiter,
    workers: int,
    force: bool,
    job_name: str,
) -> tuple[int, int, int, list[dict]]:
    if not jobs:
        return 0, 0, 0, []
    prog = Progress(len(jobs), job_name)
    prog.start_heartbeat()
    rows = 0
    oks = 0
    fails = 0
    failures: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [
            pool.submit(pull_one_ohlc, client, limiter, sym, dates, force, is_w)
            for sym, dates, is_w in jobs
        ]
        for i, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            prog.mark(rec["symbol"], rows=rec["rows"], elapsed_s=rec["elapsed_s"], ok=rec["ok"])
            rows += rec["rows"]
            if rec["ok"]:
                oks += 1
            else:
                fails += 1
                failures.append(rec)
            if i % 32 == 0:
                prog.heartbeat()
    prog.stop_heartbeat()
    prog.heartbeat()
    return rows, oks, fails, failures


def pull_iwm(*, client, limiter: ThetaLimiter, force: bool = False) -> tuple[int, int]:
    sessions = virgin_sessions()
    VIRGIN_IWM.mkdir(parents=True, exist_ok=True)
    n_ok = 0
    n_fail = 0
    warmup = set(virgin_warmup_sessions())
    for group in month_groups(sessions):
        need = [d for d in group if force or not virgin_iwm_path(d).exists()]
        if not need:
            n_ok += len(group)
            continue
        start_d, end_d = need[0], need[-1]
        kwargs = {
            "symbol": "IWM",
            "interval": INTERVAL,
            "start_time": START_TIME,
            "end_time": END_TIME,
            "venue": VENUE,
        }
        if start_d == end_d:
            kwargs["date"] = start_d
        else:
            kwargs["start_date"] = start_d
            kwargs["end_date"] = end_d
        try:
            df, _elapsed = call_theta(limiter, client.stock_history_ohlc, **kwargs)
            is_w = all(d in warmup for d in need)
            norm = normalize_ohlc_full(df, "IWM", is_warmup=is_w)
            parts = split_sessions(norm, set(need))
            for d in need:
                part = parts.get(d)
                path = virgin_iwm_path(d)
                if part is None or part.height == 0:
                    _empty_full_frame("IWM", is_w).write_parquet(path)
                else:
                    part.write_parquet(path)
                n_ok += 1
            print(f"IWM wrote {start_d}..{end_d} days={len(need)} dir={VIRGIN_IWM}", flush=True)
        except NoDataFoundError:
            for d in need:
                _empty_full_frame("IWM", False).write_parquet(virgin_iwm_path(d))
            print(f"IWM no data {start_d}..{end_d}", flush=True)
        except Exception as exc:  # noqa: BLE001
            n_fail += 1
            print(f"IWM pull failed {start_d}..{end_d}: {type(exc).__name__}", flush=True)
    print(f"IWM sessions on disk={n_ok}/{len(sessions)} dir={VIRGIN_IWM}", flush=True)
    return n_ok, n_fail


def _scan_one(item: tuple[str, date]) -> dict:
    sym, d = item
    p = virgin_bar_path(d, sym)
    if not p.exists():
        return {
            "symbol": sym,
            "session_date": d,
            "status": "missing",
            "rows": 0,
            "has_0400": False,
            "first_after_0730": False,
        }
    df = pl.read_parquet(p, columns=["bar_start"])
    n = df.height
    if n == 0:
        return {
            "symbol": sym,
            "session_date": d,
            "status": "empty",
            "rows": 0,
            "has_0400": False,
            "first_after_0730": False,
        }
    times = df["bar_start"].dt.time()
    first = times.min()
    return {
        "symbol": sym,
        "session_date": d,
        "status": "pulled",
        "rows": n,
        "has_0400": bool((times == START_TIME).any()),
        "first_after_0730": first is not None and first > PRE_CUT,
    }


def _write_manifest(elig: pl.DataFrame, workers: int) -> tuple[pl.DataFrame, int, int]:
    pairs = [
        (str(s), d)
        for s, d in elig.filter(pl.col("eligible")).select("symbol", "session_date").iter_rows()
    ]
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for rec in pool.map(_scan_one, pairs, chunksize=32):
            rows.append(rec)
    man = pl.DataFrame(rows)
    VIRGIN_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    man.write_parquet(VIRGIN_MANIFEST)
    n_0400 = int(man["has_0400"].sum()) if man.height else 0
    n_after = int(man["first_after_0730"].sum()) if man.height else 0
    return man, n_0400, n_after


def _write_report(
    *,
    elig: pl.DataFrame,
    man: pl.DataFrame,
    workers: int,
    theta_n: int,
    cpu: int,
    wall_s: float,
    failures: list[dict],
    n_0400: int,
    n_after: int,
    first5_note: str,
    iwm_ok: int,
    iwm_fail: int,
) -> None:
    ok = elig.filter(pl.col("eligible"))
    n_elig = ok.height
    n_sess = ok["session_date"].n_unique()
    n_rows = int(man["rows"].sum()) if man.height else 0
    n_pulled = man.filter(pl.col("status") == "pulled").height
    n_empty = man.filter(pl.col("status") == "empty").height
    n_miss = man.filter(pl.col("status") == "missing").height
    mean_bars = n_rows / n_elig if n_elig else 0.0
    n_10m = int(ok.filter(pl.col("pdv_ge_10m")).height) if "pdv_ge_10m" in ok.columns else 0
    n_gt50 = int(ok.filter(pl.col("prior_close") > 50).height)
    warm = virgin_warmup_sessions()
    study = virgin_study_sessions()
    iwm_disk = len(list(VIRGIN_IWM.glob("*.parquet"))) if VIRGIN_IWM.exists() else 0
    lines = [
        "Arrow 41 — virgin 04:00-16:00 1-minute tape (ingest, not a book)",
        "No fills. No $200 verdict. Did not score engines. Did not touch data/full or Lab A data/bars. No Arrow 42.",
        f"venue={VENUE} interval={INTERVAL} window=04:00-16:00ET last_bar=15:59",
        "eligibility: common stock + ETP denylist, prior_close [$1, $80], prior DV >= $1M, "
        "$10M is a filter column not an ingest wall, no 400 cap",
        f"warmup n={len(warm)} {warm[0]}..{warm[-1]} (last 10 NYSE 2025; not scored)",
        f"study n={len(study)} {study[0]}..{study[-1]} (first 2026 session through last full May; all of January in study)",
        f"workers={workers} theta_concurrency={theta_n} cpu_count={cpu}",
        f"output bars={VIRGIN_BARS} eligibility={VIRGIN_ELIGIBILITY} manifest={VIRGIN_MANIFEST} iwm={VIRGIN_IWM}",
        "",
        f"sessions_attempted={n_sess}",
        f"name_days_eligible={n_elig}",
        f"unique_symbols={ok['symbol'].n_unique()}",
        f"1m_rows={n_rows}",
        f"mean_bars_per_name_day={mean_bars:.1f}",
        f"name_days_pdv_ge_10m={n_10m}",
        f"name_days_prior_close_gt_50={n_gt50}",
        f"manifest pulled={n_pulled} empty={n_empty} missing={n_miss}",
        f"failures={len(failures)}",
        f"iwm_sessions_on_disk={iwm_disk} iwm_ok={iwm_ok} iwm_fail={iwm_fail}",
        f"wall_s={wall_s:.1f} wall_min={wall_s / 60:.1f}",
        first5_note,
        f"name_days_with_04:00_print={n_0400}",
        f"name_days_first_print_after_07:30={n_after}",
        "",
    ]
    if failures:
        lines.append("failure sample (up to 20):")
        for rec in failures[:20]:
            lines.append(
                f"  {rec.get('symbol')} {rec.get('error_class')} {rec.get('error_message', '')[:120]}"
            )
    text = "\n".join(lines) + "\n"
    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / "tape41_ingest.txt"
    out.write_text(text, encoding="utf-8")
    print(text, flush=True)
    print(f"wrote {out}", flush=True)


def run_arrow41(*, workers: int | None = None, theta_concurrency: int = 8, force: bool = False) -> int:
    _assert_virgin_tree()
    ensure_virgin_dirs()
    cpu = os.cpu_count() or 1
    workers = max(1, workers or min(8, cpu))
    theta_n = max(1, min(8, int(theta_concurrency)))
    t0 = time.monotonic()
    warm = virgin_warmup_sessions()
    study = virgin_study_sessions()
    first5 = study[:5]
    rest = list(warm) + study[5:]
    print(
        f"ingest start mode=arrow41 span=warmup:{warm[0]}..{warm[-1]} "
        f"study={study[0]}..{study[-1]} endpoint=stock_history_ohlc interval={INTERVAL} "
        f"venue={VENUE} window=04:00-16:00ET workers={workers} "
        f"theta_concurrency={theta_n} cpu_count={cpu} output={VIRGIN_BARS} "
        f"do_not_touch=data/full,data/bars no_arrow_42",
        flush=True,
    )
    if not SYMBOLS.exists():
        raise FileNotFoundError(f"missing {SYMBOLS}; reuse Lab A common list, do not overwrite")
    symbols = pl.read_parquet(SYMBOLS)["symbol"].to_list()
    print(f"commons={len(symbols)} from {SYMBOLS} (read-only)", flush=True)
    client = get_shared_client()
    limiter = ThetaLimiter(theta_n)

    eod, eod_fail = pull_eod(client, limiter, symbols, workers, force)
    elig = build_virgin_eligibility(eod, symbols)

    print("pull IWM 04:00-16:00 into data/virgin/bench (not data/full/bench)", flush=True)
    iwm_ok, iwm_fail = pull_iwm(client=client, limiter=limiter, force=force)

    jobs5 = _jobs_for(elig, first5)
    print(f"phase 1: first 5 study sessions {first5[0]}..{first5[-1]} jobs={len(jobs5)}", flush=True)
    t1 = time.monotonic()
    rows5, ok5, fail5, fail_a = _run_jobs(
        jobs5, client=client, limiter=limiter, workers=workers, force=force, job_name="virgin_first5"
    )
    elapsed5 = time.monotonic() - t1
    n5 = elig.filter(pl.col("eligible") & pl.col("session_date").is_in(first5)).height
    remain_nd = elig.filter(pl.col("eligible") & pl.col("session_date").is_in(rest)).height
    eta_s = (elapsed5 / n5 * remain_nd) if n5 else 0.0
    first5_note = (
        f"after_first_5_study_sessions elapsed_s={elapsed5:.1f} name_days={n5} rows={rows5} "
        f"remaining_name_days={remain_nd} eta_min={eta_s / 60:.1f} (estimate)"
    )
    print(first5_note, flush=True)

    jobs_rest = _jobs_for(elig, rest)
    print(f"phase 2: remaining warmup+study jobs={len(jobs_rest)}", flush=True)
    rows_r, ok_r, fail_r, fail_b = _run_jobs(
        jobs_rest, client=client, limiter=limiter, workers=workers, force=force, job_name="virgin_rest"
    )
    failures = eod_fail + fail_a + fail_b
    print(
        f"pull done rows={rows5 + rows_r} ok_jobs={ok5 + ok_r} fail_jobs={fail5 + fail_r} "
        f"eod_fail={len(eod_fail)}",
        flush=True,
    )
    print("write manifest + 04:00 stats", flush=True)
    man, n_0400, n_after = _write_manifest(elig, workers)
    wall = time.monotonic() - t0
    _write_report(
        elig=elig,
        man=man,
        workers=workers,
        theta_n=limiter.concurrency,
        cpu=cpu,
        wall_s=wall,
        failures=failures,
        n_0400=n_0400,
        n_after=n_after,
        first5_note=first5_note,
        iwm_ok=iwm_ok,
        iwm_fail=iwm_fail,
    )
    return 0
