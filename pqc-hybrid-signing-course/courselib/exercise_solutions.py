"""Reference solutions for CI / instructors. Learners edit exercises.py."""

from __future__ import annotations

from courselib.pqc import (
    HybridSigner,
    HybridVerifier,
    envelope_is_hybrid,
    pqc_available,
    refuse_single_orbit,
    strip_pq,
    why_hybrid_brief,
)

MODULES = ("m1", "m2", "m3", "m4", "m5")


def exercise_m1_why_hybrid() -> None:
    brief = why_hybrid_brief()
    assert "hybrid" in brief and "downgrade" in brief
    assert "Ed25519" in brief["classical_alone"] or "classical" in brief["classical_alone"].lower()
    # A classical-only envelope is not hybrid.
    classical = {"algorithm": "ed25519", "public_key": "x", "value": "y"}
    assert envelope_is_hybrid(classical) is False


def exercise_m2_dual_identity() -> None:
    signer = HybridSigner(enable_pq=True)
    ident = signer.identity()
    assert ident.classical_public_key_b64
    assert len(ident.classical_public_key_b64) > 20
    if pqc_available():
        assert ident.pq_enabled is True
        assert ident.pq_public_key_b64
    else:
        assert ident.pq_enabled is False
        assert signer.pq_skipped is True


def exercise_m3_sign_receipt() -> None:
    signer = HybridSigner(enable_pq=True)
    receipt = {
        "capability": "course.exercise@v1",
        "output_hash": "sha256:cafe",
        "issued_at": "2026-09-08T12:00:00Z",
        "request_id": "ex-m3",
    }
    signed = signer.sign_receipt(receipt)
    sig = signed["signature"]
    assert sig["algorithm"] == "ed25519"
    assert sig["public_key"] == signer.public_key_b64
    assert sig["value"]
    if pqc_available():
        assert envelope_is_hybrid(sig)
    else:
        assert sig.get("pq_skipped") is True
        assert not envelope_is_hybrid(sig)


def exercise_m4_verify_offline() -> None:
    signer = HybridSigner(enable_pq=True)
    signed = signer.sign_receipt(
        {
            "capability": "course.exercise@v1",
            "output_hash": "sha256:beef",
            "issued_at": "2026-09-08T12:00:00Z",
            "request_id": "ex-m4",
        }
    )
    verifier = HybridVerifier(
        require_pq=False,
        pinned_ed_b64=signer.public_key_b64,
        pinned_pq_b64=signer.pq_public_key_b64,
    )
    result = verifier.verify_receipt(signed)
    assert result.classical_ok is True
    if pqc_available():
        assert result.ok is True
        assert result.pq_ok is True
        assert result.hybrid is True
    else:
        # Classical still verifies; hybrid claim must not be invented.
        assert result.classical_ok is True
        assert signed["signature"].get("pq_skipped") is True


def exercise_m5_refuse_single_orbit() -> None:
    signer = HybridSigner(enable_pq=True)
    signed = signer.sign_receipt(
        {
            "capability": "course.gate@v1",
            "output_hash": "sha256:gate",
            "issued_at": "2026-09-08T12:00:00Z",
            "request_id": "ex-m5",
        }
    )
    msg = signed["_canonical"].encode()
    sig = signed["signature"]

    # Classical-only must be refused by the gate.
    stripped = strip_pq(sig)
    refused = refuse_single_orbit(stripped, msg, pinned_ed_b64=signer.public_key_b64)
    assert refused.refused is True
    assert refused.ok is False

    if pqc_available():
        accepted = refuse_single_orbit(
            sig,
            msg,
            pinned_ed_b64=signer.public_key_b64,
            pinned_pq_b64=signer.pq_public_key_b64,
        )
        assert accepted.ok is True
        assert accepted.hybrid is True
    else:
        # Without dilithium we still prove the gate refuses single-orbit;
        # we do not invent a hybrid accept path.
        assert signer.pq_skipped is True


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
