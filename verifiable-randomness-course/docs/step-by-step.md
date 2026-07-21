# Step-by-step course guide

> **Audience:** developers who need randomness a lottery player can verify — before wiring `lottery/` on Base.
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

Most lotteries, raffles, and "random" drops trust an operator who can quietly re-roll an unfavourable result. This course shows you the cryptography that removes that trust: a verifiable chaos draw, a verifiable delay function (VDF) that proves elapsed work, an ECVRF proof you can verify offline from **80 bytes**, and an RSW time-lock that hides a value until provable work unseals it. You then **build a biased lottery, attack it, and fix it** with a draw the operator cannot grind — exactly the pattern the AIMarket `lottery/` contracts consume on Base.

Every lab talks to a **real AIMarket oracle** — Platon, Chronos, Sortes, Aestus — running locally, not a mock. Each prints a `Trace` block so the verifiable artifact (proof, beta, puzzle, VDF vector) is something you can inspect, not take on faith.

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — Platon chaos VRF](#module-m1--platon-chaos-vrf)
4. [Module M2 — Chronos VDF](#module-m2--chronos-vdf)
5. [Module M3 — Sortes ECVRF](#module-m3--sortes-ecvrf)
6. [Module M4 — Aestus time-lock](#module-m4--aestus-time-lock)
7. [Module M5 — Commit–reveal & bias attacks](#module-m5--commitreveal--bias-attacks)
8. [Module M6 — On-chain verification](#module-m6--on-chain-verification)
9. [Reading the trace (every lab)](#reading-the-trace-every-lab)
10. [Exercises & certificate](#exercises--certificate)
11. [Bridge: from course to the lottery on Base](#bridge-from-course-to-the-lottery-on-base)
12. [Self-check checklist](#self-check-checklist)
13. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Oracles |
|-------|---------|------|---------|
| **Basic** | M1 → M2 → M3 → M4 | ~2 h | Platon, Chronos, Sortes, Aestus (all local) |
| **Economy** | Basic + M5 | +30 min | Sortes (fair vs biased lottery) |
| **Advanced** | Economy + M6 | +30 min | Chronos + Sortes → Base testnet vector |

Every lab prints a `Trace` — treat it as the lab's audit log. See [Reading the trace](#reading-the-trace-every-lab).

---

## Setup (10 minutes)

### Step 1 — Clone and install

The exact quickstart commands (note the `[oracles,dev]` extra — `oracles` pulls Platon/Chronos/Sortes/Aestus, `dev` pulls pytest):

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/verifiable-randomness-course
pip install -e ".[oracles,dev]"
```

**From the aicom monorepo** (recommended for contributors): the oracle packages resolve automatically via sibling paths under `oracles/` — `courselib/oracle_paths.py` walks up to the monorepo root and adds `oracles/oracles/{chronos,sortes,aestus}` and `oracles/oracles/platon/backend` to `sys.path`. No extra install needed beyond `numpy` for Platon.

```bash
cd courses/verifiable-randomness-course
pip install -e ".[oracles,dev]"
```

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** all tests pass (i18n parity across en/ru/es, randomness helpers, exercise checks).

### Step 3 — Pick a language (optional)

The lab UI strings (titles, `proof`/`verify`/`trace` labels, ticket names, audit notes) come from `i18n/{en,ru,es}.json`. Switch with `COURSE_LANG`:

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_platon_chaos.py
```

### Step 4 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/verifiable-randomness-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + `pip install -e ".[oracles,dev]"`).
3. Set `os.environ["COURSE_LANG"] = "ru"` in the setup cell if you want a localized run.
4. Run the lab cell.

---

## Module M1 — Platon chaos VRF

**Concept:** unbiasable randomness from a verifiable chaos oracle — chaos state + client seed + OS entropy, bound by an Ed25519 signature.
**Lab:** `labs/lab01_platon_chaos.py` · **Time:** ~15 min · **Prerequisites:** setup done (`numpy` + Platon)

### Steps

1. Read the docstring at the top of `labs/lab01_platon_chaos.py` (industry map: lottery, gaming).
2. Run it locally:

   ```bash
   python labs/lab01_platon_chaos.py
   ```

3. Watch the output: the `proof` scheme, the first bytes of the draw, and the `verify` result.
4. Open `courselib/randomness.py` → `chaos_draw()`: it spins up a temp-dir `Signer`, builds a chaos `state`, calls `draw_randomness(...)`, then `verify_randomness(result, public_key)`.

### Expected output (EN)

- Header line `== Chaos VRF with Platon ==`
- `proof: scheme=platon-chaos-vrf/v1`
- A signed **32-byte** draw (`result: <hex>…`)
- `verify: True`
- A `trace` block with one `chaos_draw` event (`verified=True, bytes=32`)

### Self-check

- [ ] You can explain why a client seed + signature makes the draw unbiasable
- [ ] You see the draw is **32 bytes** and `verified: True` against the public key

---

## Module M2 — Chronos VDF

**Concept:** a Wesolowski VDF proves elapsed *sequential* work on an RSA-2048 unknown-order group — proof-of-elapsed-work, not trust in a wall clock.
**Lab:** `labs/lab02_chronos_vdf.py` · **Time:** ~20 min · **Prerequisites:** M1

### Steps

1. Run `python labs/lab02_chronos_vdf.py`.
2. Read the `proof` line: the Wesolowski proof `pi` and prime `l`; `verify: True`.
3. Note the **tamper demo**: the lab re-imports `chronos.vdf` and calls `vdf.verify(g, y+1, …)` on a corrupted output — it prints `False`.
4. Open `courselib/randomness.py` → `vdf_eval()`: `hash_to_group` → `evaluate` → `prove` → `verify`. The lab uses `difficulty=700` (~700 squarings) so it runs in seconds.

### Expected output (EN)

- `proof: pi=<…>… l=<prime>`
- `verify: True`
- `tampered VDF verify: False`
- `trace` with `vdf_eval` and `tamper_check` events

### Self-check

- [ ] You can state what a VDF proves (sequential work) and what it does **not** (real time)
- [ ] You watched verification reject a tampered output

---

## Module M3 — Sortes ECVRF

**Concept:** an RFC 9381 ECVRF proof. For a fixed (public key, alpha) there is exactly **one** valid beta — the operator cannot grind for a favourable output. The proof is **80 bytes** and verifies offline, without calling the oracle again.
**Lab:** `labs/lab03_sortes_ecvrf.py` · **Time:** ~20 min · **Prerequisites:** M1

### Steps

1. Run `python labs/lab03_sortes_ecvrf.py`.
2. Confirm the proof is exactly **80 bytes** (`80 bytes = <hex>…`).
3. Note `beta` (the verifiable random output) and `verify: True`.
4. Open `courselib/randomness.py` → `ecvrf_draw()`: `sk_to_pk` → `prove(sk, alpha)` → `verify(pk, alpha, pi)`.

### Expected output (EN)

- `proof: 80 bytes = <hex>…`
- `result: beta=<hex>…`
- `verify: True`
- `trace` with one `ecvrf` event (`proof_len=80, verified=True`)

### Self-check

- [ ] You can explain "one beta per (pk, alpha)" and why that blocks grinding
- [ ] You verified the proof is **80 bytes** (this is the offline-verify number from the tagline)

---

## Module M4 — Aestus time-lock

**Concept:** an RSW time-lock puzzle. Seal a value now; anyone can open it only after `T` sequential squarings — encrypt now, decrypt after a provable delay. The building block for sealed bids and commit-reveal where no one should peek early.
**Lab:** `labs/lab04_aestus_timelock.py` · **Time:** ~20 min · **Prerequisites:** M2

### Steps

1. Run `python labs/lab04_aestus_timelock.py`.
2. Watch the seal → open roundtrip: `T=350` squarings, then the opened payload and `verify: True`.
3. Open `courselib/randomness.py` → `timelock_seal()`: `rsw.seal(message, T=...)` → `rsw.open_puzzle(puzzle)`; `message_match` confirms the plaintext came back intact.

### Expected output (EN)

- `proof: T=350 squarings`
- `result: <opened payload>` (the sealed-bid string)
- `verify: True`
- `trace` with one `timelock` event (`T=350, opened=True`)

### Self-check

- [ ] You can explain why a time-lock hides a value without a trusted third party
- [ ] You saw the sealed message recovered after `T` squarings

---

## Module M5 — Commit–reveal & bias attacks

**Concept:** the payoff module. Build a lottery a dishonest operator can grind, demonstrate the bias, then replace the draw with a Sortes ECVRF the operator **cannot** grind.
**Lab:** `labs/lab05_commit_reveal.py` · **Time:** ~25 min · **Track:** economy · **Prerequisites:** M3

### Steps

1. Run `python labs/lab05_commit_reveal.py`.
2. Compare the two tickets: `biased ticket` vs `fair VRF ticket`. The `verify VRF: True` line proves the fair draw carries a verifiable proof.
3. Read the **audit note** the lab prints: *"Fair draw binds one beta per seed — operator cannot grind."*
4. Open `courselib/randomness.py` → `BiasedLottery` (loops up to 200 attempts grinding `operator_secret|player_seed|attempt` for a jackpot) vs `FairLottery` (one ECVRF draw → one ticket, no grinding possible).

### Expected output (EN)

- `biased ticket: <n>` and `fair VRF ticket: <n>`
- `verify VRF: True`
- The audit note line
- `trace` with `commit` and `draw` events (`vrf_ok=True`)

### Self-check

- [ ] You can describe the grinding attack the `BiasedLottery` performs
- [ ] You can explain why `FairLottery` (one beta per seed) is immune

---

## Module M6 — On-chain verification

**Concept:** package the proofs for an on-chain consumer — a Wesolowski VDF vector shaped for a Solidity verifier, plus a 32-byte lottery word derived from a Sortes ECVRF beta.
**Lab:** `labs/lab06_onchain_consumer.py` · **Time:** ~20 min · **Track:** advanced · **Prerequisites:** M2, M3

### Steps

1. Run `python labs/lab06_onchain_consumer.py`.
2. Note the `protocol: wesolowski-vdf` line, `verify: True`, and the 32-byte `lottery word: 0x…`.
3. Open `courselib/randomness.py` → `onchain_vdf_vector()` (emits `scheme/seed/difficulty/y/pi/l/valid` as strings ready to feed a verifier) and `lottery_word_from_vrf()` (takes the first 32 bytes of the ECVRF beta).
4. **Bridge:** the lab prints a deploy note pointing at [lottery/docs/deployments-base.md](https://github.com/alexar76/lottery/blob/main/docs/deployments-base.md) for the live `ChronosVDF.sol` verifier on Base.

### Expected output (EN)

- `protocol: wesolowski-vdf`
- `verify: True`
- `lottery word: 0x<hex>…`
- The deploy note line
- `trace` with `onchain_vdf` and `lottery_word` events

### Self-check

- [ ] You can name the two artifacts an on-chain consumer needs (VDF vector + VRF word)
- [ ] You know where to find the Base deployment docs

---

## Reading the trace (every lab)

**Concept:** every lab logs a small `Trace` (see `courselib/trace.py`) so agent/oracle behaviour is inspectable, not magic.

### Steps (repeat after each lab)

1. Scroll to the `trace (<n> events):` block at the bottom of the lab output.
2. Read each event dict — `kind` plus the fields the lab logged (e.g. `chaos_draw` → `verified, bytes`; `vdf_eval` → `difficulty, valid`; `tamper_check` → `valid=False`).
3. Map each event to a line you saw in stdout above it. The trace is the lab's "unit-test log" for verifiable randomness.

### Self-check

- [ ] You can point to the one event that proves a draw verified
- [ ] In M2 you can find the `tamper_check` event that shows `valid=False`

---

## Exercises & certificate

After the labs, run the DIY checks. Each module has a self-contained exercise in `courselib/exercises.py` (e.g. M2 tampers a VDF and asserts verify fails; M3 asserts the proof is exactly 80 bytes; M5 asserts the fair draw verifies):

```bash
python labs/run_exercises.py                       # run all six, prints ✓/✗ per module
python labs/run_exercises.py --module m3           # run just one module's check
```

When all six pass, mint your certificate:

```bash
python labs/run_exercises.py --certificate "Your Name" --lang en   # or --lang ru / es
```

This writes `certificate.html` — open it in a browser and **Print → Save as PDF**. The credential ID is derived deterministically from name + issue date (`courselib/certificate.py`). The certificate is gated on the exercises passing unless you pass `--skip-check`.

---

## Bridge: from course to the lottery on Base

**Goal:** the same proofs you produced locally are what the AIMarket `lottery/` contracts verify on Base.

| Course | Lottery on Base |
|--------|-----------------|
| M2 Chronos VDF vector | `ChronosVDF.sol` Wesolowski verifier |
| M3 Sortes ECVRF beta | 32-byte lottery word (M6 `lottery_word_from_vrf`) |
| M5 fair vs biased draw | Why the consumer uses VRF, not a trusted beacon |
| M6 `onchain_vdf_vector()` | The exact `{y, pi, l}` vector the verifier consumes |

Deployment addresses and the Solidity verifier live in [lottery/docs/deployments-base.md](https://github.com/alexar76/lottery/blob/main/docs/deployments-base.md).

---

## Self-check checklist

After the basic track you should be able to:

- [ ] Run lab01–lab04 locally (and in Colab) in EN, RU, ES
- [ ] Explain chaos VRF, VDF, ECVRF, and time-lock in one sentence each
- [ ] Show that a tampered VDF output fails verification (M2)
- [ ] State why an 80-byte ECVRF proof can be verified offline (M3)

After the economy + advanced tracks add:

- [ ] Run lab05 and describe the grinding attack + the VRF fix
- [ ] Run lab06 and produce a Base-ready VDF vector + lottery word
- [ ] `pytest -q` green and `python labs/run_exercises.py` all ✓

---

## Troubleshooting

| Issue | Fix |
| --- | --- |
| `No module named 'chronos'` | `pip install -e ".[oracles]"`, or run from the aicom monorepo |
| `No module named 'oracle_core'` | ensure `oracles/core` is on the path — automatic in the monorepo; pulled by `[oracles]` for Sortes/Platon |
| `Oracle package '…' not installed` | not in a monorepo and extra missing — install `.[oracles]` or clone next to `oracles/` |
| Platon import fails | install `numpy`; ensure `oracles/oracles/platon/backend` exists |
| Slow VDF lab | labs use ~700 squarings (M2) / `T=350` (M4) — lower difficulty in your own exercise only, not the labs |
| Empty RU/ES strings | set `COURSE_LANG=ru\|es`; check `i18n/ru.json` keys match `i18n/en.json` |
| `pytest` i18n failure | add the missing key to **all three** JSON catalogs (en/ru/es) |
| Colab old code | re-run the setup cell; pin the `main` branch |

---

## Regenerate site & notebooks

After editing labs or i18n:

```bash
python3 scripts/build_course_assets.py
```

Guides in `docs/` are hand-maintained — update EN first, then the RU/ES mirrors.
