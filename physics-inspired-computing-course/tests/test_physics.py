"""Tests for live oracle bridge (monorepo oracles on PYTHONPATH)."""

import pytest

from courselib.physics import (
    ablation_cascade,
    colony_tsp,
    demo_circuit_ops,
    demo_exposure_graph,
    landauer_audit,
    murmuration_aggregate,
    turing_bluenoise,
)


@pytest.fixture(scope="module", autouse=True)
def _require_oracles():
    from courselib.oracle_paths import ensure_oracles

    ensure_oracles("murmuration", "colony", "turing", "ablation", "landauer")


def test_murmuration_resists_outlier():
    out = murmuration_aggregate([1.0, 1.1, 1.05, 100.0])
    assert out["biweight"] < 10.0


def test_colony_tsp_gap():
    pts = [[0, 0], [1, 0], [1, 1], [0, 1]]
    out = colony_tsp(pts)
    assert out["length"] >= out["lower_bound"]
    assert out["gap"] >= 0.0


def test_turing_bluenoise_seed():
    out = turing_bluenoise(24, seed=1)
    assert out["count"] == 24
    assert out["min_distance"] > 0.0


def test_ablation_cascade():
    out = ablation_cascade(demo_exposure_graph(), grains=400)
    assert out["tau"] > 0.0
    assert out["topple_total"] >= 0


def test_landauer_audit():
    out = landauer_audit(demo_circuit_ops())
    assert out["irreversible_bits"] >= 0
    assert out["energy_floor_j"] >= 0.0
