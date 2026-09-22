"""Offline crypto tests for HybridSigner / HybridVerifier / gate."""

from __future__ import annotations

import pytest

from courselib.pqc import (
    HybridSigner,
    HybridVerifier,
    demo_hybrid_roundtrip,
    envelope_is_hybrid,
    fetch_live_hybrid_envelope,
    pqc_available,
    refuse_single_orbit,
    strip_pq,
    why_hybrid_brief,
)


def test_why_hybrid_brief_complete():
    brief = why_hybrid_brief()
    assert set(brief) >= {"classical_alone", "pq_alone", "hybrid", "downgrade"}


def test_envelope_is_hybrid_shape():
    assert envelope_is_hybrid({"algorithm": "ed25519", "public_key": "a", "value": "b"}) is False
    assert (
        envelope_is_hybrid(
            {
                "algorithm": "ed25519",
                "public_key": "a",
                "value": "b",
                "pq_algorithm": "ml-dsa-65",
                "pq_public_key": "c",
                "pq_value": "d",
            }
        )
        is True
    )


def test_classical_sign_and_verify_always():
    signer = HybridSigner(enable_pq=False)
    signed = signer.sign_receipt(
        {
            "capability": "t@v1",
            "output_hash": "sha256:x",
            "issued_at": "2026-01-01T00:00:00Z",
            "request_id": "t1",
        }
    )
    result = HybridVerifier(pinned_ed_b64=signer.public_key_b64).verify_receipt(signed)
    assert result.classical_ok is True
    assert result.ok is True
    assert result.hybrid is False
    assert envelope_is_hybrid(signed["signature"]) is False


def test_refuse_single_orbit_blocks_downgrade():
    signer = HybridSigner(enable_pq=True)
    signed = signer.sign_receipt(
        {
            "capability": "t@v1",
            "output_hash": "sha256:y",
            "issued_at": "2026-01-01T00:00:00Z",
            "request_id": "t2",
        }
    )
    msg = signed["_canonical"].encode()
    stripped = strip_pq(signed["signature"])
    refused = refuse_single_orbit(stripped, msg, pinned_ed_b64=signer.public_key_b64)
    assert refused.refused is True
    assert refused.ok is False


@pytest.mark.skipif(not pqc_available(), reason="dilithium-py not installed")
def test_hybrid_roundtrip_with_dilithium():
    out = demo_hybrid_roundtrip(require_pq=True)
    assert out["identity"]["pq_enabled"] is True
    assert out["verify"]["ok"] is True
    assert out["verify"]["hybrid"] is True
    assert envelope_is_hybrid(out["signed"]["signature"])


@pytest.mark.skipif(not pqc_available(), reason="dilithium-py not installed")
def test_tampered_pq_fails():
    signer = HybridSigner(enable_pq=True)
    signed = signer.sign_receipt(
        {
            "capability": "t@v1",
            "output_hash": "sha256:z",
            "issued_at": "2026-01-01T00:00:00Z",
            "request_id": "t3",
        }
    )
    sig = dict(signed["signature"])
    raw = bytearray(__import__("base64").b64decode(sig["pq_value"]))
    raw[0] ^= 0xFF
    sig["pq_value"] = __import__("base64").b64encode(bytes(raw)).decode()
    result = HybridVerifier(
        require_pq=True,
        pinned_ed_b64=signer.public_key_b64,
        pinned_pq_b64=signer.pq_public_key_b64,
    ).verify_envelope(sig, signed["_canonical"].encode())
    assert result.classical_ok is True
    assert result.pq_ok is False
    assert result.ok is False


def test_live_fetch_optional():
    """Network optional — skip cleanly when offline / blocked."""
    try:
        live = fetch_live_hybrid_envelope(timeout=8.0)
    except Exception as exc:
        pytest.skip(f"live hub unreachable: {exc}")
    assert live["source"] == "LIVE"
    assert live["hybrid"] is True
    assert live["classical_verified_offline"] is True
    assert live["pq_status"] in ("verified", "inspected_only_dilithium_missing", "verify_failed")
    if live["pq_status"] == "inspected_only_dilithium_missing":
        assert live["pq_verified_offline"] is None  # never invent success
