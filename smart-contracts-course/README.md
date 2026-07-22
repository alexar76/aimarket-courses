<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/smart-contracts-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/smart-contracts-course/notebooks/lab01_unbiasable_draw.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# Smart Contracts for Agent Lotteries

**Unbiasable draws, VDF verify, and escrow — lottery/ patterns in Python with Foundry vectors.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/smart-contracts-course/](https://alexar76.github.io/aimarket-courses/smart-contracts-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Unbiasable lottery draw | [`lab01_unbiasable_draw`](labs/lab01_unbiasable_draw.py) |
| M2 | VDF verify on-chain | [`lab02_vdf_verify`](labs/lab02_vdf_verify.py) |
| M3 | Escrow & payment channels | [`lab03_escrow_channel`](labs/lab03_escrow_channel.py) |
| M4 | Relayer round lifecycle | [`lab04_relayer_round`](labs/lab04_relayer_round.py) |
| M5 | Capstone: fair round | [`lab05_lottery_capstone`](labs/lab05_lottery_capstone.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/smart-contracts-course
pip install -e ".[oracles,dev]"
pytest -q
python labs/lab01_unbiasable_draw.py
python labs/run_exercises.py
```

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/smart-contracts-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).