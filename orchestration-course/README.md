# AI Agent Orchestration

<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/alexar76/aimarket-courses/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/orchestration-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/orchestration-course/notebooks/lab01_agent_and_tool.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

**Learn the patterns. Run them against a real agent economy.**

Interactive Python course: 9 modules (M1–M9), runnable labs, full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/orchestration-course/](https://alexar76.github.io/aimarket-courses/orchestration-course/) |
| **Colab** | Open any lab from the site — notebooks live in [`notebooks/`](notebooks/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |

## Documentation (step-by-step)

Concepts live in lab docstrings and `i18n/`. For a full hands-on path (setup → M1–M9 → factory bridge):

| Guide | Language |
|-------|----------|
| [docs/step-by-step.md](docs/step-by-step.md) | English |
| [docs/step-by-step.ru.md](docs/step-by-step.ru.md) | Русский |
| [docs/step-by-step.es.md](docs/step-by-step.es.md) | Español |

See [docs/README.md](docs/README.md) for the doc index.

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Agent loop & tool use | [`lab01`](labs/lab01_agent_and_tool.py) |
| M2 | Topologies (sequential, parallel, router) | [`lab02`](labs/lab02_topologies.py) |
| M3 | Handoffs & delegation | [`lab03`](labs/lab03_handoff.py) |
| M4 | Discovery & invocation | [`lab04`](labs/lab04_discover_invoke.py) |
| M5 | State, memory, context | [`lab05`](labs/lab05_state_context.py) |
| M6 | Guardrails & safety | [`lab06`](labs/lab06_guardrails.py) |
| M7 | Trust & provenance | [`lab07`](labs/lab07_receipt_verify.py) |
| M8 | Economics of orchestration | [`lab08`](labs/lab08_metered_economy.py) |
| M9 | Observability | covered via `Trace` in every lab |

**Basic track:** labs 1–3 & 5–6 — deterministic patterns, no extra deps; optional LLM in lab01 (`USE_LLM=1`).  
**Economy labs:** labs 4 & 7 need `[hub-lite]` (~5 MB); lab 8 needs the full `aimarket-agent` SDK (`[sandbox]`, ~50 MB).  
**Exercises:** `python labs/run_exercises.py` — DIY checks after each lab.  
**Certificate:** `python labs/run_exercises.py --certificate "Your Name" --lang ru`

## Quick start (local)

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/orchestration-course
pip install -e ".[dev]"          # add [hub-lite] for labs 4 & 7, [sandbox] for lab 8
pytest -q
python labs/lab01_agent_and_tool.py
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Jane Doe" --lang en
```

| Extra | Used by | Size |
| --- | --- | --- |
| *(none)* | M1–M3, M5–M6 | 0 |
| `[hub-lite]` | M4, M7 | ~5 MB |
| `[sandbox]` | M8 only | ~50 MB (git clones) |

Optional LLM demo: `USE_LLM=1 OPENAI_API_KEY=sk-… python labs/lab01_agent_and_tool.py`

## Google Colab

Each lab has a notebook under `notebooks/` with a one-cell setup (clone + pip install). Example:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/orchestration-course/notebooks/lab01_agent_and_tool.ipynb)

Set `COURSE_LANG` in the setup cell to `ru` or `es` before running the lab cell.

## Project layout

```
courselib/     # Neutral orchestration primitives + economy sandbox bridge
docs/          # Step-by-step guides (EN / RU / ES)
labs/          # Runnable lab scripts
notebooks/     # Colab-ready .ipynb (generated — run scripts/build_course_assets.py)
i18n/          # en / ru / es JSON catalogs
tests/         # pytest suite
site/          # GitHub Pages static output (built in CI)
```

## Regenerate site & notebooks

```bash
python3 scripts/build_course_assets.py
```

## Testing & coverage

```bash
pytest -q          # 28 tests, all green
```

Coverage is rendered to `docs/badges/coverage.svg` by `scripts/ci_coverage_badge.sh` (run in CI).

## Source of truth

Part of the [**aimarket-courses**](https://github.com/alexar76/aimarket-courses) monorepo — **academy portal:** [alexar76.github.io/aimarket-courses](https://alexar76.github.io/aimarket-courses/). Developed in the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/orchestration-course/`. Legacy standalone repo `alexar76/orchestration-course` is archived.

## License

MIT — see [LICENSE](LICENSE).