"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.randomness import (
    BiasedLottery,
    FairLottery,
    chaos_draw,
    ecvrf_draw,
    onchain_vdf_vector,
    timelock_seal,
    vdf_eval,
)

MODULES = ("m1", "m2", "m3", "m4", "m5", "m6")


def exercise_m1_verify_platon() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_verify_platon: implement this exercise")

def exercise_m2_vdf_tamper_fails() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_vdf_tamper_fails: implement this exercise")

def exercise_m3_ecvrf_80_bytes() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_ecvrf_80_bytes: implement this exercise")

def exercise_m4_timelock_roundtrip() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_timelock_roundtrip: implement this exercise")

def exercise_m5_fair_beats_biased_audit() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_fair_beats_biased_audit: implement this exercise")

def exercise_m6_onchain_vector_valid() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m6_onchain_vector_valid: implement this exercise")

EXERCISES = {
    "m1": exercise_m1_verify_platon,
    "m2": exercise_m2_vdf_tamper_fails,
    "m3": exercise_m3_ecvrf_80_bytes,
    "m4": exercise_m4_timelock_roundtrip,
    "m5": exercise_m5_fair_beats_biased_audit,
    "m6": exercise_m6_onchain_vector_valid,
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
