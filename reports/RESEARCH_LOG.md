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

## 2026-09-08T08:20:11-04:00 — Arrow 7

VERDICT: FAIL — no Arrow 7 experiment has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Same Tracks A and B. No new hours. Six experiments only: failed_yday_break with baseline / 2R / time-box 10:45; channel_position with 2R / trail-after-1R; yday_level_break with tight book (2 positions, 4 entries) + 2R. Did not retry exact dead Arrow 6 (track, rule, stance) pairs. Did not promote develop-red / holdout-green. Pass = holdout >= $200/day and develop not red.

Engine: 2R target = entry +/- 2 x stop distance; trail after close >= +1R (stop to entry, then 0.5% from favorable extreme). Stops/targets trigger on bar H/L, fill next open. Time-box flattens at first tradeable open >= 10:45.

What died (holdout < $200, or holdout green with red develop):
- Track A failed_yday_break|baseline: holdout $-111.86/day develop $-335.28/day trades_holdout=155 avgR=-0.184. Do not retry this exact (track, id) without a new costed reason.
- Track A failed_yday_break|2R: holdout $-49.81/day develop $-312.60/day trades_holdout=181 avgR=-0.142. Do not retry this exact (track, id) without a new costed reason.
- Track A failed_yday_break|time_box: holdout $-56.46/day develop $-233.27/day trades_holdout=171 avgR=-0.091. Do not retry this exact (track, id) without a new costed reason.
- Track A channel_position|2R: holdout $11.36/day develop $14.34/day trades_holdout=98 avgR=0.013. Do not retry this exact (track, id) without a new costed reason.
- Track A channel_position|trail: holdout $11.36/day develop $14.34/day trades_holdout=98 avgR=0.013. Do not retry this exact (track, id) without a new costed reason.
- Track A yday_level_break|tight_2R: holdout $-60.98/day develop $-31.63/day trades_holdout=50 avgR=-0.373. Do not retry this exact (track, id) without a new costed reason.
- Track B failed_yday_break|baseline: holdout $-59.57/day develop $-154.40/day trades_holdout=156 avgR=-0.181. Do not retry this exact (track, id) without a new costed reason.
- Track B failed_yday_break|2R: holdout $-62.95/day develop $-215.57/day trades_holdout=174 avgR=-0.224. Do not retry this exact (track, id) without a new costed reason.
- Track B failed_yday_break|time_box: holdout $-57.66/day develop $-151.30/day trades_holdout=158 avgR=-0.203. Do not retry this exact (track, id) without a new costed reason.
- Track B channel_position|2R: holdout $-14.64/day develop $36.51/day trades_holdout=104 avgR=-0.016. Do not retry this exact (track, id) without a new costed reason.
- Track B channel_position|trail: holdout $-14.64/day develop $34.11/day trades_holdout=104 avgR=-0.016. Do not retry this exact (track, id) without a new costed reason.
- Track B yday_level_break|tight_2R: holdout $-70.50/day develop $-6.20/day trades_holdout=48 avgR=-0.311. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T08:44:39-04:00 — Arrow 8

VERDICT: FAIL — no Arrow 8 experiment has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Same Tracks A and B. No new hours. Six experiments only: orb_wide baseline / 2R / trail / breadth-vs-book-median / cost gate (skip if round-trip cost > 0.25R); three_day_hl with 2R. Did not retry exact dead Arrow 6/7 pairs. Did not rerun channel|2R or channel|trail. Pass = holdout >= $200/day and develop not red.

orb_wide width band:
  Track A: or_names=49187 width_fail=16714 width_ok=32473 fired=29476
  Track B: or_names=25578 width_fail=8259 width_ok=17319 fired=15685

