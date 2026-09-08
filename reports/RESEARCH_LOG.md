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

## 2026-09-07T20:06:40-04:00 — Arrow 4

VERDICT: FAIL — no Arrow 4 track/rule printed ≥ $200/day net on holdout

Tracks: A = existing Lab A bars with prior_close [10,30] and ADV>=$5M; B = [10,50] ADV>=$5M commons not ETP, cap top 400/day because raw >800.
Rules only: cash; OR-break after 09:45 of 09:30-09:44 range; next-open swing; open_drive Y=2.0 frozen; vwap_reclaim min_price=$10 frozen. No gap-fade. No Arrow 3 grids.

What died:
- Track A or_break param=None: holdout $-169.07/day develop $-200.34/day trades_holdout=97. Do not retry this exact (track, rule, frozen param) without a new costed reason.
- Track A swing param=None: holdout $-266.41/day develop $-35.38/day trades_holdout=97. Do not retry this exact (track, rule, frozen param) without a new costed reason.
- Track A open_drive param=2.0: holdout $47.19/day develop $-45.59/day trades_holdout=104. Do not retry this exact (track, rule, frozen param) without a new costed reason.
- Track A vwap_reclaim param=10.0: holdout $-380.62/day develop $-80.19/day trades_holdout=189. Do not retry this exact (track, rule, frozen param) without a new costed reason.
- Track B or_break param=None: holdout $-148.21/day develop $-80.68/day trades_holdout=133. Do not retry this exact (track, rule, frozen param) without a new costed reason.
- Track B swing param=None: holdout $-53.74/day develop $-94.93/day trades_holdout=105. Do not retry this exact (track, rule, frozen param) without a new costed reason.
- Track B open_drive param=2.0: holdout $-123.79/day develop $4.80/day trades_holdout=109. Do not retry this exact (track, rule, frozen param) without a new costed reason.
- Track B vwap_reclaim param=10.0: holdout $-265.95/day develop $-62.21/day trades_holdout=202. Do not retry this exact (track, rule, frozen param) without a new costed reason.

Do not retry: Arrow 3 gap-fade {3,5,8} / open-drive grid / vwap {3,5,8} on the ~2000-name $1–$30 book.

## 2026-09-07T20:43:34-04:00 — Arrow 5

VERDICT: HOLD OUT CLEARS $200 — B/down_day_then_trend

Ten frozen trend-with rules on Track A ($10-30, ADV>=$5M) and Track B ($10-50, 400/day cap). Trend = 10 prior official EOD closes. Flat = no trade. Did not fade the 10-session trend. Did not rebuild gap-fade, open-drive, VWAP reclaim, 15-min OR-break, or Arrow 4 +1.5% swing.

What died:
- Track A trend_open: holdout $-273.19/day develop $-100.77/day trades_holdout=106. Do not retry this exact (track, rule) without a new costed reason.
- Track A trend_pullback: holdout $-482.95/day develop $-108.66/day trades_holdout=218. Do not retry this exact (track, rule) without a new costed reason.
- Track A yday_level_break: holdout $-94.72/day develop $-65.27/day trades_holdout=135. Do not retry this exact (track, rule) without a new costed reason.
- Track A gap_with_trend: holdout $62.45/day develop $-133.56/day trades_holdout=105. Do not retry this exact (track, rule) without a new costed reason.
- Track A compression_expansion: holdout $-75.47/day develop $-35.26/day trades_holdout=39. Do not retry this exact (track, rule) without a new costed reason.
- Track A rs_vs_book: holdout $-138.78/day develop $-330.44/day trades_holdout=109. Do not retry this exact (track, rule) without a new costed reason.
- Track A down_day_then_trend: holdout $26.06/day develop $-37.20/day trades_holdout=108. Do not retry this exact (track, rule) without a new costed reason.
- Track A adv_expanding: holdout $-227.25/day develop $-478.10/day trades_holdout=184. Do not retry this exact (track, rule) without a new costed reason.
- Track A late_with_trend: holdout $-89.64/day develop $-34.18/day trades_holdout=103. Do not retry this exact (track, rule) without a new costed reason.
- Track A channel_position: holdout $11.36/day develop $13.37/day trades_holdout=98. Do not retry this exact (track, rule) without a new costed reason.
- Track B trend_open: holdout $-176.28/day develop $-36.37/day trades_holdout=107. Do not retry this exact (track, rule) without a new costed reason.
- Track B trend_pullback: holdout $-338.69/day develop $27.33/day trades_holdout=217. Do not retry this exact (track, rule) without a new costed reason.
- Track B yday_level_break: holdout $-138.70/day develop $-60.91/day trades_holdout=149. Do not retry this exact (track, rule) without a new costed reason.
- Track B gap_with_trend: holdout $-331.52/day develop $-8.48/day trades_holdout=104. Do not retry this exact (track, rule) without a new costed reason.
- Track B compression_expansion: holdout $-15.93/day develop $-24.32/day trades_holdout=23. Do not retry this exact (track, rule) without a new costed reason.
- Track B rs_vs_book: holdout $-255.99/day develop $-130.63/day trades_holdout=110. Do not retry this exact (track, rule) without a new costed reason.
- Track B adv_expanding: holdout $-180.43/day develop $-128.13/day trades_holdout=196. Do not retry this exact (track, rule) without a new costed reason.
- Track B late_with_trend: holdout $-57.81/day develop $7.92/day trades_holdout=108. Do not retry this exact (track, rule) without a new costed reason.
- Track B channel_position: holdout $-14.64/day develop $34.32/day trades_holdout=104. Do not retry this exact (track, rule) without a new costed reason.

Cleared: B/down_day_then_trend

