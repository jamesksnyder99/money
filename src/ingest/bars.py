from __future__ import annotations

from datetime import date, time
from zoneinfo import ZoneInfo

import polars as pl

from ingest.calendar import SESSION_OPEN, WINDOW_END, WARMUP_SESSIONS

ET = ZoneInfo("America/New_York")
RTH_OPEN = time(9, 30)


def normalize_ohlc(df: pl.DataFrame, symbol: str, is_warmup: bool) -> pl.DataFrame:
    if df is None or df.height == 0:
        return _empty()
    cols = {c.lower(): c for c in df.columns}
    ts_name = None
    for key in ("timestamp", "datetime", "bar_start", "time"):
        if key in cols:
            ts_name = cols[key]
            break
    if ts_name is None:
        raise ValueError(f"OHLC missing timestamp: {df.columns}")

    def pick(*names: str) -> pl.Expr:
        for n in names:
            if n in cols:
                return pl.col(cols[n])
        return pl.lit(None)

    out = df.select(
        pl.lit(symbol).alias("symbol"),
        pl.col(ts_name).alias("bar_start"),
        pick("open").cast(pl.Float64).alias("open"),
        pick("high").cast(pl.Float64).alias("high"),
        pick("low").cast(pl.Float64).alias("low"),
        pick("close").cast(pl.Float64).alias("close"),
        pick("volume").cast(pl.Int64).alias("volume"),
        pick("count").cast(pl.Int64).alias("count"),
        pick("vwap").cast(pl.Float64).alias("vwap"),
    )
    dtype = out.schema["bar_start"]
    if isinstance(dtype, pl.Datetime) and dtype.time_zone is None:
        out = out.with_columns(pl.col("bar_start").dt.replace_time_zone("UTC"))
    out = out.with_columns(
        pl.col("bar_start").dt.convert_time_zone("America/New_York")
    )
    t = pl.col("bar_start").dt.time()
    out = out.filter((t >= SESSION_OPEN) & (t < WINDOW_END))
    return out.with_columns(
        pl.col("bar_start").dt.date().alias("session_date"),
        pl.when(t < RTH_OPEN).then(pl.lit("pre")).otherwise(pl.lit("rth")).alias("session"),
        pl.lit(is_warmup).alias("is_warmup"),
    )


def _empty() -> pl.DataFrame:
    return pl.DataFrame(
        schema={
            "symbol": pl.String,
            "bar_start": pl.Datetime("us", "America/New_York"),
            "open": pl.Float64,
            "high": pl.Float64,
            "low": pl.Float64,
            "close": pl.Float64,
            "volume": pl.Int64,
            "count": pl.Int64,
            "vwap": pl.Float64,
            "session_date": pl.Date,
            "session": pl.String,
            "is_warmup": pl.Boolean,
        }
    )


def split_sessions(df: pl.DataFrame, keep: set[date]) -> dict[date, pl.DataFrame]:
    if df.height == 0:
        return {}
    out: dict[date, pl.DataFrame] = {}
    for key, part in df.group_by("session_date"):
        d = key[0] if isinstance(key, tuple) else key
        if d in keep:
            out[d] = part
    return out


def warmup_keep(dates: list[date]) -> set[date]:
    allowed = set(WARMUP_SESSIONS)
    return {d for d in dates if d in allowed}
