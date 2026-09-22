"""Smoke tests for generated labs.

Learner stubs in courselib/exercises.py must stay unimplemented until filled.
Reference solutions are checked in test_exercises.py, not here.
"""

import importlib

LABS = [
    "lab01_live_vs_sim",
    "lab02_licence_gate",
    "lab03_honesty_claims",
    "lab04_atlas_map_read",
    "lab05_add_sensor_capstone",
]


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
