"""Optimization oracle integration tests."""

from courselib.optimization import (
    gp_posterior,
    proof_portfolio,
    route_least_time,
    solve_transport,
    solve_tsp,
)


def test_tsp_gap_certificate():
    out = solve_tsp()
    assert out["certificate_valid"] is True
    assert out["length"] >= out["lower_bound"]


def test_transport_dual_verified():
    out = solve_transport()
    assert out["verified"] is True
    assert out["cost"] > 0


def test_fermat_route_verified():
    out = route_least_time()
    assert out["verified"] is True
    assert out["path"][0] == "client"


def test_gp_posterior_verified():
    out = gp_posterior()
    assert out["verified"] is True


def test_proof_portfolio_all_verified():
    out = proof_portfolio()
    assert out["all_verified"] is True
