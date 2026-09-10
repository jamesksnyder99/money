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

## 2026-09-08T12:36:36-04:00 — Arrow 13

VERDICT: FAIL — no Arrow 13 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Combined Arrow 12 B-short gap15 with 2R. New short entry: 5-min close below ema9. Longs are not a flipped short: pullback to OR mid/ema9; VWAP reclaim after a loss; quiet-open (|gap|<0.5%) 1-4% OR upside break. Did not rerun Q4, 5-min ORBR, two-close, 11:30 flatten, or a mirrored long.

n_vs_control (shorts):
  A/short_gap15|control: develop n=149 vs control 149 (1.00x) holdout n=52 vs control 52 (1.00x)
  A/short_gap15|2R: develop n=150 vs control 149 (1.01x) holdout n=52 vs control 52 (1.00x)
  A/short_gap15|c5_ema9: develop n=196 vs control 149 (1.32x) holdout n=89 vs control 52 (1.71x)
  B/short_gap15|control: develop n=112 vs control 112 (1.00x) holdout n=41 vs control 41 (1.00x)
  B/short_gap15|2R: develop n=113 vs control 112 (1.01x) holdout n=41 vs control 41 (1.00x)
  B/short_gap15|c5_ema9: develop n=158 vs control 112 (1.41x) holdout n=63 vs control 41 (1.54x)

What died (holdout < $200, or holdout green with red develop):
- Track A short_gap15|control (short): holdout $22.54/day develop $-27.70/day trades_holdout=52 avgR=0.048. Do not retry this exact (track, id) without a new costed reason.
- Track A short_gap15|2R (short): holdout $21.43/day develop $-23.05/day trades_holdout=52 avgR=0.045. Do not retry this exact (track, id) without a new costed reason.
- Track A short_gap15|c5_ema9 (short): holdout $-37.72/day develop $-47.22/day trades_holdout=89 avgR=-0.073. Do not retry this exact (track, id) without a new costed reason.
- Track A long_pb_mid_ema9 (long): holdout $-322.82/day develop $-217.14/day trades_holdout=186 avgR=-1.371. Do not retry this exact (track, id) without a new costed reason.
- Track A long_vwap_reclaim (long): holdout $-288.02/day develop $-195.36/day trades_holdout=176 avgR=-1.599. Do not retry this exact (track, id) without a new costed reason.
- Track A long_quiet_or15 (long): holdout $-183.51/day develop $-103.46/day trades_holdout=101 avgR=-0.232. Do not retry this exact (track, id) without a new costed reason.
- Track B short_gap15|control (short): holdout $73.44/day develop $39.87/day trades_holdout=41 avgR=0.198. Do not retry this exact (track, id) without a new costed reason.
- Track B short_gap15|2R (short): holdout $72.32/day develop $49.47/day trades_holdout=41 avgR=0.195. Do not retry this exact (track, id) without a new costed reason.
- Track B short_gap15|c5_ema9 (short): holdout $164.18/day develop $57.16/day trades_holdout=63 avgR=0.267. Do not retry this exact (track, id) without a new costed reason.
- Track B long_pb_mid_ema9 (long): holdout $-175.13/day develop $-189.03/day trades_holdout=135 avgR=-0.859. Do not retry this exact (track, id) without a new costed reason.
- Track B long_vwap_reclaim (long): holdout $-151.58/day develop $-131.24/day trades_holdout=132 avgR=-1.986. Do not retry this exact (track, id) without a new costed reason.
- Track B long_quiet_or15 (long): holdout $-141.04/day develop $-87.83/day trades_holdout=84 avgR=-0.215. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T15:53:03-04:00 — Arrow 14

VERDICT: FAIL — no Arrow 14 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Kernel: Arrow 13 B/short_gap15|c5_ema9 (develop +$57, holdout +$164). Short only. RISK_PER_IDEA stayed 200. Caps: cap5=5/10/1000, cap8=8/16/1600, cap10=10/20/2000. Ids: cap5 control; cap8; cap10; cap8+2R; cap8+trail; cap8 union (5-min close < ema9 OR 1-min close < OR low). Did not rerun Arrow 13 longs, Q4, 5-min ORBR, or 11:30 flatten.

n and mean concurrent vs cap5:
  A/c5_ema9|cap5: develop n=196 vs cap5 196 (1.00x) holdout n=89 vs cap5 89 (1.00x); mean_conc dev=3.54 hold=3.09 (cap5 3.54/3.09); mean_peak dev=4.07 hold=3.82
  A/c5_ema9|cap8: develop n=277 vs cap5 196 (1.41x) holdout n=117 vs cap5 89 (1.31x); mean_conc dev=4.80 hold=3.79 (cap5 3.54/3.09); mean_peak dev=5.74 hold=4.86
  A/c5_ema9|cap10: develop n=317 vs cap5 196 (1.62x) holdout n=128 vs cap5 89 (1.44x); mean_conc dev=5.52 hold=4.11 (cap5 3.54/3.09); mean_peak dev=6.64 hold=5.32
  A/c5_ema9|cap8|2R: develop n=283 vs cap5 196 (1.44x) holdout n=117 vs cap5 89 (1.31x); mean_conc dev=4.49 hold=3.56 (cap5 3.54/3.09); mean_peak dev=5.76 hold=4.86
  A/c5_ema9|cap8|trail: develop n=286 vs cap5 196 (1.46x) holdout n=118 vs cap5 89 (1.33x); mean_conc dev=4.02 hold=3.16 (cap5 3.54/3.09); mean_peak dev=5.69 hold=4.91
  A/c5_ema9|cap8|union: develop n=277 vs cap5 196 (1.41x) holdout n=118 vs cap5 89 (1.33x); mean_conc dev=4.82 hold=3.82 (cap5 3.54/3.09); mean_peak dev=5.76 hold=4.91
  B/c5_ema9|cap5: develop n=158 vs cap5 158 (1.00x) holdout n=63 vs cap5 63 (1.00x); mean_conc dev=2.98 hold=2.47 (cap5 2.98/2.47); mean_peak dev=3.43 hold=2.77
  B/c5_ema9|cap8: develop n=203 vs cap5 158 (1.28x) holdout n=76 vs cap5 63 (1.21x); mean_conc dev=3.81 hold=2.90 (cap5 2.98/2.47); mean_peak dev=4.45 hold=3.36
  B/c5_ema9|cap10: develop n=229 vs cap5 158 (1.45x) holdout n=82 vs cap5 63 (1.30x); mean_conc dev=4.25 hold=3.04 (cap5 2.98/2.47); mean_peak dev=5.05 hold=3.59
  B/c5_ema9|cap8|2R: develop n=206 vs cap5 158 (1.30x) holdout n=77 vs cap5 63 (1.22x); mean_conc dev=3.58 hold=2.78 (cap5 2.98/2.47); mean_peak dev=4.48 hold=3.32
  B/c5_ema9|cap8|trail: develop n=209 vs cap5 158 (1.32x) holdout n=77 vs cap5 63 (1.22x); mean_conc dev=3.16 hold=2.51 (cap5 2.98/2.47); mean_peak dev=4.43 hold=3.18
  B/c5_ema9|cap8|union: develop n=203 vs cap5 158 (1.28x) holdout n=76 vs cap5 63 (1.21x); mean_conc dev=3.77 hold=2.89 (cap5 2.98/2.47); mean_peak dev=4.45 hold=3.36

What died (holdout < $200, or holdout green with red develop):
- Track A c5_ema9|cap5: holdout $-37.72/day develop $-47.22/day trades_holdout=89 avgR=-0.073. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|cap8: holdout $-99.65/day develop $-50.73/day trades_holdout=117 avgR=-0.159. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|cap10: holdout $-95.70/day develop $-54.71/day trades_holdout=128 avgR=-0.153. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|cap8|2R: holdout $-143.36/day develop $-23.29/day trades_holdout=117 avgR=-0.207. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|cap8|trail: holdout $-121.73/day develop $-64.89/day trades_holdout=118 avgR=-0.164. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|cap8|union: holdout $-84.62/day develop $-42.99/day trades_holdout=118 avgR=-0.143. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap5: holdout $164.18/day develop $57.16/day trades_holdout=63 avgR=0.267. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap8: holdout $178.85/day develop $59.06/day trades_holdout=76 avgR=0.233. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap10: holdout $161.58/day develop $69.35/day trades_holdout=82 avgR=0.182. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap8|2R: holdout $122.55/day develop $49.21/day trades_holdout=77 avgR=0.168. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap8|trail: holdout $61.75/day develop $55.58/day trades_holdout=77 avgR=0.090. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap8|union: holdout $173.25/day develop $72.65/day trades_holdout=76 avgR=0.225. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T16:38:27-04:00 — Arrow 15

