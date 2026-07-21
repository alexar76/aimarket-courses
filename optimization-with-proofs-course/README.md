<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/optimization-with-proofs-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/optimization-with-proofs-course/notebooks/lab01_colony_tsp.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# Optimization with Proofs

**TSP gaps, transport duals, eikonal certificates, and GP uncertainty — every answer ships a proof.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/optimization-with-proofs-course/](https://alexar76.github.io/aimarket-courses/optimization-with-proofs-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |

## Documentation (step-by-step)

Concepts live in lab docstrings and `i18n/`. For a full hands-on path (setup → M1–M5 → production-oracle bridge):

| Guide | Language |
|-------|----------|
| [docs/step-by-step.md](docs/step-by-step.md) | English |
| [docs/step-by-step.ru.md](docs/step-by-step.ru.md) | Русский |
| [docs/step-by-step.es.md](docs/step-by-step.es.md) | Español |

See [docs/README.md](docs/README.md) for the doc index.

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | TSP with quality gap | [`lab01_colony_tsp`](labs/lab01_colony_tsp.py) |
| M2 | Optimal transport | [`lab02_kantor_transport`](labs/lab02_kantor_transport.py) |
| M3 | Least-time routing | [`lab03_fermat_route`](labs/lab03_fermat_route.py) |
| M4 | Gaussian processes | [`lab04_gauss_gp`](labs/lab04_gauss_gp.py) |
| M5 | Proof portfolio capstone | [`lab05_proof_capstone`](labs/lab05_proof_capstone.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/optimization-with-proofs-course
pip install -e ".[oracles,dev]"
pytest -q
python labs/lab01_colony_tsp.py
python labs/run_exercises.py
```

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/optimization-with-proofs-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).