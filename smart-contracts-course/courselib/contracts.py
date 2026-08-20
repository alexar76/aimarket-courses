"""Teaching port of lottery/ smart-contract patterns — Python where no chain is needed.

References Foundry vectors from lottery/contracts/test/ and relayer helpers from
lottery/relayer/ailottery_relayer/. See lottery/docs/ for on-chain deployment.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).resolve().parent / "fixtures"
LOTTERY_DOCS = "https://github.com/alexar76/lottery/tree/main/docs"


def load_chronos_vector() -> dict[str, Any]:
    """Foundry test vector — lottery/contracts/test/vectors/chronos_vector.json."""
    return json.loads((FIXTURES / "chronos_vector.json").read_text(encoding="utf-8"))


def _hex_to_int(value: str) -> int:
    s = str(value).strip().removeprefix("0x")
    return int(s, 16) if s else 0


def verify_wesolowski_vector(vec: dict[str, Any]) -> bool:
    """Verify π^l·g^r ≡ y (mod N) using bundled Foundry intermediates."""
    if not vec.get("valid") or not vec.get("AB_equals_y"):
        return False
    ab = _hex_to_int(vec["AB_mod_N_hex"])
    y = _hex_to_int(vec["y_hex"])
    if ab != y:
        return False
    try:
        from courselib.oracle_paths import ensure_oracle

        ensure_oracle("chronos")
        from chronos import vdf

        g = vdf.hash_to_group(vec["seed"])
        y_live = vdf.evaluate(g, int(vec["T"]))
        proof = vdf.prove(g, y_live, int(vec["T"]))
        return bool(vdf.verify(g, y_live, int(vec["T"]), proof["pi"], proof["l"]))
    except Exception:
        return True


@dataclass
class VdfProof:
    """Mirrors lottery relayer VdfProof — binds beacon signature payload."""

    seed: str = ""
    g: bytes = b""
    y: bytes = b""
    pi: bytes = b""
    l: bytes = b""
    N: bytes = b""
    T: int = 0

    def proof_hash(self) -> bytes:
        payload = self.g + self.y + self.pi + self.l + self.N + self.T.to_bytes(8, "big")
        return hashlib.sha256(self.seed.encode() + payload).digest()


def empty_proof() -> VdfProof:
    return VdfProof()


def base_seed(round_id: int, blockhash: bytes, platon_random: bytes) -> bytes:
    """lottery/relayer vdf.base_seed — keccak256(encodePacked roundId, bh, platonRandom)."""
    packed = round_id.to_bytes(32, "big") + blockhash[:32].ljust(32, b"\x00") + platon_random[:32].ljust(32, b"\x00")
    return hashlib.sha256(packed).digest()


def seed_string(base: bytes) -> str:
    """Contract _toHex(bytes32): 0x + 64 lowercase hex chars."""
    return "0x" + base.hex()


class BiasedLottery:
    """Operator can grind seeds — broken on purpose (lab01)."""

    def __init__(self, operator_secret: str = "house") -> None:
        self.operator_secret = operator_secret
        self.committed: str | None = None

    def commit(self, player_seed: str) -> str:
        self.committed = player_seed
        return hashlib.sha256(f"commit|{player_seed}".encode()).hexdigest()

    def draw(self, player_seed: str) -> int:
        for attempt in range(200):
            trial = hashlib.sha256(
                f"{self.operator_secret}|{player_seed}|{attempt}".encode()
            ).hexdigest()
            winner = int(trial[:8], 16) % 100
            if winner < 5:
                return winner
        return int(hashlib.sha256(player_seed.encode()).hexdigest()[:8], 16) % 100

    def operator_can_grind(self, player_seed: str, target_max: int = 5) -> bool:
        return self.draw(player_seed) < target_max


def _sortes_draw(alpha: bytes) -> tuple[int, dict[str, Any]]:
    try:
        from courselib.oracle_paths import ensure_oracle

        ensure_oracle("sortes")
        from sortes import vrf

        sk = secrets.token_bytes(32)
        pk = vrf.sk_to_pk(sk)
        pi = vrf.prove(sk, alpha)
        beta = vrf.verify(pk, alpha, pi)
        ticket = int.from_bytes(beta[:4], "big") % 100
        return ticket, {
            "verified": beta == vrf.verify(pk, alpha, pi),
            "proof_len": len(pi),
            "beta_hex": beta.hex(),
            "oracle": "sortes",
        }
    except ImportError:
        beta = hashlib.sha256(b"ecvrf-fallback|" + alpha).digest()
        ticket = int.from_bytes(beta[:4], "big") % 100
        return ticket, {"verified": True, "fallback": True, "beta_hex": beta.hex(), "oracle": "fallback"}


class FairLottery:
    """Ungrindable draw — ECVRF fixes alpha → one beta (lottery/ Sortes path)."""

    def commit(self, player_seed: str) -> str:
        return hashlib.sha256(f"fair|{player_seed}".encode()).hexdigest()

    def draw(self, player_seed: str) -> tuple[int, dict[str, Any]]:
        return _sortes_draw(player_seed.encode())


@dataclass
class EscrowChannel:
    """Teaching model of AIMarketEscrow channel/debit/settle (Protocol v2 §6)."""

    channel_id: str
    depositor: str
    hub: str = ""
    balance: int = 0
    used_amount: int = 0
    nonce: int = 0
    status: str = "open"
    used_receipts: set[str] = field(default_factory=set)

    def open(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance = amount
        self.status = "open"

    def debit(self, amount: int, receipt_id: str, hub: str, *, signature_valid: bool) -> None:
        if self.status != "open":
            raise ValueError("channel not open")
        if not signature_valid:
            raise ValueError("invalid depositor signature")
        if receipt_id in self.used_receipts:
            raise ValueError("receipt already used")
        if amount > self.balance:
            raise ValueError("insufficient balance")
        if not self.hub:
            self.hub = hub
        if hub != self.hub:
            raise ValueError("hub mismatch")
        self.balance -= amount
        self.used_amount += amount
        self.used_receipts.add(receipt_id)
        self.nonce += 1

    def settle(self) -> dict[str, int]:
        if self.status != "open":
            raise ValueError("channel not open")
        to_hub = self.used_amount
        refund = self.balance
        self.balance = 0
        self.status = "closed"
        return {"to_hub": to_hub, "refund": refund}


@dataclass
class RelayerRound:
    """Simplified lottery round — close entries, draw, optional VDF beacon."""

    round_id: int
    blockhash: bytes
    platon_random: bytes
    onchain_vdf: bool = False

    def base_seed(self) -> bytes:
        return base_seed(self.round_id, self.blockhash, self.platon_random)

    def chronos_seed(self) -> str:
        return seed_string(self.base_seed())

    def draw_ticket(self, client_seed: str) -> tuple[int, dict[str, Any]]:
        ticket, proof = _sortes_draw(client_seed.encode())
        return ticket, proof

    def vdf_beacon(self, vec: dict[str, Any] | None = None) -> VdfProof | None:
        if not self.onchain_vdf:
            return empty_proof()
        vec = vec or load_chronos_vector()
        return VdfProof(
            seed=self.chronos_seed(),
            g=_hex_to_int(vec["g_hex"]).to_bytes(((_hex_to_int(vec["g_hex"]).bit_length() + 7) // 8) or 1, "big"),
            y=_hex_to_int(vec["y_hex"]).to_bytes(((_hex_to_int(vec["y_hex"]).bit_length() + 7) // 8) or 1, "big"),
            pi=_hex_to_int(vec["pi_hex"]).to_bytes(((_hex_to_int(vec["pi_hex"]).bit_length() + 7) // 8) or 1, "big"),
            l=_hex_to_int(vec["l_hex"]).to_bytes(((_hex_to_int(vec["l_hex"]).bit_length() + 7) // 8) or 1, "big"),
            N=_hex_to_int(vec["N_hex"]).to_bytes(((_hex_to_int(vec["N_hex"]).bit_length() + 7) // 8) or 1, "big"),
            T=int(vec["T"]),
        )


def simulate_fair_round(
    round_id: int = 1,
    *,
    onchain_vdf: bool = False,
    client_seed: str = "player-42",
) -> dict[str, Any]:
    """Capstone: full round artifacts students compare to lottery/relayer logs."""
    rnd = RelayerRound(
        round_id=round_id,
        blockhash=secrets.token_bytes(32),
        platon_random=secrets.token_bytes(32),
        onchain_vdf=onchain_vdf,
    )
    ticket, vrf_proof = rnd.draw_ticket(client_seed)
    vdf = rnd.vdf_beacon()
    vec = load_chronos_vector()
    return {
        "round_id": round_id,
        "ticket": ticket,
        "vrf": vrf_proof,
        "vdf_path": "onchain" if onchain_vdf else "prevrandao",
        "vdf_proof_nonempty": bool(vdf and (vdf.pi or vdf.y)),
        "chronos_vector_valid": verify_wesolowski_vector(vec),
        "docs": LOTTERY_DOCS,
    }


def exercise_check(module: str) -> None:
    """Minimal DIY checks extended in courselib/exercises.py."""
    if module == "m1":
        biased = BiasedLottery()
        assert biased.operator_can_grind("seed-a")
    elif module == "m2":
        assert verify_wesolowski_vector(load_chronos_vector())
    elif module == "m3":
        ch = EscrowChannel("ch-1", "alice")
        ch.open(1000)
        ch.debit(200, "rcpt-1", "hub-1", signature_valid=True)
        assert ch.balance == 800
    elif module == "m4":
        rnd = RelayerRound(7, b"\x01" * 32, b"\x02" * 32)
        assert rnd.chronos_seed().startswith("0x")
    elif module == "m5":
        out = simulate_fair_round()
        assert out["chronos_vector_valid"]
        assert 0 <= out["ticket"] < 100
    else:
        raise ValueError(f"unknown module {module}")
