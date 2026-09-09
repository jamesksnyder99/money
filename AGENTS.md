# Agent rules

- Never print, log, commit, or echo `.env` or credential values.
- Stocks Professional only unless the user says otherwise. No options, no bulk/flat files, no streaming, no tick or sub-minute bars unless asked.
- Prefer the official `thetadata` Python SDK (HTTPS/gRPC). Do not launch Theta Terminal unless asked.
- Follow `docs/DATA_CONTRACT.md`. Universe is the eligibility rules (prior close $1–$30, prior-day dollar volume ≥ $1M, common stock), not an arbitrary 50-name cap.
- Economic rule is `docs/SUCCESS.md`: target $300–$500 net per trading day average on $100k; below $200/day average is failure. Do not optimize for pretty backtests that cannot clear $200.
- **Granularity law:** read and act on the finest tape we have (one-minute bars now). A higher timeframe (5-minute, 15-minute) is allowed only when a scored side-by-side shows gain versus twitching on one-minute. Default doors, stops, and trails are one-minute. Fifteen-minute EMA regime is a stance, not an execution clock, and must still be justified or replaced.
- Keep live pulls resumable. Pilot (5 symbols × 5 days) before full Jun–Aug + warmup ingest.
- Parallelize by default: multi-core workers for local compute, parquet, tape replay, validation, and independent subprocesses. Theta pulls use up to 8 concurrent requests (Pro cap) with backoff on 429. Serial loops need a reason.
- Long jobs: stdout heartbeat at least every 15 minutes with an ETA estimate. Soft time budgets are hints, not kill switches — checkpoint and resume.
- Do not commit `data/`, parquet, or secrets. Manifests and reports may be committed if they contain no credentials.
- Every new or changed file Build commits is audited by Grok before the next arrow is written. Prefer small, reviewable commits over one opaque dump.
- Expand acronyms on first use in briefs and reports.
