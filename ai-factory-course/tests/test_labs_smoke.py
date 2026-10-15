"""Smoke tests for generated labs.

Learner stubs in courselib/exercises.py must stay unimplemented until filled.
Reference solutions are checked in test_exercises.py, not here.
"""

import importlib

LABS = [
    "lab01_pipeline_overview",
    "lab02_pipeline_status",
    "lab03_products_catalog",
    "lab04_orchestrator_stages",
    "lab05_factory_capstone",
]


def test_labs_importable():
    for stem in LABS:
        mod = importlib.import_module(f"labs.{stem}")
        assert hasattr(mod, "main")
