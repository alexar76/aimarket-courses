"""Smoke tests for labs.

Learner stubs in courselib/exercises.py must stay unimplemented until filled.
Reference solutions are checked in test_exercises.py, not here.
"""

import importlib

LABS = [
    "lab01_why_hybrid",
    "lab02_key_identity",
    "lab03_sign_receipt",
    "lab04_verify_offline",
    "lab05_hybrid_gate_capstone",
]


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")


def test_labs_main_runs():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        mod.main()
