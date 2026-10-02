# Guide pas à pas

> **Public :** opérateurs de hub et builders rejoignant la fédération AIMarket.  
> **Langues :** `COURSE_LANG=en|ru|es|fr|zh` · chaînes UI dans `i18n/`.  
> **English :** [step-by-step.md](./step-by-step.md)

---

## Pourquoi ce cours

Un knock de fédération est une **observation**. Il ne doit jamais indexer le catalogue d'un inconnu. Le cours suit le chemin d'admission réel de [modelmarket.dev](https://modelmarket.dev) : well-known, porte ouverte/fermée, quarantaine preview (search/invoke ne lisent pas cette table), declared vs read, approve → crawl. Les labs préfèrent des GET publics live ; les fixtures sont étiquetées et jamais présentées comme LIVE.

---

## Parcours

| Parcours | Modules | Durée |
|----------|---------|-------|
| **Basic** | M1 → M4 | ~2 h |
| **Advanced** | + M5 | +30 min |

Chaque lab affiche un `Trace`.

---

## Installation

```bash
cd courses/federation-peer-hubs-course
pip install -e ".[hub-lite,dev]"
pytest -q
export COURSE_LANG=fr
python labs/lab01_well_known_announce.py
```

`COURSE_OFFLINE=1` = fixtures. `COURSE_LIVE=1 pytest tests/test_live_optional.py` = réseau optionnel.

---

## M1 — Well-known et announce

1. Lancez le lab 01.
2. Confirmez LIVE `/.well-known/ai-market.json` : name, compteurs, signer, signature hybride.
3. knock ≠ index.

---

## M2 — Porte ouverte vs fermée

1. Lab 02 sur `/federation/peers`.
2. Notez `door`, trusted, pending.
3. Contre-factuel porte fermée : pending peut encore exister.

---

## M3 — Quarantaine preview

1. Lab 03 ; les trois gardes de lecture à `false`.
2. File pending vide = preuve valide de la règle.

---

## M4 — Declared vs read

1. Lab 04 : comparez claims et compteurs vérifiés.
2. Pending : `declared_capabilities` vs `preview_capabilities`.
3. L'UI doit montrer **les deux**.

---

## M5 — Capstone : approuver un inconnu

1. Checklist announce → pending → preview → approve → crawl.
2. Probe live ; Approve exige un bearer admin — le lab s'arrête à l'API publique.

---

## Exercices et certificat

1. Remplissez les stubs dans `courselib/exercises.py`.
2. `python labs/run_exercises.py`
3. `python labs/run_exercises.py --certificate "Votre Nom" --lang fr`
4. CI : `COURSE_USE_SOLUTIONS=1 python labs/run_exercises.py`

Docs : [federation-admission.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-admission.md), [federation-peer-keys.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-peer-keys.md).

---

## Dépannage

| Symptôme | Correctif |
|----------|-----------|
| Réseau / HTTP | `COURSE_OFFLINE=1` ou `COURSE_HUB_URL` |
| Exercices en échec | stubs ou `COURSE_USE_SOLUTIONS=1` |
| Site obsolète | `python scripts/build_course_assets.py` |
