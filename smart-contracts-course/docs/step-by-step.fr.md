# Guide pas à pas — Smart Contracts for Agent Lotteries

> **Public :** développeurs qui construisent sur l'écosystème AIMarket.  
> **Langues :** `COURSE_LANG=en|ru|es|fr|zh` · chaînes UI dans `i18n/`  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Pourquoi ce cours

Unbiasable draws, VDF verify, and escrow — lottery/ patterns in Python with Foundry vectors.

Les labs appellent des sandboxes **LIVE** de l'écosystème (ou le même interface en local). Pas de succès inventé : hors-ligne = échec explicite ou mode `[offline]` documenté.

---

## Installation (10 minutes)

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/smart-contracts-course
pip install -e ".[dev]"
pytest -q
export COURSE_LANG=fr
python labs/lab01_unbiasable_draw.py
```

Colab : ouvrez le [site du cours](https://alexar76.github.io/aimarket-courses/smart-contracts-course/) → **Open in Colab**.

---

## Modules

| Module | Titre | Lab |
|--------|-------|-----|
| M1 | Unbiasable lottery draw | `lab01_unbiasable_draw` |
| M2 | VDF verify on-chain | `lab02_vdf_verify` |
| M3 | Escrow & payment channels | `lab03_escrow_channel` |
| M4 | Relayer round lifecycle | `lab04_relayer_round` |
| M5 | Capstone: fair round | `lab05_lottery_capstone` |

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
