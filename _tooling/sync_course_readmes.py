#!/usr/bin/env python3
"""Refresh per-course README badges, URLs, and markdown formatting for aimarket-courses."""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES_BASE = "https://alexar76.github.io/aimarket-courses"
GITHUB_REPO = "alexar76/aimarket-courses"
GITHUB_CLONE = f"https://github.com/{GITHUB_REPO}.git"
COVERAGE_SVG = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/docs/badges/coverage.svg"
MARKER_START = "<!-- aicom-readme-badges -->"
MARKER_END = "<!-- /aicom-readme-badges -->"

# Legacy standalone course repos (no CI workflow — shields shows red "repo or workflow not found").
_STANDALONE_REPO = re.compile(
    r"https://img\.shields\.io/github/actions/workflow/status/alexar76/[a-z0-9-]+-course/"
)
_BAD_CLONE = re.compile(
    r"https://github\.com/alexar76/aimarket-courses/tree/main/[a-z0-9-]+-course\.git"
)
_OLD_COLAB = re.compile(
    r"colab\.research\.google\.com/github/alexar76/([a-z0-9-]+-course)/blob/main/"
)
_OLD_STANDALONE_GH = re.compile(r"https://github\.com/alexar76/[a-z0-9-]+-course(?:\.git|/|$)")


def _fix_colab_urls(text: str) -> str:
    return _OLD_COLAB.sub(
        rf"colab.research.google.com/github/{GITHUB_REPO}/blob/main/\1/",
        text,
    )


def _colab_badge_url(folder: str) -> str:
    cfg = json.loads((ROOT / folder / "course.config.json").read_text(encoding="utf-8"))
    labs = cfg.get("labs") or []
    if not labs:
        return f"https://github.com/{GITHUB_REPO}/tree/main/{folder}/notebooks"
    stem = labs[0].get("stem") or labs[0].get("notebook", "").removesuffix(".ipynb")
    return (
        f"https://colab.research.google.com/github/{GITHUB_REPO}"
        f"/blob/main/{folder}/notebooks/{stem}.ipynb"
    )


def _badge_block(folder: str) -> str:
    pages = f"{PAGES_BASE}/{folder}/"
    colab = _colab_badge_url(folder)
    return f"""{MARKER_START}
<p align="center">
  <a href="https://github.com/{GITHUB_REPO}/actions/workflows/ci.yml"><img src="https://github.com/{GITHUB_REPO}/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="{pages}"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="{colab}"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="{COVERAGE_SVG}"><img src="{COVERAGE_SVG}" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
{MARKER_END}"""


def _strip_legacy_badges(text: str) -> str:
    """Remove duplicate badge rows outside the injected marker block."""
    lines: list[str] = []
    in_marker = False
    for line in text.splitlines():
        if MARKER_START in line:
            in_marker = True
        if in_marker:
            lines.append(line)
            if MARKER_END in line:
                in_marker = False
            continue
        if _STANDALONE_REPO.search(line):
            continue
        if "docs/badges/coverage.svg" in line and MARKER_START not in text[: text.find(line)]:
            continue
        if re.search(r"!\[CI\]|github/actions/workflow/status/alexar76/[a-z0-9-]+-course", line):
            continue
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def _inject_badges(text: str, block: str) -> str:
    pattern = re.compile(re.escape(MARKER_START) + r"[\s\S]*?" + re.escape(MARKER_END) + r"\n?")
    if pattern.search(text):
        return pattern.sub(block + "\n\n", text, count=1)
    m = re.search(r"^#\s+.+\n", text, re.MULTILINE)
    if m:
        pos = m.start()
        return text[:pos] + block + "\n\n" + text[pos:]
    return block + "\n\n" + text


def _normalize_body(text: str) -> str:
    """Remove accidental 8-space indent that breaks markdown headings."""
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        if line.startswith("        ") and not line.startswith("          "):
            out.append(line[8:])
        else:
            out.append(line)
    return "\n".join(out)


def _collapse_blank_lines(text: str) -> str:
    """Idempotent sync must not accumulate blank lines between badge block and body."""
    return re.sub(r"\n{3,}", "\n\n", text)


