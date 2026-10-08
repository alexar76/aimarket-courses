"""Offline unit tests for federation helpers."""

from courselib.federation import (
    FIXTURE_PEERS,
    FIXTURE_WELL_KNOWN,
    announce_checklist,
    fixture_probe,
    hybrid_signature_info,
    open_vs_closed,
    peer_summary,
    preview_quarantine,
)


def test_hybrid_signature_info_fixture():
    info = hybrid_signature_info(FIXTURE_WELL_KNOWN)
    assert info["hybrid"] is True
    assert info["pq_algorithm"] == "ml-dsa-65"
    assert info["has_classical"] is True


def test_open_vs_closed_independent_preview():
    open_m = open_vs_closed(FIXTURE_PEERS)
    assert open_m["door"] == "open"
    assert open_m["preview_independent_of_door"] is True
    closed = open_vs_closed({**FIXTURE_PEERS, "open_federation": False})
    assert closed["door"] == "closed"
    assert closed["pending_count"] == open_m["pending_count"]


def test_preview_quarantine_never_indexed():
    q = preview_quarantine(peers_payload=FIXTURE_PEERS)
    assert q["quarantined"] is True
    assert q["search_reads_preview_table"] is False
    assert q["invoke_reads_preview_table"] is False
    assert q["pending_count"] == 1


def test_peer_summary_honesty_gap():
    s = peer_summary(FIXTURE_PEERS["pending"][0], role="pending")
    assert s["declared_capabilities"] == 7
    assert s["observed_capabilities"] == 3
    assert s["gap"] == 4
    t = peer_summary(FIXTURE_PEERS["peers"][0], role="trusted")
    assert t["observed_source"] == "indexed_catalogue"


def test_announce_checklist_order():
    steps = [r["step"] for r in announce_checklist()]
    assert steps == ["announce", "pending", "preview", "approve", "crawl"]


def test_fixture_probe_not_live():
    probe = fixture_probe()
    assert probe["live"] is False
    assert probe["hub"].startswith("fixture://")
    assert len(probe["checklist"]) == 5
