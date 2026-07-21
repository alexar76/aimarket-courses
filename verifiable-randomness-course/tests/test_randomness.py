"""Tests for live oracle bridge (monorepo oracles on PYTHONPATH)."""

import pytest

from courselib.randomness import (
    BiasedLottery,
    FairLottery,
    chaos_draw,
    ecvrf_draw,
    onchain_vdf_vector,
    timelock_seal,
    vdf_eval,
)


@pytest.fixture(scope="module", autouse=True)
def _require_oracles():
    from courselib.oracle_paths import ensure_oracles

    ensure_oracles("chronos", "sortes", "aestus")
    try:
        from courselib.oracle_paths import ensure_oracle

        ensure_oracle("platon")
    except ImportError:
        pytest.skip("platon oracle not available")


def test_chaos_draw_verifies():
    out = chaos_draw("test-seed")
    assert out["verified"] is True


def test_vdf_roundtrip():
    out = vdf_eval("pytest", difficulty=500)
    assert out["valid"] is True


def test_ecvrf_80_byte_proof():
    out = ecvrf_draw(b"pytest")
    assert out["proof_len"] == 80
    assert out["verified"] is True


def test_timelock():
    out = timelock_seal("hello", T=150)
    assert out["message_match"] is True


def test_fair_lottery_vrf():
    fair = FairLottery()
    ticket, proof = fair.draw("player-1")
    assert 0 <= ticket < 100
    assert proof["verified"] is True


def test_onchain_vector():
    vec = onchain_vdf_vector()
    assert vec["valid"] is True
