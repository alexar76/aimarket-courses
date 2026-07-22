"""Lab 04 — LUMEN PageRank scores (Module 4).

Call /api/reputation/lumen and bind scores to graph node ids.

Run:  python labs/lab04_lumen_scores.py
Exercise: python labs/run_exercises.py --module m4
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.viz import probe_lumen_scores, resolve_monitor_url


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    url, mock = resolve_monitor_url()
    try:
        lumen = probe_lumen_scores(url)
        if not lumen.ok:
            print(f"{t('labs.lab04.error')}: {lumen.error}")
        else:
            ranked = sorted(lumen.by_id().items(), key=lambda kv: kv[1], reverse=True)
            print(f"\n{t('ui.score')} ({len(ranked)} nodes):")
            for node_id, score in ranked:
                bar = "█" * int(score * 40)
                print(f"  {node_id:24s} {score:.4f}  {bar}")
                trace.log("lumen_score", node=node_id, score=round(score, 4))
            if lumen.iterations is not None:
                print(f"\n{t('labs.lab04.iterations')}: {lumen.iterations}")
    finally:
        if mock:
            mock.stop()

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
