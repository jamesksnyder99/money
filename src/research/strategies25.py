from __future__ import annotations

from datetime import time

import polars as pl

from research.harness import attach_atr
from research.signals import RTH_OPEN, Signal, bar_time
from research.strategies15 import candle_anatomy, resample_5m
from research.strategies23 import _long_ok

FLUSH_UNDERCUT = 0.02
FLY_ORW_MIN = 0.051
FLY_DV0929_MIN = 98_000.0
FLY_EXT0944_MIN = 0.034
PX5 = 5.0


def fly_cell_ok(orw: float | None, dv0929: float | None, ext0944: float | None) -> bool:
    """Arrow 24 develop-locked FLY cell. Holdout did not pick these cuts."""
    if orw is None or dv0929 is None or ext0944 is None:
        return False
    return (
        float(orw) >= FLY_ORW_MIN - 1e-12
        and float(dv0929) >= FLY_DV0929_MIN - 1e-9
        and float(ext0944) >= FLY_EXT0944_MIN - 1e-12
    )


def flush_ring_long(
    bars: pl.DataFrame,
    last_px_0800: float | None,
    *,
    min_undercut: float = FLUSH_UNDERCUT,
    max_undercut: float | None = None,
    min_close_loc: float = 0.75,
    reclaim_0800: bool = False,
    flush_after: time | None = None,
    tag: str = "flush_ring",
) -> list[Signal]:
    """Flush then higher-low. Optional depth, reclaim, and first-flush clock cuts."""
    if last_px_0800 is None or last_px_0800 <= 0:
        return []
    px = float(last_px_0800)
    thresh = px * (1.0 - min_undercut)
    floor = px * (1.0 - max_undercut) if max_undercut is not None else None
    bars5 = resample_5m(bars)
    flushed = False
    flush_low = None
    prev = None
    for b in bars5:
        if bar_time(b["start"]) < RTH_OPEN:
            prev = b
            continue
        already = flushed
        if b["low"] <= thresh + 1e-12:
            if not flushed:
                if flush_after is not None and bar_time(b["start"]) < flush_after:
                    return []
                flushed = True
                flush_low = b["low"]
            else:
                flush_low = min(flush_low, b["low"])
        if floor is not None and flush_low is not None and flush_low < floor - 1e-12:
            return []
        if (
            already
            and flushed
            and flush_low is not None
            and prev is not None
            and bar_time(prev["start"]) >= RTH_OPEN
            and b["low"] > prev["low"] + 1e-12
        ):
            a = candle_anatomy(b["open"], b["high"], b["low"], b["close"])
            if a is None or a["close_loc"] < min_close_loc - 1e-12:
                prev = b
                continue
            if reclaim_0800 and b["close"] < px - 1e-12:
                prev = b
                continue
            stop = float(flush_low)
            if _long_ok(b["close"], stop):
                sig = Signal(
                    b["last_ts"],
                    b["symbol"],
                    1,
                    stop,
                    None,
                    b["close"] - stop,
                    tag,
                )
                return [attach_atr(sig, bars)]
        prev = b
    return []


def score_flush(sig: Signal, score: float) -> Signal:
    return Signal(
        signal_ts=sig.signal_ts,
        symbol=sig.symbol,
        side=sig.side,
        stop=sig.stop,
        target=sig.target,
        score=float(score),
        tag=sig.tag,
        stop_from_entry=sig.stop_from_entry,
        overnight=sig.overnight,
        atr=sig.atr,
    )
