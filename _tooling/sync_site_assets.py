#!/usr/bin/env python3
"""Copy canonical site_assets (app.js, progress.js) into every course folder."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "_tooling" / "site_assets"


def main() -> int:
    for name in ("app.js", "progress.js", "certificate.js"):
        src = CANON / name
        if not src.is_file():
            print(f"missing canonical {src}", file=__import__("sys").stderr)
            return 1
    for course in sorted(ROOT.glob("*-course")):
        dest = course / "site_assets"
        dest.mkdir(parents=True, exist_ok=True)
        for name in ("app.js", "progress.js", "certificate.js"):
            shutil.copy2(CANON / name, dest / name)
        key = f"{course.name}-progress-v1"
        progress = (dest / "progress.js").read_text(encoding="utf-8")
        (dest / "progress.js").write_text(progress.replace("__STORAGE_KEY__", key), encoding="utf-8")
        print(f"  ✓ {course.name}/site_assets/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
