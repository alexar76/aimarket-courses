# Guía paso a paso

> **Audiencia:** operadores de hub y builders que se unen a la federación AIMarket.  
> **Idiomas:** `COURSE_LANG=en|ru|es|fr|zh` · cadenas UI en `i18n/`.  
> **English:** [step-by-step.md](./step-by-step.md)

---

## Por qué este curso

Un knock de federación es una **observación**. Nunca debe indexar el catálogo de un extraño. El curso sigue la admisión real de [modelmarket.dev](https://modelmarket.dev): well-known, puerta abierta/cerrada, cuarentena preview (search/invoke no leen esa tabla), declared vs read, approve → crawl. Los labs prefieren GET públicos en vivo; los fixtures están etiquetados y nunca se presentan como LIVE.

---

## Pistas

| Pista | Módulos | Tiempo |
|-------|---------|--------|
| **Basic** | M1 → M4 | ~2 h |
| **Advanced** | + M5 | +30 min |

Cada lab imprime un `Trace`.

---

## Instalación

```bash
cd courses/federation-peer-hubs-course
pip install -e ".[hub-lite,dev]"
pytest -q
export COURSE_LANG=es
python labs/lab01_well_known_announce.py
```

`COURSE_OFFLINE=1` = fixtures. `COURSE_LIVE=1 pytest tests/test_live_optional.py` = red opcional.

---

## M1 — Well-known y announce

1. Ejecuta el lab 01.
2. Confirma LIVE `/.well-known/ai-market.json`: name, conteos, signer, firma híbrida.
3. knock ≠ index.

---

## M2 — Puerta abierta vs cerrada

1. Lab 02 contra `/federation/peers`.
2. Anota `door`, trusted, pending.
3. Contrafactual con puerta cerrada: pending aún puede existir.

---

## M3 — Cuarentena preview

1. Lab 03; los tres read guards en `false`.
2. Cola pending vacía sigue siendo evidencia válida de la regla.

---

## M4 — Declared vs read

1. Lab 04: compara claims vs conteos verificados.
2. Pending: `declared_capabilities` vs `preview_capabilities`.
3. La UI debe mostrar **ambos**.

---

## M5 — Capstone: aprobar un extraño

1. Checklist announce → pending → preview → approve → crawl.
2. Probe live; Approve necesita bearer admin — el lab se detiene en la API pública.

---

## Ejercicios y certificado

1. Completa stubs en `courselib/exercises.py`.
2. `python labs/run_exercises.py`
3. `python labs/run_exercises.py --certificate "Tu Nombre" --lang es`
4. CI: `COURSE_USE_SOLUTIONS=1 python labs/run_exercises.py`

Docs: [federation-admission.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-admission.md), [federation-peer-keys.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-peer-keys.md).

---

## Solución de problemas

| Síntoma | Fix |
|---------|-----|
| Red / HTTP | `COURSE_OFFLINE=1` o `COURSE_HUB_URL` |
| Ejercicios fallan | stubs o `COURSE_USE_SOLUTIONS=1` |
| Site viejo | `python scripts/build_course_assets.py` |
