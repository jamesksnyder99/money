"""Research CLI. See docs/BUILD_ARROW_03.md."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from research.arrow3 import run_arrow3  # noqa: E402
from research.arrow4 import run_arrow4  # noqa: E402
from research.arrow5 import run_arrow5  # noqa: E402
from research.arrow6 import run_arrow6  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    cpu = os.cpu_count() or 1
    p = argparse.ArgumentParser(description="Lab A research replay")
    p.add_argument(
        "--mode",
        choices=("arrow3", "arrow4", "arrow5", "arrow6"),
        default="arrow6",
        help="arrow5 and arrow6 are both valid; arrow6 is repaired engine + optional trend",
    )
    p.add_argument("--workers", type=int, default=min(8, cpu), help="default min(8, cpu_count)")
    args = p.parse_args(argv)
    if args.mode == "arrow3":
        return run_arrow3(workers=args.workers)
    if args.mode == "arrow4":
        return run_arrow4(workers=args.workers)
    if args.mode == "arrow5":
        return run_arrow5(workers=args.workers)
    if args.mode == "arrow6":
        return run_arrow6(workers=args.workers)
    raise SystemExit(f"unknown mode {args.mode}")


if __name__ == "__main__":
    sys.exit(main())
