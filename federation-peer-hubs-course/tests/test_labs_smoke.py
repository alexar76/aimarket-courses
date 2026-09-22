"""Smoke tests for labs.

Learner stubs in courselib/exercises.py stay unimplemented until filled.
Reference solutions are checked in test_exercises.py.
"""

import importlib
import os

LABS = [
    "lab01_well_known_announce",
    "lab02_open_vs_closed",
    "lab03_preview_quarantine",
    "lab04_declared_vs_read",
    "lab05_approve_capstone",
]


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")


def test_labs_run_offline():
    os.environ["COURSE_OFFLINE"] = "1"
    try:
        for stem in LABS:
            mod = importlib.import_module(f"labs.{stem}")
            mod.main()
    finally:
        os.environ.pop("COURSE_OFFLINE", None)
