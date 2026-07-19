"""Lab 05 — Capstone: factory probe (Module 5).

End-to-end probe: pipeline status + products catalog.
Run:  python labs/lab05_factory_capstone.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.factory import probe_factory
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    out = probe_factory()
    st = out["status"]
    cat = out["catalog"]
    trace.log(
        "capstone",
        in_pipeline=st["products_in_pipeline"],
        shipped=st["products_shipped"],
        products=cat["count"],
        source=st["source"],
    )

    print(f"{t('ui.result')}: in_pipeline={st['products_in_pipeline']} shipped={st['products_shipped']}")
    print(f"{t('labs.lab05.products')}: {cat['count']} via {cat['source']}")
    print(f"{t('labs.lab05.phases')}: {', '.join(out['phases'])}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
