"""Hands-on exercises for each module."""

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
    biased = BiasedLottery()
    assert biased.operator_can_grind("player-seed")
    fair = FairLottery()
    ticket, proof = fair.draw("player-seed")
    assert 0 <= ticket < 100
    assert proof.get("verified") is True


def exercise_m2_foundry_vector() -> None:
    vec = load_chronos_vector()
    assert vec.get("valid") is True
    assert verify_wesolowski_vector(vec)


def exercise_m3_escrow_debit() -> None:
    ch = EscrowChannel("ch-test", "alice")
    ch.open(500)
    ch.debit(100, "rcpt-a", "hub-1", signature_valid=True)
    settled = ch.settle()
    assert settled["to_hub"] == 100
    assert settled["refund"] == 400


def exercise_m4_relayer_seed() -> None:
    rnd = RelayerRound(3, b"\xaa" * 32, b"\xbb" * 32, onchain_vdf=True)
    assert rnd.chronos_seed().startswith("0x")
    assert len(rnd.base_seed()) == 32


def exercise_m5_capstone_round() -> None:
    out = simulate_fair_round(onchain_vdf=True)
    assert out["chronos_vector_valid"]
    assert out["vdf_path"] == "onchain"


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


def all_passed() -> bool:
    return all(v == "ok" for v in run_all().values())
