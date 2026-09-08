# Build Arrow 15 — twelve distinct short hypotheses on the live cell

Read `docs/SUCCESS.md`, `reports/arrow13_results.txt`, `reports/arrow14_results.txt` if present, `reports/RESEARCH_LOG.md` first.

Pass = holdout ≥ $200/day **and** develop not red. Tracks A and B, 42/22. No 12:00–16:00. **Short only.** Do not rerun Arrow 13 longs.

James's charge: prior arrows under-used the search. This arrow is **twelve different doors**, not one door and five knobs. Informed by the live cell. Not a random indicator dump. Not ML.

## Shared population (unless an id says otherwise)

`dv_rank ≥ 0.80`, gap-down `≥ 1.5%`, 15-min OR width `> 2.5%`, `ema15` short-stack at signal time. Flatten 11:59. `RISK_PER_IDEA = 200`.

**Book:** if Arrow 14 `cap8` did not turn develop red on the kernel, use **cap8** (8 / 16 / $1600). If cap8 diluted the kernel, use **cap5** and say so in the report header.

## Twelve short-only ids

Control is id 1 (the Arrow 13 winner). Every other id must differ by **entry logic or a structural filter**, not only 2R/trail/seats.

| id | door |
|---|---|
| 1 | **control** — first completed 5-min close below ema9 after 09:45. Stop = max(OR high, that 5-min high) |
| 2 | first completed 5-min close below **ema21** (slower average) |
| 3 | **two consecutive** 5-min closes below ema9 |
| 4 | 5-min close below ema9 whose **high tagged ema9** (rejection at the average, then close under) |
| 5 | first **10-min** close below ema9 after 09:45 |
| 6 | first 5-min close below ema9 **at or after 10:00** (ignore 09:45–09:59) |
| 7 | first 1-min close below the **15-min OR low** after 09:45 (classic range break, same pop) |
| 8 | 5-min close below ema9 **and** that close is below **OR mid** |
| 9 | after 09:45, 5-min **lower high** then close below the prior 5-min low (market structure, stop = that lower high) |
| 10 | first 5-min close below **RTH VWAP** after 09:45, still in this pop |
| 11 | same as control, plus **bearish location**: 09:44 close in the lower half of the OR |
| 12 | same as control, plus **volume**: first-15-min dollar volume ≥ median first-15 of that name's prior 10 sessions |

No 13th id. No long ids. 2R/trail only if you have leftover wall time after these twelve; do not substitute them for a door.

## Outputs

- `reports/arrow15_results.txt` — two-sided pass; table track × id; n vs id 1; which doors beat control on **both** slices.
- Append `reports/RESEARCH_LOG.md` with doors that added a *different* path vs knobs that did nothing.
- Tests: id 3 silent after a single close under ema9; id 6 silent on a 09:50-only cross; id 9 silent if 5-min highs are rising; shorts only.

Commit code + reports. No parquet. No Arrow 16.
