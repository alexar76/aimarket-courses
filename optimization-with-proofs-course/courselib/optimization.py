"""Live oracle bridge — COLONY, KANTOR, FERMAT, GAUSS with verifiable certificates."""

from __future__ import annotations

from typing import Any

from courselib.oracle_paths import ensure_oracle, ensure_oracles


def demo_tsp_points() -> list[list[float]]:
    """Pentagon + center — small TSP instance for teaching."""
    import math

    pts: list[list[float]] = []
    for i in range(5):
        ang = 2 * math.pi * i / 5 - math.pi / 2
        pts.append([math.cos(ang), math.sin(ang)])
    pts.append([0.0, 0.0])
    return pts


def solve_tsp(points: list[list[float]] | None = None, *, iterations: int = 500) -> dict[str, Any]:
    ensure_oracle("colony")
    from colony import tsp  # noqa: WPS433

    pts = points or demo_tsp_points()
    out = tsp.solve(pts, iterations=iterations)
    gap_ok = out["gap"] >= 0 and out["length"] >= out["lower_bound"]
    return {
        **out,
        "certificate_valid": gap_ok,
        "oracle": "colony",
    }


def solve_transport(
    a: list[float] | None = None,
    b: list[float] | None = None,
    *,
    points_a: list[list[float]] | None = None,
    points_b: list[list[float]] | None = None,
) -> dict[str, Any]:
    ensure_oracle("kantor")
    from kantor import transport as kt  # noqa: WPS433

    pa = points_a or [[0.0], [1.0], [2.0]]
    pb = points_b or [[0.5], [1.5]]
    weights_a = a or [0.4, 0.3, 0.3]
    weights_b = b or [0.6, 0.4]
    solve_out = kt.transport(
        {
            "a": weights_a,
            "b": weights_b,
            "source_points": pa,
            "sink_points": pb,
            "metric": "euclidean",
            "p": 2,
            "method": "exact",
        }
    )
    verify_out = kt.verify(
        {
            "a": weights_a,
            "b": weights_b,
            "source_points": pa,
            "sink_points": pb,
            "metric": "euclidean",
            "p": 2,
            "claimed_cost": solve_out["cost"],
            "potentials": solve_out["potentials"],
        }
    )
    return {
        "transport": solve_out,
        "cost": solve_out["cost"],
        "wasserstein": solve_out.get("wasserstein"),
        "verified": verify_out["valid"],
        "oracle": "kantor",
    }


def demo_routing_graph() -> tuple[list[Any], list[Any], str, str]:
    """Agent composition graph with cost/latency/reputation blend."""
    nodes = ["client", "router", "tool-a", "tool-b", "sink"]
    edges = [
        {"from": "client", "to": "router", "cost": 1.0, "latency": 10, "reputation": 0.9},
        {"from": "router", "to": "tool-a", "cost": 2.0, "latency": 5, "reputation": 0.95},
        {"from": "router", "to": "tool-b", "cost": 1.5, "latency": 20, "reputation": 0.4},
        {"from": "tool-a", "to": "sink", "cost": 1.0, "latency": 8, "reputation": 0.9},
        {"from": "tool-b", "to": "sink", "cost": 0.5, "latency": 5, "reputation": 0.5},
    ]
    return nodes, edges, "client", "sink"


def route_least_time(
    nodes: list[Any] | None = None,
    edges: list[Any] | None = None,
    start: str | None = None,
    goal: str | None = None,
) -> dict[str, Any]:
    ensure_oracle("fermat")
    from fermat import eikonal  # noqa: WPS433

    n, e, s, g = demo_routing_graph()
    nodes = nodes or n
    edges = edges or e
    start = start or s
    goal = goal or g
    route_out = eikonal.route(nodes, edges, start, goal)
    verify_out = eikonal.verify(
        nodes,
        edges,
        route_out["path"],
        route_out["potentials"],
        start,
        goal,
        total=route_out["total"],
    )
    return {
        "route": route_out,
        "path": route_out["path"],
        "total": route_out["total"],
        "verified": verify_out["valid"],
        "oracle": "fermat",
    }


def gp_posterior(
    X: list[list[float]] | None = None,
    y: list[float] | None = None,
    query: list[list[float]] | None = None,
) -> dict[str, Any]:
    ensure_oracle("gauss")
    from gauss import gp  # noqa: WPS433

    train_x = X or [[0.0], [0.5], [1.0], [1.5]]
    train_y = y or [1.0, 0.5, 0.2, 0.8]
    q = query or [[0.25], [0.75], [1.25]]
    field_out = gp.field({"X": train_x, "y": train_y, "query": q})
    verify_out = gp.verify(
        {
            "X": train_x,
            "y": train_y,
            "query": q,
            "claimed_mean": field_out["mean"],
            "claimed_var": field_out["var"],
            "hyperparams": field_out["hyperparams"],
        }
    )
    suggest_out = gp.suggest(
        {
            "X": train_x,
            "y": train_y,
            "bounds": [[0.0, 2.0]],
            "grid": 32,
            "goal": "min",
        }
    )
    return {
        "field": field_out,
        "mean": field_out["mean"],
        "std": field_out["std"],
        "suggest": suggest_out,
        "verified": verify_out["valid"],
        "oracle": "gauss",
    }


def proof_portfolio() -> dict[str, Any]:
    """Capstone: run all four oracles and collect certificate flags."""
    tsp = solve_tsp()
    transport = solve_transport()
    route = route_least_time()
    gp = gp_posterior()
    flags = {
        "tsp_gap_ok": tsp["certificate_valid"],
        "transport_verified": transport["verified"],
        "route_verified": route["verified"],
        "gp_verified": gp["verified"],
    }
    return {
        "tsp": tsp,
        "transport": transport,
        "route": route,
        "gp": gp,
        "all_verified": all(flags.values()),
        "flags": flags,
    }


def ensure_all_oracles() -> None:
    ensure_oracles("colony", "kantor", "fermat", "gauss")
