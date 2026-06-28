<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/alexar76/aimarket-courses/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/verifiable-randomness-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/verifiable-randomness-course/notebooks/lab01_platon_chaos.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# Verifiable Randomness & Cryptographic Time

**Build and break biased lotteries — then verify proofs offline from 80 bytes.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/verifiable-randomness-course/](https://alexar76.github.io/aimarket-courses/verifiable-randomness-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Chaos VRF with Platon | [`lab01_platon_chaos`](labs/lab01_platon_chaos.py) |
| M2 | VDF time with Chronos | [`lab02_chronos_vdf`](labs/lab02_chronos_vdf.py) |
| M3 | ECVRF & Sortes | [`lab03_sortes_ecvrf`](labs/lab03_sortes_ecvrf.py) |
| M4 | Time-lock RSW with Aestus | [`lab04_aestus_timelock`](labs/lab04_aestus_timelock.py) |
| M5 | Commit–reveal & bias attacks | [`lab05_commit_reveal`](labs/lab05_commit_reveal.py) |
| M6 | On-chain verification | [`lab06_onchain_consumer`](labs/lab06_onchain_consumer.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/verifiable-randomness-course
pip install -e ".[oracles,dev]"
pytest -q
python labs/lab01_platon_chaos.py
python labs/run_exercises.py
```

## Documentation (step-by-step)

| Guide | Language |
| --- | --- |
| [docs/step-by-step.md](docs/step-by-step.md) | English |
| [docs/step-by-step.ru.md](docs/step-by-step.ru.md) | Русский |
| [docs/step-by-step.es.md](docs/step-by-step.es.md) | Español |

See [docs/README.md](docs/README.md) for the doc index.

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/verifiable-randomness-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).