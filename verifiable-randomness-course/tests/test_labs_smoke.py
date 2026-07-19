"""Smoke tests for lab scripts."""

import importlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_CFG = json.loads((ROOT / "course.config.json").read_text())
LABS = _CFG.get("smoke_labs", [])


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
