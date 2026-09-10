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
    round_trip_cost,
    signed_pnl,
)
from research.harness import cost_gate_blocks, harness_stop_px
from research.fills import is_tradeable
from research.signals import Signal, bar_time, MINUTE_1159, MINUTE_1559

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
    atr: float = 0.0
    already_scaled: bool = False
    orig_shares: int = 0
    unarmed_red_checked: bool = False


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


def session_low_at_or_before(arr: _Arrays, ts: datetime) -> float | None:
    lo = None
    for i, t in enumerate(arr.ts):
        if t > ts:
            break
        if _tradeable(arr, i):
            lo = float(arr.low[i]) if lo is None else min(lo, float(arr.low[i]))
    return lo


def ssr_active(
    session_low: float | None,
    prior_close: float | None,
    *,
    prior_session_low: float | None = None,
    prior_session_prior_close: float | None = None,
) -> bool:
    """R1: session low ≤ 0.90×prior_close, or the prior session tripped the same rule."""
    if (
        session_low is not None
        and prior_close is not None
        and float(prior_close) > 0
        and float(session_low) <= SSR_FRAC * float(prior_close) + 1e-12
    ):
        return True
    if (
        prior_session_low is not None
        and prior_session_prior_close is not None
        and float(prior_session_prior_close) > 0
        and float(prior_session_low) <= SSR_FRAC * float(prior_session_prior_close) + 1e-12
    ):
        return True
    return False


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


def _ssr_now(
    sig: Signal,
    arr: _Arrays | None,
    prior_close: float | None,
    prior_session_low: float | None,
    prior_session_prior_close: float | None,
) -> bool:
    lo = session_low_at_or_before(arr, sig.signal_ts) if arr is not None else None
    return ssr_active(
        lo,
        prior_close,
        prior_session_low=prior_session_low,
        prior_session_prior_close=prior_session_prior_close,
    )


def _effective_ssr_policy(ssr_policy: str, ssr_filter: bool) -> str:
    if ssr_policy:
        return ssr_policy
    return "reject" if ssr_filter else "off"


