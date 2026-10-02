"""Tests for AI-Factory pipeline client."""

from courselib.factory import (
    PIPELINE_PHASES,
    factory_client,
    probe_factory,
    walk_to_ship,
)


def test_pipeline_phases():
    assert len(PIPELINE_PHASES) == 5


def test_mock_pipeline_status():
    with factory_client(prefer_live=False) as client:
        st = client.get_pipeline_status()
    assert st["products_in_pipeline"] >= 0
    assert st["source"] == "mock"


def test_mock_products():
    with factory_client(prefer_live=False) as client:
        cat = client.list_products()
    assert cat["count"] >= 1
    assert cat["products"][0]["id"]


def test_orchestrator_walk():
    path = walk_to_ship()
    states = [p["state"] for p in path]
    assert "IDEA_RECEIVED" in states
    assert "COMPLETED" in states


def test_probe_factory():
    out = probe_factory()
    assert out["catalog"]["count"] >= 1
