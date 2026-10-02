"""Live oracle bridge — Platon chaos VRF, Chronos VDF, Sortes ECVRF, Aestus RSW.

Imports real oracle packages when available (monorepo or ``pip install -e .[oracles]``).
Every function returns verifiable artifacts students inspect in labs.
"""

from __future__ import annotations

import hashlib
import secrets
import tempfile
from pathlib import Path
from typing import Any

from courselib.oracle_paths import ensure_oracle, ensure_oracles, monorepo_root


def chaos_draw(client_seed: str = "", *, num_bytes: int = 32) -> dict[str, Any]:
    """Platon chaos-VRF draw with Ed25519 signature (requires numpy + platon)."""
    ensure_oracle("platon", "oracles/oracles/platon/backend")
    import numpy as np
    from platon.randomness import draw_randomness, verify_randomness
    from platon.signing import Signer

    with tempfile.TemporaryDirectory() as td:
        signer = Signer(Path(td) / "platon-course.key")
        state = np.random.default_rng(hash(client_seed) & 0xFFFFFFFF).normal(size=64)
        result = draw_randomness(
            state,
            tick=42,
            timestamp="2026-06-28T12:00:00Z",
            signer=signer,
            num_bytes=num_bytes,
            client_seed=client_seed,
        )
        ok = verify_randomness(result, signer.public_key_b64)
    return {"draw": result, "verified": ok, "oracle": "platon"}


def vdf_eval(seed: str, difficulty: int = 800) -> dict[str, Any]:
    """Chronos Wesolowski VDF — evaluate and attach Wesolowski proof."""
    ensure_oracle("chronos")
    from chronos import vdf

    g = vdf.hash_to_group(seed)
    y = vdf.evaluate(g, difficulty)
    proof = vdf.prove(g, y, difficulty)
    valid = vdf.verify(g, y, difficulty, proof["pi"], proof["l"])
    return {
        "g": g,
        "y": y,
        "difficulty": difficulty,
        "proof": proof,
        "valid": valid,
        "oracle": "chronos",
    }


def ecvrf_draw(alpha: bytes, *, sk_hex: str | None = None) -> dict[str, Any]:
    """Sortes ECVRF — 80-byte proof, offline verify (RFC 9381)."""
    ensure_oracle("sortes")
    from sortes import vrf

    sk = secrets.token_bytes(32)
    pk = vrf.sk_to_pk(sk)
    pi = vrf.prove(sk, alpha)
    beta = vrf.verify(pk, alpha, pi)
    return {
        "alpha": alpha.hex(),
        "public_key": pk.hex(),
        "proof_hex": pi.hex(),
        "proof_len": len(pi),
        "beta_hex": beta.hex(),
        "verified": beta == vrf.verify(pk, alpha, pi),
        "oracle": "sortes",
    }


def timelock_seal(message: str, T: int = 500) -> dict[str, Any]:
    """Aestus RSW time-lock — seal now, open after T sequential squarings."""
    ensure_oracle("aestus")
    from aestus import rsw

    puzzle = rsw.seal(message, T=T)
    opened = rsw.open_puzzle(puzzle)
    plaintext = opened.get("data") or opened.get("plaintext") or opened.get("message") or ""
    return {
        "puzzle": puzzle,
        "opened": opened,
        "message_match": plaintext == message and opened.get("valid", True),
        "oracle": "aestus",
    }


def lottery_word_from_vrf(alpha: str) -> bytes:
    """32-byte lottery word from ECVRF output (lottery/ consumer pattern)."""
    out = ecvrf_draw(alpha.encode())
    return bytes.fromhex(out["beta_hex"])[:32]


class BiasedLottery:
    """Operator can grind seeds — intentionally broken for lab05."""

    def __init__(self, operator_secret: str = "house"):
        self.operator_secret = operator_secret
        self.committed: str | None = None

    def commit(self, player_seed: str) -> str:
        self.committed = player_seed
        return hashlib.sha256(f"commit|{player_seed}".encode()).hexdigest()

    def draw(self, player_seed: str) -> int:
        # Operator picks a seed that wins until they like the outcome.
        for attempt in range(200):
            trial = hashlib.sha256(
                f"{self.operator_secret}|{player_seed}|{attempt}".encode()
            ).hexdigest()
            winner = int(trial[:8], 16) % 100
            if winner < 5:  # house keeps grinding for jackpot
                return winner
        return int(hashlib.sha256(player_seed.encode()).hexdigest()[:8], 16) % 100


class FairLottery:
    """Ungrindable draw — Sortes ECVRF fixes (alpha) → one beta."""

    def commit(self, player_seed: str) -> str:
        return hashlib.sha256(f"fair|{player_seed}".encode()).hexdigest()

    def draw(self, player_seed: str) -> tuple[int, dict[str, Any]]:
        vrf_out = ecvrf_draw(player_seed.encode())
        word = bytes.fromhex(vrf_out["beta_hex"])
        ticket = int.from_bytes(word[:4], "big") % 100
        return ticket, vrf_out


def onchain_vdf_vector() -> dict[str, Any]:
    """Return a VDF output shaped like lottery on-chain verify expects."""
    out = vdf_eval("lottery-round-1", difficulty=600)
    return {
        "scheme": "wesolowski-vdf",
        "seed": "lottery-round-1",
        "difficulty": out["difficulty"],
        "y": str(out["y"]),
        "pi": str(out["proof"]["pi"]),
        "l": out["proof"]["l"],
        "valid": out["valid"],
        "note": "Feed to ChronosVDF.sol verifier on Base testnet (see lottery/docs/)",
    }


def ensure_all_oracles() -> None:
    ensure_oracles("chronos", "sortes", "aestus")
    root = monorepo_root()
    if root and (root / "oracles/oracles/platon/backend").is_dir():
        ensure_oracle("platon", "oracles/oracles/platon/backend")
