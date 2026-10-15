"""Lab 01 — Why hybrid (Module 1).

Concept: classical breaks later; PQ alone breaks interop today; hybrid migrates safely.
Run:  python labs/lab01_why_hybrid.py
      COURSE_LANG=ru python labs/lab01_why_hybrid.py
Optional LIVE: set PQC_COURSE_FETCH_LIVE=1 to inspect modelmarket.dev hybrid envelope.
"""

from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.pqc import (
    envelope_is_hybrid,
    fetch_live_hybrid_envelope,
    pqc_available,
    why_hybrid_brief,
)
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))
    print(f"{t('modules.m1.industry')}: {t('labs.lab01.industry_note')}")

    brief = why_hybrid_brief()
    for key in ("classical_alone", "pq_alone", "hybrid", "downgrade"):
        print(f"\n[{key}]")
        print(f"  {brief[key]}")
        trace.log("why_hybrid", point=key)

    # Shape check — not cryptography, just the envelope contract.
    classical_shape = {"algorithm": "ed25519", "public_key": "…", "value": "…"}
    hybrid_shape = {
        **classical_shape,
        "pq_algorithm": "ml-dsa-65",
        "pq_public_key": "…",
        "pq_value": "…",
    }
    print(f"\n{t('ui.proof')}: classical hybrid? {envelope_is_hybrid(classical_shape)}")
    print(f"{t('ui.proof')}: dual-orbit hybrid? {envelope_is_hybrid(hybrid_shape)}")
    print(f"{t('ui.result')}: dilithium-py available locally? {pqc_available()}")
    trace.log(
        "shape",
        classical_hybrid=envelope_is_hybrid(classical_shape),
        dual_hybrid=envelope_is_hybrid(hybrid_shape),
        pqc_lib=pqc_available(),
    )

    if os.environ.get("PQC_COURSE_FETCH_LIVE", "").strip() in ("1", "true", "yes", "on"):
        try:
            live = fetch_live_hybrid_envelope()
            print(f"\n{t('ui.verify')} LIVE ({live['url']}):")
            print(f"  source={live['source']} hybrid={live['hybrid']}")
            print(f"  classical_verified_offline={live['classical_verified_offline']}")
            print(f"  pq_status={live['pq_status']}")
            print(f"  note={live['note']}")
            trace.log("live_fetch", hybrid=live["hybrid"], pq_status=live["pq_status"])
        except Exception as exc:
            print(f"\n{t('ui.blocked')}: live fetch skipped — {exc}")
            trace.log("live_fetch", error=str(exc))
    else:
        print(f"\n{t('labs.lab01.live_hint')}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("labs.lab01_why_hybrid.hint"))


if __name__ == "__main__":
    main()
