# Пошаговое руководство по курсу

> **Для кого:** разработчики, защищающие MCP-агентов до (или параллельно с) ARGUS / AI-Factory.  
> **Язык лаб:** `COURSE_LANG=en|ru|es` · строки UI в `i18n/` · этот гайд на русском.  
> **English:** [step-by-step.md](./step-by-step.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Зачем этот курс

MCP (Model Context Protocol) подключает агента к внешним серверам инструментов — но каждое *описание* инструмента и каждая JSON-*схема* это текст, контролируемый атакующим, который модель читает как доверенную инструкцию. Курс учит строить модель угроз этой поверхности, статически сканировать отравленные определения инструментов, ранжировать серверы графовым доверием (LUMEN), включать fail-closed allowlist владельца и собирать всё в gate WARDEN, который блокирует вредоносный typosquat-сервер. Каждый примитив это запускаемый, без LLM, Python-порт боевого MCP-firewall ARGUS WARDEN — то, что вы изучаете, ложится прямо на реальный код.

---

## Содержание

0. [Зачем этот курс](#зачем-этот-курс)
1. [Выбор трека](#выбор-трека)
2. [Установка (10 минут)](#установка-10-минут)
3. [M1 — Модель угроз MCP](#m1--модель-угроз-mcp)
4. [M2 — Статическое сканирование и политика](#m2--статическое-сканирование-и-политика)
5. [M3 — Оценка доверия LUMEN](#m3--оценка-доверия-lumen)
6. [M4 — Owner-lock и fail-closed](#m4--owner-lock-и-fail-closed)
7. [M5 — Capstone: вредоносный сервер](#m5--capstone-вредоносный-сервер)
8. [Упражнения и сертификат](#упражнения-и-сертификат)
9. [Наблюдаемость в каждой лабе](#наблюдаемость-в-каждой-лабе)
10. [Мост: от курса к ARGUS WARDEN](#мост-от-курса-к-argus-warden)
11. [Чеклист самопроверки](#чеклист-самопроверки)
12. [Типичные проблемы](#типичные-проблемы)

---

## Выбор трека

| Трек | Модули | Время | Оракулы |
|------|--------|-------|---------|
| **Базовый** | M1 → M2 → M3 → M4 | ~2 ч | LUMEN (только M3) |
| **Продвинутый** | Базовый + M5 capstone | +30 мин | LUMEN + полная цепочка WARDEN |
| **Мост к Factory** | После M4 или M5 | +30 мин | Реальный ARGUS + Hub |

Каждая лаба печатает блок `Trace` — относитесь к нему как к журналу аудита лабы.

---

## Установка (10 минут)

### Шаг 1 — Клон и установка

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/mcp-security-course
pip install -e ".[oracles,dev]"
```

**Из монорепозитория aicom** (рекомендуется для контрибьюторов):

```bash
cd courses/mcp-security-course
pip install -e ".[oracles,dev]"
```

LUMEN подтягивается автоматически из `oracles/oracles/lumen` при запуске внутри монорепозитория.

**Отдельный клон** без соседнего монорепозитория:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
pip install -e _deps/oracles/oracles/lumen
pip install -e ".[oracles,dev]"
```

### Шаг 2 — Тесты

```bash
pytest -q
```

**Ожидается:** паритет i18n, статическое сканирование WARDEN, PageRank LUMEN, упражнения, smoke-импорты лаб.

### Шаг 3 — Язык интерфейса лаб (опционально)

```bash
export COURSE_LANG=ru   # или es, по умолчанию en
python labs/lab01_threat_model.py
```

### Шаг 4 — Google Colab

1. Откройте [сайт курса](https://alexar76.github.io/aimarket-courses/mcp-security-course/) → **Open in Colab** на любой лабе.
2. Выполните setup-ячейку (clone + pip + срез oracles).
3. При необходимости задайте `os.environ["COURSE_LANG"] = "ru"` в setup.
4. Запустите ячейку лабы.

---

## M1 — Модель угроз MCP

**Концепция:** внедрение промптов, отравление инструментов и каналы утечки данных в MCP.  
**Лаба:** `labs/lab01_threat_model.py` · **~15 мин** · установка завершена

### Шаги

1. Прочитайте docstring в начале `labs/lab01_threat_model.py`.
2. Запустите локально:

   ```bash
   python labs/lab01_threat_model.py
   ```

3. Разберите два сценария:
   - **Prompt injection** — текст атакующего, спрятанный в *описании* инструмента.
   - **Tool poisoning** — поля схемы, запрашивающие секреты или exfil-URL.
4. Прочитайте блок **trace** — каждая поверхность атаки логируется как событие.
5. Бегло просмотрите `courselib/warden.py` — найдите `INJECTION_PATTERNS`, `EXFIL_PATTERNS`, `SECRET_PATTERNS` (5 мин).

### Самопроверка

- [ ] Объясняете, почему *описания* инструментов это текст атакующего, которому модель доверяет
- [ ] Видите разницу между injection в промпте пользователя и отравлением определения инструмента

---

## M2 — Статическое сканирование и политика

**Концепция:** ловим вредоносные схемы инструментов до того, как агент их вызовет.  
**Лаба:** `labs/lab02_static_scan.py` · **~20 мин** · нужен M1

### Шаги

1. `python labs/lab02_static_scan.py`
2. Сравните блоки сканирования **benign** vs **malicious**:
   - benign → высокая оценка, ноль или низкая критичность срабатываний;
   - malicious → низкая оценка, `TOOL_DEF_INJECTION`, `TOOL_DEF_EXFIL`, `TOOL_DEF_SECRET_REQUEST`.
3. Прочитайте сообщения срабатываний — какой haystack совпал (`description` vs JSON-схема).
4. Откройте `argus/src/warden/static-scan.ts` в монорепозитории — сравните паритет регулярок с `courselib/warden.py`.
5. **Упражнение:** `python labs/run_exercises.py --module m2`

### Самопроверка

- [ ] Статическое сканирование идёт по описанию *и* по тексту JSON-схемы
- [ ] Одно критическое срабатывание обрушивает оценку gate, но в одиночку не всегда даёт фатальную блокировку

---

## M3 — Оценка доверия LUMEN

**Концепция:** репутация на графе — кто-кому-доверяет PageRank по MCP-серверам.  
**Лаба:** `labs/lab03_lumen_score.py` · **~20 мин** · нужен `[oracles]` (numpy + lumen)

### Шаги

1. Подтвердите установку: `pip install -e ".[oracles,dev]"`.
2. `python labs/lab03_lumen_score.py`
3. Посмотрите рёбра графа доверия: `hub` → официальные серверы; typosquat изолирован.
4. Изучите ранжированные оценки — `hub` и официальные серверы должны обгонять `offical-mcp-drainer`.
5. Прочитайте `courselib/lumen.py` — `demo_mcp_trust_graph()` и `score_servers()`.
6. Опционально: откройте `oracles/oracles/lumen/lumen/pagerank.py` — ядро EigenTrust.
7. **Упражнение:** `python labs/run_exercises.py --module m3`

### Самопроверка

- [ ] Оценки в сумме дают 1 (распределение вероятностей)
- [ ] Транзитивное доверие поднимает узлы, которым доверяют доверенные узлы

---

## M4 — Owner-lock и fail-closed

**Концепция:** привязка агентов к спискам инструментов, одобренным владельцем (аналог Telegram owner-lock).  
**Лаба:** `labs/lab04_owner_lock.py` · **~15 мин** · нужен M2

### Шаги

1. `python labs/lab04_owner_lock.py`
2. Разрешённые инструменты (`read_file`, `search_docs`) проходят; `exec_shell`, `transfer_funds` блокируются.
3. Обратите внимание на демо с **пустым allowlist** — fail-closed, каждый инструмент запрещён.
4. Прочитайте `OwnerLock` в `courselib/warden.py` — `check_tool()` и `OwnerLockGate`.
5. Доп. чтение: [argus/docs/channels.md](https://github.com/alexar76/aicom/blob/main/argus/docs/channels.md) § Telegram owner-lock.
6. **Упражнение:** `python labs/run_exercises.py --module m4`

### Самопроверка

- [ ] Allowlist явный — неизвестные инструменты запрещаются, а не молча разрешаются
- [ ] Пустой allowlist это fail-closed (нулевое доверие по умолчанию)

---

## M5 — Capstone: вредоносный сервер

**Концепция:** полная цепочка gate WARDEN блокирует отравленный typosquat MCP-сервер.  
**Лаба:** `labs/lab05_warden_capstone.py` · **~30 мин** · нужны M1–M4

### Шаги

1. `python labs/lab05_warden_capstone.py`
2. Сравните вердикты:
   - **Benign официальный сервер** → `allowed`, высокая составная оценка;
   - **Poisoned typosquat** → `blocked`, `decided_by` называет провалившийся gate.
3. Порядок gate в учебном порте: static-scan → threat-feed → reputation (LUMEN) → owner-lock → pinning.
4. Изучите список срабатываний — до блокировки могут отметиться несколько gate.
5. Прочитайте `Warden.vet()` в `courselib/warden.py` — составная оценка это произведение оценок gate.
6. **Упражнение:** `python labs/run_exercises.py --module m5`

### Самопроверка

- [ ] Threat feed ловит id typosquat-сервера (`offical-mcp-drainer`)
- [ ] Static-scan ловит injection + exfil в определениях инструментов
- [ ] Низкая репутация LUMEN вносит вклад при `allow_unknown_servers=False`

---

## Упражнения и сертификат

После лаб запустите DIY-проверки:

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Иван Петров" --lang ru
```

Откроется `certificate.html` — Print → Save as PDF в браузере. ID удостоверения выводится из имени + даты.

| Модуль | Проверка упражнения |
|--------|---------------------|
| M1 | Сигнатура injection обнаружена в отравленном инструменте |
| M2 | Benign-инструменты не дают критических срабатываний |
| M3 | Hub обгоняет typosquat на графе доверия |
| M4 | Owner-lock запрещает инструменты вне списка |
| M5 | Полный WARDEN блокирует вредоносный capstone-сервер |

---

## Наблюдаемость в каждой лабе

**Концепция:** каждая лаба логирует решения в `Trace` — это ваш аудит-след событий безопасности.

### Шаги (повторять после каждой лабы)

1. Прокрутите к секции **trace** в выводе лабы.
2. Сопоставьте события со stdout: срабатывания, оценки доверия, решения owner-lock, вердикты WARDEN.
3. В M5 сопоставьте события `warden_finding` с напечатанным списком срабатываний.

### Самопроверка

- [ ] Trace это «превью SIEM» для безопасности агента
- [ ] Можете указать на gate, заблокировавший подключение

---

## Мост: от курса к ARGUS WARDEN

**Цель:** связать концепции курса с боевым ARGUS (~30 мин).

1. **Прочитайте документацию WARDEN** — [argus/docs/security-warden.md](https://github.com/alexar76/aicom/blob/main/argus/docs/security-warden.md)

2. **Сопоставление курс → ARGUS**

   | Курс | ARGUS |
   |------|-------|
   | M2 static-scan | `src/warden/static-scan.ts` |
   | M3 LUMEN | `ReputationGate` + оракул LUMEN |
   | M4 owner-lock | Owner-lock канала + allowlist egress |
   | M5 capstone | Цепочка gate `Warden.create()` |

3. **Запустите ARGUS** (опционально, из монорепозитория):

   ```bash
   cd argus && npm install && npm test -- warden
   ```

4. **Безопасность supply в Hub** — [aimarket-hub/docs/supply-security.md](https://github.com/alexar76/aicom/blob/main/aimarket-hub/docs/supply-security.md)

---

## Чеклист самопроверки

После базового трека вы умеете:

- [ ] Запускать lab01–lab04 локально и в Colab
- [ ] Называть три семейства сигнатур static-scan (injection, exfil, secrets)
- [ ] Объяснять PageRank-доверие на графе MCP-серверов
- [ ] Описывать fail-closed allowlist владельца
- [ ] Читать блок `Trace` и находить заблокированный инструмент или gate

После продвинутого трека добавьте:

- [ ] Запустить lab05 и объяснить, какой gate заблокировал typosquat-сервер
- [ ] Открыть `argus/src/warden/index.ts` и найти боевой порядок gate

---

## Типичные проблемы

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: courselib` | Запуск из корня репозитория; лабы добавляют родительский путь в `sys.path` |
| `ImportError: Oracle package 'lumen'` | Установите срез oracles или запускайте из монорепозитория aicom |
| Нет `numpy` | `pip install -e ".[oracles,dev]"` |
| Пустые строки RU/ES | Задайте `COURSE_LANG`; ключи `i18n/ru.json` должны совпадать с `en.json` |
| Падение pytest по i18n | Добавьте недостающие ключи во все три JSON-файла |
| M5 блокирует benign-сервер | Проверьте, что allowlist owner-lock включает имена benign-инструментов |
| Старый код в Colab | Перезапустите setup-ячейку; закрепите ветку `main` |

**Проблемы с ARGUS:** [argus/README.md](https://github.com/alexar76/aicom/blob/main/argus/README.md)

---

## Пересборка сайта и ноутбуков

После правок лаб или i18n:

```bash
python3 scripts/build_course_assets.py
python3 scripts/labs_to_notebooks.py
```

Гайды в `docs/` правятся вручную — сначала EN, затем зеркала RU/ES.
