<!-- aicom-mirror-notice -->
> **📖 Read-only mirror.** `aimarket-courses` is published from the canonical AI-Factory monorepo.
> **Pull requests are not accepted** — any commit pushed here is overwritten by
> `scripts/mirror_satellites.sh` on the next sync.
> 🐞 Found a bug or have a request? Please **[open an issue](https://github.com/alexar76/aimarket-courses/issues)**.

# AIMarket Courses

<!-- aicom-readme-badges -->
<p align="center">
  <a href="https://github.com/alexar76/aimarket-courses/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/alexar76/aimarket-courses/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <img src="https://img.shields.io/badge/courses-10-brightgreen" alt="10 courses" />
  <img src="https://img.shields.io/badge/languages-EN%20%2F%20RU%20%2F%20ES-blue" alt="EN RU ES" />
  <a href="https://alexar76.github.io/aimarket-courses/"><img src="https://img.shields.io/badge/Pages-academy-6e40c9" alt="Course portal" /></a>
  <a href="docs/badges/coverage.svg"><img src="docs/badges/coverage.svg" alt="Test coverage" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
</p>
<!-- /aicom-readme-badges -->



**Ten hands-on Python academies — one monorepo, like [aimarket-desktop](https://github.com/alexar76/aimarket-desktop).**

Each course is a folder with its own `README.md`, labs, Colab notebooks (EN/RU/ES), step-by-step docs, and GitHub Pages sub-site. All embed the **live AIMarket ecosystem** as a sandbox — oracles, WARDEN, Hub/SDK, lottery, alien-monitor, factory API.

| Course | Folder | Live site |
| --- | --- | --- |
| **AI Agent Orchestration** | [orchestration-course/](orchestration-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/orchestration-course/) |
| **Verifiable Randomness & Cryptographic Time** | [verifiable-randomness-course/](verifiable-randomness-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/verifiable-randomness-course/) |
| **MCP Security & Agent Safety** | [mcp-security-course/](mcp-security-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/mcp-security-course/) |
| **Build an Agent Economy from Scratch** | [agent-economy-course/](agent-economy-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/agent-economy-course/) |
| **The Mathematics of Trust** | [mathematics-of-trust-course/](mathematics-of-trust-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/mathematics-of-trust-course/) |
| **Optimization with Proofs** | [optimization-with-proofs-course/](optimization-with-proofs-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/optimization-with-proofs-course/) |
| **Smart Contracts for Agent Economies** | [smart-contracts-course/](smart-contracts-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/smart-contracts-course/) |
| **Build Your Own Autonomous AI Factory** | [ai-factory-course/](ai-factory-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/ai-factory-course/) |
| **3D Data Viz with React-Three-Fiber** | [3d-data-viz-course/](3d-data-viz-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/3d-data-viz-course/) |
| **Physics-Inspired Computing** | [physics-inspired-computing-course/](physics-inspired-computing-course/) | [Pages ↗](https://alexar76.github.io/aimarket-courses/physics-inspired-computing-course/) |

**Portal:** [alexar76.github.io/aimarket-courses](https://alexar76.github.io/aimarket-courses/) · **Colab:** open any lab from a course site → **Open in Colab**

---

## Quality bar (every course)

- Live labs wired to real ecosystem assets
- Graded exercises + HTML certificate
- **3 languages** (EN / RU / ES)
- Step-by-step docs (`docs/step-by-step.md` + RU/ES)
- CI — pytest, asset build, smoke labs
- GitHub Pages sub-site under this repo

---

## Develop

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/orchestration-course   # pick any course folder
pip install -e ".[hub-lite,dev]"
pytest -q
python3 scripts/build_course_assets.py     # notebooks + local site/
```

Build the **unified Pages tree** (portal + all course sites):

```bash
python3 _tooling/build_monorepo_pages.py   # writes site/
```

---

## Monorepo source

Developed in the [aicom](https://github.com/alexar76/aicom) monorepo under `courses/`. Published here via:

```bash
./scripts/publish_all_repos.sh --satellite aimarket-courses
```

Legacy standalone repo `alexar76/orchestration-course` is **archived** — use [`aimarket-courses`](https://github.com/alexar76/aimarket-courses) and the [academy portal](https://alexar76.github.io/aimarket-courses/).

---

## Scaffold a new course

See [`catalog.yaml`](catalog.yaml) and:

```bash
python3 _tooling/scaffold_course.py --id course-NAME
python3 _tooling/sync_monorepo_config.py
```

Do **not** re-scaffold shipped courses (`--force` overwrites real content).
