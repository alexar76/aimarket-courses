# Build an Agent Economy from Scratch

<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/agent-economy-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/agent-economy-course/notebooks/lab01_protocol_overview.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

**Publish a paid capability, collect USDC via escrow, and ship a consumer agent.**

Interactive Python course: 6 modules (M1–M6), runnable labs, full **EN / RU / ES** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/agent-economy-course/](https://alexar76.github.io/aimarket-courses/agent-economy-course/) |
| **Colab** | Open any lab from the site — notebooks live in [`notebooks/`](notebooks/) |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` |

## Documentation (step-by-step)

| Guide | Language |
|-------|----------|
| [docs/step-by-step.md](docs/step-by-step.md) | English |
| [docs/step-by-step.ru.md](docs/step-by-step.ru.md) | Русский |
| [docs/step-by-step.es.md](docs/step-by-step.es.md) | Español |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Protocol v2 overview | [`lab01`](labs/lab01_protocol_overview.py) |
| M2 | SDK & Hub integration | [`lab02`](labs/lab02_hub_discover.py) |
| M3 | Escrow & payment channels | [`lab03`](labs/lab03_escrow_channel.py) |
| M4 | Reputation & trust | [`lab04`](labs/lab04_reputation_trust.py) |
| M5 | Publish a capability | [`lab05`](labs/lab05_publish_capability.py) |
| M6 | Capstone: paid agent loop | [`lab06`](labs/lab06_paid_capability_capstone.py) |

**Hub-lite track:** labs 1–5 need `[hub-lite]` (~5 MB, no git clones).  
**Sandbox track:** lab 6 needs the full `aimarket-agent` SDK (`[sandbox]`, ~50 MB).  
**Exercises:** `python labs/run_exercises.py` — DIY checks after each lab.  
**Certificate:** `python labs/run_exercises.py --certificate "Your Name" --lang ru`

## Quick start (local)

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/agent-economy-course
pip install -e ".[hub-lite,dev]"    # add [sandbox] for lab 6
pytest -q
python labs/lab01_protocol_overview.py
python labs/run_exercises.py
```

| Extra | Used by | Size |
| --- | --- | --- |
| `[hub-lite]` | M1–M5 | ~5 MB |
| `[sandbox]` | M6 only | ~50 MB (git clones) |

## Project layout

```
courselib/     # protocol validation, hub-lite, economy sandbox, trust
docs/          # Step-by-step guide (EN)
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

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/agent-economy-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).