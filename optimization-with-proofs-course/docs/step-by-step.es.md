# Guía paso a paso del curso

> **Audiencia:** desarrolladores que entregan resultados de optimización que un revisor pueda *verificar*, no solo confiar en ellos.
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · UI en `i18n/` · esta guía en español.
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## ¿Por qué pruebas?

La mayoría del código de optimización devuelve una respuesta — un recorrido, un plan de transporte, una ruta, una predicción — y te pide que confíes. Este curso invierte esa lógica: **cada lab entrega un certificado** que quien llama puede revisar de forma barata, sin re-ejecutar el solucionador y sin confiar en el oráculo que lo produjo.

- **TSP** devuelve un recorrido *y* una cota inferior admisible → puedes acotar la **brecha** respecto al óptimo.
- **Transporte óptimo** devuelve un plan *y* potenciales duales → testigo de dualidad fuerte en O(m×n).
- **Enrutamiento de tiempo mínimo** devuelve una ruta *y* potenciales eikonales → verificación arista por arista, sin re-resolver.
- **Procesos gaussianos** devuelven una posterior *y* una comprobación reproducible de media y varianza.

Los cuatro labs usan oráculos **AIMarket** en vivo — COLONY, KANTOR, FERMAT, GAUSS — y el proyecto final M5 encadena los cuatro certificados en una sola auditoría. Este es el patrón de los agentes verificables: una respuesta que un agente posterior puede rechazar localmente si el certificado falla.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 min)](#instalación-10-min)
3. [M1 — TSP con brecha de calidad](#m1--tsp-con-brecha-de-calidad)
4. [M2 — Transporte óptimo](#m2--transporte-óptimo)
5. [M3 — Enrutamiento de tiempo mínimo](#m3--enrutamiento-de-tiempo-mínimo)
6. [M4 — Procesos gaussianos](#m4--procesos-gaussianos)
7. [M5 — Proyecto final: cartera de pruebas](#m5--proyecto-final-cartera-de-pruebas)
8. [Ejercicios y certificado](#ejercicios-y-certificado)
9. [Observabilidad en cada lab](#observabilidad-en-cada-lab)
10. [Puente: del curso a los oráculos de producción](#puente-del-curso-a-los-oráculos-de-producción)
11. [Lista de autocomprobación](#lista-de-autocomprobación)
12. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Oráculos |
|-------|---------|--------|----------|
| **Básico** | M1 → M2 → M3 → M4 | ~2 h | COLONY, KANTOR, FERMAT, GAUSS |
| **Avanzado** | Básico + proyecto final M5 | +30 min | Los cuatro en una auditoría |

Cada lab imprime un `Trace` que puedes inspeccionar — trátalo como el registro de certificados del lab.

---

## Instalación (10 min)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/optimization-with-proofs-course
pip install -e ".[oracles,dev]"
```

El extra `[oracles]` instala `numpy`; `[dev]` instala `pytest`. Requiere Python 3.11+.

**Desde el monorepo aicom** (recomendado para colaboradores):

```bash
cd courses/optimization-with-proofs-course
pip install -e ".[oracles,dev]"
```

Los paquetes de oráculos se resuelven solos: `courselib/oracle_paths.py` sube hasta la raíz del monorepo y añade a `sys.path` los directorios `oracles/oracles/{colony,kantor,fermat,gauss}` y `oracles/core` (la dependencia de FERMAT).

**Clon independiente** sin el monorepo hermano:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
pip install -e _deps/oracles/core
for pkg in colony kantor fermat gauss; do
  pip install -e _deps/oracles/oracles/$pkg
done
pip install -e ".[oracles,dev]"
```

### Paso 2 — Verificar los tests

```bash
pytest -q
```

**Esperado:** paridad de claves i18n (en/ru/es), integración de oráculos de optimización, ejercicios y smoke imports de los labs pasan.

### Paso 3 — Elige idioma (opcional)

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_colony_tsp.py
```

`COURSE_LANG` cambia los títulos de módulo, los conceptos y las pistas de ejercicios vía `i18n/{en,ru,es}.json`. Los números, certificados y nombres de oráculos no cambian.

### Paso 4 — Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/optimization-with-proofs-course/) → **Open in Colab** en cualquier lab.
2. Ejecuta la **celda de setup** (clone + pip + sección de oráculos).
3. Si lo necesitas, define `os.environ["COURSE_LANG"] = "es"`.
4. Ejecuta la celda del lab.

---

## M1 — TSP con brecha de calidad

**Concepto:** recorrido «vecino más cercano» + 2-opt con cota inferior admisible.
**Lab:** `labs/lab01_colony_tsp.py` · **~20 min**

### Pasos

1. `python labs/lab01_colony_tsp.py`
2. Lee el docstring y luego observa el **recorrido**, la **longitud**, la **cota inferior**, la **brecha %** y la **base nn**.
3. La instancia es un pentágono con centro de `demo_tsp_points()`; `solve_tsp()` llama a `colony.tsp.solve(...)` y añade el flag `certificate_valid`.
4. Confirma `certificate_valid=True` — se cumple cuando `gap >= 0` **y** `length >= lower_bound` (certificado admisible).
5. **Ejercicio:** `python labs/run_exercises.py --module m1`

**Qué prueba:** la brecha `(length - lower_bound) / lower_bound` es un certificado de calidad: aun sin el recorrido óptimo, puedes afirmar «dentro de un X% del óptimo».

### Autocomprobación

- [ ] La brecha es no negativa e igual a `(length - lb) / lb`
- [ ] 2-opt nunca alarga el recorrido NN

---

## M2 — Transporte óptimo

**Concepto:** plan de Kantorovich exacto con certificado dual.
**Lab:** `labs/lab02_kantor_transport.py` · **~25 min**

### Pasos

1. `python labs/lab02_kantor_transport.py`
2. Compara el **coste de transporte**, la **distancia W₂**, el **objetivo dual** y el **método**.
3. `solve_transport()` llama a `kantor.transport(...)` y luego a `kantor.verify(...)`, pasando el coste declarado y los potenciales duales. KANTOR espera `source_points`/`sink_points`, no `points_a`/`points_b`.
4. Confirma `verify: True` — los potenciales atestiguan la optimalidad en O(m×n).
5. **Ejercicio:** `python labs/run_exercises.py --module m2`

**Qué prueba:** dualidad fuerte — el coste ≈ `Σ aᵢuᵢ + Σ bⱼvⱼ`, con `uᵢ + vⱼ ≤ Cᵢⱼ` en cada par. El verificador lo comprueba en una pasada.

### Autocomprobación

- [ ] Dualidad fuerte: cost ≈ Σ aᵢuᵢ + Σ bⱼvⱼ
- [ ] Factibilidad dual: uᵢ + vⱼ ≤ Cᵢⱼ en cada par

---

## M3 — Enrutamiento de tiempo mínimo

**Concepto:** potenciales eikonales y optimalidad dual en redes de agentes.
**Lab:** `labs/lab03_fermat_route.py` · **~20 min** · requiere M1 o M2

### Pasos

1. `python labs/lab03_fermat_route.py`
2. Observa la ruta `client → router → … → sink` y el **coste total**.
3. El grafo viene de `demo_routing_graph()`: las aristas combinan **coste**, **latencia** y **reputación** entre cinco nodos. `route_least_time()` llama a `fermat.eikonal.route(...)` y luego a `eikonal.verify(...)`.
4. Confirma `verify: True` — `T(v) ≤ T(u) + n(u,v)` en cada arista, con igualdad en las aristas de la ruta elegida.
5. **Ejercicio:** `python labs/run_exercises.py --module m3`

> FERMAT depende de `oracle_core`; `ensure_oracles` instala `oracle_core` antes que `fermat`.

**Qué prueba:** los potenciales `T` forman un certificado dual — el verificador confirma que la ruta es de tiempo mínimo sin re-ejecutar Dijkstra.

### Autocomprobación

- [ ] Los potenciales T son certificado dual sin re-ejecutar Dijkstra
- [ ] Aristas de la ruta con igualdad: T(v) = T(u) + n(u,v)

---

## M4 — Procesos gaussianos

**Concepto:** incertidumbre posterior y Expected Improvement.
**Lab:** `labs/lab04_gauss_gp.py` · **~25 min**

### Pasos

1. `python labs/lab04_gauss_gp.py`
2. Observa la **μ** y la **σ** posteriores en cada punto de consulta, y luego la sugerencia de Expected Improvement `x` y `EI`.
3. `gp_posterior()` llama a `gauss.gp.field(...)`, `gauss.gp.verify(...)` y `gauss.gp.suggest(...)` con `goal="min"`. EI sugiere el siguiente mejor experimento para minimizar.
4. Confirma `verify: True` — la media/varianza posterior se reproduce a partir de los datos de entrenamiento.
5. **Ejercicio:** `python labs/run_exercises.py --module m4`

**Qué prueba:** un certificado de reproducción — cualquiera puede recomputar la posterior desde los puntos de entrenamiento y rechazar una afirmación que no coincida. EI convierte la incertidumbre en la siguiente consulta.

### Autocomprobación

- [ ] La varianza posterior crece lejos de los puntos de entrenamiento
- [ ] EI equilibra explotación (media baja) y exploración (σ alta)

---

## M5 — Proyecto final: cartera de pruebas

**Concepto:** encadenar los certificados de TSP, transporte, ruta y GP en una sola auditoría.
**Lab:** `labs/lab05_proof_capstone.py` · **~30 min** · requiere M1–M4

### Pasos

1. `python labs/lab05_proof_capstone.py`
2. Observa cada flag de certificado impreso como `success`/`blocked`: `tsp_gap_ok`, `transport_verified`, `route_verified`, `gp_verified`.
3. Lee `proof_portfolio()` en `courselib/optimization.py` — ejecuta los cuatro oráculos y recoge los flags.
4. Confirma `all_verified=True` — cada certificado de oráculo pasa.
5. **Ejercicio:** `python labs/run_exercises.py --module m5`

**Qué prueba:** un único objeto de auditoría compuesto — un agente posterior rechaza el resultado completo si falla cualquier certificado; ningún oráculo se acepta a ciegas.

### Autocomprobación

- [ ] Puedes explicar qué prueba cada certificado
- [ ] Un verificador rechaza una mala respuesta sin confiar en el oráculo

---

## Ejercicios y certificado

Tras los labs, ejecuta las comprobaciones:

```bash
python labs/run_exercises.py                          # todos los ejercicios
python labs/run_exercises.py --module m1              # un módulo
python labs/run_exercises.py --certificate "Tu Nombre" --lang es
```

| Módulo | Comprobaciones del ejercicio |
|--------|------------------------------|
| M1 | Certificado de brecha TSP válido; `length >= lower_bound`; `gap >= 0` |
| M2 | La dual de Kantorovich verifica; cost > 0 |
| M3 | Los potenciales de ruta FERMAT verifican; ruta `client → sink` |
| M4 | La posterior GP verifica; `len(mean) == len(std)` |
| M5 | Cartera completa — los cuatro certificados pasan |

`run_exercises.py` ejecuta cada comprobación e imprime `✓`/`✗` por módulo. El flag `--certificate` genera `certificate.html` **solo tras aprobar todos los ejercicios** (usa `--skip-check` para omitirlo). Ábrelo en el navegador y **Print → Save as PDF**. El ID de credencial es un SHA-256 de nombre + fecha, y el certificado se localiza según `--lang en|ru|es`.

---

## Observabilidad en cada lab

**Concepto:** cada lab registra sus decisiones en `Trace` (`courselib/trace.py`) — tu rastro de auditoría para los certificados de optimización.

### Pasos (tras cada lab)

1. Busca la línea **trace** en la salida (imprime el número de eventos).
2. Mapea los eventos al stdout: brecha TSP, coste de transporte, total de ruta, verificación GP.
3. En M5, cada flag de oráculo se convierte en un evento `certificate` — correlaciona un flag fallido con su evento.

### Autocomprobación

- [ ] Trace registra el resultado de verificación de cada llamada al oráculo
- [ ] Puedes explicar qué fallaría si un oráculo mintiera sobre la optimalidad

---

## Puente: del curso a los oráculos de producción

**Objetivo:** conectar los conceptos del curso con despliegues de oráculos AIMarket en vivo (~30 min).

1. **Lee los README de los oráculos** en `oracles/oracles/{colony,kantor,fermat,gauss}/`.

2. **Mapeo curso → capacidades del oráculo**

   | Curso | Oráculo | Capacidad |
   |-------|---------|-----------|
   | M1 | COLONY | TSP + certificado de brecha |
   | M2 | KANTOR | `kantor.transport@v1` + `kantor.verify@v1` |
   | M3 | FERMAT | `fermat.route@v1` + `fermat.verify@v1` |
   | M4 | GAUSS | `gauss.field@v1` + `gauss.suggest@v1` + `gauss.verify@v1` |
   | M5 | Todos | Auditoría compuesta en `proof_portfolio()` |

3. **Compara los certificados** — cada oráculo devuelve una comprobación barata O(n) u O(E) que el verificador ejecuta localmente, independiente del solucionador.

---

## Lista de autocomprobación

Track básico:

- [ ] lab01–lab04 en local y en Colab
- [ ] Explicas la brecha TSP como certificado de calidad
- [ ] Enuncias las condiciones de factibilidad dual de Kantorovich
- [ ] Verificas una ruta FERMAT sin re-resolver
- [ ] Interpretas la incertidumbre posterior de GP y el EI

Track avanzado añade:

- [ ] lab05 y la lista de los cuatro tipos de certificado
- [ ] Un esbozo de flujo de agente que rechaza respuestas que fallan `verify`

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: courselib` | Ejecuta desde la raíz del repo; los labs añaden el padre a `sys.path` |
| `Oracle package '...' not installed` | Ejecuta desde el monorepo aicom o `pip install -e ".[oracles]"` |
| `ImportError: Oracle package 'fermat'` | Instala `oracle_core` primero y luego fermat (`ensure_oracles` lo hace) |
| `provide source_points+sink_points` | KANTOR espera `source_points`/`sink_points`, no `points_a` |
| `'goal' must be 'max' or 'min'` | El EI de GAUSS usa `goal="min"` o `"max"` |
| Falta `numpy` | `pip install -e ".[oracles,dev]"` |
| Cadenas RU/ES vacías | Define `COURSE_LANG`; revisa la paridad de claves i18n |
| Código viejo en Colab | Re-ejecuta la celda de setup; fija la rama `main` |

---

## Regenerar sitio y notebooks

Tras editar labs o i18n:

```bash
python3 scripts/build_course_assets.py
python3 scripts/labs_to_notebooks.py
```

Las guías en `docs/` son de mantenimiento manual — actualiza EN primero, luego los espejos RU/ES.
