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

## 2026-09-08T07:51:57-04:00 — Arrow 6

VERDICT: FAIL — no Arrow 6 rule has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass (Arrow 5 B/down_day_then_trend warning).

Tether correction: Arrow 5 chained the 10-session EOD trend onto every mechanism. James's warmup-trend intent is a stance for some variants, not a lock on all of them. Arrow 6 with-trend: trend_open, gap_with_trend, down_day_then_trend, late_with_trend, channel_position (skip flat). Free: session_pullback (renamed from trend_pullback), yday_level_break, compression_expansion (15-min expansion direction), rs_vs_book, adv_expanding (09:30-10:00 session direction). No 10d-trend fade book. No 11th rule.

Engine: Trade.risk stored; avgR = mean(pnl/risk); RTH-only VWAP helper; rth_open_entries sorted by |score| and can_enter before queue; next-open stop fills kept (slippage through stop intended).

Develop-red / holdout-green is not a pass. Arrow 5 B/down_day_then_trend (develop about -$185/day, holdout +$217 on 22 days) is not promoted.

What died (holdout < $200, or holdout green with red develop):
- Track A trend_open (with-trend): holdout $-620.24/day develop $700.06/day trades_holdout=107 avgR=-1.273. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A gap_with_trend (with-trend): holdout $62.45/day develop $-133.56/day trades_holdout=105 avgR=0.416. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A down_day_then_trend (with-trend): holdout $26.06/day develop $-37.20/day trades_holdout=108 avgR=0.055. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A late_with_trend (with-trend): holdout $-89.64/day develop $-34.18/day trades_holdout=103 avgR=-0.096. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A channel_position (with-trend): holdout $11.36/day develop $13.37/day trades_holdout=98 avgR=0.013. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A session_pullback (free): holdout $-540.78/day develop $-290.63/day trades_holdout=218 avgR=-1.475. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A yday_level_break (free): holdout $-161.12/day develop $-97.72/day trades_holdout=131 avgR=-0.657. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A compression_expansion (free): holdout $-27.53/day develop $-27.28/day trades_holdout=37 avgR=-0.100. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A rs_vs_book (free): holdout $-227.08/day develop $-338.21/day trades_holdout=109 avgR=-0.438. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track A adv_expanding (free): holdout $-162.49/day develop $-422.11/day trades_holdout=108 avgR=-0.310. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B trend_open (with-trend): holdout $-250.88/day develop $-135.20/day trades_holdout=110 avgR=-0.502. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B gap_with_trend (with-trend): holdout $-331.52/day develop $-8.48/day trades_holdout=104 avgR=-0.716. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B down_day_then_trend (with-trend): holdout $216.79/day develop $-185.04/day trades_holdout=110 avgR=0.434. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B late_with_trend (with-trend): holdout $-57.81/day develop $7.92/day trades_holdout=108 avgR=-0.059. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B channel_position (with-trend): holdout $-14.64/day develop $34.32/day trades_holdout=104 avgR=-0.016. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B session_pullback (free): holdout $-376.61/day develop $-135.45/day trades_holdout=219 avgR=-1.437. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B yday_level_break (free): holdout $-171.96/day develop $-69.32/day trades_holdout=142 avgR=-0.509. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B compression_expansion (free): holdout $-11.79/day develop $-12.00/day trades_holdout=23 avgR=-0.083. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B rs_vs_book (free): holdout $-182.30/day develop $-148.74/day trades_holdout=110 avgR=-0.340. Do not retry this exact (track, rule, stance) without a new costed reason.
- Track B adv_expanding (free): holdout $-144.26/day develop $-105.15/day trades_holdout=110 avgR=-0.249. Do not retry this exact (track, rule, stance) without a new costed reason.

