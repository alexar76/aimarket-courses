# Step-by-step course guide

> **Audience:** hub operators and agent builders joining the AIMarket federation.  
> **Languages:** `COURSE_LANG=en|ru|es|fr|zh` · UI strings in `i18n/` · this guide in English.  
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Why this course

A federation knock is an **observation**. It must never index a stranger’s catalogue. This course walks the real admission path used by [modelmarket.dev](https://modelmarket.dev): well-known identity, open vs closed door, preview quarantine (search/invoke never read that table), declared vs read capability counts, and approve → crawl. Labs prefer live public GETs; fixtures are labelled and never presented as LIVE.

---

## Table of contents

0. [Why this course](#why-this-course)
1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — Well-known & announce](#module-m1--well-known--announce)
4. [Module M2 — Open door vs closed door](#module-m2--open-door-vs-closed-door)
5. [Module M3 — Preview quarantine](#module-m3--preview-quarantine)
6. [Module M4 — Declared vs read counts](#module-m4--declared-vs-read-counts)
7. [Module M5 — Capstone: approve a stranger](#module-m5--capstone-approve-a-stranger)
8. [Exercises & certificate](#exercises--certificate)
9. [Bridge to production docs](#bridge-to-production-docs)
10. [Self-check checklist](#self-check-checklist)
11. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Network |
|-------|---------|------|---------|
| **Basic** | M1 → M4 | ~2 h | Live hub preferred; `COURSE_OFFLINE=1` OK |
| **Advanced** | Basic + M5 capstone | +30 min | Live probe of modelmarket.dev |
| **Operator bridge** | After M5 | +30 min | Read admission + peer-keys docs |

Every lab prints a `Trace` — treat it as the lab’s audit log.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/federation-peer-hubs-course
pip install -e ".[hub-lite,dev]"
```

**From the aicom monorepo:**

```bash
cd courses/federation-peer-hubs-course
pip install -e ".[hub-lite,dev]"
```

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** i18n parity (5 langs), federation fixtures, exercise solutions, lab smoke (offline).

### Step 3 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, fr, zh — default en
python labs/lab01_well_known_announce.py
```

### Step 4 — Offline vs live

- Default labs hit `https://modelmarket.dev` (override with `COURSE_HUB_URL`).
- `COURSE_OFFLINE=1` forces labelled fixtures.
- `COURSE_LIVE=1 pytest tests/test_live_optional.py` for optional network asserts.

---

## Module M1 — Well-known & announce

**Concept:** How a hub introduces itself; a knock never indexes.  
**Lab:** `labs/lab01_well_known_announce.py` · **Time:** ~15 min

### Steps

1. Run `python labs/lab01_well_known_announce.py`.
2. Confirm LIVE source: `/.well-known/ai-market.json`.
3. Note `name`, `federated_capabilities_count`, `signer_public_key`, and hybrid signature (`ed25519` + `ml-dsa-65`).
4. Read the knock note: announce = observation only.

### Self-check

- [ ] You can name the well-known fields an operator trusts for identity
- [ ] You understand knock ≠ index

---

## Module M2 — Open door vs closed door

**Concept:** `open_federation` is the door; pending can exist either way; preview is separate.  
**Lab:** `labs/lab02_open_vs_closed.py` · **Time:** ~20 min

### Steps

1. Run the lab against the live peers endpoint.
2. Record `door`, `trusted_count`, `pending_count`.
3. Study the counterfactual with the door forced closed — pending still allowed in the teaching model.

### Self-check

- [ ] Open door allows stranger announce → pending
- [ ] Closed door does not erase quarantine / pending from seeds

---

## Module M3 — Preview quarantine

**Concept:** Signed pending manifests land in a table search/invoke never read.  
**Lab:** `labs/lab03_preview_quarantine.py` · **Time:** ~20 min

### Steps

1. Run the lab; confirm all three read guards are `false`.
2. Inspect pending snapshot (may be empty on a quiet hub — empty queue is still evidence).
3. Skim `aimarket-hub` docs on admission / preview.

### Self-check

- [ ] Preview rows are never searchable or invocable
- [ ] Empty pending does not weaken the quarantine rule

---

## Module M4 — Declared vs read counts

**Concept:** Declared claim ≠ verified count; UI must show both.  
**Lab:** `labs/lab04_declared_vs_read.py` · **Time:** ~20 min

### Steps

1. Compare hub `federated_capabilities_count` with indexed peer rows.
2. For pending: `declared_capabilities` vs `preview_capabilities`.
3. If the live queue is empty, study the labelled fixture stranger gap.

### Self-check

- [ ] You never trust the knock claim alone
- [ ] Operator UI shows declared **and** read

---

## Module M5 — Capstone: approve a stranger

**Concept:** Checklist announce → pending → preview → approve → crawl + live probe.  
**Lab:** `labs/lab05_approve_capstone.py` · **Time:** ~30 min · **Track:** advanced

### Steps

1. Walk the printed checklist.
2. Run the live probe: name, hybrid signature, door, peers.
3. Note that Approve/repin need an admin bearer — this lab stops at the public surface.

### Self-check

- [ ] You can recite the five admission steps in order
- [ ] You know where operator Approve lives vs what the public API shows

---

## Exercises & certificate

1. Fill `# YOUR CODE HERE` stubs in `courselib/exercises.py` (hints print at the end of each lab).
2. `python labs/run_exercises.py`
3. Certificate: `python labs/run_exercises.py --certificate "Your Name"`
4. Instructors / CI: `COURSE_USE_SOLUTIONS=1 python labs/run_exercises.py`

---

## Bridge to production docs

- [federation-admission.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-admission.md) — assay, auto-admit, sandbox evidence
- [federation-peer-keys.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-peer-keys.md) — pin, key_mismatch, repin

---

## Self-check checklist

- [ ] Live well-known returns hybrid signature fields
- [ ] `open_federation` interpreted correctly
- [ ] Preview quarantine never feeds search/invoke
- [ ] Declared vs read honesty gap understood
- [ ] Capstone checklist order memorized
- [ ] Exercises pass; certificate generated

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Network / HTTP errors | `COURSE_OFFLINE=1` or check `COURSE_HUB_URL` |
| Exercises all fail | Fill stubs, or use `COURSE_USE_SOLUTIONS=1` for reference |
| i18n missing key | Ensure `COURSE_LANG` is one of en/ru/es/fr/zh |
| Site assets stale | `python scripts/build_course_assets.py` |
