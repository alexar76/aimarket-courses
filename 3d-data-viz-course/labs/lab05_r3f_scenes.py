"""Lab 05 — R3F oracle scene mapping (Module 5).

Map oracle nodes from the topology graph to React Three Fiber scene specs.

Run:  python labs/lab05_r3f_scenes.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.viz import map_graph_to_r3f_scenes, probe_topology, resolve_monitor_url


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    url, mock = resolve_monitor_url()
    try:
        graph = probe_topology(url)
        scenes = map_graph_to_r3f_scenes(graph)
        print(f"\n{t('labs.lab05.scenes')}: {len(scenes)}")
        for spec in scenes:
            cam = spec.camera
            kind = "ambient" if spec.ambient else "r3f"
            print(f"\n  {spec.slug} ({kind})")
            print(f"    camera: ({cam[0]}, {cam[1]}, {cam[2]})")
            print(f"    accent: {spec.accent}")
            print(f"    primitive: {spec.primitive[:72]}…")
            trace.log("r3f_scene", slug=spec.slug, ambient=spec.ambient)
    finally:
        if mock:
            mock.stop()

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
