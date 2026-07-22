"""Hands-on exercises — DIY checks for each module."""

from __future__ import annotations

from courselib.trust import (
    aggregate_consensus,
    analyze_cascade,
    analyze_percolation,
    analyze_spectral,
    demo_agent_estimates,
    demo_exposure_graph,
    demo_trust_graph,
    score_pagerank,
    trust_audit_summary,
    two_cliques_bridge_edges,
)

MODULES = ("m1", "m2", "m3", "m4", "m5", "m6")


def exercise_m1_pagerank_sums_to_one() -> None:
    scores = score_pagerank(demo_trust_graph())
    assert abs(sum(scores.values()) - 1.0) < 1e-6


def exercise_m2_keystone_detected() -> None:
    out = analyze_percolation(two_cliques_bridge_edges(), samples=9)
    assert out["verified"] is True
    assert out["f_c"] <= 2.0 / 9
    assert set(out["keystones"]) & {"3", "4", "8"}


def exercise_m3_spectral_certificate() -> None:
    out = analyze_spectral(demo_trust_graph())
    assert out["fiedler_value"] >= 0
    assert out["verified"] is True


def exercise_m4_consensus_robust() -> None:
    out = aggregate_consensus(demo_agent_estimates())
    assert out["median"] < 150
    assert out["biweight"] < 150
    assert out["median"] < out["trimmed_mean"] or abs(out["median"] - out["trimmed_mean"]) < 50


def exercise_m5_cascade_verified() -> None:
    out = analyze_cascade(demo_exposure_graph(), grains=400, nonce="exercise")
    assert out["verified"] is True
    assert out["max_avalanche"] >= 0


def exercise_m6_trust_audit() -> None:
    audit = trust_audit_summary(demo_trust_graph())
    # Capstone: every signal in the combined audit carries its own proof.
    assert audit["spectral_verified"] is True
    assert audit["percolation_verified"] is True
    # PageRank surfaces the hub as the most-trusted node.
    assert audit["top_trusted"] == "hub"
    assert audit["top_score"] > 0
    # Spectral and percolation thresholds are well-formed.
    assert audit["fiedler_value"] >= 0
    assert 0.0 < audit["percolation_f_c"] <= 1.0
    assert audit["keystones"]


EXERCISES = {
    "m1": exercise_m1_pagerank_sums_to_one,
    "m2": exercise_m2_keystone_detected,
    "m3": exercise_m3_spectral_certificate,
    "m4": exercise_m4_consensus_robust,
    "m5": exercise_m5_cascade_verified,
    "m6": exercise_m6_trust_audit,
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
