# Step-by-step course guide

> **Audience:** developers shipping optimization results that a reviewer can *verify*, not just trust.
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why proofs?

Most optimization code returns an answer — a tour, a transport plan, a route, a prediction — and asks you to trust it. This course flips that: **every lab ships a certificate** the caller can re-check cheaply, without re-running the solver and without trusting the oracle that produced it.

- **TSP** returns a tour *plus* an admissible lower bound → an optimality **gap** you can bound.
- **Optimal transport** returns a plan *plus* dual potentials → strong-duality witness in O(m×n).
- **Least-time routing** returns a path *plus* eikonal potentials → edge-by-edge verification, no re-solve.
- **Gaussian processes** return a posterior *plus* a replayable mean/variance check.

The four labs use live **AIMarket oracles** — COLONY, KANTOR, FERMAT, GAUSS — and the M5 capstone chains all four certificates into one audit. This is the pattern behind verifiable agents: an answer a downstream agent can reject locally if the certificate fails.

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — TSP with quality gap](#module-m1--tsp-with-quality-gap)
4. [Module M2 — Optimal transport](#module-m2--optimal-transport)
5. [Module M3 — Least-time routing](#module-m3--least-time-routing)
6. [Module M4 — Gaussian processes](#module-m4--gaussian-processes)
7. [Module M5 — Proof portfolio capstone](#module-m5--proof-portfolio-capstone)
8. [Exercises & certificate](#exercises--certificate)
9. [Observability in every lab](#observability-in-every-lab)
10. [Bridge: from course to production oracles](#bridge-from-course-to-production-oracles)
11. [Self-check checklist](#self-check-checklist)
12. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Oracles |
|-------|---------|------|---------|
| **Basic** | M1 → M2 → M3 → M4 | ~2 h | COLONY, KANTOR, FERMAT, GAUSS |
| **Advanced** | Basic + M5 capstone | +30 min | All four chained in one audit |

Every lab prints a `Trace` you can inspect — treat it as the lab's certificate log.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/optimization-with-proofs-course
pip install -e ".[oracles,dev]"
```

The `[oracles]` extra pulls `numpy`; `[dev]` pulls `pytest`. Python 3.11+ is required.

**From the aicom monorepo** (recommended for contributors):

```bash
cd courses/optimization-with-proofs-course
pip install -e ".[oracles,dev]"
```

Oracle packages resolve automatically: `courselib/oracle_paths.py` walks up to the monorepo root and adds `oracles/oracles/{colony,kantor,fermat,gauss}` plus `oracles/core` (the FERMAT dependency) to `sys.path`.

**Standalone clone** without the monorepo sibling:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
pip install -e _deps/oracles/core
for pkg in colony kantor fermat gauss; do
  pip install -e _deps/oracles/oracles/$pkg
done
pip install -e ".[oracles,dev]"
```

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** i18n parity (en/ru/es keys match), optimization oracle integration, exercises, and lab smoke imports all pass.

### Step 3 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_colony_tsp.py
```

`COURSE_LANG` switches the printed module titles, concepts, and exercise hints via `i18n/{en,ru,es}.json`. Numbers, certificates, and oracle names stay the same.

### Step 4 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/optimization-with-proofs-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + pip + oracles slice).
3. Set `os.environ["COURSE_LANG"] = "ru"` in setup if needed.
4. Run the lab cell.

---

## Module M1 — TSP with quality gap

**Concept:** Nearest-neighbour + 2-opt tour with an admissible lower bound.
**Lab:** `labs/lab01_colony_tsp.py` · **Time:** ~20 min · **Prerequisites:** setup done

### Steps

1. Run `python labs/lab01_colony_tsp.py`.
2. Read the docstring header, then inspect the printed **tour**, **length**, **lower bound**, **gap %**, and **nn baseline**.
3. The instance is a pentagon-plus-center from `demo_tsp_points()` in `courselib/optimization.py`; `solve_tsp()` calls `colony.tsp.solve(...)` and adds the `certificate_valid` flag.
4. Confirm `certificate_valid=True` — it holds iff `gap >= 0` **and** `length >= lower_bound` (an admissible certificate).
5. **Exercise:** `python labs/run_exercises.py --module m1`.

### What it proves / produces

The gap `(length - lower_bound) / lower_bound` is a *quality certificate*: even without the optimal tour, you can state "within X% of optimal."

### Self-check

- [ ] Gap is non-negative and equals `(length - lb) / lb`
- [ ] 2-opt never lengthens the NN tour

---

## Module M2 — Optimal transport

**Concept:** Exact Kantorovich plan with a dual certificate.
**Lab:** `labs/lab02_kantor_transport.py` · **Time:** ~25 min · **Prerequisites:** setup done

### Steps

1. Run `python labs/lab02_kantor_transport.py`.
2. Compare **transport cost**, **W₂ distance**, **dual objective**, and **method** in the output.
3. `solve_transport()` calls `kantor.transport(...)` then `kantor.verify(...)`, passing the claimed cost and dual potentials. Note KANTOR expects `source_points`/`sink_points` (not `points_a`/`points_b`).
4. Confirm `verify: True` — the potentials witness optimality in O(m×n).
5. **Exercise:** `python labs/run_exercises.py --module m2`.

### What it proves / produces

Strong duality: the primal transport cost equals the dual objective `Σ aᵢuᵢ + Σ bⱼvⱼ`, with `uᵢ + vⱼ ≤ Cᵢⱼ` on every pair. A verifier checks this in one pass.

### Self-check

- [ ] Strong duality: cost ≈ Σ aᵢuᵢ + Σ bⱼvⱼ
- [ ] Dual feasibility: uᵢ + vⱼ ≤ Cᵢⱼ on every pair

---

## Module M3 — Least-time routing

**Concept:** Eikonal potentials and dual optimality on agent networks.
**Lab:** `labs/lab03_fermat_route.py` · **Time:** ~20 min · **Prerequisites:** M1 or M2

### Steps

1. Run `python labs/lab03_fermat_route.py`.
2. Inspect the path `client → router → … → sink` and the **total cost**.
3. The graph comes from `demo_routing_graph()`: edges blend **cost**, **latency**, and **reputation** between five nodes. `route_least_time()` calls `fermat.eikonal.route(...)` then `eikonal.verify(...)`.
4. Confirm `verify: True` — `T(v) ≤ T(u) + n(u,v)` on every edge, tight on the chosen path edges.
5. **Exercise:** `python labs/run_exercises.py --module m3`.

> FERMAT depends on `oracle_core`; `ensure_oracles` installs `oracle_core` before `fermat`.

### What it proves / produces

The potentials `T` form a dual certificate: a verifier confirms the path is least-time without re-running Dijkstra.

### Self-check

- [ ] Potentials T form a dual certificate without re-running Dijkstra
- [ ] Path edges are tight: T(v) = T(u) + n(u,v)

---

## Module M4 — Gaussian processes

**Concept:** Posterior uncertainty and Expected Improvement.
**Lab:** `labs/lab04_gauss_gp.py` · **Time:** ~25 min · **Prerequisites:** setup done

### Steps

1. Run `python labs/lab04_gauss_gp.py`.
2. Inspect posterior **μ** and **σ** at each query point, then the **Expected Improvement** suggestion `x` and `EI`.
3. `gp_posterior()` calls `gauss.gp.field(...)`, `gauss.gp.verify(...)`, and `gauss.gp.suggest(...)` with `goal="min"`. EI suggests the next best experiment for minimization.
4. Confirm `verify: True` — the posterior mean/variance replays from the training data.
5. **Exercise:** `python labs/run_exercises.py --module m4`.

### What it proves / produces

A replay certificate: anyone can recompute the posterior from training points and reject a mismatched claim. EI turns the uncertainty into the next query.

### Self-check

- [ ] Posterior variance rises far from training points
- [ ] EI balances exploitation (low mean) and exploration (high σ)

---

## Module M5 — Proof portfolio capstone

**Concept:** Chain TSP, transport, route, and GP certificates in one audit.
**Lab:** `labs/lab05_proof_capstone.py` · **Time:** ~30 min · **Prerequisites:** M1–M4

### Steps

1. Run `python labs/lab05_proof_capstone.py`.
2. Inspect each certificate flag printed as `success`/`blocked`: `tsp_gap_ok`, `transport_verified`, `route_verified`, `gp_verified`.
3. Read `proof_portfolio()` in `courselib/optimization.py` — it runs all four oracles and collects the flags.
4. Confirm `all_verified=True` — every oracle certificate passes.
5. **Exercise:** `python labs/run_exercises.py --module m5`.

### What it proves / produces

One composite audit object: a downstream agent rejects the whole result if any single certificate fails — no oracle is trusted blindly.

### Self-check

- [ ] You can explain what each certificate proves
- [ ] A verifier can reject a bad answer without trusting the oracle

---

## Exercises & certificate

After the labs, run the DIY checks:

```bash
python labs/run_exercises.py                          # run all module exercises
python labs/run_exercises.py --module m1              # run one module
python labs/run_exercises.py --certificate "Your Name" --lang ru
```

| Module | Exercise checks |
|--------|-----------------|
| M1 | TSP gap certificate valid; `length >= lower_bound`; `gap >= 0` |
| M2 | Kantorovich dual verifies; cost > 0 |
| M3 | FERMAT route potentials verify; path runs `client → sink` |
| M4 | GP posterior verifies; `len(mean) == len(std)` |
| M5 | Full proof portfolio — all four certificates pass |

`run_exercises.py` runs every check and prints `✓`/`✗` per module. The `--certificate` flag generates `certificate.html` **only after all exercises pass** (use `--skip-check` to bypass). Open it in a browser and **Print → Save as PDF**. The credential ID is a SHA-256 of name + date, and the certificate localizes to `--lang en|ru|es`.

---

## Observability in every lab

**Concept:** Every lab logs decisions to `Trace` (`courselib/trace.py`) — your audit trail for optimization certificates.

### Steps (repeat after each lab)

1. Scroll to the **trace** line in lab output (it prints the event count).
2. Map events to stdout: TSP gap, transport cost, route total, GP verification.
3. In M5, each oracle flag becomes a `certificate` trace event — correlate one failed flag to one event.

### Self-check

- [ ] Trace records verification outcomes for every oracle call
- [ ] You can explain what would fail if an oracle lied about optimality

---

## Bridge: from course to production oracles

**Goal:** Connect course concepts to live AIMarket oracle deployments (~30 min).

1. **Read oracle READMEs** in `oracles/oracles/{colony,kantor,fermat,gauss}/`.

2. **Map course → oracle capabilities**

   | Course | Oracle | Capability |
   |--------|--------|------------|
   | M1 | COLONY | TSP + gap certificate |
   | M2 | KANTOR | `kantor.transport@v1` + `kantor.verify@v1` |
   | M3 | FERMAT | `fermat.route@v1` + `fermat.verify@v1` |
   | M4 | GAUSS | `gauss.field@v1` + `gauss.suggest@v1` + `gauss.verify@v1` |
   | M5 | All | Composite audit in `proof_portfolio()` |

3. **Compare certificates** — each oracle returns a cheap O(n) or O(E) check a verifier runs locally, independent of the solver.

---

## Self-check checklist

After the basic track you should be able to:

- [ ] Run lab01–lab04 locally and in Colab
- [ ] Explain the TSP gap as a quality certificate
- [ ] State Kantorovich dual feasibility conditions
- [ ] Verify a FERMAT path without re-solving
- [ ] Interpret GP posterior uncertainty and EI

After the advanced track add:

- [ ] Run lab05 and list all four certificate types
- [ ] Sketch an agent workflow that rejects answers failing `verify`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: courselib` | Run from repo root; labs prepend the parent to `sys.path` |
| `Oracle package '...' not installed` | Run from the aicom monorepo, or `pip install -e ".[oracles]"` |
| `ImportError: Oracle package 'fermat'` | Install `oracle_core` first, then fermat (`ensure_oracles` does this) |
| `provide source_points+sink_points` | KANTOR expects `source_points`/`sink_points`, not `points_a` |
| `'goal' must be 'max' or 'min'` | GAUSS EI uses `goal="min"` or `"max"` |
| `numpy` missing | `pip install -e ".[oracles,dev]"` |
| Empty RU/ES strings | Set `COURSE_LANG`; check i18n key parity |
| Colab old code | Re-run the setup cell; pin the `main` branch |

---

## Regenerate site & notebooks

After editing labs or i18n:

```bash
python3 scripts/build_course_assets.py
python3 scripts/labs_to_notebooks.py
```

Guides in `docs/` are hand-maintained — update EN first, then the RU/ES mirrors.
