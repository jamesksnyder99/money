from __future__ import annotations

import os
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo

import polars as pl
from thetadata.errors import NoDataFoundError

from ingest.bars import normalize_ohlc, split_sessions
from ingest.calendar import (
    EOD_END,
    EOD_START,
    WARMUP_SESSIONS,
    eod_dates_for_warmup,
    sessions_frame,
    study_sessions,
)
from ingest.eligibility import build_warmup_eligibility, eod_session_dates
from ingest.manifest import Manifest
from ingest.paths import (
    BARS_DIR,
    CALENDAR,
    ELIGIBILITY,
    SPLITS,
    SYMBOLS,
    bar_path,
    ensure_dirs,
    eod_path,
)
from ingest.progress import Progress
from ingest.report import write_reports
from ingest.symbols import filter_common
from ingest.theta_pool import ThetaLimiter, call_theta
from ingest.validate import validate_warmup
from theta.client import get_shared_client

ET = ZoneInfo("America/New_York")
VENUE = "utp_cta"
INTERVAL = "1m"
START_TIME = time(7, 30)
END_TIME = time(12, 0)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _banner(*, mode: str, workers: int, theta_concurrency: int, cpu: int) -> None:
    print(
        f"ingest start mode={mode} span=warmup:{WARMUP_SESSIONS[0]}..{WARMUP_SESSIONS[-1]} "
        f"eod={EOD_START}..{EOD_END} endpoint=stock_history_ohlc interval={INTERVAL} "
        f"venue={VENUE} window=07:30-12:00ET workers={workers} "
        f"theta_concurrency={theta_concurrency} cpu_count={cpu} "
        f"output={BARS_DIR}",
        flush=True,
    )


def write_calendar() -> pl.DataFrame:
    ensure_dirs()
    df = sessions_frame()
    df.write_parquet(CALENDAR)
    empty_splits = pl.DataFrame(
        schema={"symbol": pl.String, "ex_date": pl.Date, "factor": pl.Float64}
    )
    empty_splits.write_parquet(SPLITS)
    print(
        f"calendar rows={df.height} warmup={df.filter(pl.col('is_warmup')).height} "
        f"study={df.filter(~pl.col('is_warmup')).height} "
        f"memorial_absent={date(2026, 5, 25) not in set(df['session_date'].to_list())} "
        f"jul3_absent={date(2026, 7, 3) not in set(df['session_date'].to_list())} "
        f"n_study={len(study_sessions())} eod_priors={eod_dates_for_warmup()}",
        flush=True,
    )
    return df


def list_commons(client, limiter: ThetaLimiter, manifest: Manifest, force: bool) -> list[str]:
    if not force and SYMBOLS.exists() and manifest.already_ok(
        endpoint="stock_list_symbols",
        symbol="*",
        start_date="",
        end_date="",
    ):
        df = pl.read_parquet(SYMBOLS)
        symbols = df["symbol"].to_list()
        print(f"LIST resume commons={len(symbols)}", flush=True)
        return symbols
    df, elapsed = call_theta(limiter, client.stock_list_symbols)
    col = "symbol" if "symbol" in df.columns else df.columns[0]
    raw = [str(x) for x in df[col].to_list()]
    commons = filter_common(raw)
    pl.DataFrame({"symbol": commons}).write_parquet(SYMBOLS)
    manifest.append(
        endpoint="stock_list_symbols",
        symbol="*",
        row_count=len(commons),
        elapsed_s=elapsed,
        ok=True,
    )
    print(
        f"LIST raw={len(raw)} commons={len(commons)} elapsed={elapsed:.2f}s "
        f"first5={commons[:5]}",
        flush=True,
    )
    return commons


def _empty_eod(symbol: str) -> pl.DataFrame:
    return pl.DataFrame(
        schema={
            "symbol": pl.String,
            "eod_date": pl.Date,
            "close": pl.Float64,
            "volume": pl.Int64,
        }
    ).with_columns(pl.lit(symbol).alias("symbol"))


