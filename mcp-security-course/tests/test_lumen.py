"""LUMEN trust graph scoring tests."""

import pytest

from courselib.lumen import TrustGraph, demo_mcp_trust_graph, score_servers


def test_scores_sum_to_one():
    scores = score_servers(demo_mcp_trust_graph())
    assert abs(sum(scores.values()) - 1.0) < 1e-6


def test_hub_beats_typosquat():
    scores = score_servers(demo_mcp_trust_graph())
    assert scores["hub"] > scores["offical-mcp-drainer"]


def test_isolated_node_low_score():
    graph = TrustGraph(
        nodes=["a", "b", "lonely"],
        edges=[("a", "b", 1.0), ("b", "a", 1.0)],
    )
    scores = score_servers(graph)
    assert scores["lonely"] < scores["a"]


def test_empty_graph():
    assert score_servers(TrustGraph()) == {}


def test_unknown_server_zero():
    from courselib.lumen import score_entity

    out = score_entity("missing", demo_mcp_trust_graph())
    assert out["score"] == 0.0