VERDICT: FAIL — no Arrow 15 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Preserved Arrow 14 B/c5_ema9|cap8 as id 1 (cap8, RISK_PER_IDEA=200). Shorts 2-4: memory, weak close, 5-min AVWAP (no 9/21). Shorts 5-6: 1-min close below ema9 after 09:45; 1-min close below ema9 from 09:31 with running OR width > 2.5%. Longs 7-12: washout hammer, hold-the-open, grind-up, AVWAP reclaim, prior-day morning high, 1-min hammer. Did not rerun Arrow 13 longs, union, cap10-as-idea, Q4, or 11:30 flatten.

1-min doors that beat the 5-min control on BOTH slices: none

n vs id 1 on shorts:
  A/c5_ema9|cap8: develop n=277 vs id1 277 (1.00x) holdout n=117 vs id1 117 (1.00x)
  A/c5_ema9|mem: develop n=214 vs id1 277 (0.77x) holdout n=95 vs id1 117 (0.81x)
  A/c5_ema9|weak: develop n=163 vs id1 277 (0.59x) holdout n=61 vs id1 117 (0.52x)
  A/c5_avwap|weak: develop n=318 vs id1 277 (1.15x) holdout n=150 vs id1 117 (1.28x)
  A/c1_ema9: develop n=276 vs id1 277 (1.00x) holdout n=116 vs id1 117 (0.99x)
  A/c1_ema9|early: develop n=387 vs id1 277 (1.40x) holdout n=170 vs id1 117 (1.45x)
  B/c5_ema9|cap8: develop n=203 vs id1 203 (1.00x) holdout n=76 vs id1 76 (1.00x)
  B/c5_ema9|mem: develop n=159 vs id1 203 (0.78x) holdout n=56 vs id1 76 (0.74x)
  B/c5_ema9|weak: develop n=113 vs id1 203 (0.56x) holdout n=42 vs id1 76 (0.55x)
  B/c5_avwap|weak: develop n=249 vs id1 203 (1.23x) holdout n=103 vs id1 76 (1.36x)
  B/c1_ema9: develop n=206 vs id1 203 (1.01x) holdout n=79 vs id1 76 (1.04x)
  B/c1_ema9|early: develop n=282 vs id1 203 (1.39x) holdout n=111 vs id1 76 (1.46x)

1-min tape vs 5-min control:
  A/c1_ema9: develop $-64.23 vs control $-50.73 (no); holdout $-88.14 vs control $-99.65 (BEATS); both_slices=NO
  A/c1_ema9|early: develop $-233.21 vs control $-50.73 (no); holdout $-446.88 vs control $-99.65 (no); both_slices=NO
  B/c1_ema9: develop $80.51 vs control $59.06 (BEATS); holdout $138.20 vs control $178.85 (no); both_slices=NO
  B/c1_ema9|early: develop $-31.47 vs control $59.06 (no); holdout $-33.21 vs control $178.85 (no); both_slices=NO

What died (holdout < $200, or holdout green with red develop):
- Track A c5_ema9|cap8 (short): holdout $-99.65/day develop $-50.73/day trades_holdout=117 avgR=-0.159. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|mem (short): holdout $-43.20/day develop $-45.27/day trades_holdout=95 avgR=-0.073. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|weak (short): holdout $-82.70/day develop $41.61/day trades_holdout=61 avgR=-0.180. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_avwap|weak (short): holdout $-163.03/day develop $-1.63/day trades_holdout=150 avgR=-0.143. Do not retry this exact (track, id) without a new costed reason.
- Track A c1_ema9 (short): holdout $-88.14/day develop $-64.23/day trades_holdout=116 avgR=-0.136. Do not retry this exact (track, id) without a new costed reason.
- Track A c1_ema9|early (short): holdout $-446.88/day develop $-233.21/day trades_holdout=170 avgR=-0.577. Do not retry this exact (track, id) without a new costed reason.
- Track A long_wash_hammer (long): holdout $-82.55/day develop $-40.31/day trades_holdout=19 avgR=-1.157. Do not retry this exact (track, id) without a new costed reason.
- Track A long_hold_open (long): holdout $-258.68/day develop $-151.87/day trades_holdout=144 avgR=-0.381. Do not retry this exact (track, id) without a new costed reason.
- Track A long_grind (long): holdout $-263.41/day develop $-287.11/day trades_holdout=255 avgR=-0.338. Do not retry this exact (track, id) without a new costed reason.
- Track A long_avwap_rc (long): holdout $-584.45/day develop $-441.14/day trades_holdout=297 avgR=-0.701. Do not retry this exact (track, id) without a new costed reason.
- Track A long_pd_morn (long): holdout $-253.74/day develop $-189.57/day trades_holdout=270 avgR=-0.317. Do not retry this exact (track, id) without a new costed reason.
- Track A long_c1_hammer (long): holdout $-287.50/day develop $-366.55/day trades_holdout=325 avgR=-1.615. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap8 (short): holdout $178.85/day develop $59.06/day trades_holdout=76 avgR=0.233. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|mem (short): holdout $139.90/day develop $103.32/day trades_holdout=56 avgR=0.316. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|weak (short): holdout $43.63/day develop $112.51/day trades_holdout=42 avgR=0.098. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_avwap|weak (short): holdout $84.09/day develop $107.22/day trades_holdout=103 avgR=0.078. Do not retry this exact (track, id) without a new costed reason.
- Track B c1_ema9 (short): holdout $138.20/day develop $80.51/day trades_holdout=79 avgR=0.141. Do not retry this exact (track, id) without a new costed reason.
- Track B c1_ema9|early (short): holdout $-33.21/day develop $-31.47/day trades_holdout=111 avgR=-0.217. Do not retry this exact (track, id) without a new costed reason.
- Track B long_wash_hammer (long): holdout $-37.96/day develop $-75.92/day trades_holdout=12 avgR=-0.962. Do not retry this exact (track, id) without a new costed reason.
- Track B long_hold_open (long): holdout $-151.86/day develop $-100.15/day trades_holdout=102 avgR=-0.302. Do not retry this exact (track, id) without a new costed reason.
- Track B long_grind (long): holdout $-235.25/day develop $-469.50/day trades_holdout=258 avgR=-0.299. Do not retry this exact (track, id) without a new costed reason.
- Track B long_avwap_rc (long): holdout $-273.60/day develop $-273.87/day trades_holdout=220 avgR=-0.532. Do not retry this exact (track, id) without a new costed reason.
- Track B long_pd_morn (long): holdout $-522.96/day develop $-79.42/day trades_holdout=288 avgR=-0.446. Do not retry this exact (track, id) without a new costed reason.
- Track B long_c1_hammer (long): holdout $-275.75/day develop $-242.28/day trades_holdout=253 avgR=-2.315. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T17:41:29-04:00 — Arrow 16

VERDICT: FAIL — no Arrow 16 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass.

Preserved B/c5_ema9|cap8 as id 1 (cap8, RISK_PER_IDEA=200). Ten shorts: control; memory; three down 5-min closes; close below AVWAP; rel vol >= 3x (rocket-scan full-window definition); stop = prior session morning high if above fill and >= 0.4%; first signal at/after 10:00; not a premarket +10% rocket; expanding 5-min range; memory+AVWAP. Did not rerun 09:31 early 1-min, Arrow 13/15 longs, Q4, cap10-as-idea, 11:30 flatten, or union.

Ids that beat control on BOTH slices: A/c5_ema9|mem, A/c5_ema9|3down, A/c5_ema9|avwap, A/c5_ema9|rv3, A/c5_ema9|pdhigh, A/c5_ema9|1000, A/c5_ema9|mem_avwap

