"""Smoke tests for generated labs."""

import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABS = [
    "lab01_protocol_overview",
    "lab02_hub_discover",
    "lab03_escrow_channel",
    "lab04_reputation_trust",
    "lab05_publish_capability",
]


def test_exercises_pass():
    r = subprocess.run([sys.executable, "labs/run_exercises.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
