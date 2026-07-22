# Step-by-step course guide

> **Audience:** developers building agent trust, reputation, and systemic-risk audits with AIMarket oracles.  
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.  
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

Multi-agent systems must answer one recurring question: *which agent (or aggregate, or path) do I trust, and can I prove it?* This course turns that question into math you can run. Five live AIMarket oracles compute the signals — **LUMEN** (PageRank/EigenTrust), **PERCOLA** (percolation thresholds), **FOURIER** (spectral connectivity), **MURMURATION** (robust consensus), and **ABLATION** (sandpile cascade risk) — and every signal ships with its own **verification certificate**, so you never have to take the oracle's word for it. The labs are deterministic NumPy: no API keys, no network for the basic track.

You finish able to score a who-trusts-whom graph, spot the keystone whose removal fractures it, measure how close it is to splitting, aggregate noisy estimates against an adversary, and quantify systemic-cascade tail risk — then fold all of it into one verifiable trust audit.

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — EigenTrust with LUMEN](#module-m1--eigentrust-with-lumen)
4. [Module M2 — Percolation & keystones](#module-m2--percolation--keystones)
5. [Module M3 — Spectral connectivity](#module-m3--spectral-connectivity)
6. [Module M4 — Robust consensus](#module-m4--robust-consensus)
7. [Module M5 — Cascade risk](#module-m5--cascade-risk)
8. [Module M6 — Trust math capstone](#module-m6--trust-math-capstone)
9. [Exercises & certificate](#exercises--certificate)
10. [Observability in every lab](#observability-in-every-lab)
11. [Bridge: from course to production oracles](#bridge-from-course-to-production-oracles)
12. [Self-check checklist](#self-check-checklist)
13. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Oracles |
|-------|---------|------|---------|
| **Basic** | M1 → M2 → M3 → M4 | ~2 h | LUMEN, PERCOLA, FOURIER, MURMURATION |
| **Advanced** | Basic + M5 cascade | +30 min | + ABLATION sandpile |
| **Capstone** | M6 combined audit | +20 min | LUMEN + FOURIER + PERCOLA together |

There are **six runnable labs** (`labs/lab01`–`lab06`), one per module. Every lab prints a `Trace` you can inspect — treat it as the lab’s audit log. Labs that call a verifiable oracle also print `verify: True`, meaning the result was independently re-checked, not just asserted.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/mathematics-of-trust-course
pip install -e ".[oracles,dev]"
```

**From the aicom monorepo** (recommended for contributors):

```bash
cd courses/mathematics-of-trust-course
pip install -e ".[oracles,dev]"
```

All five oracles resolve automatically from `oracles/oracles/*` when run inside the monorepo.

**Standalone clone** without monorepo sibling:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
for pkg in lumen murmuration fourier percola ablation; do
  pip install -e _deps/oracles/oracles/$pkg
done
pip install -e ".[oracles,dev]"
```

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** i18n parity, trust oracle integration, exercises, lab smoke imports.

### Step 3 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_keystone_nodes.py
```

### Step 4 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/mathematics-of-trust-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + pip + oracles slice).
3. Set `os.environ["COURSE_LANG"] = "ru"` in setup if needed.
4. Run the lab cell.

---

## Module M1 — EigenTrust with LUMEN

**Concept:** PageRank stationary distribution over a who-trusts-whom graph.  
**Lab:** `labs/lab02_trust_pagerank.py` · **Time:** ~20 min · **Prerequisites:** setup done

### Steps

1. Run `python labs/lab02_trust_pagerank.py`.
2. Inspect the teaching graph in `courselib/trust.py` — `demo_trust_graph()`.
3. Note ranked scores — `hub` and well-connected agents should outrank peripheral nodes.
4. Read `oracles/oracles/lumen/lumen/pagerank.py` for the EigenTrust kernel (5 min).
5. **Exercise:** `python labs/run_exercises.py --module m1`.

### Self-check

- [ ] Scores sum to 1 (probability distribution)
- [ ] Transitive trust elevates nodes trusted by trusted nodes

---

## Module M2 — Percolation & keystones

**Concept:** Targeted node removal and critical thresholds on trust graphs.  
**Lab:** `labs/lab01_keystone_nodes.py` · **Time:** ~20 min · **Prerequisites:** setup done

### Steps

1. Run `python labs/lab01_keystone_nodes.py`.
2. Watch `f_c` — the critical fraction of nodes whose removal collapses connectivity.
3. Inspect `keystones` — bridge nodes between two cliques (`3`, `4`, `8` in the teaching graph).
4. Confirm `verify: True` — PERCOLA re-computes the threshold without trusting the oracle.
5. **Exercise:** `python labs/run_exercises.py --module m2`.

### Self-check

- [ ] You can explain why a bridge node is a keystone
- [ ] Verification passes without re-running the full Monte Carlo search

---

## Module M3 — Spectral connectivity

**Concept:** Fiedler value and spectral bisection — how close is the graph to splitting?  
**Lab:** `labs/lab03_spectral_cut.py` · **Time:** ~20 min · **Prerequisites:** M1 or M2

### Steps

1. Run `python labs/lab03_spectral_cut.py`.
2. Read λ₂ (Fiedler value) — small values mean the graph has a narrow bottleneck.
3. Inspect the spectral cut sets A and B plus conductance.
4. Open `oracles/oracles/fourier/fourier/spectral.py` — `analyze()` and `verify()` (5 min).
5. **Exercise:** `python labs/run_exercises.py --module m3`.

### Self-check

- [ ] Fiedler eigenpair certificate verifies in O(E)
- [ ] Conductance quantifies how “expensive” the cut is

---

## Module M4 — Robust consensus

**Concept:** Median, trimmed mean, and biweight location over agent estimates.  
**Lab:** `labs/lab04_consensus_aggregate.py` · **Time:** ~15 min · **Prerequisites:** setup done

### Steps

1. Run `python labs/lab04_consensus_aggregate.py`.
2. Compare naive mean vs median vs biweight on `demo_agent_estimates()` (one outlier at 500).
3. Read `murmuration/consensus.py` — breakdown points and DeGroot iteration count.
4. **Exercise:** `python labs/run_exercises.py --module m4`.

### Self-check

- [ ] Median and biweight resist the adversarial outlier
- [ ] DeGroot converges to the arithmetic mean on the complete graph

---

## Module M5 — Cascade risk

**Concept:** Abelian sandpile avalanches and power-law tail risk.  
**Lab:** `labs/lab05_sandpile_cascade.py` · **Time:** ~30 min · **Prerequisites:** M1–M4

### Steps

1. Run `python labs/lab05_sandpile_cascade.py`.
2. Inspect τ (power-law exponent), max avalanche, and CVaR 99%.
3. Read top trigger nodes — who most often ignites large cascades.
4. Confirm `verify: True` — topple total and τ replay bit-for-bit.
5. **Exercise:** `python labs/run_exercises.py --module m5`.

### Self-check

- [ ] Avalanche sizes are order-independent (abelian property)
- [ ] Heavy tail (small τ) signals systemic contagion risk

---

## Module M6 — Trust math capstone

**Concept:** Combine PageRank, spectral, and percolation signals into one verifiable trust audit.  
**Lab:** `labs/lab06_trust_audit.py` · **Time:** ~20 min · **Prerequisites:** M1–M3

### Steps

1. Run `python labs/lab06_trust_audit.py`.
2. Read the one-line audit over `demo_trust_graph()`:
   - **Most trusted** node + its PageRank score (LUMEN) — expect `hub`.
   - **Algebraic connectivity** λ₂ + its FOURIER `verify` flag.
   - **Percolation threshold** f_c + its PERCOLA `verify` flag.
   - **Keystone nodes** that bridge the graph.
3. Confirm the final `verify: True` — it is the **AND** of the spectral and percolation certificates. A single failed proof fails the whole audit.
4. Open `courselib/trust.py` — read `trust_audit_summary()`: it calls `score_pagerank`, `analyze_spectral`, and `analyze_percolation`, then returns `top_trusted`, `fiedler_value`, `percolation_f_c`, `keystones`, and both verify flags.
5. Sketch how you would gate an agent action on all three signals at once (trusted source **and** connected graph **and** no keystone fragility).
6. **Exercise:** `python labs/run_exercises.py --module m6`.

### Expected output (EN)

- Line `== Trust math capstone ==`
- `Trust audit (7 nodes)` with most-trusted = `hub`, λ₂, f_c, and keystones
- Final `verify: True`

### Self-check

- [ ] You can name the three oracles the audit composes (LUMEN, FOURIER, PERCOLA)
- [ ] You understand why the audit verifies only when *every* signal verifies

---

## Exercises & certificate

After labs, run DIY checks:

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Your Name" --lang ru
```

| Module | Exercise checks |
|--------|-----------------|
| M1 | PageRank scores sum to 1 |
| M2 | Keystone nodes detected; PERCOLA verify passes |
| M3 | Fiedler certificate verifies |
| M4 | Consensus resists outlier |
| M5 | Cascade τ and topple total verify |
| M6 | Combined audit: `hub` top-trusted, spectral + percolation proofs both pass |

The certificate covers all six modules. The HTML opens in a browser; **Print → Save as PDF** for a shareable copy. The credential ID is `sha256(name|date)[:12]`, so the same name on the same day always reproduces the same ID. To regenerate without re-running the checks, add `--skip-check`; to choose where it lands, pass `-o path/to/certificate.html`.

---

## Observability in every lab

**Concept:** Every lab logs decisions to `Trace` — your audit trail for trust events.

### Steps (repeat after each lab)

1. Scroll to the **trace** section in lab output.
2. Map events to stdout: trust scores, percolation thresholds, spectral values, consensus stats, cascade metrics.
3. In M5, correlate `cascade` events to printed τ and CVaR.

### Self-check

- [ ] Trace is the lab’s “SIEM preview” for trust math
- [ ] You can point to the verification flag for each oracle call

---

## Bridge: from course to production oracles

**Goal:** Connect course concepts to live AIMarket oracle deployments (~30 min).

1. **Read oracle READMEs** in `oracles/oracles/{lumen,percola,fourier,murmuration,ablation}/`.

2. **Map course → oracle capabilities**

   | Course | Oracle | Capability |
   |--------|--------|------------|
   | M1 | LUMEN | `lumen.pagerank@v1` |
   | M2 | PERCOLA | `percola.threshold@v1` + `percola.verify@v1` |
   | M3 | FOURIER | `fourier.spectrum@v1` + `fourier.verify@v1` |
   | M4 | MURMURATION | `murmuration.aggregate@v1` |
   | M5 | ABLATION | `ablation.cascade@v1` + `ablation.verify@v1` |
   | M6 | LUMEN + FOURIER + PERCOLA | composed audit (`trust_audit_summary`) |

3. **Invoke via Hub** (optional, from monorepo):

   ```bash
   cd aimarket-hub && pytest -q -k lumen
   ```

---

## Self-check checklist

After the basic track you should be able to:

- [ ] Run lab01–lab04 locally and in Colab
- [ ] Explain PageRank trust on a who-trusts-whom graph
- [ ] Name keystone nodes on a bridge graph
- [ ] Interpret Fiedler value and conductance
- [ ] Choose median vs mean for adversarial agent estimates

After the advanced track add:

- [ ] Run lab05 and explain sandpile tail risk
- [ ] Run lab06 and read `trust_audit_summary()`; explain why the audit verifies only when every signal verifies

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: courselib` | Run from repo root; labs prepend parent to `sys.path` |
| `ImportError: Oracle package 'lumen'` | Install oracles slice or run from aicom monorepo |
| `numpy` missing | `pip install -e ".[oracles,dev]"` |
| Empty RU/ES strings | Set `COURSE_LANG`; check `i18n/ru.json` keys match `en.json` |
| pytest i18n failure | Add missing keys to all three JSON files |
| PERCOLA verify fails | Ensure `samples` matches between analyze and verify |
| Colab old code | Re-run setup cell; pin `main` branch |

---

## Regenerate site & notebooks

After editing labs or i18n:

```bash
python3 scripts/build_course_assets.py
python3 scripts/labs_to_notebooks.py
```

Guides in `docs/` are hand-maintained — update EN first, then RU/ES mirrors when added.
