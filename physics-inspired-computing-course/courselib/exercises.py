"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

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
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_robust_median: implement this exercise")

def exercise_m2_tsp_certificate() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_tsp_certificate: implement this exercise")

def exercise_m3_blue_noise_spacing() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_blue_noise_spacing: implement this exercise")

def exercise_m4_cascade_tau() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_cascade_tau: implement this exercise")

def exercise_m5_landauer_floor() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_landauer_floor: implement this exercise")

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


def all_passed(results: dict[str, str] | None = None) -> bool:
    results = results if results is not None else run_all()
    return all(v == "ok" for v in results.values())
