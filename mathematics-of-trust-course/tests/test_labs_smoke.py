"""Smoke tests for generated labs."""

import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABS = [
    "lab01_keystone_nodes",
    "lab02_trust_pagerank",
    "lab03_spectral_cut",
    "lab04_consensus_aggregate",
    "lab05_sandpile_cascade",
    "lab06_trust_audit",
]


def test_exercises_pass():
    r = subprocess.run([sys.executable, "labs/run_exercises.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
