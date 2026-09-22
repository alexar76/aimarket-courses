# Пошагово — PQC · Гибридная подпись

> **Языки:** `COURSE_LANG=en|ru|es|fr|zh` · [EN](./step-by-step.md) · [ES](./step-by-step.es.md) · [FR](./step-by-step.fr.md) · [ZH](./step-by-step.zh.md)

## Зачем курс

Подписи — утверждения о **прошлом**. Квитанция, оспоренная через годы, уже должна противостоять квантовому противнику. Замена Ed25519 на один ML-DSA ломает совместимость сегодня. Хаб AIMarket публикует **гибрид**: Ed25519 + ML-DSA-65 — LIVE: [`modelmarket.dev/.well-known/ai-market.json`](https://modelmarket.dev/.well-known/ai-market.json). SIM не выдаём за LIVE.

## Установка

```bash
pip install -e ".[dev]"       # cryptography
pip install -e ".[pqc,dev]"   # опционально dilithium-py
pytest -q
COURSE_LANG=ru python labs/lab01_why_hybrid.py
```

Без dilithium: классика проверяется, LIVE-поля осматриваются, PQ-подпись помечена как skipped — без фейкового успеха.

## Модули

| Модуль | Лаб | Суть |
| --- | --- | --- |
| M1 | `lab01_why_hybrid` | Зачем гибрид; опционально LIVE |
| M2 | `lab02_key_identity` | Двойная идентичность / pin обоих ключей |
| M3 | `lab03_sign_receipt` | Подписать квитанцию |
| M4 | `lab04_verify_offline` | Офлайн-проверка |
| M5 | `lab05_hybrid_gate_capstone` | `refuse_single_orbit` — фаза 3 |

## Упражнения

Заполните `# YOUR CODE HERE` в `courselib/exercises.py` → `python labs/run_exercises.py` → `--certificate "Имя"`.

## Чеклист

- [ ] Понятен даунгрейд без `require_pq`
- [ ] Офлайн classical verify работает
- [ ] Шлюз отклоняет single-orbit
- [ ] LIVE осмотрен без выдачи SIM за LIVE
