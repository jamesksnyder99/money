# Research log

## 2026-09-07T19:41:48-04:00 — Arrow 3

VERDICT: FAIL — no named rule printed ≥ $200/day net on holdout

Tried (only these): cash; gap-fade X in {3,5,8}; open-drive Y in {1.5,2.0,3.0}; RTH VWAP reclaim min-price in {3,5,8}. Parameters picked on develop $/day only; holdout once.

Nothing cleared the $200 holdout line.

What died:
- gap_fade (param 3.0): holdout $-446.50/day, develop $-134.86/day, trades_holdout=105. Do not retry this exact grid without a new costed reason.
- open_drive (param 1.5): holdout $-187.46/day, develop $-254.10/day, trades_holdout=105. Do not retry this exact grid without a new costed reason.
- vwap_reclaim (param 8.0): holdout $-342.01/day, develop $-111.01/day, trades_holdout=178. Do not retry this exact grid without a new costed reason.

Do not retry in Arrow 3: extra indicators, ML, MACD, extra setups, peeking holdout.

