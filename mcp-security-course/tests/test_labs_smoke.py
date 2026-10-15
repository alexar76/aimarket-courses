"""Smoke tests for lab scripts.

Learner stubs in courselib/exercises.py must stay unimplemented until filled.
Reference solutions are checked in test_exercises.py, not here.
"""

import importlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_CFG = json.loads((ROOT / "course.config.json").read_text(encoding="utf-8"))
LABS = _CFG.get("smoke_labs", [])


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
