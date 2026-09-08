from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time

import polars as pl

from research.costs import (
    MAX_ENTRIES,
    MAX_POSITIONS,
    MAX_RISK_OUTSTANDING,
    RISK_PER_IDEA,
    position_shares,
    signed_pnl,
)
from research.fills import is_tradeable
from research.signals import Signal, bar_time, MINUTE_1159

RTH_OPEN = time(9, 30)


@dataclass
class Position:
    symbol: str
    side: int
    shares: int
    entry_px: float
    stop: float
    target: float | None
    entry_ts: datetime
    risk: float
    tag: str
    initial_r: float = 0.0
    trail_armed: bool = False
    favorable_extreme: float = 0.0


@dataclass
class Trade:
    symbol: str
    side: int
    shares: int
    entry_ts: datetime
    exit_ts: datetime
    entry_px: float
    exit_px: float
    pnl: float
    tag: str
    risk: float


@dataclass
class _Arrays:
    ts: list
    open: list
    high: list
    low: list
    close: list
    volume: list
    by_ts: dict


def _pack(df: pl.DataFrame) -> _Arrays:
    ts = df["bar_start"].to_list()
    return _Arrays(
        ts=ts,
        open=df["open"].to_list(),
        high=df["high"].to_list(),
        low=df["low"].to_list(),
        close=df["close"].to_list(),
        volume=df["volume"].to_list(),
        by_ts={t: i for i, t in enumerate(ts)},
    )


def _tradeable(arr: _Arrays, i: int) -> bool:
    return is_tradeable(arr.open[i], arr.close[i], arr.volume[i])


def _next_tradeable(arr: _Arrays, i: int) -> int | None:
    for j in range(i + 1, len(arr.ts)):
        if _tradeable(arr, j):
            return j
    return None


@dataclass
class Book:
    prior_dv: dict[str, float]
    positions: dict[str, Position] = field(default_factory=dict)
    pending_entry: dict[str, tuple[int, Signal]] = field(default_factory=dict)
    pending_exit: dict[str, tuple[int, str]] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)
    entries: int = 0
    risk_out: float = 0.0
    max_positions: int = MAX_POSITIONS
    max_entries: int = MAX_ENTRIES
    take_2r: bool = False
    trail_after_1r: bool = False
    flatten_at: time = MINUTE_1159
    peak_positions: int = 0

    def n_pending_entry(self) -> int:
        return len(self.pending_entry)

    def can_enter(self, symbol: str) -> bool:
        if symbol in self.positions or symbol in self.pending_entry:
            return False
        if len(self.positions) + self.n_pending_entry() >= self.max_positions:
            return False
        if self.entries >= self.max_entries:
            return False
        if self.risk_out + RISK_PER_IDEA > MAX_RISK_OUTSTANDING + 1e-9:
            return False
        return True


def replay_session(
    bars_by_symbol: dict[str, pl.DataFrame],
    signals: list[Signal],
    prior_dv: dict[str, float],
    rth_open_entries: list[Signal] | None = None,
    *,
    take_2r: bool = False,
    trail_after_1r: bool = False,
    flatten_at: time | None = None,
    max_positions: int | None = None,
    max_entries: int | None = None,
) -> list[Trade]:
    packed = {sym: _pack(df) for sym, df in bars_by_symbol.items()}
    book = Book(
        prior_dv=prior_dv,
        take_2r=take_2r,
        trail_after_1r=trail_after_1r,
        flatten_at=flatten_at or MINUTE_1159,
        max_positions=max_positions if max_positions is not None else MAX_POSITIONS,
        max_entries=max_entries if max_entries is not None else MAX_ENTRIES,
    )
    sigs_at: dict = {}
    for sig in signals:
        if sig.overnight:
            continue
        sigs_at.setdefault(sig.signal_ts, []).append(sig)

    if rth_open_entries:
        ranked = sorted(rth_open_entries, key=lambda s: -abs(s.score))
        for sig in ranked:
            if not book.can_enter(sig.symbol):
                continue
            arr = packed.get(sig.symbol)
            if arr is None:
                continue
            idx = None
            for i, t in enumerate(arr.ts):
                if bar_time(t) >= RTH_OPEN and _tradeable(arr, i):
                    idx = i
                    break
            if idx is not None:
                book.pending_entry[sig.symbol] = (idx, sig)

    times = sorted({t for arr in packed.values() for t in arr.ts})
    for ts in times:
        tclock = bar_time(ts)
        # 1) fills at this open
        _fills_at(book, packed, ts)
        if tclock >= book.flatten_at:
            _flatten_open(book, packed, ts)
            continue
        if tclock < RTH_OPEN:
            continue
        # 2) stop/target on this bar H/L → next open; trail at close after +1R
        for pos in list(book.positions.values()):
            arr = packed.get(pos.symbol)
            if arr is None:
                continue
            i = arr.by_ts.get(ts)
            if i is None or not _tradeable(arr, i):
                continue
            if pos.symbol in book.pending_exit:
                continue
            hit, tag = _hit_stop_target(pos, arr.high[i], arr.low[i])
            if hit:
                nxt = _next_tradeable(arr, i)
                if nxt is not None:
                    book.pending_exit[pos.symbol] = (nxt, tag)
                continue
            if book.trail_after_1r:
                _update_trail(pos, arr.high[i], arr.low[i], arr.close[i])
        # 3) new entries from signals at this close
        batch = sigs_at.get(ts, [])
        batch = sorted(batch, key=lambda s: -abs(s.score))
        for sig in batch:
            if not book.can_enter(sig.symbol):
                continue
            arr = packed.get(sig.symbol)
            if arr is None:
                continue
            i = arr.by_ts.get(ts)
            if i is None:
                continue
            nxt = _next_tradeable(arr, i)
            if nxt is None:
                continue
            if bar_time(arr.ts[nxt]) >= book.flatten_at:
                continue
            book.pending_entry[sig.symbol] = (nxt, sig)
    return book.trades


