#!/usr/bin/env python3
"""Fail if any course README or doc still has broken badges or clone URLs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BAD_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("standalone CI badge", re.compile(r"github/actions/workflow/status/alexar76/(?!aimarket-courses)[a-z0-9-]+-course")),
    ("broken tree/main clone", re.compile(r"github\.com/alexar76/aimarket-courses/tree/main/[a-z0-9-]+-course\.git")),
    ("standalone repo URL", re.compile(r"github\.com/alexar76/[a-z0-9-]+-course(?:\.git|/issues)")),
    ("local coverage in subfolder README", re.compile(r'href="#testing--coverage".*docs/badges/coverage\.svg')),
    ("legacy github.io course root", re.compile(r"alexar76\.github\.io/(?!aimarket-courses)[a-z0-9-]+-course")),
    ("legacy colab standalone repo", re.compile(r"colab\.research\.google\.com/github/alexar76/(?!aimarket-courses)[a-z0-9-]+-course")),
    (
        "malformed colab tree URL",
        re.compile(r"colab\.research\.google\.com/github/[^/]+/tree/main/"),
    ),
]

ECOSYSTEM_FILES = [
    Path(__file__).resolve().parents[2] / "README.md",
    Path(__file__).resolve().parents[2] / "ecosystem-README.md",
    Path(__file__).resolve().parents[2] / "ecosystem-landing" / "index.html",
    Path(__file__).resolve().parents[2] / "scripts" / "profile-readme" / "README.md",
    Path(__file__).resolve().parents[2] / "scripts" / "wiki-gitea" / "Ecosystem.md",
    Path(__file__).resolve().parents[2] / "docs" / "awesome-list-submissions.md",
]

REQUIRED_IN_README = [
    # GitHub-native: …/aimarket-courses/actions/workflows/ci.yml/badge.svg
    # (legacy shields used …/aimarket-courses/ci.yml?branch=… — both OK)
    "aimarket-courses/actions/workflows/ci.yml",
    "img.shields.io/badge/Pages-course",
    "img.shields.io/badge/Colab-notebooks",
]


def _has_monorepo_ci_badge(text: str) -> bool:
    return (
        "aimarket-courses/actions/workflows/ci.yml" in text
        or "aimarket-courses/ci.yml" in text
    )


def main() -> int:
    errors: list[str] = []
    for course_dir in sorted(ROOT.glob("*-course")):
        folder = course_dir.name
        readme = course_dir / "README.md"
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        for label, pat in BAD_PATTERNS:
            if pat.search(text):
                errors.append(f"{folder}/README.md: {label}")
        for req in REQUIRED_IN_README:
            if req not in text:
                errors.append(f"{folder}/README.md: missing {req!r}")
        for doc in (course_dir / "docs").glob("*.md"):
            body = doc.read_text(encoding="utf-8")
            for label, pat in BAD_PATTERNS:
                if pat.search(body):
                    errors.append(f"{folder}/docs/{doc.name}: {label}")

    root_readme = ROOT / "README.md"
    if root_readme.is_file():
        root = root_readme.read_text(encoding="utf-8")
        if not _has_monorepo_ci_badge(root):
            errors.append("courses/README.md: missing monorepo CI badge")

    ecosystem_bad = [p for p in BAD_PATTERNS if p[0] != "local coverage in subfolder README"]
    for path in ECOSYSTEM_FILES:
        if not path.is_file():
            continue
        rel = path.relative_to(Path(__file__).resolve().parents[2])
        body = path.read_text(encoding="utf-8")
        for label, pat in ecosystem_bad:
            if pat.search(body):
                errors.append(f"{rel}: {label}")

    if errors:
        print("verify_course_readmes: FAILED", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"verify_course_readmes: OK ({len(list(ROOT.glob('*-course')))} courses)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
