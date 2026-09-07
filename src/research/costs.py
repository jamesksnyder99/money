from __future__ import annotations

import math

ACCOUNT = 100_000.0
RISK_PER_IDEA = 200.0
MAX_NOTIONAL_FRAC = 0.10
ADV_NOTIONAL_FRAC = 0.02
COMMISSION_PER_SHARE = 0.005
MAX_POSITIONS = 5
MAX_ENTRIES = 10
MAX_RISK_OUTSTANDING = 1_000.0
FAILURE_LINE = 200.0
TARGET_LO = 300.0
TARGET_HI = 500.0


def spread_proxy(price: float) -> float:
    """One-side spread when no quote: max($0.01, 0.10% of price)."""
    if not math.isfinite(price) or price <= 0:
        return 0.01
    return max(0.01, 0.001 * price)


def cost_per_share(price: float) -> float:
    return COMMISSION_PER_SHARE + spread_proxy(price)


def round_trip_cost(shares: int, entry_px: float, exit_px: float) -> float:
    return float(shares) * (cost_per_share(entry_px) + cost_per_share(exit_px))


def position_shares(stop_distance: float, price: float, prior_dollar_volume: float) -> int:
    if not math.isfinite(stop_distance) or stop_distance < 0.01:
        return 0
    if not math.isfinite(price) or price <= 0:
        return 0
    raw = RISK_PER_IDEA / stop_distance
    cap_notional = min(MAX_NOTIONAL_FRAC * ACCOUNT, ADV_NOTIONAL_FRAC * max(prior_dollar_volume, 0.0))
    cap_shares = cap_notional / price if cap_notional > 0 else 0.0
    shares = math.floor(min(raw, cap_shares))
    return shares if shares >= 1 else 0


def signed_pnl(side: int, shares: int, entry_px: float, exit_px: float) -> float:
    gross = side * (exit_px - entry_px) * shares
    return gross - round_trip_cost(shares, entry_px, exit_px)
