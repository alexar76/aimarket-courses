"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

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
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_well_known_fields: implement this exercise")


def exercise_m2_open_door_model() -> None:
    """Open-door fixture must report door=open and preview_independent_of_door."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_open_door_model: implement this exercise")


def exercise_m3_preview_never_indexed() -> None:
    """Quarantine helper must assert search/invoke never read the preview table."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_preview_never_indexed: implement this exercise")


def exercise_m4_declared_vs_observed() -> None:
    """Pending stranger: declared_capabilities > preview_capabilities (honesty gap)."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_declared_vs_observed: implement this exercise")


def exercise_m5_announce_checklist() -> None:
    """Capstone checklist must include announce → preview → approve → crawl."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_announce_checklist: implement this exercise")


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
