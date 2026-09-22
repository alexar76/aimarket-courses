# Guide pas à pas du cours

> **Public :** développeurs et opérateurs qui branchent des capteurs du monde physique sur GAIA / ATLAS avant de facturer des SKU Hub.  
> **Langues :** `COURSE_LANG=en|ru|es|fr|zh` · chaînes UI dans `i18n/` · ce guide en français.  
> **English :** [step-by-step.md](./step-by-step.md) · **Русский :** [step-by-step.ru.md](./step-by-step.ru.md) · **Español :** [step-by-step.es.md](./step-by-step.es.md) · **中文 :** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Pourquoi ce cours

GAIA expose des lectures IoT attestées comme capacités (`gaia.weather.read@v1`, `gaia.fleet.status@v1`, …). ATLAS transforme la même flotte en carte opérateur (`atlas.nearest.read@v1`). La difficulté n’est pas HTTP : c’est l’**honnêteté** (Open-Meteo ≠ station in-situ ; SIM ≠ LIVE) et la **licence** (seulement CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY sur le rail commercial). Ce cours enseigne les deux via des labs sur le sandbox live :

| Service | URL |
|---------|-----|
| GAIA | https://iot.modelmarket.dev |
| ATLAS | https://atlas.modelmarket.dev |

Les labs appellent les API live si le réseau est disponible ; hors ligne ils affichent `[offline]` et **n’inventent jamais de lectures**.