def _fix_clone_urls(text: str, folder: str) -> str:
    text = _BAD_CLONE.sub(GITHUB_CLONE, text)
    # Restore correct monorepo clone + cd (never tree/main/… .git).
    text = re.sub(
        rf"git clone {re.escape(GITHUB_CLONE)}\s*\n\s*cd {re.escape(folder)}",
        f"git clone {GITHUB_CLONE}\n        cd aimarket-courses/{folder}",
        text,
    )
    text = re.sub(
        rf"git clone {re.escape(GITHUB_CLONE)}\s*\n\s*cd aimarket-courses/{re.escape(folder)}",
        f"git clone {GITHUB_CLONE}\n        cd aimarket-courses/{folder}",
        text,
    )
    # Standalone clone URLs → monorepo layout.
    def _repl_standalone(m: re.Match[str]) -> str:
        url = m.group(0)
        if folder in url:
            return GITHUB_CLONE
        return url

    text = _OLD_STANDALONE_GH.sub(_repl_standalone, text)
    return text


def _fix_pages_urls(text: str, folder: str) -> str:
    pages = f"{PAGES_BASE}/{folder}/"
    text = re.sub(rf"https?://alexar76\.github\.io/{re.escape(folder)}/?", pages, text)
    text = text.replace(f"alexar76.github.io/{folder}", pages.replace("https://", ""))
    return text


def _quickstart_block(folder: str) -> str:
    cfg_path = ROOT / folder / "course.config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cmds = cfg.get("quickstart_commands") or []
    if not cmds:
        cmds = [
            f"git clone {GITHUB_CLONE}",
            f"cd aimarket-courses/{folder}",
            'pip install -e ".[dev]"',
        ]
    body = "\n".join(f"        {c}" for c in cmds)
    return f"        ```bash\n{body}\n        ```"


def _refresh_quickstart_section(text: str, folder: str) -> str:
    block = _quickstart_block(folder)
    pattern = re.compile(r"        ## Quick start\s*\n\s*```bash[\s\S]*?```", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(f"        ## Quick start\n\n{block}", text, count=1)
    return text


def _course_title(folder: str) -> str:
    cfg = json.loads((ROOT / folder / "course.config.json").read_text(encoding="utf-8"))
    return cfg.get("title") or folder.replace("-", " ").title()


def _ensure_title(text: str, folder: str) -> str:
    title = _course_title(folder)
    if re.search(rf"^#\s+{re.escape(title)}\s*$", text, re.MULTILINE):
        return text
    # Drop orphan indented pseudo-headings.
    text = re.sub(rf"^\s+# {re.escape(title)}\s*\n", "", text, flags=re.MULTILINE)
    marker_end = text.find(MARKER_END)
    insert_at = text.find("\n", marker_end) + 1 if marker_end != -1 else 0
    while insert_at < len(text) and text[insert_at] == "\n":
        insert_at += 1
    return text[:insert_at] + f"# {title}\n\n" + text[insert_at:].lstrip("\n")


def _fix_pyproject(course_dir: Path, folder: str) -> None:
    pyproject = course_dir / "pyproject.toml"
    if not pyproject.is_file():
        return
    text = pyproject.read_text(encoding="utf-8")
    pages = f"{PAGES_BASE}/{folder}/"
    text = re.sub(r'Repository = "https://github\.com/alexar76/[^"]+"', f'Repository = "https://github.com/{GITHUB_REPO}"', text)
    text = re.sub(r'Issues = "https://github\.com/alexar76/[^"]+/issues"', f'Issues = "https://github.com/{GITHUB_REPO}/issues"', text)
    text = re.sub(r'Homepage = "https://alexar76\.github\.io/[^"]+"', f'Homepage = "{pages}"', text)
    text = re.sub(r'Documentation = "https://alexar76\.github\.io/[^"]+"', f'Documentation = "{pages}"', text)
    pyproject.write_text(text, encoding="utf-8")


def _fix_markdown_file(path: Path, folder: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = _strip_legacy_badges(text)
    text = _fix_clone_urls(text, folder)
    text = _fix_pages_urls(text, folder)
    text = _fix_colab_urls(text)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for course_dir in sorted(ROOT.glob("*-course")):
        folder = course_dir.name
        readme = course_dir / "README.md"
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        text = _strip_legacy_badges(text)
        text = _inject_badges(text, _badge_block(folder))
        text = _ensure_title(text, folder)
        text = _normalize_body(text)
        text = _fix_clone_urls(text, folder)
        text = _fix_pages_urls(text, folder)
        text = _fix_colab_urls(text)
        text = _refresh_quickstart_section(text, folder)
        text = _collapse_blank_lines(text)
        readme.write_text(text, encoding="utf-8")
        print(f"  ✓ {folder}/README.md")

        docs = course_dir / "docs"
        if docs.is_dir():
            for doc in docs.glob("*.md"):
                _fix_markdown_file(doc, folder)
                print(f"    · docs/{doc.name}")

        _fix_pyproject(course_dir, folder)
        print(f"    · {folder}/pyproject.toml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
