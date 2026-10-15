<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/pqc-hybrid-signing-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/pqc-hybrid-signing-course/notebooks/lab01_why_hybrid.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# PQC · Hybrid Signing

**Classical Ed25519 + post-quantum — dual orbits, one receipt, offline verify.**

Interactive Python course with runnable labs and full **EN / RU / ES / FR / ZH** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/pqc-hybrid-signing-course/](https://alexar76.github.io/aimarket-courses/pqc-hybrid-signing-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` · `fr` · `zh` |
| **Live hub** | [`modelmarket.dev/.well-known/ai-market.json`](https://modelmarket.dev/.well-known/ai-market.json) already carries hybrid `pq_*` fields |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Why hybrid | [`lab01_why_hybrid`](labs/lab01_why_hybrid.py) |
| M2 | Key material & identity | [`lab02_key_identity`](labs/lab02_key_identity.py) |
| M3 | Sign a receipt | [`lab03_sign_receipt`](labs/lab03_sign_receipt.py) |
| M4 | Verify offline | [`lab04_verify_offline`](labs/lab04_verify_offline.py) |
| M5 | Capstone: hybrid gate | [`lab05_hybrid_gate_capstone`](labs/lab05_hybrid_gate_capstone.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/pqc-hybrid-signing-course
pip install -e ".[pqc,dev]"
python labs/lab01_why_hybrid.py
python labs/run_exercises.py
```

Without `dilithium-py`, labs still **verify classical Ed25519** and can **inspect** a LIVE hybrid envelope (`PQC_COURSE_FETCH_LIVE=1`). They never invent fake PQ success — PQ sign is labeled skipped.

## Honesty rules

- LIVE hub crypto is LIVE. Do not present SIM / stub signatures as live.
- `require_pq` / `refuse_single_orbit` is phase 3 — without it, hybrid is migration ability, not PQ security.
- Pin both public keys out-of-band.

## Docs

Step-by-step guides: [`docs/`](docs/) (EN / RU / ES / FR / ZH).

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/pqc-hybrid-signing-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).