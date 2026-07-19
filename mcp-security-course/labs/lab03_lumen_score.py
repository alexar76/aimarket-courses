"""Lab 03 — LUMEN trust scoring (Module 3).

Score MCP servers on a trust graph using the LUMEN PageRank oracle.

Run:  python labs/lab03_lumen_score.py
      COURSE_LANG=ru python labs/lab03_lumen_score.py
Exercise: python labs/run_exercises.py --module m3
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.lumen import demo_mcp_trust_graph, score_servers
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    graph = demo_mcp_trust_graph()
    scores = score_servers(graph)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

    print(f"\n{t('labs.lab03.graph_heading')} ({len(graph.nodes)} nodes, {len(graph.edges)} edges)")
    for src, dst, w in graph.edges:
        print(f"  {src} → {dst}  (w={w})")

    print(f"\n{t('ui.score')} ({t('labs.lab03.pagerank')}):")
    for server_id, score in ranked:
        bar = "█" * int(score * 40)
        print(f"  {server_id:28s} {score:.4f}  {bar}")
        trace.log("trust_score", server=server_id, score=round(score, 4))

    top = ranked[0][0]
    bottom = ranked[-1][0]
    print(f"\n{t('labs.lab03.top')}: {top}")
    print(f"{t('labs.lab03.bottom')}: {bottom}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
