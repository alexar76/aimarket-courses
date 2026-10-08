"""Lab 05 - Publish a metered capability (Module 5).

Register a new paid capability on the embedded hub, validate the manifest
updates, and invoke it — the provider side of the agent economy.

Run:  python labs/lab05_publish_capability.py   (COURSE_LANG=ru|es to localize)
Needs: pip install -e ".[hub-lite]"
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.hub_lite import embedded_hub_lite
from courselib.i18n import get_translator
from courselib.orchestration import Trace
from courselib.protocol import validate_manifest


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    trace = Trace()
    product_id = "prod-course"
    capability_id = "sentiment.metered@v1"

    with embedded_hub_lite() as hub:
        before = len(hub.manifest().get("tools", []))
        reg = hub.register_capability(
            product_id,
            capability_id,
            0.007,
            t("labs.lab05.description"),
        )
        trace.emit("register", capability=capability_id, success=reg.get("success"))
        print(f"{t('labs.lab05.registered')}:", reg.get("success"))
        print(f"  {product_id}/{capability_id}  ${reg.get('capability', {}).get('price_per_call_usd')}")

        manifest = hub.manifest()
        man_errors = validate_manifest(manifest)
        after = len(manifest.get("tools", []))
        trace.emit("manifest", tools=after, valid=not man_errors)
        print(f"\n{t('labs.lab05.manifest_tools')}: {before} → {after}")

        matches = hub.discover("sentiment")
        trace.emit("discover", matches=len(matches))
        print(f"{t('ui.discover')}('sentiment'): {len(matches)} {t('ui.matches')}")

        out = hub.invoke(product_id, capability_id, {"text": t("labs.lab05.sample")})
        trace.emit("invoke", price_usd=out.get("price_usd"), success=out.get("success"))
        print(f"\n{t('ui.invoke')} {capability_id}")
        print(f"  {t('ui.price')}    : ${out.get('price_usd')}")
        print(f"  {t('ui.receipt')}  : {(out.get('receipt') or {}).get('nonce', 'n/a')[:8]}…")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