def _fills_at(book: Book, packed: dict[str, _Arrays], ts: datetime) -> None:
    pending = sorted(
        list(book.pending_entry.items()),
        key=lambda kv: -abs(kv[1][1].score),
    )
    for sym, (idx, sig) in pending:
        arr = packed.get(sym)
        if arr is None or arr.ts[idx] != ts:
            continue
        del book.pending_entry[sym]
        if not _tradeable(arr, idx):
            nxt = _next_tradeable(arr, idx)
            if nxt is not None and bar_time(arr.ts[nxt]) < book.flatten_at:
                book.pending_entry[sym] = (nxt, sig)
            continue
        _open_position(book, sig, float(arr.open[idx]), ts)

    for sym, (idx, tag) in list(book.pending_exit.items()):
        arr = packed.get(sym)
        if arr is None or arr.ts[idx] != ts:
            continue
        del book.pending_exit[sym]
        if not _tradeable(arr, idx):
            nxt = _next_tradeable(arr, idx)
            if nxt is not None:
                book.pending_exit[sym] = (nxt, tag)
            continue
        pos = book.positions.get(sym)
        if pos is not None:
            _close_position(book, pos, float(arr.open[idx]), ts, tag)


def _open_position(book: Book, sig: Signal, px: float, ts: datetime) -> None:
    if not book.can_enter(sig.symbol):
        return
    if sig.stop_from_entry:
        dist = max(0.10, 0.01 * px)
        stop = px - sig.side * dist
        stop_dist = abs(px - stop)
        sig = Signal(
            signal_ts=sig.signal_ts,
            symbol=sig.symbol,
            side=sig.side,
            stop=stop,
            target=sig.target,
            score=sig.score,
            tag=sig.tag,
            stop_from_entry=True,
            overnight=sig.overnight,
        )
    else:
        stop_dist = abs(px - sig.stop)
    shares = position_shares(stop_dist, px, book.prior_dv.get(sig.symbol, 0.0))
    if shares < 1:
        return
    risk = min(RISK_PER_IDEA, shares * stop_dist)
    target = sig.target
    if book.take_2r:
        target = px + sig.side * 2.0 * stop_dist
    book.positions[sig.symbol] = Position(
        symbol=sig.symbol,
        side=sig.side,
        shares=shares,
        entry_px=px,
        stop=sig.stop,
        target=target,
        entry_ts=ts,
        risk=risk,
        tag=sig.tag,
        initial_r=stop_dist,
        trail_armed=False,
        favorable_extreme=px,
    )
    book.entries += 1
    book.risk_out += risk
    book.peak_positions = max(book.peak_positions, len(book.positions))


def _close_position(book: Book, pos: Position, px: float, ts: datetime, tag: str) -> None:
    held = book.positions.pop(pos.symbol, None)
    if held is None:
        return
    book.risk_out = max(0.0, book.risk_out - held.risk)
    book.trades.append(
        Trade(
            symbol=held.symbol,
            side=held.side,
            shares=held.shares,
            entry_ts=held.entry_ts,
            exit_ts=ts,
            entry_px=held.entry_px,
            exit_px=px,
            pnl=signed_pnl(held.side, held.shares, held.entry_px, px),
            tag=tag,
            risk=held.risk,
        )
    )


def _update_trail(pos: Position, high: float, low: float, close: float) -> None:
    """After close ≥ +1R, stop to entry; then trail 0.5% from favorable extreme."""
    r = pos.initial_r
    if r <= 0:
        return
    if pos.side > 0:
        pos.favorable_extreme = max(pos.favorable_extreme, high)
        if not pos.trail_armed and close >= pos.entry_px + r - 1e-12:
            pos.trail_armed = True
            pos.stop = pos.entry_px
        if pos.trail_armed:
            pos.stop = max(pos.stop, pos.favorable_extreme * (1.0 - 0.005))
    else:
        pos.favorable_extreme = min(pos.favorable_extreme, low)
        if not pos.trail_armed and close <= pos.entry_px - r + 1e-12:
            pos.trail_armed = True
            pos.stop = pos.entry_px
        if pos.trail_armed:
            pos.stop = min(pos.stop, pos.favorable_extreme * (1.0 + 0.005))


def _hit_stop_target(pos: Position, high: float, low: float) -> tuple[bool, str]:
    if pos.side > 0:
        if low <= pos.stop:
            return True, "stop"
        if pos.target is not None and high >= pos.target:
            return True, "target"
    else:
        if high >= pos.stop:
            return True, "stop"
        if pos.target is not None and low <= pos.target:
            return True, "target"
    return False, ""


def _flatten_open(book: Book, packed: dict[str, _Arrays], ts: datetime) -> None:
    for pos in list(book.positions.values()):
        arr = packed.get(pos.symbol)
        if arr is None:
            continue
        i = arr.by_ts.get(ts)
        if i is None or not _tradeable(arr, i):
            continue
        _close_position(book, pos, float(arr.open[i]), ts, "time")
    book.pending_entry.clear()
