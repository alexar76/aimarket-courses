<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/3d-data-viz-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/3d-data-viz-course/notebooks/lab01_health_probe.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# 3D Data Visualization with Alien Monitor

**Probe alien-monitor API health, topology, and LUMEN reputation — then map oracle scenes to R3F.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/3d-data-viz-course/](https://alexar76.github.io/aimarket-courses/3d-data-viz-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |
| **Step-by-step guide** | [English](docs/step-by-step.md) · [Русский](docs/step-by-step.ru.md) · [Español](docs/step-by-step.es.md) |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Monitor health & modes | [`lab01_health_probe`](labs/lab01_health_probe.py) |
| M2 | Topology graph model | [`lab02_topology_graph`](labs/lab02_topology_graph.py) |
| M3 | Federation reputation | [`lab03_reputation_peers`](labs/lab03_reputation_peers.py) |
| M4 | LUMEN PageRank scores | [`lab04_lumen_scores`](labs/lab04_lumen_scores.py) |
| M5 | R3F oracle scene mapping | [`lab05_r3f_scenes`](labs/lab05_r3f_scenes.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/3d-data-viz-course
pip install -e ".[dev]"
pytest -q
python labs/lab01_health_probe.py
python labs/run_exercises.py
```

Labs auto-start an in-process mock server when [alien-monitor](https://github.com/alexar76/alien-monitor) is not running on `127.0.0.1:9100`.

## What you build

- **M1** — probe `/api/health` (TEST / REAL / UNIVERSE modes)
- **M2** — typed `MonitorNode` / `MonitorLink` graph from `/api/topology`
- **M3** — federation peer trust from `/api/reputation/peers`
- **M4** — LUMEN PageRank scores via `/api/reputation/lumen`
- **M5** — oracle slug → R3F camera / accent / primitive mapping

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/3d-data-viz-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).