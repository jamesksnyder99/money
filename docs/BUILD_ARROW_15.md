# Build Arrow 15 — keep the paying short; memory, candles, and longs that are not a flip

Read `docs/SUCCESS.md`, `reports/arrow14_results.txt`, `reports/RESEARCH_LOG.md` first.

Pass = holdout ≥ $200/day **and** develop not red. Tracks A and B, 42/22. No 12:00–16:00.

Do **not** throw away the live short. Arrow 14 `B/c5_ema9|cap8` is develop **+$59** / holdout **+$179**. That is failure vs $200 and it is also the best two-sided object we have. Id 1 is that exact book. Cap8 (8 / 16 / $1600), RISK_PER_IDEA=200, flatten 11:59.

Do not rerun Arrow 13 pullback / VWAP-reclaim / quiet-OR longs (avgR ≈ −1 to −2). Do not rerun union, 11:30 flatten, Q4, or cap10-as-the-idea.

James: 9/21 is one stack, not climate. Memory of what just printed, and the anatomy of the bar that fires, are fair tech. Stocks generally lift; a lab that only pays on the short side is incomplete. Longs in this arrow must be **different machines**, not `side = +1` on id 1.

## Helpers to build (use in the ids below)

- **Memory (5-min, current session, completed bars only):** last 3 completed 5-min highs/lows/closes; count of consecutive down closes; whether the last two 5-min highs are descending.
- **Candle (the signal 5-min or 1-min bar):** `body = abs(close-open)`; `range = high-low`; `close_loc = (close-low)/range`; upper wick, lower wick. A **weak close** is close_loc ≤ 0.25. A **strong close** is close_loc ≥ 0.75. A **hammer-like** bar is lower wick ≥ 2× body and close_loc ≥ 0.6.
- **Anchored VWAP** from the 09:30 RTH open (typical × volume, RTH only).

## Twelve experiments

**Short 1–6** — `side = -1` only. Shared pop unless noted: `dv_rank ≥ 0.80`, gap-down `≥ 1.5%`, OR width `> 2.5%`.

| id | idea |
|---|---|
| 1 | **control** — exact Arrow 14 B kernel: ema9 < ema21 and first 5-min close below ema9 after 09:45. Stop = max(OR high, that 5-min high). cap8 |
| 2 | control entry **plus memory**: last two completed 5-min highs are descending |
| 3 | control entry **plus candle**: the signal 5-min bar is a weak close (close_loc ≤ 0.25) |
| 4 | no 9/21 required. Door = first 5-min close below **09:30-anchored VWAP** after 09:45, weak close. Same pop. Stop = max(OR high, bar high) |
| 5 | no 9/21 required. Door = 5-min **lower high then close below prior 5-min low** (structure). Same pop. Stop = that lower high |
| 6 | control pop, door = first 5-min bar with **body ≥ 0.6 × its range** and close below the bar open and below ema9 (decisive down candle through the average) |

**Long 7–12** — `side = +1` only. Not a flipped short.

| id | idea |
|---|---|
| 7 | **Washout hammer:** Q5, gap-**down** ≥ 1.5% (same bruised names), OR width > 2.5%. After 09:45 a 5-min **hammer-like** bar whose low is at or below OR low, close back **inside** the OR. Stop = that low. This is a bounce of a dump, not a trend-up stack |
| 8 | **Hold the open:** Q5, gap-**up** ≥ 1.5%, 09:44 close in the **top half** of the OR. After 09:45 first 5-min **strong close** that holds above OR mid. Stop = OR mid. No ema stack required |
| 9 | **Memory grind-up:** Q5, `|gap| < 1%`, last three completed 5-min closes each higher, last bar strong close. Enter that close. Stop = lowest low of those three 5-min bars |
| 10 | **Anchored VWAP reclaim after a dip:** Q5, gap-up ≥ 1%. Lose 09:30 AVWAP once after 09:45, then a 5-min **strong close** back above it. Stop = that 5-min low. Not Arrow 13's 1-min VWAP reclaim |
| 11 | **Prior-day high break with a real body:** Q5, prior session morning high from stats. After 09:45 a 5-min close above that high with body ≥ 0.5 × range and strong close. Stop = that 5-min low |
| 12 | **ema long + hammer only:** Q5, ema9 > ema21, after 09:45 a hammer-like 5-min that tags ema9 and closes strong. Stop = hammer low. The only long that may use 9/21 |

No 13th. Score A and B separately. Header must print cap used and that id 1 is the preserved kernel.

## Outputs

- `reports/arrow15_results.txt` — two-sided pass; table track × id × side; n vs id 1 on shorts; call out any long that is green on **both** slices.
- Append `reports/RESEARCH_LOG.md`.
- Tests: weak-close rejects close_loc=0.8; hammer rejects a long-upper-wick bar; descending-high memory rejects rising 5-min highs; long helpers emit no shorts; id 1 still requires ema9 < ema21.

Commit code + reports. No parquet. No Arrow 16.
