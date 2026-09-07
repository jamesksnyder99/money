from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time

RTH_OPEN = time(9, 30)
MINUTE_0934 = time(9, 34)
MINUTE_0935 = time(9, 35)
MINUTE_1000 = time(10, 0)
MINUTE_1158 = time(11, 58)
MINUTE_1159 = time(11, 59)


@dataclass(frozen=True, slots=True)
class Signal:
    """Decision at signal_ts close; fill at the next tradeable open."""

    signal_ts: datetime
    symbol: str
    side: int  # +1 long, -1 short
    stop: float
    target: float | None
    score: float  # rank competing signals at the same timestamp
    tag: str


def bar_time(ts: datetime) -> time:
    return ts.timetz().replace(tzinfo=None) if ts.tzinfo else ts.time()
