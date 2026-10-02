# Pas à pas — PQC · Signature hybride

> **Langues :** `COURSE_LANG=en|ru|es|fr|zh` · [EN](./step-by-step.md) · [RU](./step-by-step.ru.md) · [ES](./step-by-step.es.md) · [ZH](./step-by-step.zh.md)

## Pourquoi ce cours

Les signatures portent sur le **passé**. Un reçu contesté dans des années doit déjà résister à un adversaire quantique. Remplacer Ed25519 par ML-DSA seul casse l'interop aujourd'hui. Le hub AIMarket publie l'**hybride** : Ed25519 + ML-DSA-65 — LIVE : [`modelmarket.dev/.well-known/ai-market.json`](https://modelmarket.dev/.well-known/ai-market.json). Jamais présenter du SIM comme LIVE.

## Installation

```bash
pip install -e ".[dev]"
pip install -e ".[pqc,dev]"   # optionnel
pytest -q
COURSE_LANG=fr python labs/lab01_why_hybrid.py
```

Sans dilithium : Ed25519 se vérifie ; l'enveloppe LIVE s'inspecte ; la signature PQ est marquée skipped — jamais de faux succès.

## Modules

| Module | Lab | Idée |
| --- | --- | --- |
| M1 | `lab01_why_hybrid` | Pourquoi l'hybride ; LIVE optionnel |
| M2 | `lab02_key_identity` | Identité duale ; épingler les deux clés |
| M3 | `lab03_sign_receipt` | Signer un reçu |
| M4 | `lab04_verify_offline` | Vérifier hors ligne |
| M5 | `lab05_hybrid_gate_capstone` | `refuse_single_orbit` (phase 3) |

## Exercices

Remplir `# YOUR CODE HERE` dans `courselib/exercises.py` → `python labs/run_exercises.py` → `--certificate "Votre Nom"`.

## Checklist

- [ ] Downgrade sans `require_pq` compris
- [ ] Vérif classique hors ligne OK
- [ ] La porte refuse le single-orbit
- [ ] LIVE inspecté sans le nommer SIM
