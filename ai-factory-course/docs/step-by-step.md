# Step-by-step course guide

> **Audience:** developers integrating with the AI-Factory pipeline — public status endpoints, the shipped-products catalog, and the orchestrator stage flow.
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

AI-Factory turns a one-line idea into a shipped product by walking it through orchestrated stages: **research → design → build → test → ship**. Each stage is owned by an agent (analyst, architect, developer, QA, devops), and the factory exposes a small **public API surface** so anyone can watch the pipeline breathe and list what it has shipped.

This course teaches that surface from the outside in. You probe the same two public endpoints the homepage uses, walk the orchestrator state machine from `IDEA_RECEIVED` to `COMPLETED`, and finish with a capstone probe — **without needing a running factory**. Every lab falls back to an **embedded mock factory** on `127.0.0.1`, so the whole course runs offline. Point one env var at a live factory and the exact same labs read real data.

Every lab prints a `Trace` block: the orchestration is logged, not magic.

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (5 minutes)](#setup-5-minutes)
3. [Module M1 — Pipeline overview](#module-m1--pipeline-overview)
4. [Module M2 — Pipeline status API](#module-m2--pipeline-status-api)
5. [Module M3 — Shipped products catalog](#module-m3--shipped-products-catalog)
6. [Module M4 — Orchestrator stage flow](#module-m4--orchestrator-stage-flow)
7. [Module M5 — Capstone: factory probe](#module-m5--capstone-factory-probe)
8. [Live factory vs embedded mock](#live-factory-vs-embedded-mock)
9. [Observability — the Trace in every lab](#observability--the-trace-in-every-lab)
10. [Exercises & certificate](#exercises--certificate)
11. [Bridge: from course to AI-Factory](#bridge-from-course-to-ai-factory)
12. [Self-check checklist](#self-check-checklist)
13. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Live factory |
|-------|---------|------|--------------|
| **Basic** | M1 → M2 → M3 → M4 | ~1.5 h | No — embedded mock |
| **Advanced** | Basic + M5 capstone | +30 min | Optional (`COURSE_FACTORY_URL`) |
| **Factory bridge** | After M5 | +30 min | Yes — real factory + Hub |

You never *need* a live factory: M2, M3 and M5 start an embedded mock automatically when none is reachable. The `source` field in each lab's output tells you which one answered (`mock` or `live`).

---

## Setup (5 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/ai-factory-course
pip install -e ".[factory,dev]"
```

The `[factory]` extra pulls in `fastapi` + `uvicorn` — they power the embedded mock factory that M2/M3/M5 fall back to. `[dev]` adds `pytest`. (Python 3.11+ is required.)

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** all tests pass — i18n parity across `en/ru/es`, the factory client and orchestrator walk, the exercise checks, and a smoke run of all five labs.

### Step 3 — Run the first lab

```bash
python labs/lab01_pipeline_overview.py
```

You should see the five pipeline phases mapped to agents, then a `trace` block, then a "Your turn" exercise hint.

### Step 4 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es; default is en
python labs/lab01_pipeline_overview.py
```

All headings, labels and hints switch language; code, state names (`COMPLETED`), and endpoint paths stay in English. Resolution order is explicit arg → `COURSE_LANG` → English fallback.

### Step 5 — Colab alternative

Open the [course site](https://alexar76.github.io/aimarket-courses/ai-factory-course/) → **Open in Colab** on any lab → run the setup cell (clone + `pip install -e ".[factory,dev]"`) → set `os.environ["COURSE_LANG"] = "ru"` if you want, then run the lab cell.

---

## Module M1 — Pipeline overview

**Concept:** research → design → build → test → ship as orchestrated stages, each owned by an agent.
**Lab:** `labs/lab01_pipeline_overview.py` · **Time:** ~15 min · **Prerequisites:** setup done

### Steps

1. Open `labs/lab01_pipeline_overview.py` and read the docstring.
2. Run it:

   ```bash
   python labs/lab01_pipeline_overview.py
   ```

3. Read the **five pipeline phases** table — each line is `phase → agent → state`, e.g. `research → analyst → MARKET_RESEARCHED`, ending at `ship → devops → COMPLETED`.
4. Open `courselib/factory.py` and find `PIPELINE_PHASES` — the exact tuple the lab prints (this is the teaching map; the real orchestrator graph comes later in M4).

### What it proves

The factory is not a black box: there is a fixed, inspectable mapping from a business phase to the agent that owns it and the state it leaves behind. Every `phase` line is also logged as a trace event.

### Self-check

- [ ] You can name all five phases in order
- [ ] You can say which agent owns each phase

---

## Module M2 — Pipeline status API

**Concept:** the homepage heartbeat — `GET /api/public/pipeline-status` returns *in-pipeline* vs *shipped* counts.
**Lab:** `labs/lab02_pipeline_status.py` · **Time:** ~15 min · **Prerequisites:** M1

### Steps

1. Run:

   ```bash
   python labs/lab02_pipeline_status.py
   ```

2. Read three lines: **In pipeline**, **Shipped**, and **Data source**.
3. Note the `Data source` value — `mock` (embedded factory started for you) or `live` (if `COURSE_FACTORY_URL` points at a reachable factory).
4. Open `courselib/factory.py` → `FactoryClient.get_pipeline_status()` to see the single HTTP `GET` behind it.

### What it proves

A public heartbeat endpoint is enough to answer "is the factory busy, and how much has it shipped?" — the same numbers the landing page shows. The mock returns a deterministic 4 in-pipeline / 2 shipped so the lab is reproducible offline.

### Self-check

- [ ] You can read in-pipeline vs shipped from the output
- [ ] You know whether your run hit `mock` or `live`

---

## Module M3 — Shipped products catalog

**Concept:** `GET /ai-market/products` lists `COMPLETED` products and their capabilities.
**Lab:** `labs/lab03_products_catalog.py` · **Time:** ~15 min · **Prerequisites:** M2

### Steps

1. Run:

   ```bash
   python labs/lab03_products_catalog.py
   ```

2. Read the **Shipped products** count and the first few products: `id: name (N caps)`.
3. Each product carries `capabilities` — id plus `price_per_call_usd`. Skim `MOCK_PRODUCTS` in `courselib/factory.py` for the shape (`demo-analytics`, `demo-orchestrator`).
4. The trace logs one `products` event plus one `product` event per listed item.

### What it proves

What the factory ships becomes a marketplace catalog: each product exposes priced, invokable capabilities. This is the bridge between "the pipeline finished something" and "you can call it" — explored in the Factory bridge below.

### Self-check

- [ ] `count` equals the number of products listed
- [ ] You can point to a capability id and its per-call price

---

## Module M4 — Orchestrator stage flow

**Concept:** the orchestrator is a state machine; walk it from `IDEA_RECEIVED` to `COMPLETED`.
**Lab:** `labs/lab04_orchestrator_stages.py` · **Time:** ~20 min · **Prerequisites:** M1

### Steps

1. Run:

   ```bash
   python labs/lab04_orchestrator_stages.py
   ```

2. Read the **Orchestrator path** — each line is `STATE  agent=<who>`, starting at `IDEA_RECEIVED` and ending at `COMPLETED`.
3. The transitions come from `config/pipeline_flow.json` **in the monorepo** when present; standalone, the lab uses the built-in `agent_flow` fallback in `courselib/factory.py`.
4. Open `walk_to_ship()` and `next_state()` in `courselib/factory.py` — note the `max_steps` guard that stops the walk at `COMPLETED`/`DEPLOYED_PRODUCTION` and prevents infinite loops.

### What it proves

The phase map from M1 is backed by a real transition table. Each `STATE → (agent, next_state)` edge is logged as a `transition` trace event, so the whole path is auditable.

### Self-check

- [ ] The path begins at `IDEA_RECEIVED` and reaches `COMPLETED`
- [ ] You can explain why the walk terminates (the loop guard)

---

## Module M5 — Capstone: factory probe

**Concept:** one end-to-end probe — heartbeat + catalog + phases — against a live factory or the embedded mock.
**Lab:** `labs/lab05_factory_capstone.py` · **Time:** ~20 min · **Prerequisites:** M2–M4 · **Track:** advanced

### Steps

1. Run:

   ```bash
   python labs/lab05_factory_capstone.py
   ```

2. Read the combined result: `in_pipeline=… shipped=…`, the catalog `count` and its `source`, then the five `phases`.
3. Open `probe_factory()` in `courselib/factory.py` — it reuses one `factory_client()` to call both endpoints, then attaches the phase list. This is exactly the basic-track labs composed into one call.
4. Re-run with `COURSE_FACTORY_URL` set to watch `source` flip from `mock` to `live`.

### What it proves

You can health-check and inventory a factory in a single round trip, and the answer is identical in shape whether it came from a real deployment or the local mock — the integration contract is stable.

### Self-check

- [ ] You can name the chain: status → products → phases in one probe
- [ ] You can explain the `source ∈ {live, mock}` distinction

---

## Live factory vs embedded mock

Every networked lab (M2, M3, M5) uses `factory_client()`, which:

1. Reads a base URL from `COURSE_FACTORY_URL` (or `AIFACTORY_URL` / `FACTORY_PUBLIC_URL`).
2. If set **and reachable**, talks to that live factory — output shows `source: live`.
3. Otherwise starts an **embedded FastAPI mock** on a free `127.0.0.1` port, waits for `/api/health`, and serves deterministic data — output shows `source: mock`.

Point at a live factory:

```bash
export COURSE_FACTORY_URL=https://your-factory.example
python labs/lab02_pipeline_status.py    # now reads real counts
```

The exercise checks (`prefer_live=False`) always use the mock so they pass offline and in CI.

---

## Observability — the Trace in every lab

**Concept:** every lab records what it did so behaviour is inspectable, not magic.
**Covered in:** all five labs via the `Trace` helper · **Time:** 5 min after each lab

### Steps (repeat after M1–M5)

1. Scroll to the `trace (N events):` block at the end of the lab output.
2. Map each event to a line you saw above it — a `phase`/`transition`/`product`/`pipeline_status`/`capstone` entry per action.
3. Compare across labs: M1 logs five `phase` events; M4 logs one `transition` per state hop; M5 logs a single rolled-up `capstone` event.

### Self-check

- [ ] The trace is the lab's "unit-test log" for what the probe did
- [ ] You can correlate one printed line to one trace event

---

## Exercises & certificate

Each lab ends with a "Your turn" hint. Run the matching DIY check:

```bash
python labs/run_exercises.py --module m1     # one module
python labs/run_exercises.py                 # all modules → ✓/✗ per module
```

The module checks live in `courselib/exercises.py` (e.g. M1 asserts the five phases in order; M4 asserts the walk starts at `IDEA_RECEIVED` and reaches `COMPLETED`).

When all five pass, mint a certificate:

```bash
python labs/run_exercises.py --certificate "Your Name" --lang en
```

This writes `certificate.html`; open it and **Print → Save as PDF**. The credential ID is a SHA-256 of name + issue date (stable for the same name on the same day). Use `--lang ru` / `--lang es` for a localized certificate, `-o path.html` to choose the output file, and `--skip-check` only if you must generate without re-running the checks.

---

## Bridge: from course to AI-Factory

**Goal:** run the same probes against the *real* factory pipeline (~30 min).

1. **Start the factory** (from the monorepo root):

   ```bash
   docker compose up -d app
   # → http://localhost:9080
   ```

2. **Point the labs at it:**

   ```bash
   export COURSE_FACTORY_URL=http://localhost:9080
   python labs/lab05_factory_capstone.py    # source: live
   ```

3. **Submit an idea** — follow [USER_GUIDE.md](https://github.com/alexar76/aicom/blob/main/docs/USER_GUIDE.md) § "Your first 15 minutes": `/admin/login` → **New product** → **Pipeline** and watch the stage strip advance through the real states you walked in M4.

4. **Map course → factory:**

   | Course | Factory |
   |--------|---------|
   | M1 phases | Pipeline stage strip (real agents) |
   | M2 status | Homepage `/api/public/pipeline-status` |
   | M3 catalog | Shipped products on `/ai-market/products` |
   | M4 stage flow | Orchestrator `config/pipeline_flow.json` |
   | M5 capstone | One probe against the live deployment |

5. **Invoke a shipped capability** — once a product is `COMPLETED`, its capabilities are callable via the Hub: [hub-integration-guide.md](https://github.com/alexar76/aicom/blob/main/docs/hub-integration-guide.md).

---

## Self-check checklist

After the basic track you should be able to:

- [ ] Run lab01–lab04 locally (and in Colab)
- [ ] Name the five phases and the agent that owns each
- [ ] Read in-pipeline vs shipped from `pipeline-status`
- [ ] Explain `source ∈ {live, mock}` and how `COURSE_FACTORY_URL` decides
- [ ] Walk the orchestrator from `IDEA_RECEIVED` to `COMPLETED` and explain the loop guard

After the advanced track add:

- [ ] Run lab05 and describe status → products → phases in one probe
- [ ] Point a lab at a live factory and see `source` flip to `live`
- [ ] Mint a certificate with `--certificate "<name>" --lang <en|ru|es>`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: courselib` | Run from the repo root; labs prepend the parent dir to `sys.path` |
| Mock factory "did not become ready" | Port contention or `[factory]` extra missing — reinstall with `pip install -e ".[factory,dev]"` |
| `source` always `mock` when you expect `live` | `COURSE_FACTORY_URL` unset or unreachable; the client silently falls back to the mock |
| `fastapi`/`uvicorn` import error | You installed without `[factory]`; that extra provides the mock server |
| Empty RU/ES strings | Set `COURSE_LANG`; missing keys fall back to English (never crash) |
| pytest i18n parity failure | A key exists in one catalog but not all three — add it to `i18n/en.json`, `ru.json`, `es.json` |
| Colab running old code | Re-run the setup cell to re-clone `main` |

**Factory issues:** [FAQ.md](https://github.com/alexar76/aicom/blob/main/docs/FAQ.md)

---

## Regenerate site & notebooks

After editing labs or `i18n/`:

```bash
python3 scripts/build_course_assets.py
```

Guides in `docs/` are hand-maintained — update EN first, then the RU/ES mirrors.
