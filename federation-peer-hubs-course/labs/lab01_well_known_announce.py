"""Lab 01 — Well-known & announce (Module 1).

Live GET ``/.well-known/ai-market.json`` on the public hub: name, federated
capability count, signer key, and hybrid (Ed25519 + ML-DSA) signature fields.
A knock is only an observation — it must never index a catalogue.

Run:  python labs/lab01_well_known_announce.py
      COURSE_LANG=ru python labs/lab01_well_known_announce.py
      COURSE_OFFLINE=1 python labs/lab01_well_known_announce.py   # fixture only
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.federation import (
    DEFAULT_HUB,
    FederationError,
    fixture_probe,
    hybrid_signature_info,
    well_known,
)
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    offline = os.environ.get("COURSE_OFFLINE", "").strip().lower() in ("1", "true", "yes")
    if offline:
        probe = fixture_probe()
        wk = {
            "name": probe["name"],
            "hub_version": probe["hub_version"],
            "federated_capabilities_count": probe["federated_capabilities_count"],
            "signer_public_key": "fixture-ed25519-pubkey",
            "signature": {
                "algorithm": "ed25519",
                "pq_algorithm": "ml-dsa-65",
                "value": "fixture-sig",
                "pq_public_key": "x",
                "pq_value": "y",
            },
        }
        print(f"\n{t('labs.lab01.source')}: fixture (COURSE_OFFLINE=1) — not LIVE")
        trace.log("fixture_well_known", live=False)
    else:
        hub = DEFAULT_HUB
        print(f"\n{t('labs.lab01.source')}: LIVE {hub}{t('labs.lab01.well_known_path')}")
        try:
            wk = well_known(hub)
            trace.log("live_well_known", hub=hub, name=wk.get("name"))
        except FederationError as exc:
            print(f"{t('ui.error')}: {exc}")
            print(t("labs.lab01.offline_hint"))
            probe = fixture_probe()
            print(f"\n{t('labs.lab01.fallback')}: fixture (labelled, not LIVE)")
            wk = {
                "name": probe["name"],
                "hub_version": probe["hub_version"],
                "federated_capabilities_count": probe["federated_capabilities_count"],
                "signer_public_key": "fixture-ed25519-pubkey",
                "signature": {
                    "algorithm": "ed25519",
                    "pq_algorithm": "ml-dsa-65",
                    "value": "x",
                    "pq_public_key": "y",
                    "pq_value": "z",
                },
            }
            trace.log("fallback_fixture", reason=str(exc))

    sig = hybrid_signature_info(wk)
    print(f"\n{t('labs.lab01.name')}: {wk.get('name')}")
    print(f"{t('labs.lab01.version')}: {wk.get('hub_version')}")
    print(f"{t('labs.lab01.federated_count')}: {wk.get('federated_capabilities_count')}")
    print(f"{t('labs.lab01.signer')}: {sig['signer_public_key']}…")
    print(f"{t('labs.lab01.classical')}: {sig['algorithm']}  hybrid={sig['hybrid']}")
    if sig["pq_algorithm"]:
        print(f"{t('labs.lab01.pq')}: {sig['pq_algorithm']}")
    print(f"\n{t('labs.lab01.knock_note')}")
    trace.log("signature", hybrid=sig["hybrid"], pq=sig["pq_algorithm"])

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event["kind"], {k: v for k, v in event.items() if k != "kind"})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
