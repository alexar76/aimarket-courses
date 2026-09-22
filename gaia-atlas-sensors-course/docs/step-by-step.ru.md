# Пошаговое руководство по курсу

> **Аудитория:** разработчики и операторы, подключающие датчики физического мира к GAIA / ATLAS до выставления платных Hub SKU.  
> **Языки:** `COURSE_LANG=en|ru|es|fr|zh` · строки UI в `i18n/` · это руководство на русском.  
> **English:** [step-by-step.md](./step-by-step.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md) · **中文:** [step-by-step.zh.md](./step-by-step.zh.md)

---

## Зачем этот курс

GAIA отдаёт аттестованные IoT-показания как capability (`gaia.weather.read@v1`, `gaia.fleet.status@v1`, …). ATLAS превращает тот же флот в операторскую карту (`atlas.nearest.read@v1`). Сложность не в HTTP, а в **честности** (Open-Meteo ≠ полевая станция; SIM ≠ LIVE) и **лицензии** (на коммерческой рельсе только CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY). Курс учит обоим через лаборатории на живой песочнице:

| Сервис | URL |
|--------|-----|
| GAIA | https://iot.modelmarket.dev |
| ATLAS | https://atlas.modelmarket.dev |

Лаборатории вызывают live API при доступности; офлайн печатают `[offline]` и **никогда не выдумывают показания**.

