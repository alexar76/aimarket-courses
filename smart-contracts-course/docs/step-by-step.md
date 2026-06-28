# Step-by-step course guide

> **Audience:** developers learning lottery smart-contract patterns before touching Base mainnet.  
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.  
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

On-chain lotteries fail when the *operator* can quietly re-roll a draw until they like the winner — a "grinding" attack. The `lottery/` contracts on Base defeat that with verifiable randomness (ECVRF via the **Sortes** oracle) and a **Wesolowski VDF** beacon from the **Chronos** oracle, settling payouts through a receipt-gated **AIMarketEscrow** channel. This course teaches each of those primitives as a small, runnable, LLM-free Python port. You verify the *same* Foundry test vector the Solidity contracts use (`ChronosVDF.t.sol`), walk a relayer round end to end, and finish with a capstone that simulates a full fair round with verifiable artifacts — so what you learn maps directly onto the production `lottery/` code.

---

## Table of contents

0. [Why this course](#why-this-course)
1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — Unbiasable lottery draw](#module-m1--unbiasable-lottery-draw)
4. [Module M2 — VDF verify on-chain](#module-m2--vdf-verify-on-chain)
5. [Module M3 — Escrow & payment channels](#module-m3--escrow--payment-channels)
6. [Module M4 — Relayer round lifecycle](#module-m4--relayer-round-lifecycle)
7. [Module M5 — Capstone: fair round](#module-m5--capstone-fair-round)
8. [Exercises & certificate](#exercises--certificate)
9. [Observability in every lab](#observability-in-every-lab)
10. [Bridge: from course to lottery/](#bridge-from-course-to-lottery)
11. [Self-check checklist](#self-check-checklist)
12. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Oracles |
|-------|---------|------|---------|
| **Basic** | M1 → M2 → M3 → M4 | ~1.5 h | Sortes + Chronos (fallback if not installed) |
| **Advanced** | Basic + M5 capstone | +30 min | Sortes + Chronos VDF path |
| **lottery/ bridge** | After M4 or M5 | +30 min | Live `forge test` + Base contracts |

Read **Observability** after each lab — every script prints a `Trace` you can inspect.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/smart-contracts-course
pip install -e ".[oracles,dev]"
```

The `[oracles]` extra wires in the **Sortes** (ECVRF) and **Chronos** (VDF) oracle packages. If the extra is unavailable in your environment the labs still run — `courselib` falls back to a deterministic stdlib implementation and the trace marks `oracle=fallback`. Python 3.11+ is required.

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** all tests pass (i18n parity across en/ru/es, contract primitives, the bundled Foundry vector, certificate rendering).

### Step 3 — Run the first lab

```bash
python labs/lab01_unbiasable_draw.py
python labs/run_exercises.py
```

### Step 4 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_unbiasable_draw.py
```

`COURSE_LANG` only switches the lab's printed strings (module titles, labels, hints) — code, commands, ticket numbers, and the Foundry vector are identical in every language.

### Step 5 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/smart-contracts-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + `pip install -e ".[oracles,dev]"`).
3. Set `os.environ["COURSE_LANG"] = "ru"` in the setup cell if needed.
4. Run the lab cell.

---

## Module M1 — Unbiasable lottery draw

**Concept:** Commit–reveal and ECVRF fix operator grinding attacks.  
**Lab:** `labs/lab01_unbiasable_draw.py` · **Time:** ~15 min · **Prerequisites:** setup done

### Steps

1. Open `labs/lab01_unbiasable_draw.py` and read the module docstring.
2. Run locally:

   ```bash
   python labs/lab01_unbiasable_draw.py
   ```

3. Compare the two draws in the output:
   - **Biased lottery (operator grind)** — `grindable=True`: the operator re-hashes with a secret until a favorable ticket appears (`BiasedLottery.operator_can_grind`).
   - **Fair lottery (ECVRF)** — one `alpha` maps to exactly one `beta`, with `verified=True`. The operator cannot re-roll.
4. Open `courselib/contracts.py` — read `BiasedLottery`, `FairLottery`, and `_sortes_draw` (the Sortes ECVRF path with a stdlib fallback).
5. **Exercise:** `python labs/run_exercises.py --module m1` — proves the fair draw verifies while the biased one grinds.

### What it proves

A verifiable draw removes operator discretion: the winner is a deterministic function of a public seed plus a proof anyone can check. On-chain consumer reference: `lottery/docs/` and `AIAgentLottery.sol`.

### Self-check

- [ ] You can explain why `BiasedLottery` is broken on purpose
- [ ] You see why ECVRF (`alpha → beta`) closes the grinding attack

---

## Module M2 — VDF verify on-chain

**Concept:** Wesolowski proofs from Chronos match Foundry test vectors.  
**Lab:** `labs/lab02_vdf_verify.py` · **Time:** ~15 min · **Prerequisites:** M1

### Steps

1. Run `python labs/lab02_vdf_verify.py`.
2. The lab loads the bundled Foundry vector (`courselib/fixtures/chronos_vector.json`, a copy of `lottery/contracts/test/vectors/chronos_vector.json`) and verifies `π^l·g^r ≡ y (mod N)`. Output shows `verify: True (AB_equals_y=True)`.
3. If the Chronos oracle is installed, `verify_wesolowski_vector` also re-derives the proof live (`vdf.hash_to_group → evaluate → prove → verify`); otherwise the bundled intermediates alone are checked.
4. **Exercise:** `python labs/run_exercises.py --module m2` — verifies the same vector the Solidity test uses.

### What it proves

The Python verifier and the Solidity verifier agree on the *exact same bytes*. Run `forge test` in `lottery/contracts` — `ChronosVDF.t.sol` consumes the identical vector, so a green Python check predicts a green Foundry check.

### Self-check

- [ ] You can name the Wesolowski check (`π^l·g^r ≡ y mod N`)
- [ ] You understand why a VDF makes randomness *slow to compute, fast to verify*

---

## Module M3 — Escrow & payment channels

**Concept:** Hold funds until delivery; receipt-gated debit like AIMarketEscrow.  
**Lab:** `labs/lab03_escrow_channel.py` · **Time:** ~20 min · **Prerequisites:** M1

### Steps

1. Run `python labs/lab03_escrow_channel.py`.
2. Follow the channel lifecycle in the output: **open** (deposit) → **debit** (receipt-gated) → **settle** (split between hub and refund).
3. Watch the **Receipt replay** line: a second `debit` with the same `receipt_id` is rejected (`blocked=True`). This is the on-chain replay guard — `EscrowChannel.used_receipts`.
4. Skim `courselib/contracts.py` → `EscrowChannel`. It models `AIMarketEscrow` open/debit/settle (Protocol v2 §6): signature check, nonce, hub-match, balance guard.
5. **Exercise:** `python labs/run_exercises.py --module m3` — debit twice with one receipt; the second must fail.

### Self-check

- [ ] You can name the four debit guards (signature, replay, balance, hub-match)
- [ ] You can explain how `settle` splits `to_hub` vs `refund`

---

## Module M4 — Relayer round lifecycle

**Concept:** baseSeed, Sortes draw, optional on-chain VDF path.  
**Lab:** `labs/lab04_relayer_round.py` · **Time:** ~20 min · **Prerequisites:** M1–M2

### Steps

1. Run `python labs/lab04_relayer_round.py`.
2. Trace the three phases in the output and the `Trace` block:
   - **Chronos seed** — `base_seed = sha256(roundId ‖ blockhash ‖ platonRandom)`, the keccak-packed seed the relayer feeds Chronos.
   - **Sortes ticket** — the verifiable draw for this round (`verified=True`).
   - **VDF vector** — when `onchain_vdf=True`, the round attaches a `VdfProof` beacon and re-verifies the Foundry vector (`vector_valid=True`).
3. Cross-read: `lottery/relayer/ailottery_relayer/economy_draw.py` — the production draw flow this lab mirrors.
4. **Exercise:** `python labs/run_exercises.py --module m4` — trace `baseSeed → Sortes → VDF beacon`.

### Self-check

- [ ] You can describe what binds a round to its seed (roundId, blockhash, Platon random)
- [ ] You know when the on-chain VDF path is taken vs the prevrandao path

---

## Module M5 — Capstone: fair round

**Concept:** Simulate a full lottery round with verifiable artifacts.  
**Lab:** `labs/lab05_lottery_capstone.py` · **Time:** ~30 min · **Prerequisites:** M1–M4 · **Track:** advanced

### Steps

1. Run `python labs/lab05_lottery_capstone.py`.
2. The lab calls `simulate_fair_round(onchain_vdf=True, client_seed=...)` and prints the round artifacts: `ticket`, `vdf_path=onchain`, and `chronos_vector=True`.
3. Compare these artifacts to a real `lottery/relayer` log — every field has a production counterpart.
4. **Exercise:** `python labs/run_exercises.py --module m5` — run `simulate_fair_round` with `onchain_vdf=True` and confirm the path and vector.

### What it proves

You can assemble the M1–M4 primitives into one auditable round: a verifiable ticket, a VDF beacon, and a checkable vector — the artifacts a player (or auditor) needs to trust the result without trusting the operator.

### Self-check

- [ ] You can list the artifacts a fair round produces
- [ ] You can explain `vdf_path=onchain` vs `prevrandao`

---

## Exercises & certificate

After the labs, run the DIY checks:

```bash
python labs/run_exercises.py                 # all modules
python labs/run_exercises.py --module m3     # one module
```

Each module prints `✓` or `✗`; fix any failures and re-run. When all pass, generate a certificate:

```bash
python labs/run_exercises.py --certificate "Your Name" --lang en
```

This writes `certificate.html` (override with `-o`). Open it in a browser and **Print → Save as PDF**. The credential ID is derived from name + date (`courselib/certificate.py`). You can also generate it from the **Certificate** section of the course site.

---

## Observability in every lab

**Concept:** Every lab logs decisions to `Trace` — treat it as your audit log.  
**Covered in:** every lab via `courselib/trace.py` · **Time:** 5 min after each lab

### Steps (repeat after each lab)

1. Scroll to the **trace** section at the end of the lab output.
2. Count the `events` and map each to a step you saw in stdout — `biased_draw`, `fair_draw`, `vdf_verify`, `open`/`debit`/`settle`, `base_seed`/`sortes_draw`/`vdf_beacon`, `capstone`.
3. In M4, correlate the three trace events to the three printed phases.

### Self-check

- [ ] Trace is the lab's "on-chain event log" for the round
- [ ] You can point to the single event that proves a draw was fair

---

## Bridge: from course to lottery/

**Goal:** Connect course primitives to the production `lottery/` repo (~30 min).

1. **Foundry vector** — `lottery/contracts/test/vectors/chronos_vector.json` (bundled in `courselib/fixtures/`). The course verifier reads the same file the Solidity test does.

2. **On-chain verifier** — `lottery/contracts/src/ChronosVDF.sol`; its test is `ChronosVDF.t.sol`. Run it:

   ```bash
   cd lottery/contracts && forge test
   ```

3. **Relayer draw flow** — `lottery/relayer/ailottery_relayer/economy_draw.py` (mirrored by M4).

4. **Map course → lottery/**

   | Course | lottery/ |
   |--------|----------|
   | M1 fair draw | Sortes ECVRF + `AIAgentLottery.sol` |
   | M2 VDF verify | `ChronosVDF.sol` + `ChronosVDF.t.sol` |
   | M3 escrow channel | `AIMarketEscrow` open/debit/settle |
   | M4 relayer round | `economy_draw.py` round lifecycle |
   | M5 capstone | Full relayer round + on-chain VDF beacon |

5. **Docs:** [lottery/docs/](https://github.com/alexar76/lottery/tree/main/docs).

---

## Self-check checklist

After the basic track you should be able to:

- [ ] Run lab01–lab04 locally and in Colab
- [ ] Explain why a verifiable draw beats operator grinding
- [ ] Verify the Chronos Foundry vector and say why it matches `ChronosVDF.t.sol`
- [ ] Describe the escrow open → debit → settle flow and the replay guard
- [ ] Read a `Trace` block and find the event proving fairness

After the advanced track add:

- [ ] Run lab05 and list the artifacts of a fair round
- [ ] Run `forge test` in `lottery/contracts` and connect it to M2

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: courselib` | Run from the repo root; labs prepend the parent dir to `sys.path` |
| Oracle import fails / `pip install ".[oracles]"` errors | Labs still run with the stdlib fallback (trace shows `oracle=fallback`); for the live ECVRF/VDF path run from the aicom monorepo where `oracles/` resolves |
| `verify: False` in M2 | Confirm `courselib/fixtures/chronos_vector.json` is intact (`valid` and `AB_equals_y` must be true) |
| Empty RU/ES strings | Set `COURSE_LANG`; check `i18n/ru.json` keys match `en.json` |
| pytest i18n parity failure | Add the missing key to all three of `i18n/{en,ru,es}.json` |
| Colab running old code | Re-run the setup cell; pin the `main` branch |

**lottery/ deployment & on-chain issues:** [lottery/docs/](https://github.com/alexar76/lottery/tree/main/docs).

---

Guides in `docs/` are hand-maintained — update EN first, then the RU/ES mirrors.
