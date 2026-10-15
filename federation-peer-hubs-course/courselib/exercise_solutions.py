"""Reference solutions (CI / instructors)."""

from __future__ import annotations

from courselib.federation import (
    FIXTURE_PEERS,
    FIXTURE_WELL_KNOWN,
    announce_checklist,
    hybrid_signature_info,
    open_vs_closed,
    peer_summary,
    preview_quarantine,
)

MODULES = ("m1", "m2", "m3", "m4", "m5")


def exercise_m1_well_known_fields() -> None:
    """Fixture well-known must expose name, federated count, and hybrid signature."""
    wk = FIXTURE_WELL_KNOWN
    assert wk.get("name")
    assert int(wk.get("federated_capabilities_count") or 0) > 0
    assert wk.get("signer_public_key")
    info = hybrid_signature_info(wk)
    assert info["hybrid"] is True
    assert info["pq_algorithm"] == "ml-dsa-65"


def exercise_m2_open_door_model() -> None:
    """Open-door fixture must report door=open and preview_independent_of_door."""
    model = open_vs_closed(FIXTURE_PEERS)
    assert model["door"] == "open"
    assert model["open_federation"] is True
    assert model["preview_independent_of_door"] is True
    assert model["pending_count"] >= 1
    closed = open_vs_closed({**FIXTURE_PEERS, "open_federation": False})
    assert closed["door"] == "closed"
    assert closed["pending_count"] >= 1  # closed door still keeps pending


def exercise_m3_preview_never_indexed() -> None:
    """Quarantine helper must assert search/invoke never read the preview table."""
    q = preview_quarantine(peers_payload=FIXTURE_PEERS)
    assert q["quarantined"] is True
    assert q["search_reads_preview_table"] is False
    assert q["invoke_reads_preview_table"] is False
    assert q["manifest_reads_preview_table"] is False
    assert q["pending_count"] == 1
    assert q["pending_snapshot"][0]["url"] == "https://stranger.example"


def exercise_m4_declared_vs_observed() -> None:
    """Pending stranger: declared_capabilities > preview_capabilities (honesty gap)."""
    stranger = FIXTURE_PEERS["pending"][0]
    summary = peer_summary(stranger, role="pending")
    assert summary["declared_capabilities"] == 7
    assert summary["observed_capabilities"] == 3
    assert summary["gap"] == 4
    assert summary["observed_source"] == "preview_table"
    trusted = peer_summary(FIXTURE_PEERS["peers"][0], role="trusted")
    assert trusted["observed_source"] == "indexed_catalogue"
    assert trusted["observed_capabilities"] == 11


def exercise_m5_announce_checklist() -> None:
    """Capstone checklist must include announce → preview → approve → crawl."""
    steps = [row["step"] for row in announce_checklist()]
    assert steps == ["announce", "pending", "preview", "approve", "crawl"]
    assert "announce" in steps and "approve" in steps and "crawl" in steps


EXERCISES = {
    "m1": exercise_m1_well_known_fields,
    "m2": exercise_m2_open_door_model,
    "m3": exercise_m3_preview_never_indexed,
    "m4": exercise_m4_declared_vs_observed,
    "m5": exercise_m5_announce_checklist,
}


def run_all() -> dict[str, str]:
    out: dict[str, str] = {}
    for mod, fn in EXERCISES.items():
        try:
            fn()
            out[mod] = "ok"
        except Exception as exc:
            out[mod] = f"fail: {exc}"
    return out


def all_passed(results: dict[str, str] | None = None) -> bool:
    results = results if results is not None else run_all()
    return all(v == "ok" for v in results.values())
