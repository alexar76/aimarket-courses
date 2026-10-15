#!/usr/bin/env python3
"""Aggregate pytest coverage across all courses → courses/docs/badges/coverage.svg."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "orchestration-course" / "scripts" / "generate_coverage_badge.py"
OUT = ROOT / "docs" / "badges" / "coverage.svg"


def course_python() -> str:
    """Keep a supported interpreter; avoid Xcode's Python 3.9 when mirroring."""
    override = os.environ.get("COURSE_PYTHON")
    if override:
        candidates = [shutil.which(override) or str(Path(override).absolute())]
    elif sys.version_info >= (3, 11):
        return sys.executable
    else:
        candidates = [str(ROOT / ".venv" / "bin" / "python")]
        if (ROOT.parent / "aimarket-hub").is_dir():
            candidates.append(str(ROOT.parent / ".venv" / "bin" / "python"))

    for candidate in candidates:
        try:
            result = subprocess.run(
                [candidate, "-c", "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"],
                capture_output=True,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0:
            return candidate
    raise SystemExit(
        "Course tests require Python >=3.11 (including aimarket-hub). "
        f"Current interpreter: {sys.executable}. "
        "Activate a Python 3.11+ environment with the course test dependencies, "
        "or set COURSE_PYTHON=/absolute/path/to/venv/bin/python."
    )


def main() -> int:
    python = course_python()
    print(f"Course test interpreter: {python}", flush=True)
    totals_covered = 0.0
    totals_num = 0.0
    ran = 0
    for course in sorted(ROOT.glob("*-course")):
        print(f"==> coverage {course.name}", flush=True)
        subprocess.run(
            [python, "-m", "pytest", "-q", "--cov=courselib", "--cov-report=json:coverage.json"],
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
    subprocess.run([python, str(GEN), str(tmp), str(OUT)], check=True)
    tmp.unlink(missing_ok=True)
    print(f"Wrote {OUT} ({pct:.0f}% across {ran} courses)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