n vs id 1:
  A/c5_ema9|cap8: develop n=277 vs id1 277 (1.00x) holdout n=117 vs id1 117 (1.00x)
  A/c5_ema9|mem: develop n=214 vs id1 277 (0.77x) holdout n=95 vs id1 117 (0.81x)
  A/c5_ema9|3down: develop n=144 vs id1 277 (0.52x) holdout n=34 vs id1 117 (0.29x)
  A/c5_ema9|avwap: develop n=217 vs id1 277 (0.78x) holdout n=82 vs id1 117 (0.70x)
  A/c5_ema9|rv3: develop n=42 vs id1 277 (0.15x) holdout n=35 vs id1 117 (0.30x)
  A/c5_ema9|pdhigh: develop n=251 vs id1 277 (0.91x) holdout n=112 vs id1 117 (0.96x)
  A/c5_ema9|1000: develop n=281 vs id1 277 (1.01x) holdout n=112 vs id1 117 (0.96x)
  A/c5_ema9|nopre: develop n=277 vs id1 277 (1.00x) holdout n=117 vs id1 117 (1.00x)
  A/c5_ema9|expand: develop n=168 vs id1 277 (0.61x) holdout n=60 vs id1 117 (0.51x)
  A/c5_ema9|mem_avwap: develop n=182 vs id1 277 (0.66x) holdout n=70 vs id1 117 (0.60x)
  B/c5_ema9|cap8: develop n=203 vs id1 203 (1.00x) holdout n=76 vs id1 76 (1.00x)
  B/c5_ema9|mem: develop n=159 vs id1 203 (0.78x) holdout n=56 vs id1 76 (0.74x)
  B/c5_ema9|3down: develop n=102 vs id1 203 (0.50x) holdout n=27 vs id1 76 (0.36x)
  B/c5_ema9|avwap: develop n=168 vs id1 203 (0.83x) holdout n=58 vs id1 76 (0.76x)
  B/c5_ema9|rv3: develop n=21 vs id1 203 (0.10x) holdout n=16 vs id1 76 (0.21x)
  B/c5_ema9|pdhigh: develop n=192 vs id1 203 (0.95x) holdout n=73 vs id1 76 (0.96x)
  B/c5_ema9|1000: develop n=216 vs id1 203 (1.06x) holdout n=75 vs id1 76 (0.99x)
  B/c5_ema9|nopre: develop n=203 vs id1 203 (1.00x) holdout n=76 vs id1 76 (1.00x)
  B/c5_ema9|expand: develop n=114 vs id1 203 (0.56x) holdout n=33 vs id1 76 (0.43x)
  B/c5_ema9|mem_avwap: develop n=141 vs id1 203 (0.69x) holdout n=45 vs id1 76 (0.59x)

vs control on both slices:
  A/c5_ema9|mem: develop $-45.27 vs control $-50.73 (BEATS); holdout $-43.20 vs control $-99.65 (BEATS); both_slices=YES
  A/c5_ema9|3down: develop $-32.04 vs control $-50.73 (BEATS); holdout $26.10 vs control $-99.65 (BEATS); both_slices=YES
  A/c5_ema9|avwap: develop $23.72 vs control $-50.73 (BEATS); holdout $-4.91 vs control $-99.65 (BEATS); both_slices=YES
  A/c5_ema9|rv3: develop $-41.24 vs control $-50.73 (BEATS); holdout $34.84 vs control $-99.65 (BEATS); both_slices=YES
  A/c5_ema9|pdhigh: develop $28.11 vs control $-50.73 (BEATS); holdout $-68.63 vs control $-99.65 (BEATS); both_slices=YES
  A/c5_ema9|1000: develop $18.11 vs control $-50.73 (BEATS); holdout $-84.96 vs control $-99.65 (BEATS); both_slices=YES
  A/c5_ema9|nopre: develop $-50.73 vs control $-50.73 (no); holdout $-99.65 vs control $-99.65 (no); both_slices=NO
  A/c5_ema9|expand: develop $42.50 vs control $-50.73 (BEATS); holdout $-104.40 vs control $-99.65 (no); both_slices=NO
  A/c5_ema9|mem_avwap: develop $2.35 vs control $-50.73 (BEATS); holdout $-4.36 vs control $-99.65 (BEATS); both_slices=YES
  B/c5_ema9|mem: develop $103.32 vs control $59.06 (BEATS); holdout $139.90 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|3down: develop $17.83 vs control $59.06 (no); holdout $18.05 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|avwap: develop $85.35 vs control $59.06 (BEATS); holdout $122.88 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|rv3: develop $0.30 vs control $59.06 (no); holdout $102.97 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|pdhigh: develop $14.53 vs control $59.06 (no); holdout $46.99 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|1000: develop $54.21 vs control $59.06 (no); holdout $102.76 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|nopre: develop $59.06 vs control $59.06 (no); holdout $178.85 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|expand: develop $93.06 vs control $59.06 (BEATS); holdout $42.81 vs control $178.85 (no); both_slices=NO
  B/c5_ema9|mem_avwap: develop $113.75 vs control $59.06 (BEATS); holdout $121.32 vs control $178.85 (no); both_slices=NO

What died (holdout < $200, or holdout green with red develop):
- Track A c5_ema9|cap8 (short): holdout $-99.65/day develop $-50.73/day trades_holdout=117 avgR=-0.159. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|mem (short): holdout $-43.20/day develop $-45.27/day trades_holdout=95 avgR=-0.073. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|3down (short): holdout $26.10/day develop $-32.04/day trades_holdout=34 avgR=0.086. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|avwap (short): holdout $-4.91/day develop $23.72/day trades_holdout=82 avgR=-0.035. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|rv3 (short): holdout $34.84/day develop $-41.24/day trades_holdout=35 avgR=0.059. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|pdhigh (short): holdout $-68.63/day develop $28.11/day trades_holdout=112 avgR=-0.070. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|1000 (short): holdout $-84.96/day develop $18.11/day trades_holdout=112 avgR=-0.194. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|nopre (short): holdout $-99.65/day develop $-50.73/day trades_holdout=117 avgR=-0.159. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|expand (short): holdout $-104.40/day develop $42.50/day trades_holdout=60 avgR=-0.247. Do not retry this exact (track, id) without a new costed reason.
- Track A c5_ema9|mem_avwap (short): holdout $-4.36/day develop $2.35/day trades_holdout=70 avgR=-0.035. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|cap8 (short): holdout $178.85/day develop $59.06/day trades_holdout=76 avgR=0.233. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|mem (short): holdout $139.90/day develop $103.32/day trades_holdout=56 avgR=0.316. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|3down (short): holdout $18.05/day develop $17.83/day trades_holdout=27 avgR=0.073. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|avwap (short): holdout $122.88/day develop $85.35/day trades_holdout=58 avgR=0.236. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|rv3 (short): holdout $102.97/day develop $0.30/day trades_holdout=16 avgR=0.663. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|pdhigh (short): holdout $46.99/day develop $14.53/day trades_holdout=73 avgR=0.068. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|1000 (short): holdout $102.76/day develop $54.21/day trades_holdout=75 avgR=0.103. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|nopre (short): holdout $178.85/day develop $59.06/day trades_holdout=76 avgR=0.233. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|expand (short): holdout $42.81/day develop $93.06/day trades_holdout=33 avgR=0.087. Do not retry this exact (track, id) without a new costed reason.
- Track B c5_ema9|mem_avwap (short): holdout $121.32/day develop $113.75/day trades_holdout=45 avgR=0.298. Do not retry this exact (track, id) without a new costed reason.

## 2026-09-08T19:58:14-04:00 — Arrow 18

Repairs then kernel-only rescore. Flatten leak fixed (zero-volume 11:59 no longer orphans).
SSR proxy (last close <= 0.90 * prior close) and crude borrow proxy (gap<=-5% and prior DV < 10M).
Dispersion: std/se/t/bootstrap CI on $/day. IWM same-window alpha. Holdout is contaminated; not EV.
Four rows: B no-filter, B SSR+borrow, A no-filter, A SSR+borrow. Did not rerun Arrow 3-16 grids.

HONESTY:
Holdout has been used to pick rings (or25 -> c5_ema9 -> cap8). +179/day is not an expected value. It is a contaminated holdout print.
Arithmetic: 200 risk x avgR x trades/day. Develop avgR ~0.05 and ~5 fills/day ~ 50/day. Holdout avgR ~0.23 x ~3.5 ~ 160/day.
300/day on this cell needs more R, more fills, or more dollars at risk — not another 5-min pattern.
SSR/borrow were unmodelled before this arrow. Flatten leak: a zero-volume 11:59 bar no longer orphans a live position.

- Track B kernel|nofilter: develop $68.05/day holdout $178.85/day trades_holdout=76 avgR=0.233 t=1.39 IWM_alpha_hold $127.30/day.
- Track B kernel|ssr_borrow: develop $59.13/day holdout $79.27/day trades_holdout=67 avgR=0.117 t=0.66 IWM_alpha_hold $31.51/day.
- Track A kernel|nofilter: develop $-40.34/day holdout $-93.60/day trades_holdout=120 avgR=-0.149 t=-0.67 IWM_alpha_hold $-129.23/day.
- Track A kernel|ssr_borrow: develop $-48.36/day holdout $-118.89/day trades_holdout=109 avgR=-0.176 t=-0.96 IWM_alpha_hold $-153.08/day.

## 2026-09-08T21:01:27-04:00 — Arrow 20

VERDICT: FAIL — no Arrow 20 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass. First swing, not EV.

