"""Lab 05 — Capstone: approve a stranger (Module 5).

Walk announce → pending → preview → approve → crawl as a checklist, then
probe the live public hub. Admin Approve is not exercised here (needs a
token); the lab teaches the operator path against real peer data.

Run:  python labs/lab05_approve_capstone.py
      COURSE_OFFLINE=1 python labs/lab05_approve_capstone.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.federation import (
    DEFAULT_HUB,
    FederationError,
    announce_checklist,
    fixture_probe,
    live_probe,
)
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    print(f"\n--- {t('labs.lab05.checklist_heading')} ---")
    for i, row in enumerate(announce_checklist(), 1):
        print(f"  {i}. [{row['step']}] {row['detail']}")
        trace.log("checklist_step", step=row["step"])

    offline = os.environ.get("COURSE_OFFLINE", "").strip().lower() in ("1", "true", "yes")
    if offline:
        probe = fixture_probe()
        print(f"\n{t('labs.lab05.source')}: fixture (not LIVE)")
    else:
        print(f"\n{t('labs.lab05.source')}: LIVE probe {DEFAULT_HUB}")
        try:
            probe = live_probe(DEFAULT_HUB)
            trace.log("live_probe", hub=probe["hub"], name=probe["name"])
        except FederationError as exc:
            print(f"{t('ui.error')}: {exc}")
            probe = fixture_probe()
            print(t("labs.lab05.fallback"))
            trace.log("fallback_fixture", reason=str(exc))

    print(f"\n{t('labs.lab05.probe_heading')}:")
    print(f"  hub={probe['hub']}  live={probe['live']}")
    print(f"  name={probe['name']}  version={probe.get('hub_version')}")
    print(f"  federated_capabilities={probe.get('federated_capabilities_count')}")
    sig = probe.get("signature") or {}
    print(f"  hybrid_signature={sig.get('hybrid')}  pq={sig.get('pq_algorithm')}")
    door = probe.get("door") or {}
    print(f"  door={door.get('door')}  pending={door.get('pending_count')}  trusted={door.get('trusted_count')}")

    print(f"\n{t('labs.lab05.peers_heading')}:")
    for s in (probe.get("trusted_peers") or [])[:5]:
        print(f"  ✓ {s['name'][:48]}  caps={s['observed_capabilities']}  trust={s['trust_score']}")
    pending = probe.get("pending_peers") or []
    if pending:
        for s in pending[:5]:
            print(
                f"  ○ {s['name'][:48]}  declared={s['declared_capabilities']} "
                f"preview={s['observed_capabilities']}"
            )
    else:
        print(f"  {t('labs.lab05.no_pending')}")

    print(f"\n{t('labs.lab05.operator_note')}")
    print(t("labs.lab05.docs_hint"))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event["kind"], {k: v for k, v in event.items() if k != "kind"})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
