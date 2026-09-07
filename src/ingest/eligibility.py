from __future__ import annotations

from datetime import date

import polars as pl

from ingest.calendar import WARMUP_SESSIONS, prior_session

MIN_CLOSE = 1.00
MAX_CLOSE = 30.00
MIN_DOLLAR_VOLUME = 1_000_000.0


def eod_session_dates(df: pl.DataFrame) -> pl.DataFrame:
    cols = df.columns
    if "created" in cols:
        stamp = pl.col("created")
    elif "last_trade" in cols:
        stamp = pl.col("last_trade")
    elif "date" in cols:
        out = df.with_columns(pl.col("date").cast(pl.Date).alias("eod_date"))
        return out
    else:
        raise ValueError(f"EOD frame missing date column: {cols}")
    return df.with_columns(stamp.dt.date().alias("eod_date"))


def evaluate_session(
    eod: pl.DataFrame,
    session: date,
    *,
    is_warmup: bool,
    prior: date | None = None,
) -> pl.DataFrame:
    """Point-in-time eligibility for session D using official EOD of D-1."""
    prior = prior or prior_session(session)
    if prior >= session:
        raise ValueError(f"prior {prior} must be before session {session}")
    day = eod.filter(pl.col("eod_date") == prior)
    close_col = "close" if "close" in day.columns else day.columns[-1]
    vol_col = "volume" if "volume" in day.columns else None
    if vol_col is None:
        raise ValueError("EOD frame missing volume")

    out = day.select(
        pl.lit(session).alias("session_date"),
        pl.col("symbol").cast(pl.String),
        pl.col(close_col).cast(pl.Float64).alias("prior_close"),
        pl.col(vol_col).cast(pl.Int64).alias("prior_volume"),
    ).with_columns(
        (pl.col("prior_close") * pl.col("prior_volume")).alias("prior_dollar_volume"),
        pl.lit(is_warmup).alias("is_warmup"),
    )

    reason = (
        pl.when(pl.col("prior_close").is_null() | pl.col("prior_volume").is_null())
        .then(pl.lit("no_prior_eod"))
        .when((pl.col("prior_close") < MIN_CLOSE) | (pl.col("prior_close") > MAX_CLOSE))
        .then(pl.lit("prior_close_out_of_range"))
        .when(pl.col("prior_dollar_volume") < MIN_DOLLAR_VOLUME)
        .then(pl.lit("prior_dollar_volume_low"))
        .otherwise(pl.lit(""))
    )
    return out.with_columns(
        reason.alias("exclude_reason"),
        (reason == "").alias("eligible"),
    )


def build_warmup_eligibility(
    eod: pl.DataFrame, symbols: list[str] | None = None
) -> pl.DataFrame:
    if symbols is None:
        symbols = (
            eod["symbol"].unique().to_list()
            if eod.height and "symbol" in eod.columns
            else []
        )
    frames = []
    universe = pl.DataFrame({"symbol": symbols})
    for session in WARMUP_SESSIONS:
        day = evaluate_session(eod, session, is_warmup=True)
        base = universe.with_columns(pl.lit(session).alias("session_date"))
        merged = base.join(day, on=["symbol", "session_date"], how="left")
        merged = merged.with_columns(
            pl.col("is_warmup").fill_null(True),
            pl.when(pl.col("exclude_reason").is_null() & pl.col("eligible").is_null())
            .then(pl.lit("no_prior_eod"))
            .otherwise(pl.col("exclude_reason"))
            .alias("exclude_reason"),
        ).with_columns((pl.col("exclude_reason") == "").alias("eligible"))
        frames.append(merged)
    if not frames:
        return pl.DataFrame()
    return pl.concat(frames, how="vertical_relaxed")


def eligible_pairs(elig: pl.DataFrame) -> list[tuple[str, date]]:
    rows = elig.filter(pl.col("eligible")).select("symbol", "session_date")
    return [(str(s), d) for s, d in rows.iter_rows()]
