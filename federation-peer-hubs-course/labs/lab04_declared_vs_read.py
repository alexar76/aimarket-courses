"""Lab 04 — Declared vs read counts (Module 4).

What a peer claims ≠ what this hub verified. Pending rows expose both
``declared_capabilities`` and ``preview_capabilities``; trusted rows expose
the indexed ``capabilities_count``. Operator UIs must show both.

Run:  python labs/lab04_declared_vs_read.py
      COURSE_OFFLINE=1 python labs/lab04_declared_vs_read.py
Exercise: python labs/run_exercises.py --module m4
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
    peer_summary,
    well_known,
)
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    offline = os.environ.get("COURSE_OFFLINE", "").strip().lower() in ("1", "true", "yes")
    if offline:
        payload = FIXTURE_PEERS
        fed_count = 12
        print(f"\n{t('labs.lab04.source')}: fixture (not LIVE)")
        trace.log("fixture_counts", live=False)
    else:
        print(f"\n{t('labs.lab04.source')}: LIVE {DEFAULT_HUB}")
        try:
            payload = list_peers(DEFAULT_HUB)
            wk = well_known(DEFAULT_HUB)
            fed_count = int(wk.get("federated_capabilities_count") or 0)
            trace.log("live_counts", peers=payload.get("count"), federated=fed_count)
        except FederationError as exc:
            print(f"{t('ui.error')}: {exc}")
            payload = FIXTURE_PEERS
            fed_count = 12
            print(t("labs.lab04.fallback"))
            trace.log("fallback_fixture", reason=str(exc))

    print(f"\n{t('labs.lab04.hub_federated')}: {fed_count}")
    print(f"\n{t('labs.lab04.trusted_heading')}:")
    indexed_sum = 0
    for peer in (payload.get("peers") or [])[:6]:
        s = peer_summary(peer, role="trusted")
        indexed_sum += int(s["observed_capabilities"])
        print(
            f"  {s['name'][:40]:40}  indexed={s['observed_capabilities']:4}  "
            f"trust={s['trust_score']}  status={s['status']}"
        )
        trace.log("trusted_peer", url=s["url"], indexed=s["observed_capabilities"])

    print(f"\n{t('labs.lab04.pending_heading')}:")
    pending = payload.get("pending") or []
    if not pending:
        print(f"  {t('labs.lab04.no_pending')}")
        # Teaching fixture so the honesty gap is still visible offline/live-empty
        demo = peer_summary(FIXTURE_PEERS["pending"][0], role="pending")
        print(f"  {t('labs.lab04.demo_gap')}:")
        print(
            f"    stranger declared={demo['declared_capabilities']} "
            f"preview/read={demo['observed_capabilities']} gap={demo['gap']}"
        )
        print(f"    {demo['honesty_note']}")
        trace.log("demo_honesty_gap", gap=demo["gap"])
    else:
        for peer in pending[:6]:
            s = peer_summary(peer, role="pending")
            print(
                f"  {s['name'][:40]:40}  declared={s['declared_capabilities']:4}  "
                f"preview={s['observed_capabilities']:4}  gap={s['gap']}"
            )
            print(f"    {s['honesty_note']}")
            trace.log(
                "pending_peer",
                url=s["url"],
                declared=s["declared_capabilities"],
                preview=s["observed_capabilities"],
            )

    print(f"\n{t('labs.lab04.sum_note')}: indexed_peers≈{indexed_sum}  hub_federated={fed_count}")
    print(t("labs.lab04.ui_rule"))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event["kind"], {k: v for k, v in event.items() if k != "kind"})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
