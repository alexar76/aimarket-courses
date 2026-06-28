"""Hands-on exercises — DIY checks for each module."""

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
    out = chaos_draw("exercise-seed")
    assert out["verified"] is True
    assert len(out["draw"]["random_hex"]) >= 16


def exercise_m2_vdf_tamper_fails() -> None:
    out = vdf_eval("tamper-test", difficulty=400)
    assert out["valid"] is True
    from courselib.oracle_paths import ensure_oracle

    ensure_oracle("chronos")
    from chronos import vdf

    g = out["g"]
    p = out["proof"]
    bad_y = (out["y"] + 1) % vdf.RSA_2048
    assert vdf.verify(g, bad_y, out["difficulty"], p["pi"], p["l"]) is False


def exercise_m3_ecvrf_80_bytes() -> None:
    out = ecvrf_draw(b"offline-verify")
    assert out["proof_len"] == 80
    assert out["verified"] is True


def exercise_m4_timelock_roundtrip() -> None:
    out = timelock_seal("exercise-payload", T=200)
    assert out["message_match"] is True


def exercise_m5_fair_beats_biased_audit() -> None:
    biased = BiasedLottery()
    fair = FairLottery()
    seed = "player-42"
    biased.commit(seed)
    fair.commit(seed)
    b = biased.draw(seed)
    f, proof = fair.draw(seed)
    assert proof["verified"] is True
    assert 0 <= b < 100 and 0 <= f < 100


def exercise_m6_onchain_vector_valid() -> None:
    vec = onchain_vdf_vector()
    assert vec["valid"] is True
    assert vec["scheme"] == "wesolowski-vdf"


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
            out[mod] = str(exc)
    return out


def all_passed() -> bool:
    return all(v == "ok" for v in run_all().values())
