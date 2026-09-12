# Build Arrow 68 — Wednesday H10 one-look on Sep–Dec 2025

Read `docs/SUCCESS.md`, `AGENTS.md`, `docs/DATA_CONTRACT.md`,
`docs/BUILD_ARROW_65.md`, `reports/arrow65_results.txt`,
`docs/BUILD_ARROW_66.md`, `reports/arrow66_results.txt`,
`docs/BUILD_ARROW_67.md`, `reports/tape67_ingest.txt`,
`reports/tape61_ingest.txt`, `reports/tape41_ingest.txt`.

One look of the **frozen** paper book on tape those arrows never scored.
Do not retune lookback, n, weekday, hold, ticket, or fill.
Do not walk rings. Do not use 2026 sessions as this window — Jan–Aug 2026
already had its IS/OOS look.

Frozen book: Wednesday signal, 15-session close-to-close (IWM subtract
is a scalar; rank = eight largest 15-session returns), short eight,
fill **next session last-RTH**, $4,000, hold 10 from the fill session,
drop a name if the exit bar is missing. Field $10–$80 PDV ≥ $10M ETP denylist.
MTM daily equity as Arrow 65.
Reuse `src/research/clock.py` and Arrow 65 fill/MTM path.

Window: signal Wednesdays whose 15-session lookback and fill/exit live on
`data/virgin/` from **2025-09-02 through 2025-12-31**.
First legal signal is the first Wednesday on or after 2025-09-02 that has
15 prior sessions on virgin (expect late September). Do not invent August 2025.
Last signal: last Wednesday in December 2025 whose 10-session exit is still
on or before 2025-12-31. If a December signal would exit in January 2026,
allow the exit to read January 2026 virgin (already on disk) and say so.

This window is **one slice**. Print odd months (Sep, Nov) and even months
(Oct, Dec) as a courtesy table. Do not treat them as IS/OOS for promotion.
Do not drop anything after seeing a month.

No new ingest. Do not touch Lab A `data/bars/` except to read a helper.
Do not touch `data/full/` (this window is virgin).

Acronyms: IS = in-sample; OOS = out-of-sample; PDV = prior-day dollar
volume; IWM = iShares Russell 2000 ETF; RTH = regular trading hours;
EV = expected value; SSR = Short Sale Restriction; CI = confidence interval;
MTM = mark-to-market.

## Ids (frozen — do not add a 2nd book)

| id | what |
|---|---|
| 0 `wed_h10_4k` | frozen paper book |

One id. Character: n signals, first/last signal date, n trades, months.

## Score

Print entry-attributed $/day **and** MTM $/day over the window (total PnL /
NYSE sessions in 2025-09-02..2025-12-31, and separately / sessions from first
signal through last exit).
Hit, wins, losses, avgWin, avgLoss, PF, se, t, CI on the MTM daily series.
MTM daily-close DD, worst day, peak live |shares × last|.
IWM alpha (book vs short IWM same notionals and calendar).
By month: Sep, Oct, Nov, Dec.
Say when a CI excludes 0. Do not call a CI that includes 0 "EV."
Do not call this window a pass/fail against the $200 slate rule as if it were
the original OOS. Report the dollars and whether the sign matches 2026.

## Report

`reports/arrow68_results.txt`.

First paragraph: first signal date, n, MTM $/day, months all green or not,
peak live, whether this looks like 2026 Wednesday H10 or not.

Append RESEARCH_LOG.md.

Tests:
- only one id;
- fill is next last-RTH not signal close (fixture);
- no signal before 15 prior sessions exist (fixture);
- 2026-01 through 2026-08 are not in the signal set;
- do not read Lab A `data/bars/`.

Commit code + reports. No parquet. No Arrow 69.