def _short_blocked(
    sig: Signal,
    arr: _Arrays | None,
    prior_close: float | None,
    prior_dv: float,
    *,
    ssr_filter: bool,
    borrow_filter: bool,
    ssr_policy: str = "",
    prior_session_low: float | None = None,
    prior_session_prior_close: float | None = None,
) -> bool:
    if sig.side != -1:
        return False
    policy = _effective_ssr_policy(ssr_policy, ssr_filter)
    if policy == "reject" and _ssr_now(
        sig, arr, prior_close, prior_session_low, prior_session_prior_close
    ):
        return True
    if arr is None:
        return False
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
    take_r: float = 0.0
    scale_half_at_1r: bool = False
    atr_trail: bool = False
    harness_stop: bool = False
    cost_gate: bool = False
    use_structure_stop: bool = True
    cost_skips: int = 0
    pending_scale: dict[str, tuple[int, int]] = field(default_factory=dict)
    hold_plus_r: float = 0.0
    late_flatten_at: time = MINUTE_1559
    ssr_filter: bool = False
    ssr_policy: str = ""
    ssr_uptick_minutes: int = 10
    ssr_fill_cap: float = 0.0
    prior_session_low: dict[str, float] = field(default_factory=dict)
    prior_session_prior_close: dict[str, float] = field(default_factory=dict)
    ssr_at_signal: dict[str, bool] = field(default_factory=dict)
    ssr_nofill: int = 0
    n_short_signals: int = 0
    n_ssr_signals: int = 0
    last_entry_at: time = MINUTE_1159
    crossed_at_creation: int = 0
    liquidation_requested: int = 0
    liquidation_filled: int = 0
    unresolved_flatten: int = 0
    flatten_backdate_avoided: int = 0
    trail_atr_mult: float = 1.0
    trail_arm_r: float = 1.0
    unarmed_red_minutes: float = 0.0
    unarmed_red_exits: int = 0

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
    last_entry_at: time | None = None,
    max_positions: int | None = None,
    max_entries: int | None = None,
    max_risk_outstanding: float | None = None,
    prior_close: dict[str, float] | None = None,
    ssr_filter: bool = False,
    borrow_filter: bool = False,
    min_stop_frac: float = 0.0,
    morning_dv: dict[str, float] | None = None,
    allow_premarket: bool = False,
    take_r: float = 0.0,
    scale_half_at_1r: bool = False,
    atr_trail: bool = False,
    harness_stop: bool = False,
    cost_gate: bool = False,
    use_structure_stop: bool = True,
    hold_plus_r: float = 0.0,
    late_flatten_at: time | None = None,
    ssr_policy: str = "",
    ssr_uptick_minutes: int = 10,
    trail_atr_mult: float = 1.0,
    trail_arm_r: float = 1.0,
    unarmed_red_minutes: float = 0.0,
    ssr_fill_cap: float = 0.0,
    prior_session_low: dict[str, float] | None = None,
    prior_session_prior_close: dict[str, float] | None = None,
    stats: dict | None = None,
) -> list[Trade]:
    packed = {sym: _pack(df) for sym, df in bars_by_symbol.items()}
    book = Book(
        prior_dv=prior_dv,
        take_2r=take_2r,
        trail_after_1r=trail_after_1r,
        flatten_at=flatten_at or MINUTE_1159,
        last_entry_at=last_entry_at if last_entry_at is not None else (flatten_at or MINUTE_1159),
        max_positions=max_positions if max_positions is not None else MAX_POSITIONS,
        max_entries=max_entries if max_entries is not None else MAX_ENTRIES,
        max_risk_outstanding=(
            max_risk_outstanding if max_risk_outstanding is not None else MAX_RISK_OUTSTANDING
        ),
        min_stop_frac=float(min_stop_frac or 0.0),
        morning_dv=dict(morning_dv or {}),
        allow_premarket=bool(allow_premarket),
        take_r=2.0 if take_2r else float(take_r or 0.0),
        scale_half_at_1r=bool(scale_half_at_1r),
        atr_trail=bool(atr_trail),
        harness_stop=bool(harness_stop),
        cost_gate=bool(cost_gate),
        use_structure_stop=bool(use_structure_stop),
        hold_plus_r=float(hold_plus_r or 0.0),
        late_flatten_at=late_flatten_at or MINUTE_1559,
        ssr_filter=bool(ssr_filter),
        ssr_policy=str(ssr_policy or ""),
        ssr_uptick_minutes=int(ssr_uptick_minutes or 10),
        trail_atr_mult=float(trail_atr_mult if trail_atr_mult is not None else 1.0),
        trail_arm_r=float(trail_arm_r if trail_arm_r is not None else 1.0),
        unarmed_red_minutes=float(unarmed_red_minutes or 0.0),
        ssr_fill_cap=float(ssr_fill_cap or 0.0),
        prior_session_low=dict(prior_session_low or {}),
        prior_session_prior_close=dict(prior_session_prior_close or {}),
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
                ssr_policy=book.ssr_policy,
                prior_session_low=book.prior_session_low.get(sig.symbol),
                prior_session_prior_close=book.prior_session_prior_close.get(sig.symbol),
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
    early_cut_done = False
    flatten_requested = False
    for ts in times:
        tclock = bar_time(ts)
        # 1) fills at this open
        _fills_at(book, packed, ts)
        holding_late = (
            book.hold_plus_r > 0
            and tclock >= book.flatten_at
            and tclock < book.late_flatten_at
        )
        if tclock >= book.flatten_at and not holding_late:
            if not flatten_requested:
                clock = book.late_flatten_at if book.hold_plus_r > 0 else book.flatten_at
                _request_time_exit(book, packed, ts, clock)
                flatten_requested = True
            continue
        if holding_late:
            if not early_cut_done:
                _conditional_hold_cut(book, packed, ts)
                early_cut_done = True
        elif tclock < RTH_OPEN and not book.allow_premarket:
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
            if book.trail_after_1r or book.atr_trail or book.scale_half_at_1r:
                crossed = _update_trail(pos, arr.high[i], arr.low[i], arr.close[i], book)
                if crossed and pos.symbol not in book.pending_exit:
                    nxt = _next_tradeable(arr, i)
                    if nxt is not None:
                        book.pending_exit[pos.symbol] = (nxt, "trail_cross")
                        book.crossed_at_creation += 1
            if (
                book.unarmed_red_minutes > 0
                and not pos.trail_armed
                and not pos.unarmed_red_checked
                and pos.symbol not in book.pending_exit
            ):
                elapsed = (ts - pos.entry_ts).total_seconds() / 60.0
                if elapsed + 1e-12 >= book.unarmed_red_minutes:
                    pos.unarmed_red_checked = True
                    px = float(arr.close[i])
                    net = signed_pnl(pos.side, pos.shares, pos.entry_px, px) - round_trip_cost(
                        pos.shares, pos.entry_px, px
                    )
                    if net < 0:
                        nxt = _next_tradeable(arr, i)
                        if nxt is not None:
                            book.pending_exit[pos.symbol] = (nxt, "unarmed_red")
                            book.unarmed_red_exits += 1
            if (
                book.scale_half_at_1r
                and not pos.already_scaled
                and pos.symbol not in book.pending_exit
                and pos.symbol not in book.pending_scale
            ):
                r = pos.initial_r
                armed = (
                    (pos.side > 0 and arr.close[i] >= pos.entry_px + r - 1e-12)
                    or (pos.side < 0 and arr.close[i] <= pos.entry_px - r + 1e-12)
                )
                if armed:
                    pos.trail_armed = True
                    pos.stop = pos.entry_px
                    if pos.shares >= 2:
                        nxt = _next_tradeable(arr, i)
                        if nxt is not None:
                            book.pending_scale[pos.symbol] = (nxt, pos.shares // 2)
                    pos.already_scaled = True
        # 3) new entries from signals at this close (A3: last_entry_at, not flatten_at)
        if tclock >= book.last_entry_at:
            continue
        batch = sigs_at.get(ts, [])
        batch = sorted(batch, key=lambda s: -abs(s.score))
        for sig in batch:
            arr = packed.get(sig.symbol)
            pc = (prior_close or {}).get(sig.symbol)
            if sig.side == -1:
                book.n_short_signals += 1
                active = _ssr_now(
                    sig,
                    arr,
                    pc,
                    book.prior_session_low.get(sig.symbol),
                    book.prior_session_prior_close.get(sig.symbol),
                )
                if active:
                    book.n_ssr_signals += 1
                book.ssr_at_signal[sig.symbol] = active
            if _short_blocked(
                sig,
                arr,
                pc,
                book.prior_dv.get(sig.symbol, 0.0),
                ssr_filter=ssr_filter,
                borrow_filter=borrow_filter,
                ssr_policy=book.ssr_policy,
                prior_session_low=book.prior_session_low.get(sig.symbol),
                prior_session_prior_close=book.prior_session_prior_close.get(sig.symbol),
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
            if bar_time(arr.ts[nxt]) >= book.last_entry_at:
                continue
            book.pending_entry[sig.symbol] = (nxt, sig)
    _flatten_leftovers(book, packed, times)
    if stats is not None:
        stats["cost_skips"] = book.cost_skips
        stats["ssr_nofill"] = book.ssr_nofill
        stats["n_short_signals"] = book.n_short_signals
        stats["n_ssr_signals"] = book.n_ssr_signals
        stats["crossed_at_creation"] = book.crossed_at_creation
        stats["liquidation_requested"] = book.liquidation_requested
        stats["liquidation_filled"] = book.liquidation_filled
        stats["unresolved_flatten"] = book.unresolved_flatten
        stats["flatten_backdate_avoided"] = book.flatten_backdate_avoided
        stats["unarmed_red_exits"] = book.unarmed_red_exits
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
            if nxt is not None and bar_time(arr.ts[nxt]) < book.last_entry_at:
                book.pending_entry[sym] = (nxt, sig)
            continue
        policy = _effective_ssr_policy(book.ssr_policy, book.ssr_filter)
        if (
            policy == "uptick"
            and sig.side == -1
            and book.ssr_at_signal.get(sym)
            and not _uptick_ok(book, arr, idx, sig)
        ):
            nxt = _next_tradeable(arr, idx)
            if (
                nxt is not None
                and bar_time(arr.ts[nxt]) < book.last_entry_at
                and _within_uptick_window(book, arr.ts[nxt], sig)
            ):
                book.pending_entry[sym] = (nxt, sig)
            else:
                book.ssr_nofill += 1
            continue
        _open_position(book, sig, float(arr.open[idx]), ts)

    for sym, (idx, nclose) in list(book.pending_scale.items()):
        arr = packed.get(sym)
        if arr is None or arr.ts[idx] != ts:
            continue
        del book.pending_scale[sym]
        if not _tradeable(arr, idx):
            nxt = _next_tradeable(arr, idx)
            if nxt is not None:
                book.pending_scale[sym] = (nxt, nclose)
            continue
        pos = book.positions.get(sym)
        if pos is not None:
            _scale_position(book, pos, int(nclose), float(arr.open[idx]), ts)

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
            if tag == "time":
                book.liquidation_filled += 1


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
        if book.harness_stop:
            stop, stop_dist = harness_stop_px(
                px,
                sig.stop,
                float(sig.atr or 0.0),
                sig.side,
                use_structure=book.use_structure_stop,
            )
            sig = Signal(
                signal_ts=sig.signal_ts,
                symbol=sig.symbol,
                side=sig.side,
                stop=stop,
                target=sig.target,
                score=sig.score,
                tag=sig.tag,
                stop_from_entry=sig.stop_from_entry,
                overnight=sig.overnight,
                atr=sig.atr,
            )
    if px > 0 and book.min_stop_frac > 0 and stop_dist / px < book.min_stop_frac - 1e-12:
        return
    if book.cost_gate and cost_gate_blocks(px, stop_dist):
        book.cost_skips += 1
        return
    mdv = book.morning_dv.get(sig.symbol) if book.morning_dv else None
    shares = position_shares(stop_dist, px, book.prior_dv.get(sig.symbol, 0.0), morning_dv=mdv)
    if shares < 1:
        return
    risk = min(RISK_PER_IDEA, shares * stop_dist)
    target = sig.target
    if book.take_r > 0:
        target = px + sig.side * book.take_r * stop_dist
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
        atr=float(sig.atr or 0.0),
        already_scaled=False,
        orig_shares=shares,
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


def _stop_through_close(pos: Position, close: float) -> bool:
    if pos.side > 0:
        return float(close) <= pos.stop + 1e-12
    return float(close) >= pos.stop - 1e-12


def _update_trail(pos: Position, high: float, low: float, close: float, book: Book | None = None) -> bool:
    """After close ≥ +1R, stop to entry; then trail 0.5% or ATR from favorable extreme.

    Returns True when a ratchet leaves the new stop already through the current close (A4).
    Does not switch to a rolling ATR manager.
    """
    r = pos.initial_r
    if r <= 0:
        return False
    atr_mode = bool(book.atr_trail) if book is not None else False
    arm_r = float(book.trail_arm_r) if book is not None else 1.0
    if arm_r <= 0:
        arm_r = 1.0
    atr_mult = float(book.trail_atr_mult) if book is not None else 1.0
    if atr_mult <= 0:
        atr_mult = 1.0
    width = pos.atr * atr_mult
    prev_stop = pos.stop
    if pos.side > 0:
        pos.favorable_extreme = max(pos.favorable_extreme, high)
        if not pos.trail_armed and close >= pos.entry_px + arm_r * r - 1e-12:
            pos.trail_armed = True
            pos.stop = pos.entry_px
        if pos.trail_armed:
            if atr_mode and pos.atr > 0:
                pos.stop = max(pos.stop, pos.favorable_extreme - width)
            else:
                pos.stop = max(pos.stop, pos.favorable_extreme * (1.0 - 0.005))
    else:
        pos.favorable_extreme = min(pos.favorable_extreme, low)
        if not pos.trail_armed and close <= pos.entry_px - arm_r * r + 1e-12:
            pos.trail_armed = True
            pos.stop = pos.entry_px
        if pos.trail_armed:
            if atr_mode and pos.atr > 0:
                pos.stop = min(pos.stop, pos.favorable_extreme + width)
            else:
                pos.stop = min(pos.stop, pos.favorable_extreme * (1.0 + 0.005))
    if not pos.trail_armed:
        return False
    if abs(pos.stop - prev_stop) <= 1e-12:
        return False
    return _stop_through_close(pos, close)


def _scale_position(book: Book, pos: Position, nclose: int, px: float, ts: datetime) -> None:
    nclose = min(int(nclose), pos.shares)
    if nclose < 1:
        return
    closed_risk = pos.risk * (nclose / pos.shares) if pos.shares else 0.0
    book.trades.append(
        Trade(
            symbol=pos.symbol,
            side=pos.side,
            shares=nclose,
            entry_ts=pos.entry_ts,
            exit_ts=ts,
            entry_px=pos.entry_px,
            exit_px=px,
            pnl=signed_pnl(pos.side, nclose, pos.entry_px, px),
            tag="scale",
            risk=closed_risk,
        )
    )
    pos.shares -= nclose
    pos.risk = max(0.0, pos.risk - closed_risk)
    book.risk_out = max(0.0, book.risk_out - closed_risk)
    pos.stop = pos.entry_px
    pos.trail_armed = True
    pos.already_scaled = True
    if pos.shares < 1:
        book.positions.pop(pos.symbol, None)


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


def _first_tradeable_clock_at_or_after(
    arr: _Arrays, clock: time, after_ts: datetime
) -> int | None:
    """First tradeable bar with bar_time >= clock and ts >= after_ts. Never looks backward."""
    for i, t in enumerate(arr.ts):
        if t < after_ts:
            continue
        if bar_time(t) < clock:
            continue
        if _tradeable(arr, i):
            return i
    return None


def _had_tradeable_before_clock(arr: _Arrays, clock: time, after_ts: datetime) -> bool:
    for i, t in enumerate(arr.ts):
        if t < after_ts:
            continue
        if bar_time(t) >= clock:
            break
        if _tradeable(arr, i):
            return True
    return False


def _flatten_one(
    book: Book,
    packed: dict[str, _Arrays],
    pos: Position,
    flatten_ts: datetime | None,
    clock: time | None = None,
) -> None:
    """A5: fill at or after flatten clock. Never backdate to an earlier print."""
    arr = packed.get(pos.symbol)
    book.liquidation_requested += 1
    if arr is None:
        book.unresolved_flatten += 1
        _close_position(book, pos, pos.entry_px, pos.entry_ts, "unresolved")
        return
    clock = clock or book.flatten_at
    idx = _first_tradeable_clock_at_or_after(arr, clock, pos.entry_ts)
    if idx is None:
        if _had_tradeable_before_clock(arr, clock, pos.entry_ts):
            book.flatten_backdate_avoided += 1
        book.unresolved_flatten += 1
        _close_position(book, pos, pos.entry_px, pos.entry_ts, "unresolved")
        return
    if flatten_ts is not None and arr.ts[idx] < flatten_ts and bar_time(arr.ts[idx]) < clock:
        # should not happen; belt-and-suspenders against backdate
        if _had_tradeable_before_clock(arr, clock, pos.entry_ts):
            book.flatten_backdate_avoided += 1
        book.unresolved_flatten += 1
        _close_position(book, pos, pos.entry_px, pos.entry_ts, "unresolved")
        return
    _close_position(book, pos, float(arr.open[idx]), arr.ts[idx], "time")
    book.liquidation_filled += 1


def _request_time_exit(
    book: Book, packed: dict[str, _Arrays], now_ts: datetime, clock: time | None = None
) -> None:
    """A5: queue flatten at first own-tape tradeable at or after `clock`. No backdate."""
    clock = clock or book.flatten_at
    for pos in list(book.positions.values()):
        if pos.symbol in book.pending_exit:
            continue
        book.liquidation_requested += 1
        arr = packed.get(pos.symbol)
        if arr is None:
            book.unresolved_flatten += 1
            _close_position(book, pos, pos.entry_px, pos.entry_ts, "unresolved")
            continue
        idx = _first_tradeable_clock_at_or_after(arr, clock, pos.entry_ts)
        if idx is None:
            if _had_tradeable_before_clock(arr, clock, pos.entry_ts):
                book.flatten_backdate_avoided += 1
            book.unresolved_flatten += 1
            _close_position(book, pos, pos.entry_px, pos.entry_ts, "unresolved")
            continue
        if arr.ts[idx] == now_ts:
            _close_position(book, pos, float(arr.open[idx]), now_ts, "time")
            book.liquidation_filled += 1
        else:
            book.pending_exit[pos.symbol] = (idx, "time")
    book.pending_entry.clear()
    book.pending_scale.clear()


def _flatten_open(book: Book, packed: dict[str, _Arrays], ts: datetime) -> None:
    _request_time_exit(book, packed, ts)
    book.pending_scale.clear()


def _within_uptick_window(book: Book, fill_ts: datetime, sig: Signal) -> bool:
    return (fill_ts - sig.signal_ts).total_seconds() <= book.ssr_uptick_minutes * 60.0 + 1e-9


def _prior_bar_close(arr: _Arrays, i: int) -> float | None:
    for j in range(i - 1, -1, -1):
        if _tradeable(arr, j):
            return float(arr.close[j])
    return None


def _uptick_ok(book: Book, arr: _Arrays, idx: int, sig: Signal) -> bool:
    if not _within_uptick_window(book, arr.ts[idx], sig):
        return False
    prev_c = _prior_bar_close(arr, idx)
    o = float(arr.open[idx])
    if prev_c is None or o <= prev_c + 1e-12:
        return False
    if book.ssr_fill_cap > 0:
        i_sig = arr.by_ts.get(sig.signal_ts)
        if i_sig is None:
            return False
        sig_close = float(arr.close[i_sig])
        if o > sig_close * (1.0 + book.ssr_fill_cap) + 1e-12:
            return False
    return True


def _unrealized_r(pos: Position, px: float) -> float:
    if pos.initial_r <= 1e-12:
        return 0.0
    return pos.side * (px - pos.entry_px) / pos.initial_r


def _conditional_hold_cut(book: Book, packed: dict[str, _Arrays], ts: datetime) -> None:
    """Keep names ≥ hold_plus_r at the early flatten open; flatten the rest."""
    for pos in list(book.positions.values()):
        arr = packed.get(pos.symbol)
        if arr is None:
            _flatten_one(book, packed, pos, ts)
            continue
        i = arr.by_ts.get(ts)
        if i is None or not _tradeable(arr, i):
            _flatten_one(book, packed, pos, ts)
            continue
        if _unrealized_r(pos, float(arr.open[i])) >= book.hold_plus_r - 1e-12:
            continue
        _flatten_one(book, packed, pos, ts)
    book.pending_entry.clear()


def _flatten_leftovers(book: Book, packed: dict[str, _Arrays], times: list) -> None:
    """Fill remaining pending time-exits; unresolved if no event at or after flatten clock."""
    clock = book.late_flatten_at if book.hold_plus_r > 0 else book.flatten_at
    # leftovers keep the session's true flatten clock (late if a hold-plus-R book)
    flatten_ts = None
    for t in times:
        if bar_time(t) >= clock:
            flatten_ts = t
            break
    if book.pending_exit:
        # last chance: fill pending time exits whose bar exists
        if times:
            _fills_at(book, packed, times[-1])
        for sym, (idx, tag) in list(book.pending_exit.items()):
            arr = packed.get(sym)
            pos = book.positions.get(sym)
            if pos is None or arr is None:
                book.pending_exit.pop(sym, None)
                continue
            if idx < len(arr.ts) and _tradeable(arr, idx) and bar_time(arr.ts[idx]) >= clock:
                _close_position(book, pos, float(arr.open[idx]), arr.ts[idx], tag)
                if tag == "time":
                    book.liquidation_filled += 1
            book.pending_exit.pop(sym, None)
    if book.positions:
        for pos in list(book.positions.values()):
            _flatten_one(book, packed, pos, flatten_ts, clock=clock)
        book.pending_entry.clear()
        book.pending_exit.clear()
    if book.positions:
        for pos in list(book.positions.values()):
            book.unresolved_flatten += 1
            _close_position(book, pos, pos.entry_px, pos.entry_ts, "unresolved")


def daily_close_drawdown(daily: list[float]) -> float:
    """Old maxDD on the daily-close equity series. Renamed for A7."""
    peak = 0.0
    eq = 0.0
    max_dd = 0.0
    for x in daily:
        eq += x
        peak = max(peak, eq)
        max_dd = min(max_dd, eq - peak)
    return max_dd


def _trade_ts(tr, key: str):
    if hasattr(tr, key):
        return getattr(tr, key)
    return tr[key]


def _trade_field(tr, key: str, default=None):
    if hasattr(tr, key):
        return getattr(tr, key)
    return tr.get(key, default) if isinstance(tr, dict) else default


def marked_equity_session(
    trades: list,
    bars_by_symbol: dict[str, pl.DataFrame],
    *,
    start_equity: float = 0.0,
) -> dict:
    """1-min marked-to-market equity for one session's trades.

    Returns daily_close_pnl (session total), intraday_peak_to_trough (min of eq-peak
    on the 1-min curve), and the last mark.
    """
    if not trades:
        return {
            "daily_close_pnl": 0.0,
            "intraday_peak_to_trough": 0.0,
            "n_marks": 0,
            "end_equity": start_equity,
        }
    packed = {}
    for sym, df in bars_by_symbol.items():
        if df is None or df.height == 0:
            continue
        packed[sym] = _pack(df)
    times = sorted({t for arr in packed.values() for t in arr.ts})
    open_pos: dict[str, list] = {}
    realized = 0.0
    last_close: dict[str, float] = {}
    peak = start_equity
    trough_dd = 0.0
    n_marks = 0
    eq = start_equity
    by_entry = {}
    for tr in trades:
        by_entry.setdefault(_trade_field(tr, "symbol"), []).append(tr)
    pending_open = []
    pending_close = []
    for tr in trades:
        pending_open.append((_trade_ts(tr, "entry_ts"), tr, 1))
        pending_close.append((_trade_ts(tr, "exit_ts"), tr, -1))
    events = pending_open + pending_close
    events.sort(key=lambda x: (x[0], x[2]))
    ei = 0
    for ts in times:
        while ei < len(events) and events[ei][0] <= ts:
            _, tr, d = events[ei]
            sym = _trade_field(tr, "symbol")
            if d > 0:
                open_pos.setdefault(sym, []).append(tr)
            else:
                bag = open_pos.get(sym) or []
                keep = []
                closed = False
                for p in bag:
                    if not closed and p is tr:
                        realized += float(_trade_field(tr, "pnl") or 0.0)
                        closed = True
                    else:
                        keep.append(p)
                open_pos[sym] = keep
            ei += 1
        for sym, arr in packed.items():
            i = arr.by_ts.get(ts)
            if i is not None and _tradeable(arr, i):
                last_close[sym] = float(arr.close[i])
        unreal = 0.0
        for sym, bag in open_pos.items():
            px = last_close.get(sym)
            if px is None:
                continue
            for tr in bag:
                side = int(_trade_field(tr, "side") or 0)
                shares = int(_trade_field(tr, "shares") or 0)
                entry = float(_trade_field(tr, "entry_px") or 0.0)
                unreal += side * shares * (px - entry)
        eq = start_equity + realized + unreal
        peak = max(peak, eq)
        trough_dd = min(trough_dd, eq - peak)
        n_marks += 1
    daily_close_pnl = sum(float(_trade_field(t, "pnl") or 0.0) for t in trades)
    return {
        "daily_close_pnl": daily_close_pnl,
        "intraday_peak_to_trough": trough_dd,
        "n_marks": n_marks,
        "end_equity": start_equity + daily_close_pnl,
    }


def mfe_capture(trades: list) -> float:
    """realised / sum(max(0, MFE_R) × risk). 0 if the denominator is empty."""
    realised = 0.0
    denom = 0.0
    for t in trades:
        realised += float(_trade_field(t, "pnl") or 0.0)
        mfe_r = _trade_field(t, "mfe_r")
        if mfe_r is None:
            mfe_r = _trade_field(t, "mfe_R")
        risk = float(_trade_field(t, "risk") or 0.0)
        denom += max(0.0, float(mfe_r or 0.0)) * risk
    if denom <= 1e-12:
        return 0.0
    return realised / denom


def joint_peak_risk(*trade_lists: list) -> float:
    """Peak concurrent outstanding risk across books. Missing book is 0, not dropped."""
    ev = []
    for trades in trade_lists:
        for t in trades or []:
            risk = float(_trade_field(t, "risk") or 0.0)
            ev.append((_trade_ts(t, "entry_ts"), risk))
            ev.append((_trade_ts(t, "exit_ts"), -risk))
    if not ev:
        return 0.0
    ev.sort(key=lambda x: (x[0], x[1]))
    run = 0.0
    peak = 0.0
    for _, d in ev:
        run += d
        peak = max(peak, run)
    return peak