What died (holdout < $200, or holdout green with red develop):
- Track A orb_wide|baseline: holdout $-150.24/day develop $-188.48/day trades_holdout=108 avgR=-0.231. Do not retry this exact (track, id) without a new costed reason.
- Track A orb_wide|2R: holdout $-147.65/day develop $-164.49/day trades_holdout=110 avgR=-0.224. Do not retry this exact (track, id) without a new costed reason.
- Track A orb_wide|trail: holdout $-111.02/day develop $-189.67/day trades_holdout=129 avgR=-0.145. Do not retry this exact (track, id) without a new costed reason.
- Track A orb_wide|breadth: holdout $-104.75/day develop $-254.18/day trades_holdout=102 avgR=-0.228. Do not retry this exact (track, id) without a new costed reason.
- Track A orb_wide|cost_gate: holdout $-150.24/day develop $-188.48/day trades_holdout=108 avgR=-0.231. Do not retry this exact (track, id) without a new costed reason.
- Track A three_day_hl|2R: holdout $-150.18/day develop $-128.56/day trades_holdout=106 avgR=-0.312. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_wide|baseline: holdout $-126.85/day develop $-87.28/day trades_holdout=134 avgR=-0.114. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_wide|2R: holdout $-136.38/day develop $-81.02/day trades_holdout=138 avgR=-0.119. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_wide|trail: holdout $-152.86/day develop $-122.08/day trades_holdout=157 avgR=-0.122. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_wide|breadth: holdout $9.27/day develop $-154.99/day trades_holdout=121 avgR=0.009. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_wide|cost_gate: holdout $-126.85/day develop $-87.28/day trades_holdout=134 avgR=-0.114. Do not retry this exact (track, id) without a new costed reason.
- Track B three_day_hl|2R: holdout $-3.90/day develop $-25.60/day trades_holdout=109 avgR=-0.007. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T09:15:14-04:00 — Arrow 9

VERDICT: FAIL — no Arrow 9 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Phase 1 (develop only): mean post-09:44 range by DV quintile, |gap|, OR-width, 10d trend, and clock hour of the session extreme. Holdout was not used to choose buckets or the paragraph.

Where movement lives: On develop, leftover range after 09:44 concentrates where the tables are tallest: liquid names (Q5) that already printed a real opening range and/or a real gap. Track A: post-09:44 range is larger in Q5 (3.28% n=6548) than Q1 (2.92% n=6433). Highest |gap| bucket is >=2% (4.65% n=5107); highest OR-width bucket is >4% (6.16% n=4259). Q5 intersection with the most leftover range: Q5 × |gap| >=2% × OR >4% (mean 7.34% n=576). Session extremes by clock: 9h 7487 (23%), 10h 10179 (31%), 11h 14836 (46%). Track B: post-09:44 range is larger in Q5 (3.47% n=3341) than Q1 (2.81% n=3341). Highest |gap| bucket is >=2% (4.60% n=3221); highest OR-width bucket is >4% (6.31% n=2235). Q5 intersection with the most leftover range: Q5 × |gap| >=2% × OR >4% (mean 7.82% n=367). Session extremes by clock: 9h 3779 (23%), 10h 5179 (31%), 11h 7753 (46%).

Phase 2 six frozen books on that intended population (Q5 DV, wide OR and/or |gap|>=2%). orb_wide / gap-continuation / three_day_hl; manage baseline, 2R, trail, or 11:00 flatten. No 7th. No ML. No Arrow 8 cost_gate rerun.

What died (holdout < $200, or holdout green with red develop):
- Track A orb_q5|baseline: holdout $-125.12/day develop $-44.75/day trades_holdout=139 avgR=-0.122. Do not retry this exact (track, id) without a new costed reason.
- Track A orb_q5|2R: holdout $-128.31/day develop $-53.39/day trades_holdout=142 avgR=-0.121. Do not retry this exact (track, id) without a new costed reason.
- Track A gap_q5|2R: holdout $-301.55/day develop $-99.62/day trades_holdout=110 avgR=-0.228. Do not retry this exact (track, id) without a new costed reason.
- Track A orb_q5_gapsign|trail: holdout $-68.74/day develop $-67.03/day trades_holdout=132 avgR=-0.065. Do not retry this exact (track, id) without a new costed reason.
- Track A three_day_q5|2R: holdout $-99.34/day develop $-87.88/day trades_holdout=109 avgR=-0.201. Do not retry this exact (track, id) without a new costed reason.
- Track A orb_q5|flat1100: holdout $-151.47/day develop $-119.44/day trades_holdout=135 avgR=-0.142. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_q5|baseline: holdout $-159.98/day develop $-120.90/day trades_holdout=131 avgR=-0.154. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_q5|2R: holdout $-182.27/day develop $-121.45/day trades_holdout=132 avgR=-0.172. Do not retry this exact (track, id) without a new costed reason.
- Track B gap_q5|2R: holdout $-329.31/day develop $-77.34/day trades_holdout=109 avgR=-0.519. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_q5_gapsign|trail: holdout $-107.88/day develop $-46.97/day trades_holdout=124 avgR=-0.125. Do not retry this exact (track, id) without a new costed reason.
- Track B three_day_q5|2R: holdout $6.54/day develop $-67.94/day trades_holdout=110 avgR=0.016. Do not retry this exact (track, id) without a new costed reason.
- Track B orb_q5|flat1100: holdout $-195.09/day develop $-142.44/day trades_holdout=125 avgR=-0.191. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T09:46:41-04:00 — Arrow 10

