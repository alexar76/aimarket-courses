<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/mathematics-of-trust-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/mathematics-of-trust-course/notebooks/lab01_keystone_nodes.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# Mathematics of Trust

**PageRank, percolation, spectral cuts, consensus, and cascade risk — with live AIMarket oracles.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/mathematics-of-trust-course/](https://alexar76.github.io/aimarket-courses/mathematics-of-trust-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | EigenTrust with LUMEN | [`lab02_trust_pagerank`](labs/lab02_trust_pagerank.py) |
| M2 | Percolation & keystones | [`lab01_keystone_nodes`](labs/lab01_keystone_nodes.py) |
| M3 | Spectral connectivity | [`lab03_spectral_cut`](labs/lab03_spectral_cut.py) |
| M4 | Robust consensus | [`lab04_consensus_aggregate`](labs/lab04_consensus_aggregate.py) |
| M5 | Cascade risk | [`lab05_sandpile_cascade`](labs/lab05_sandpile_cascade.py) |
| M6 | Trust math capstone | [`lab06_trust_audit`](labs/lab06_trust_audit.py) |

## Documentation (step-by-step)

For a full hands-on path (setup → M1–M6 → production-oracle bridge):

| Guide | Language |
| --- | --- |
| [docs/step-by-step.md](docs/step-by-step.md) | English |
| [docs/step-by-step.ru.md](docs/step-by-step.ru.md) | Русский |
| [docs/step-by-step.es.md](docs/step-by-step.es.md) | Español |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/mathematics-of-trust-course
pip install -e ".[oracles,dev]"
pytest -q
python labs/lab01_keystone_nodes.py
python labs/run_exercises.py
```

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/mathematics-of-trust-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).