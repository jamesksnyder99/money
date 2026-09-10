"""Reusable IS/OOS clock split for Arrow 43 onward.

Odd calendar months are in-sample (IS). Even calendar months are
out-of-sample (OOS). Split on the entry session, not the exit.
Combined study calendar is virgin Jan–May 2026 plus full Jun–Aug 2026.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import polars as pl

from ingest.calendar import VIRGIN_STUDY_END, study_sessions, virgin_study_sessions
from ingest.paths import FULL_BARS, VIRGIN_BARS, safe_symbol_filename

IS_MONTHS = frozenset({1, 3, 5, 7, 9, 11})
OOS_MONTHS = frozenset({2, 4, 6, 8, 10, 12})


def combined_study_sessions() -> list[date]:
    """Virgin study then full study. No overlapping dates. No warmup fills."""
    return list(virgin_study_sessions()) + list(study_sessions())


def is_is_session(d: date) -> bool:
    return d.month in IS_MONTHS


def is_oos_session(d: date) -> bool:
    return d.month in OOS_MONTHS


def entry_split(d: date) -> str:
    """IS or OOS from the entry session month."""
    if is_is_session(d):
        return "IS"
    if is_oos_session(d):
        return "OOS"
    raise ValueError(f"session {d} is neither IS nor OOS")


def split_is_oos(sessions: list[date] | None = None) -> tuple[list[date], list[date]]:
    sess = list(sessions) if sessions is not None else combined_study_sessions()
    return [d for d in sess if is_is_session(d)], [d for d in sess if is_oos_session(d)]


def tape_name(d: date) -> str:
    if d <= VIRGIN_STUDY_END:
        return "virgin"
    return "full"


def tape_root(d: date) -> Path:
    if d <= VIRGIN_STUDY_END:
        return VIRGIN_BARS
    return FULL_BARS


def session_bar_path(d: date, symbol: str) -> Path:
    iso = d.isoformat()
    return tape_root(d) / iso / f"{safe_symbol_filename(symbol)}.parquet"


def next_session(d: date, sessions: list[date] | None = None) -> date | None:
    sess = sessions if sessions is not None else combined_study_sessions()
    for x in sess:
        if x > d:
            return x
    return None


def clock_frame(sessions: list[date] | None = None) -> pl.DataFrame:
    sess = list(sessions) if sessions is not None else combined_study_sessions()
    return pl.DataFrame(
        {
            "session_date": sess,
            "split": [entry_split(d) for d in sess],
            "tape": [tape_name(d) for d in sess],
        }
    )
