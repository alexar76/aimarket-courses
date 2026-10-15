"""Live oracle bridge — Murmuration, Colony, Turing, Ablation, Landauer."""

from __future__ import annotations

from typing import Any

from courselib.oracle_paths import ensure_oracle, ensure_oracles


def murmuration_aggregate(values: list[float], trim: float = 0.1) -> dict[str, Any]:
    """Robust consensus over agent estimates (Murmuration oracle)."""
    ensure_oracle("murmuration")
    from murmuration.consensus import aggregate

    out = aggregate(values, trim=trim)
    return {"oracle": "murmuration", **out}


def colony_tsp(points: list[list[float]], iterations: int = 500) -> dict[str, Any]:
    """TSP tour with optimality-gap certificate (Colony oracle)."""
    ensure_oracle("colony")
    from colony.tsp import solve

    out = solve(points, iterations=iterations)
    return {"oracle": "colony", **out}


def turing_bluenoise(count: int = 64, candidates: int = 10, seed: int = 42) -> dict[str, Any]:
    """Mitchell best-candidate blue-noise sample (Turing oracle)."""
    ensure_oracle("turing")
    from turing.bluenoise import bluenoise

    out = bluenoise(count, candidates=candidates, seed=seed)
    return {"oracle": "turing", **out}


def ablation_cascade(
    edges: list[list[str]],
    grains: int = 800,
    nonce: str = "course",
) -> dict[str, Any]:
    """Abelian sandpile cascade-risk analysis (Ablation oracle)."""
    ensure_oracle("ablation")
    from ablation.sandpile import cascade

    out = cascade(edges, grains=grains, nonce=nonce)
    return {"oracle": "ablation", **out}


def landauer_audit(ops: list[dict[str, Any]], temperature_k: float = 300.0) -> dict[str, Any]:
    """Thermodynamic bit-erasure audit (Landauer oracle)."""
    ensure_oracle("landauer")
    from landauer.thermo import audit

    out = audit(ops, temperature_k=temperature_k)
    return {"oracle": "landauer", **out}


def demo_exposure_graph() -> list[list[str]]:
    """Small directed exposure graph for Ablation labs."""
    return [
        ["bank-a", "bank-b"],
        ["bank-b", "bank-c"],
        ["bank-c", "bank-d"],
        ["bank-a", "bank-c"],
        ["bank-d", "sink"],
    ]


def demo_circuit_ops() -> list[dict[str, Any]]:
    """Small irreversible circuit for Landauer labs."""
    return [
        {"id": "in1", "gate": "input", "width": 8},
        {"id": "and1", "gate": "and", "inputs": ["in1", "in2"]},
        {"id": "in2", "gate": "input", "width": 8},
        {"id": "out1", "gate": "output", "inputs": ["and1"]},
    ]


def exercise_check(module: str) -> None:
    """Minimal DIY check students extend in each module."""
    assert module.startswith("m"), module
    ensure_oracles("murmuration", "colony", "turing", "ablation", "landauer")
    if module == "m1":
        out = murmuration_aggregate([1.0, 1.1, 1.05, 50.0, 0.9])
        assert out["biweight"] < 10.0
    elif module == "m2":
        pts = [[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.5]]
        out = colony_tsp(pts)
        assert out["gap"] >= 0.0
    elif module == "m3":
        out = turing_bluenoise(32, seed=7)
        assert out["min_distance"] > 0.0
    elif module == "m4":
        out = ablation_cascade(demo_exposure_graph(), grains=200)
        assert out["tau"] > 0.0
    elif module == "m5":
        out = landauer_audit(demo_circuit_ops())
        assert out["irreversible_bits"] >= 0
    else:
        raise AssertionError(f"unknown module {module}")
