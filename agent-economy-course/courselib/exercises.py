"""Hands-on exercises — DIY checks for each module (M1–M6).

Run all:  python labs/run_exercises.py
Or pytest: pytest tests/test_exercises.py -q
"""

from __future__ import annotations

from courselib.hub_lite import embedded_hub_lite
from courselib.protocol import is_valid_manifest, is_valid_well_known, validate_well_known
from courselib.trust import TrustGraph, sign_receipt, tamper_receipt, verify_receipt

MODULES = ("m1", "m2", "m3", "m4", "m5", "m6")


def exercise_m1_validate_well_known() -> None:
    """Parse and validate a Protocol v2 well-known document."""
    with embedded_hub_lite() as hub:
        wk = hub.well_known()
        assert is_valid_well_known(wk), validate_well_known(wk)
        manifest = hub.manifest()
        assert is_valid_manifest(manifest)


def exercise_m2_discover_capability() -> None:
    """Discover a translate capability on hub-lite."""
    with embedded_hub_lite() as hub:
        matches = hub.discover("translate")
        assert matches
        assert any("translate" in m["capability_id"] for m in matches)


def exercise_m3_open_close_channel() -> None:
    """Open a payment channel, then close it with a refund."""
    with embedded_hub_lite() as hub:
        opened = hub.open_channel(budget_usd=0.5)
        assert opened.get("success") is True
        channel_id = opened["channel_id"]
        closed = hub.close_channel(channel_id)
        assert closed.get("success") is True
        assert closed.get("refund_usd", 0) >= 0


def exercise_m4_verify_receipt_and_trust() -> None:
    """Verify a signed receipt and feed the trust graph."""
    secret = "exercise-secret"
    receipt = sign_receipt({"product_id": "prod-demo", "price_usd": 0.02}, secret)
    assert verify_receipt(receipt, secret)
    bad = tamper_receipt(receipt, price_usd=0.0)
    assert not verify_receipt(bad, secret)

    graph = TrustGraph()
    good = graph.record("prod-demo", 0.02, verified=True)
    assert good > 0.5
    bad = graph.record("prod-demo", 0.02, verified=False)
    assert bad < good


def exercise_m5_publish_capability() -> None:
    """Register a metered capability and discover it."""
    with embedded_hub_lite() as hub:
        reg = hub.register_capability(
            "prod-custom",
            "echo.metered@v1",
            0.003,
            "Echo input for a fee (exercise)",
        )
        assert reg.get("success") is True
        matches = hub.discover("echo.metered")
        assert any(m["capability_id"] == "echo.metered@v1" for m in matches)


def exercise_m6_paid_invoke_flow() -> None:
    """Invoke a paid capability and verify the receipt."""
    with embedded_hub_lite() as hub:
        out = hub.invoke("prod-translate", "translate.multi@v2", {"text": "paid invoke"})
        assert out.get("success") is True
        assert out.get("price_usd", 0) > 0
        assert hub.verify_receipt(out.get("receipt") or {})


EXERCISES: dict[str, callable] = {
    "m1": exercise_m1_validate_well_known,
    "m2": exercise_m2_discover_capability,
    "m3": exercise_m3_open_close_channel,
    "m4": exercise_m4_verify_receipt_and_trust,
    "m5": exercise_m5_publish_capability,
    "m6": exercise_m6_paid_invoke_flow,
}


def run_all() -> dict[str, str]:
    results: dict[str, str] = {}
    for mod, fn in EXERCISES.items():
        try:
            fn()
            results[mod] = "ok"
        except Exception as e:
            results[mod] = f"fail: {e}"
    return results


def all_passed(results: dict[str, str] | None = None) -> bool:
    results = results or run_all()
    return all(v == "ok" for v in results.values())
