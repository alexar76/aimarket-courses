# Guía paso a paso del curso

> **Audiencia:** desarrolladores que necesitan aleatoriedad que el propio jugador de lotería pueda verificar — antes de cablear `lottery/` en Base.
> **Idiomas:** `COURSE_LANG=en|ru|es` · cadenas de UI en `i18n/` · esta guía en español.
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

La mayoría de las loterías y sorteos «aleatorios» confían en un operador que puede volver a tirar en silencio un resultado desfavorable. Este curso muestra la criptografía que elimina esa confianza: un sorteo caótico verificable, una función de retardo verificable (VDF) que demuestra el trabajo transcurrido, una prueba ECVRF que verificas sin conexión a partir de **80 bytes**, y un time-lock RSW que oculta un valor hasta que un trabajo demostrable lo abre. Después **construyes una lotería sesgada, la rompes y la arreglas** con un sorteo que el operador no puede iterar — exactamente el patrón que consumen los contratos AIMarket `lottery/` en Base.

Cada lab habla con un **oráculo real de AIMarket** — Platon, Chronos, Sortes, Aestus — ejecutándose en local, no con un mock. Cada uno imprime un bloque `trace` para que el artefacto verificable (prueba, beta, puzzle, vector VDF) sea algo que puedas inspeccionar, no aceptar a ciegas.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 min)](#instalación-10-min)
3. [M1 — Chaos VRF con Platon](#m1--chaos-vrf-con-platon)
4. [M2 — Tiempo VDF con Chronos](#m2--tiempo-vdf-con-chronos)
5. [M3 — ECVRF y Sortes](#m3--ecvrf-y-sortes)
6. [M4 — Time-lock RSW con Aestus](#m4--time-lock-rsw-con-aestus)
7. [M5 — Commit–reveal y ataques de sesgo](#m5--commitreveal-y-ataques-de-sesgo)
8. [M6 — Verificación on-chain](#m6--verificación-on-chain)
9. [Leer la traza (en cada lab)](#leer-la-traza-en-cada-lab)
10. [Ejercicios y certificado](#ejercicios-y-certificado)
11. [Puente: del curso a la lotería en Base](#puente-del-curso-a-la-lotería-en-base)
12. [Lista de autocomprobación](#lista-de-autocomprobación)
13. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Oráculos |
|-------|---------|--------|----------|
| **Básico** | M1 → M2 → M3 → M4 | ~2 h | Platon, Chronos, Sortes, Aestus (en local) |
| **Economía** | Básico + M5 | +30 min | Sortes (lotería justa vs sesgada) |
| **Avanzado** | Economía + M6 | +30 min | Chronos + Sortes → vector para la testnet de Base |

Tras **cada** lab revisa el bloque `trace` — es su registro de auditoría.

---

## Instalación (10 min)

### Paso 1 — Clonar e instalar

Los comandos exactos de inicio rápido (fíjate en el extra `[oracles,dev]` — `oracles` trae Platon/Chronos/Sortes/Aestus, `dev` trae pytest):

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/verifiable-randomness-course
pip install -e ".[oracles,dev]"
```

**Desde el monorepo aicom** (recomendado para colaboradores): los paquetes de oráculos se resuelven automáticamente por rutas hermanas en `oracles/` — `courselib/oracle_paths.py` sube hasta la raíz del monorepo y añade `oracles/oracles/{chronos,sortes,aestus}` y `oracles/oracles/platon/backend` a `sys.path`. No necesitas instalar nada más allá de `numpy` para Platon.

```bash
cd courses/verifiable-randomness-course
pip install -e ".[oracles,dev]"
```

### Paso 2 — Verificar tests

```bash
pytest -q
```

**Esperado:** todos los tests en verde (paridad i18n en/ru/es, helpers de aleatoriedad, comprobaciones de ejercicios).

### Paso 3 — Elige idioma (opcional)

Las cadenas de UI (títulos, etiquetas `prueba`/`verificación`/`traza`, nombres de billetes) salen de `i18n/{en,ru,es}.json`. Cambia con `COURSE_LANG`:

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_platon_chaos.py
```

### Paso 4 — Alternativa Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/verifiable-randomness-course/) → **Open in Colab** en cualquier lab.
2. Ejecuta la **celda de setup** (clone + `pip install -e ".[oracles,dev]"`).
3. Si quieres una ejecución localizada, pon `os.environ["COURSE_LANG"] = "es"` en la celda de setup.
4. Ejecuta la celda del lab.

---

## M1 — Chaos VRF con Platon

**Concepto:** aleatoriedad insesgable desde un oráculo caótico verificable — chaos-state + client seed + entropía del SO, ligados por una firma Ed25519.
**Lab:** `labs/lab01_platon_chaos.py` · **~15 min** · requiere `numpy` + Platon

### Pasos

1. Lee el docstring al inicio de `labs/lab01_platon_chaos.py` (sector: lotería, gaming).
2. `python labs/lab01_platon_chaos.py`
3. Observa la salida: el esquema en `prueba`, los primeros bytes del sorteo y el resultado de `verificación`.
4. `courselib/randomness.py` → `chaos_draw()`: un `Signer` temporal, un `state` caótico, `draw_randomness(...)` y luego `verify_randomness(...)`.

### Salida esperada

- `proof: scheme=platon-chaos-vrf/v1`, sorteo firmado de **32 bytes**, `verify: True`
- bloque `trace` con un evento `chaos_draw` (`verified=True, bytes=32`)

### Autocomprobación

- [ ] Explicas por qué un client seed + firma hacen insesgable el sorteo
- [ ] Ves los 32 bytes y `verify: True` contra la clave pública

---

## M2 — Tiempo VDF con Chronos

**Concepto:** un VDF de Wesolowski demuestra trabajo *secuencial* transcurrido sobre un grupo de orden desconocido RSA-2048 — prueba de trabajo transcurrido, no confianza en el reloj del sistema.
**Lab:** `labs/lab02_chronos_vdf.py` · **~20 min** · requiere M1

### Pasos

1. `python labs/lab02_chronos_vdf.py`
2. Lee la línea `prueba`: la prueba de Wesolowski `pi` y el primo `l`; `verify: True`.
3. Fíjate en la **demo de manipulación**: el lab llama a `vdf.verify(g, y+1, …)` sobre una salida corrupta — imprime `False`.
4. `courselib/randomness.py` → `vdf_eval()`: `hash_to_group` → `evaluate` → `prove` → `verify`. Usa `difficulty=700` (~700 cuadrados) para que corra en segundos.

### Salida esperada

- `proof: pi=…… l=<primo>`, `verify: True`, `verificación de VDF manipulado: False`
- `trace` con eventos `vdf_eval` y `tamper_check`

### Autocomprobación

- [ ] Enuncias qué demuestra un VDF (trabajo secuencial) y qué **no** (tiempo real)
- [ ] Viste cómo la verificación rechaza una salida manipulada

---

## M3 — ECVRF y Sortes

**Concepto:** una prueba ECVRF según RFC 9381. Para una pareja fija (clave pública, alpha) existe exactamente **una** beta válida — el operador no puede iterar buscando una salida favorable. La prueba mide **80 bytes** y se verifica sin conexión, sin volver a llamar al oráculo.
**Lab:** `labs/lab03_sortes_ecvrf.py` · **~20 min** · requiere M1

### Pasos

1. `python labs/lab03_sortes_ecvrf.py`
2. Confirma que la prueba mide exactamente **80 bytes** (`80 bytes = <hex>…`).
3. Observa `beta` (la salida aleatoria verificable) y `verify: True`.
4. `courselib/randomness.py` → `ecvrf_draw()`: `sk_to_pk` → `prove(sk, alpha)` → `verify(pk, alpha, pi)`.

### Salida esperada

- `proof: 80 bytes = <hex>…`, `result: beta=<hex>…`, `verify: True`
- `trace` con un evento `ecvrf` (`proof_len=80, verified=True`)

### Autocomprobación

- [ ] Explicas «una beta por (pk, alpha)» y por qué bloquea la iteración
- [ ] Verificaste que la prueba mide **80 bytes** (la cifra de verificación sin conexión del tagline)

---

## M4 — Time-lock RSW con Aestus

**Concepto:** un puzzle time-lock RSW. Sella un valor ahora; cualquiera puede abrirlo solo tras `T` cuadrados secuenciales — cifra ahora, descifra tras un retardo demostrable. El bloque básico para pujas selladas y commit-reveal donde nadie debe espiar antes de tiempo.
**Lab:** `labs/lab04_aestus_timelock.py` · **~20 min** · requiere M2

### Pasos

1. `python labs/lab04_aestus_timelock.py`
2. Observa el ciclo seal → open: `T=350` cuadrados, luego el payload abierto y `verify: True`.
3. `courselib/randomness.py` → `timelock_seal()`: `rsw.seal(message, T=...)` → `rsw.open_puzzle(puzzle)`; `message_match` confirma que el texto plano volvió intacto.

### Salida esperada

- `proof: T=350 squarings`, `result: <payload abierto>`, `verify: True`
- `trace` con un evento `timelock` (`T=350, opened=True`)

### Autocomprobación

- [ ] Explicas por qué un time-lock oculta un valor sin tercero de confianza
- [ ] Viste el mensaje sellado recuperado tras `T` cuadrados

---

## M5 — Commit–reveal y ataques de sesgo

**Concepto:** el módulo clave. Construye una lotería que un operador deshonesto puede iterar, demuestra el sesgo, y luego sustituye el sorteo por un Sortes ECVRF que el operador **no** puede iterar.
**Lab:** `labs/lab05_commit_reveal.py` · **~25 min** · track: economía · requiere M3

### Pasos

1. `python labs/lab05_commit_reveal.py`
2. Compara los dos billetes: `billete sesgado` vs `billete VRF justo`. La línea `verify VRF: True` prueba que el sorteo justo lleva una prueba verificable.
3. Lee la **nota de auditoría** que imprime el lab: «El sorteo justo vincula una beta por cada seed — el operador no puede iterar.»
4. `courselib/randomness.py` → `BiasedLottery` (hasta 200 intentos iterando `operator_secret|player_seed|attempt` por un jackpot) vs `FairLottery` (un sorteo ECVRF → un billete, iteración imposible).

### Salida esperada

- `billete sesgado: <n>` y `billete VRF justo: <n>`, `verify VRF: True`, la línea de la nota de auditoría
- `trace` con eventos `commit` y `draw` (`vrf_ok=True`)

### Autocomprobación

- [ ] Describes el ataque de iteración que realiza `BiasedLottery`
- [ ] Explicas por qué `FairLottery` (una beta por seed) es inmune

---

## M6 — Verificación on-chain

**Concepto:** empaqueta las pruebas para un consumidor on-chain — un vector VDF de Wesolowski con la forma que espera un verificador en Solidity, más una palabra de lotería de 32 bytes derivada de la beta de Sortes ECVRF.
**Lab:** `labs/lab06_onchain_consumer.py` · **~20 min** · track: avanzado · requiere M2, M3

### Pasos

1. `python labs/lab06_onchain_consumer.py`
2. Fíjate en la línea `protocolo: wesolowski-vdf`, `verify: True` y la `palabra de lotería: 0x…` de 32 bytes.
3. `courselib/randomness.py` → `onchain_vdf_vector()` (emite `scheme/seed/difficulty/y/pi/l/valid` como cadenas listas para un verificador) y `lottery_word_from_vrf()` (los primeros 32 bytes de la beta ECVRF).
4. **Puente:** el lab imprime una nota de despliegue que apunta a [lottery/docs/deployments-base.md](https://github.com/alexar76/lottery/blob/main/docs/deployments-base.md) — el verificador `ChronosVDF.sol` en vivo en Base.

### Salida esperada

- `protocol: wesolowski-vdf`, `verify: True`, `palabra de lotería: 0x<hex>…`, la línea de la nota de despliegue
- `trace` con eventos `onchain_vdf` y `lottery_word`

### Autocomprobación

- [ ] Nombras los dos artefactos que necesita un consumidor on-chain (vector VDF + palabra VRF)
- [ ] Sabes dónde encontrar la documentación de despliegue en Base

---

## Leer la traza (en cada lab)

**Concepto:** cada lab registra una pequeña `Trace` (ver `courselib/trace.py`) para que el comportamiento del agente/oráculo sea inspeccionable, no magia.

### Pasos (tras cada lab)

1. Baja al bloque `trace (<n> eventos):` al final de la salida del lab.
2. Lee cada evento — `kind` más los campos que registró el lab (`chaos_draw` → `verified, bytes`; `vdf_eval` → `difficulty, valid`; `tamper_check` → `valid=False`).
3. Mapea cada evento a una línea de stdout encima. La traza es el «registro de tests unitarios» de la aleatoriedad verificable.

### Autocomprobación

- [ ] Señalas el evento que prueba que un sorteo se verificó
- [ ] En M2 encuentras el evento `tamper_check` con `valid=False`

---

## Ejercicios y certificado

Tras los labs, ejecuta las comprobaciones DIY. Cada módulo tiene un ejercicio autocontenido en `courselib/exercises.py` (M2 manipula un VDF y comprueba que la verificación falla; M3 comprueba que la prueba mide exactamente 80 bytes; M5 comprueba que el sorteo justo verifica):

```bash
python labs/run_exercises.py                       # corre los seis, imprime ✓/✗ por módulo
python labs/run_exercises.py --module m3           # corre solo la comprobación de un módulo
```

Cuando los seis pasen, emite tu certificado:

```bash
python labs/run_exercises.py --certificate "Tu Nombre" --lang es   # o --lang en / ru
```

Escribe `certificate.html` — ábrelo en un navegador y **Print → Save as PDF**. El ID de credencial se deriva de forma determinista del nombre + la fecha de emisión (`courselib/certificate.py`). El certificado queda bloqueado hasta que pasen los ejercicios, salvo que pases `--skip-check`.

---

## Puente: del curso a la lotería en Base

**Objetivo:** las mismas pruebas que produjiste en local son las que verifican los contratos AIMarket `lottery/` en Base.

| Curso | Lotería en Base |
|-------|-----------------|
| M2 vector Chronos VDF | verificador de Wesolowski `ChronosVDF.sol` |
| M3 beta Sortes ECVRF | palabra de lotería de 32 bytes (M6 `lottery_word_from_vrf`) |
| M5 sorteo justo vs sesgado | por qué el consumidor usa VRF y no un beacon de confianza |
| M6 `onchain_vdf_vector()` | el vector exacto `{y, pi, l}` que consume el verificador |

Las direcciones de despliegue y el verificador en Solidity están en [lottery/docs/deployments-base.md](https://github.com/alexar76/lottery/blob/main/docs/deployments-base.md).

---

## Lista de autocomprobación

Track básico:

- [ ] Ejecutas lab01–lab04 en local (y en Colab) en EN, RU, ES
- [ ] Explicas chaos VRF, VDF, ECVRF y time-lock en una frase cada uno
- [ ] Muestras que un VDF manipulado falla la verificación (M2)
- [ ] Enuncias por qué una prueba ECVRF de 80 bytes se verifica sin conexión (M3)

Tracks economía + avanzado:

- [ ] Ejecutas lab05 y describes el ataque de iteración + el arreglo con VRF
- [ ] Ejecutas lab06 y produces un vector VDF + palabra de lotería listos para Base
- [ ] `pytest -q` en verde y `python labs/run_exercises.py` todo ✓

---

## Problemas frecuentes

| Problema | Solución |
| --- | --- |
| `No module named 'chronos'` | `pip install -e ".[oracles]"`, o ejecuta desde el monorepo aicom |
| `No module named 'oracle_core'` | `oracles/core` debe estar en la ruta — automático en el monorepo; lo trae `[oracles]` para Sortes/Platon |
| `Oracle package '…' not installed` | fuera del monorepo y sin el extra — instala `.[oracles]` o clona junto a `oracles/` |
| Falla el import de Platon | instala `numpy`; comprueba que existe `oracles/oracles/platon/backend` |
| Lab VDF lento | los labs usan ~700 cuadrados (M2) / `T=350` (M4) — baja la dificultad solo en tu propio ejercicio |
| Cadenas RU/ES vacías | `export COURSE_LANG=ru\|es`; las claves de `i18n/ru.json` deben coincidir con `i18n/en.json` |
| Fallo i18n en `pytest` | añade la clave que falta a **los tres** catálogos (en/ru/es) |
| Código viejo en Colab | reejecuta la celda de setup; fija la rama `main` |

---

## Regenerar sitio y notebooks

Tras editar labs o i18n:

```bash
python3 scripts/build_course_assets.py
```

Las guías en `docs/` se mantienen a mano — actualiza EN primero, luego los espejos RU/ES.
