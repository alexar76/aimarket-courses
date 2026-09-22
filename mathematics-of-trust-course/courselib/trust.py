"""Live oracle bridge — LUMEN, PERCOLA, FOURIER, MURMURATION, ABLATION."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from courselib.oracle_paths import ensure_oracle, ensure_oracles


@dataclass
class TrustGraph:
    """Directed weighted trust edges between node ids."""

    nodes: list[str] = field(default_factory=list)
    edges: list[tuple[str, str, float]] = field(default_factory=list)

    def node_index(self) -> dict[str, int]:
        return {name: i for i, name in enumerate(self.nodes)}

    def to_lumen_edges(self) -> list[list[float]]:
        idx = self.node_index()
        return [[idx[src], idx[dst], w] for src, dst, w in self.edges]

    def to_undirected_edge_list(self) -> list[list[Any]]:
        seen: set[tuple[str, str]] = set()
        out: list[list[Any]] = []
        for src, dst, w in self.edges:
            key = (src, dst) if src <= dst else (dst, src)
            if key in seen:
                continue
            seen.add(key)
            out.append([src, dst, w])
        return out


def demo_trust_graph() -> TrustGraph:
    """Teaching graph: hub trusts official agents; bridge node connects two cliques."""
    return TrustGraph(
        nodes=["hub", "agent-a", "agent-b", "agent-c", "bridge", "agent-d", "agent-e"],
        edges=[
            ("hub", "agent-a", 3.0),
            ("hub", "agent-b", 2.0),
            ("hub", "bridge", 1.5),
            ("agent-a", "hub", 1.0),
            ("agent-b", "hub", 1.0),
            ("agent-a", "agent-b", 0.5),
            ("bridge", "agent-c", 2.0),
            ("bridge", "agent-d", 2.0),
            ("agent-c", "agent-d", 1.0),
            ("agent-d", "agent-e", 1.0),
        ],
    )


def two_cliques_bridge_edges() -> list[list[Any]]:
    """Two K4 cliques joined by a single bridge — PERCOLA teaching graph."""
    a = [[i, j] for i in range(4) for j in range(i + 1, 4)]
    b = [[i, j] for i in range(4, 8) for j in range(i + 1, 8)]
    bridge = [[3, 8], [8, 4]]
    return a + b + bridge


def score_pagerank(graph: TrustGraph) -> dict[str, float]:
    ensure_oracle("lumen")
    from lumen import pagerank  # noqa: WPS433

    if not graph.nodes:
        return {}
    out = pagerank.pagerank(len(graph.nodes), graph.to_lumen_edges())
    return {graph.nodes[i]: out["scores"][i] for i in range(len(graph.nodes))}


def analyze_percolation(edges: list[list[Any]], *, samples: int = 9) -> dict[str, Any]:
    ensure_oracle("percola")
    from percola import percolation as pc  # noqa: WPS433

    out = pc.analyze(None, edges, samples=samples, attack="targeted")
    targeted = out["targeted"]
    verified = pc.verify(None, edges, attack="targeted", f_c=targeted["f_c"], samples=samples)
    return {
        "analysis": out,
        "verified": verified["valid"],
        "f_c": targeted["f_c"],
        "keystones": targeted["keystones"],
        "robustness": out["robustness"],
        "oracle": "percola",
    }


def analyze_spectral(graph: TrustGraph) -> dict[str, Any]:
    ensure_oracle("fourier")
    from fourier import spectral  # noqa: WPS433

    edges = graph.to_undirected_edge_list()
    out = spectral.analyze(graph.nodes, edges)
    cert = spectral.verify(
        graph.nodes,
        edges,
        out["fiedler_value"],
        out["fiedler_vector"],
    )
    return {
        "spectrum": out,
        "fiedler_value": out["fiedler_value"],
        "spectral_cut": out["spectral_cut"],
        "verified": cert["valid"],
        "oracle": "fourier",
    }


def aggregate_consensus(values: list[float], *, trim: float = 0.1) -> dict[str, Any]:
    ensure_oracle("murmuration")
    from murmuration import consensus  # noqa: WPS433

    out = consensus.aggregate(values, trim=trim)
    return {**out, "oracle": "murmuration"}


def demo_agent_estimates() -> list[float]:
    """Swarm price estimates with one adversarial outlier."""
    return [100.2, 99.8, 100.5, 100.1, 99.9, 500.0, 100.0, 99.7]


def analyze_cascade(edges: list[list[Any]], *, grains: int = 800, nonce: str = "trust-lab") -> dict[str, Any]:
    ensure_oracle("ablation")
    from ablation import sandpile  # noqa: WPS433

    out = sandpile.cascade(edges, grains=grains, nonce=nonce)
    verified = sandpile.verify(
        edges,
        grains=grains,
        nonce=nonce,
        claimed_tau=out["tau"],
        claimed_topple_total=out["topple_total"],
    )
    return {
        "cascade": out,
        "tau": out["tau"],
        "max_avalanche": out["max_avalanche"],
        "cvar99": out["cvar99"],
        "triggers": out["triggers"],
        "verified": verified["valid"],
        "oracle": "ablation",
    }


def demo_exposure_graph() -> list[list[Any]]:
    """Directed exposure graph for sandpile cascade lab."""
    return [
        ["bank", "broker"],
        ["broker", "fund-a"],
        ["broker", "fund-b"],
        ["fund-a", "counterparty"],
        ["fund-b", "counterparty"],
        ["counterparty", "insurer"],
    ]


def trust_audit_summary(graph: TrustGraph) -> dict[str, Any]:
    """Capstone-style summary combining pagerank, spectral, and percolation signals."""
    ensure_oracles("lumen", "fourier", "percola")
    scores = score_pagerank(graph)
    spectral = analyze_spectral(graph)
    perc = analyze_percolation(graph.to_undirected_edge_list(), samples=min(9, len(graph.nodes)))
    top = max(scores, key=scores.get) if scores else None
    return {
        "top_trusted": top,
        "top_score": scores.get(top, 0.0) if top else 0.0,
        "fiedler_value": spectral["fiedler_value"],
        "spectral_verified": spectral["verified"],
        "percolation_f_c": perc["f_c"],
        "keystones": perc["keystones"],
        "percolation_verified": perc["verified"],
    }


def ensure_all_oracles() -> None:
    ensure_oracles("lumen", "murmuration", "fourier", "percola", "ablation")
