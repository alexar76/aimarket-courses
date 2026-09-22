"""Hybrid Ed25519 + ML-DSA-65 signing for the PQC course.

Mirrors the AIMarket hub / attested-meter shape:
  algorithm / public_key / value  (+ optional pq_algorithm / pq_public_key / pq_value)

Rules taught here:
  1. Ed25519 always verifies first (classical orbit).
  2. When ``pq_value`` is present, ML-DSA-65 must verify too (or fail-closed).
  3. ``refuse_single_orbit`` (phase-3 gate) rejects classical-only envelopes.
  4. Never invent fake PQ success — if dilithium-py is missing, label clearly.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

try:
    from dilithium_py.ml_dsa import ML_DSA_65 as _MLDSA

    _PQ_LIB = True
except Exception:  # pragma: no cover - optional extra
    _MLDSA = None
    _PQ_LIB = False

DEFAULT_WELL_KNOWN = "https://modelmarket.dev/.well-known/ai-market.json"
PQ_ALGORITHM = "ml-dsa-65"
CLASSICAL_ALGORITHM = "ed25519"


def pqc_available() -> bool:
    """True when THIS process can produce/verify ML-DSA-65 signatures."""
    return _PQ_LIB


def object_canonical(obj: dict[str, Any]) -> str:
    """Hub-compatible canonical over an entire object (minus ``signature``)."""
    body = {k: v for k, v in obj.items() if k != "signature"}
    return json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def receipt_canonical(receipt: dict[str, Any]) -> str:
    """Deterministic canonical for a teaching receipt (stable field order)."""
    payload = {
        "capability": receipt.get("capability", ""),
        "output_hash": receipt.get("output_hash", ""),
        "issued_at": receipt.get("issued_at", ""),
        "request_id": receipt.get("request_id", ""),
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def envelope_is_hybrid(sig: dict[str, Any] | None) -> bool:
    """True when the signature object carries both classical and PQ fields."""
    if not isinstance(sig, dict):
        return False
    return bool(
        sig.get("algorithm")
        and sig.get("public_key")
        and sig.get("value")
        and sig.get("pq_algorithm")
        and sig.get("pq_public_key")
        and sig.get("pq_value")
    )


def strip_pq(sig: dict[str, Any]) -> dict[str, Any]:
    """Return a classical-only copy — the downgrade attack phase-3 blocks."""
    return {
        k: v
        for k, v in sig.items()
        if k not in ("pq_algorithm", "pq_public_key", "pq_value")
    }


@dataclass(frozen=True)
class Identity:
    """Dual-orbit peer identity (public half only)."""

    classical_public_key_b64: str
    pq_public_key_b64: str | None
    pq_enabled: bool
    note: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "classical_algorithm": CLASSICAL_ALGORITHM,
            "classical_public_key": self.classical_public_key_b64,
            "pq_algorithm": PQ_ALGORITHM if self.pq_enabled else None,
            "pq_public_key": self.pq_public_key_b64,
            "pq_enabled": self.pq_enabled,
            "note": self.note,
        }


class HybridSigner:
    """Ed25519 signer with optional ML-DSA-65 second orbit.

    When dilithium-py is missing, ``sign`` still produces a valid classical
    envelope and sets ``pq_skipped=True`` — never a fake PQ signature.
    """

    def __init__(self, *, enable_pq: bool = True) -> None:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        self._ed_priv = Ed25519PrivateKey.generate()
        self._ed_pub = self._ed_priv.public_key()
        self._pq: tuple[bytes, bytes] | None = None
        self.pq_skipped = False
        self.pq_skip_reason: str | None = None

        if enable_pq and _PQ_LIB:
            pk, sk = _MLDSA.keygen()
            self._pq = (pk, sk)
        elif enable_pq and not _PQ_LIB:
            self.pq_skipped = True
            self.pq_skip_reason = (
                "dilithium-py not installed — PQ sign skipped; "
                "classical Ed25519 still real. Install: pip install '.[pqc]'"
            )

    @property
    def public_key_b64(self) -> str:
        return base64.b64encode(self._ed_pub.public_bytes_raw()).decode()

    @property
    def pq_public_key_b64(self) -> str | None:
        if self._pq is None:
            return None
        return base64.b64encode(self._pq[0]).decode()

    def identity(self) -> Identity:
        if self._pq is not None:
            note = "dual-orbit identity (Ed25519 + ML-DSA-65)"
        elif self.pq_skipped:
            note = f"classical-only identity — {self.pq_skip_reason}"
        else:
            note = "classical-only identity (PQ disabled by caller)"
        return Identity(
            classical_public_key_b64=self.public_key_b64,
            pq_public_key_b64=self.pq_public_key_b64,
            pq_enabled=self._pq is not None,
            note=note,
        )

    def sign_bytes(self, message: bytes) -> dict[str, Any]:
        value = base64.b64encode(self._ed_priv.sign(message)).decode()
        sig: dict[str, Any] = {
            "algorithm": CLASSICAL_ALGORITHM,
            "public_key": self.public_key_b64,
            "value": value,
        }
        if self._pq is not None:
            pk, sk = self._pq
            sig["pq_algorithm"] = PQ_ALGORITHM
            sig["pq_public_key"] = base64.b64encode(pk).decode()
            sig["pq_value"] = base64.b64encode(_MLDSA.sign(sk, message)).decode()
        elif self.pq_skipped:
            sig["pq_skipped"] = True
            sig["pq_skip_reason"] = self.pq_skip_reason
        return sig

    def sign_canonical(self, canonical: str) -> dict[str, Any]:
        return self.sign_bytes(canonical.encode())

    def sign_receipt(self, receipt: dict[str, Any]) -> dict[str, Any]:
        """Attach a hybrid (or classical) signature object to a receipt copy."""
        out = dict(receipt)
        canonical = receipt_canonical(out)
        out["signature"] = self.sign_canonical(canonical)
        out["_canonical"] = canonical
        return out


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    classical_ok: bool
    pq_ok: bool | None
    hybrid: bool
    refused: bool
    reason: str
    mode: str  # "hybrid" | "classical" | "refused" | "fail"

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "classical_ok": self.classical_ok,
            "pq_ok": self.pq_ok,
            "hybrid": self.hybrid,
            "refused": self.refused,
            "reason": self.reason,
            "mode": self.mode,
        }


class HybridVerifier:
    """Offline verifier with optional phase-3 refuse-single-orbit gate."""

    def __init__(
        self,
        *,
        require_pq: bool = False,
        pinned_ed_b64: str | None = None,
        pinned_pq_b64: str | None = None,
    ) -> None:
        self.require_pq = require_pq
        self.pinned_ed_b64 = pinned_ed_b64
        self.pinned_pq_b64 = pinned_pq_b64

    @staticmethod
    def verify_ed25519(public_key_b64: str, value_b64: str, message: bytes) -> bool:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        try:
            pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
            pub.verify(base64.b64decode(value_b64), message)
            return True
        except (InvalidSignature, ValueError):
            return False

    @staticmethod
    def verify_ml_dsa(public_key_b64: str, value_b64: str, message: bytes) -> bool:
        if not _PQ_LIB:
            return False
        try:
            pk = base64.b64decode(public_key_b64)
            sig = base64.b64decode(value_b64)
            return bool(_MLDSA.verify(pk, message, sig))
        except Exception:
            return False

    def verify_envelope(self, sig: dict[str, Any], message: bytes) -> VerifyResult:
        hybrid = envelope_is_hybrid(sig)
        ed_key = self.pinned_ed_b64 or sig.get("public_key") or ""
        classical_ok = bool(
            ed_key and self.verify_ed25519(ed_key, sig.get("value", ""), message)
        )
        if not classical_ok:
            return VerifyResult(
                ok=False,
                classical_ok=False,
                pq_ok=None,
                hybrid=hybrid,
                refused=False,
                reason="Ed25519 verification failed",
                mode="fail",
            )

        if self.require_pq and not sig.get("pq_value"):
            return VerifyResult(
                ok=False,
                classical_ok=True,
                pq_ok=False,
                hybrid=False,
                refused=True,
                reason="refuse_single_orbit: classical-only envelope rejected (require_pq)",
                mode="refused",
            )

        if not sig.get("pq_value"):
            return VerifyResult(
                ok=True,
                classical_ok=True,
                pq_ok=None,
                hybrid=False,
                refused=False,
                reason="classical-only accepted (require_pq=False)",
                mode="classical",
            )

        if not _PQ_LIB:
            # Fail-closed on present PQ we cannot evaluate — never claim PQ success.
            return VerifyResult(
                ok=False,
                classical_ok=True,
                pq_ok=None,
                hybrid=hybrid,
                refused=False,
                reason=(
                    "pq_value present but dilithium-py missing — cannot verify PQ "
                    "(fail-closed). Classical Ed25519 alone is NOT treated as hybrid success."
                ),
                mode="fail",
            )

        presented = sig.get("pq_public_key", "")
        if self.pinned_pq_b64 and presented != self.pinned_pq_b64:
            return VerifyResult(
                ok=False,
                classical_ok=True,
                pq_ok=False,
                hybrid=hybrid,
                refused=False,
                reason="pinned PQ public key mismatch",
                mode="fail",
            )

        pq_ok = self.verify_ml_dsa(presented, sig.get("pq_value", ""), message)
        if not pq_ok:
            return VerifyResult(
                ok=False,
                classical_ok=True,
                pq_ok=False,
                hybrid=hybrid,
                refused=False,
                reason="ML-DSA-65 verification failed",
                mode="fail",
            )
        return VerifyResult(
            ok=True,
            classical_ok=True,
            pq_ok=True,
            hybrid=True,
            refused=False,
            reason="hybrid verified (Ed25519 + ML-DSA-65)",
            mode="hybrid",
        )

    def verify_receipt(self, receipt: dict[str, Any]) -> VerifyResult:
        sig = receipt.get("signature") or {}
        canonical = receipt.get("_canonical") or receipt_canonical(receipt)
        return self.verify_envelope(sig, canonical.encode())


def refuse_single_orbit(
    sig: dict[str, Any],
    message: bytes,
    *,
    pinned_ed_b64: str | None = None,
    pinned_pq_b64: str | None = None,
) -> VerifyResult:
    """Phase-3 gate: accept only hybrid envelopes that verify on both orbits."""
    return HybridVerifier(
        require_pq=True,
        pinned_ed_b64=pinned_ed_b64,
        pinned_pq_b64=pinned_pq_b64,
    ).verify_envelope(sig, message)


def why_hybrid_brief() -> dict[str, str]:
    """Teaching bullets for lab01 — not crypto claims about SIM data."""
    return {
        "classical_alone": (
            "Ed25519 alone is fine today, but signatures are about the past: "
            "a receipt disputed years later must already resist a quantum adversary."
        ),
        "pq_alone": (
            "ML-DSA alone breaks interop today — verifiers without the library "
            "fail-closed, and young PQ implementations must not be a forgery channel."
        ),
        "hybrid": (
            "Hybrid keeps Ed25519 authoritative and adds ML-DSA over the SAME canonical. "
            "Migration capability now; post-quantum security only after require_pq (phase 3)."
        ),
        "downgrade": (
            "Without refuse_single_orbit, an adversary who breaks Ed25519 strips pq_* "
            "and is accepted. Phase 3 closes that downgrade."
        ),
    }


def fetch_live_hybrid_envelope(
    url: str | None = None,
    *,
    timeout: float = 12.0,
) -> dict[str, Any]:
    """Fetch a LIVE hub well-known and inspect its hybrid signature envelope.

    Returns inspection metadata. Classical Ed25519 is verified offline when possible.
    PQ is verified only when dilithium-py is installed — otherwise labeled inspected-only.
    Never invents fake PQ success. Network failures raise; callers may skip.
    """
    target = (url or os.environ.get("PQC_COURSE_WELL_KNOWN") or DEFAULT_WELL_KNOWN).strip()
    req = urllib.request.Request(target, headers={"User-Agent": "pqc-hybrid-signing-course/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"live fetch failed: {exc}") from exc

    doc = json.loads(raw.decode())
    if not isinstance(doc, dict):
        raise RuntimeError("well-known document is not a JSON object")

    sig = doc.get("signature")
    if not isinstance(sig, dict):
        raise RuntimeError("well-known missing signature object")

    canonical = object_canonical(doc)
    hybrid = envelope_is_hybrid(sig)
    classical_ok = HybridVerifier.verify_ed25519(
        sig.get("public_key", ""), sig.get("value", ""), canonical.encode()
    )

    pq_status: str
    pq_ok: bool | None = None
    if not sig.get("pq_value"):
        pq_status = "absent"
    elif not _PQ_LIB:
        pq_status = "inspected_only_dilithium_missing"
        # Do NOT claim verify success.
    else:
        presented = sig.get("pq_public_key", "")
        pq_ok = HybridVerifier.verify_ml_dsa(
            presented, sig.get("pq_value", ""), canonical.encode()
        )
        pq_status = "verified" if pq_ok else "verify_failed"

    return {
        "source": "LIVE",
        "url": target,
        "hub_name": doc.get("name"),
        "hub_version": doc.get("hub_version"),
        "generated_at": doc.get("generated_at"),
        "signature": {
            "algorithm": sig.get("algorithm"),
            "pq_algorithm": sig.get("pq_algorithm"),
            "has_public_key": bool(sig.get("public_key")),
            "has_value": bool(sig.get("value")),
            "has_pq_public_key": bool(sig.get("pq_public_key")),
            "has_pq_value": bool(sig.get("pq_value")),
            "public_key_prefix": (sig.get("public_key") or "")[:16],
            "pq_public_key_prefix": (sig.get("pq_public_key") or "")[:16],
        },
        "hybrid": hybrid,
        "classical_verified_offline": classical_ok,
        "pq_status": pq_status,
        "pq_verified_offline": pq_ok,
        "canonical_len": len(canonical),
        "note": (
            "LIVE envelope from the hub — not a SIM. "
            + (
                "PQ orbit verified offline with dilithium-py."
                if pq_status == "verified"
                else (
                    "PQ fields present; local ML-DSA verify skipped (install dilithium-py)."
                    if pq_status == "inspected_only_dilithium_missing"
                    else f"PQ status={pq_status}."
                )
            )
        ),
    }


def demo_hybrid_roundtrip(*, require_pq: bool = False) -> dict[str, Any]:
    """Offline teaching roundtrip used by labs and tests (no network)."""
    signer = HybridSigner(enable_pq=True)
    receipt = {
        "capability": "course.demo@v1",
        "output_hash": "sha256:deadbeef",
        "issued_at": "2026-09-08T12:00:00Z",
        "request_id": "lab-demo-1",
    }
    signed = signer.sign_receipt(receipt)
    verifier = HybridVerifier(
        require_pq=require_pq,
        pinned_ed_b64=signer.public_key_b64,
        pinned_pq_b64=signer.pq_public_key_b64,
    )
    result = verifier.verify_receipt(signed)
    return {
        "identity": signer.identity().as_dict(),
        "pq_skipped": signer.pq_skipped,
        "pq_skip_reason": signer.pq_skip_reason,
        "signed": signed,
        "verify": result.as_dict(),
    }
