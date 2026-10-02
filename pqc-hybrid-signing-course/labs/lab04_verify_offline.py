"""Lab 04 — Verify offline (Module 4).

Concept: check both orbits without calling the hub back.
Run:  python labs/lab04_verify_offline.py
Optional LIVE: PQC_COURSE_FETCH_LIVE=1 inspects + verifies classical on modelmarket.dev.
"""

from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.pqc import (
    HybridSigner,
    HybridVerifier,
    fetch_live_hybrid_envelope,
    pqc_available,
)
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    signer = HybridSigner(enable_pq=True)
    signed = signer.sign_receipt(
        {
            "capability": "course.verify@v1",
            "output_hash": "sha256:offline",
            "issued_at": "2026-09-08T12:00:00Z",
            "request_id": "lab04",
        }
    )
    verifier = HybridVerifier(
        require_pq=False,
        pinned_ed_b64=signer.public_key_b64,
        pinned_pq_b64=signer.pq_public_key_b64,
    )
    result = verifier.verify_receipt(signed)

    print(f"\n{t('ui.verify')}: {result.as_dict()}")
    if signer.pq_skipped:
        print(f"{t('ui.blocked')}: {signer.pq_skip_reason}")
        print(t("labs.lab04.pq_skipped_note"))
    else:
        print(f"{t('ui.success')}: {result.reason}")

    # Tamper must fail classical.
    tampered = dict(signed)
    tampered["output_hash"] = "sha256:tampered"
    # Recompute would change canonical — leave stale signature intentionally.
    bad = HybridVerifier(
        pinned_ed_b64=signer.public_key_b64,
        pinned_pq_b64=signer.pq_public_key_b64,
    ).verify_envelope(tampered["signature"], tampered.get("_canonical", "x").encode())
    # Force wrong message:
    bad2 = HybridVerifier(pinned_ed_b64=signer.public_key_b64).verify_envelope(
        signed["signature"], b"not-the-canonical"
    )
    print(f"{t('ui.proof')}: wrong-message classical_ok={bad2.classical_ok}")
    trace.log(
        "verify_offline",
        ok=result.ok,
        classical_ok=result.classical_ok,
        pq_ok=result.pq_ok,
        tamper_rejected=not bad2.classical_ok,
        pqc_lib=pqc_available(),
    )
    _ = bad  # quiet unused if refactor

    if os.environ.get("PQC_COURSE_FETCH_LIVE", "").strip() in ("1", "true", "yes", "on"):
        try:
            live = fetch_live_hybrid_envelope()
            print(f"\n{t('ui.verify')} LIVE:")
            print(f"  classical_verified_offline={live['classical_verified_offline']}")
            print(f"  pq_status={live['pq_status']}")
            print(f"  note={live['note']}")
            trace.log("live_verify", **{k: live[k] for k in ("hybrid", "pq_status", "classical_verified_offline")})
        except Exception as exc:
            print(f"\n{t('ui.blocked')}: live fetch skipped — {exc}")
            trace.log("live_verify", error=str(exc))
    else:
        print(f"\n{t('labs.lab04.live_hint')}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("labs.lab04_verify_offline.hint"))


if __name__ == "__main__":
    main()
