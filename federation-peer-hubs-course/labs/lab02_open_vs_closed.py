"""Lab 02 — Open door vs closed door (Module 2).

Live ``GET /ai-market/v2/federation/peers``: ``open_federation`` is the door.
Pending peers can exist either way; preview quarantine is a separate switch.

Run:  python labs/lab02_open_vs_closed.py
      COURSE_OFFLINE=1 python labs/lab02_open_vs_closed.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.federation import (
    DEFAULT_HUB,
    FIXTURE_PEERS,
    FederationError,
    list_peers,
    open_vs_closed,
)
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    offline = os.environ.get("COURSE_OFFLINE", "").strip().lower() in ("1", "true", "yes")
    if offline:
        payload = FIXTURE_PEERS
        print(f"\n{t('labs.lab02.source')}: fixture (not LIVE)")
        trace.log("fixture_peers", live=False)
    else:
        print(f"\n{t('labs.lab02.source')}: LIVE {DEFAULT_HUB}/ai-market/v2/federation/peers")
        try:
            payload = list_peers(DEFAULT_HUB)
            trace.log("live_peers", count=payload.get("count"), pending=payload.get("pending_count"))
        except FederationError as exc:
            print(f"{t('ui.error')}: {exc}")
            payload = FIXTURE_PEERS
            print(t("labs.lab02.fallback"))
            trace.log("fallback_fixture", reason=str(exc))

    model = open_vs_closed(payload)
    print(f"\n{t('labs.lab02.door')}: {model['door']}  (open_federation={model['open_federation']})")
    print(f"{t('labs.lab02.trusted')}: {model['trusted_count']}")
    print(f"{t('labs.lab02.pending')}: {model['pending_count']}")
    print(f"{t('labs.lab02.preview_switch')}: {model['preview_independent_of_door']}")
    print(f"\n{t('labs.lab02.teaching')}:")
    for key, text in model["teaching"].items():
        print(f"  [{key}] {text}")

    # Closed-door teaching counterfactual from the same pending queue
    closed = open_vs_closed({**payload, "open_federation": False})
    print(f"\n{t('labs.lab02.counterfactual')}: door={closed['door']} pending={closed['pending_count']}")
    print(t("labs.lab02.counterfactual_note"))
    trace.log("door_model", door=model["door"], pending=model["pending_count"])

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event["kind"], {k: v for k, v in event.items() if k != "kind"})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
