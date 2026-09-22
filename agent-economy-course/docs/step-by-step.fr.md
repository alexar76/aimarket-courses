# Guide pas à pas — Build an Agent Economy from Scratch

> **Public :** développeurs qui construisent sur l'écosystème AIMarket.  
> **Langues :** `COURSE_LANG=en|ru|es|fr|zh` · chaînes UI dans `i18n/`  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Pourquoi ce cours

Publish a paid capability, collect USDC via escrow, and ship a consumer agent.

Les labs appellent des sandboxes **LIVE** de l'écosystème (ou le même interface en local). Pas de succès inventé : hors-ligne = échec explicite ou mode `[offline]` documenté.

---

## Installation (10 minutes)

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/agent-economy-course
pip install -e ".[dev]"
pytest -q
export COURSE_LANG=fr
python labs/lab01_protocol_overview.py
```

Colab : ouvrez le [site du cours](https://alexar76.github.io/aimarket-courses/agent-economy-course/) → **Open in Colab**.

---

## Modules

| Module | Titre | Lab |
|--------|-------|-----|
| M1 | Protocol v2 overview | `lab01_protocol_overview` |
| M2 | SDK & Hub integration | `lab02_hub_discover` |
| M3 | Escrow & payment channels | `lab03_escrow_channel` |
| M4 | Reputation & trust | `lab04_reputation_trust` |
| M5 | Publish a capability | `lab05_publish_capability` |
| M6 | Capstone: paid agent loop | `lab06_paid_capability_capstone` |

---

## Parcours recommandé

1. Lisez le concept dans la docstring du lab.
2. Exécutez le lab (`COURSE_LANG=fr` optionnel).
3. Complétez les stubs `# YOUR CODE` dans `courselib/exercises.py`.
4. `python labs/run_exercises.py --certificate "Votre Nom"`.

---

## Certificat

Les certificats sont **uniquement** émis par le CLI après réussite de tous les exercices — pas en cochant des cases dans le navigateur.

---

## Suite

Retournez au [portail des académies](https://alexar76.github.io/aimarket-courses/) ou à l'[School](https://edu.modelmarket.dev/) pour le clip on-ramp.
