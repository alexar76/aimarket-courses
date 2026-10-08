#!/usr/bin/env python3
"""Point every course.config.json at the aimarket-courses monorepo satellite."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB_REPO = "alexar76/aimarket-courses"
CLONE_DIR = "aimarket-courses"
PAGES_BASE = "https://alexar76.github.io/aimarket-courses"


def main() -> int:
    for cfg_path in sorted(ROOT.glob("*-course/course.config.json")):
        folder = cfg_path.parent.name
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["github_repo"] = GITHUB_REPO
        cfg["github_pages"] = f"{PAGES_BASE}/{folder}/"
        cfg["repo_subpath"] = folder
        cfg["clone_dir"] = CLONE_DIR
        extras = cfg.get("pip_extras_default") or "[dev]"
        cfg["quickstart_commands"] = [
            f"git clone https://github.com/{GITHUB_REPO}.git",
            f"cd {CLONE_DIR}/{folder}",
            f'pip install -e ".{extras}"',
            f"python labs/{cfg['labs'][0]['stem']}.py",
            "python labs/run_exercises.py",
        ]
        cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  ✓ {folder}")

        pages = cfg["github_pages"]
        pyproject = cfg_path.parent / "pyproject.toml"
        if pyproject.is_file():
            text = pyproject.read_text(encoding="utf-8")
            text = re.sub(
                r'Homepage = "https://alexar76\.github\.io/[^"]+"',
                f'Homepage = "{pages}"',
                text,
            )
            text = re.sub(
                r'Documentation = "https://alexar76\.github\.io/[^"]+"',
                f'Documentation = "{pages}"',
                text,
            )
            pyproject.write_text(text, encoding="utf-8")
            print(f"    · {folder}/pyproject.toml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
