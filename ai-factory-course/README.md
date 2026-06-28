<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/alexar76/aimarket-courses/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/ai-factory-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/ai-factory-course/notebooks/lab01_pipeline_overview.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# AI Factory Pipeline & Orchestration

**Research→design→build→test→ship — probe factory APIs and orchestrator stages.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/ai-factory-course/](https://alexar76.github.io/aimarket-courses/ai-factory-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Pipeline overview | [`lab01_pipeline_overview`](labs/lab01_pipeline_overview.py) |
| M2 | Pipeline status API | [`lab02_pipeline_status`](labs/lab02_pipeline_status.py) |
| M3 | Shipped products catalog | [`lab03_products_catalog`](labs/lab03_products_catalog.py) |
| M4 | Orchestrator stage flow | [`lab04_orchestrator_stages`](labs/lab04_orchestrator_stages.py) |
| M5 | Capstone: factory probe | [`lab05_factory_capstone`](labs/lab05_factory_capstone.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/ai-factory-course
pip install -e ".[factory,dev]"
pytest -q
python labs/lab01_pipeline_overview.py
python labs/run_exercises.py
```

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/ai-factory-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).