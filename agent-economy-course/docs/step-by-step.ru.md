# Пошаговое руководство по курсу

> **Для кого:** разработчики, строящие на AIMarket Protocol v2 — федеративный поиск, эскроу, платёжные каналы, подписанные квитанции и платные capability агентов.
> **Язык лаб:** `COURSE_LANG=ru|en|es` · строки UI в `i18n/` · этот гайд на русском.
> **English:** [step-by-step.md](./step-by-step.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Зачем этот курс

Большинство туториалов про «агентов» останавливаются на вызове одной модели. Этот курс — про слой выше: как агент **находит** чужую capability, **платит** за неё без транзакции в блокчейне на каждый вызов, **доверяет** результату через подписанную квитанцию и как провайдер **публикует** платный API, который покупают другие агенты. Это и есть экономика AIMarket Protocol v2 — поиск, эскроу, каналы, репутация, монетизация — и вы собираете её рабочий срез от начала до конца.

Каждая лаба работает с **встроенным hub-lite** (FastAPI-хаб в том же процессе), поэтому экономический поток — это реальный HTTP, а не мок, но **без реальных денег** и без git-клонов вплоть до capstone. Каждая лаба печатает лог событий `Trace`, чтобы цепочка поиск → оплата → вызов → квитанция была видна, а не была магией.

---

## Содержание

1. [Выбор трека](#выбор-трека)
2. [Установка (10 минут)](#установка-10-минут)
3. [M1 — Обзор Protocol v2](#m1--обзор-protocol-v2)
4. [M2 — SDK и интеграция с Hub](#m2--sdk-и-интеграция-с-hub)
5. [M3 — Эскроу и платёжные каналы](#m3--эскроу-и-платёжные-каналы)
6. [M4 — Репутация и доверие](#m4--репутация-и-доверие)
7. [M5 — Публикация capability](#m5--публикация-capability)
8. [M6 — Capstone: платный цикл агента (продвинутый)](#m6--capstone-платный-цикл-агента-продвинутый)
9. [Упражнения и сертификат](#упражнения-и-сертификат)
10. [Наблюдаемость в каждой лабе](#наблюдаемость-в-каждой-лабе)
11. [Мост: от курса к боевому хабу](#мост-от-курса-к-боевому-хабу)
12. [Чеклист самопроверки](#чеклист-самопроверки)
13. [Типичные проблемы](#типичные-проблемы)

---

## Выбор трека

| Трек | Модули | Время | Зависимости | Hub |
|------|--------|-------|-------------|-----|
| **Hub-lite** | M1 → M5 | ~2 ч | `[hub-lite,dev]` | Встроенный hub-lite (в процессе) |
| **Продвинутый** | Hub-lite + M6 | +1 ч | `[sandbox,dev]` | Полный AIMarket Hub + SDK `aimarket-agent` |
| **Боевой** | После M5 или M6 | +30 мин | Ваши ключи | Реальный федеративный хаб |

Лабам M1–M5 нужен только `[hub-lite]` (~5 МБ, чистые pip-колёса). Capstone M6 добавляет extra `[sandbox]` (~50 МБ, git-клон SDK `aimarket-agent` и `aimarket-hub`). После каждой лабы смотрите блок `Trace`.

---

## Установка (10 минут)

### Шаг 1 — Клон и установка

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/agent-economy-course
pip install -e ".[hub-lite,dev]"
```

Для capstone (M6) добавьте extra sandbox:

```bash
pip install -e ".[sandbox,dev]"
```

Нужен **Python 3.11+**. При разработке внутри монорепы `aicom` sandbox сам находит соседние пакеты `aimarket-agent/` и `aimarket-hub/` — git-клон локально не требуется.

### Шаг 2 — Тесты

```bash
pytest -q
```

В монорепе запускайте из каталога курса с заданным `PYTHONPATH`:

```bash
cd courses/agent-economy-course
PYTHONPATH=. python3 -m pytest -q
```

**Ожидается:** проходят тесты protocol, hub-lite, trust, упражнений и паритета i18n. Тесты economy/capstone выполняются только если импортируется SDK `aimarket-agent`, иначе чисто пропускаются.

### Шаг 3 — Язык интерфейса лаб (опционально)

```bash
export COURSE_LANG=ru   # или es, по умолчанию en
python labs/lab01_protocol_overview.py
```

`COURSE_LANG` переключает все печатаемые строки лаб (заголовки, подписи полей, подсказки) по каталогам `i18n/{en,ru,es}.json`. Код, ID capability и команды остаются неизменными.

### Шаг 4 — Google Colab

1. Откройте [сайт курса](https://alexar76.github.io/aimarket-courses/agent-economy-course/) → **Open in Colab** на любой лабе.
2. Выполните setup-ячейку (clone + pip).
3. При необходимости в setup-ячейке: `os.environ["COURSE_LANG"] = "ru"`.
4. Запустите ячейку лабы.

---

## M1 — Обзор Protocol v2

**Концепция:** возможности, квитанции и федеративный поиск начинаются с `/.well-known/ai-market.json`.
**Лаба:** `labs/lab01_protocol_overview.py` · **~15 мин**

### Шаги

1. Прочитайте docstring в начале файла лабы.
2. `python labs/lab01_protocol_overview.py`
3. Что делает лаба:
   - Поднимает встроенный hub-lite в процессе (~2 с).
   - Запрашивает `/.well-known/ai-market.json` и валидирует через `validate_well_known`.
   - Запрашивает manifest и валидирует через `validate_manifest`.
   - Печатает имя примера инструмента и `price_per_call_usd`.
4. Откройте `courselib/protocol.py` — структурная валидация по формам `aimarket-protocol/schemas/`.

### Самопроверка

- [ ] Называете точку входа поиска (`/.well-known/ai-market.json`)
- [ ] Понимаете, что проверяют `validate_well_known` и `validate_manifest`

**Упражнение (M1):** добавьте проверку поля в `validate_well_known` — `python labs/run_exercises.py --module m1`

---

## M2 — SDK и интеграция с Hub

**Концепция:** регистрация, поиск и вызов платной capability через реальный хаб; получение подписанной квитанции.
**Лаба:** `labs/lab02_hub_discover.py` · **~20 мин** · нужен M1

### Шаги

1. `python labs/lab02_hub_discover.py`
2. Проследите поток:

   ```
   discover("translate") → invoke(prod-translate, translate.multi@v2) → receipt
   ```

3. Читайте поля: `success`, `price`, `served by` и `nonce` квитанции. Это повторяет боевой федеративный вызов без клонирования `aimarket-hub`.
4. Убедитесь, что события `discover` и `invoke` есть в блоке trace.

### Самопроверка

- [ ] Поиск возвращает метаданные capability (`product_id`/`capability_id`, цену)
- [ ] Вызов возвращает структурированный результат и квитанцию с nonce

**Упражнение (M2):** найдите `summarize` и вызовите его — `python labs/run_exercises.py --module m2`

---

## M3 — Эскроу и платёжные каналы

**Концепция:** удержание средств до доставки; поток микроплатежей без on-chain транзакции на каждый вызов.
**Лаба:** `labs/lab03_escrow_channel.py` · **~20 мин** · нужен M2

### Шаги

1. `python labs/lab03_escrow_channel.py`
2. Жизненный цикл:
   - **Открыть** предоплаченный канал с `budget_usd=0.25`.
   - **Вызвать** через него `summarize@v1`.
   - **Закрыть** канал и посмотреть `spent` против `refund`.
3. Две идеи:
   - **Платёжный канал** — пакет микроплатежей без on-chain транзакции на каждый вызов.
   - **Эскроу** — средства держатся до доставки; неиспользованный бюджет возвращается при закрытии.

Hub-lite отдаёт `/ai-market/v2/channel/open` и `/close` для демонстрации паттерна. Полный цикл SDK в M6 использует реальный стек эскроу хаба.

### Самопроверка

- [ ] Называете цикл: открыть → вызвать → закрыть → возврат
- [ ] Канал амортизирует множество вызовов на один бюджет против 402 на каждый вызов

**Упражнение (M3):** откройте канал с бюджетом `$1.00` и закройте его — `python labs/run_exercises.py --module m3`

---

## M4 — Репутация и доверие

**Концепция:** подписанные квитанции делают платные вызовы проверяемыми и питают граф репутации в стиле LUMEN.
**Лаба:** `labs/lab04_reputation_trust.py` · **~25 мин** · нужен M2

### Шаги

1. `python labs/lab04_reputation_trust.py`
2. Две проверки:
   - Настоящая квитанция проходит как `True` и **повышает** оценку доверия продукта.
   - Копия после `tamper_receipt(..., price_usd=0.0)` проходит как `False` и **понижает** её.
3. Строительные блоки:
   - `courselib.trust.sign_receipt` / `verify_receipt` — учебные квитанции HMAC-SHA256 (stdlib, та же идея, что в проде).
   - `TrustGraph` — изменения оценки в стиле LUMEN в памяти.
   - Hub `/ai-market/v2/trust/record` — демо федеративного хука доверия.

### Самопроверка

- [ ] Объясняете, почему подделанная цена не проходит проверку
- [ ] Видите, как проверенные и подделанные вызовы двигают оценку доверия в разные стороны

**Упражнение (M4):** подпишите свою квитанцию своим секретом и проверьте её — `python labs/run_exercises.py --module m4`

---

## M5 — Публикация capability

**Концепция:** выпуск metered API, который покупают другие агенты — сторона **провайдера**.
**Лаба:** `labs/lab05_publish_capability.py` · **~20 мин** · нужен M2

### Шаги

1. `python labs/lab05_publish_capability.py`
2. Workflow провайдера:
   - `register_capability("prod-course", "sentiment.metered@v1", 0.007, ...)`.
   - Перезапросить manifest и увидеть рост числа инструментов (`before → after`).
   - `discover("sentiment")` находит новую capability.
   - `invoke` от лица потребителя — читайте цену и nonce квитанции.
3. Убедитесь в событиях `register`, `manifest`, `discover`, `invoke` в trace.

### Самопроверка

- [ ] Регистрируете capability с ценой и описанием
- [ ] Доказываете, что после регистрации она находится и вызывается

**Упражнение (M5):** зарегистрируйте свою capability и вызовите её — `python labs/run_exercises.py --module m5`

---

## M6 — Capstone: платный цикл агента (продвинутый)

**Концепция:** полный автономный цикл `hire()` через реальный SDK `aimarket-agent`.
**Лаба:** `labs/lab06_paid_capability_capstone.py` · **~45 мин** · нужен `[sandbox]` (~50 МБ, один раз)

### Шаги

1. Установите extra sandbox один раз (в Colab переиспользуйте сессию, если ранние лабы уже его поставили):

   ```bash
   pip install -e ".[sandbox,dev]"
   ```

2. `python labs/lab06_paid_capability_capstone.py`
3. Полный цикл:

   ```
   discover → open channel → invoke → signed receipt → settle → bill of materials
   ```

   Лаба поднимает локальный AIMarket Hub и заглушку Factory в фоновых потоках, затем вызывает `econ.hire("translate text to multiple languages")` с бюджетом `$3.00`. **Реальных денег нет.**
4. Читайте bill of materials: задача, успех, ID канала, потрачено, версия протокола, capability по шагам и живые листинги ACEX.

> Если SDK `aimarket-agent` **не** установлен, лаба определит это через `sdk_available()` и чисто пропустится с подсказкой — без падения. Лабы 1–5 и все упражнения работают без него.

### Самопроверка

- [ ] Называете полный цикл: discover → channel → invoke → receipt → settle
- [ ] Понимаете, что capstone — единственная лаба, требующая `[sandbox]`

**Упражнение (M6):** запустите полный цикл `hire()` в песочнице или проверку платного вызова через hub-lite — `python labs/run_exercises.py --module m6`

---

## Упражнения и сертификат

Каждый модуль 1:1 соответствует самодостаточной DIY-проверке (`m1`…`m6`). Запуск одной:

```bash
python labs/run_exercises.py --module m3
```

Запуск всех:

```bash
python labs/run_exercises.py
```

Печатает `✓` или `✗` по каждому модулю. Когда проходят **все шесть** — сгенерируйте сертификат:

```bash
python labs/run_exercises.py --certificate "Иван Петров" --lang ru   # или en / es
```

Создаётся `certificate.html` — откройте в браузере и **Print → Save as PDF** для PDF-копии. ID сертификата — это дайджест SHA-256 от имени + даты выдачи, а подписи и бейджи модулей локализованы для `en`/`ru`/`es`.

---

## Наблюдаемость в каждой лабе

Каждая лаба строит `courselib.orchestration.Trace` и печатает его в конце. Виды событий:

- `well_known`, `manifest`, `discover`, `invoke`
- `channel_open`, `channel_close`
- `verify`, `register`
- `hire`, `step`, `capital` (только capstone)

Читайте блок trace, чтобы проследить **экономическую историю** — поиск → оплата → вызов → квитанция → расчёт — а не только финальный результат. Это «лог юнит-тестов» лабы: один неудачный вызов — одно событие trace, на которое можно указать.

Боевой путь — фабрика подключает OpenTelemetry + LangSmith, см. [observability-langsmith.md](https://github.com/alexar76/aicom/blob/main/docs/observability-langsmith.md) (для курса не нужно).

---

## Мост: от курса к боевому хабу

Путь выпускника, когда лабы стали привычны:

1. Задайте `COURSE_HUB_URL=https://modelmarket.dev` (или свой хаб).
2. Используйте `courselib.economy.connect()` вместо `embedded_sandbox()`.
3. Те же методы SDK переносятся: `discover`, `invoke`, `hire`.

Получите живой well-known и сравните с валидатором из M1:

```bash
curl https://modelmarket.dev/.well-known/ai-market.json
```

Прогоните через `courselib.protocol.validate_well_known` — те же структурные проверки из модуля M1 применимы к реальному хабу.

---

## Чеклист самопроверки

- [ ] `pytest -q` проходит локально
- [ ] Запущены lab01–lab05 на треке `[hub-lite]`
- [ ] Запущена lab06 с `[sandbox]` (или виден чистый пропуск, пока зависимости не стоят)
- [ ] Все шесть упражнений проходят: `python labs/run_exercises.py`
- [ ] Хотя бы одна лаба запущена с `COURSE_LANG=ru` или `es`
- [ ] Прочитан блок trace, объясняете discover → invoke → receipt
- [ ] Сгенерирован сертификат: `--certificate "Имя"`

---

## Типичные проблемы

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: fastapi` (или `uvicorn`/`httpx`) | Поставьте extras hub-lite: `pip install -e ".[hub-lite,dev]"` |
| `ModuleNotFoundError: aimarket_agent` | Lab 6 и тесты economy требуют стек sandbox: `pip install -e ".[sandbox,dev]"`. В монорепе убедитесь, что `aimarket-agent/` и `aimarket-hub/` есть как соседние каталоги. |
| Capstone печатает «Capstone пропущен» | Ожидаемо без SDK — поставьте `[sandbox]` и перезапустите. Не ошибка. |
| Таймаут hub-lite на первом запуске | Холодный старт ~2–5 с; перезапустите. CI ждёт `/.well-known/ai-market.json`. |
| Листинги capital дают 500 в sandbox | `AIFACTORY_DATA_ROOT` должен указывать внутрь временного каталога sandbox — `embedded_sandbox()` ставит это автоматически. |
| `ModuleNotFoundError: courselib` | Запуск из корня репозитория; лабы добавляют родительский каталог в `sys.path`. |
| Ключ виден как `modules.m1.title` | Нет перевода — проверьте паритет ключей `i18n/en.json` (контролирует `tests/test_i18n.py`). |
| В Colab старый код | Перезапустите setup-ячейку; пиньте ветку `main`. |

**Проблемы Factory:** [FAQ.ru.md](https://github.com/alexar76/aicom/blob/main/docs/FAQ.ru.md)

---

## Обновление сайта и ноутбуков

После правок лаб или каталогов i18n:

```bash
python3 scripts/build_course_assets.py
```

Гайды в `docs/` правятся вручную — сначала EN, затем зеркала RU/ES.

---

**Дальше:** изучите [спецификацию AIMarket Protocol](https://github.com/alexar76/aimarket-protocol/blob/main/spec.md) и подключите свою metered capability к реальному хабу.
