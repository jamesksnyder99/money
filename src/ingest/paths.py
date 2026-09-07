from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
REPORTS = REPO_ROOT / "reports"
CALENDAR = DATA / "calendar" / "sessions.parquet"
ELIGIBILITY = DATA / "universe" / "eligibility.parquet"
SPLITS = DATA / "ref" / "splits.parquet"
SYMBOLS = DATA / "ref" / "symbols_common.parquet"
EOD_DIR = DATA / "eod" / "warmup"
BARS_DIR = DATA / "bars" / "ohlc_1m"
MANIFEST = DATA / "manifests" / "pulls.jsonl"
INGEST_REPORT = REPORTS / "ingest_latest.txt"
ARROW01_REPORT = REPORTS / "arrow01_timing.txt"


def ensure_dirs() -> None:
    for path in (
        CALENDAR.parent,
        ELIGIBILITY.parent,
        SPLITS.parent,
        EOD_DIR,
        BARS_DIR,
        MANIFEST.parent,
        REPORTS,
        DATA / "tmp",
    ):
        path.mkdir(parents=True, exist_ok=True)


# Windows reserved device names (CON, PRN, AUX, ...) cannot be filenames.
_WIN_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def safe_symbol_filename(symbol: str) -> str:
    stem = symbol.split(".")[0].upper()
    if stem in _WIN_RESERVED:
        return f"_{symbol}"
    return symbol


def bar_path(session_date, symbol: str) -> Path:
    return BARS_DIR / f"session_date={session_date.isoformat()}" / f"{safe_symbol_filename(symbol)}.parquet"


def eod_path(symbol: str) -> Path:
    return EOD_DIR / f"{safe_symbol_filename(symbol)}.parquet"
