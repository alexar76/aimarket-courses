# Guía paso a paso del curso

> **Audiencia:** desarrolladores y operadores que conectan sensores del mundo físico a GAIA / ATLAS antes de cobrar SKUs del Hub.  
> **Idiomas:** `COURSE_LANG=en|ru|es|fr|zh` · cadenas UI en `i18n/` · esta guía en español.  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Por qué este curso

GAIA expone lecturas IoT atestadas como capacidades (`gaia.weather.read@v1`, `gaia.fleet.status@v1`, …). ATLAS convierte la misma flota en un mapa de operador (`atlas.nearest.read@v1`). Lo difícil no es HTTP: es la **honestidad** (Open-Meteo ≠ estación in-situ; SIM ≠ LIVE) y la **licencia** (solo CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY en el riel comercial). Este curso enseña ambas con labs contra el sandbox en vivo:

| Servicio | URL |
|----------|-----|
| GAIA | https://iot.modelmarket.dev |
| ATLAS | https://atlas.modelmarket.dev |

Los labs llaman APIs live si hay red; offline imprimen `[offline]` y **nunca inventan lecturas**.

Docs canónicos: [LIVE-RELAYS.md](https://github.com/alexar76/gaia/blob/main/docs/LIVE-RELAYS.md) · [add-gaia-atlas-sensor.md](https://github.com/alexar76/aicom/blob/main/docs/add-gaia-atlas-sensor.md)

---

## Índice

1. [Elige tu pista](#elige-tu-pista)
2. [Setup (10 minutos)](#setup-10-minutos)
3. [Módulo M1 — Qué es un relé LIVE](#módulo-m1--qué-es-un-relé-live)
4. [Módulo M2 — Licencia y riel comercial](#módulo-m2--licencia-y-riel-comercial)
5. [Módulo M3 — Flota y honestidad de pines](#módulo-m3--flota-y-honestidad-de-pines)
6. [Módulo M4 — Mapa de operador ATLAS](#módulo-m4--mapa-de-operador-atlas)
7. [Módulo M5 — Capstone: añadir un sensor](#módulo-m5--capstone-añadir-un-sensor)
8. [Ejercicios y certificado](#ejercicios-y-certificado)
9. [Autocomprobación](#autocomprobación)
10. [Solución de problemas](#solución-de-problemas)

---

## Elige tu pista

| Pista | Módulos | Tiempo | Red |
|-------|---------|--------|-----|
| **Básica** | M1 → M2 → M3 → M4 | ~2 h | Opcional |
| **Avanzada** | Básica + M5 | +30 min | Conteo live opcional |
| **Puente ops** | Tras M5 | +30 min | GAIA + ATLAS + Recipe A |

---

## Setup (10 minutos)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

**Desde el monorepo aicom:**

```bash
cd courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

### Paso 2 — Verificar tests

```bash
pytest -q
```

**Esperado:** paridad i18n (5 idiomas), tests de licence/honesty, solutions de ejercicios, smoke de imports. Los tests de red se omiten si GAIA no responde o `COURSE_SKIP_NETWORK=1`.

### Paso 3 — Idioma (opcional)

```bash
export COURSE_LANG=es
python labs/lab01_live_vs_sim.py
```

### Paso 4 — Endpoints live

```bash
export COURSE_GAIA_URL=https://iot.modelmarket.dev
export COURSE_ATLAS_URL=https://atlas.modelmarket.dev
```

---

## Módulo M1 — Qué es un relé LIVE

**Concepto:** allowlist HTTPS, offline ante fallo, nunca inventar lecturas.  
**Lab:** `labs/lab01_live_vs_sim.py` · **Tiempo:** ~20 min

### Pasos

1. Lee el docstring — par `om-wx-01` (LIVE) vs `ws-01` (SIM).
2. Ejecuta `python labs/lab01_live_vs_sim.py`.
3. Confirma que `classify_mode` pasa offline.
4. Online: revisa `/health` e invoke de weather.
5. Revisa `courselib/sensors.py`.

### Autocomprobación

- [ ] LIVE solo si `source` está definido en el dispositivo de flota
- [ ] No etiquetarías `ws-01` como LIVE

---

## Módulo M2 — Licencia y riel comercial

**Concepto:** solo CC0 / CC BY / OGL / PD.  
**Lab:** `labs/lab02_licence_gate.py` · **Tiempo:** ~20 min

### Pasos

1. Ejecuta el lab y lee la tabla pass/fail.
2. **Pass:** OpenAQ, USGS/NWS PD, Safecast CC0, FIRMS, UK OGL.
3. **Fail:** AirNow (requiere assent), OpenSky, ADSBx, PurpleAir, BY-NC.

### Autocomprobación

- [ ] Recuerdas las familias de licencia del pass-bar
- [ ] AirNow es Hold, no «casi en prod»

---

## Módulo M3 — Flota y honestidad de pines

**Concepto:** Open-Meteo ≠ estación; AIS público ≠ edge propio.  
**Lab:** `labs/lab03_honesty_claims.py` · **Tiempo:** ~20 min

### Autocomprobación

- [ ] Rechazas «Open-Meteo es estación in-situ»
- [ ] Offline honesto = fail-loud, sin debit

---

## Módulo M4 — Mapa de operador ATLAS

**Concepto:** nearest, distance, mode/source.  
**Lab:** `labs/lab04_atlas_map_read.py` · **Tiempo:** ~20 min

### Pasos

1. Assert offline de forma del payload.
2. Online: `atlas.nearest.read@v1` cerca de Berlín (`52.52, 13.41`).
3. Revisa `stations` en `/health`.

---

## Módulo M5 — Capstone: añadir un sensor

**Concepto:** Recipe A — licence → kind → YAML → redeploy GAIA→ATLAS → honesty.  
**Lab:** `labs/lab05_add_sensor_capstone.py` · **Tiempo:** ~25 min

### Autocomprobación

- [ ] Orden de redeploy: GAIA luego ATLAS
- [ ] LIVE exige `GAIA_ENABLE_LIVE=1` y un `source` real

---

## Ejercicios y certificado

Stubs: `courselib/exercises.py` (`# YOUR CODE HERE`).  
Soluciones: `courselib/exercise_solutions.py`.

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Ana García" --lang es
```

Las casillas del navegador **no** emiten certificado.

---

## Autocomprobación

- [ ] M1: LIVE vs SIM por `source`
- [ ] M2: pass-bar; AirNow Hold
- [ ] M3: clasificador de honesty
- [ ] M4: forma nearest + lectura live
- [ ] M5: orden Recipe A + conteo de flota
- [ ] Ejercicios rellenados; certificado CLI OK

---

## Solución de problemas

| Síntoma | Qué hacer |
|---------|-----------|
| `[offline] … unreachable` | Red o sigue offline — la parte unitaria sigue enseñando |
| `SensorsError: HTTP …` | Revisa `capability_id` y `device_id` |
| pytest network skip | Normal offline; quita `COURSE_SKIP_NETWORK` para live |
| Todos los exercises fallan | Rellena stubs — es intencional |
| Idioma incorrecto | `COURSE_LANG` ∈ `en,ru,es,fr,zh` |

Variables: `COURSE_GAIA_URL`, `COURSE_ATLAS_URL`, `COURSE_LANG`, `COURSE_SKIP_NETWORK=1`.
