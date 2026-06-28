# Step-by-step course guide

> **Audience:** developers building on AIMarket Protocol v2 — federated discovery, escrow, payment channels, signed receipts, and paid agent capabilities.
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

Most "agent" tutorials stop at calling one model. This course teaches the layer above that: how an agent **finds** a capability it doesn't own, **pays** for it without a per-call blockchain transaction, **trusts** the result via a signed receipt, and how a provider **publishes** a metered API other agents can buy. That is the AIMarket Protocol v2 economy — discovery, escrow, channels, reputation, monetization — and you build a working slice of it end to end.

Every lab runs against an **embedded hub-lite** (an in-process FastAPI hub) so the economic flow is real HTTP, not a mock — but with **zero real money** and no git clones until the capstone. Each lab prints a `Trace` event log so the discover → pay → invoke → receipt story is inspectable, not magic.

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — Protocol v2 overview](#module-m1--protocol-v2-overview)
4. [Module M2 — SDK & Hub integration](#module-m2--sdk--hub-integration)
5. [Module M3 — Escrow & payment channels](#module-m3--escrow--payment-channels)
6. [Module M4 — Reputation & trust](#module-m4--reputation--trust)
7. [Module M5 — Publish a capability](#module-m5--publish-a-capability)
8. [Module M6 — Capstone: paid agent loop (advanced)](#module-m6--capstone-paid-agent-loop-advanced)
9. [Exercises & certificate](#exercises--certificate)
10. [Observability in every lab](#observability-in-every-lab)
11. [Bridge: from course to production hub](#bridge-from-course-to-production-hub)
12. [Self-check checklist](#self-check-checklist)
13. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Deps | Hub |
|-------|---------|------|------|-----|
| **Hub-lite** | M1 → M5 | ~2 h | `[hub-lite,dev]` | Embedded hub-lite (in-process) |
| **Advanced** | Hub-lite + M6 | +1 h | `[sandbox,dev]` | Full AIMarket Hub + `aimarket-agent` SDK |
| **Production** | After M5 or M6 | +30 min | Your keys | Real federation hub |

Labs M1–M5 only need `[hub-lite]` (~5 MB, pure pip wheels). The capstone M6 adds the `[sandbox]` extra (~50 MB, git clones the `aimarket-agent` SDK and `aimarket-hub`). Read **Observability** after every lab — each script prints a `Trace` you can inspect.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/agent-economy-course
pip install -e ".[hub-lite,dev]"
```

For the capstone (M6) add the sandbox extra:

```bash
pip install -e ".[sandbox,dev]"
```

Requires **Python 3.11+**. When developing inside the `aicom` monorepo, the sandbox auto-discovers sibling `aimarket-agent/` and `aimarket-hub/` packages — no git clone needed locally.

### Step 2 — Verify tests

```bash
pytest -q
```

In the monorepo, run from the course directory with `PYTHONPATH` set:

```bash
cd courses/agent-economy-course
PYTHONPATH=. python3 -m pytest -q
```

**Expected:** protocol, hub-lite, trust, exercises, and i18n parity tests pass. The economy/capstone tests run only when the `aimarket-agent` SDK is importable; otherwise they skip cleanly.

### Step 3 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_protocol_overview.py
```

`COURSE_LANG` switches every lab's printed strings (titles, field labels, hints) using the `i18n/{en,ru,es}.json` catalogs. Code, capability IDs, and commands stay identical.

### Step 4 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/agent-economy-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + pip).
3. Set `os.environ["COURSE_LANG"] = "ru"` in the setup cell if needed.
4. Run the lab cell.

---

## Module M1 — Protocol v2 overview

**Concept:** Capabilities, receipts, and federated discovery all start at `/.well-known/ai-market.json`.
**Lab:** `labs/lab01_protocol_overview.py` · **Time:** ~15 min · **Prerequisites:** setup done

### Steps

1. Open `labs/lab01_protocol_overview.py` and read the module docstring (industry map: agent protocols).
2. Run locally:

   ```bash
   python labs/lab01_protocol_overview.py
   ```

3. Watch what the lab does:
   - Boots the embedded hub-lite in-process (~2 s).
   - Fetches `/.well-known/ai-market.json` and validates it with `validate_well_known`.
   - Fetches the manifest and validates it with `validate_manifest`.
   - Prints a sample tool's name and `price_per_call_usd`.
4. Read `courselib/protocol.py` — structural validation aligned with the `aimarket-protocol/schemas/` shapes.

### Expected output (EN)

- Header line `== Protocol v2 overview ==`
- `hub:` and `protocol:` lines from the well-known
- `well-known valid: yes` and `manifest valid: yes`
- A `trace` block with `well_known` and `manifest` events

### Self-check

- [ ] You can name the discovery entry point (`/.well-known/ai-market.json`)
- [ ] You know what `validate_well_known` vs `validate_manifest` each check

**Exercise (M1):** add a field check to `validate_well_known` — `python labs/run_exercises.py --module m1`

---

## Module M2 — SDK & Hub integration

**Concept:** Register, discover, and invoke a paid capability across a real hub; receive a signed receipt.
**Lab:** `labs/lab02_hub_discover.py` · **Time:** ~20 min · **Prerequisites:** M1

### Steps

1. Run `python labs/lab02_hub_discover.py`.
2. Follow the flow:

   ```
   discover("translate") → invoke(prod-translate, translate.multi@v2) → receipt
   ```

3. Read the printed fields: `success`, `price`, `served by`, and the receipt `nonce`. This mirrors a production federation call without cloning `aimarket-hub`.
4. Confirm the `discover` and `invoke` events appear in the trace block.

### Self-check

- [ ] Discovery returns capability metadata (`product_id`/`capability_id`, price)
- [ ] Invoke returns a structured result plus a receipt with a nonce

**Exercise (M2):** discover `summarize` and invoke it — `python labs/run_exercises.py --module m2`

---

## Module M3 — Escrow & payment channels

**Concept:** Hold funds until delivery; stream micropayments without a per-call on-chain transaction.
**Lab:** `labs/lab03_escrow_channel.py` · **Time:** ~20 min · **Prerequisites:** M2

### Steps

1. Run `python labs/lab03_escrow_channel.py`.
2. Follow the lifecycle:
   - **Open** a pre-funded channel with `budget_usd=0.25`.
   - **Invoke** `summarize@v1` through it.
   - **Close** the channel and inspect `spent` vs `refund`.
3. Note the two ideas:
   - **Payment channel** — batch micropayments without per-call on-chain txs.
   - **Escrow** — funds held until delivery; unused budget refunded on close.

Hub-lite exposes `/ai-market/v2/channel/open` and `/close` for teaching the pattern. The full SDK cycle in M6 uses the real hub escrow stack.

### Self-check

- [ ] You can name the lifecycle: open → invoke → close → refund
- [ ] A channel amortizes many calls against one funded budget vs a per-call 402

**Exercise (M3):** open a `$1.00` channel and close it — `python labs/run_exercises.py --module m3`

---

## Module M4 — Reputation & trust

**Concept:** Signed receipts make paid agent calls verifiable and feed a LUMEN-style reputation graph.
**Lab:** `labs/lab04_reputation_trust.py` · **Time:** ~25 min · **Prerequisites:** M2

### Steps

1. Run `python labs/lab04_reputation_trust.py`.
2. Watch two verifications:
   - A genuine receipt verifies `True` and **raises** the product's trust score.
   - A `tamper_receipt(..., price_usd=0.0)` copy verifies `False` and **lowers** it.
3. Read the building blocks:
   - `courselib.trust.sign_receipt` / `verify_receipt` — HMAC-SHA256 teaching receipts (stdlib, same idea as production).
   - `TrustGraph` — in-memory LUMEN-style score bumps.
   - Hub `/ai-market/v2/trust/record` — the federated trust hook demo.

### Self-check

- [ ] You can explain why a tampered price fails verification
- [ ] You see how verified vs tampered calls move the trust score in opposite directions

**Exercise (M4):** sign your own receipt with a custom secret and verify it — `python labs/run_exercises.py --module m4`

---

## Module M5 — Publish a capability

**Concept:** Ship a metered API other agents can buy — the **provider** side of the economy.
**Lab:** `labs/lab05_publish_capability.py` · **Time:** ~20 min · **Prerequisites:** M2

### Steps

1. Run `python labs/lab05_publish_capability.py`.
2. Follow the provider workflow:
   - `register_capability("prod-course", "sentiment.metered@v1", 0.007, ...)`.
   - Re-fetch the manifest and watch the tool count grow (`before → after`).
   - `discover("sentiment")` finds the new capability.
   - `invoke` it as a consumer and read the price + receipt nonce.
3. Confirm `register`, `manifest`, `discover`, and `invoke` events in the trace.

### Self-check

- [ ] You can register a capability with a price and a description
- [ ] You can prove it is discoverable and invocable after registration

**Exercise (M5):** register a custom capability and invoke it — `python labs/run_exercises.py --module m5`

---

## Module M6 — Capstone: paid agent loop (advanced)

**Concept:** A full autonomous `hire()` cycle via the real `aimarket-agent` SDK.
**Lab:** `labs/lab06_paid_capability_capstone.py` · **Time:** ~45 min · **Prerequisites:** `[sandbox]` (~50 MB, install once)

### Steps

1. Install the sandbox extra once (Colab: reuse the session if earlier labs already ran it):

   ```bash
   pip install -e ".[sandbox,dev]"
   ```

2. Run `python labs/lab06_paid_capability_capstone.py`.
3. Follow the full cycle:

   ```
   discover → open channel → invoke → signed receipt → settle → bill of materials
   ```

   The lab boots a local AIMarket Hub + stub Factory in background threads, then calls `econ.hire("translate text to multiple languages")` with a `$3.00` budget. **Zero real money.**
4. Read the printed bill of materials: task, success, channel ID, total spent, protocol version, per-step capabilities, and live ACEX listings.

> If the `aimarket-agent` SDK is **not** installed, the lab detects this via `sdk_available()` and skips cleanly with a hint — it does not crash. Labs 1–5 and all exercises run without it.

### Self-check

- [ ] You can name the full cycle: discover → channel → invoke → receipt → settle
- [ ] You understand the capstone is the only lab needing `[sandbox]`

**Exercise (M6):** run the full `hire()` cycle in the sandbox, or the paid-invoke check via hub-lite — `python labs/run_exercises.py --module m6`

---

## Exercises & certificate

Each module maps 1:1 to a self-contained DIY check (`m1`…`m6`). Run one:

```bash
python labs/run_exercises.py --module m3
```

Run all of them:

```bash
python labs/run_exercises.py
```

Each prints `✓` or `✗` per module. When **all six** pass, generate a certificate:

```bash
python labs/run_exercises.py --certificate "Jane Doe" --lang en   # or ru / es
```

This writes `certificate.html` — open it in a browser and **Print → Save as PDF** for a PDF copy. The credential ID is a SHA-256 digest derived from your name + the issue date, and the certificate labels and module badges are localized for `en`/`ru`/`es`.

---

## Observability in every lab

Each lab builds a `courselib.orchestration.Trace` and prints it at the end. The event kinds you will see:

- `well_known`, `manifest`, `discover`, `invoke`
- `channel_open`, `channel_close`
- `verify`, `register`
- `hire`, `step`, `capital` (capstone only)

Read the trace block to follow the **economic story** — discover → pay → invoke → receipt → settle — not just the final result. Treat it as the lab's "unit test log": one failed invoke maps to one trace event you can point at.

For the production path, the full factory wires OpenTelemetry + LangSmith — see [observability-langsmith.md](https://github.com/alexar76/aicom/blob/main/docs/observability-langsmith.md) (not required for the course).

---

## Bridge: from course to production hub

Graduate path once the labs feel familiar:

1. Set `COURSE_HUB_URL=https://modelmarket.dev` (or your own hub).
2. Use `courselib.economy.connect()` instead of `embedded_sandbox()`.
3. The same SDK methods carry over: `discover`, `invoke`, `hire`.

Fetch a live well-known and compare it to the validator you used in M1:

```bash
curl https://modelmarket.dev/.well-known/ai-market.json
```

Run it through `courselib.protocol.validate_well_known` — the same structural checks you learned in Module M1 apply to a real hub.

---

## Self-check checklist

- [ ] `pytest -q` passes locally
- [ ] Ran lab01–lab05 on the `[hub-lite]` track
- [ ] Ran lab06 with `[sandbox]` (or saw the clean skip until deps are installed)
- [ ] All six exercises pass: `python labs/run_exercises.py`
- [ ] Tried at least one lab in `COURSE_LANG=ru` or `es`
- [ ] Read a trace block and can explain discover → invoke → receipt
- [ ] Generated a certificate with `--certificate "Your Name"`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: fastapi` (or `uvicorn`/`httpx`) | Install the hub-lite extras: `pip install -e ".[hub-lite,dev]"` |
| `ModuleNotFoundError: aimarket_agent` | Lab 6 and economy tests need the sandbox stack: `pip install -e ".[sandbox,dev]"`. In the monorepo, ensure `aimarket-agent/` and `aimarket-hub/` exist as sibling directories. |
| Capstone prints "Capstone skipped" | Expected when the SDK is absent — install `[sandbox]` and re-run. Not an error. |
| Hub-lite timeout on first run | Cold start takes ~2–5 s; re-run once. CI waits for `/.well-known/ai-market.json`. |
| Capital listings 500 in sandbox | Ensure `AIFACTORY_DATA_ROOT` points inside the temp sandbox dir — `embedded_sandbox()` sets this automatically. |
| `ModuleNotFoundError: courselib` | Run from the repo root; labs prepend the parent dir to `sys.path`. |
| i18n key shows as `modules.m1.title` | Missing translation — check `i18n/en.json` key parity (enforced by `tests/test_i18n.py`). |
| Colab running stale code | Re-run the setup cell; pin the `main` branch. |

**Factory issues:** [FAQ.md](https://github.com/alexar76/aicom/blob/main/docs/FAQ.md)

---

## Regenerate site & notebooks

After editing labs or i18n catalogs:

```bash
python3 scripts/build_course_assets.py
```

Guides in `docs/` are hand-maintained — update EN first, then mirror to RU/ES.

---

**Next:** explore the [AIMarket Protocol spec](https://github.com/alexar76/aimarket-protocol/blob/main/spec.md) and wire your own metered capability on a real hub.
