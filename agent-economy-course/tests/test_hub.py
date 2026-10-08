"""Tests for hub-lite (M2–M5 fast path)."""

import pytest

pytest.importorskip("fastapi")

from courselib.hub_lite import embedded_hub_lite


def test_hub_lite_discover_invoke_verify():
    with embedded_hub_lite() as hub:
        wk = hub.well_known()
        assert wk.get("name") == "course-hub-lite"
        matches = hub.discover("translate")
        assert matches
        out = hub.invoke("prod-translate", "translate.multi@v2", {"text": "hi"})
        assert out["success"] is True
        assert hub.verify_receipt(out["receipt"])


def test_hub_lite_channel_open_close():
    with embedded_hub_lite() as hub:
        opened = hub.open_channel(budget_usd=0.5)
        assert opened["success"] is True
        closed = hub.close_channel(opened["channel_id"])
        assert closed["success"] is True


def test_hub_lite_register_capability():
    with embedded_hub_lite() as hub:
        reg = hub.register_capability("prod-x", "demo@v1", 0.01, "demo")
        assert reg["success"] is True
        assert hub.discover("demo")
