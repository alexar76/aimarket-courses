# Paso a paso — PQC · Firma híbrida

> **Idiomas:** `COURSE_LANG=en|ru|es|fr|zh` · [EN](./step-by-step.md) · [RU](./step-by-step.ru.md) · [FR](./step-by-step.fr.md) · [ZH](./step-by-step.zh.md)

## Por qué este curso

Las firmas hablan del **pasado**. Un recibo disputado años después ya debe resistir un adversario cuántico. Sustituir Ed25519 solo por ML-DSA rompe la interoperabilidad hoy. El hub AIMarket publica **híbrido**: Ed25519 + ML-DSA-65 — LIVE en [`modelmarket.dev/.well-known/ai-market.json`](https://modelmarket.dev/.well-known/ai-market.json). Nunca presentes SIM como LIVE.

## Instalación

```bash
pip install -e ".[dev]"
pip install -e ".[pqc,dev]"   # opcional
pytest -q
COURSE_LANG=es python labs/lab01_why_hybrid.py
```

Sin dilithium: Ed25519 se verifica; el envelope LIVE se inspecciona; la firma PQ se marca como omitida — sin inventar éxito.

## Módulos

| Módulo | Lab | Idea |
| --- | --- | --- |
| M1 | `lab01_why_hybrid` | Por qué híbrido; LIVE opcional |
| M2 | `lab02_key_identity` | Identidad dual; fijar ambas claves |
| M3 | `lab03_sign_receipt` | Firmar recibo |
| M4 | `lab04_verify_offline` | Verificar offline |
| M5 | `lab05_hybrid_gate_capstone` | `refuse_single_orbit` (fase 3) |

## Ejercicios

Rellena `# YOUR CODE HERE` en `courselib/exercises.py` → `python labs/run_exercises.py` → `--certificate "Tu Nombre"`.

## Checklist

- [ ] Entiendes el downgrade sin `require_pq`
- [ ] Verify clásico offline funciona
- [ ] La puerta rechaza single-orbit
- [ ] Inspeccionaste LIVE sin llamarlo SIM
