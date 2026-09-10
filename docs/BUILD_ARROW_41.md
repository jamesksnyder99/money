# Build Arrow 41 — virgin ingest January–May 2026

Read `docs/DATA_CONTRACT.md`, `docs/SUCCESS.md`, `AGENTS.md`, `reports/tape17_ingest.txt`.

This arrow is **ingest only**. Do not score engines. Do not tune. Do not touch `data/full/` or Lab A `data/bars/`.

## Window

- Warmup: **first 10 NYSE trading days of 2026** (do not score later; they exist for prior volume / EMA stitch).
- Study: the **11th** 2026 trading day through **2026-05-29** (last full session in May if the 29th is not a session).
- Keep holidays that exist; do not invent bars.

## Universe (pull)

- Stocks only, common stock, same ETP denylist as Arrow 17.
- Prior close **[$1, $80]** (keeps today’s $1–$50 names; adds $50–$80).
- Prior-day dollar volume **≥ $1,000,000**. **$10M is a column/filter, not an ingest wall.**
- Session **04:00–16:00** ET, one-minute UTP/CTA, 720-bar grid with zeros, same as `data/full/`.
- Also pull **IWM** 04:00–16:00 for the same dates into `data/virgin/bench/`.

## Store

`data/virgin/` (bars + manifest). Gitignore parquet. Resumable manifest. Theta ≤8 concurrent, 429 backoff. Workers for write/validate. Heartbeat + ETA every 15 minutes.

Report: sessions, name-days, symbols, row count, bars/name-day, failures, wall time, how many name-days have PDV ≥ $10M, how many prior_close > $50.

## Outputs

`reports/tape41_ingest.txt`. Append RESEARCH_LOG.md.
No engine replay. No Arrow 42 in this commit (42 will be the one-look score).

Commit code + report + manifest if no secrets. No parquet.
