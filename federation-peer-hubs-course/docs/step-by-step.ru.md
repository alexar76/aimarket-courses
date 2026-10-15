# Пошаговое руководство

> **Аудитория:** операторы хабов и разработчики агентов, входящие в федерацию AIMarket.  
> **Языки:** `COURSE_LANG=en|ru|es|fr|zh` · строки UI в `i18n/`.  
> **English:** [step-by-step.md](./step-by-step.md)

---

## Зачем этот курс

Стук в федерацию — это **наблюдение**. Он не должен индексировать каталог незнакомца. Курс проходит реальный путь admission на [modelmarket.dev](https://modelmarket.dev): well-known, открытая/закрытая дверь, карантин preview (search/invoke не читают эту таблицу), declared vs read, approve → crawl. Labs предпочитают live GET; фикстуры помечены и никогда не выдаются за LIVE.

---

## Треки

| Трек | Модули | Время |
|------|--------|-------|
| **Basic** | M1 → M4 | ~2 ч |
| **Advanced** | + M5 | +30 мин |

Каждый lab печатает `Trace`.

---

## Установка

```bash
cd courses/federation-peer-hubs-course   # или клон спутникового репо
pip install -e ".[hub-lite,dev]"
pytest -q
export COURSE_LANG=ru
python labs/lab01_well_known_announce.py
```

`COURSE_OFFLINE=1` — только фикстуры. `COURSE_LIVE=1 pytest tests/test_live_optional.py` — опциональная сеть.

---

## M1 — Well-known и announce

1. `python labs/lab01_well_known_announce.py`
2. Проверьте LIVE `/.well-known/ai-market.json`: name, `federated_capabilities_count`, signer, hybrid (`ed25519` + `ml-dsa-65`).
3. Запомните: knock ≠ index.

**Самопроверка:** поля идентичности; announce не индексирует.

---

## M2 — Открытая vs закрытая дверь

1. `python labs/lab02_open_vs_closed.py`
2. Запишите `door`, trusted/pending counts.
3. Контрфактуал с закрытой дверью — pending всё ещё возможен (сиды/краулер).

**Самопроверка:** дверь и preview — разные переключатели.

---

## M3 — Карантин preview

1. `python labs/lab03_preview_quarantine.py`
2. Все read-guards = `false`.
3. Пустая очередь pending — тоже валидное LIVE-доказательство правила.

**Самопроверка:** preview не searchable / не invocable.

---

## M4 — Declared vs read

1. `python labs/lab04_declared_vs_read.py`
2. Сравните заявленное и прочитанное; для pending — `declared_capabilities` vs `preview_capabilities`.
3. UI оператора показывает **оба** числа.

**Самопроверка:** не доверяйте только knock-claim.

---

## M5 — Capstone: одобрить незнакомца

1. `python labs/lab05_approve_capstone.py`
2. Чеклист: announce → pending → preview → approve → crawl.
3. Live probe; Approve/repin требуют admin bearer — lab на публичном API.

---

## Упражнения и сертификат

1. Заполните stubs в `courselib/exercises.py`.
2. `python labs/run_exercises.py`
3. `python labs/run_exercises.py --certificate "Ваше Имя" --lang ru`
4. CI: `COURSE_USE_SOLUTIONS=1 python labs/run_exercises.py`

Прод-доки: [federation-admission.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-admission.md), [federation-peer-keys.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-peer-keys.md).

---

## Устранение проблем

| Симптом | Решение |
|---------|---------|
| Сеть / HTTP | `COURSE_OFFLINE=1` или `COURSE_HUB_URL` |
| Упражнения fail | stubs или `COURSE_USE_SOLUTIONS=1` |
| Сайт устарел | `python scripts/build_course_assets.py` |
