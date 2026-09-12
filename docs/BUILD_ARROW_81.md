# Build Arrow 81 — Wednesday H10 last-RTH adverse stop (IS / OOS)

Read `docs/SUCCESS.md`, `AGENTS.md`, `docs/DATA_CONTRACT.md`,
`docs/BUILD_ARROW_66.md`, `reports/arrow66_results.txt`,
`docs/BUILD_ARROW_71.md`, `reports/arrow71_results.txt`,
`docs/BUILD_ARROW_65.md`, `reports/arrow65_results.txt`,
`reports/tape17_ingest.txt`, `reports/tape41_ingest.txt`.

Same leftover short as Arrow 66 `h10_4k`. Same entries. Only the exit
can change. **Cash only. Do not replace** a flattened name with leftover
9–20 or with a new Wednesday name mid-hold. Do not retune rank, n,
weekday, ticket, or fill. Do not retune frozen B / flush.

Parent: Wednesday signal, eight largest 15-session close-to-close returns,
fill next session last-RTH, $4,000, hold-10 **backstop**, drop if the fill
bar is missing. Field $10–$80 PDV ≥ $10M ETP denylist.
MTM as Arrow 65. Split on the **signal** Wednesday. Odd months IS, even OOS.
Jan–Aug 2026 only (virgin + full). Do not mix Sep–Dec 2025.
Reuse `src/research/clock.py`.

OOS is one look. Do not drop an id after seeing OOS.
Do not use an OOS month to pick a percent.
The four stops below are frozen. Do not search a fifth percent.

Acronyms: IS = in-sample; OOS = out-of-sample; PDV = prior-day dollar
volume; IWM = iShares Russell 2000 ETF; RTH = regular trading hours;
EV = expected value; SSR = Short Sale Restriction; CI = confidence interval;
MTM = mark-to-market.

## Stop (known at last-RTH)

Each session the name is still on, after that last-RTH exists:

If last-RTH ≥ fill × (1 + k), cash at that last-RTH (same cost model as
any exit). k ∈ {0.03, 0.06, 0.09, 0.12}.

This is **not** a 1-minute wick stop. Do not flatten on an intra-session
high that closed below the trigger.
Day 10 last-RTH is always an exit if still on.
Empty slot stays empty until the next Wednesday rank.

This is not Arrow 71 rule B (k = 0). Do not add k = 0.

## Ids (frozen — do not add a 6th)

| id | k |
|---|---|
| 0 `h10_4k` | none | control. Reprint Arrow 66 `h10_4k` IS MTM $/day within ±10% and n within ±10% of 116 |
| 1 `stop_3` | 3% |
| 2 `stop_6` | 6% |
| 3 `stop_9` | 9% |
| 4 `stop_12` | 12% |

## Order of work

1. Id 0 reprint. If it misses the band, stop and fix.
2. IS character on id 0 names: fraction that would have tripped 3 / 6 / 9 / 12%
   on each hold-day 1..10. Description. Does not pick an id.
3. Score all five. One OOS look.

Pass for a seat: OOS MTM $/day ≥ $100 **and** IS MTM not red.
Slate: OOS MTM ≥ $200 **and** IS MTM not red **and** peak live ≤ $100k.
A stop id beats id 0 only if it lifts MTM $/day on **both** IS and OOS
and does not worsen OOS max DD by more than 25%.
Print t, CI, mean hold, n stopped early. Say when a CI excludes 0.
Do not call a CI that includes 0 "EV."

## Report

`reports/arrow81_results.txt`.

First paragraph: reprint, which k beat id 0 on both slices, mean hold,
whether 3% is B-again (flattened winners) or 12% is inert.
Then each id × IS × OOS: entry $/day, MTM $/day, n, mean hold, stopped n,
hit, wins, losses, PF, t, CI, MTM DD, worst day, peak live, months.

Append RESEARCH_LOG.md.

Tests:
- id 0 hold 10, no stop (fixture);
- id 1 cashes a name whose last-RTH ≥ fill × 1.03 before day 10 (fixture);
- id 4 does not open a new leftover after a stop (fixture);
- even-month signal is not IS;
- do not read Lab A `data/bars/`.

Commit code + reports. No parquet. No Arrow 82.