def pull_one_eod(client, limiter, manifest, symbol: str, force: bool) -> tuple[str, bool, str, str, float]:
    path = eod_path(symbol)
    start, end = EOD_START.isoformat(), EOD_END.isoformat()
    if (
        not force
        and path.exists()
        and manifest.already_ok(
            endpoint="stock_history_eod",
            symbol=symbol,
            start_date=start,
            end_date=end,
        )
    ):
        return symbol, True, "", "", 0.0
    try:
        df, elapsed = call_theta(
            limiter,
            client.stock_history_eod,
            symbol=symbol,
            start_date=EOD_START,
            end_date=EOD_END,
        )
        if "symbol" not in df.columns:
            df = df.with_columns(pl.lit(symbol).alias("symbol"))
        df = eod_session_dates(df)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(path)
        manifest.append(
            endpoint="stock_history_eod",
            symbol=symbol,
            start_date=start,
            end_date=end,
            row_count=df.height,
            elapsed_s=elapsed,
            ok=True,
        )
        return symbol, True, "", "", elapsed
    except NoDataFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        _empty_eod(symbol).write_parquet(path)
        manifest.append(
            endpoint="stock_history_eod",
            symbol=symbol,
            start_date=start,
            end_date=end,
            row_count=0,
            elapsed_s=0.0,
            ok=True,
        )
        return symbol, True, "", "", 0.0
    except Exception as exc:  # noqa: BLE001
        manifest.append(
            endpoint="stock_history_eod",
            symbol=symbol,
            start_date=start,
            end_date=end,
            ok=False,
            error_class=type(exc).__name__,
            error_message=str(exc)[:500],
        )
        return symbol, False, type(exc).__name__, str(exc)[:500], 0.0


