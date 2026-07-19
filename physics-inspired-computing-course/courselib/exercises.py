"""Hands-on exercises — DIY checks for each module."""

from __future__ import annotations

from courselib.physics import (
    ablation_cascade,
    colony_tsp,
    demo_circuit_ops,
    demo_exposure_graph,
    landauer_audit,
    murmuration_aggregate,
    turing_bluenoise,
)

MODULES = ("m1", "m2", "m3", "m4", "m5")


def exercise_m1_robust_median() -> None:
    out = murmuration_aggregate([2.0, 2.1, 1.9, 100.0, 2.05])
    assert out["median"] < 10.0
    assert out["biweight"] < 10.0


def exercise_m2_tsp_certificate() -> None:
    pts = [[0, 0], [2, 0], [2, 2], [0, 2], [1, 1]]
    out = colony_tsp(pts)
    assert out["length"] >= out["lower_bound"]
    assert 0 <= out["gap"] < 2.0


def exercise_m3_blue_noise_spacing() -> None:
    out = turing_bluenoise(48, candidates=12, seed=99)
    assert out["count"] == 48
    assert out["min_distance"] > 0.01


def exercise_m4_cascade_tau() -> None:
    out = ablation_cascade(demo_exposure_graph(), grains=300, nonce="exercise")
    assert out["tau"] > 0.5
    assert out["n_avalanches"] >= 1


def exercise_m5_landauer_floor() -> None:
    out = landauer_audit(demo_circuit_ops(), temperature_k=300.0)
    assert out["energy_floor_j"] >= 0.0
    assert out["irreversible_bits"] >= 1


EXERCISES = {
    "m1": exercise_m1_robust_median,
    "m2": exercise_m2_tsp_certificate,
    "m3": exercise_m3_blue_noise_spacing,
    "m4": exercise_m4_cascade_tau,
    "m5": exercise_m5_landauer_floor,
}


def run_all() -> dict[str, str]:
    out: dict[str, str] = {}
    for mod, fn in EXERCISES.items():
        try:
            fn()
            out[mod] = "ok"
        except Exception as exc:
            out[mod] = f"fail: {exc}"
    return out


def all_passed() -> bool:
    return all(v == "ok" for v in run_all().values())
