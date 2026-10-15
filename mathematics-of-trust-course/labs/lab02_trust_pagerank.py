"""Lab 02 — EigenTrust PageRank (Module 1).

Score agents on a who-trusts-whom graph with LUMEN PageRank.

Run:  python labs/lab02_trust_pagerank.py
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.trust import demo_trust_graph, score_pagerank


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    graph = demo_trust_graph()
    scores = score_pagerank(graph)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

    print(f"\n{t('labs.lab02.graph_heading')} ({len(graph.nodes)} nodes)")
    for src, dst, w in graph.edges:
        print(f"  {src} → {dst}  (w={w})")

    print(f"\n{t('ui.score')} (PageRank):")
    for node_id, score in ranked:
        bar = "█" * int(score * 40)
        print(f"  {node_id:12s} {score:.4f}  {bar}")
        trace.log("trust_score", node=node_id, score=round(score, 4))

    print(f"\n{t('labs.lab02.top')}: {ranked[0][0]}")
    print(f"{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
