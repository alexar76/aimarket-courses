"""Lab 03 — Preview quarantine (Module 3).

Pending peer manifests land in a quarantine table. Search, invoke, and the
published catalogue never read it. Live peer snapshot shows the empty-or-pending queue.

Run:  python labs/lab03_preview_quarantine.py
      COURSE_OFFLINE=1 python labs/lab03_preview_quarantine.py
Exercise: python labs/run_exercises.py --module m3
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
    preview_quarantine,
)
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    offline = os.environ.get("COURSE_OFFLINE", "").strip().lower() in ("1", "true", "yes")
    if offline:
        q = preview_quarantine(peers_payload=FIXTURE_PEERS)
        print(f"\n{t('labs.lab03.source')}: fixture (not LIVE)")
        trace.log("fixture_quarantine", pending=q["pending_count"])
    else:
        print(f"\n{t('labs.lab03.source')}: LIVE {DEFAULT_HUB}")
        try:
            peers = list_peers(DEFAULT_HUB)
            q = preview_quarantine(DEFAULT_HUB, peers_payload=peers)
            trace.log("live_quarantine", pending=q["pending_count"])
        except FederationError as exc:
            print(f"{t('ui.error')}: {exc}")
            q = preview_quarantine(peers_payload=FIXTURE_PEERS)
            print(t("labs.lab03.fallback"))
            trace.log("fallback_fixture", reason=str(exc))

    print(f"\n{t('labs.lab03.rule')}:")
    print(f"  {q['rule']}")
    print(f"\n{t('labs.lab03.guards')}:")
    print(f"  search_reads_preview_table = {q['search_reads_preview_table']}")
    print(f"  invoke_reads_preview_table = {q['invoke_reads_preview_table']}")
    print(f"  manifest_reads_preview_table = {q['manifest_reads_preview_table']}")
    print(f"\n{t('labs.lab03.pending_count')}: {q['pending_count']}")
    if q["pending_snapshot"]:
        print(f"{t('labs.lab03.snapshot')}:")
        for row in q["pending_snapshot"]:
            print(
                f"  {row.get('name') or row.get('url')}: "
                f"declared={row.get('declared_capabilities')} "
                f"preview={row.get('preview_capabilities')} "
                f"assay={row.get('assay_verdict')}"
            )
            trace.log("pending_row", url=row.get("url"), preview=row.get("preview_capabilities"))
    elif q.get("empty_pending_note"):
        print(f"{t('labs.lab03.empty')}: {q['empty_pending_note']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event["kind"], {k: v for k, v in event.items() if k != "kind"})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
