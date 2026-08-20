# MCP Security & Agent Safety

<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/mcp-security-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/mcp-security-course/notebooks/lab01_threat_model.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

**Threat-model MCP, catch tool poisoning with WARDEN, harden agents with LUMEN scoring.**

Interactive Python course with runnable labs and full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/mcp-security-course/](https://alexar76.github.io/aimarket-courses/mcp-security-course/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |
| **Step-by-step guide** | [EN](docs/step-by-step.md) · [Русский](docs/step-by-step.ru.md) · [Español](docs/step-by-step.es.md) — [doc index](docs/README.md) |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | MCP threat model | [`lab01_threat_model`](labs/lab01_threat_model.py) |
| M2 | Static scan & policy | [`lab02_static_scan`](labs/lab02_static_scan.py) |
| M3 | LUMEN trust scoring | [`lab03_lumen_score`](labs/lab03_lumen_score.py) |
| M4 | Owner-lock & fail-closed | [`lab04_owner_lock`](labs/lab04_owner_lock.py) |
| M5 | Capstone: malicious server | [`lab05_warden_capstone`](labs/lab05_warden_capstone.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/mcp-security-course
pip install -e ".[oracles,dev]"
pytest -q
python labs/lab01_threat_model.py
python labs/run_exercises.py
```

From the **aicom monorepo**, LUMEN resolves from `oracles/oracles/lumen` automatically. Standalone clones pull the oracle via CI or:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
pip install -e _deps/oracles/core
pip install -e _deps/oracles/oracles/lumen
pip install -e ".[oracles,dev]"
```

## What you build

- **M1** — map prompt injection and tool-poisoning attack surfaces
- **M2** — static-scan MCP tool definitions (injection, exfil, secret requests)
- **M3** — rank MCP servers with LUMEN PageRank on a trust graph
- **M4** — owner-approved tool allowlists (fail-closed)
- **M5** — full WARDEN pipeline blocks a malicious typosquat server

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/mcp-security-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).