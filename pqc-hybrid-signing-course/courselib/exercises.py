"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.pqc import (
    HybridSigner,
    HybridVerifier,
    envelope_is_hybrid,
    refuse_single_orbit,
    strip_pq,
    why_hybrid_brief,
)

MODULES = ("m1", "m2", "m3", "m4", "m5")


def exercise_m1_why_hybrid() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_why_hybrid: implement this exercise")


def exercise_m2_dual_identity() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_dual_identity: implement this exercise")


def exercise_m3_sign_receipt() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_sign_receipt: implement this exercise")


def exercise_m4_verify_offline() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_verify_offline: implement this exercise")


def exercise_m5_refuse_single_orbit() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_refuse_single_orbit: implement this exercise")


EXERCISES = {
    "m1": exercise_m1_why_hybrid,
    "m2": exercise_m2_dual_identity,
    "m3": exercise_m3_sign_receipt,
    "m4": exercise_m4_verify_offline,
    "m5": exercise_m5_refuse_single_orbit,
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
