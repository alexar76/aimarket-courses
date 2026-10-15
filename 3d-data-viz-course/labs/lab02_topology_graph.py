"""Lab 02 — Topology graph (Module 2).

Parse /api/topology into typed MonitorNode / MonitorLink structures.

Run:  python labs/lab02_topology_graph.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.viz import probe_topology, resolve_monitor_url


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    url, mock = resolve_monitor_url()
    try:
        graph = probe_topology(url)
        print(f"\n{t('labs.lab02.nodes')}: {len(graph.nodes)}")
        print(f"{t('labs.lab02.links')}: {len(graph.links)}")
        for node in graph.nodes[:6]:
            pos = node.position
            print(
                f"  {node.id:20s} group={node.group:8s} "
                f"pos=({pos.x:.1f},{pos.y:.1f},{pos.z:.1f}) status={node.status}"
            )
            trace.log("node", id=node.id, group=node.group)
        edges = graph.adjacency()
        print(f"\n{t('labs.lab02.adjacency')}: {len(edges)} directed edges")
    finally:
        if mock:
            mock.stop()

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
