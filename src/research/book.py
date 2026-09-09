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
SSR_FRAC = 0.90
BORROW_GAP = -0.05
BORROW_DV = 10_000_000.0


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


def ssr_blocks_short(last_close: float | None, prior_close: float | None) -> bool:
    """Reg SHO 201 proxy: last close ≤ 90% of prior close. Crude; no uptick model."""
    if last_close is None or prior_close is None or prior_close <= 0:
        return False
    return float(last_close) <= SSR_FRAC * float(prior_close) + 1e-12


def borrow_blocks_short(gap: float | None, prior_dv: float | None) -> bool:
    """Crude HTB proxy: gap ≤ −5% and prior dollar volume < $10M. Not a fee table."""
    if gap is None or prior_dv is None:
        return False
    return float(gap) <= BORROW_GAP + 1e-12 and float(prior_dv) < BORROW_DV - 1e-9


def _last_close_at_or_before(arr: _Arrays, ts: datetime) -> float | None:
    last = None
    for i, t in enumerate(arr.ts):
        if t > ts:
            break
        if _tradeable(arr, i):
            last = float(arr.close[i])
    return last


def _gap_from_arr(arr: _Arrays, prior_close: float | None) -> float | None:
    if prior_close is None or prior_close <= 0:
        return None
    for i, t in enumerate(arr.ts):
        if bar_time(t) < RTH_OPEN:
            continue
        if not _tradeable(arr, i):
            continue
        o = float(arr.open[i])
        if o <= 0:
            return None
        return o / float(prior_close) - 1.0
    return None


def _last_tradeable_at_or_before(arr: _Arrays, ts: datetime, after_ts: datetime) -> int | None:
    best = None
    for i, t in enumerate(arr.ts):
        if t < after_ts:
            continue
        if t > ts:
            break
        if _tradeable(arr, i):
            best = i
    return best


def _last_tradeable_after(arr: _Arrays, after_ts: datetime) -> int | None:
    best = None
    for i, t in enumerate(arr.ts):
        if t < after_ts:
            continue
        if _tradeable(arr, i):
            best = i
    return best


def _short_blocked(
    sig: Signal,
    arr: _Arrays | None,
    prior_close: float | None,
    prior_dv: float,
    *,
    ssr_filter: bool,
    borrow_filter: bool,
) -> bool:
    if sig.side != -1:
        return False
    if arr is None:
        return False
    if ssr_filter and ssr_blocks_short(_last_close_at_or_before(arr, sig.signal_ts), prior_close):
        return True
    if borrow_filter and borrow_blocks_short(_gap_from_arr(arr, prior_close), prior_dv):
        return True
    return False


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
    max_risk_outstanding: float = MAX_RISK_OUTSTANDING
    min_stop_frac: float = 0.0
    morning_dv: dict[str, float] = field(default_factory=dict)
    allow_premarket: bool = False

    def n_pending_entry(self) -> int:
        return len(self.pending_entry)

    def can_enter(self, symbol: str) -> bool:
        if symbol in self.positions or symbol in self.pending_entry:
            return False
        if len(self.positions) + self.n_pending_entry() >= self.max_positions:
            return False
        if self.entries >= self.max_entries:
            return False
        if self.risk_out + RISK_PER_IDEA > self.max_risk_outstanding + 1e-9:
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
    max_risk_outstanding: float | None = None,
    prior_close: dict[str, float] | None = None,
    ssr_filter: bool = False,
    borrow_filter: bool = False,
    min_stop_frac: float = 0.0,
    morning_dv: dict[str, float] | None = None,
    allow_premarket: bool = False,
) -> list[Trade]:
    packed = {sym: _pack(df) for sym, df in bars_by_symbol.items()}
    book = Book(
        prior_dv=prior_dv,
        take_2r=take_2r,
        trail_after_1r=trail_after_1r,
        flatten_at=flatten_at or MINUTE_1159,
        max_positions=max_positions if max_positions is not None else MAX_POSITIONS,
        max_entries=max_entries if max_entries is not None else MAX_ENTRIES,
        max_risk_outstanding=(
            max_risk_outstanding if max_risk_outstanding is not None else MAX_RISK_OUTSTANDING
        ),
        min_stop_frac=float(min_stop_frac or 0.0),
        morning_dv=dict(morning_dv or {}),
        allow_premarket=bool(allow_premarket),
    )
    sigs_at: dict = {}
    for sig in signals:
        if sig.overnight:
            continue
        sigs_at.setdefault(sig.signal_ts, []).append(sig)

    if rth_open_entries:
        ranked = sorted(rth_open_entries, key=lambda s: -abs(s.score))
        for sig in ranked:
            arr = packed.get(sig.symbol)
            if arr is None:
                continue
            pc = (prior_close or {}).get(sig.symbol)
            if _short_blocked(
                sig,
                arr,
                pc,
                book.prior_dv.get(sig.symbol, 0.0),
                ssr_filter=ssr_filter,
                borrow_filter=borrow_filter,
            ):
                continue
            if not book.can_enter(sig.symbol):
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
        if tclock < RTH_OPEN and not book.allow_premarket:
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
            arr = packed.get(sig.symbol)
            pc = (prior_close or {}).get(sig.symbol)
            if _short_blocked(
                sig,
                arr,
                pc,
                book.prior_dv.get(sig.symbol, 0.0),
                ssr_filter=ssr_filter,
                borrow_filter=borrow_filter,
            ):
                continue
            if not book.can_enter(sig.symbol):
                continue
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
    _flatten_leftovers(book, packed, times)
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
        if sig.side > 0 and sig.stop >= px - 1e-12:
            return
        if sig.side < 0 and sig.stop <= px + 1e-12:
            return
        stop_dist = abs(px - sig.stop)
    if px > 0 and book.min_stop_frac > 0 and stop_dist / px < book.min_stop_frac - 1e-12:
        return
    mdv = book.morning_dv.get(sig.symbol) if book.morning_dv else None
    shares = position_shares(stop_dist, px, book.prior_dv.get(sig.symbol, 0.0), morning_dv=mdv)
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


