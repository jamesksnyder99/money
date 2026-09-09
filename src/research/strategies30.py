from __future__ import annotations

from datetime import datetime, timedelta

import polars as pl

from research.fills import is_tradeable
from research.harness import STOP_FLOOR_FRAC, atr_last6_5m
from research.signals import MINUTE_0945, RTH_OPEN, bar_time
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


HARVEST_MIN_VOL = 2000


def harvestable_altitude(
    pack: dict | None,
    confirm_ts: datetime | None,
    prior_close: float | None,
    r1: float,
) -> dict:
    """C-R7: altitude from the first fillable bar after confirm+5m.

    RTH launches harvest from RTH; premarket launches from 09:45.
    Fillable = tradeable open/close and volume ≥ 2000.
    """
    out = {
        "harvest_ts": None,
        "harvestable": 0.0,
        "max_high": None,
    }
    if pack is None or confirm_ts is None or prior_close is None or float(prior_close) <= 0:
        return out
    launch_pre = bar_time(confirm_ts) < RTH_OPEN
    earliest = confirm_ts + timedelta(minutes=5)
    if launch_pre:
        floor_clock = MINUTE_0945
    else:
        floor_clock = RTH_OPEN
    times = pack["ts"]
    opens = pack["open"]
    highs = pack["high"]
    closes = pack["close"]
    vols = pack["vol"]
    harvest_i = None
    for i, ts in enumerate(times):
        if ts < earliest:
            continue
        if bar_time(ts) < floor_clock:
            continue
        if not is_tradeable(opens[i], closes[i], vols[i]):
            continue
        if float(vols[i] or 0.0) < HARVEST_MIN_VOL - 1e-12:
            continue
        harvest_i = i
        break
    if harvest_i is None:
        return out
    mh = None
    for i in range(harvest_i, len(times)):
        h = float(highs[i])
        mh = h if mh is None else max(mh, h)
    out["harvest_ts"] = times[harvest_i]
    out["max_high"] = mh
    out["harvestable"] = gross_altitude(mh, prior_close, r1)
    return out
