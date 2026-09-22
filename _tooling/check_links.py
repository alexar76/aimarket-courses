#!/usr/bin/env python3
"""Check internal links in built course sites (monorepo QA)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HREF_RE = re.compile(r'href=["\\\']([^"\\\']+)["\\\']')

COURSES = sorted(
    p.name
    for p in ROOT.iterdir()
    if p.is_dir() and (p / "course.config.json").is_file() and not p.name.startswith("_")
)


def _check_course(course_dir: Path) -> list[str]:
    errors: list[str] = []
    site = course_dir / "site"
    data_path = site / "data" / "course.json"
    if not data_path.is_file():
        return [f"{course_dir.name}: missing {data_path.relative_to(ROOT)}"]
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    repo = payload.get("repo", "")

    for lab in payload.get("labs", []):
        val = lab.get("script", "")
        if val and not (course_dir / val).is_file():
            errors.append(f"{course_dir.name}: missing lab file {val}")
        colab = lab.get("colab", "")
        if repo and colab and repo not in colab:
            errors.append(f"{course_dir.name}: colab URL repo mismatch: {colab}")

    index = site / "index.html"
    if index.is_file():
        for href in HREF_RE.findall(index.read_text(encoding="utf-8")):
            if href.startswith("#") or href.startswith("http"):
                continue
            target = (site / href.split("?")[0]).resolve()
            if not target.is_file():
                errors.append(f"{course_dir.name}: broken href in index.html: {href}")

    for asset in ("assets/app.js", "assets/style.css", "assets/progress.js", "assets/certificate.js"):
        if not (site / asset).is_file():
            errors.append(f"{course_dir.name}: missing {asset}")

    nb_dir = course_dir / "notebooks"
    for lab in payload.get("labs", []):
        nb = nb_dir / lab.get("notebook", "")
        if lab.get("notebook") and not nb.is_file():
            errors.append(f"{course_dir.name}: missing notebook {nb.name}")

    return errors


def _check_portal(site: Path) -> list[str]:
    errors: list[str] = []
    index = site / "index.html"
    if not index.is_file():
        return errors
    html = index.read_text(encoding="utf-8")
    if re.search(r"colab\.research\.google\.com/github/[^/]+/tree/main/", html):
        errors.append("portal: malformed Colab URL (use /blob/main/…/lab.ipynb, not /tree/…/notebooks)")
    return errors


def main() -> int:
    all_errors: list[str] = []
    portal_site = ROOT / "site"
    all_errors.extend(_check_portal(portal_site))
    for name in COURSES:
        course_dir = ROOT / name
        if not (course_dir / "site/data/course.json").is_file():
            subprocess.run(
                [sys.executable, "scripts/build_course_assets.py"],
                cwd=course_dir,
                check=True,
            )
        errs = _check_course(course_dir)
        if errs:
            all_errors.extend(errs)
        else:
            print(f"OK  {name}")

    if all_errors:
        print("\nLink / asset errors:", file=sys.stderr)
        for e in all_errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"\nAll {len(COURSES)} courses passed link check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
