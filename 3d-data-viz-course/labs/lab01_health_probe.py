"""Lab 01 — Monitor health probe (Module 1).

Probe alien-monitor /api/health (live or mock server).

Run:  python labs/lab01_health_probe.py
      COURSE_LANG=ru python labs/lab01_health_probe.py
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.viz import monitor_reachable, probe_health, resolve_monitor_url


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    live = monitor_reachable()
    print(f"\n{t('labs.lab01.live')}: {live}")
    url, mock = resolve_monitor_url()
    try:
        health = probe_health(url)
        print(f"{t('ui.result')}: status={health.status} mode={health.mode}")
        trace.log("health", status=health.status, mode=health.mode, url=url)
        if mock:
            print(t("labs.lab01.mock_note"))
    finally:
        if mock:
            mock.stop()

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
