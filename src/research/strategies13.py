from __future__ import annotations

import math
from datetime import datetime, timedelta

import polars as pl

from research.ema15 import ema9_at
from research.fills import is_tradeable, rth_session_vwap, tradeable_mask
from research.signals import MINUTE_0945, RTH_OPEN, Signal, bar_time
from research.strategies8 import _t, _tradeable, opening_range


def long_gap_pop(
    dv_rank: float,
    gap: float | None,
    *,
    dv_min: float = 0.80,
    gap_min: float = 0.015,
) -> bool:
    """Q5 gap-up population. Not a flipped short kernel."""
    if dv_rank < dv_min - 1e-12:
        return False
    if gap is None or gap <= 0:
        return False
    return gap >= gap_min - 1e-12


def quiet_open_pop(
    dv_rank: float,
    gap: float | None,
    or_w: float | None,
    *,
    dv_min: float = 0.80,
    gap_max: float = 0.005,
    or_w_lo: float = 0.01,
    or_w_hi: float = 0.04,
) -> bool:
    """Q5, |gap| < 0.5%, OR width in [1%, 4%]."""
    if dv_rank < dv_min - 1e-12:
        return False
    if gap is None or abs(gap) >= gap_max - 1e-12:
        return False
    if or_w is None or or_w < or_w_lo - 1e-12 or or_w > or_w_hi + 1e-12:
        return False
    return True


def resample_5m_ohlc(df: pl.DataFrame) -> list[dict]:
    """Current-session 5-min bars: start, high, low, close, last_ts, symbol."""
    if df.height == 0:
        return []
    ok = df.filter(tradeable_mask(df)).sort("bar_start")
    if ok.height == 0:
        return []
    ok = ok.with_columns(pl.col("bar_start").dt.truncate("5m").alias("b5"))
    g = (
        ok.group_by("b5")
        .agg(
            pl.col("high").max().alias("high"),
            pl.col("low").min().alias("low"),
            pl.col("close").sort_by("bar_start").last().alias("close"),
            pl.col("bar_start").sort_by("bar_start").last().alias("last_ts"),
            pl.col("symbol").first().alias("symbol"),
        )
        .sort("b5")
    )
    out: list[dict] = []
    for rec in g.iter_rows(named=True):
        out.append(
            {
                "start": rec["b5"],
                "high": float(rec["high"]),
                "low": float(rec["low"]),
                "close": float(rec["close"]),
                "last_ts": rec["last_ts"],
                "symbol": str(rec["symbol"]),
            }
        )
    return out


def five_min_close_below_ema9(
    bars: pl.DataFrame,
    stitched: list[tuple[datetime, float]],
    or_high: float,
) -> list[Signal]:
    """After 09:45, first completed 5-min close below ema9. Shorts only. Not an OR-low break."""
    bars5 = resample_5m_ohlc(bars)
    delta = timedelta(minutes=5)
    for b in bars5:
        if bar_time(b["start"]) < MINUTE_0945:
            continue
        ema9 = ema9_at(stitched, b["start"] + delta)
        if ema9 is None:
            continue
        if b["close"] < ema9:
            stop = max(or_high, b["high"])
            return [
                Signal(
                    b["last_ts"],
                    b["symbol"],
                    -1,
                    stop,
                    None,
                    ema9 - b["close"],
                    "c5_ema9_short",
                )
            ]
    return []


def pullback_or_mid_ema9(
    bars: pl.DataFrame, stitched: list[tuple[datetime, float]]
) -> list[Signal]:
    """After 09:45, low tags OR mid or ema9 and close back above that level. Longs only."""
    rng = opening_range(bars)
    if rng is None:
        return []
    hi, lo, _w = rng
    mid = (hi + lo) / 2.0
    df = _t(_tradeable(bars)).sort("bar_start")
    later = df.filter(pl.col("t") >= MINUTE_0945)
    for rec in later.iter_rows(named=True):
        low = float(rec["low"])
        close = float(rec["close"])
        ema9 = ema9_at(stitched, rec["bar_start"])
        levels: list[float] = []
        if low <= mid and close > mid:
            levels.append(mid)
        if ema9 is not None and low <= ema9 and close > ema9:
            levels.append(ema9)
        if not levels:
            continue
        stop = low
        if stop >= close:
            continue
        return [
            Signal(
                rec["bar_start"],
                str(rec["symbol"]),
                1,
                stop,
                None,
                close - stop,
                "pb_mid_ema9",
            )
        ]
    return []


def vwap_reclaim_long(bars: pl.DataFrame) -> list[Signal]:
    """At least one RTH close below RTH VWAP, then first later close back above. Longs only."""
    df = bars.sort("bar_start")
    if df.height == 0:
        return []
    vw = rth_session_vwap(df)
    times = df["bar_start"].to_list()
    opens = df["open"].to_list()
    closes = df["close"].to_list()
    vols = df["volume"].to_list()
    lost = False
    for i in range(df.height):
        t = bar_time(times[i])
        if t < RTH_OPEN:
            continue
        if not is_tradeable(opens[i], closes[i], vols[i]):
            continue
        c = float(closes[i])
        v = vw[i]
        if not math.isfinite(v):
            continue
        if not lost:
            if c < v:
                lost = True
            continue
        if c > v:
            return [
                Signal(
                    times[i],
                    str(df["symbol"][i]),
                    1,
                    v,
                    None,
                    c - v,
                    "vwap_reclaim_long",
                )
            ]
    return []