VERDICT: FAIL — no Arrow 10 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Same Tracks A and B. No new hours. Six asymmetric books: long hot-cell gap-up 15m break + ema stack; long same + rising lows + 2R; long Q5 5-min high-retest + ema stack; short hot-cell gap-down 15m break + ema stack; short same + falling highs + 2R; short Q5 5-min low-retest + ema stack. Long ids emit only longs. Short ids emit only shorts. eod10 is a report tag. Did not rerun Arrow 9 Q5+1-4% books. No 7th. No Arrow 11.

ema15 vs eod10 on develop:
  Track A: n=27393 agree=15680 (57.2%) ema_long=13829 ema_short=13564 eod_up=12200 eod_down=10839 eod_flat=4354
  Track B: n=16281 agree=9158 (56.2%) ema_long=8140 ema_short=8141 eod_up=7209 eod_down=6478 eod_flat=2594

hot cell:
  Track A: hot=870 gap_up=415 gap_down=455
  Track B: hot=511 gap_up=258 gap_down=253

What died (holdout < $200, or holdout green with red develop):
- Track A long_hot_or15|ema (long): holdout $-78.39/day develop $-5.17/day trades_holdout=53 avgR=-0.163. Do not retry this exact (track, id) without a new costed reason.
- Track A long_hot_or15|ema_hhhl|2R (long): holdout $8.46/day develop $-10.10/day trades_holdout=14 avgR=0.068. Do not retry this exact (track, id) without a new costed reason.
- Track A long_q5_orbr5|ema (long): holdout $-196.33/day develop $-179.48/day trades_holdout=137 avgR=-0.303. Do not retry this exact (track, id) without a new costed reason.
- Track A short_hot_or15|ema (short): holdout $-21.16/day develop $-20.48/day trades_holdout=28 avgR=-0.083. Do not retry this exact (track, id) without a new costed reason.
- Track A short_hot_or15|ema_hhhl|2R (short): holdout $-18.24/day develop $-0.07/day trades_holdout=8 avgR=-0.252. Do not retry this exact (track, id) without a new costed reason.
- Track A short_q5_orbr5|ema (short): holdout $-153.50/day develop $-48.03/day trades_holdout=132 avgR=-0.204. Do not retry this exact (track, id) without a new costed reason.
- Track B long_hot_or15|ema (long): holdout $-17.23/day develop $20.42/day trades_holdout=26 avgR=-0.073. Do not retry this exact (track, id) without a new costed reason.
- Track B long_hot_or15|ema_hhhl|2R (long): holdout $4.01/day develop $-8.22/day trades_holdout=8 avgR=0.055. Do not retry this exact (track, id) without a new costed reason.
- Track B long_q5_orbr5|ema (long): holdout $-117.72/day develop $-70.99/day trades_holdout=129 avgR=-0.178. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot_or15|ema (short): holdout $21.53/day develop $5.58/day trades_holdout=16 avgR=0.149. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot_or15|ema_hhhl|2R (short): holdout $0.37/day develop $-3.29/day trades_holdout=2 avgR=0.020. Do not retry this exact (track, id) without a new costed reason.
- Track B short_q5_orbr5|ema (short): holdout $-103.77/day develop $35.73/day trades_holdout=132 avgR=-0.205. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T10:03:55-04:00 — Arrow 11

VERDICT: FAIL — no Arrow 11 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Kernel: Arrow 10 B/short_hot_or15|ema (develop +$5.58, holdout +$21.53, 58/16 trades). Short only. Did not mirror into longs. Did not rerun 5-min ORBR. Did not stack HH/HL. Six rings: control on both tracks; gap>=1%; OR>2.5%; dv>=0.60; two-close below OR low; first close below RTH VWAP. Flatten 11:59.

