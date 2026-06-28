"""Hands-on exercises for each module."""

from __future__ import annotations

from courselib.factory import (
    PIPELINE_PHASES,
    factory_client,
    pipeline_flow_document,
    probe_factory,
    walk_to_ship,
)

MODULES = ["m1", "m2", "m3", "m4", "m5"]


def exercise_m1_phases() -> None:
    assert [p[0] for p in PIPELINE_PHASES] == [
        "research",
        "design",
        "build",
        "test",
        "ship",
    ]


def exercise_m2_pipeline_status() -> None:
    with factory_client(prefer_live=False) as client:
        st = client.get_pipeline_status()
    assert st["products_in_pipeline"] >= 0
    assert st["products_shipped"] >= 0


def exercise_m3_products() -> None:
    with factory_client(prefer_live=False) as client:
        cat = client.list_products()
    assert cat["count"] == len(cat["products"])
    assert cat["products"][0]["id"]


def exercise_m4_orchestrator_path() -> None:
    doc = pipeline_flow_document()
    assert isinstance(doc.get("agent_flow"), dict)
    path = walk_to_ship()
    assert path[0]["state"] == "IDEA_RECEIVED"
    assert any(p["state"] == "COMPLETED" for p in path)


def exercise_m5_factory_probe() -> None:
    out = probe_factory()
    assert out["catalog"]["count"] >= 1
    assert out["status"]["source"] in {"live", "mock"}


EXERCISES = {
    "m1": exercise_m1_phases,
    "m2": exercise_m2_pipeline_status,
    "m3": exercise_m3_products,
    "m4": exercise_m4_orchestrator_path,
    "m5": exercise_m5_factory_probe,
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


def all_passed() -> bool:
    return all(v == "ok" for v in run_all().values())
