"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.contracts import (
    BiasedLottery,
    EscrowChannel,
    FairLottery,
    RelayerRound,
    load_chronos_vector,
    simulate_fair_round,
    verify_wesolowski_vector,
)

MODULES = ["m1", "m2", "m3", "m4", "m5"]


def exercise_m1_fair_beats_bias() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_fair_beats_bias: implement this exercise")

def exercise_m2_foundry_vector() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_foundry_vector: implement this exercise")

def exercise_m3_escrow_debit() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_escrow_debit: implement this exercise")

def exercise_m4_relayer_seed() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_relayer_seed: implement this exercise")

def exercise_m5_capstone_round() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_capstone_round: implement this exercise")

EXERCISES = {
    "m1": exercise_m1_fair_beats_bias,
    "m2": exercise_m2_foundry_vector,
    "m3": exercise_m3_escrow_debit,
    "m4": exercise_m4_relayer_seed,
    "m5": exercise_m5_capstone_round,
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