First long swing on data/full at the 09:29 hot gate (prior_close $1-20, pre_dv>=250k, pre_dv_rel>=3, ext in [3%, 15)). Six ids: 09:30 open flatten 11:59; flatten 15:59; strong 5-min hold; new high after 09:45; less-extended <10% open; open+2R. Did not rescore the B-short. Did not touch data/bars. First look, not EV.

hot develop: n_sess=42 total=501 mean=11.93 median=10.0 max=55
hot holdout: n_sess=22 total=473 mean=21.50 median=19.0 max=63

- open|flat1159: develop $-46.90/day holdout $-238.29/day trades_holdout=171 avgR=-0.183 t=-1.70.
- open|flat1559: develop $-42.70/day holdout $-256.88/day trades_holdout=171 avgR=-0.196 t=-1.51.
- strong5: develop $-178.88/day holdout $-652.47/day trades_holdout=214 avgR=-0.506 t=-4.42.
- newhigh: develop $-236.53/day holdout $-498.29/day trades_holdout=157 avgR=-0.432 t=-3.77.
- open|lt10: develop $-30.39/day holdout $-334.41/day trades_holdout=166 avgR=-0.255 t=-2.60.
- open|2R: develop $-62.55/day holdout $-220.09/day trades_holdout=171 avgR=-0.168 t=-1.57.

## 2026-09-08T21:38:41-04:00 — Arrow 21

VERDICT: FAIL — no Arrow 21 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass. Did not rerun strong5/newhigh/flat1559.

Same 09:29 hot gate as Arrow 20 (prior_close $1-20, pre_dv>=250k, pre_dv_rel>=3, ext in [3%, 15)). Six ids: pullback to 09:29 px or RTH VWAP; 09:30 open only if open <= +1% vs 09:29; tighter ext [3%, 8%); pre_dv>=1M 09:30 open; pullback with max_positions=3; short the 09:30 open of the same hot names. Flatten 11:59. Did not rerun strong5/newhigh/flat1559. Did not rescore the B-short. Did not touch data/bars. No Arrow 22.

hot develop: n_sess=42 total=501 mean=11.93 median=10.0 max=55
hot holdout: n_sess=22 total=473 mean=21.50 median=19.0 max=63

- pullback: develop $-514.03/day holdout $-1087.29/day trades_holdout=266 avgR=-0.679 t=-5.14.
- open|gap1: develop $-37.09/day holdout $-236.91/day trades_holdout=171 avgR=-0.187 t=-1.65.
- open|ext8: develop $8.64/day holdout $-293.90/day trades_holdout=162 avgR=-0.234 t=-2.22.
- open|dv1m: develop $-78.59/day holdout $-336.48/day trades_holdout=156 avgR=-0.245 t=-2.65.
- pullback|max3: develop $-204.18/day holdout $-494.70/day trades_holdout=127 avgR=-0.719 t=-3.91.
- fade|open: develop $-204.55/day holdout $-84.60/day trades_holdout=163 avgR=-0.071 t=-0.56.

## 2026-09-08T21:57:07-04:00 — Arrow 22

VERDICT: FAIL — no Arrow 22 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass. Did not rerun 09:29 open/pullback/strong5/newhigh/fade.

08:00 hot gate (prior_close $1-20, pre_dv_0800>=400k, pre_dv_rel_0800>=3, ext in [2%, 10)). Fill next tradeable open. Size min(10pct account, 5pct pre_dv_0800, 2pct prior-day DV). Six longs: flatten 09:29; flatten 11:59; pre_dv>=750k; ext [2%, 6%); max_positions=3; skip sessions with >15 hot names. Did not rerun 09:29 open/pullback/strong5/newhigh/fade. Did not rescore the B-short. Did not touch data/bars. No Arrow 23.

08:00 hot develop: n_sess=42 total=328 mean=7.81 median=6.0 max=31
08:00 hot holdout: n_sess=22 total=279 mean=12.68 median=11.0 max=27

- open|flat0929: develop $-313.00/day holdout $-184.44/day trades_holdout=158 avgR=0.027 t=-1.76.
- open|flat1159: develop $-266.05/day holdout $-183.79/day trades_holdout=158 avgR=-0.143 t=-0.88.
- open|dv750k: develop $-230.55/day holdout $-167.89/day trades_holdout=141 avgR=0.023 t=-1.92.
- open|ext6: develop $-223.43/day holdout $-293.50/day trades_holdout=144 avgR=-0.251 t=-3.36.
- open|max3: develop $-164.69/day holdout $-132.04/day trades_holdout=64 avgR=-0.241 t=-2.94.
- open|nocluster: develop $-295.61/day holdout $-234.78/day trades_holdout=112 avgR=-0.244 t=-2.92.

## 2026-09-09T07:19:45-04:00 — Arrow 23

VERDICT: FAIL — no Arrow 23 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass. Did not rerun 08:00/09:29 buy-the-open, A21 pullback, strong5, newhigh, or fade-the-hot-open.

Six orthogonal jobs on data/full: coil break; afternoon AM-high break; failed-rocket short; flush higher-low; vs-IWM hold; climax short. cap8. Did not rerun 08:00/09:29 buy-the-open, A21 pullback, strong5, newhigh, or fade. Did not rescore the B-short. Did not touch data/bars. No Arrow 24.

coil develop: n_sess=42 total=538 mean=12.81 median=13.0 max=24
coil holdout: n_sess=22 total=381 mean=17.32 median=17.5 max=30
08:00 hot develop: n_sess=42 total=328 mean=7.81 median=6.0 max=31
08:00 hot holdout: n_sess=22 total=279 mean=12.68 median=11.0 max=27

- coil_break: develop $-115.22/day holdout $-236.32/day trades_holdout=153 avgR=-0.210 hit=0.346 PF=0.537 reached_1R=0.209 t=-2.67.
- am_high_pm: develop $-5.77/day holdout $-92.51/day trades_holdout=49 avgR=-0.375 hit=0.367 PF=0.536 reached_1R=0.592 t=-2.01.
- fail_rocket: develop $-86.90/day holdout $-140.66/day trades_holdout=184 avgR=-0.085 hit=0.478 PF=0.720 reached_1R=0.136 t=-1.55.
- flush_hl: develop $-72.79/day holdout $-63.13/day trades_holdout=159 avgR=-0.062 hit=0.384 PF=0.901 reached_1R=0.403 t=-0.38.
- vs_iwm: develop $-701.72/day holdout $-561.71/day trades_holdout=265 avgR=-0.482 hit=0.309 PF=0.404 reached_1R=0.343 t=-5.50.
- climax: develop $-418.33/day holdout $-634.97/day trades_holdout=266 avgR=-0.443 hit=0.327 PF=0.414 reached_1R=0.342 t=-5.12.

Shape vs Arrows 20-22: those books were ~30% hit, negative avgR, stop-driven losses from buying an already-extended open. Three jobs here are a different shape even though none clear $200. fail_rocket shorts print 48% holdout hit and PF 0.720 with 82% time-flattens and avgR near zero — a slow bleed, not a chase wash. am_high_pm is almost flat on develop (-6/day) and 59% of holdout trades tag +1R, then give it back (medR -1.2, 59% stopped). flush_hl is the least-bad holdout (-63/day, PF 0.901) with a fat right tail (p90R 1.73) and 40% reaching +1R; still negative EV. coil_break is ~80% time-flatten dead money (mean extension ~1.5%). vs_iwm and climax are the same wreck as 20-22, only larger.

## 2026-09-09T08:13:01-04:00 — Arrow 24

VERDICT: FAIL — no Arrow 24 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass. Holdout is not a tuner. Did not rerun 08:00/09:29 buy-the-extended-open, A21 pullback, strong5, newhigh, fade, vs_iwm, climax.

Part A develop FLY=1152 FAIL=1335 other=61113. Cell (develop-locked, holdout PEEK): orw >= 0.0510, dv0929 >= 98028.1104, ext0944 >= 0.0337. n=569 FLY=431 rate=0.757 vs baseline 0.463. Applied as an extra population cut on every long door.
100-grid both-green=0. flush-family beat harness control on develop: 6/25. cost_skips=2261.

- flush_hl|harness: develop $-19.60/day holdout $141.51/day n_hold=28 avgR=0.549 hit=0.607 PF=3.535 t=1.97.
- am_high_pm|harness: develop $10.82/day holdout $-25.48/day n_hold=3 avgR=-0.936 hit=0.000 PF=0.000 t=-1.81.

