# Guía paso a paso del curso

> **Audiencia:** desarrolladores que construyen confianza entre agentes, reputación y auditorías de riesgo sistémico con oráculos de AIMarket.  
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · cadenas de UI en `i18n/` · esta guía en español.  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

Los sistemas multi-agente responden siempre a una misma pregunta: *¿en qué agente (o agregado, o ruta) confío, y puedo demostrarlo?* Este curso convierte esa pregunta en matemáticas ejecutables. Cinco oráculos vivos de AIMarket calculan las señales — **LUMEN** (PageRank/EigenTrust), **PERCOLA** (umbrales de percolación), **FOURIER** (conectividad espectral), **MURMURATION** (consenso robusto) y **ABLATION** (riesgo de cascada de pila de arena) — y cada señal viene con su propio **certificado de verificación**, así que nunca tienes que creer al oráculo bajo palabra. Los labs son NumPy determinista: sin claves de API ni red para el track básico.

Al terminar sabes puntuar un grafo de quién-confía-en-quién, detectar el nodo clave cuya eliminación lo fractura, medir qué tan cerca está de partirse, agregar estimaciones ruidosas frente a un adversario y cuantificar el riesgo de cola de una cascada sistémica — y luego reunir todo en una sola auditoría de confianza verificable.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 minutos)](#instalación-10-minutos)
3. [M1 — EigenTrust con LUMEN](#m1--eigentrust-con-lumen)
4. [M2 — Percolación y nodos clave](#m2--percolación-y-nodos-clave)
5. [M3 — Conectividad espectral](#m3--conectividad-espectral)
6. [M4 — Consenso robusto](#m4--consenso-robusto)
7. [M5 — Riesgo de cascada](#m5--riesgo-de-cascada)
8. [M6 — Proyecto final: matemáticas de la confianza](#m6--proyecto-final-matemáticas-de-la-confianza)
9. [Ejercicios y certificado](#ejercicios-y-certificado)
10. [Observabilidad en cada lab](#observabilidad-en-cada-lab)
11. [Puente: del curso a los oráculos en producción](#puente-del-curso-a-los-oráculos-en-producción)
12. [Lista de autocomprobación](#lista-de-autocomprobación)
13. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Oráculos |
|-------|---------|--------|----------|
| **Básico** | M1 → M2 → M3 → M4 | ~2 h | LUMEN, PERCOLA, FOURIER, MURMURATION |
| **Avanzado** | Básico + M5 cascada | +30 min | + ABLATION (pila de arena) |
| **Proyecto final** | M6 auditoría combinada | +20 min | LUMEN + FOURIER + PERCOLA juntos |

Hay **seis labs ejecutables** (`labs/lab01`–`lab06`), uno por módulo. Cada lab imprime un bloque `Trace` (traza) que puedes inspeccionar — es su registro de auditoría. Los labs que llaman a un oráculo verificable imprimen además `verify: True`: el resultado se reverificó de forma independiente, no solo se afirmó.

---

## Instalación (10 minutos)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/mathematics-of-trust-course
pip install -e ".[oracles,dev]"
```

**Desde el monorepo aicom** (recomendado para contribuidores):

```bash
cd courses/mathematics-of-trust-course
pip install -e ".[oracles,dev]"
```

Los cinco oráculos se resuelven automáticamente desde `oracles/oracles/*` al ejecutar dentro del monorepo.

**Clon independiente** sin el monorepo hermano:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
for pkg in lumen murmuration fourier percola ablation; do
  pip install -e _deps/oracles/oracles/$pkg
done
pip install -e ".[oracles,dev]"
```

### Paso 2 — Verificar tests

```bash
pytest -q
```

**Esperado:** paridad i18n, integración con oráculos de confianza, ejercicios, smoke-import de labs.

### Paso 3 — Elegir idioma (opcional)

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_keystone_nodes.py
```

### Paso 4 — Alternativa con Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/mathematics-of-trust-course/) → **Open in Colab** en cualquier lab.
2. Ejecuta la **celda de setup** (clone + pip + slice de oráculos).
3. Si hace falta: `os.environ["COURSE_LANG"] = "es"`.
4. Ejecuta la celda del lab.

---

## M1 — EigenTrust con LUMEN

**Concepto:** distribución estacionaria de PageRank sobre un grafo de quién-confía-en-quién.  
**Lab:** `labs/lab02_trust_pagerank.py` · **~20 min** · requiere instalación

### Pasos

1. `python labs/lab02_trust_pagerank.py`
2. Inspecciona el grafo didáctico en `courselib/trust.py` — `demo_trust_graph()`.
3. Observa las puntuaciones ordenadas: `hub` y los agentes bien conectados deben superar a los nodos periféricos.
4. Lee `oracles/oracles/lumen/lumen/pagerank.py` para el kernel EigenTrust (5 min).
5. **Ejercicio:** `python labs/run_exercises.py --module m1`.

### Autocomprobación

- [ ] Las puntuaciones suman 1 (distribución de probabilidad)
- [ ] La confianza transitiva eleva a los nodos en quienes confían los nodos de confianza

---

## M2 — Percolación y nodos clave

**Concepto:** eliminación dirigida de nodos y umbrales críticos en grafos de confianza.  
**Lab:** `labs/lab01_keystone_nodes.py` · **~20 min** · requiere instalación

### Pasos

1. `python labs/lab01_keystone_nodes.py`
2. Observa `f_c` — la fracción crítica de nodos cuya eliminación colapsa la conectividad.
3. Inspecciona `keystones` (nodos clave) — nodos puente entre dos cliques (`3`, `4`, `8` en el grafo didáctico).
4. Confirma `verify: True` — PERCOLA recalcula el umbral sin fiarse del oráculo.
5. **Ejercicio:** `python labs/run_exercises.py --module m2`.

### Autocomprobación

- [ ] Sabes explicar por qué un nodo puente es un nodo clave
- [ ] La verificación pasa sin repetir toda la búsqueda Monte Carlo

---

## M3 — Conectividad espectral

**Concepto:** valor de Fiedler y bisección espectral — ¿qué tan cerca está el grafo de partirse?  
**Lab:** `labs/lab03_spectral_cut.py` · **~20 min** · requiere M1 o M2

### Pasos

1. `python labs/lab03_spectral_cut.py`
2. Lee λ₂ (valor de Fiedler) — valores pequeños indican un cuello de botella estrecho.
3. Inspecciona el corte espectral — conjuntos A y B más la conductancia.
4. Abre `oracles/oracles/fourier/fourier/spectral.py` — `analyze()` y `verify()` (5 min).
5. **Ejercicio:** `python labs/run_exercises.py --module m3`.

### Autocomprobación

- [ ] El certificado del par propio de Fiedler se verifica en O(E)
- [ ] La conductancia cuantifica cuán «caro» es el corte

---

## M4 — Consenso robusto

**Concepto:** mediana, media recortada y estimador biweight de posición sobre estimaciones de agentes.  
**Lab:** `labs/lab04_consensus_aggregate.py` · **~15 min** · requiere instalación

### Pasos

1. `python labs/lab04_consensus_aggregate.py`
2. Compara media ingenua vs mediana vs biweight en `demo_agent_estimates()` (un valor atípico en 500).
3. Lee `murmuration/consensus.py` — puntos de ruptura (breakdown points) y número de iteraciones de DeGroot.
4. **Ejercicio:** `python labs/run_exercises.py --module m4`.

### Autocomprobación

- [ ] La mediana y el biweight resisten el valor atípico adversario
- [ ] DeGroot converge a la media aritmética en el grafo completo

---

## M5 — Riesgo de cascada

**Concepto:** avalanchas de pila de arena abeliana y riesgo de cola con ley de potencias.  
**Lab:** `labs/lab05_sandpile_cascade.py` · **~30 min** · requiere M1–M4

### Pasos

1. `python labs/lab05_sandpile_cascade.py`
2. Inspecciona τ (exponente de ley de potencias), la avalancha máxima y el CVaR 99%.
3. Lee los nodos disparadores principales — quién enciende con más frecuencia grandes cascadas.
4. Confirma `verify: True` — el total de derrumbes y τ se reproducen bit a bit.
5. **Ejercicio:** `python labs/run_exercises.py --module m5`.

### Autocomprobación

- [ ] Los tamaños de avalancha no dependen del orden (propiedad abeliana)
- [ ] Una cola pesada (τ pequeño) señala riesgo de contagio sistémico

---

## M6 — Proyecto final: matemáticas de la confianza

**Concepto:** combinar las señales de PageRank, espectral y percolación en una sola auditoría de confianza verificable.  
**Lab:** `labs/lab06_trust_audit.py` · **~20 min** · requiere M1–M3

### Pasos

1. `python labs/lab06_trust_audit.py`
2. Lee la auditoría de una línea sobre `demo_trust_graph()`:
   - Nodo **más confiable** y su puntuación PageRank (LUMEN) — se espera `hub`.
   - **Conectividad algebraica** λ₂ y su bandera `verify` de FOURIER.
   - **Umbral de percolación** f_c y su bandera `verify` de PERCOLA.
   - **Nodos clave** que actúan de puente en el grafo.
3. Confirma el `verify: True` final — es el **AND** de los certificados espectral y de percolación. Una sola prueba fallida hace fallar toda la auditoría.
4. Abre `courselib/trust.py` — `trust_audit_summary()`: llama a `score_pagerank`, `analyze_spectral` y `analyze_percolation`, y devuelve `top_trusted`, `fiedler_value`, `percolation_f_c`, `keystones` y ambas banderas de verificación.
5. Esboza cómo bloquearías una acción de un agente usando las tres señales a la vez (fuente de confianza **y** grafo conectado **y** sin fragilidad de nodos clave).
6. **Ejercicio:** `python labs/run_exercises.py --module m6`.

### Salida esperada

- Línea `== Trust math capstone ==`
- `Trust audit (7 nodes)` con el más confiable = `hub`, λ₂, f_c y los nodos clave
- `verify: True` final

### Autocomprobación

- [ ] Sabes nombrar los tres oráculos que compone la auditoría (LUMEN, FOURIER, PERCOLA)
- [ ] Entiendes por qué la auditoría solo se verifica cuando se verifica *cada* señal

---

## Ejercicios y certificado

Tras los labs, ejecuta las comprobaciones:

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Tu Nombre" --lang es
```

| Módulo | Qué comprueba el ejercicio |
|--------|----------------------------|
| M1 | Las puntuaciones PageRank suman 1 |
| M2 | Nodos clave detectados; la verificación PERCOLA pasa |
| M3 | El certificado de Fiedler se verifica |
| M4 | El consenso resiste el valor atípico |
| M5 | τ de cascada y el total de derrumbes se verifican |
| M6 | Auditoría combinada: `hub` el más confiable, pruebas espectral y de percolación pasan |

El certificado cubre los seis módulos. El HTML se abre en el navegador; **Print → Save as PDF** para una copia que compartir. El ID de credencial es `sha256(nombre|fecha)[:12]`, así que el mismo nombre en la misma fecha siempre reproduce el mismo ID. Para regenerar sin volver a correr las comprobaciones, añade `--skip-check`; para elegir dónde se guarda, pasa `-o path/to/certificate.html`.

---

## Observabilidad en cada lab

**Concepto:** cada lab registra sus decisiones en `Trace` (traza) — tu rastro de auditoría de eventos de confianza.

### Pasos (tras cada lab)

1. Desplázate a la sección **trace** al final de la salida.
2. Mapea los eventos al stdout: puntuaciones de confianza, umbrales de percolación, valores espectrales, estadísticas de consenso, métricas de cascada.
3. En M5, correlaciona los eventos `cascade` con los τ y CVaR impresos.

### Autocomprobación

- [ ] La traza es la «vista previa de SIEM» para las matemáticas de la confianza
- [ ] Sabes señalar la bandera de verificación de cada llamada a un oráculo

---

## Puente: del curso a los oráculos en producción

**Objetivo:** conectar los conceptos del curso con los despliegues vivos de oráculos de AIMarket (~30 min).

1. **Lee los README de los oráculos** en `oracles/oracles/{lumen,percola,fourier,murmuration,ablation}/`.

2. **Mapeo curso → capacidades del oráculo**

   | Curso | Oráculo | Capacidad |
   |-------|---------|-----------|
   | M1 | LUMEN | `lumen.pagerank@v1` |
   | M2 | PERCOLA | `percola.threshold@v1` + `percola.verify@v1` |
   | M3 | FOURIER | `fourier.spectrum@v1` + `fourier.verify@v1` |
   | M4 | MURMURATION | `murmuration.aggregate@v1` |
   | M5 | ABLATION | `ablation.cascade@v1` + `ablation.verify@v1` |
   | M6 | LUMEN + FOURIER + PERCOLA | auditoría compuesta (`trust_audit_summary`) |

3. **Invocar vía Hub** (opcional, desde el monorepo):

   ```bash
   cd aimarket-hub && pytest -q -k lumen
   ```

---

## Lista de autocomprobación

Track básico:

- [ ] labs 01–04 en local y en Colab
- [ ] Explicas la confianza PageRank en un grafo de quién-confía-en-quién
- [ ] Nombras los nodos clave en un grafo puente
- [ ] Interpretas el valor de Fiedler y la conductancia
- [ ] Eliges mediana vs media para estimaciones de agentes adversarias

Track avanzado:

- [ ] lab05 y explicas el riesgo de cola de la pila de arena
- [ ] lab06 y `trust_audit_summary()`; explicas por qué la auditoría solo se verifica cuando cada señal se verifica

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: courselib` | Ejecutar desde la raíz del repo; los labs anteponen el padre a `sys.path` |
| `ImportError: Oracle package 'lumen'` | Instala el slice de oráculos o ejecuta desde el monorepo aicom |
| Falta `numpy` | `pip install -e ".[oracles,dev]"` |
| Cadenas RU/ES vacías | `export COURSE_LANG=es`; las claves de `i18n/es.json` deben coincidir con `en.json` |
| Fallo de i18n en pytest | Añade las claves que faltan a los tres JSON |
| La verificación de PERCOLA falla | `samples` debe coincidir entre analyze y verify |
| Código viejo en Colab | Re-ejecuta la celda de setup; fija la rama `main` |

---

## Regenerar sitio y notebooks

Tras editar labs o i18n:

```bash
python3 scripts/build_course_assets.py
python3 scripts/labs_to_notebooks.py
```

Las guías en `docs/` se mantienen a mano — primero EN, luego los espejos RU/ES.