Docs canoniques : [LIVE-RELAYS.md](https://github.com/alexar76/gaia/blob/main/docs/LIVE-RELAYS.md) · [add-gaia-atlas-sensor.md](https://github.com/alexar76/aicom/blob/main/docs/add-gaia-atlas-sensor.md)

---

## Table des matières

1. [Choisir sa piste](#choisir-sa-piste)
2. [Installation (10 minutes)](#installation-10-minutes)
3. [Module M1 — Qu’est-ce qu’un relais LIVE](#module-m1--quest-ce-quun-relais-live)
4. [Module M2 — Licence et rail commercial](#module-m2--licence-et-rail-commercial)
5. [Module M3 — Flotte et honnêteté des pins](#module-m3--flotte-et-honnêteté-des-pins)
6. [Module M4 — Carte opérateur ATLAS](#module-m4--carte-opérateur-atlas)
7. [Module M5 — Capstone : ajouter un capteur](#module-m5--capstone--ajouter-un-capteur)
8. [Exercices et certificat](#exercices-et-certificat)
9. [Auto-contrôle](#auto-contrôle)
10. [Dépannage](#dépannage)

---

## Choisir sa piste

| Piste | Modules | Durée | Réseau |
|-------|---------|-------|--------|
| **Basique** | M1 → M2 → M3 → M4 | ~2 h | Optionnel |
| **Avancée** | Basique + M5 | +30 min | Comptage live optionnel |
| **Pont ops** | Après M5 | +30 min | GAIA + ATLAS + Recipe A |

---

## Installation (10 minutes)

### Étape 1 — Cloner et installer

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

**Depuis le monorepo aicom :**

```bash
cd courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

### Étape 2 — Vérifier les tests

```bash
pytest -q
```

**Attendu :** parité i18n (5 langues), tests licence/honesty, solutions d’exercices, smoke d’imports. Les tests réseau sont ignorés si GAIA est injoignable ou `COURSE_SKIP_NETWORK=1`.

### Étape 3 — Langue (optionnel)

```bash
export COURSE_LANG=fr
python labs/lab01_live_vs_sim.py
```

### Étape 4 — Endpoints live

```bash
export COURSE_GAIA_URL=https://iot.modelmarket.dev
export COURSE_ATLAS_URL=https://atlas.modelmarket.dev
```

---

## Module M1 — Qu’est-ce qu’un relais LIVE

**Concept :** allowlist HTTPS, offline en cas d’échec, ne jamais inventer de lectures.  
**Lab :** `labs/lab01_live_vs_sim.py` · **Durée :** ~20 min

### Étapes

1. Lire la docstring — paire `om-wx-01` (LIVE) vs `ws-01` (SIM).
2. Lancer `python labs/lab01_live_vs_sim.py`.
3. Confirmer que `classify_mode` passe hors ligne.
4. En ligne : inspecter `/health` et l’invoke weather.
5. Parcourir `courselib/sensors.py`.

### Auto-contrôle

- [ ] LIVE seulement si `source` est défini sur le device de flotte
- [ ] Vous n’étiquetteriez pas `ws-01` comme LIVE

---

## Module M2 — Licence et rail commercial

**Concept :** CC0 / CC BY / OGL / PD uniquement.  
**Lab :** `labs/lab02_licence_gate.py` · **Durée :** ~20 min

### Étapes

1. Lancer le lab et lire le tableau pass/fail.
2. **Pass :** OpenAQ, USGS/NWS PD, Safecast CC0, FIRMS, UK OGL.
3. **Fail :** AirNow (assent requis), OpenSky, ADSBx, PurpleAir, BY-NC.

### Auto-contrôle

- [ ] Vous citez les familles de licence du pass-bar
- [ ] AirNow est Hold, pas « presque en prod »

---

## Module M3 — Flotte et honnêteté des pins

**Concept :** Open-Meteo ≠ station ; AIS public ≠ edge propre.  
**Lab :** `labs/lab03_honesty_claims.py` · **Durée :** ~20 min

### Auto-contrôle

- [ ] Vous rejetez « Open-Meteo = station in-situ »
- [ ] Politique offline honnête = fail-loud, pas de débit

---

## Module M4 — Carte opérateur ATLAS

**Concept :** nearest, distance, mode/source.  
**Lab :** `labs/lab04_atlas_map_read.py` · **Durée :** ~20 min

### Étapes

1. Assert hors ligne sur la forme du payload.
2. En ligne : `atlas.nearest.read@v1` près de Berlin (`52.52, 13.41`).
3. Vérifier `stations` sur `/health`.

---

## Module M5 — Capstone : ajouter un capteur

**Concept :** Recipe A — licence → kind → YAML → redeploy GAIA→ATLAS → honesty.  
**Lab :** `labs/lab05_add_sensor_capstone.py` · **Durée :** ~25 min

### Auto-contrôle

- [ ] Ordre de redeploy : GAIA puis ATLAS
- [ ] LIVE exige `GAIA_ENABLE_LIVE=1` et un vrai `source`

---

## Exercices et certificat

Stubs : `courselib/exercises.py` (`# YOUR CODE HERE`).  
Solutions : `courselib/exercise_solutions.py`.

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Camille Dupont" --lang fr
```

Les cases du navigateur **n’émettent pas** de certificat.

---

## Auto-contrôle

- [ ] M1 : LIVE vs SIM via `source`
- [ ] M2 : pass-bar ; AirNow Hold
- [ ] M3 : classificateur honesty
- [ ] M4 : forme nearest + lecture live
- [ ] M5 : ordre Recipe A + compte flotte
- [ ] Exercices remplis ; certificat CLI OK

---

## Dépannage

| Symptôme | Action |
|----------|--------|
| `[offline] … unreachable` | Réseau ou continuez hors ligne — la partie unitaire enseigne quand même |
| `SensorsError: HTTP …` | Vérifier `capability_id` et `device_id` |
| pytest network skip | Normal hors ligne ; retirer `COURSE_SKIP_NETWORK` pour le live |
| Tous les exercises échouent | Remplir les stubs — c’est voulu |
| Mauvaise langue | `COURSE_LANG` ∈ `en,ru,es,fr,zh` |

Variables : `COURSE_GAIA_URL`, `COURSE_ATLAS_URL`, `COURSE_LANG`, `COURSE_SKIP_NETWORK=1`.
