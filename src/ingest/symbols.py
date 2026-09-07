from __future__ import annotations

import re

# Primary-listed common: 1–5 letters, optional single-letter share class (BRK.B).
# Drops preferreds (.PR), warrants (.WS/.WT/.W), units (.U/.UN), rights (.RT),
# when-issued (/WI, .WI), and leading-dot Theta junk (.PR.I.PR.A).
_COMMON = re.compile(r"^[A-Z]{1,5}(\.[A-Z])?$")


def is_common_stock_ticker(symbol: str) -> bool:
    if not symbol:
        return False
    text = symbol.strip().upper()
    if "/" in text:
        return False
    if any(token in text for token in (".PR", ".WS", ".WT", ".UN", ".RT", ".WI")):
        return False
    if re.search(r"\.[UW]$", text):
        return False
    return bool(_COMMON.match(text))


def filter_common(symbols: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in symbols:
        sym = str(raw).strip().upper()
        if sym in seen:
            continue
        if is_common_stock_ticker(sym):
            seen.add(sym)
            out.append(sym)
    return out