Top 5 grid by holdout $/day:
- flush|flat1159|px5: develop $-6.31/day holdout $146.05/day n=27 avgR=0.588 hit=0.630.
- flush|flat1159|cap3: develop $-18.28/day holdout $145.33/day n=27 avgR=0.591 hit=0.630.
- flush|flat1159|cost: develop $-19.60/day holdout $141.51/day n=28 avgR=0.549 hit=0.607.
- flush|t15R|cap3: develop $-33.50/day holdout $121.23/day n=32 avgR=0.414 hit=0.656.
- flush|t15R|base: develop $-31.80/day holdout $119.90/day n=34 avgR=0.385 hit=0.647.

FLY vs FAIL named a develop-locked cell (wide 09:30-09:44 OR, pre_dv_0929 >= ~98k, ext_0944 >= 3.4%) with 76% FLY rate vs 46% baseline; it was applied to every long door and holdout was not used to pick it. Door families vs Arrows 20-22 (those were ~30% hit chasing an already-extended open): flush is a different shape — holdout hit ~60% and PF ~3.5 on the harness control and on flush|flat1159|*, but develop is still slightly red so not a pass (closest flush|flat1159|px5 -6/+146). volfirst|half1R_trail hits ~70% and often tags +1R, still sub-$200. launch is sparse after the cell cut. giveback is a wreck, and giveback|flat1159 is structurally zero (entry after 13:00 vs flatten 11:59). both-green=0 of 100. Holdout was not a tuner.

## 2026-09-09T08:39:08-04:00 — Arrow 25

VERDICT: FAIL — no Arrow 25 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass. +146 holdout on Arrow 24 flush|flat1159|px5 is not EV.

Ten longs on flush + FLY cell. Harness on. Did not rerun the 100-grid, giveback, launch-catch, volfirst-as-hero, 08:00 open-buy, vs_iwm, climax. +146 is not EV. No Arrow 26.

- flush|ctrl: develop $-9.14/day holdout $146.05/day n_hold=27 vs_id1=1.00x avgR=0.588 hit=0.630 PF=3.847 t=2.05.
- flush|cap3: develop $-8.27/day holdout $154.57/day n_hold=26 vs_id1=0.96x avgR=0.647 hit=0.654 PF=4.613 t=2.15.
- flush|flat1559: develop $-24.30/day holdout $74.36/day n_hold=29 vs_id1=1.07x avgR=0.277 hit=0.517 PF=1.753 t=1.41.
- flush|half1R: develop $-18.75/day holdout $104.63/day n_hold=45 vs_id1=1.67x avgR=0.671 hit=0.778 PF=2.405 t=1.84.
- flush|deep3: develop $-5.51/day holdout $121.32/day n_hold=23 vs_id1=0.85x avgR=0.578 hit=0.609 PF=3.906 t=1.71.
- flush|max6: develop $11.29/day holdout $116.77/day n_hold=23 vs_id1=0.85x avgR=0.550 hit=0.609 PF=3.363 t=1.70.
- flush|reclaim: develop $-18.20/day holdout $90.71/day n_hold=20 vs_id1=0.74x avgR=0.499 hit=0.500 PF=3.871 t=1.43.
- flush|after10: develop $-1.99/day holdout $-6.63/day n_hold=3 vs_id1=0.11x avgR=-0.248 hit=0.333 PF=0.288 t=-0.85.
- flush|rel5: develop $-8.91/day holdout $96.97/day n_hold=11 vs_id1=0.41x avgR=0.970 hit=0.727 PF=5.903 t=1.46.
- flush|nocell: develop $-58.00/day holdout $124.00/day n_hold=90 vs_id1=3.33x avgR=0.141 hit=0.456 PF=1.391 t=1.15.

Beat control on both slices: flush|cap3

## 2026-09-09T10:37:41-04:00 — Arrow 26

VERDICT: FAIL — no Arrow 26 book has holdout >= $200/day AND non-red develop. Develop-red / holdout-green is not a pass. +117 holdout on Arrow 25 flush|max6 is not EV.

Ten longs on flush|max6 accel/decel rings. Harness on. Did not rerun nocell, after10, giveback, launch-catch, 08:00 open-buy, vs_iwm, climax, or the 100-grid. +117 is not EV. No Arrow 27.

- flush|max6: develop $11.29/day holdout $116.77/day n_hold=23 vs_id1=1.00x avgR=0.550 hit=0.609 PF=3.363 t=1.70 both_green=True.
- flush|cap3: develop $11.29/day holdout $125.28/day n_hold=22 vs_id1=0.96x avgR=0.618 hit=0.636 PF=4.063 t=1.80 both_green=True.
- flush|rngaccel: develop $-0.69/day holdout $34.11/day n_hold=11 vs_id1=0.48x avgR=0.353 hit=0.727 PF=3.785 t=2.07 both_green=False.
- flush|decel: develop $18.19/day holdout $57.35/day n_hold=20 vs_id1=0.87x avgR=0.318 hit=0.700 PF=2.586 t=1.37 both_green=True.
- flush|volaccel: develop $-0.83/day holdout $17.53/day n_hold=6 vs_id1=0.26x avgR=0.320 hit=0.333 PF=1.687 t=0.41 both_green=False.
- flush|slowwash: develop $2.43/day holdout $18.14/day n_hold=3 vs_id1=0.13x avgR=0.828 hit=0.667 PF=8.203 t=0.99 both_green=True.
- flush|twohl: develop $-4.53/day holdout $50.22/day n_hold=20 vs_id1=0.87x avgR=0.269 hit=0.550 PF=2.202 t=1.20 both_green=False.
- flush|skip0950: develop $1.45/day holdout $11.36/day n_hold=4 vs_id1=0.17x avgR=0.400 hit=0.500 PF=2.220 t=0.57 both_green=True.
- flush|hold05: develop $23.71/day holdout $75.23/day n_hold=23 vs_id1=1.00x avgR=0.354 hit=0.522 PF=2.419 t=1.16 both_green=True.
- flush|noreclaim: develop $-6.34/day holdout $81.66/day n_hold=18 vs_id1=0.78x avgR=0.499 hit=0.500 PF=3.969 t=1.20 both_green=False.

Beat control on both slices: none
Both-green: flush|max6, flush|cap3, flush|decel, flush|slowwash, flush|skip0950, flush|hold05

## 2026-09-09T12:11:47-04:00 — Arrow 27

VERDICT: FAIL — no Arrow 27 book has holdout >= $200/day AND non-red develop. Combined holdout is not EV. Combined develop is the helper print, not '$200 minus one improvement'.

Repairs R1-R5. combine_books. B-short SSR policy rows on Lab A. flush|max6 reprint on data/full. No rocket rings. No $500/idea. No virgin pull. R6 skipped beta-IWM. No Arrow 28.
R3: launch-catch was under-sampled in A24 (cell vs launch gates almost disjoint), not refuted. Not rerun here.
Honesty: do not write that the account is one improvement from $200. A18 SSR-on (~+$59) plus A26 flush (~+$11) was ~+$70 before this helper. combine_books this file: develop $80.37/day. Combined holdout is not EV.

- B_reject: develop $30.96/day holdout $68.29/day n_hold=63 avgR=0.094 t=0.56 ssr_share=0.193 ssr_nofill=0 peak_conc=8.
- B_nofilter: develop $68.19/day holdout $178.85/day n_hold=76 avgR=0.233 t=1.39 ssr_share=0.193 ssr_nofill=0 peak_conc=8.
- B_uptick10: develop $58.59/day holdout $129.86/day n_hold=75 avgR=0.166 t=1.09 ssr_share=0.193 ssr_nofill=1 peak_conc=8.
- B_uptick5: develop $50.95/day holdout $117.14/day n_hold=73 avgR=0.148 t=0.95 ssr_share=0.193 ssr_nofill=9 peak_conc=8.
- B_uptick10_cap: develop $55.05/day holdout $132.75/day n_hold=73 avgR=0.175 t=1.12 ssr_share=0.193 ssr_nofill=4 peak_conc=8.
- flush|max6: develop $12.18/day holdout $116.77/day n_hold=23 avgR=0.550 t=1.70 peak_conc=4.
- COMBINED B_nofilter+flush|max6: develop $80.37/day holdout $295.62/day corr_dev=-0.190 corr_hold=-0.048 (holdout not EV).

## 2026-09-09T14:07:00-04:00 — Arrow 28

VERDICT: HOLD OUT CLEARS $200 WITH NON-RED DEVELOP — B_uptick10|atr1559

B-short on data/full. SSR=B_uptick10. Afternoon exits. No rocket rings. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 29.
Row 0 counts vs A27 B_uptick10: develop 212/204 (1.04x) holdout 94/75 (1.25x) — DRIFT beyond ±10%. Likely causes: data/full 04:00-16:00 tape adds premarket 15m bars to the EMA stitch (Lab A started 07:30), and ssr_active session-low now includes 04:00-07:30 prints; harness ATR/0.6pct floor is on (A27 B-short did not use it) which changes size not skips.
Honesty: combined develop is the combine_books number. Combined holdout is not EV.

