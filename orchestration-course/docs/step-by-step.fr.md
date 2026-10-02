# Guide pas à pas — AI Agent Orchestration

> **Public :** développeurs qui construisent sur l'écosystème AIMarket.  
> **Langues :** `COURSE_LANG=en|ru|es|fr|zh` · chaînes UI dans `i18n/`  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Pourquoi ce cours

Hands-on Python course on AI agent orchestration patterns and agent economy.

Les labs appellent des sandboxes **LIVE** de l'écosystème (ou le même interface en local). Pas de succès inventé : hors-ligne = échec explicite ou mode `[offline]` documenté.

---

## Installation (10 minutes)

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/orchestration-course
pip install -e ".[dev]"
pytest -q
export COURSE_LANG=fr
python labs/lab01_agent_and_tool.py
```

Colab : ouvrez le [site du cours](https://alexar76.github.io/aimarket-courses/orchestration-course/) → **Open in Colab**.

---

## Modules

| Module | Titre | Lab |
|--------|-------|-----|
| M1 | m1 | `lab01_agent_and_tool` |
| M2 | m2 | `lab02_topologies` |
| M3 | m3 | `lab03_handoff` |
| M4 | m4 | `lab04_discover_invoke` |
| M5 | m5 | `lab05_state_context` |
| M6 | m6 | `lab06_guardrails` |
| M7 | m7 | `lab07_receipt_verify` |
| M8 | m8 | `lab08_metered_economy` |
| M9 | m9 | — |

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
