<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://alexar76.github.io/aimarket-courses/federation-peer-hubs-course/"><img src="https://img.shields.io/badge/Pages-course-6e40c9" alt="Course site" /></a>
  <a href="https://colab.research.google.com/github/alexar76/aimarket-courses/blob/main/federation-peer-hubs-course/notebooks/lab01_well_known_announce.ipynb"><img src="https://img.shields.io/badge/Colab-notebooks-yellow" alt="Colab" /></a>
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg"><img src="https://raw.githubusercontent.com/alexar76/aimarket-courses/main/docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->

# Federation & Peer Hubs

**Announce, quarantine, preview, approve — how hubs join without trusting strangers.**

Interactive Python course with live public GETs against [modelmarket.dev](https://modelmarket.dev), runnable labs, and full **EN / RU / ES / FR / ZH** localization.

| | |
| --- | --- |
| **Course site** | [alexar76.github.io/aimarket-courses/federation-peer-hubs-course/](https://alexar76.github.io/aimarket-courses/federation-peer-hubs-course/) |
| **Live hub** | `https://modelmarket.dev` |
| **Languages** | `COURSE_LANG=en` · `ru` · `es` · `fr` · `zh` |
| **Docs** | [Step-by-step (EN)](docs/step-by-step.md) · [RU](docs/step-by-step.ru.md) · [ES](docs/step-by-step.es.md) · [FR](docs/step-by-step.fr.md) · [ZH](docs/step-by-step.zh.md) |

## Modules

| Module | Topic | Lab |
| --- | --- | --- |
| M1 | Well-known & announce | [`lab01_well_known_announce`](labs/lab01_well_known_announce.py) |
| M2 | Open door vs closed door | [`lab02_open_vs_closed`](labs/lab02_open_vs_closed.py) |
| M3 | Preview quarantine | [`lab03_preview_quarantine`](labs/lab03_preview_quarantine.py) |
| M4 | Declared vs read counts | [`lab04_declared_vs_read`](labs/lab04_declared_vs_read.py) |
| M5 | Capstone: approve a stranger | [`lab05_approve_capstone`](labs/lab05_approve_capstone.py) |

## Quick start

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/federation-peer-hubs-course
pip install -e ".[hub-lite,dev]"
python labs/lab01_well_known_announce.py
python labs/run_exercises.py
```

Offline (no network): `COURSE_OFFLINE=1 python labs/lab01_well_known_announce.py`  
Optional live pytest: `COURSE_LIVE=1 pytest -q tests/test_live_optional.py`

## Concepts (map to production)

| Course idea | Live surface |
| --- | --- |
| Knock / announce | Observation only — never indexes |
| Open vs closed door | `open_federation` on `/federation/peers` |
| Preview quarantine | Pending manifests; search/invoke never read that table |
| Declared vs read | `declared_capabilities` vs `preview_capabilities` / indexed count |
| Approve → crawl | Operator Approve or assay auto-admit, then index |

Hub docs: [`federation-admission.md`](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-admission.md), [`federation-peer-keys.md`](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-peer-keys.md).

Labs prefer **live public GETs**. Fixtures are labelled and never presented as LIVE.

## Source of truth

Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/federation-peer-hubs-course/`, mirrored to this repository.

## License

MIT — see [LICENSE](LICENSE).