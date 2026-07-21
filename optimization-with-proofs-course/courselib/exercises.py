"""Hands-on exercises — DIY checks for each module."""

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
    out = solve_tsp()
    assert out["certificate_valid"] is True
    assert out["length"] >= out["lower_bound"]
    assert out["gap"] >= 0


def exercise_m2_transport_dual() -> None:
    out = solve_transport()
    assert out["verified"] is True
    assert out["cost"] > 0


def exercise_m3_fermat_route() -> None:
    out = route_least_time()
    assert out["verified"] is True
    assert out["path"] is not None
    assert out["path"][0] == "client"
    assert out["path"][-1] == "sink"


def exercise_m4_gp_posterior() -> None:
    out = gp_posterior()
    assert out["verified"] is True
    assert len(out["mean"]) == len(out["std"])


def exercise_m5_proof_portfolio() -> None:
    out = proof_portfolio()
    assert out["all_verified"] is True


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


def all_passed() -> bool:
    return all(v == "ok" for v in run_all().values())
