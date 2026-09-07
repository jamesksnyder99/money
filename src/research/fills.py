from __future__ import annotations

import math
from datetime import time

import polars as pl

RTH_OPEN = time(9, 30)
RTH_END = time(12, 0)


def is_tradeable(open_: float, close: float, volume: int | float | None) -> bool:
    if volume is None or volume <= 0:
        return False
    if close is None or open_ is None:
        return False
    if not math.isfinite(float(close)) or not math.isfinite(float(open_)):
        return False
    return True


def tradeable_mask(df: pl.DataFrame) -> pl.Expr:
    return (
        (pl.col("volume") > 0)
        & pl.col("close").is_finite()
        & pl.col("open").is_finite()
        & pl.col("high").is_finite()
        & pl.col("low").is_finite()
    )


def next_tradeable_row(df: pl.DataFrame, after_idx: int) -> int | None:
    """Index of the next tradeable bar strictly after after_idx, or None."""
    n = df.height
    opens = df["open"].to_list()
    closes = df["close"].to_list()
    vols = df["volume"].to_list()
    for j in range(after_idx + 1, n):
        if is_tradeable(opens[j], closes[j], vols[j]):
            return j
    return None
