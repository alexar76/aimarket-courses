# Guía paso a paso del curso

> **Audiencia:** desarrolladores que aprenden patrones de smart-contracts de lotería antes de tocar Base mainnet.  
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · UI en `i18n/` · esta guía en español.  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

Las loterías on-chain fallan cuando el **operador** puede repetir un sorteo en silencio hasta que le guste el ganador: el ataque de *grinding*. Los contratos `lottery/` en Base lo cierran con aleatoriedad verificable (ECVRF mediante el oráculo **Sortes**) y una baliza VDF de Wesolowski del oráculo **Chronos**, liquidando los pagos por un canal de depósito en garantía **AIMarketEscrow** con débito autorizado por recibo. El curso enseña cada uno de esos primitivos como un port en Python pequeño, ejecutable y sin LLM. Verificas el **mismo** vector de test de Foundry que usan los contratos Solidity (`ChronosVDF.t.sol`), recorres una ronda del relayer de principio a fin y terminas con un proyecto final que simula una ronda justa completa con artefactos verificables, de modo que lo aprendido se traslada directamente al código de producción `lottery/`.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 min)](#instalación-10-min)
3. [M1 — Sorteo de lotería insesgable](#m1--sorteo-de-lotería-insesgable)
4. [M2 — Verificación de VDF on-chain](#m2--verificación-de-vdf-on-chain)
5. [M3 — Depósito en garantía y canales de pago](#m3--depósito-en-garantía-y-canales-de-pago)
6. [M4 — Ciclo de vida de la ronda del relayer](#m4--ciclo-de-vida-de-la-ronda-del-relayer)
7. [M5 — Proyecto final: ronda justa](#m5--proyecto-final-ronda-justa)
8. [Ejercicios y certificado](#ejercicios-y-certificado)
9. [Observabilidad en cada lab](#observabilidad-en-cada-lab)
10. [Puente: del curso a lottery/](#puente-del-curso-a-lottery)
11. [Lista de autocomprobación](#lista-de-autocomprobación)
12. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Oráculos |
|-------|---------|--------|----------|
| **Básico** | M1 → M4 | ~1,5 h | Sortes + Chronos (fallback si no están instalados) |
| **Avanzado** | Básico + M5 proyecto final | +30 min | Sortes + ruta Chronos VDF |
| **Puente lottery/** | Tras M4 o M5 | +30 min | `forge test` en vivo + contratos en Base |

Tras **cada** lab revisa el bloque `Trace` (sección Observabilidad).

---

## Instalación (10 min)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/smart-contracts-course
pip install -e ".[oracles,dev]"
```

El extra `[oracles]` conecta los paquetes de los oráculos **Sortes** (ECVRF) y **Chronos** (VDF). Si el extra no está disponible en tu entorno, los labs igual se ejecutan: `courselib` recurre a una implementación determinista de la stdlib y la traza marca `oracle=fallback`. Se requiere Python 3.11+.

### Paso 2 — Verificar los tests

```bash
pytest -q
```

**Esperado:** todos los tests pasan (paridad de i18n en en/ru/es, primitivos de contratos, el vector de Foundry incluido, render del certificado).

### Paso 3 — Ejecutar el primer lab

```bash
python labs/lab01_unbiasable_draw.py
python labs/run_exercises.py
```

### Paso 4 — Elegir idioma (opcional)

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_unbiasable_draw.py
```

`COURSE_LANG` solo cambia las cadenas que imprime el lab (títulos de módulo, etiquetas, pistas); el código, los comandos, los números de boleto y el vector de Foundry son idénticos en todos los idiomas.

### Paso 5 — Alternativa en Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/smart-contracts-course/) → **Open in Colab** en cualquier lab.
2. Ejecuta la **celda de setup** (clone + `pip install -e ".[oracles,dev]"`).
3. Si lo necesitas, en la celda de setup: `os.environ["COURSE_LANG"] = "es"`.
4. Ejecuta la celda del lab.

---

## M1 — Sorteo de lotería insesgable

**Concepto:** Commit–reveal y ECVRF cierran los ataques de grinding del operador.  
**Lab:** `labs/lab01_unbiasable_draw.py` · **~15 min**

### Pasos

1. `python labs/lab01_unbiasable_draw.py`
2. Compara los dos sorteos en la salida:
   - **Lotería sesgada (grinding del operador)** — `grindable=True`: el operador rehashéa con un secreto hasta que sale un boleto favorable (`BiasedLottery.operator_can_grind`).
   - **Lotería justa (ECVRF)** — un `alpha` mapea a exactamente un `beta`, con `verified=True`. El operador no puede repetir.
3. Abre `courselib/contracts.py` — `BiasedLottery`, `FairLottery`, `_sortes_draw` (la ruta ECVRF de Sortes con fallback de stdlib).
4. **Ejercicio:** `python labs/run_exercises.py --module m1` — el sorteo justo se verifica mientras el sesgado hace grinding.

**Qué demuestra:** un sorteo verificable elimina la discreción del operador. Consumidor on-chain: `lottery/docs/` y `AIAgentLottery.sol`.

---

## M2 — Verificación de VDF on-chain

**Concepto:** Las pruebas Wesolowski de Chronos coinciden con los vectores de test de Foundry.  
**Lab:** `labs/lab02_vdf_verify.py` · **~15 min** · requiere M1

### Pasos

1. `python labs/lab02_vdf_verify.py`
2. El lab carga el vector de Foundry incluido (`courselib/fixtures/chronos_vector.json`, copia de `lottery/contracts/test/vectors/chronos_vector.json`) y verifica `π^l·g^r ≡ y (mod N)`. Salida: `verify: True (AB_equals_y=True)`.
3. Si el oráculo Chronos está instalado, `verify_wesolowski_vector` además re-deriva la prueba en vivo (`hash_to_group → evaluate → prove → verify`).
4. **Ejercicio:** `python labs/run_exercises.py --module m2`.

**Qué demuestra:** el verificador de Python y el de Solidity coinciden sobre los mismos bytes. Ejecuta `forge test` en `lottery/contracts` — `ChronosVDF.t.sol` usa el mismo vector.

---

## M3 — Depósito en garantía y canales de pago

**Concepto:** Retener fondos hasta la entrega; débito autorizado por recibo, como en AIMarketEscrow.  
**Lab:** `labs/lab03_escrow_channel.py` · **~20 min** · requiere M1

### Pasos

1. `python labs/lab03_escrow_channel.py`
2. Ciclo de vida del canal: **open** (depósito) → **debit** (por recibo) → **settle** (reparto entre hub y reembolso).
3. Línea **Reuso de recibo**: un segundo `debit` con el mismo `receipt_id` se rechaza (`blocked=True`) — es la protección contra repetición, `EscrowChannel.used_receipts`.
4. `courselib/contracts.py` → `EscrowChannel` modela `AIMarketEscrow` open/debit/settle (Protocol v2 §6): firma, nonce, coincidencia de hub, control de saldo.
5. **Ejercicio:** `python labs/run_exercises.py --module m3` — debita dos veces con un recibo; el segundo debe fallar.

---

## M4 — Ciclo de vida de la ronda del relayer

**Concepto:** baseSeed, sorteo de Sortes, ruta opcional de VDF on-chain.  
**Lab:** `labs/lab04_relayer_round.py` · **~20 min** · requiere M1–M2

### Pasos

1. `python labs/lab04_relayer_round.py`
2. Tres fases en la salida y en el bloque `Trace`:
   - **Semilla de Chronos** — `base_seed = sha256(roundId ‖ blockhash ‖ platonRandom)`.
   - **Boleto de Sortes** — el sorteo verificable de la ronda (`verified=True`).
   - **Vector VDF** — con `onchain_vdf=True` la ronda adjunta una baliza `VdfProof` y reverifica el vector de Foundry (`vector_valid=True`).
3. Lectura cruzada: `lottery/relayer/ailottery_relayer/economy_draw.py` — el flujo de sorteo de producción que este lab refleja.
4. **Ejercicio:** `python labs/run_exercises.py --module m4` — traza `baseSeed → Sortes → baliza VDF`.

---

## M5 — Proyecto final: ronda justa

**Concepto:** Simula una ronda completa de lotería con artefactos verificables.  
**Lab:** `labs/lab05_lottery_capstone.py` · **~30 min** · requiere M1–M4 · **track:** avanzado

### Pasos

1. `python labs/lab05_lottery_capstone.py`
2. El lab llama a `simulate_fair_round(onchain_vdf=True, client_seed=...)` e imprime los artefactos de la ronda: `ticket`, `vdf_path=onchain` y `chronos_vector=True`.
3. Compara estos artefactos con un log real de `lottery/relayer` — cada campo tiene su contraparte de producción.
4. **Ejercicio:** `python labs/run_exercises.py --module m5` — ejecuta `simulate_fair_round` con `onchain_vdf=True`.

**Qué demuestra:** ensamblas los primitivos M1–M4 en una sola ronda auditable — un boleto verificable, una baliza VDF y un vector comprobable: los artefactos que un jugador necesita para confiar en el resultado sin confiar en el operador.

---

## Ejercicios y certificado

```bash
python labs/run_exercises.py                 # todos los módulos
python labs/run_exercises.py --module m3     # un módulo
```

Cada módulo imprime `✓` o `✗`; corrige los fallos y reejecuta. Cuando todo pasa, genera el certificado:

```bash
python labs/run_exercises.py --certificate "Tu Nombre" --lang es
```

Esto escribe `certificate.html` (cámbialo con `-o`). Ábrelo en un navegador y **Imprimir → Guardar como PDF**. El ID de la credencial se deriva de nombre + fecha (`courselib/certificate.py`). También puedes generarlo desde la sección **Certificado** del sitio del curso.

---

## Observabilidad en cada lab

Tras cada lab (5 min):

1. Bloque **trace** al final de la salida.
2. Mapea los `events` a los pasos en stdout: `biased_draw`, `fair_draw`, `vdf_verify`, `open`/`debit`/`settle`, `base_seed`/`sortes_draw`/`vdf_beacon`, `capstone`.
3. En M4, correlaciona los tres eventos de la traza con las tres fases impresas.

La traza es el «log de eventos on-chain» de la ronda: por ella encuentras el evento que demuestra que el sorteo fue justo.

---

## Puente: del curso a lottery/

1. **Vector de Foundry** — `lottery/contracts/test/vectors/chronos_vector.json` (incluido en `courselib/fixtures/`). El verificador del curso lee el mismo archivo que el test de Solidity.
2. **Verificador on-chain** — `lottery/contracts/src/ChronosVDF.sol`, su test `ChronosVDF.t.sol`:

   ```bash
   cd lottery/contracts && forge test
   ```

3. **Flujo de sorteo del relayer** — `lottery/relayer/ailottery_relayer/economy_draw.py` (reflejado por M4).
4. Tabla curso → lottery/:

   | Curso | lottery/ |
   |-------|----------|
   | M1 sorteo justo | Sortes ECVRF + `AIAgentLottery.sol` |
   | M2 verificación VDF | `ChronosVDF.sol` + `ChronosVDF.t.sol` |
   | M3 canal de garantía | `AIMarketEscrow` open/debit/settle |
   | M4 ronda del relayer | `economy_draw.py` |
   | M5 proyecto final | Ronda completa + baliza VDF on-chain |

5. **Docs:** [lottery/docs/](https://github.com/alexar76/lottery/tree/main/docs).

---

## Lista de autocomprobación

Track básico:

- [ ] labs 01–04 en local y en Colab
- [ ] Explicas por qué un sorteo verificable vence al grinding del operador
- [ ] Verificas el vector de Foundry de Chronos y lo conectas con `ChronosVDF.t.sol`
- [ ] Describes el flujo open → debit → settle y la protección contra repetición
- [ ] Lees un bloque `Trace` y encuentras el evento de equidad

Track avanzado:

- [ ] lab05 + enumerar los artefactos de una ronda justa
- [ ] `forge test` en `lottery/contracts` y su relación con M2

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: courselib` | Ejecutar desde la raíz del repo |
| Falla el import del oráculo / error en `pip install ".[oracles]"` | Los labs igual corren con el fallback de stdlib (`oracle=fallback`); para la ruta ECVRF/VDF en vivo, ejecuta desde el monorepo aicom donde se resuelve `oracles/` |
| `verify: False` en M2 | Confirma que `courselib/fixtures/chronos_vector.json` está intacto (`valid` y `AB_equals_y` deben ser true) |
| Cadenas RU/ES vacías | Define `COURSE_LANG`; las claves de `i18n/es.json` deben coincidir con `en.json` |
| Fallo de paridad de i18n en pytest | Añade la clave que falta en los tres `i18n/{en,ru,es}.json` |
| Colab con código viejo | Reejecuta la celda de setup; fija la rama `main` |

**Despliegue de lottery/ y on-chain:** [lottery/docs/](https://github.com/alexar76/lottery/tree/main/docs).

---

Las guías en `docs/` se mantienen a mano — primero EN, luego los espejos RU/ES.
