# Пошаговое руководство по курсу

> **Для кого:** разработчики, изучающие паттерны лотерейных смарт-контрактов до выхода на Base mainnet.  
> **Язык лаб:** `COURSE_LANG=en|ru|es` · строки UI в `i18n/` · этот гайд на русском.  
> **English:** [step-by-step.md](./step-by-step.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Зачем этот курс

On-chain лотереи ломаются, когда **оператор** может незаметно перекатывать розыгрыш, пока ему не понравится победитель, — это атака grinding. Контракты `lottery/` на Base закрывают её проверяемой случайностью (ECVRF через оракул **Sortes**) и VDF-маяком Wesolowski из оракула **Chronos**, а выплаты проходят через escrow-канал **AIMarketEscrow** со списанием по чеку. Курс разбирает каждый из этих примитивов как небольшой запускаемый порт на Python без LLM. Вы проверяете **тот же** Foundry-вектор, что и Solidity-контракты (`ChronosVDF.t.sol`), проходите раунд релейера от начала до конца и завершаете капстоуном, который симулирует полный честный раунд с проверяемыми артефактами — всё это напрямую отображается на боевой код `lottery/`.

---

## Содержание

1. [Выбор трека](#выбор-трека)
2. [Установка (10 минут)](#установка-10-минут)
3. [M1 — Несмещаемый розыгрыш лотереи](#m1--несмещаемый-розыгрыш-лотереи)
4. [M2 — Проверка VDF on-chain](#m2--проверка-vdf-on-chain)
5. [M3 — Escrow и платёжные каналы](#m3--escrow-и-платёжные-каналы)
6. [M4 — Жизненный цикл раунда релейера](#m4--жизненный-цикл-раунда-релейера)
7. [M5 — Капстоун: честный раунд](#m5--капстоун-честный-раунд)
8. [Упражнения и сертификат](#упражнения-и-сертификат)
9. [Наблюдаемость в каждой лабе](#наблюдаемость-в-каждой-лабе)
10. [Мост: от курса к lottery/](#мост-от-курса-к-lottery)
11. [Чеклист самопроверки](#чеклист-самопроверки)
12. [Типичные проблемы](#типичные-проблемы)

---

## Выбор трека

| Трек | Модули | Время | Оракулы |
|------|--------|-------|---------|
| **Базовый** | M1 → M4 | ~1,5 ч | Sortes + Chronos (fallback, если не установлены) |
| **Продвинутый** | Базовый + M5 капстоун | +30 мин | Sortes + путь Chronos VDF |
| **Мост к lottery/** | После M4 или M5 | +30 мин | Живой `forge test` + контракты на Base |

После **каждой** лабы смотрите блок `Trace` (раздел «Наблюдаемость»).

---

## Установка (10 минут)

### Шаг 1 — Клон и установка

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/smart-contracts-course
pip install -e ".[oracles,dev]"
```

Экстра `[oracles]` подключает пакеты оракулов **Sortes** (ECVRF) и **Chronos** (VDF). Если экстра недоступна в вашем окружении, лабы всё равно работают — `courselib` переключается на детерминированную реализацию из stdlib, и трейс помечает `oracle=fallback`. Нужен Python 3.11+.

### Шаг 2 — Тесты

```bash
pytest -q
```

**Ожидается:** все тесты проходят (паритет i18n по en/ru/es, примитивы контрактов, вложенный Foundry-вектор, рендеринг сертификата).

### Шаг 3 — Первая лаба

```bash
python labs/lab01_unbiasable_draw.py
python labs/run_exercises.py
```

### Шаг 4 — Язык интерфейса лаб (опционально)

```bash
export COURSE_LANG=ru   # или es, по умолчанию en
python labs/lab01_unbiasable_draw.py
```

`COURSE_LANG` меняет только печатаемые строки лабы (названия модулей, метки, подсказки) — код, команды, номера билетов и Foundry-вектор одинаковы на всех языках.

### Шаг 5 — Google Colab

1. Откройте [сайт курса](https://alexar76.github.io/aimarket-courses/smart-contracts-course/) → **Open in Colab** на любой лабе.
2. Выполните setup-ячейку (clone + `pip install -e ".[oracles,dev]"`).
3. При необходимости в setup-ячейке: `os.environ["COURSE_LANG"] = "ru"`.
4. Запустите ячейку лабы.

---

## M1 — Несмещаемый розыгрыш лотереи

**Концепция:** Commit–reveal и ECVRF закрывают grinding-атаки оператора.  
**Лаба:** `labs/lab01_unbiasable_draw.py` · **~15 мин**

### Шаги

1. `python labs/lab01_unbiasable_draw.py`
2. Сравните два розыгрыша в выводе:
   - **Смещённая лотерея (grinding оператора)** — `grindable=True`: оператор перехеширует с секретом, пока не выпадет нужный билет (`BiasedLottery.operator_can_grind`).
   - **Честная лотерея (ECVRF)** — одно `alpha` даёт ровно одно `beta`, `verified=True`. Перекатить нельзя.
3. Откройте `courselib/contracts.py` — `BiasedLottery`, `FairLottery`, `_sortes_draw` (путь Sortes ECVRF с fallback из stdlib).
4. **Упражнение:** `python labs/run_exercises.py --module m1` — честный розыгрыш проверяется, смещённый поддаётся grinding.

**Что доказывает:** проверяемый розыгрыш убирает произвол оператора. On-chain потребитель: `lottery/docs/` и `AIAgentLottery.sol`.

---

## M2 — Проверка VDF on-chain

**Концепция:** Доказательства Wesolowski из Chronos совпадают с тест-векторами Foundry.  
**Лаба:** `labs/lab02_vdf_verify.py` · **~15 мин** · нужен M1

### Шаги

1. `python labs/lab02_vdf_verify.py`
2. Лаба грузит вложенный Foundry-вектор (`courselib/fixtures/chronos_vector.json`, копия `lottery/contracts/test/vectors/chronos_vector.json`) и проверяет `π^l·g^r ≡ y (mod N)`. Вывод: `verify: True (AB_equals_y=True)`.
3. Если оракул Chronos установлен, `verify_wesolowski_vector` ещё и заново выводит доказательство вживую (`hash_to_group → evaluate → prove → verify`).
4. **Упражнение:** `python labs/run_exercises.py --module m2`.

**Что доказывает:** Python- и Solidity-верификаторы согласны по одним и тем же байтам. Запустите `forge test` в `lottery/contracts` — `ChronosVDF.t.sol` использует тот же вектор.

---

## M3 — Escrow и платёжные каналы

**Концепция:** Удержание средств до поставки; списание по чеку, как в AIMarketEscrow.  
**Лаба:** `labs/lab03_escrow_channel.py` · **~20 мин** · нужен M1

### Шаги

1. `python labs/lab03_escrow_channel.py`
2. Жизненный цикл канала: **open** (депозит) → **debit** (по чеку) → **settle** (раздел между hub и возвратом).
3. Строка **Повтор чека**: второй `debit` с тем же `receipt_id` отклоняется (`blocked=True`) — это защита от повтора, `EscrowChannel.used_receipts`.
4. `courselib/contracts.py` → `EscrowChannel` моделирует `AIMarketEscrow` open/debit/settle (Protocol v2 §6): подпись, nonce, совпадение hub, проверка баланса.
5. **Упражнение:** `python labs/run_exercises.py --module m3` — спишите дважды по одному чеку, второе должно упасть.

---

## M4 — Жизненный цикл раунда релейера

**Концепция:** baseSeed, розыгрыш Sortes, опциональный путь VDF on-chain.  
**Лаба:** `labs/lab04_relayer_round.py` · **~20 мин** · нужны M1–M2

### Шаги

1. `python labs/lab04_relayer_round.py`
2. Три фазы в выводе и в блоке `Trace`:
   - **Сид Chronos** — `base_seed = sha256(roundId ‖ blockhash ‖ platonRandom)`.
   - **Билет Sortes** — проверяемый розыгрыш раунда (`verified=True`).
   - **Вектор VDF** — при `onchain_vdf=True` раунд прикрепляет маяк `VdfProof` и заново проверяет Foundry-вектор (`vector_valid=True`).
3. Сверьтесь: `lottery/relayer/ailottery_relayer/economy_draw.py` — боевой розыгрыш, который зеркалит эта лаба.
4. **Упражнение:** `python labs/run_exercises.py --module m4` — проследите трейс `baseSeed → Sortes → VDF-маяк`.

---

## M5 — Капстоун: честный раунд

**Концепция:** Симуляция полного раунда лотереи с проверяемыми артефактами.  
**Лаба:** `labs/lab05_lottery_capstone.py` · **~30 мин** · нужны M1–M4 · **трек:** продвинутый

### Шаги

1. `python labs/lab05_lottery_capstone.py`
2. Лаба вызывает `simulate_fair_round(onchain_vdf=True, client_seed=...)` и печатает артефакты раунда: `ticket`, `vdf_path=onchain`, `chronos_vector=True`.
3. Сравните артефакты с реальным логом `lottery/relayer` — у каждого поля есть боевой аналог.
4. **Упражнение:** `python labs/run_exercises.py --module m5` — запустите `simulate_fair_round` с `onchain_vdf=True`.

**Что доказывает:** примитивы M1–M4 собираются в один аудируемый раунд — проверяемый билет, VDF-маяк и проверяемый вектор: артефакты, которым игрок верит, не доверяя оператору.

---

## Упражнения и сертификат

```bash
python labs/run_exercises.py                 # все модули
python labs/run_exercises.py --module m3     # один модуль
```

Каждый модуль печатает `✓` или `✗`; исправьте сбои и перезапустите. Когда всё зелёное — сертификат:

```bash
python labs/run_exercises.py --certificate "Иван Петров" --lang ru
```

Создаётся `certificate.html` (переопределяется через `-o`). Откройте в браузере и **Печать → Сохранить как PDF**. ID диплома выводится из имени и даты (`courselib/certificate.py`). Сертификат также можно получить в разделе **Сертификат** на сайте курса.

---

## Наблюдаемость в каждой лабе

После каждой лабы (5 мин):

1. Блок **trace** в конце вывода.
2. Сопоставьте `events` с шагами в stdout: `biased_draw`, `fair_draw`, `vdf_verify`, `open`/`debit`/`settle`, `base_seed`/`sortes_draw`/`vdf_beacon`, `capstone`.
3. В M4 свяжите три события трейса с тремя напечатанными фазами.

Trace — это «лог on-chain событий» раунда: по нему вы находите событие, доказывающее честность розыгрыша.

---

## Мост: от курса к lottery/

1. **Foundry-вектор** — `lottery/contracts/test/vectors/chronos_vector.json` (вложен в `courselib/fixtures/`). Верификатор курса читает тот же файл, что и Solidity-тест.
2. **On-chain верификатор** — `lottery/contracts/src/ChronosVDF.sol`, тест `ChronosVDF.t.sol`:

   ```bash
   cd lottery/contracts && forge test
   ```

3. **Розыгрыш релейера** — `lottery/relayer/ailottery_relayer/economy_draw.py` (зеркало M4).
4. Сопоставление:

   | Курс | lottery/ |
   |------|----------|
   | M1 честный розыгрыш | Sortes ECVRF + `AIAgentLottery.sol` |
   | M2 проверка VDF | `ChronosVDF.sol` + `ChronosVDF.t.sol` |
   | M3 escrow-канал | `AIMarketEscrow` open/debit/settle |
   | M4 раунд релейера | `economy_draw.py` |
   | M5 капстоун | Полный раунд + VDF-маяк on-chain |

5. **Документация:** [lottery/docs/](https://github.com/alexar76/lottery/tree/main/docs).

---

## Чеклист самопроверки

Базовый трек:

- [ ] lab01–lab04 локально и в Colab
- [ ] Объясняете, почему проверяемый розыгрыш бьёт grinding оператора
- [ ] Проверяете Foundry-вектор Chronos и связываете его с `ChronosVDF.t.sol`
- [ ] Описываете escrow open → debit → settle и защиту от повтора
- [ ] Читаете блок `Trace` и находите событие честности

Продвинутый трек:

- [ ] lab05 + перечисление артефактов честного раунда
- [ ] `forge test` в `lottery/contracts` и его связь с M2

---

## Типичные проблемы

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: courselib` | Запуск из корня репозитория |
| Импорт оракула падает / ошибка `pip install ".[oracles]"` | Лабы работают на fallback из stdlib (`oracle=fallback`); для живого ECVRF/VDF запускайте из монорепо aicom, где резолвится `oracles/` |
| `verify: False` в M2 | Проверьте целостность `courselib/fixtures/chronos_vector.json` (`valid` и `AB_equals_y` должны быть true) |
| Пустые RU/ES строки | `export COURSE_LANG=ru`; ключи `i18n/ru.json` должны совпадать с `en.json` |
| Падение паритета i18n в pytest | Добавьте недостающий ключ во все три `i18n/{en,ru,es}.json` |
| В Colab старый код | Перезапустите setup-ячейку; зафиксируйте ветку `main` |

**Деплой lottery/ и on-chain:** [lottery/docs/](https://github.com/alexar76/lottery/tree/main/docs).

---

Гайды в `docs/` правятся вручную — сначала EN, затем зеркала RU/ES.
