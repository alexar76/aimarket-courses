"""Lab 05 — Capstone: hybrid gate / refuse single orbit (Module 5).

Concept: phase-3 policy rejects classical-only envelopes even if Ed25519 verifies.
Run:  python labs/lab05_hybrid_gate_capstone.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.pqc import (
    HybridSigner,
    HybridVerifier,
    envelope_is_hybrid,
    pqc_available,
    refuse_single_orbit,
    strip_pq,
)
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    signer = HybridSigner(enable_pq=True)
    signed = signer.sign_receipt(
        {
            "capability": "course.gate@v1",
            "output_hash": "sha256:capstone",
            "issued_at": "2026-09-08T12:00:00Z",
            "request_id": "lab05",
        }
    )
    msg = signed["_canonical"].encode()
    sig = signed["signature"]

    # Gate 1 — classical-only (downgrade) MUST be refused.
    stripped = strip_pq(sig)
    refused = refuse_single_orbit(
        stripped, msg, pinned_ed_b64=signer.public_key_b64
    )
    print(f"\n{t('ui.blocked')} single-orbit: {refused.as_dict()}")
    assert refused.refused and not refused.ok
    trace.log("refuse_single_orbit", ok=refused.ok, refused=refused.refused)

    # Gate 2 — permissive verifier still accepts classical-only (migration phase).
    permissive = HybridVerifier(require_pq=False, pinned_ed_b64=signer.public_key_b64)
    allowed = permissive.verify_envelope(stripped, msg)
    print(f"{t('ui.allowed')} require_pq=False: mode={allowed.mode} ok={allowed.ok}")
    assert allowed.ok and allowed.mode == "classical"
    trace.log("permissive_classical", ok=allowed.ok, mode=allowed.mode)

    # Gate 3 — full hybrid accepted only when PQ is real locally.
    if pqc_available() and envelope_is_hybrid(sig):
        accepted = refuse_single_orbit(
            sig,
            msg,
            pinned_ed_b64=signer.public_key_b64,
            pinned_pq_b64=signer.pq_public_key_b64,
        )
        print(f"{t('ui.success')} hybrid gate: {accepted.as_dict()}")
        assert accepted.ok and accepted.hybrid
        trace.log("hybrid_accepted", ok=accepted.ok, hybrid=accepted.hybrid)
    else:
        print(f"{t('ui.blocked')}: {signer.pq_skip_reason or 'PQ unavailable'}")
        print(t("labs.lab05.pq_skipped_note"))
        trace.log("hybrid_accept_skipped", pq_lib=pqc_available())

    print(f"\n{t('ui.result')}: {t('labs.lab05.takeaway')}")
    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("labs.lab05_hybrid_gate_capstone.hint"))


if __name__ == "__main__":
    main()
