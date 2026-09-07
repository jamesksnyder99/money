# Grok Build — how to work this repo

Read `AGENTS.md` and `docs/DATA_CONTRACT.md` before writing code.

## What to build first

1. Keep using `src/theta/client.py` for auth. Do not print `.env`.
2. Ingest CLI, e.g. `python -m scripts.ingest --mode pilot|eligibility|bars|validate`.
3. Fixture tests under `tests/` with tiny synthetic frames (no live credentials in CI).
4. Pilot path must work before any full-universe loop is enabled.

Do not treat “pull all history now” as the definition of done. Done is: correct contract, resumable writes, visible progress, validation report.

## Soft budgets

Budgets in the data contract are **not** hard stops. If a Build session is running long:

- Flush in-progress parquet + a manifest line.
- Print where to resume.
- Leave the CLI in a state the next session can continue without re-pulling ok partitions.

## Concurrency

Default Theta pulls serial. Parallelize CPU work and parquet writes. Document flags in `--help`.

## Progress

Stdout only (plus `reports/ingest_latest.txt` at end). Heartbeat ≤ 15 minutes on long jobs, with ETA.