Rings that diluted the kernel (develop red and/or holdout red): A/short_hot|gap1, A/short_hot|or25, A/short_hot|dv60, A/short_hot|two_close, A/short_hot|vwap, B/short_hot|dv60, B/short_hot|two_close.

n_vs_control:
  A/short_hot|control: develop n=92 vs control 92 (1.00x) holdout n=28 vs control 28 (1.00x)
  A/short_hot|gap1: develop n=116 vs control 92 (1.26x) holdout n=40 vs control 28 (1.43x)
  A/short_hot|or25: develop n=131 vs control 92 (1.42x) holdout n=43 vs control 28 (1.54x)
  A/short_hot|dv60: develop n=114 vs control 92 (1.24x) holdout n=48 vs control 28 (1.71x)
  A/short_hot|two_close: develop n=202 vs control 92 (2.20x) holdout n=97 vs control 28 (3.46x)
  A/short_hot|vwap: develop n=220 vs control 92 (2.39x) holdout n=108 vs control 28 (3.86x)
  B/short_hot|control: develop n=58 vs control 58 (1.00x) holdout n=16 vs control 16 (1.00x)
  B/short_hot|gap1: develop n=72 vs control 58 (1.24x) holdout n=25 vs control 16 (1.56x)
  B/short_hot|or25: develop n=97 vs control 58 (1.67x) holdout n=37 vs control 16 (2.31x)
  B/short_hot|dv60: develop n=85 vs control 58 (1.47x) holdout n=27 vs control 16 (1.69x)
  B/short_hot|two_close: develop n=161 vs control 58 (2.78x) holdout n=85 vs control 16 (5.31x)
  B/short_hot|vwap: develop n=191 vs control 58 (3.29x) holdout n=98 vs control 16 (6.12x)

What died (holdout < $200, or holdout green with red develop):
- Track A short_hot|control: holdout $-21.16/day develop $-20.48/day trades_holdout=28 avgR=-0.083. Do not retry this exact (track, id) without a new costed reason.
- Track A short_hot|gap1: holdout $-18.37/day develop $-14.28/day trades_holdout=40 avgR=-0.051. Do not retry this exact (track, id) without a new costed reason.
- Track A short_hot|or25: holdout $29.10/day develop $-24.57/day trades_holdout=43 avgR=0.075. Do not retry this exact (track, id) without a new costed reason.
- Track A short_hot|dv60: holdout $-28.73/day develop $-3.64/day trades_holdout=48 avgR=-0.066. Do not retry this exact (track, id) without a new costed reason.
- Track A short_hot|two_close: holdout $-25.89/day develop $-40.80/day trades_holdout=97 avgR=-0.061. Do not retry this exact (track, id) without a new costed reason.
- Track A short_hot|vwap: holdout $-41.56/day develop $-25.79/day trades_holdout=108 avgR=-0.089. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot|control: holdout $21.53/day develop $5.58/day trades_holdout=16 avgR=0.149. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot|gap1: holdout $3.43/day develop $0.15/day trades_holdout=25 avgR=0.015. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot|or25: holdout $81.56/day develop $19.36/day trades_holdout=37 avgR=0.243. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot|dv60: holdout $-6.62/day develop $-3.32/day trades_holdout=27 avgR=-0.027. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot|two_close: holdout $-19.51/day develop $23.84/day trades_holdout=85 avgR=-0.075. Do not retry this exact (track, id) without a new costed reason.
- Track B short_hot|vwap: holdout $61.62/day develop $69.71/day trades_holdout=98 avgR=-0.084. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T10:20:06-04:00 — Arrow 12

VERDICT: FAIL — no Arrow 12 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Kernel: Arrow 11 B/short_hot|or25 (develop +$19.36, holdout +$81.56, 97/37 trades). Short only. Did not mirror into longs. Did not rerun Q4, two-close, 5-min ORBR, or VWAP entry. Six ids: control; 2R; trail after 1R; flatten 11:30; bearish OR (09:44 close in lower half); gap-down >= 1.5% with OR > 2.5% still.

