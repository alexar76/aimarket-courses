"""Lab 01 - Protocol v2 overview (Module 1).

Parse the well-known manifest and validate a capability catalog against
Protocol v2 shapes. Uses hub-lite for live JSON — no git clones.

Run:  python labs/lab01_protocol_overview.py   (COURSE_LANG=ru|es to localize)
Needs: pip install -e ".[hub-lite]"
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.hub_lite import embedded_hub_lite
from courselib.i18n import get_translator
from courselib.orchestration import Trace
from courselib.protocol import validate_manifest, validate_well_known


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    trace = Trace()

    with embedded_hub_lite() as hub:
        wk = hub.well_known()
        wk_errors = validate_well_known(wk)
        trace.emit("well_known", name=wk.get("name"), valid=not wk_errors)
        print(f"\n{t('ui.hub')}:", wk.get("name"))
        print(f"{t('ui.protocol')}:", ", ".join(wk.get("protocol_versions", [])))
        print(f"{t('labs.lab01.well_known_valid')}:", "yes" if not wk_errors else wk_errors)

        manifest = hub.manifest()
        man_errors = validate_manifest(manifest)
        trace.emit("manifest", tools=len(manifest.get("tools", [])), valid=not man_errors)
        print(f"\n{t('labs.lab01.manifest_tools')}: {len(manifest.get('tools', []))}")
        print(f"{t('labs.lab01.manifest_valid')}:", "yes" if not man_errors else man_errors)
        if manifest.get("tools"):
            tool = manifest["tools"][0]
            print(f"  {t('ui.sample')}: {tool.get('name')}  ${tool.get('price_per_call_usd')}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
