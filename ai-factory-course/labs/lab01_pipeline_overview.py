"""Lab 01 — Pipeline overview (Module 1).

Research → design → build → test → ship as orchestrated stages.
Run:  python labs/lab01_pipeline_overview.py
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.factory import PIPELINE_PHASES
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    print(f"\n--- {t('labs.lab01.phases_heading')} ---")
    for phase, agent, state in PIPELINE_PHASES:
        trace.log("phase", phase=phase, agent=agent, state=state)
        print(f"  {phase:8} → {agent:12} → {state}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
