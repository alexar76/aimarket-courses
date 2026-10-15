"""Lab 04 — Orchestrator stage flow (Module 4).

Walk IDEA_RECEIVED → COMPLETED using pipeline_flow.json.
Run:  python labs/lab04_orchestrator_stages.py
Exercise: python labs/run_exercises.py --module m4
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.factory import walk_to_ship
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    path = walk_to_ship()
    print(f"\n--- {t('labs.lab04.path_heading')} ({len(path)} steps) ---")
    for step in path[:8]:
        trace.log("transition", state=step["state"], agent=step.get("agent") or "—")
        agent = step.get("agent") or "—"
        print(f"  {step['state']:24} agent={agent}")
    if len(path) > 8:
        print(f"  … +{len(path) - 8} more → {path[-1]['state']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
