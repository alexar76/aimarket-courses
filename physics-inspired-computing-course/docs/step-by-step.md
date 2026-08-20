# Step-by-step course guide

> **Audience:** engineers who want physics-inspired primitives — consensus, routing, sampling, risk, thermodynamics — as ready-to-call AIMarket oracles.
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

Most "AI" courses stop at prompting. This one teaches **deterministic, physics-inspired computation** that you can verify, certify, and bill — the kind of primitive that sits *underneath* an agent, not on top of it. Each module wraps a real AIMarket oracle: **Murmuration** (robust swarm consensus), **Colony** (TSP tours with an admissible optimality-gap certificate), **Turing** (blue-noise sampling), **Ablation** (systemic-risk cascades as a self-organised-critical sandpile), and **Landauer** (the kT·ln2 thermodynamic floor on irreversible compute).

Every lab is **reproducible** (seeded, no LLM by default) and prints a `Trace` you can inspect. By the end you can call any of these five oracles, read its output, and earn a course certificate.

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — Murmuration consensus](#module-m1--murmuration-consensus)
4. [Module M2 — Colony TSP certificate](#module-m2--colony-tsp-certificate)
5. [Module M3 — Turing blue-noise](#module-m3--turing-blue-noise)
6. [Module M4 — Ablation cascade risk](#module-m4--ablation-cascade-risk)
7. [Module M5 — Landauer thermodynamic audit (advanced)](#module-m5--landauer-thermodynamic-audit-advanced)
8. [Tracing in every lab](#tracing-in-every-lab)
9. [Exercises & certificate](#exercises--certificate)
10. [Bridge: from course to AIMarket](#bridge-from-course-to-aimarket)
11. [Self-check checklist](#self-check-checklist)
12. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | NumPy | LLM |
|-------|---------|------|-------|-----|
| **Basic** | M1 → M2 → M3 → M4 | ~2 h | Yes (`[oracles]`) | No |
| **Advanced** | Basic + M5 | +45 min | Yes | No |

Every lab is deterministic — there is **no LLM** in this course. The "intelligence" is in the physics: robust statistics, combinatorial bounds, criticality, thermodynamics. Read the [Tracing](#tracing-in-every-lab) note after each lab — every script prints a `Trace` block.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/physics-inspired-computing-course
pip install -e ".[oracles,dev]"
```

The `[oracles]` extra pulls in **NumPy** (the only runtime dependency); `[dev]` adds pytest. Python **3.11+** is required.

> **Inside the aicom monorepo?** You can skip the oracle wheels — the labs resolve `murmuration`, `colony`, `turing`, `ablation`, and `landauer` straight from `oracles/oracles/*` via `courselib/oracle_paths.py`. Outside the monorepo, `[oracles]` is what makes the imports work.

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** all tests pass (i18n parity across `en/ru/es`, oracle bridges, certificate, exercises).

### Step 3 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_murmuration_consensus.py
```

`COURSE_LANG` switches every lab's printed strings (titles, concepts, labels) via `courselib/i18n.py`. Numbers, oracle names, and trace kinds stay the same — only the prose is localized. Unknown values fall back to English, never crash.

### Step 4 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/physics-inspired-computing-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + `pip install -e ".[oracles,dev]"`).
3. Set `os.environ["COURSE_LANG"] = "ru"` in the setup cell if needed.
4. Run the lab cell.

---

## Module M1 — Murmuration consensus

**Concept:** robust DeGroot consensus and Tukey-biweight aggregation over noisy agent estimates.
**Lab:** `labs/lab01_murmuration_consensus.py` · **Oracle:** Murmuration · **Time:** ~15 min · **Track:** basic

### Steps

1. Open `labs/lab01_murmuration_consensus.py` and read the docstring (industry map: *swarm intelligence, robust stats*).
2. Run it:

   ```bash
   python labs/lab01_murmuration_consensus.py
   ```

3. The lab feeds six estimates — five near `2.0` plus one wild outlier `50.0` — into the oracle and prints:
   - `median`, `trimmed_mean`, `biweight`
   - `converged` value and the number of DeGroot `iterations`
   - a `Trace` block at the end
4. Note that `biweight` ≈ 2.0 even though the raw mean would be ~10 — the outlier is **resisted**, not averaged in.
5. Skim `courselib/physics.py::murmuration_aggregate` and the oracle's `murmuration.consensus.aggregate`.

### What it proves

A single bad sensor (or a malicious agent) cannot drag the consensus. The biweight estimator down-weights far-out points, so the swarm agrees on the truth, not the noise.

### Self-check

- [ ] You can explain why `biweight` < `mean` for this input
- [ ] You see why the lab is deterministic (no LLM, seeded data)

---

## Module M2 — Colony TSP certificate

**Concept:** nearest-neighbour + 2-opt tour with an **admissible optimality-gap bound**.
**Lab:** `labs/lab02_colony_tsp.py` · **Oracle:** Colony · **Time:** ~20 min · **Track:** basic · **Prerequisites:** M1

### Steps

1. Run:

   ```bash
   python labs/lab02_colony_tsp.py
   ```

2. The lab solves a 6-city tour and prints:
   - `tour` (the visiting order)
   - `length` of the tour
   - `lower_bound` (a provable floor on the optimal length)
   - `gap` as a percentage — how far the tour *could* be from optimal
3. Read the `Trace` block — the `tsp` event logs `length` and `gap`.
4. The key idea: `length ≥ lower_bound` always, so `gap` is a **certificate**. You ship the tour *and* a guarantee on its quality.

### What it proves

You don't need the exact optimum to act — a small `gap` (say < 5%) is often a good-enough answer with a number attached. This is how you make heuristics accountable.

### Self-check

- [ ] You can read the `gap` and say "this tour is at most X% worse than optimal"
- [ ] You understand why `length` is never below `lower_bound`

---

## Module M3 — Turing blue-noise

**Concept:** Mitchell best-candidate sampling for even-but-irregular point sets.
**Lab:** `labs/lab03_turing_bluenoise.py` · **Oracle:** Turing · **Time:** ~20 min · **Track:** basic · **Prerequisites:** M1

### Steps

1. Run:

   ```bash
   python labs/lab03_turing_bluenoise.py
   ```

2. The lab requests 64 points (`candidates=12`, `seed=2026`) and prints:
   - `count`
   - `min_distance` — the smallest gap between any two points
   - `seed` and its `seed_source`
   - a 3-point `sample` of the coordinates
3. Compare to a uniform-random scatter: blue-noise **maximises the minimum distance**, so there are no clumps and no gaps.
4. Re-run with a different `seed` (edit the lab) — the layout changes but `min_distance` stays high.

### What it proves

Blue-noise sampling beats naive random sampling for Monte Carlo, dithering, and procedural placement: even coverage with no visible structure.

### Self-check

- [ ] You can explain why a high `min_distance` is the goal, and that `seed` makes the sample reproducible

---

## Module M4 — Ablation cascade risk

**Concept:** Abelian sandpile self-organised criticality — power-law avalanche sizes and tail risk.
**Lab:** `labs/lab04_ablation_cascade.py` · **Oracle:** Ablation · **Time:** ~20 min · **Track:** basic · **Prerequisites:** M1

### Steps

1. Run:

   ```bash
   python labs/lab04_ablation_cascade.py
   ```

2. The lab builds a small directed **exposure graph** (`demo_exposure_graph()` — banks A→D plus a sink), drops 1200 grains, and prints:
   - `tau` — the power-law exponent of the avalanche-size distribution
   - `max_avalanche` — the largest cascade observed
   - `cvar95` — the 95% conditional value-at-risk (expected size of the worst 5% of cascades)
   - `topple_total`
3. Read the `Trace` block — the `cascade` event logs `tau` and `max_avalanche`.
4. The intuition: in a critical system, small perturbations occasionally trigger **system-wide** cascades. `tau` and `cvar95` quantify that tail.

### What it proves

Average behaviour hides the danger. A heavy-tailed (`tau`-governed) distribution means rare-but-huge cascades dominate the risk — exactly the failure mode of interconnected financial or infrastructure networks.

### Self-check

- [ ] You can explain why a *mean* avalanche size understates the risk
- [ ] You know what `cvar95` measures versus a simple average

---

## Module M5 — Landauer thermodynamic audit (advanced)

**Concept:** the kT·ln2 bit-erasure energy floor over an operation DAG.
**Lab:** `labs/lab05_landauer_audit.py` · **Oracle:** Landauer · **Time:** ~30 min · **Track:** advanced

### Steps

1. Run:

   ```bash
   python labs/lab05_landauer_audit.py
   ```

2. The lab audits a small irreversible circuit (`demo_circuit_ops()` — two inputs, an AND gate, an output) at `temperature_k=300.0` and prints:
   - `irreversible_bits` — bits destroyed by the logic
   - `energy_floor_j` — the Landauer floor in joules (kT·ln2 per erased bit)
   - `efficiency`
   - `circuit_commitment` — a hash committing to the audited circuit
3. Read the `Trace` block — the `landauer` event logs `bits` and `floor_j`.
4. The physics: erasing one bit at temperature T costs **at least** kT·ln2 joules. An AND gate destroys information (two inputs → one output), so it has a non-zero floor.

### What it proves

There is a hard, temperature-dependent lower bound on the energy any irreversible computation must dissipate. The audit turns that physical law into a number you can attribute to a circuit — and the `circuit_commitment` makes the audit tamper-evident.

### Self-check

- [ ] You can name the kT·ln2 floor and what each term means
- [ ] You understand why the AND gate has `irreversible_bits ≥ 1`

---

## Tracing in every lab

**Concept:** every lab logs a `Trace` so its behaviour is inspectable, not magic.
**Covered in:** all five labs · **Time:** 5 min after each lab

Every script builds a `courselib.trace.Trace` and calls `trace.log(kind, **fields)`. The lab prints how many `events` it recorded; the `kind` (`consensus`, `tsp`, `bluenoise`, `cascade`, `landauer`) tells you which physics primitive ran and the fields capture the headline numbers.

### Steps (repeat after each lab)

1. Scroll to the `trace` / `events` line at the end of the lab output.
2. Map the logged `kind` and fields to the result block you just read.
3. Treat the trace as the lab's "unit-test log" — in production these become billing receipts and audit records.

### Self-check

- [ ] You can match each trace event to a printed result
- [ ] You see the trace as the bridge from lab output to a verifiable receipt

---

## Exercises & certificate

After the labs, run the DIY checks:

```bash
python labs/run_exercises.py
```

This runs all five module exercises (`m1`–`m5`) and prints a `✓`/`✗` per module. Run one at a time while iterating:

```bash
python labs/run_exercises.py --module m4
```

Each exercise asserts the property the lab teaches — e.g. `m1` checks that `biweight` resists an outlier, `m2` that `length ≥ lower_bound`, `m4` that `tau > 0.5`.

Once all five pass, generate your certificate:

```bash
python labs/run_exercises.py --certificate "Your Name" --lang en
```

This writes `certificate.html` (use `--lang ru` or `--lang es` for a localized credential). Open it in a browser and **Print → Save as PDF**. The credential ID is a hash of name + date, so it is stable and verifiable. Pass `--skip-check` only if you want the HTML without re-running the exercises.

---

## Bridge: from course to AIMarket

The five oracles you called locally are the same packages served live in the AIMarket ecosystem. To go from "I ran the lab" to "I called a hosted oracle":

| Course (local lab) | AIMarket (hosted oracle) |
|--------------------|--------------------------|
| M1 `murmuration_aggregate` | Murmuration oracle — consensus capability |
| M2 `colony_tsp` | Colony oracle — routing + certificate |
| M3 `turing_bluenoise` | Turing oracle — sampling capability |
| M4 `ablation_cascade` | Ablation oracle — systemic-risk capability |
| M5 `landauer_audit` | Landauer oracle — thermodynamic audit |
| Lab `Trace` | Hosted invoke receipt + provenance |

The `circuit_commitment` (M5) and the `gap` certificate (M2) are exactly the kind of verifiable output that lets a buyer trust an oracle's answer without re-running it.

---

## Self-check checklist

After the **basic** track you should be able to:

- [ ] Run lab01–lab04 locally and in Colab
- [ ] Explain robust consensus (M1) and why the outlier is resisted
- [ ] Read a TSP `gap` certificate (M2) as a quality guarantee
- [ ] Say why blue-noise (M3) beats uniform random for coverage
- [ ] Describe what `tau`/`cvar95` capture about cascade risk (M4)
- [ ] Read a `Trace` block and match each event to a result

After the **advanced** track add:

- [ ] Run lab05 and state the kT·ln2 floor in words
- [ ] Pass all five exercises and generate a certificate

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: courselib` | Run from the repo root; labs prepend the parent dir to `sys.path` |
| `ImportError: Oracle package '…' not installed` | Run `pip install -e ".[oracles]"`, or run from inside the aicom monorepo so `oracles/oracles/*` resolves |
| `ModuleNotFoundError: numpy` | The `[oracles]` extra installs NumPy — re-run `pip install -e ".[oracles,dev]"` |
| Python version error | Course requires **Python 3.11+** |
| Empty / English strings under another language | Set `COURSE_LANG`; check the key exists in `i18n/ru.json` / `i18n/es.json` |
| pytest i18n parity failure | Add the missing key to **all three** of `i18n/en.json`, `ru.json`, `es.json` |
| Certificate refuses to generate | Exercises must pass first; run `python labs/run_exercises.py`, or pass `--skip-check` |
| Colab running old code | Re-run the setup cell; pin the `main` branch |

---

## Regenerate site & notebooks

After editing labs or `i18n/`:

```bash
python3 scripts/build_course_assets.py
```

Guides in `docs/` are hand-maintained — update EN first, then mirror the RU/ES versions.
