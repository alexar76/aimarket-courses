"""Tests for lottery smart-contract teaching port."""

from courselib.contracts import (
    BiasedLottery,
    EscrowChannel,
    FairLottery,
    RelayerRound,
    load_chronos_vector,
    simulate_fair_round,
    verify_wesolowski_vector,
)


def test_biased_grindable():
    biased = BiasedLottery()
    assert biased.operator_can_grind("seed-x")


def test_fair_draw_range():
    fair = FairLottery()
    ticket, proof = fair.draw("player-1")
    assert 0 <= ticket < 100
    assert proof["verified"] is True


def test_chronos_vector_valid():
    vec = load_chronos_vector()
    assert vec["valid"] is True
    assert verify_wesolowski_vector(vec)


def test_escrow_receipt_replay_blocked():
    ch = EscrowChannel("ch-1", "alice")
    ch.open(100)
    ch.debit(10, "r1", "hub", signature_valid=True)
    try:
        ch.debit(10, "r1", "hub", signature_valid=True)
        assert False, "expected replay error"
    except ValueError as exc:
        assert "already used" in str(exc).lower()


def test_relayer_round_seed():
    rnd = RelayerRound(1, b"\x01" * 32, b"\x02" * 32)
    assert rnd.chronos_seed().startswith("0x")


def test_capstone_simulation():
    out = simulate_fair_round(onchain_vdf=False)
    assert out["chronos_vector_valid"]
    assert 0 <= out["ticket"] < 100
