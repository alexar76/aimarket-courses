"""Resolve oracle packages from pip install or monorepo sibling paths."""

from __future__ import annotations

import sys
from pathlib import Path

# (import_name, monorepo relative path under oracles/oracles/)
_ORACLE_PACKAGES: tuple[tuple[str, str], ...] = (
    ("chronos", "oracles/oracles/chronos"),
    ("sortes", "oracles/oracles/sortes"),
    ("aestus", "oracles/oracles/aestus"),
    ("lumen", "oracles/oracles/lumen"),
    ("murmuration", "oracles/oracles/murmuration"),
    ("fourier", "oracles/oracles/fourier"),
    ("percola", "oracles/oracles/percola"),
    ("ablation", "oracles/oracles/ablation"),
    ("colony", "oracles/oracles/colony"),
    ("kantor", "oracles/oracles/kantor"),
    ("fermat", "oracles/oracles/fermat"),
    ("gauss", "oracles/oracles/gauss"),
    ("turing", "oracles/oracles/turing"),
    ("landauer", "oracles/oracles/landauer"),
)


def monorepo_root() -> Path | None:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "oracles" / "oracles" / "chronos").is_dir():
            return p
        if (p / "courses" / "orchestration-course").is_dir() and (p / "oracles").is_dir():
            return p
    return None


def ensure_oracle(import_name: str, rel_path: str | None = None) -> None:
    try:
        __import__(import_name)
        return
    except ImportError:
        pass
    root = monorepo_root()
    if root is None:
        raise ImportError(
            f"Oracle package '{import_name}' not installed. "
            f"pip install -e \".[oracles]\" or run from the aicom monorepo."
        )
    rel = rel_path or next((r for n, r in _ORACLE_PACKAGES if n == import_name), "")
    pkg = root / rel
    if not pkg.is_dir():
        raise ImportError(f"Oracle path missing: {pkg}")
    s = str(pkg)
    if s not in sys.path:
        sys.path.insert(0, s)


def ensure_oracles(*names: str) -> None:
    for name in names:
        rel = next((r for n, r in _ORACLE_PACKAGES if n == name), f"oracles/oracles/{name}")
        ensure_oracle(name, rel)
