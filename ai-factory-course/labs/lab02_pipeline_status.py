"""Lab 02 — Pipeline status API (Module 2).

GET /api/public/pipeline-status — live factory or embedded mock.
Run:  python labs/lab02_pipeline_status.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.factory import factory_client
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    with factory_client() as client:
        status = client.get_pipeline_status()
    trace.log("pipeline_status", **status)

    print(f"{t('labs.lab02.in_pipeline')}: {status['products_in_pipeline']}")
    print(f"{t('labs.lab02.shipped')}: {status['products_shipped']}")
    print(f"{t('labs.lab02.source')}: {status['source']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
