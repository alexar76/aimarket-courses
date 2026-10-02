#!/usr/bin/env python3
"""Aggregate pytest coverage across all courses → courses/docs/badges/coverage.svg."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "orchestration-course" / "scripts" / "generate_coverage_badge.py"
OUT = ROOT / "docs" / "badges" / "coverage.svg"


def main() -> int:
    totals_covered = 0.0
    totals_num = 0.0
    ran = 0
    for course in sorted(ROOT.glob("*-course")):
        print(f"==> coverage {course.name}")
        subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--cov=courselib", "--cov-report=json:coverage.json"],
            cwd=course,
            check=True,
        )
        data = json.loads((course / "coverage.json").read_text(encoding="utf-8"))
        t = data["totals"]
        totals_covered += float(t["covered_lines"])
        totals_num += float(t["num_statements"])
        ran += 1
    pct = (totals_covered / totals_num * 100.0) if totals_num else 0.0
    merged = {"totals": {"percent_covered": pct}}
    tmp = ROOT / ".coverage-merged.json"
    tmp.write_text(json.dumps(merged), encoding="utf-8")
    subprocess.run([sys.executable, str(GEN), str(tmp), str(OUT)], check=True)
    tmp.unlink(missing_ok=True)
    print(f"Wrote {OUT} ({pct:.0f}% across {ran} courses)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
