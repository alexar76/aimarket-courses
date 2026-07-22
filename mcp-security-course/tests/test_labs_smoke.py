"""Smoke tests for lab scripts."""

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_CFG = json.loads((ROOT / "course.config.json").read_text(encoding="utf-8"))
LABS = _CFG.get("smoke_labs", [])


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")


def test_exercises_pass():
    r = subprocess.run(
        [sys.executable, "labs/run_exercises.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
