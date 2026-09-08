# Build Arrow 10 — hot cell from Arrow 9 + 5-min ORBR + two trend defs

Read `docs/SUCCESS.md`, `reports/arrow09_character.txt`, `reports/arrow09_results.txt`, `reports/RESEARCH_LOG.md` first.

Pass = holdout ≥ $200/day **and** develop not red. Same Tracks A/B, repaired engine, 42/22. No 12:00–16:00. Do not rerun Arrow 9's Q5+1–4% books or gap-fade.

## Answers already known (do not rediscover)

- **5-min ORBR + retest + trend:** not tested. We broke a **15-minute** range (09:30–09:44) without a retest. Different animal.
- **Trend:** one definition only, in `trend.py`: 10 prior official EOD closes; up = `C10 > C1` and `C10 > mean(C1..C10)`; down = inverse; else flat. Never 5-day, never 20-day, never SMA-only, never higher-high structure as the trend flag.

Arrow 9 character (develop): leftover range lives in **Q5 × |gap| ≥ 2% × OR width > 4%**. Session extremes cluster in the **11:00 hour**. Arrow 8/9 **excluded** OR > 4%. This arrow trades that cell and does not flatten at 11:00.

## Trend flags (compute both; do not invent a third)

- `eod10` — existing helper.
- `eod5` — same recipe on the **5** prior official EOD closes: up = `C5 > C1` and `C5 > mean(C1..C5)`.

If fewer than 5 priors, that name-day is flat for `eod5`.

## Hot cell (point-in-time, each session)

- `dv_rank ≥ 0.80` among that session's eligible names
- `|09:30 open / prior_close − 1| ≥ 0.02`
- 09:30–09:44 range / mid **> 0.04**

Small n (Arrow 9 develop ~576 A / 367 B name-days). That is intended.

## 5-min ORBR + retest (classic)

- Range = 09:30–09:34 high/low. Require range / mid ≥ 0.004 so it is not a flat print.
- **Break:** after 09:35, first tradeable close beyond the range.
- **Retest:** after that break, a later tradeable bar whose **low** comes back to the range high (long) or **high** comes back to the range low (short), without closing back through the far side of the range. Signal on that retest bar's close. Stop = far side of the 5-min range.
- If no retest by 11:00, no trade.
- Not a 15-min OR. Not a failed-break fade.

## Six experiments only

| id | population | entry | trend filter | manage |
|---|---|---|---|---|
| 1 | hot cell | 15-min OR break (09:45+ close beyond 09:30–09:44), stop other side | none | flatten 11:59 |
| 2 | hot cell | same 15-min break | none | 2R, else 11:59 |
| 3 | hot cell | same 15-min break | **eod10 with the break** (skip flat / against) | flatten 11:59 |
| 4 | dv_rank ≥ 0.80 | 5-min ORBR + retest | **eod10 with the break** | flatten 11:59 |
| 5 | dv_rank ≥ 0.80 | 5-min ORBR + retest | **eod5 with the break** | flatten 11:59 |
| 6 | hot cell | 5-min ORBR + retest | eod10 with the break | 2R, else 11:59 |

No 11:00 flatten. No 7th id. No ML.

## Outputs

- `reports/arrow10_results.txt` — two-sided pass; table track × id; counts of hot-cell name-days develop vs holdout.
- Append `reports/RESEARCH_LOG.md` noting 5-min ORBR and eod5 are first looks.
- Tests: 5-min ORBR silent with no retest; silent if range is a flat print; eod5 up/down/flat on a 5-close fixture; hot-cell rejects OR width 3%.

Commit code + reports. No parquet. No Arrow 11.
