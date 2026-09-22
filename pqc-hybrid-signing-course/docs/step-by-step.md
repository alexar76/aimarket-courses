# Step-by-step — PQC · Hybrid Signing

> **Audience:** engineers migrating signing to post-quantum without breaking today's federation.
> **Languages:** `COURSE_LANG=en|ru|es|fr|zh` · catalogs in `i18n/` · this guide in English.
> **Other languages:** [RU](./step-by-step.ru.md) · [ES](./step-by-step.es.md) · [FR](./step-by-step.fr.md) · [ZH](./step-by-step.zh.md)

---

## Why this course

Signatures are statements about the **past**. A receipt disputed years from now must already resist a quantum adversary. Replacing Ed25519 with ML-DSA alone breaks interoperability today (fail-closed verifiers, young libraries). The AIMarket hub ships **hybrid**: Ed25519 + ML-DSA-65 over the same canonical — see the LIVE envelope at [`https://modelmarket.dev/.well-known/ai-market.json`](https://modelmarket.dev/.well-known/ai-market.json) (`pq_algorithm=ml-dsa-65`).

This course teaches: why hybrid, dual-orbit identity, sign a receipt, verify offline, and **refuse single-orbit** (phase 3). It never presents SIM crypto as LIVE.

---

## Setup (10 minutes)

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/pqc-hybrid-signing-course
pip install -e ".[dev]"            # cryptography>=42 required
pip install -e ".[pqc,dev]"        # optional: dilithium-py for local ML-DSA
pytest -q
```

Without `dilithium-py` you can still verify Ed25519 and inspect LIVE hybrid fields — PQ sign is labeled skipped, never faked.

```bash
export COURSE_LANG=ru   # or es|fr|zh
python labs/lab01_why_hybrid.py
PQC_COURSE_FETCH_LIVE=1 python labs/lab01_why_hybrid.py   # optional LIVE
```

---

## Module M1 — Why hybrid

**Lab:** `labs/lab01_why_hybrid.py` · ~15 min

1. Read the four bullets: classical alone, PQ alone, hybrid, downgrade.
2. Confirm `envelope_is_hybrid` is false for classical-only shapes.
3. Optional: `PQC_COURSE_FETCH_LIVE=1` — inspect LIVE hub signature; classical verified offline; PQ verified only if dilithium is installed.

**Exercise:** assert `why_hybrid_brief` keys; classical shape is not hybrid.

---

## Module M2 — Key identity

**Lab:** `labs/lab02_key_identity.py` · ~15 min

1. `HybridSigner(enable_pq=True)` prints dual public keys (or labeled PQ skip).
2. Remember: pin **both** keys out-of-band. A self-asserted PQ key is worthless against a broken classical key.

**Exercise:** assert classical key present; PQ key or `pq_skipped`.

---

## Module M3 — Sign a receipt

**Lab:** `labs/lab03_sign_receipt.py` · ~20 min

1. Sign a capability receipt over `receipt_canonical`.
2. Inspect `algorithm` / `value` and optional `pq_*`.
3. If dilithium missing: message says PQ skipped — classical signature is still real.

**Exercise:** `sign_receipt`; assert Ed25519 fields; hybrid if PQ available.

---

## Module M4 — Verify offline

**Lab:** `labs/lab04_verify_offline.py` · ~20 min

1. Verify your signed receipt with pinned keys — no hub callback.
2. Wrong message → classical fails.
3. Optional LIVE fetch verifies classical on the hub envelope offline.

**Exercise:** offline verify; never claim PQ success without dilithium.

---

## Module M5 — Capstone: hybrid gate

**Lab:** `labs/lab05_hybrid_gate_capstone.py` · ~25 min

1. `strip_pq` simulates a downgrade attack.
2. `refuse_single_orbit` **must** refuse classical-only even if Ed25519 verifies.
3. `require_pq=False` still accepts classical (migration phase).
4. Full hybrid accepted only when ML-DSA is real locally.

**Exercise:** implement the refuse path; accept hybrid only when PQ is real.

---

## Exercises & certificate

```bash
# fill # YOUR CODE HERE in courselib/exercises.py (see exercise_solutions.py)
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Your Name"
```

Browser checkboxes do **not** issue certificates.

---

## Self-check

- [ ] Explained why hybrid beats classical-only and PQ-only
- [ ] Generated dual-orbit identity (or labeled skip)
- [ ] Signed and verified a receipt offline
- [ ] Proved refuse_single_orbit blocks downgrade
- [ ] Inspected LIVE hub hybrid fields without calling them SIM

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `cryptography` ImportError | `pip install -e ".[dev]"` |
| PQ always skipped | `pip install -e ".[pqc]"` |
| Live fetch fails | offline OK — tests skip; or set `PQC_COURSE_WELL_KNOWN` |
| Exercises all fail | fill stubs; CI checks `exercise_solutions` |
