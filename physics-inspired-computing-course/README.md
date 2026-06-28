<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/alexar76/aimarket-courses/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/physics-inspired-computing-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/physics-inspired-computing-course/notebooks/lab01_murmuration_consensus.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# Physics-Inspired Computing for Engineers

**Consensus swarms, TSP certificates, blue-noise sampling, cascade risk, and Landauer thermodynamics.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/physics-inspired-computing-course/](https://alexar76.github.io/aimarket-courses/physics-inspired-computing-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |
| **Step-by-step guide** | [English](docs/step-by-step.md) · [Русский](docs/step-by-step.ru.md) · [Español](docs/step-by-step.es.md) |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Murmuration consensus | [`lab01_murmuration_consensus`](labs/lab01_murmuration_consensus.py) |
| M2 | Colony TSP certificate | [`lab02_colony_tsp`](labs/lab02_colony_tsp.py) |
| M3 | Turing blue-noise | [`lab03_turing_bluenoise`](labs/lab03_turing_bluenoise.py) |
| M4 | Ablation cascade risk | [`lab04_ablation_cascade`](labs/lab04_ablation_cascade.py) |
| M5 | Landauer thermodynamic audit | [`lab05_landauer_audit`](labs/lab05_landauer_audit.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/physics-inspired-computing-course
pip install -e ".[oracles,dev]"
pytest -q
python labs/lab01_murmuration_consensus.py
python labs/run_exercises.py
```

From the **aicom monorepo**, oracles resolve from `oracles/oracles/*` automatically.

## What you build

- **M1** — robust DeGroot + Tukey-biweight consensus (Murmuration)
- **M2** — TSP tour with admissible optimality gap (Colony)
- **M3** — Mitchell blue-noise point sets (Turing)
- **M4** — sandpile cascade τ exponent and tail risk (Ablation)
- **M5** — kT·ln2 bit-erasure energy floor (Landauer)

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/physics-inspired-computing-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).