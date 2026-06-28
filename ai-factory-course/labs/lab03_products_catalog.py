"""Lab 03 — Shipped products catalog (Module 3).

GET /ai-market/products — COMPLETED products from factory.
Run:  python labs/lab03_products_catalog.py
Exercise: python labs/run_exercises.py --module m3
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
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    with factory_client() as client:
        catalog = client.list_products()
    trace.log("products", count=catalog["count"], source=catalog["source"])

    print(f"{t('labs.lab03.count')}: {catalog['count']} ({catalog['source']})")
    for product in catalog["products"][:3]:
        caps = len(product.get("capabilities") or [])
        trace.log("product", id=product["id"], caps=caps)
        print(f"  • {product['id']}: {product.get('name', '')} ({caps} caps)")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