- B_uptick10|flat1159: develop $14.62/day holdout $148.24/day n_hold=94 avgR=0.202 PF=1.629 t=1.06 peak_conc=8 mean_conc=3.79.
- B_uptick10|flat1559: develop $-12.99/day holdout $293.68/day n_hold=95 avgR=0.382 PF=2.319 t=2.05 peak_conc=8 mean_conc=3.70.
- B_uptick10|hold05: develop $-2.80/day holdout $166.89/day n_hold=94 avgR=0.217 PF=1.677 t=1.12 peak_conc=8 mean_conc=3.03.
- B_uptick10|atr1559: develop $82.65/day holdout $233.20/day n_hold=95 avgR=0.292 PF=2.198 t=2.19 peak_conc=8 mean_conc=3.13.
- B_uptick10|flat1330: develop $-61.99/day holdout $199.10/day n_hold=95 avgR=0.256 PF=1.896 t=1.36 peak_conc=8 mean_conc=3.77.
- B_uptick10|hold05_1430: develop $-36.72/day holdout $175.18/day n_hold=94 avgR=0.228 PF=1.730 t=1.09 peak_conc=8 mean_conc=3.16.
- B_reject|flat1159: develop $-43.56/day holdout $83.66/day n_hold=80 avgR=0.147 PF=1.367 t=0.60 peak_conc=8 mean_conc=3.22.
- COMBINED B_uptick10|atr1559+flush|max6: develop $94.83/day holdout $349.97/day corr_dev=-0.258 (holdout not EV).

## 2026-09-09T14:59:28-04:00 — Arrow 29

VERDICT: FAIL — no Arrow 29 book has holdout >= $200/day AND non-red develop. Combined holdout is not EV.

FLY cell as population; new rocket radii. No flush|max6 synonyms. No B-short rescore. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 30.
Forward from 09:44 close (not prior close), develop FLY $5-20 n=261: median ext_1159=0.0187. Gate requires median ext_1159>0 and frac reaching +1 ATR before OR-low >=0.35 (got 0.651). GATE=YES. FLY members still have leftover extension after 09:44 if median ext_1159>0 (median=0.0187); OR-low stop is tagged by 28% by 11:59.
GATE=YES.

- cell0945|flat1159: develop $-133.88/day holdout $-36.66/day n_hold=144 avgR=-0.029 t=-0.30 peak_conc=8 skipped=False shelve=False.
- cell0945|hold05: develop $-120.10/day holdout $-152.37/day n_hold=144 avgR=-0.118 t=-1.57 peak_conc=8 skipped=False shelve=False.
- cell0945|atr1559: develop $-141.29/day holdout $-4.81/day n_hold=144 avgR=-0.005 t=-0.05 peak_conc=8 skipped=False shelve=False.
- flush_0944|flat1159: develop $7.55/day holdout $0.79/day n_hold=17 avgR=0.027 t=0.02 peak_conc=2 skipped=False shelve=False.
- flush_orh|flat1159: develop $0.00/day holdout $0.00/day n_hold=0 avgR=0.000 t=0.00 peak_conc=0 skipped=False shelve=False.
- launch_compat|flat1159: develop $-8.19/day holdout $-31.68/day n_hold=11 avgR=-0.315 t=-0.94 peak_conc=2 skipped=False shelve=True.
- COMBINED B_uptick10|atr1559+flush_0944|flat1159: develop $90.20/day holdout $233.99/day (holdout not EV).

## 2026-09-09T19:43:52-04:00 — Arrow 31

VERDICT: FAIL — no Arrow 31 book has holdout >= $200/day AND non-red develop. Combined holdout is not expected value (EV).

Integrity repairs A1-A7 and C-R1-R7. Rescored flush|max6|repaired and B_uptick10 trail locked vs full. No new engine. No rocket rings. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 32.
Honesty: repaired flush and locked trail are both-green on the printed slices.
A1 look-ahead rejected n=18 PnL$=1473.78.
C-R3 stitch 04:00 flat n=214/94  07:30 flat n=223/92 vs A27 204/75. Neither champion.
- flush|max6|repaired: develop $6.20/day holdout $79.10/day n_hold=19 MFE-capture=0.369
- B|uptick10|flat1159|lock: develop $8.36/day holdout $160.35/day n_hold=94 MFE-capture=0.234 IWM skip=0
- B|uptick10|atr1559|lock: develop $70.09/day holdout $169.55/day n_hold=94 MFE-capture=0.217 IWM skip=0
- B|uptick10|atr1559|full: develop $70.09/day holdout $171.24/day n_hold=95 MFE-capture=0.218 IWM skip=0
COMBINED lock develop $76.30 holdout $248.65 NOT EV
FULL develop $76.30 holdout $250.35 NOT EV

## 2026-09-09T20:20:53-04:00 — Arrow 32

VERDICT: HOLD OUT CLEARS $200 WITH NON-RED DEVELOP — B|atr150|lock

B-short conjunction and trail rings on the A31 lock. A1-A5 on. last_entry_at=11:59. No flush rings. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 33.
Id 0 is the A31 lock reprint. B|atr150|lock is the $200 pass (develop not red). COMBINED uses the brief's best develop-not-red B (B|conj|atr1559|lock), not the pass book. Combined holdout is not EV.
Id 0 vs A31 B|uptick10|atr1559|lock: develop 216/216 holdout 94/94 — within ±10%.
Id 1 vs id 0 filled: develop added=7 dropped=0 holdout added=0 dropped=0 trades 244/216 and 98/94 cap8-displace_sess=1

- B|uptick10|atr1559|lock: develop $70.09/day holdout $169.55/day n_hold=94 MFE-capture=0.217 IWM skip=0
- B|conj|atr1559|lock: develop $73.03/day holdout $177.63/day n_hold=98 MFE-capture=0.220 IWM skip=0
- B|atr075|lock: develop $54.04/day holdout $160.90/day n_hold=95 MFE-capture=0.214 IWM skip=0
- B|atr150|lock: develop $26.46/day holdout $206.64/day n_hold=94 MFE-capture=0.246 IWM skip=0
- B|arm05|lock: develop $65.30/day holdout $134.80/day n_hold=96 MFE-capture=0.187 IWM skip=0
- B|unarmed20|lock: develop $-30.84/day holdout $65.52/day n_hold=97 MFE-capture=0.105 IWM skip=0
COMBINED B|conj|atr1559|lock+flush|max6|repaired develop $79.23 holdout $256.74 NOT EV

## 2026-09-09T21:02:05-04:00 — Arrow 33

VERDICT: FAIL — no Arrow 33 book has holdout >= $200/day AND non-red develop. Combined holdout is not expected value (EV).

Hygiene, cap/rank on A32 conjunction lock, develop depth rollup. Do not promote atr150. No flush rings. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 34.
Do not promote A32 atr150. Frozen leader is B|conj|atr1559|lock. COMBINED uses best develop-not-red B (B|conj|atr1559|lock, develop $72.57/day) + A31 flush reprint. Combined holdout is not EV.
Id 0 vs A32 B|conj|atr1559|lock: develop 228/244 holdout 93/98 — within ±10%.
RVOL skip share=0.071 (42/590).
drift_elig (prior_close [10,30] Lab-A band) develop n=191 holdout n=70 vs A27 B_uptick10 holdout 75 and A32 conj holdout 98. Not a champion.
Leftover lever: the door — leader covers little of the gap/OR field.

- B|conj|atr1559|lock: develop $72.57/day holdout $175.40/day n_hold=93 MFE-capture=0.230 IWM skip=0
- B|conj|cap12: develop $64.34/day holdout $134.90/day n_hold=109 MFE-capture=0.159 IWM skip=0
- B|conj|cap16: develop $41.55/day holdout $142.46/day n_hold=113 MFE-capture=0.163 IWM skip=0
- B|conj|rank_gap: develop $38.19/day holdout $132.44/day n_hold=93 MFE-capture=0.178 IWM skip=0
- B|conj|rank_rvol: develop $37.04/day holdout $142.91/day n_hold=93 MFE-capture=0.192 IWM skip=0
- B|conj|rank_orw: develop $47.32/day holdout $146.55/day n_hold=93 MFE-capture=0.200 IWM skip=0
- drift_elig: develop $-6.56/day holdout $63.77/day n_hold=70 MFE-capture=0.110 IWM skip=0
COMBINED B|conj|atr1559|lock+flush|max6|repaired develop $78.77 holdout $254.50 NOT EV

## 2026-09-09T21:56:41-04:00 — Arrow 34

