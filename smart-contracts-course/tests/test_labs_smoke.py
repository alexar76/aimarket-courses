"""Smoke tests for generated labs.

Learner stubs in courselib/exercises.py must stay unimplemented until filled.
Reference solutions are checked in test_exercises.py, not here.
"""

import importlib

LABS = [
    "lab01_unbiasable_draw",
    "lab02_vdf_verify",
    "lab03_escrow_channel",
    "lab04_relayer_round",
    "lab05_lottery_capstone",
]


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
