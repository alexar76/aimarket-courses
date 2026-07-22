# Guía paso a paso del curso

> **Audiencia:** ingenieros que quieren primitivas inspiradas en la física —consenso, enrutamiento, muestreo, riesgo, termodinámica— como oráculos AIMarket listos para invocar.
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · UI en `i18n/` · esta guía en español.
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

La mayoría de los cursos de «IA» se quedan en los prompts. Este enseña **cómputo determinista inspirado en la física** que puedes verificar, certificar y facturar: el tipo de primitiva que está *debajo* de un agente, no encima. Cada módulo envuelve un oráculo AIMarket real:

- **Murmuration** — consenso de enjambre robusto que sobrevive a los valores atípicos.
- **Colony** — rutas TSP que vienen con un *certificado admisible de brecha de optimalidad*.
- **Turing** — muestreo de ruido azul para conjuntos de puntos uniformes pero irregulares.
- **Ablation** — riesgo sistémico modelado como una cascada en un modelo de arena auto-organizado-crítico.
- **Landauer** — un umbral termodinámico (kT·ln2) sobre el coste energético del cómputo irreversible.

Cada lab es **reproducible** (con semilla, sin LLM por defecto) e imprime un bloque `Trace` que puedes inspeccionar. Al final podrás invocar cualquiera de los cinco oráculos, leer su salida y obtener un certificado del curso.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 min)](#instalación-10-min)
3. [M1 — Consenso Murmuration](#m1--consenso-murmuration)
4. [M2 — Certificado TSP de Colony](#m2--certificado-tsp-de-colony)
5. [M3 — Ruido azul de Turing](#m3--ruido-azul-de-turing)
6. [M4 — Riesgo de cascada Ablation](#m4--riesgo-de-cascada-ablation)
7. [M5 — Auditoría termodinámica Landauer (avanzado)](#m5--auditoría-termodinámica-landauer-avanzado)
8. [Traza en cada lab](#traza-en-cada-lab)
9. [Ejercicios y certificado](#ejercicios-y-certificado)
10. [Puente: del curso a AIMarket](#puente-del-curso-a-aimarket)
11. [Lista de autocomprobación](#lista-de-autocomprobación)
12. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | NumPy | LLM |
|-------|---------|--------|-------|-----|
| **Básico** | M1 → M2 → M3 → M4 | ~2 h | Sí (`[oracles]`) | No |
| **Avanzado** | Básico + M5 | +45 min | Sí | No |

Todos los labs son deterministas — en este curso **no hay LLM**. La «inteligencia» está en la física: estadística robusta, cotas combinatorias, criticidad, termodinámica. Lee la sección [Traza](#traza-en-cada-lab) tras cada lab — cada script imprime un bloque `Trace`.

---

## Instalación (10 min)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/physics-inspired-computing-course
pip install -e ".[oracles,dev]"
```

El extra `[oracles]` instala **NumPy** (la única dependencia en tiempo de ejecución); `[dev]` añade pytest. Se requiere Python **3.11+**.

> **¿Dentro del monorepo aicom?** Puedes omitir los wheels de oráculos — los labs resuelven `murmuration`, `colony`, `turing`, `ablation` y `landauer` directamente desde `oracles/oracles/*` vía `courselib/oracle_paths.py`. Fuera del monorepo, `[oracles]` es lo que hace funcionar los imports.

### Paso 2 — Verificar los tests

```bash
pytest -q
```

**Esperado:** todos los tests pasan (paridad i18n entre `en/ru/es`, puentes de oráculos, certificado, ejercicios).

### Paso 3 — Elegir idioma (opcional)

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_murmuration_consensus.py
```

`COURSE_LANG` cambia las cadenas impresas de cada lab (títulos, conceptos, etiquetas) vía `courselib/i18n.py`. Los números, los nombres de los oráculos y los tipos de evento de la traza no cambian — solo se localiza el texto. Los valores desconocidos recurren al inglés y nunca rompen el lab.

### Paso 4 — Alternativa en Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/physics-inspired-computing-course/) → **Open in Colab** en cualquier lab.
2. Ejecuta la **celda de setup** (clone + `pip install -e ".[oracles,dev]"`).
3. Si lo necesitas, define `os.environ["COURSE_LANG"] = "es"` en la celda de setup.
4. Ejecuta la celda del lab.

---

## M1 — Consenso Murmuration

**Concepto:** consenso robusto DeGroot y agregación Tukey-biweight sobre estimaciones ruidosas de agentes.
**Lab:** `labs/lab01_murmuration_consensus.py` · **Oráculo:** Murmuration · **~15 min** · **track:** básico

### Pasos

1. Lee el docstring al inicio del lab (sectores: *inteligencia de enjambre, estadística robusta*).
2. Ejecuta: `python labs/lab01_murmuration_consensus.py`
3. El lab alimenta seis estimaciones —cinco cerca de `2.0` más un atípico extremo `50.0`— al oráculo e imprime `median`, `trimmed_mean`, `biweight`, el valor `converged` y el número de iteraciones DeGroot, y al final un bloque `Trace`.
4. Observa que `biweight` ≈ 2.0 aunque la media bruta sería ~10 — el atípico se **resiste**, no se promedia.
5. Revisa `courselib/physics.py::murmuration_aggregate` y `murmuration.consensus.aggregate`.

### Qué demuestra

Un único sensor defectuoso (o un agente malicioso) no puede arrastrar el consenso. El estimador biweight reduce el peso de los puntos lejanos, así que el enjambre coincide en la verdad, no en el ruido.

### Autocomprobación

- [ ] Explicas por qué `biweight` < media para esta entrada
- [ ] Ves por qué el lab es determinista (sin LLM, datos con semilla)

---

## M2 — Certificado TSP de Colony

**Concepto:** ruta vecino más cercano + 2-opt con una **cota admisible de brecha de optimalidad**.
**Lab:** `labs/lab02_colony_tsp.py` · **Oráculo:** Colony · **~20 min** · requiere M1

### Pasos

1. Ejecuta: `python labs/lab02_colony_tsp.py`
2. El lab resuelve una ruta de 6 ciudades e imprime `tour` (orden de visita), `length`, `lower_bound` (un piso demostrable sobre la longitud óptima) y `gap` en porcentaje — cuánto *podría* alejarse la ruta del óptimo.
3. Lee el bloque `Trace` — el evento `tsp` registra `length` y `gap`.
4. La idea clave: siempre `length ≥ lower_bound`, así que `gap` es un **certificado**. Entregas la ruta *junto con* una garantía de su calidad.

### Qué demuestra

No necesitas el óptimo exacto para actuar — un `gap` pequeño (digamos < 5%) suele ser una respuesta lo bastante buena con un número adjunto. Así se vuelven responsables las heurísticas.

### Autocomprobación

- [ ] Lees el `gap` y dices «esta ruta es como mucho un X% peor que el óptimo»
- [ ] Entiendes por qué `length` nunca está por debajo de `lower_bound`

---

## M3 — Ruido azul de Turing

**Concepto:** muestreo por mejor candidato (Mitchell) para conjuntos de puntos uniformes pero irregulares.
**Lab:** `labs/lab03_turing_bluenoise.py` · **Oráculo:** Turing · **~20 min** · requiere M1

### Pasos

1. Ejecuta: `python labs/lab03_turing_bluenoise.py`
2. El lab pide 64 puntos (`candidates=12`, `seed=2026`) e imprime `count`, `min_distance` (la menor separación entre dos puntos cualesquiera), `seed` y su `seed_source`, y un `sample` de 3 coordenadas.
3. Compáralo con una dispersión aleatoria uniforme: el ruido azul **maximiza la distancia mínima**, así que no hay grumos ni huecos.
4. Re-ejecuta con otra `seed` (editando el lab) — la disposición cambia pero `min_distance` sigue alta.

### Qué demuestra

El muestreo de ruido azul supera al aleatorio ingenuo para Monte Carlo, dithering y colocación procedural: cobertura uniforme sin estructura visible.

### Autocomprobación

- [ ] Explicas por qué el objetivo es una `min_distance` alta
- [ ] Ves que `seed` hace reproducible la muestra

---

## M4 — Riesgo de cascada Ablation

**Concepto:** modelo de arena abeliano con auto-organización crítica — tamaños de avalancha con ley de potencias y riesgo de cola.
**Lab:** `labs/lab04_ablation_cascade.py` · **Oráculo:** Ablation · **~20 min** · requiere M1

### Pasos

1. Ejecuta: `python labs/lab04_ablation_cascade.py`
2. El lab construye un pequeño **grafo de exposición** dirigido (`demo_exposure_graph()` — bancos A→D más un sumidero), suelta 1200 granos e imprime `tau` (el exponente de ley de potencias de la distribución de tamaños de avalancha), `max_avalanche` (la mayor cascada observada), `cvar95` (el VaR condicional al 95% — tamaño esperado del peor 5% de cascadas) y `topple_total`.
3. Lee el bloque `Trace` — el evento `cascade` registra `tau` y `max_avalanche`.
4. La intuición: en un sistema crítico, pequeñas perturbaciones a veces desencadenan cascadas **a nivel de todo el sistema**. `tau` y `cvar95` cuantifican esa cola.

### Qué demuestra

El comportamiento promedio oculta el peligro. Una cola pesada (gobernada por `tau`) significa que cascadas raras pero enormes dominan el riesgo — justo el modo de fallo de las redes financieras o de infraestructura interconectadas.

### Autocomprobación

- [ ] Explicas por qué el tamaño *medio* de avalancha subestima el riesgo
- [ ] Sabes qué mide `cvar95` frente a un simple promedio

---

## M5 — Auditoría termodinámica Landauer (avanzado)

**Concepto:** el umbral de energía de borrado de bit kT·ln2 sobre un DAG de operaciones.
**Lab:** `labs/lab05_landauer_audit.py` · **Oráculo:** Landauer · **~30 min** · **track:** avanzado

### Pasos

1. Ejecuta: `python labs/lab05_landauer_audit.py`
2. El lab audita un pequeño circuito irreversible (`demo_circuit_ops()` — dos entradas, una puerta AND, una salida) a `temperature_k=300.0` e imprime `irreversible_bits` (bits destruidos por la lógica), `energy_floor_j` (el umbral de Landauer en julios, kT·ln2 por bit borrado), `efficiency` y `circuit_commitment` — un hash que fija el circuito auditado.
3. Lee el bloque `Trace` — el evento `landauer` registra `bits` y `floor_j`.
4. La física: borrar un bit a temperatura T cuesta **al menos** kT·ln2 julios. Una puerta AND destruye información (dos entradas → una salida), así que tiene un umbral no nulo.

### Qué demuestra

Hay una cota inferior dura, dependiente de la temperatura, sobre la energía que todo cómputo irreversible debe disipar. La auditoría convierte esa ley física en un número atribuible a un circuito, y el `circuit_commitment` hace la auditoría a prueba de manipulaciones.

### Autocomprobación

- [ ] Nombras el umbral kT·ln2 y qué significa cada término
- [ ] Entiendes por qué la puerta AND tiene `irreversible_bits ≥ 1`

---

## Traza en cada lab

**Concepto:** cada lab registra una `Trace` para que su comportamiento sea inspeccionable, no magia.
**Cubierto en:** los cinco labs · **~5 min tras cada lab**

Cada script construye una `courselib.trace.Trace` y llama a `trace.log(kind, **fields)`. El lab imprime cuántos `events` registró; el `kind` (`consensus`, `tsp`, `bluenoise`, `cascade`, `landauer`) indica qué primitiva física se ejecutó y los campos capturan las cifras principales.

### Pasos (tras cada lab)

1. Desplázate hasta la línea `trace` / `events` al final de la salida.
2. Mapea el `kind` y los campos al bloque de resultado que acabas de leer.
3. Trata la traza como el «log de test unitario» del lab — en producción se convierten en recibos de facturación y registros de auditoría.

### Autocomprobación

- [ ] Emparejas cada evento de la traza con un resultado impreso
- [ ] Ves la traza como el puente de la salida del lab a un recibo verificable

---

## Ejercicios y certificado

Tras los labs, ejecuta las comprobaciones DIY:

```bash
python labs/run_exercises.py
```

Esto corre los ejercicios de los cinco módulos (`m1`–`m5`) e imprime un `✓`/`✗` por módulo. Mientras iteras, ejecuta de uno en uno:

```bash
python labs/run_exercises.py --module m4
```

Cada ejercicio comprueba la propiedad que enseña el lab — p. ej. `m1` verifica que `biweight` resiste un atípico, `m2` que `length ≥ lower_bound`, `m4` que `tau > 0.5`.

Cuando los cinco pasen, genera tu certificado:

```bash
python labs/run_exercises.py --certificate "Tu Nombre" --lang es
```

Esto escribe `certificate.html` (usa `--lang en` o `--lang ru` para otra localización). Ábrelo en un navegador y **Print → Save as PDF**. El ID de credencial es un hash de nombre + fecha, así que es estable y verificable. Pasa `--skip-check` solo si quieres el HTML sin re-ejecutar los ejercicios.

---

## Puente: del curso a AIMarket

Los cinco oráculos que invocaste localmente son los mismos paquetes que se sirven en vivo en el ecosistema AIMarket. Para pasar de «ejecuté el lab» a «invoqué un oráculo alojado»:

| Curso (lab local) | AIMarket (oráculo alojado) |
|-------------------|----------------------------|
| M1 `murmuration_aggregate` | Oráculo Murmuration — capability de consenso |
| M2 `colony_tsp` | Oráculo Colony — enrutamiento + certificado |
| M3 `turing_bluenoise` | Oráculo Turing — capability de muestreo |
| M4 `ablation_cascade` | Oráculo Ablation — capability de riesgo sistémico |
| M5 `landauer_audit` | Oráculo Landauer — auditoría termodinámica |
| `Trace` del lab | Recibo de invoke + provenance alojado |

El `circuit_commitment` (M5) y el certificado `gap` (M2) son justo el tipo de salida verificable que permite a un comprador confiar en la respuesta de un oráculo sin volver a calcularla.

---

## Lista de autocomprobación

Tras el track **básico** deberías poder:

- [ ] Ejecutar lab01–lab04 en local y en Colab
- [ ] Explicar el consenso robusto (M1) y por qué se resiste el atípico
- [ ] Leer un certificado `gap` de TSP (M2) como garantía de calidad
- [ ] Decir por qué el ruido azul (M3) supera al aleatorio uniforme en cobertura
- [ ] Describir qué capturan `tau`/`cvar95` sobre el riesgo de cascada (M4)
- [ ] Leer un bloque `Trace` y emparejar cada evento con un resultado

Tras el track **avanzado** añade:

- [ ] Ejecutar lab05 y enunciar el umbral kT·ln2 con palabras
- [ ] Pasar los cinco ejercicios y generar un certificado

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: courselib` | Ejecuta desde la raíz del repo; los labs anteponen el directorio padre a `sys.path` |
| `ImportError: Oracle package '…' not installed` | Ejecuta `pip install -e ".[oracles]"`, o ejecuta desde el monorepo aicom para que `oracles/oracles/*` se resuelva |
| `ModuleNotFoundError: numpy` | El extra `[oracles]` instala NumPy — repite `pip install -e ".[oracles,dev]"` |
| Error de versión de Python | El curso requiere **Python 3.11+** |
| Cadenas vacías / en inglés con otro idioma | Define `COURSE_LANG`; comprueba que la clave exista en `i18n/ru.json` / `i18n/es.json` |
| Fallo de paridad i18n en pytest | Añade la clave que falta a **los tres** archivos `i18n/en.json`, `ru.json`, `es.json` |
| El certificado no se genera | Primero deben pasar los ejercicios; ejecuta `python labs/run_exercises.py`, o pasa `--skip-check` |
| Colab ejecuta código viejo | Re-ejecuta la celda de setup; fija la rama `main` |

---

## Regenerar sitio y notebooks

Tras editar labs o `i18n/`:

```bash
python3 scripts/build_course_assets.py
```

Las guías en `docs/` se mantienen a mano — actualiza EN primero, luego refleja las versiones RU/ES.
