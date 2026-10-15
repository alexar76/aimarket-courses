<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/gaia-atlas-sensors-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/gaia-atlas-sensors-course/notebooks/lab01_live_vs_sim.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# GAIA · ATLAS · Physical World Sensors

**Attested IoT pins, LIVE vs SIM honesty, and operator map reads — physical world as capability.**

Interactive Python course with runnable labs and full **EN / RU / ES / FR / ZH** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/gaia-atlas-sensors-course/](https://alexar76.github.io/aimarket-courses/gaia-atlas-sensors-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` · `fr` · `zh` |
| **Live sandbox** | [GAIA](https://iot.modelmarket.dev) · [ATLAS](https://atlas.modelmarket.dev) |
| **Guide** | [docs/step-by-step.md](docs/step-by-step.md) (+ [ru](docs/step-by-step.ru.md) · [es](docs/step-by-step.es.md) · [fr](docs/step-by-step.fr.md) · [zh](docs/step-by-step.zh.md)) |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | What a LIVE relay is | [`lab01_live_vs_sim`](labs/lab01_live_vs_sim.py) |
| M2 | Licence & commercial rail | [`lab02_licence_gate`](labs/lab02_licence_gate.py) |
| M3 | Fleet & pin honesty | [`lab03_honesty_claims`](labs/lab03_honesty_claims.py) |
| M4 | ATLAS operator map | [`lab04_atlas_map_read`](labs/lab04_atlas_map_read.py) |
| M5 | Capstone: add a sensor | [`lab05_add_sensor_capstone`](labs/lab05_add_sensor_capstone.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
python labs/lab01_live_vs_sim.py
python labs/run_exercises.py
```

Labs call live GAIA/ATLAS when reachable; offline they print `[offline]` and never invent readings.

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/gaia-atlas-sensors-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).