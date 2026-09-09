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
from research.arrow7 import run_arrow7  # noqa: E402
from research.arrow8 import run_arrow8  # noqa: E402
from research.arrow9 import run_arrow9  # noqa: E402
from research.arrow10 import run_arrow10  # noqa: E402
from research.arrow11 import run_arrow11  # noqa: E402
from research.arrow12 import run_arrow12  # noqa: E402
from research.arrow13 import run_arrow13  # noqa: E402
from research.arrow14 import run_arrow14  # noqa: E402
from research.arrow15 import run_arrow15  # noqa: E402
from ingest.full import run_arrow17  # noqa: E402
from research.arrow16 import run_arrow16  # noqa: E402
from research.arrow18 import run_arrow18  # noqa: E402
from research.arrow19 import run_arrow19  # noqa: E402
from research.arrow20 import run_arrow20  # noqa: E402
from research.arrow21 import run_arrow21  # noqa: E402
from research.rockets import run_rockets  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    cpu = os.cpu_count() or 1
    p = argparse.ArgumentParser(description="Lab A research replay")
    p.add_argument(
        "--mode",
        choices=(
            "arrow3",
            "arrow4",
            "arrow5",
            "arrow6",
            "arrow7",
            "arrow8",
            "arrow9",
            "arrow10",
            "arrow11",
            "arrow12",
            "arrow13",
            "arrow14",
            "arrow15",
            "arrow16",
            "arrow17",
            "arrow18",
            "arrow19",
            "arrow20",
            "arrow21",
            "rockets",
        ),
        default="arrow21",
        help="arrow21 iterate 09:29 hot book after Arrow 20 washout on data/full",
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
    if args.mode == "arrow7":
        return run_arrow7(workers=args.workers)
    if args.mode == "arrow8":
        return run_arrow8(workers=args.workers)
    if args.mode == "arrow9":
        return run_arrow9(workers=args.workers)
    if args.mode == "arrow10":
        return run_arrow10(workers=args.workers)
    if args.mode == "arrow11":
        return run_arrow11(workers=args.workers)
    if args.mode == "arrow12":
        return run_arrow12(workers=args.workers)
    if args.mode == "arrow13":
        return run_arrow13(workers=args.workers)
    if args.mode == "arrow14":
        return run_arrow14(workers=args.workers)
    if args.mode == "arrow15":
        return run_arrow15(workers=args.workers)
    if args.mode == "arrow16":
        return run_arrow16(workers=args.workers)
    if args.mode == "arrow17":
        return run_arrow17(workers=args.workers)
    if args.mode == "arrow18":
        return run_arrow18(workers=args.workers)
    if args.mode == "arrow19":
        return run_arrow19(workers=args.workers)
    if args.mode == "arrow20":
        return run_arrow20(workers=args.workers)
    if args.mode == "arrow21":
        return run_arrow21(workers=args.workers)
    if args.mode == "rockets":
        return run_rockets(workers=args.workers)
    raise SystemExit(f"unknown mode {args.mode}")


if __name__ == "__main__":
    sys.exit(main())