def pull_eod(
    client,
    limiter: ThetaLimiter,
    manifest: Manifest,
    symbols: list[str],
    workers: int,
    force: bool,
) -> tuple[pl.DataFrame, list[dict]]:
    prog = Progress(len(symbols), "eod")
    prog.start_heartbeat()
    failures: list[dict] = []
    print(f"EOD pulling {len(symbols)} commons {EOD_START}..{EOD_END}", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [
            pool.submit(pull_one_eod, client, limiter, manifest, sym, force)
            for sym in symbols
        ]
        for i, fut in enumerate(as_completed(futs), 1):
            symbol, ok, cls, msg, elapsed = fut.result()
            prog.mark(symbol, ok=ok, elapsed_s=elapsed)
            if not ok:
                failures.append(
                    {"symbol": symbol, "session": "eod", "error_class": cls, "error_message": msg}
                )
            if i % 250 == 0:
                prog.heartbeat()
    prog.stop_heartbeat()
    prog.heartbeat()
    files = list(eod_path("x").parent.glob("*.parquet"))
    if not files:
        return pl.DataFrame(), failures
    eod = pl.concat([pl.read_parquet(f) for f in files], how="diagonal_relaxed")
    print(f"EOD loaded rows={eod.height} files={len(files)} fails={len(failures)}", flush=True)
    return eod, failures


def write_eligibility(eod: pl.DataFrame, symbols: list[str]) -> pl.DataFrame:
    elig = build_warmup_eligibility(eod, symbols)
    ELIGIBILITY.parent.mkdir(parents=True, exist_ok=True)
    elig.write_parquet(ELIGIBILITY)
    per = (
        elig.filter(pl.col("eligible"))
        .group_by("session_date")
        .len()
        .sort("session_date")
    )
    print("eligibility per session:", flush=True)
    for row in per.iter_rows(named=True):
        print(f"  {row['session_date']}: {row['len']}", flush=True)
    return elig


def _ohlc_skip(symbol: str, sessions: list[date], manifest: Manifest, force: bool) -> bool:
    if force:
        return False
    if not all(bar_path(d, symbol).exists() for d in sessions):
        return False
    start, end = min(sessions).isoformat(), max(sessions).isoformat()
    return manifest.already_ok(
        endpoint="stock_history_ohlc",
        symbol=symbol,
        start_date=start,
        end_date=end,
        interval=INTERVAL,
        venue=VENUE,
    )


def pull_one_ohlc(
    client,
    limiter,
    manifest,
    symbol: str,
    sessions: list[date],
    force: bool,
) -> tuple[str, int, dict[date, int], bool, str, str, float]:
    sessions = sorted(sessions)
    start_d, end_d = sessions[0], sessions[-1]
    if _ohlc_skip(symbol, sessions, manifest, force):
        rows = {}
        total = 0
        for d in sessions:
            p = bar_path(d, symbol)
            n = pl.read_parquet(p).height if p.exists() else 0
            rows[d] = n
            total += n
        return symbol, total, rows, True, "", "", 0.0
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
        norm = normalize_ohlc(df, symbol, is_warmup=True)
        parts = split_sessions(norm, set(sessions))
        rows: dict[date, int] = {}
        total = 0
        for d in sessions:
            part = parts.get(d)
            path = bar_path(d, symbol)
            path.parent.mkdir(parents=True, exist_ok=True)
            if part is None or part.height == 0:
                normalize_ohlc(pl.DataFrame(), symbol, True).write_parquet(path)
                rows[d] = 0
            else:
                part.write_parquet(path)
                rows[d] = part.height
                total += part.height
        manifest.append(
            endpoint="stock_history_ohlc",
            symbol=symbol,
            start_date=start_d.isoformat(),
            end_date=end_d.isoformat(),
            interval=INTERVAL,
            venue=VENUE,
            row_count=total,
            elapsed_s=elapsed,
            ok=True,
        )
        return symbol, total, rows, True, "", "", elapsed
    except NoDataFoundError:
        for d in sessions:
            path = bar_path(d, symbol)
            path.parent.mkdir(parents=True, exist_ok=True)
            normalize_ohlc(pl.DataFrame(), symbol, True).write_parquet(path)
        manifest.append(
            endpoint="stock_history_ohlc",
            symbol=symbol,
            start_date=start_d.isoformat(),
            end_date=end_d.isoformat(),
            interval=INTERVAL,
            venue=VENUE,
            row_count=0,
            elapsed_s=0.0,
            ok=True,
        )
        return symbol, 0, {d: 0 for d in sessions}, True, "", "", 0.0
    except Exception as exc:  # noqa: BLE001
        manifest.append(
            endpoint="stock_history_ohlc",
            symbol=symbol,
            start_date=start_d.isoformat(),
            end_date=end_d.isoformat(),
            interval=INTERVAL,
            venue=VENUE,
            ok=False,
            error_class=type(exc).__name__,
            error_message=str(exc)[:500],
        )
        return symbol, 0, {}, False, type(exc).__name__, str(exc)[:500], 0.0


def pull_bars(
    client,
    limiter: ThetaLimiter,
    manifest: Manifest,
    elig: pl.DataFrame,
    workers: int,
    force: bool,
) -> tuple[dict[date, int], list[dict], float, int, int]:
    by_sym: dict[str, list[date]] = {}
    for symbol, session in (
        elig.filter(pl.col("eligible")).select("symbol", "session_date").iter_rows()
    ):
        by_sym.setdefault(str(symbol), []).append(session)
    jobs = list(by_sym.items())
    prog = Progress(len(jobs), "ohlc_1m")
    prog.start_heartbeat()
    print(f"BARS {len(jobs)} symbols with ≥1 eligible warmup session", flush=True)
    rows_by_session: dict[date, int] = {d: 0 for d in WARMUP_SESSIONS}
    failures: list[dict] = []
    elapsed_sum = 0.0
    elapsed_n = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [
            pool.submit(pull_one_ohlc, client, limiter, manifest, sym, dates, force)
            for sym, dates in jobs
        ]
        for i, fut in enumerate(as_completed(futs), 1):
            symbol, total, rows, ok, cls, msg, elapsed = fut.result()
            prog.mark(symbol, rows=total, elapsed_s=elapsed, ok=ok)
            if elapsed > 0:
                elapsed_sum += elapsed
                elapsed_n += 1
            if not ok:
                failures.append(
                    {
                        "symbol": symbol,
                        "session": "warmup-batch",
                        "error_class": cls,
                        "error_message": msg,
                    }
                )
            for d, n in rows.items():
                rows_by_session[d] = rows_by_session.get(d, 0) + n
            if i % 100 == 0:
                prog.heartbeat()
    prog.stop_heartbeat()
    prog.heartbeat()
    mean_s = elapsed_sum / elapsed_n if elapsed_n else 0.0
    session_fail = 0
    session_ok = 0
    for d in WARMUP_SESSIONS:
        if rows_by_session.get(d, 0) > 0:
            session_ok += 1
        else:
            session_fail += 1
    return rows_by_session, failures, mean_s, session_ok, session_fail


def run_warmup(*, workers: int, theta_concurrency: int, force: bool) -> int:
    cpu = os.cpu_count() or 1
    workers = max(1, workers)
    started = _now()
    _banner(mode="warmup", workers=workers, theta_concurrency=theta_concurrency, cpu=cpu)
    ensure_dirs()
    limiter = ThetaLimiter(theta_concurrency)
    manifest = Manifest()
    theta_start = limiter.concurrency
    failures: list[dict] = []
    extra_notes: list[str] = []

    try:
        write_calendar()
        client = get_shared_client()
        commons = list_commons(client, limiter, manifest, force)
        eod, eod_fail = pull_eod(client, limiter, manifest, commons, workers, force)
        failures.extend(eod_fail)
        elig = write_eligibility(eod, commons)
        rows_by_session, bar_fail, mean_s, sess_ok, sess_fail = pull_bars(
            client, limiter, manifest, elig, workers, force
        )
        failures.extend(bar_fail)
        issues = validate_warmup()
        extra_notes.extend(issues if issues else ["validation: no issues on warmup checks"])
        if issues:
            print("VALIDATION issues:", flush=True)
            for item in issues:
                print(f"  {item}", flush=True)
        else:
            print("VALIDATION ok", flush=True)
        ended = _now()
        write_reports(
            started=started,
            ended=ended,
            workers=workers,
            theta_concurrency_start=theta_start,
            theta_concurrency_end=limiter.concurrency,
            cpu_count=cpu,
            elig=elig,
            rows_by_session=rows_by_session,
            failures=failures,
            mean_request_s=mean_s,
            sessions_ok=sess_ok,
            sessions_fail=sess_fail,
            extra_notes=extra_notes,
        )
        print(
            f"ingest finish ok={len(failures)==0} duration={(ended-started).total_seconds():.1f}s "
            f"paths={CALENDAR}, {ELIGIBILITY}, {BARS_DIR}",
            flush=True,
        )
        return 0 if not issues else 1
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
        extra_notes.append(f"fatal {type(exc).__name__}: {exc}")
        ended = _now()
        try:
            write_reports(
                started=started,
                ended=ended,
                workers=workers,
                theta_concurrency_start=theta_start,
                theta_concurrency_end=limiter.concurrency,
                cpu_count=cpu,
                elig=pl.DataFrame(
                    schema={
                        "session_date": pl.Date,
                        "symbol": pl.String,
                        "prior_close": pl.Float64,
                        "prior_volume": pl.Int64,
                        "prior_dollar_volume": pl.Float64,
                        "eligible": pl.Boolean,
                        "exclude_reason": pl.String,
                        "is_warmup": pl.Boolean,
                    }
                ),
                rows_by_session={},
                failures=failures + [
                    {
                        "symbol": "*",
                        "session": "*",
                        "error_class": type(exc).__name__,
                        "error_message": str(exc)[:500],
                    }
                ],
                mean_request_s=0.0,
                sessions_ok=0,
                sessions_fail=len(WARMUP_SESSIONS),
                extra_notes=extra_notes,
            )
        except Exception:  # noqa: BLE001
            pass
        return 1