B two-sided green preserved: short_or25|control (dev $19.36 hold $81.56 vs control $19.36/$81.56); short_or25|2R (dev $28.28 hold $80.45 vs control $19.36/$81.56); short_or25|trail (dev $31.27 hold $71.33 vs control $19.36/$81.56); short_or25|flat1130 (dev $8.90 hold $46.97 vs control $19.36/$81.56); short_or25|bearish_or (dev $2.09 hold $64.66 vs control $19.36/$81.56); short_or25|gap15 (dev $39.87 hold $73.44 vs control $19.36/$81.56).
Approach to $200 on B green books: short_or25|control hold $81.56/day (vs $200), short_or25|2R hold $80.45/day (vs $200), short_or25|trail hold $71.33/day (vs $200), short_or25|flat1130 hold $46.97/day (vs $200), short_or25|bearish_or hold $64.66/day (vs $200), short_or25|gap15 hold $73.44/day (vs $200).

n_vs_control:
  A/short_or25|control: develop n=131 vs control 131 (1.00x) holdout n=43 vs control 43 (1.00x)
  A/short_or25|2R: develop n=132 vs control 131 (1.01x) holdout n=43 vs control 43 (1.00x)
  A/short_or25|trail: develop n=139 vs control 131 (1.06x) holdout n=44 vs control 43 (1.02x)
  A/short_or25|flat1130: develop n=127 vs control 131 (0.97x) holdout n=43 vs control 43 (1.00x)
  A/short_or25|bearish_or: develop n=109 vs control 131 (0.83x) holdout n=32 vs control 43 (0.74x)
  A/short_or25|gap15: develop n=149 vs control 131 (1.14x) holdout n=52 vs control 43 (1.21x)
  B/short_or25|control: develop n=97 vs control 97 (1.00x) holdout n=37 vs control 37 (1.00x)
  B/short_or25|2R: develop n=98 vs control 97 (1.01x) holdout n=37 vs control 37 (1.00x)
  B/short_or25|trail: develop n=102 vs control 97 (1.05x) holdout n=38 vs control 37 (1.03x)
  B/short_or25|flat1130: develop n=95 vs control 97 (0.98x) holdout n=35 vs control 37 (0.95x)
  B/short_or25|bearish_or: develop n=78 vs control 97 (0.80x) holdout n=27 vs control 37 (0.73x)
  B/short_or25|gap15: develop n=112 vs control 97 (1.15x) holdout n=41 vs control 37 (1.11x)

What died (holdout < $200, or holdout green with red develop):
- Track A short_or25|control: holdout $29.10/day develop $-24.57/day trades_holdout=43 avgR=0.075. Do not retry this exact (track, id) without a new costed reason.
- Track A short_or25|2R: holdout $27.98/day develop $-19.92/day trades_holdout=43 avgR=0.072. Do not retry this exact (track, id) without a new costed reason.
- Track A short_or25|trail: holdout $26.59/day develop $-16.65/day trades_holdout=44 avgR=0.067. Do not retry this exact (track, id) without a new costed reason.
- Track A short_or25|flat1130: holdout $-3.94/day develop $-29.90/day trades_holdout=43 avgR=-0.010. Do not retry this exact (track, id) without a new costed reason.
- Track A short_or25|bearish_or: holdout $29.05/day develop $-48.03/day trades_holdout=32 avgR=0.100. Do not retry this exact (track, id) without a new costed reason.
- Track A short_or25|gap15: holdout $22.54/day develop $-31.01/day trades_holdout=52 avgR=0.048. Do not retry this exact (track, id) without a new costed reason.
- Track B short_or25|control: holdout $81.56/day develop $19.36/day trades_holdout=37 avgR=0.243. Do not retry this exact (track, id) without a new costed reason.
- Track B short_or25|2R: holdout $80.45/day develop $28.28/day trades_holdout=37 avgR=0.240. Do not retry this exact (track, id) without a new costed reason.
- Track B short_or25|trail: holdout $71.33/day develop $31.27/day trades_holdout=38 avgR=0.207. Do not retry this exact (track, id) without a new costed reason.
- Track B short_or25|flat1130: holdout $46.97/day develop $8.90/day trades_holdout=35 avgR=0.148. Do not retry this exact (track, id) without a new costed reason.
- Track B short_or25|bearish_or: holdout $64.66/day develop $2.09/day trades_holdout=27 avgR=0.264. Do not retry this exact (track, id) without a new costed reason.
- Track B short_or25|gap15: holdout $73.44/day develop $39.87/day trades_holdout=41 avgR=0.198. Do not retry this exact (track, id) without a new costed reason.

