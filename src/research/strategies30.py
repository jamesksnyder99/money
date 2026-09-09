from __future__ import annotations

from datetime import datetime

import polars as pl

from research.harness import STOP_FLOOR_FRAC, atr_last6_5m
from research.strategies15 import resample_5m


def r1_haircut(bars: pl.DataFrame, launch_ts: datetime, prior_close: float) -> float:
    """1R as a fraction of sea level (prior close). <6 completed 5-min bars → 0.6%."""
    if prior_close is None or float(prior_close) <= 0:
        return STOP_FLOOR_FRAC
    bars5 = resample_5m(bars)
    done = [b for b in bars5 if b["last_ts"] <= launch_ts]
    if len(done) < 6:
        return STOP_FLOOR_FRAC
    atr = atr_last6_5m(bars, launch_ts)
    if atr <= 0:
        return STOP_FLOOR_FRAC
    return max(float(atr) / float(prior_close), STOP_FLOOR_FRAC)


def gross_altitude(max_high: float | None, prior_close: float | None, r1: float) -> float:
    """max(0, (max_high/prior_close − 1) − r1). Depths below sea do not subtract."""
    if max_high is None or prior_close is None or float(prior_close) <= 0:
        return 0.0
    ext = float(max_high) / float(prior_close) - 1.0
    return max(0.0, ext - float(r1))
