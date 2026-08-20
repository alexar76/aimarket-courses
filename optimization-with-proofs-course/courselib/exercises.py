"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.optimization import (
    gp_posterior,
    proof_portfolio,
    route_least_time,
    solve_transport,
    solve_tsp,
)

MODULES = ("m1", "m2", "m3", "m4", "m5")


def exercise_m1_tsp_gap_certificate() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_tsp_gap_certificate: implement this exercise")

def exercise_m2_transport_dual() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_transport_dual: implement this exercise")

def exercise_m3_fermat_route() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_fermat_route: implement this exercise")

def exercise_m4_gp_posterior() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_gp_posterior: implement this exercise")

def exercise_m5_proof_portfolio() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_proof_portfolio: implement this exercise")

EXERCISES = {
    "m1": exercise_m1_tsp_gap_certificate,
    "m2": exercise_m2_transport_dual,
    "m3": exercise_m3_fermat_route,
    "m4": exercise_m4_gp_posterior,
    "m5": exercise_m5_proof_portfolio,
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
