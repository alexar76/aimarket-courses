"""Smoke tests for generated labs.

Learner stubs in courselib/exercises.py must stay unimplemented until filled.
Reference solutions are checked in test_exercises.py, not here.
"""

import importlib

LABS = [
    "lab01_keystone_nodes",
    "lab02_trust_pagerank",
    "lab03_spectral_cut",
    "lab04_consensus_aggregate",
    "lab05_sandpile_cascade",
    "lab06_trust_audit",
]


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
