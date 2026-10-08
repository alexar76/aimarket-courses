"""courselib — teaching toolkit for PQC · Hybrid Signing."""

from courselib.i18n import available_languages, get_translator, resolve_lang
from courselib.pqc import (
    HybridSigner,
    HybridVerifier,
    envelope_is_hybrid,
    fetch_live_hybrid_envelope,
    pqc_available,
    refuse_single_orbit,
)

__all__ = [
    "available_languages",
    "get_translator",
    "resolve_lang",
    "HybridSigner",
    "HybridVerifier",
    "envelope_is_hybrid",
    "fetch_live_hybrid_envelope",
    "pqc_available",
    "refuse_single_orbit",
]
__version__ = "0.2.0"
