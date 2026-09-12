# Build Arrow 80 — open leftover, two frozen books, Sep 2025–Aug 2026

Read `docs/SUCCESS.md`, `AGENTS.md`, `docs/DATA_CONTRACT.md`,
`docs/BUILD_ARROW_79.md`, `reports/arrow79_results.txt`,
`docs/BUILD_ARROW_78.md`, `reports/arrow78_results.txt`,
`docs/BUILD_ARROW_68.md`, `reports/arrow68_results.txt`,
`docs/BUILD_ARROW_70.md`, `reports/arrow70_results.txt`,
`docs/BUILD_ARROW_65.md`, `reports/tape69_ingest.txt`,
`reports/tape67_ingest.txt`, `reports/tape41_ingest.txt`,
`reports/tape17_ingest.txt`.

One look of **two frozen** day books across the year already on disk.
Do not add a third book. Do not skip Tuesday. Do not gap-filter.
Do not retune Wednesday H10.

Chassis: 15-session leftover rank, fill first print ≥ **09:31**, exit last
print at **10:29**, $3,000, field $10–$80 PDV ≥ $10M ETP denylist. Short only.

H10 = Arrow 65/66: Wednesday signal, next last-RTH, $4,000, hold 10.
Complement = leftover eight minus names on H10 at 09:30.
Lookback may read August 2025. Jun–Aug 2026 bars from `data/full/`.
Sep 2025–May 2026 from `data/virgin/`.

Window: **2025-09-02 through 2026-08-31**. First session with 15 prior
sessions on tape (August warmup). Print 12 months. Print odd calendar
months vs even as courtesy — this year is **not** a new promotion split.
Jan–Apr 2026 already had a look; Sep–Dec 2025 and May–Aug 2026 are new
for this hotel. Do not drop a month after seeing it. Do not pick an id
from a month.

No new ingest. Do not touch Lab A `data/bars/`.

Acronyms: IS = in-sample; OOS = out-of-sample; PDV = prior-day dollar
volume; IWM = iShares Russell 2000 ETF; RTH = regular trading hours;
EV = expected value; SSR = Short Sale Restriction; CI = confidence interval;
MTM = mark-to-market.

## Ids (frozen — do not add a 3rd)

| id | who |
|---|---|
| 0 `all_0931` | eight leftover |
| 1 `comp` | leftover eight minus H10 live |

## Score

$/day = total PnL / NYSE sessions in 2025-09-02..2026-08-31, and by month.
Hit, W/L, PF, t, CI, peak live (~same-session).
Daily Pearson of each id vs H10 MTM on sessions both exist — year, fall
2025 (Sep–Dec), 2026 H10 window (Jan–Aug), and June 2026 alone.
Mean overlap / 8 of id 0 vs H10 live.

Say whether June is fat for the day book the way it is for H10.
Say whether September 2025 is a hole for the day book the way it is for H10.
Do not call the year a $200 slate pass. Do not call a CI that includes 0 "EV."

Jan–Apr id 0 should sit near Arrow 79 `all_0931` month tape. If January is
empty and April is a hole, stop and fix the seam.

## Report

`reports/arrow80_results.txt`.

First paragraph: year $/day both ids, September vs June vs H10, corr,
whether complement still looks like a second pulse on the new months.
Then 12-month table both ids. Then trade stats.

Append RESEARCH_LOG.md.

Tests:
- id 1 never shorts a name on H10 at 09:30 (fixture);
- fill is ≥ 09:31 (fixture);
- do not read Lab A `data/bars/`.

Commit code + reports. No parquet. No Arrow 81.
