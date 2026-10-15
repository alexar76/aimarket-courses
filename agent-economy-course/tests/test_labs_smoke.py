"""Smoke tests for generated labs.

Learner stubs in courselib/exercises.py must stay unimplemented until filled.
Reference solutions are checked in test_exercises.py, not here.
"""

import importlib

LABS = [
    "lab01_protocol_overview",
    "lab02_hub_discover",
    "lab03_escrow_channel",
    "lab04_reputation_trust",
    "lab05_publish_capability",
]


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
