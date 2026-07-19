"""End-to-end test of the embedded sandbox economy via the real SDK.

Boots a local AIMarket Hub + stub Factory and drives the genuine
``aimarket-agent`` client against them. No network, no money.
"""

import pytest

from courselib.economy import embedded_sandbox


@pytest.fixture(scope="module")
def econ():
    with embedded_sandbox(budget=3.0) as e:
        yield e


def test_well_known_is_served(econ):
    wk = econ.well_known()
    assert "name" in wk


def test_discover_finds_capabilities(econ):
    matches = econ.discover("translate")
    assert isinstance(matches, list) and len(matches) >= 1
    assert any("translate" in (m.get("capability_id", "") + m.get("product_id", "")) for m in matches)


def test_invoke_single_returns_signed_receipt(econ):
    out = econ.invoke("prod-translate", "translate.multi@v2", {"text": "hello world"})
    assert out.get("success") is True
    assert "receipt" in out
    assert out["result"]["output"]["served_by"] == "course-sandbox-factory"


def test_full_autonomous_cycle_through_real_sdk(econ):
    res = econ.hire("translate text to multiple languages")
    assert res["ok"] is True, res
    bom = res["bill_of_materials"]
    assert bom["all_ok"] is True
    assert bom["protocol_version"] == "v2"
    assert res["total_spent_usd"] >= 0


def test_capital_listings_does_not_500(econ):
    # Regression guard for the lab08 crash: capital_listings() used to 500
    # because the ACEX ledger resolved its SQLite path to the Docker-only
    # /app/data. embedded_sandbox now points AIFACTORY_DATA_ROOT at the temp
    # dir; the hub must serve real capital state (no defensive 'error' fallback).
    cap = econ.capital_listings()
    assert isinstance(cap.get("listings"), list), cap
    assert "error" not in cap, cap
