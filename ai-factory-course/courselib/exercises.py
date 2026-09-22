"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.factory import (
    PIPELINE_PHASES,
    factory_client,
    pipeline_flow_document,
    probe_factory,
    walk_to_ship,
)

MODULES = ["m1", "m2", "m3", "m4", "m5"]


def exercise_m1_phases() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_phases: implement this exercise")

def exercise_m2_pipeline_status() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_pipeline_status: implement this exercise")

def exercise_m3_products() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_products: implement this exercise")

def exercise_m4_orchestrator_path() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_orchestrator_path: implement this exercise")

def exercise_m5_factory_probe() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_factory_probe: implement this exercise")

EXERCISES = {
    "m1": exercise_m1_phases,
    "m2": exercise_m2_pipeline_status,
    "m3": exercise_m3_products,
    "m4": exercise_m4_orchestrator_path,
    "m5": exercise_m5_factory_probe,
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
