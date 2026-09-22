"""Lab 03 — Sign a receipt (Module 3).

Concept: dual-signature envelope over the same receipt canonical.
Run:  python labs/lab03_sign_receipt.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.pqc import HybridSigner, envelope_is_hybrid
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    signer = HybridSigner(enable_pq=True)
    receipt = {
        "capability": "atlas.situation.brief@v1",
        "output_hash": "sha256:9f86d081884c7d659a2feaa0c55ad015",
        "issued_at": "2026-09-08T12:00:00Z",
        "request_id": "lab03-receipt",
    }
    signed = signer.sign_receipt(receipt)
    sig = signed["signature"]

    print(f"\n{t('ui.proof')}: algorithm={sig['algorithm']}")
    print(f"  pq_algorithm={sig.get('pq_algorithm')}")
    print(f"  hybrid={envelope_is_hybrid(sig)}")
    if sig.get("pq_skipped"):
        print(f"  {t('ui.blocked')}: {sig.get('pq_skip_reason')}")
        print(f"  {t('labs.lab03.pq_skipped_note')}")
    else:
        print(f"  value_len={len(sig.get('value', ''))}")
        print(f"  pq_value_len={len(sig.get('pq_value', ''))}")

    print(f"\n{t('ui.result')}: canonical={signed['_canonical'][:72]}…")
    trace.log(
        "sign_receipt",
        hybrid=envelope_is_hybrid(sig),
        pq_skipped=bool(sig.get("pq_skipped")),
        capability=receipt["capability"],
    )

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("labs.lab03_sign_receipt.hint"))


if __name__ == "__main__":
    main()
