"""Optional live probes against modelmarket.dev — skipped unless COURSE_LIVE=1."""

import os

import pytest

from courselib.federation import FederationError, list_peers, live_probe, well_known

pytestmark = pytest.mark.skipif(
    os.environ.get("COURSE_LIVE", "").strip().lower() not in ("1", "true", "yes", "on"),
    reason="Set COURSE_LIVE=1 to hit the public hub",
)


def test_live_well_known():
    wk = well_known()
    assert wk.get("name")
    assert int(wk.get("federated_capabilities_count") or 0) >= 0
    assert wk.get("signer_public_key") or (wk.get("signature") or {}).get("public_key")


def test_live_peers():
    peers = list_peers()
    assert "peers" in peers
    assert "open_federation" in peers
    assert isinstance(peers.get("pending"), list)


def test_live_probe_bundle():
    try:
        probe = live_probe()
    except FederationError as exc:
        pytest.fail(f"live probe failed: {exc}")
    assert probe["live"] is True
    assert probe["signature"]["has_classical"] or probe["signature"]["hybrid"]
    assert len(probe["checklist"]) == 5
