"""Lab 06 — Trust math capstone (Module 6).

Combine percolation, spectral, and PageRank signals into one trust audit
across LUMEN, FOURIER, and PERCOLA — every signal carries its own proof.

Run:  python labs/lab06_trust_audit.py
      COURSE_LANG=ru python labs/lab06_trust_audit.py
Exercise: python labs/run_exercises.py --module m6
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.trust import demo_trust_graph, trust_audit_summary


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m6.title')} ==")
    print(t("modules.m6.concept"))

    graph = demo_trust_graph()
    audit = trust_audit_summary(graph)
    trace.log(
        "audit",
        top=audit["top_trusted"],
        fiedler=round(audit["fiedler_value"], 6),
        f_c=audit["percolation_f_c"],
    )

    verified = bool(audit["spectral_verified"] and audit["percolation_verified"])

    print(f"\n{t('labs.lab06_trust_audit.audit')} ({len(graph.nodes)} nodes)")
    print(f"  {t('labs.lab06_trust_audit.top_trusted')}: "
          f"{audit['top_trusted']} ({audit['top_score']:.4f})")
    print(f"  {t('labs.lab06_trust_audit.fiedler')}: λ₂={audit['fiedler_value']:.6f}"
          f"  ({t('ui.verify')}={audit['spectral_verified']})")
    print(f"  {t('labs.lab06_trust_audit.percolation')}: f_c={audit['percolation_f_c']:.4f}"
          f"  ({t('ui.verify')}={audit['percolation_verified']})")
    print(f"  {t('labs.lab06_trust_audit.keystones')}: {', '.join(audit['keystones'][:6])}")
    print(f"{t('ui.verify')}: {verified}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab06_hint"))


if __name__ == "__main__":
    main()
