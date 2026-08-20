"""Lab 01 — Keystone nodes & percolation (Module 2).

Find critical nodes whose removal collapses a trust graph using PERCOLA.

Run:  python labs/lab01_keystone_nodes.py
      COURSE_LANG=ru python labs/lab01_keystone_nodes.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.trust import analyze_percolation, two_cliques_bridge_edges


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    edges = two_cliques_bridge_edges()
    out = analyze_percolation(edges, samples=9)
    trace.log("percolation", f_c=out["f_c"], keystones=out["keystones"], verified=out["verified"])

    print(f"\n{t('labs.lab01.graph_heading')}: {len(edges)} edges")
    print(f"{t('ui.proof')}: f_c={out['f_c']:.4f}  robustness={out['robustness']:.4f}")
    print(f"{t('labs.lab01.keystones')}: {', '.join(out['keystones'][:6])}")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
