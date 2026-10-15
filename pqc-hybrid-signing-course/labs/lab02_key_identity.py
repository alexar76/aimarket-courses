"""Lab 02 — Key material & dual-orbit identity (Module 2).

Concept: Ed25519 + ML-DSA-65 public keys form one peer identity.
Run:  python labs/lab02_key_identity.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.pqc import HybridSigner, pqc_available
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    signer = HybridSigner(enable_pq=True)
    ident = signer.identity()
    print(f"\n{t('ui.result')}: {ident.note}")
    print(f"  classical={ident.classical_public_key_b64[:24]}…")
    if ident.pq_public_key_b64:
        print(f"  pq={ident.pq_public_key_b64[:24]}…")
    else:
        print(f"  pq=SKIPPED ({signer.pq_skip_reason})")

    trace.log(
        "identity",
        pq_enabled=ident.pq_enabled,
        pq_lib=pqc_available(),
        pq_skipped=signer.pq_skipped,
    )

    print(f"\n{t('ui.proof')}: dual-orbit={ident.pq_enabled}")
    print(f"{t('labs.lab02.pinning_note')}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("labs.lab02_key_identity.hint"))


if __name__ == "__main__":
    main()
