"""Lab 03 — Federation reputation peers (Module 3).

Probe /api/reputation/peers for Hub trust enrichment.

Run:  python labs/lab03_reputation_peers.py
Exercise: python labs/run_exercises.py --module m3
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.viz import probe_reputation_peers, resolve_monitor_url


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    url, mock = resolve_monitor_url()
    try:
        peers = probe_reputation_peers(url)
        print(f"\n{t('labs.lab03.count')}: {peers.count} ({peers.mode})")
        for peer in peers.peers:
            score = peer.trust_score if peer.trust_score is not None else "—"
            print(f"  {peer.name:16s} trust={score}  {peer.url}")
            trace.log("peer", name=peer.name, trust=peer.trust_score)
    finally:
        if mock:
            mock.stop()

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
