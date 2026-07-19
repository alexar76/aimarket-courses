"""Trust oracle integration tests."""

import pytest

from courselib.trust import (
    aggregate_consensus,
    analyze_cascade,
    analyze_percolation,
    analyze_spectral,
    demo_agent_estimates,
    demo_exposure_graph,
    demo_trust_graph,
    score_pagerank,
    two_cliques_bridge_edges,
)


def test_pagerank_sums_to_one():
    scores = score_pagerank(demo_trust_graph())
    assert abs(sum(scores.values()) - 1.0) < 1e-6


def test_hub_high_score():
    scores = score_pagerank(demo_trust_graph())
    assert scores["hub"] > scores["agent-e"]


def test_percolation_keystones():
    out = analyze_percolation(two_cliques_bridge_edges(), samples=9)
    assert out["verified"] is True
    assert set(out["keystones"]) & {"3", "4", "8"}


def test_spectral_fiedler_nonnegative():
    out = analyze_spectral(demo_trust_graph())
    assert out["fiedler_value"] >= 0
    assert out["verified"] is True


def test_consensus_robust_to_outlier():
    out = aggregate_consensus(demo_agent_estimates())
    assert out["median"] < 150
    assert out["biweight"] < 150


def test_cascade_verified():
    out = analyze_cascade(demo_exposure_graph(), grains=300, nonce="test")
    assert out["verified"] is True