Канон: [LIVE-RELAYS.md](https://github.com/alexar76/gaia/blob/main/docs/LIVE-RELAYS.md) · [add-gaia-atlas-sensor.md](https://github.com/alexar76/aicom/blob/main/docs/add-gaia-atlas-sensor.md)

---

## Содержание

1. [Выбор трека](#выбор-трека)
2. [Установка (10 минут)](#установка-10-минут)
3. [Модуль M1 — Что такое LIVE-реле](#модуль-m1--что-такое-live-реле)
4. [Модуль M2 — Лицензия и коммерческая рельса](#модуль-m2--лицензия-и-коммерческая-рельса)
5. [Модуль M3 — Флот и честность пинов](#модуль-m3--флот-и-честность-пинов)
6. [Модуль M4 — Операторская карта ATLAS](#модуль-m4--операторская-карта-atlas)
7. [Модуль M5 — Капстоун: добавить датчик](#модуль-m5--капстоун-добавить-датчик)
8. [Упражнения и сертификат](#упражнения-и-сертификат)
9. [Чеклист самопроверки](#чеклист-самопроверки)
10. [Устранение неполадок](#устранение-неполадок)

---

## Выбор трека

| Трек | Модули | Время | Сеть |
|------|--------|-------|------|
| **Базовый** | M1 → M2 → M3 → M4 | ~2 ч | Опционально |
| **Продвинутый** | Базовый + M5 | +30 мин | Опциональный live-счётчик флота |
| **Ops-мост** | После M5 | +30 мин | Live GAIA + ATLAS + Recipe A в монорепо |

---

## Установка (10 минут)

### Шаг 1 — Клон и установка

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

**Из монорепозитория aicom:**

```bash
cd courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

### Шаг 2 — Проверка тестов

```bash
pytest -q
```

**Ожидание:** паритет i18n (5 языков), unit-тесты licence/honesty, solutions упражнений, smoke импортов. Сетевые тесты пропускаются, если GAIA недоступен или `COURSE_SKIP_NETWORK=1`.

### Шаг 3 — Язык (опционально)

```bash
export COURSE_LANG=ru
python labs/lab01_live_vs_sim.py
```

### Шаг 4 — Live-эндпоинты

```bash
export COURSE_GAIA_URL=https://iot.modelmarket.dev
export COURSE_ATLAS_URL=https://atlas.modelmarket.dev
```

---

## Модуль M1 — Что такое LIVE-реле

**Концепт:** HTTPS-allowlist, offline при сбое, не выдумывать показания.  
**Лаборатория:** `labs/lab01_live_vs_sim.py` · **Время:** ~20 мин

### Шаги

1. Прочитайте docstring — пара `om-wx-01` (LIVE) vs `ws-01` (SIM).
2. Запустите `python labs/lab01_live_vs_sim.py`.
3. Убедитесь, что офлайн-assert `classify_mode` проходит без сети.
4. Онлайн: смотрите `/health` и weather invoke для обоих устройств.
5. Просмотрите `courselib/sensors.py`.

### Самопроверка

- [ ] LIVE только если у устройства флота задан `source`
- [ ] `ws-01` нельзя бейджить как LIVE

---

## Модуль M2 — Лицензия и коммерческая рельса

**Концепт:** только CC0 / CC BY / OGL / PD.  
**Лаборатория:** `labs/lab02_licence_gate.py` · **Время:** ~20 мин

### Шаги

1. Запустите лабораторию и разберите таблицу pass/fail.
2. **Pass:** OpenAQ, USGS/NWS PD, Safecast CC0, FIRMS, UK OGL.
3. **Fail:** AirNow (нужен assent), OpenSky, ADSBx, PurpleAir, BY-NC.

### Самопроверка

- [ ] Помните семейства лицензий pass-bar
- [ ] AirNow — Hold, не «почти зашили»

---

## Модуль M3 — Флот и честность пинов

**Концепт:** Open-Meteo ≠ станция; публичный AIS ≠ свой edge.  
**Лаборатория:** `labs/lab03_honesty_claims.py` · **Время:** ~20 мин

### Самопроверка

- [ ] Отвергаете «Open-Meteo = полевая станция»
- [ ] Честная политика офлайна — fail-loud, без debit

---

## Модуль M4 — Операторская карта ATLAS

**Концепт:** nearest, distance, mode/source.  
**Лаборатория:** `labs/lab04_atlas_map_read.py` · **Время:** ~20 мин

### Шаги

1. Офлайн-assert формы payload.
2. Онлайн: `atlas.nearest.read@v1` около Берлина (`52.52, 13.41`).
3. Смотрите `stations` в `/health`.

---

## Модуль M5 — Капстоун: добавить датчик

**Концепт:** Recipe A — licence → kind → YAML → redeploy GAIA→ATLAS → honesty.  
**Лаборатория:** `labs/lab05_add_sensor_capstone.py` · **Время:** ~25 мин

### Самопроверка

- [ ] Порядок redeploy: сначала GAIA, потом ATLAS
- [ ] LIVE требует `GAIA_ENABLE_LIVE=1` и реальный `source`

---

## Упражнения и сертификат

Заготовки: `courselib/exercises.py` (`# YOUR CODE HERE`).  
Эталон: `courselib/exercise_solutions.py`.

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Иван Петров" --lang ru
```

Галочки в браузере сертификат **не** выдают.

---

## Чеклист самопроверки

- [ ] M1: LIVE vs SIM по `source`
- [ ] M2: pass-bar; AirNow Hold
- [ ] M3: honesty-классификатор
- [ ] M4: форма nearest + live-чтение
- [ ] M5: порядок Recipe A + счётчик флота
- [ ] Упражнения заполнены; CLI-сертификат получен

---

## Устранение неполадок

| Симптом | Что делать |
|---------|------------|
| `[offline] … unreachable` | Сеть или продолжайте офлайн — unit-часть всё равно учит |
| `SensorsError: HTTP …` | Проверьте `capability_id` и `device_id` |
| Сетевые pytest skip | Норма офлайн; уберите `COURSE_SKIP_NETWORK` для live |
| Все exercises fail | Заполните stubs — так и задумано |
| Неверный язык | `COURSE_LANG` ∈ `en,ru,es,fr,zh` |

Переменные: `COURSE_GAIA_URL`, `COURSE_ATLAS_URL`, `COURSE_LANG`, `COURSE_SKIP_NETWORK=1`.