def concurrent_stats(trades: list[Trade]) -> tuple[int, float]:
    """Peak concurrent positions and time-weighted mean from trade entry/exit times."""
    if not trades:
        return 0, 0.0
    ev: list[tuple] = []
    for t in trades:
        ev.append((t.entry_ts, 1))
        ev.append((t.exit_ts, -1))
    ev.sort(key=lambda x: (x[0], x[1]))
    n = 0
    peak = 0
    weighted = 0.0
    dur = 0.0
    prev = None
    prev_n = 0
    for ts, d in ev:
        if prev is not None:
            dt = (ts - prev).total_seconds()
            if dt > 0:
                weighted += prev_n * dt
                dur += dt
        n += d
        peak = max(peak, n)
        prev = ts
        prev_n = n
    mean = weighted / dur if dur else float(peak)
    return peak, mean


def _flatten_one(book: Book, packed: dict[str, _Arrays], pos: Position, flatten_ts: datetime | None) -> None:
    """Close at flatten open if tradeable; else last tradeable at or before flatten after entry."""
    arr = packed.get(pos.symbol)
    if arr is None:
        _close_position(book, pos, pos.entry_px, pos.entry_ts, "orphan_flat")
        return
    if flatten_ts is not None:
        i = arr.by_ts.get(flatten_ts)
        if i is not None and _tradeable(arr, i):
            _close_position(book, pos, float(arr.open[i]), flatten_ts, "time")
            return
        j = _last_tradeable_at_or_before(arr, flatten_ts, pos.entry_ts)
        if j is not None:
            _close_position(book, pos, float(arr.open[j]), arr.ts[j], "time")
            return
    k = _last_tradeable_after(arr, pos.entry_ts)
    if k is not None:
        _close_position(book, pos, float(arr.open[k]), arr.ts[k], "time")
        return
    _close_position(book, pos, pos.entry_px, pos.entry_ts, "orphan_flat")


def _flatten_open(book: Book, packed: dict[str, _Arrays], ts: datetime) -> None:
    for pos in list(book.positions.values()):
        _flatten_one(book, packed, pos, ts)
    book.pending_entry.clear()
    book.pending_exit.clear()


def _flatten_leftovers(book: Book, packed: dict[str, _Arrays], times: list) -> None:
    flatten_ts = None
    for t in times:
        if bar_time(t) >= book.flatten_at:
            flatten_ts = t
            break
    if flatten_ts is None and times:
        flatten_ts = times[-1]
    if book.positions:
        for pos in list(book.positions.values()):
            _flatten_one(book, packed, pos, flatten_ts)
        book.pending_entry.clear()
        book.pending_exit.clear()
    if book.positions:
        for pos in list(book.positions.values()):
            _close_position(book, pos, pos.entry_px, pos.entry_ts, "orphan_flat")
