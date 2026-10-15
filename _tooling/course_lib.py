"""Shared helpers for course site builders (monorepo-only; copied into satellites at export)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_course_config(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[1]
    # When imported from a course's scripts/, config lives one level up.
    if (root / "course.config.json").is_file():
        cfg_path = root / "course.config.json"
    else:
        cfg_path = root.parent / "course.config.json"
    return json.loads(cfg_path.read_text(encoding="utf-8"))