VERDICT: FAIL — no Arrow 34 flush book has holdout >= $200/day AND non-red develop. Combined holdout is not expected value (EV).

ATR trail on A31 flush|max6|repaired. Door frozen. B-short not rescored. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 35.
Door frozen (A31 flush|max6|repaired). B-short not rescored; COMBINED uses A33 B|conj|atr1559|lock reprint (develop $72.57/day) + best develop-not-red flush (flush|max6|atr1330). Good-look diagnostic (develop>=$25 and MFE-capture>=0.30, not the pass line): none. Combined holdout is not EV.
Id 0 develop n=21 vs A31 n=21 — within ±3.

- flush|max6|flat1159: develop $6.20/day holdout $79.10/day n_hold=19 MFE-capture=0.369 reached_1R=0.263
- flush|max6|atr1559: develop $-10.41/day holdout $36.42/day n_hold=19 MFE-capture=0.226 reached_1R=0.368
- flush|max6|arm05: develop $1.88/day holdout $27.23/day n_hold=19 MFE-capture=0.188 reached_1R=0.263
- flush|max6|atr15: develop $-8.15/day holdout $62.45/day n_hold=19 MFE-capture=0.343 reached_1R=0.368
- flush|max6|atr1330: develop $11.13/day holdout $36.05/day n_hold=19 MFE-capture=0.241 reached_1R=0.368
COMBINED B|conj|atr1559|lock+flush|max6|atr1330 develop $83.70 holdout $211.45 NOT EV

## 2026-09-10T07:06:04-04:00 — Arrow 35

Diagnostic. No new engine. No $200 verdict on a book. No B-short rescore. No flush rings. No $500/idea. No virgin pull. Holdout tables are PEEK. Combined holdout is not EV. No Arrow 36.
On develop, confirmed-launch rocket-days (n=2809, prior_close $1-20) posted 10014.1 pct-points of harvestable altitude from the first fillable bar (median 0.89pp) versus 51457.4 pct-points of Arrow 30 sea-level gross (prior close, max high after launch − 1R). Sit-able share of that mountain for a next-open engine is 19.5% — the rest is either the 1R haircut from a later fillable price or premarket wick that is gone before 09:45. Arrow 30's never-sit hours (04-07 and after 12:00) held 53.3% of sea-level gross; a next-open book can still sit the 04-07 launches at 09:45, so harvestable is the honest leftover, not the specialist's 0.6% flush coverage. Holdout tables are PEEK, not a tuner. Holdout is not EV.
Frozen five (develop): minutes_since_launch rho=+0.6275, ext rho=+0.2824, orw rho=+0.2719, vwap_rel rho=+0.2042, was_rocket_prev rho=+0.1486
Develop members n=59679  holdout members n=30001  GATE=NO
COMBINED B|conj|atr1559|lock+flush|max6|repaired develop $78.77 holdout $254.50 NOT EV (reprint)

## 2026-09-10T07:45:36-04:00 — Arrow 36

VERDICT: FAIL — no Arrow 36 birth book has holdout >= $200/day AND non-red develop (ids with develop n < 40 are SHELVED). Combined holdout is not expected value (EV).

Ungated RTH confirmed-launch birth on one-minute bars. No cell. No score gate. No RVOL floor. No B-short rescore. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 37.
Ungated RTH confirmed launch. No cell. No score gate. No RVOL floor. B-short not rescored; COMBINED uses A33 B|conj|atr1559|lock reprint (develop $72.57/day) + A31 flush control reprint (flush|max6|repaired) because no develop-not-red birth id with n>=40. Combined holdout is not EV.

- birth|0945-1159|flat1159: develop $-23.03/day holdout $-181.09/day n_dev=323 n_hold=167 MFE-capture=-0.155 reached_1R=0.281
- birth|0945-1159|atr1559: develop $-176.93/day holdout $49.60/day n_dev=370 n_hold=189 MFE-capture=0.031 reached_1R=0.429
- birth|0945-1029|flat1159: develop $-45.62/day holdout $-114.77/day n_dev=241 n_hold=123 MFE-capture=-0.126 reached_1R=0.293
- birth|1030-1159|flat1159: develop $-137.13/day holdout $-192.99/day n_dev=206 n_hold=96 MFE-capture=-0.417 reached_1R=0.188
- birth|1200-1500|atr1559: develop $-199.56/day holdout $39.07/day n_dev=225 n_hold=97 MFE-capture=0.051 reached_1R=0.464
COMBINED B|conj|atr1559|lock+flush|max6|repaired develop $78.77 holdout $254.50 NOT EV (reprint)

## 2026-09-10T09:00:59-04:00 — Arrow 37

VERDICT: FAIL — no Arrow 37 continuation book has holdout >= $200/day AND non-red develop (ids with develop n < 40 are SHELVED). Combined holdout is not expected value (EV).

Noon hold / afternoon continuation. Did not rerun A36 afternoon birth. No cell. No score gate. No B-short rescore. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 38.
Noon hold / afternoon continuation. Did not rerun A36 afternoon birth. No cell. No score gate. B-short not rescored; COMBINED uses A33 B|conj|atr1559|lock reprint (develop $72.57/day) + A31 flush control reprint (flush|max6|repaired) because no develop-not-red id with n>=40. Combined holdout is not EV.

- noon|tight|atr1559: develop $-154.25/day holdout $-51.91/day n_dev=107 n_hold=53 MFE-capture=-0.144 reached_1R=0.340
- noon|tight|flat1330: develop $-127.55/day holdout $-37.04/day n_dev=107 n_hold=53 MFE-capture=-0.124 reached_1R=0.245
- noon|loose|atr1559: develop $-167.16/day holdout $-6.26/day n_dev=220 n_hold=97 MFE-capture=-0.009 reached_1R=0.392
- relaunch|atr1559: develop $-16.66/day holdout $-20.44/day n_dev=130 n_hold=64 MFE-capture=-0.091 reached_1R=0.094
- power|1430|flat1559: develop $-11.56/day holdout $24.59/day n_dev=14 n_hold=5 MFE-capture=1.676 reached_1R=0.000 SHELVE
COMBINED B|conj|atr1559|lock+flush|max6|repaired develop $78.77 holdout $254.50 NOT EV (reprint)

## 2026-09-10T09:27:34-04:00 — Arrow 38

VERDICT: FAIL — no Arrow 38 reclaim book has holdout >= $200/day AND non-red develop (ids with develop n < 40 are SHELVED). Combined holdout is not expected value (EV).

Premarket-high reclaim after the open wash. Did not rerun 36 or 37. No cell. No score gate. No B-short rescore. No $500/idea. No virgin pull. Combined holdout is not EV. No Arrow 39.
Premarket-high reclaim after the open wash. Did not rerun 36 birth or 37 noon hold. No cell. No score gate. B-short not rescored; COMBINED uses A33 B|conj|atr1559|lock reprint (develop $72.57/day) + A31 flush control reprint (flush|max6|repaired) because no develop-not-red id with n>=40. Combined holdout is not EV.

- pmrecl|dip3|flat1159: develop $-21.27/day holdout $-35.05/day n_dev=23 n_hold=29 MFE-capture=-0.193 reached_1R=0.207 SHELVE
- pmrecl|dip3|atr1559: develop $-5.19/day holdout $-57.61/day n_dev=32 n_hold=43 MFE-capture=-0.231 reached_1R=0.186 SHELVE
- pmrecl|dip2|flat1159: develop $-49.07/day holdout $-20.10/day n_dev=36 n_hold=39 MFE-capture=-0.078 reached_1R=0.231 SHELVE
- pmrecl|dip3|rvol3: develop $-11.29/day holdout $-58.04/day n_dev=9 n_hold=19 MFE-capture=-0.953 reached_1R=0.053 SHELVE
COMBINED B|conj|atr1559|lock+flush|max6|repaired develop $78.77 holdout $254.50 NOT EV (reprint)

## 2026-09-10T11:10:32-04:00 — Arrow 40

VERDICT: HOLD OUT CLEARS $200 WITH NON-RED DEVELOP — B200|F200, B200|F400, B200|F600, B400|F400, Bbud|Fbud|1600, Bbud|Fbud|2400

Session risk budget on frozen B conjunction lock + repaired flush. No new door. No Arrow 39. No atr150. No virgin pull. Combined holdout is not EV. No Arrow 41.
Frozen doors only (A33 B|conj|atr1559|lock + A31 flush|max6|repaired). Sized off intraday peak-to-trough, not daily-close DD. Good-look (combined develop>=$150 and joint intraday maxDD<3% of $100k, not the pass line): none. Do not write that $400 flush is safe because daily-close DD was small. Combined holdout is not EV.
Id 0 B n develop 228/228 holdout 93/93 — within ±10%. Id 0 flush n develop 21/21 holdout 19/19 — within ±3.

