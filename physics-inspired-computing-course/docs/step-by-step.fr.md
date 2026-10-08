# Guide pas à pas — Physics-Inspired Computing for Engineers

> **Public :** développeurs qui construisent sur l'écosystème AIMarket.  
> **Langues :** `COURSE_LANG=en|ru|es|fr|zh` · chaînes UI dans `i18n/`  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Pourquoi ce cours

Consensus swarms, TSP certificates, blue-noise sampling, cascade risk, and Landauer thermodynamics.

Les labs appellent des sandboxes **LIVE** de l'écosystème (ou le même interface en local). Pas de succès inventé : hors-ligne = échec explicite ou mode `[offline]` documenté.

---

## Installation (10 minutes)

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/physics-inspired-computing-course
pip install -e ".[dev]"
pytest -q
export COURSE_LANG=fr
python labs/lab01_murmuration_consensus.py
```

Colab : ouvrez le [site du cours](https://alexar76.github.io/aimarket-courses/physics-inspired-computing-course/) → **Open in Colab**.

---

## Modules

| Module | Titre | Lab |
|--------|-------|-----|
| M1 | Murmuration consensus | `lab01_murmuration_consensus` |
| M2 | Colony TSP certificate | `lab02_colony_tsp` |
| M3 | Turing blue-noise | `lab03_turing_bluenoise` |
| M4 | Ablation cascade risk | `lab04_ablation_cascade` |
| M5 | Landauer thermodynamic audit | `lab05_landauer_audit` |

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
