# Step-by-step course guide

> **Audience:** developers and operators wiring physical-world sensors into GAIA / ATLAS before charging Hub SKUs.  
> **Languages:** `COURSE_LANG=en|ru|es|fr|zh` · UI strings in `i18n/` · this guide in English.  
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Why this course

GAIA exposes attested IoT readings as Hub capabilities (`gaia.weather.read@v1`, `gaia.fleet.status@v1`, …). ATLAS turns the same fleet into an operator map (`atlas.nearest.read@v1`). The hard parts are not HTTP — they are **honesty** (Open-Meteo ≠ in-situ station; SIM ≠ LIVE) and **licence** (only CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY on the commercial rail). This course teaches both with runnable labs against the live sandbox:

| Service | URL |
|---------|-----|
| GAIA | https://iot.modelmarket.dev |
| ATLAS | https://atlas.modelmarket.dev |

Labs call live APIs when reachable; offline they print a clear `[offline]` line and **never invent readings**.

Canonical docs: [LIVE-RELAYS.md](https://github.com/alexar76/gaia/blob/main/docs/LIVE-RELAYS.md) · [add-gaia-atlas-sensor.md](https://github.com/alexar76/aicom/blob/main/docs/add-gaia-atlas-sensor.md)

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — What a LIVE relay is](#module-m1--what-a-live-relay-is)
4. [Module M2 — Licence & commercial rail](#module-m2--licence--commercial-rail)
5. [Module M3 — Fleet & pin honesty](#module-m3--fleet--pin-honesty)
6. [Module M4 — ATLAS operator map](#module-m4--atlas-operator-map)
7. [Module M5 — Capstone: add a sensor](#module-m5--capstone-add-a-sensor)
8. [Exercises & certificate](#exercises--certificate)
9. [Self-check checklist](#self-check-checklist)
10. [Troubleshooting](#troubleshooting)

---

## Choose your track

| Track | Modules | Time | Network |
|-------|---------|------|---------|
| **Basic** | M1 → M2 → M3 → M4 | ~2 h | Optional (labs degrade offline) |
| **Advanced** | Basic + M5 capstone | +30 min | Optional live fleet count |
| **Ops bridge** | After M5 | +30 min | Live GAIA + ATLAS + monorepo Recipe A |

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

**From the aicom monorepo:**

```bash
cd courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** i18n parity (5 langs), licence/honesty unit tests, exercise solutions, lab smoke imports. Network tests skip automatically when GAIA is unreachable or `COURSE_SKIP_NETWORK=1`.

### Step 3 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, fr, zh — default en
python labs/lab01_live_vs_sim.py
```

### Step 4 — Optional live endpoints

```bash
export COURSE_GAIA_URL=https://iot.modelmarket.dev
export COURSE_ATLAS_URL=https://atlas.modelmarket.dev
```

Defaults already point at the public sandbox.

---

## Module M1 — What a LIVE relay is

**Concept:** HTTPS allowlist, offline-on-fail, never invent readings.  
**Lab:** `labs/lab01_live_vs_sim.py` · **Time:** ~20 min

### Steps

1. Read the lab docstring — teaching pair `om-wx-01` (LIVE) vs `ws-01` (SIM).
2. Run:

   ```bash
   python labs/lab01_live_vs_sim.py
   ```

3. Confirm offline `classify_mode` asserts pass even without network.
4. When online, inspect `/health` device count and weather invoke values for both devices.
5. Skim `courselib/sensors.py` — `gaia_weather_read`, `classify_mode`, `SensorsError`.

### Expected output

- Line `== What a LIVE relay is ==` (or localized title)
- `verify: offline classify_mode LIVE/SIM — ok`
- Live lines for temperature / `fleet.source` **or** `[offline] …`

### Self-check

- [ ] LIVE iff `source` is set on the fleet device
- [ ] You would refuse to badge `ws-01` as LIVE

---

## Module M2 — Licence & commercial rail

**Concept:** CC0 / CC BY / OGL / PD only — why AirNow waits and OpenAQ ships.  
**Lab:** `labs/lab02_licence_gate.py` · **Time:** ~20 min

### Steps

1. Run the lab and read the embedded pass/fail table.
2. Note **pass:** OpenAQ, USGS/NWS PD, Safecast CC0, FIRMS, UK OGL.
3. Note **fail:** AirNow (assent required), OpenSky, ADSBx, PurpleAir, BY-NC.
4. Call `licence_gate("CC BY-NC")` mentally — must be `fail`.

### Self-check

- [ ] You can list the pass-bar licence families from memory
- [ ] You know AirNow is Hold, not “almost shipped”

---

## Module M3 — Fleet & pin honesty

**Concept:** Open-Meteo ≠ station; public AIS ≠ own-edge; warning ≠ in-situ.  
**Lab:** `labs/lab03_honesty_claims.py` · **Time:** ~20 min

### Steps

1. Run the lab — review each honesty row and its correction.
2. Online: confirm `om-wx-01` classifies LIVE and `ws-01` SIM from live fleet.
3. Fill exercise m3 stubs using `honesty_claims("om-as-station")`.

### Self-check

- [ ] You would reject “Open-Meteo is an in-situ station” in an operator UI
- [ ] Fail-loud / no-debit is the honest offline policy

---

## Module M4 — ATLAS operator map

**Concept:** Read nearest pin, distance, mode/source from the map.  
**Lab:** `labs/lab04_atlas_map_read.py` · **Time:** ~20 min

### Steps

1. Run the lab — offline shape assert first.
2. Online: `atlas.nearest.read@v1` near Berlin (`52.52, 13.41`).
3. Inspect `distance_km`, `nearest.id`, `nearest.source`, `values.temperature_c`.
4. Hit ATLAS `/health` for `stations` count.

### Self-check

- [ ] Buyers do not pass arbitrary client URLs — anchors live on the operator side
- [ ] You can explain LIVE badge from `nearest.mode` / `source`

---

## Module M5 — Capstone: add a sensor

**Concept:** Recipe A checklist — licence → kind → YAML → redeploy GAIA→ATLAS → honesty.  
**Lab:** `labs/lab05_add_sensor_capstone.py` · **Time:** ~25 min

### Steps

1. Walk the printed checklist (7 steps).
2. Online: note current `health.devices` / fleet length — after a real add, expect +1.
3. Read monorepo `docs/add-gaia-atlas-sensor.md` for Recipe A vs Recipe B.
4. Do **not** invent a new upstream in Recipe A — kind must already exist.

### Self-check

- [ ] Redeploy order is GAIA then ATLAS
- [ ] LIVE requires `GAIA_ENABLE_LIVE=1` and a real `source`

---

## Exercises & certificate

Student stubs live in `courselib/exercises.py` (`# YOUR CODE HERE`).  
Reference solutions (CI): `courselib/exercise_solutions.py`.

```bash
# after filling stubs:
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Your Name" --lang en
```

Browser checkboxes do **not** issue certificates.

---

## Self-check checklist

- [ ] M1: LIVE vs SIM from `source`
- [ ] M2: licence pass bar memorized; AirNow Hold
- [ ] M3: honesty classifier rejects station/edge confusion
- [ ] M4: nearest payload shape + live map read
- [ ] M5: Recipe A order + fleet count awareness
- [ ] Exercises filled; certificate CLI succeeds

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `[offline] … unreachable` | Check network; or continue offline — unit paths still teach |
| `SensorsError: HTTP 4xx/5xx` | Capability/input wrong — use `device_id` only on weather invoke |
| `pytest` network tests skip | Expected offline; set no `COURSE_SKIP_NETWORK` and ensure GAIA up to exercise them |
| Exercises all fail | Fill `# YOUR CODE HERE` — stubs raise `NotImplementedError` by design |
| Wrong language | `export COURSE_LANG=fr` (must be in `en,ru,es,fr,zh`) |

Env overrides: `COURSE_GAIA_URL`, `COURSE_ATLAS_URL`, `COURSE_LANG`, `COURSE_SKIP_NETWORK=1`.
