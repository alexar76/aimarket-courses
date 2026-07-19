# Step-by-step course guide

> **Audience:** developers securing MCP-connected agents before (or alongside) ARGUS / AI-Factory.  
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.  
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

MCP (Model Context Protocol) lets an agent connect to external tool servers — but every tool *description* and JSON *schema* is attacker-controlled text the model reads as trusted instruction. This course teaches you to threat-model that surface, statically scan poisoned tool definitions, rank servers by graph-based trust (LUMEN), enforce fail-closed owner allowlists, and chain it all into a WARDEN gate that blocks a malicious typosquat server. Every primitive is a runnable, LLM-free Python port of the production ARGUS WARDEN firewall, so what you learn maps directly onto real code.

---

## Table of contents

0. [Why this course](#why-this-course)
1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — MCP threat model](#module-m1--mcp-threat-model)
4. [Module M2 — Static scan & policy](#module-m2--static-scan--policy)
5. [Module M3 — LUMEN trust scoring](#module-m3--lumen-trust-scoring)
6. [Module M4 — Owner-lock & fail-closed](#module-m4--owner-lock--fail-closed)
7. [Module M5 — Capstone: malicious server](#module-m5--capstone-malicious-server)
8. [Exercises & certificate](#exercises--certificate)
9. [Observability in every lab](#observability-in-every-lab)
10. [Bridge: from course to ARGUS WARDEN](#bridge-from-course-to-argus-warden)
11. [Self-check checklist](#self-check-checklist)
12. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Oracles |
|-------|---------|------|---------|
| **Basic** | M1 → M2 → M3 → M4 | ~2 h | LUMEN (M3 only) |
| **Advanced** | Basic + M5 capstone | +30 min | LUMEN + full WARDEN chain |
| **Factory bridge** | After M4 or M5 | +30 min | Real ARGUS + Hub |

Every lab prints a `Trace` you can inspect — treat it as the lab’s audit log.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/mcp-security-course
pip install -e ".[oracles,dev]"
```

**From the aicom monorepo** (recommended for contributors):

```bash
cd courses/mcp-security-course
pip install -e ".[oracles,dev]"
```

LUMEN resolves automatically from `oracles/oracles/lumen` when run inside the monorepo.

**Standalone clone** without monorepo sibling:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
pip install -e _deps/oracles/oracles/lumen
pip install -e ".[oracles,dev]"
```

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** i18n parity, WARDEN static scan, LUMEN PageRank, exercises, lab smoke imports.

### Step 3 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_threat_model.py
```

### Step 4 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/mcp-security-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + pip + oracles slice).
3. Set `os.environ["COURSE_LANG"] = "ru"` in setup if needed.
4. Run the lab cell.

---

## Module M1 — MCP threat model

**Concept:** Prompt injection, tool poisoning, and exfiltration paths in MCP.  
**Lab:** `labs/lab01_threat_model.py` · **Time:** ~15 min · **Prerequisites:** setup done

### Steps

1. Open `labs/lab01_threat_model.py` and read the module docstring.
2. Run locally:

   ```bash
   python labs/lab01_threat_model.py
   ```

3. Watch two scenarios:
   - **Prompt injection** — attacker prose hidden in a tool *description*
   - **Tool poisoning** — schema fields that request secrets or exfil URLs

4. Read the **trace** block — each attack surface is logged as an event.

5. Skim `courselib/warden.py` — find `INJECTION_PATTERNS`, `EXFIL_PATTERNS`, `SECRET_PATTERNS` (5 min).

### Expected output (EN)

- Line `== MCP threat model ==`
- User task + poisoned tool definition
- Trace with `attack_surface` events

### Self-check

- [ ] You can explain why tool *descriptions* are attacker-controlled text the model trusts
- [ ] You see the difference between user prompt injection and tool-definition poisoning

---

## Module M2 — Static scan & policy

**Concept:** Catch malicious tool schemas before an agent runs them.  
**Lab:** `labs/lab02_static_scan.py` · **Time:** ~20 min · **Prerequisites:** M1

### Steps

1. Run `python labs/lab02_static_scan.py`.
2. Compare **benign** vs **malicious** scan sections:
   - benign → high score, zero or low-severity findings
   - malicious → low score, `TOOL_DEF_INJECTION`, `TOOL_DEF_EXFIL`, `TOOL_DEF_SECRET_REQUEST`
3. Read finding messages — note which haystack matched (`description` vs `input schema`).
4. Open `argus/src/warden/static-scan.ts` in the monorepo — compare regex parity with `courselib/warden.py`.
5. **Exercise:** `python labs/run_exercises.py --module m2`.

### Self-check

- [ ] Static scan runs on description *and* JSON schema text
- [ ] A single critical finding tanks the gate score but does not always fatal-block alone

---

## Module M3 — LUMEN trust scoring

**Concept:** Graph-based reputation — who-trusts-whom PageRank over MCP servers.  
**Lab:** `labs/lab03_lumen_score.py` · **Time:** ~20 min · **Prerequisites:** `[oracles]` (numpy + lumen)

### Steps

1. Confirm install: `pip install -e ".[oracles,dev]"`.
2. Run `python labs/lab03_lumen_score.py`.
3. Note the trust graph edges: hub → official servers; typosquat isolated.
4. Inspect ranked scores — `hub` and official servers should outrank `offical-mcp-drainer`.
5. Read `courselib/lumen.py` — `demo_mcp_trust_graph()` and `score_servers()`.
6. Optional: open `oracles/oracles/lumen/lumen/pagerank.py` for the EigenTrust kernel.
7. **Exercise:** `python labs/run_exercises.py --module m3`.

### Self-check

- [ ] Scores sum to 1 (probability distribution)
- [ ] Transitive trust elevates nodes trusted by trusted nodes

---

## Module M4 — Owner-lock & fail-closed

**Concept:** Bind agents to owner-approved tool allowlists (Telegram owner-lock analogue).  
**Lab:** `labs/lab04_owner_lock.py` · **Time:** ~15 min · **Prerequisites:** M2

### Steps

1. Run `python labs/lab04_owner_lock.py`.
2. See allowed tools (`read_file`, `search_docs`) pass; `exec_shell`, `transfer_funds` blocked.
3. Note the **empty allowlist** demo — fail-closed, every tool denied.
4. Read `OwnerLock` in `courselib/warden.py` — `check_tool()` and `OwnerLockGate`.
5. Cross-read: [argus/docs/channels.md](https://github.com/alexar76/aicom/blob/main/argus/docs/channels.md) § Telegram owner-lock.
6. **Exercise:** `python labs/run_exercises.py --module m4`.

### Self-check

- [ ] Allowlist is explicit — unknown tools are denied, not silently allowed
- [ ] Empty allowlist is fail-closed (zero trust by default)

---

## Module M5 — Capstone: malicious server

**Concept:** Full WARDEN gate chain blocks a poisoned typosquat MCP server.  
**Lab:** `labs/lab05_warden_capstone.py` · **Time:** ~30 min · **Prerequisites:** M1–M4

### Steps

1. Run `python labs/lab05_warden_capstone.py`.
2. Compare verdicts:
   - **Benign official server** → `allowed`, high composite score
   - **Poisoned typosquat** → `blocked`, `decided_by` names the failing gate
3. Gate order in the teaching port: static-scan → threat-feed → reputation (LUMEN) → owner-lock → pinning.
4. Inspect findings list — multiple gates may contribute before block.
5. Read `Warden.vet()` in `courselib/warden.py` — composite score is product of gate scores.
6. **Exercise:** `python labs/run_exercises.py --module m5`.

### Self-check

- [ ] Threat feed catches typosquat server id (`offical-mcp-drainer`)
- [ ] Static scan catches injection + exfil in tool defs
- [ ] Low LUMEN reputation contributes when `allow_unknown_servers=False`

---

## Exercises & certificate

After labs, run DIY checks:

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Your Name" --lang ru
```

Opens `certificate.html` — print to PDF from the browser. Credential ID is derived from name + date.

| Module | Exercise checks |
|--------|-----------------|
| M1 | Injection signature detected in poisoned tool |
| M2 | Benign tools produce no critical findings |
| M3 | Hub outranks typosquat on trust graph |
| M4 | Owner-lock denies unlisted tools |
| M5 | Full WARDEN blocks malicious capstone server |

---

## Observability in every lab

**Concept:** Every lab logs decisions to `Trace` — your audit trail for security events.

### Steps (repeat after each lab)

1. Scroll to the **trace** section in lab output.
2. Map events to stdout: findings, trust scores, owner-lock decisions, WARDEN verdicts.
3. In M5, correlate `warden_finding` events to the printed findings list.

### Self-check

- [ ] Trace is the lab’s “SIEM preview” for agent security
- [ ] You can point to the gate that blocked a connection

---

## Bridge: from course to ARGUS WARDEN

**Goal:** Connect course concepts to production ARGUS (~30 min).

1. **Read WARDEN docs** — [argus/docs/security-warden.md](https://github.com/alexar76/aicom/blob/main/argus/docs/security-warden.md)

2. **Map course → ARGUS**

   | Course | ARGUS |
   |--------|-------|
   | M2 static-scan | `src/warden/static-scan.ts` |
   | M3 LUMEN | `ReputationGate` + LUMEN oracle |
   | M4 owner-lock | Channel owner-lock + egress allowlist |
   | M5 capstone | `Warden.create()` gate chain |

3. **Run ARGUS** (optional, from monorepo):

   ```bash
   cd argus && npm install && npm test -- warden
   ```

4. **Hub supply security** — [aimarket-hub/docs/supply-security.md](https://github.com/alexar76/aicom/blob/main/aimarket-hub/docs/supply-security.md)

---

## Self-check checklist

After the basic track you should be able to:

- [ ] Run lab01–lab04 locally and in Colab
- [ ] Name three static-scan signature families (injection, exfil, secrets)
- [ ] Explain PageRank trust on an MCP server graph
- [ ] Describe fail-closed owner allowlists
- [ ] Read a `Trace` block and find the blocked tool or gate

After the advanced track add:

- [ ] Run lab05 and explain which gate blocked the typosquat server
- [ ] Open `argus/src/warden/index.ts` and find the production gate order

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: courselib` | Run from repo root; labs prepend parent to `sys.path` |
| `ImportError: Oracle package 'lumen'` | Install oracles slice or run from aicom monorepo |
| `numpy` missing | `pip install -e ".[oracles,dev]"` |
| Empty RU/ES strings | Set `COURSE_LANG`; check `i18n/ru.json` keys match `en.json` |
| pytest i18n failure | Add missing keys to all three JSON files |
| M5 benign server blocked | Check owner-lock allowlist includes benign tool names |
| Colab old code | Re-run setup cell; pin `main` branch |

**ARGUS issues:** [argus/README.md](https://github.com/alexar76/aicom/blob/main/argus/README.md)

---

## Regenerate site & notebooks

After editing labs or i18n:

```bash
python3 scripts/build_course_assets.py
python3 scripts/labs_to_notebooks.py
```

Guides in `docs/` are hand-maintained — update EN first, then RU/ES mirrors when added.
