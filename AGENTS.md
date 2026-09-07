# Agent rules

- Never print, log, commit, or echo `.env` or credential values.
- Stocks Professional only unless the user says otherwise. No options, no bulk pulls, no flat files, no streaming unless asked.
- Prefer the official `thetadata` Python SDK (HTTPS/gRPC). Do not launch Theta Terminal unless asked.
- Keep data pulls small: one symbol, short date windows, snapshots — unless the user explicitly requests more.