- B200|F200: develop $78.77/day holdout $254.50/day B n_hold=93 flush n_hold=19 intraday DD$=-1589.38 (1.59%) joint_peak$=1912 MFE-capture=0.260
- B200|F400: develop $77.14/day holdout $338.96/day B n_hold=93 flush n_hold=19 intraday DD$=-2605.91 (2.61%) joint_peak$=2312 MFE-capture=0.292
- B200|F600: develop $77.69/day holdout $346.61/day B n_hold=93 flush n_hold=19 intraday DD$=-2705.56 (2.71%) joint_peak$=2379 MFE-capture=0.289
- B400|F400: develop $174.95/day holdout $431.69/day B n_hold=93 flush n_hold=19 intraday DD$=-2686.26 (2.69%) joint_peak$=2916 MFE-capture=0.297
- Bbud|Fbud|1600: develop $70.29/day holdout $297.28/day B n_hold=91 flush n_hold=18 intraday DD$=-1091.76 (1.09%) joint_peak$=1596 MFE-capture=0.290
- Bbud|Fbud|2400: develop $96.69/day holdout $342.43/day B n_hold=93 flush n_hold=19 intraday DD$=-2750.78 (2.75%) joint_peak$=2152 MFE-capture=0.271

## 2026-09-10T14:56:06-04:00 — Arrow 41

VERDICT: INGEST ONLY — no $200 verdict. Did not score engines.

Virgin 04:00-16:00 1-minute tape under data/virgin/. Warmup last 10 NYSE 2025 (2025-12-17..2025-12-31, not scored). Study first 2026 session through last full May (2026-01-02..2026-05-29; all of January in study). Prior close [$1, $80], prior DV >= $1M; $10M is a filter column not an ingest wall. IWM bench 04:00-16:00. Did not touch data/full or Lab A data/bars. No Arrow 42.

sessions=112 name-days=340057 unique=5328 1m_rows=244841040 mean_bars=720.0 pdv_ge_10m=181614 prior_close_gt_50=48400 pulled=340057 empty=0 missing=0 failures=0 iwm=112/112 wall_min=155.7

## 2026-09-10T16:24:16-04:00 — Arrow 42

VERDICT: FAIL — combined frozen books do not print >= $200/day on the virgin window. This window is the first unstained look; it is still one sample of weather, not EV.

One look on data/virgin/. Frozen $200/$200 A33 B|conj|atr1559|lock + A31 flush|max6|repaired. Score 2026-01-02..2026-05-29 as one window. Did not split and pick. Did not change doors. Did not touch data/full or Lab A data/bars. Combined dollars are not EV. No Arrow 43.
COMBINED $/day=-172.52 n_B=469 n_flush=89 IWM alpha $-155.55 skip=0 NOT EV
B|pdv>=$10M $/day=-160.29 n=469
B|$20-80|pdv>=$10M $/day=-52.82 n=368

## 2026-09-10T18:05:20-04:00 — Arrow 43

VERDICT: FAIL — no Arrow 43 clock book has OOS >= $100/day AND non-red IS. Slate $200 is not this arrow's job.

Clock split. Three frozen books: on_long, on_short, rth_long. Odd months IS, even months OOS, split on entry session. Combined virgin Jan–May + full Jun–Aug. Did not retune B|conj|atr1559|lock or flush|max6|repaired. No new ingest. Did not touch Lab A data/bars. Combined of the three is a side line, not a slate. No Arrow 44.
- on_long: IS $-45.25/day n=1849  OOS $-53.71/day n=1598  no seat
- on_short: IS $-158.58/day n=1849  OOS $-127.00/day n=1598  no seat
- rth_long: IS $-79.04/day n=1887  OOS $-109.62/day n=1644  no seat

## 2026-09-10T18:30:52-04:00 — Arrow 44

VERDICT: FAIL — res_ls does not have OOS >= $100/day AND non-red IS. Legs are diagnostics. Slate $200 is not this arrow's job.

Weekly residual vs IWM. Long 15 worst / short 15 best, 5-session hold. Odd months IS, even months OOS, split on entry session. Combined virgin Jan–May + full Jun–Aug. Did not retune Arrow 43 clocks or B|conj|atr1559|lock or flush|max6|repaired. No new ingest. Did not touch Lab A data/bars. Legs are diagnostics. No Arrow 45.
- res_long: IS $-67.52/day n=283  OOS $-71.20/day n=224  no seat
- res_short: IS $246.77/day n=272  OOS $-1.37/day n=218  no seat
- res_ls: IS $179.26/day n=555  OOS $-72.57/day n=442  no seat

## 2026-09-10T18:56:51-04:00 — Arrow 45

VERDICT: FAIL — no Arrow 45 short ring has OOS >= $100/day AND non-red IS. Slate $200 is not this arrow's job.

Id 0 n15_h5 IS $/day=246.77/246.77 n=272/272 — within ±10% of Arrow 44 res_short.
Lift vs control on both IS and OOS: n15_h10.
Short only residual winners. Rings locked from IS. One OOS look. Did not use an OOS month to pick a threshold. Did not bring back res_long. Did not retune Arrow 43 clocks or frozen B/flush. No new ingest. No Arrow 46.
- n15_h5: IS $246.77/day n=272  OOS $-1.37/day n=218  no seat
- n10_h5: IS $235.76/day n=180  OOS $29.26/day n=145  no seat
- n8_h5: IS $186.11/day n=143  OOS $52.43/day n=116  no seat
- n15_h5_r04: IS $246.77/day n=272  OOS $-1.37/day n=218  no seat
- n15_h5_r08: IS $246.77/day n=272  OOS $-1.37/day n=218  no seat
- n15_h10: IS $281.72/day n=262  OOS $19.64/day n=198  no seat  lift-both

## 2026-09-10T19:21:20-04:00 — Arrow 46

VERDICT: SEAT — n15_lb10_h10 (OOS >= $100/day and IS not red). Slate $200 is not this arrow's job.

Id 0 n15_h10 IS $/day=281.72/281.72 n=262/262 — within ±10% of Arrow 45 n15_h10.
Lift vs control on both IS and OOS: none.
Short only. Hold 10. Rings locked from IS. One OOS look. Did not use an OOS month to pick a threshold. Did not add a long leg. Did not retune Arrow 43 clocks or frozen B/flush. No new ingest. No Arrow 47.
- n15_h10: IS $281.72/day n=262  OOS $19.64/day n=198  no seat
- n10_h10: IS $252.27/day n=171  OOS $78.60/day n=132  no seat
- n8_h10: IS $189.78/day n=135  OOS $88.00/day n=105  no seat
- n15_lb10_h10: IS $220.99/day n=260  OOS $122.66/day n=197  SEAT
- n15_h10_r15: IS $304.30/day n=247  OOS $19.64/day n=198  no seat
- n8_h10_r15: IS $189.83/day n=134  OOS $88.00/day n=105  no seat

## 2026-09-10T19:41:21-04:00 — Arrow 47

VERDICT: SEAT — n15_lb10_h10, n8_lb10_h10, n15_lb10_h5, n15_lb10_h10_r20, n15_lb10_h10_3k (OOS >= $100/day and IS not red). Slate $200 is not this arrow's job.

Id 0 n15_lb10_h10 IS $/day=220.99/220.99 n=260/260 — within ±10% of Arrow 46 n15_lb10_h10.
Lift vs control on both IS and OOS: n15_lb10_h10_3k.
Id 3 n15_lb10_h5 OOS $109.01/day kept the OOS lift (>= $100).
Id 5 $3k / id 0 $2k scale IS 1.50x OOS 1.50x vs linear 1.50x. Near-linear.
Short only. lb=10. Rings locked from IS. One OOS look. Did not use an OOS month to pick a threshold. Did not add a long leg. Did not retune Arrow 43 clocks or frozen B/flush. No new ingest. No Arrow 48.
- n15_lb10_h10: IS $220.99/day n=260  OOS $122.66/day n=197 t=1.39  SEAT
- n10_lb10_h10: IS $141.81/day n=170  OOS $96.69/day n=131 t=1.45  no seat
- n8_lb10_h10: IS $122.94/day n=135  OOS $102.47/day n=104 t=1.56  SEAT
- n15_lb10_h5: IS $137.97/day n=268  OOS $109.01/day n=206 t=1.50  SEAT
- n15_lb10_h10_r20: IS $232.46/day n=258  OOS $122.66/day n=197 t=1.39  SEAT
- n15_lb10_h10_3k: IS $332.58/day n=260  OOS $184.38/day n=197 t=1.39  SEAT  lift-both
