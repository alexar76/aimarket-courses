# Guía paso a paso del curso

> **Audiencia:** ingenieros que quieren convertir la telemetría en vivo del ecosistema en visualizaciones 3D — sondear la API REST de alien-monitor, modelar su topología como un grafo tipado y mapear las escenas de los oráculos a React Three Fiber.
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · UI en `i18n/` · esta guía en español.
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

[alien-monitor](https://github.com/alexar76/alien-monitor) es el mapa 3D en vivo del ecosistema AIMarket: un Hub, sus pares de federación y una constelación de oráculos, cada uno renderizado como una escena animada de React Three Fiber. Este curso enseña la capa de datos detrás de ese mapa. Aprenderás a **sondear** la API REST del monitor (`/api/health`, `/api/topology`, `/api/reputation/*`), **modelar** las respuestas como estructuras tipadas de Python, **clasificar** los nodos con las puntuaciones PageRank/EigenTrust de LUMEN y, por último, **mapear** el slug de cada oráculo a los metadatos de cámara, color de acento y primitiva que usa el front-end de R3F para dibujar su escena.

Cada lab es **determinista y funciona sin red**: si no hay un alien-monitor en vivo en `127.0.0.1:9100`, cada lab arranca automáticamente un servidor simulado en proceso con la misma forma REST, así que todo el curso se ejecuta sin red y sin claves de API. Cada lab también imprime un bloque `Trace` para que el comportamiento sea inspeccionable y no parezca magia.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 min)](#instalación-10-min)
3. [M1 — Salud del monitor y modos](#m1--salud-del-monitor-y-modos)
4. [M2 — Modelo de grafo de topología](#m2--modelo-de-grafo-de-topología)
5. [M3 — Reputación de la federación](#m3--reputación-de-la-federación)
6. [M4 — Puntuaciones PageRank de LUMEN](#m4--puntuaciones-pagerank-de-lumen)
7. [M5 — Mapeo de escenas de oráculos a R3F (avanzado)](#m5--mapeo-de-escenas-de-oráculos-a-r3f-avanzado)
8. [Conectar un monitor en vivo](#conectar-un-monitor-en-vivo)
9. [Ejercicios y certificado](#ejercicios-y-certificado)
10. [Observabilidad: el bloque Trace](#observabilidad-el-bloque-trace)
11. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Monitor en vivo | Front-end |
|-------|---------|--------|-----------------|-----------|
| **Básico** | M1 → M2 → M3 → M4 | ~1,5 h | Simulado (auto) | Ninguno — Python puro |
| **Avanzado** | Básico + M5 | +30 min | Simulado o en vivo | Specs de R3F |
| **Puente en vivo** | Tras M4 o M5 | +30 min | alien-monitor real | Opcional |

El servidor simulado respalda todos los tracks, así que nunca necesitas un monitor en ejecución para terminar el curso. Tras **cada** lab revisa la [sección Trace](#observabilidad-el-bloque-trace).

---

## Instalación (10 min)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/3d-data-viz-course
pip install -e ".[dev]"
```

`[dev]` es el único extra que necesitas — los labs usan la biblioteca estándar de Python para el sondeo HTTP, así que no hay dependencias pesadas en tiempo de ejecución. `[dev]` añade `pytest` para la suite de tests.

### Paso 2 — Verificar tests

```bash
pytest -q
```

**Esperado:** todos los tests pasan (paridad i18n en `en/ru/es`, parseo del grafo, mapeo R3F, comprobaciones de ejercicios).

### Paso 3 — Primer lab

```bash
python labs/lab01_health_probe.py
python labs/run_exercises.py
```

### Paso 4 — Elige un idioma (opcional)

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_health_probe.py
```

Todos los títulos de módulo, conceptos, etiquetas y pistas de ejercicios vienen de `i18n/{en,ru,es}.json`.

### Paso 5 — Alternativa Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/3d-data-viz-course/) → **Abrir en Colab** en cualquier lab.
2. Ejecuta la celda de **setup** (clone + `pip install -e ".[dev]"`).
3. Define `os.environ["COURSE_LANG"] = "es"` en la celda de setup si lo necesitas.
4. Ejecuta la celda del lab — el servidor simulado funciona también dentro de Colab.

---

## M1 — Salud del monitor y modos

**Concepto:** sondea `/api/health` y entiende los modos TEST, REAL y UNIVERSE.
**Lab:** `labs/lab01_health_probe.py` · **~15 min** · observabilidad, SRE

### Pasos

1. Lee el docstring al inicio del lab.
2. `python labs/lab01_health_probe.py`
3. Lee la salida: si hay un monitor en vivo; la línea `result: status=ok mode=test`. El `mode` es la fuente de datos del monitor: `test` (simulado), `real` (ecosistema en vivo) o `universe` (vista federada multi-hub). Si se usó el simulado, verás la nota correspondiente.
4. Revisa `courselib/viz.py`: `probe_health`, `HealthStatus`, `monitor_reachable`, `resolve_monitor_url`.

### Qué demuestra

Un sondeo REST funcional y el patrón `resolve_monitor_url()` (en-vivo-o-simulado) que reutiliza **cada** lab posterior.

### Autocomprobación

- [ ] Explicas qué significan `status` y `mode`
- [ ] Entiendes por qué los labs recurren a un servidor simulado

---

## M2 — Modelo de grafo de topología

**Concepto:** analiza nodos y enlaces de `/api/topology` en estructuras de grafo tipadas.
**Lab:** `labs/lab02_topology_graph.py` · **~20 min** · requiere M1 · visualización de grafos, React Flow

### Pasos

1. `python labs/lab02_topology_graph.py`
2. Lee la salida: recuento de nodos y enlaces, luego hasta seis nodos con `id`, `group`, `position` 3D y `status`.
3. Fíjate en la línea `Adjacency list: N directed edges` — `TopologyGraph.adjacency()` deduplica aristas y descarta bucles propios, la forma que consume un renderizador force-directed.
4. Estudia `courselib/viz.py`: `MonitorNode`, `MonitorLink`, `TopologyGraph` y `Vec3.from_dict`. Los classmethods `from_api` convierten defensivamente el JSON crudo en dataclasses tipadas.

### Qué demuestra

Un grafo tipado en memoria (`nodes`, `links`, `adjacency()`, `node_ids()`, `oracle_slugs()`) — el modelo sobre el que se construyen M4 y M5.

### Autocomprobación

- [ ] Puedes nombrar los campos de un `MonitorNode`
- [ ] Entiendes por qué se deduplica la adyacencia y se quitan los bucles propios

---

## M3 — Reputación de la federación

**Concepto:** enriquece el grafo de confianza con `/api/reputation/peers` del Hub.
**Lab:** `labs/lab03_reputation_peers.py` · **~20 min** · requiere M2 · EigenTrust, federación

### Pasos

1. `python labs/lab03_reputation_peers.py`
2. Lee la salida: `Federation peers: N (mode)` seguido del `name`, `trust_score` y `url` de cada par. Un par sin puntuación imprime `—`.
3. En `courselib/viz.py` estudia `ReputationPeer` y `ReputationPeers`. El `trust_score` es `float | None`, así que tu visualización debe manejar datos ausentes.

### Qué demuestra

La capa de federación del grafo: en qué Hubs externos confía este monitor y cuánto — la entrada para codificar color/tamaño de los nodos de pares.

### Autocomprobación

- [ ] Distingues una puntuación `None` de una de `0.0`
- [ ] Ves cómo los pares extienden la topología de M2 con contexto de federación

---

## M4 — Puntuaciones PageRank de LUMEN

**Concepto:** llama a `/api/reputation/lumen` y vincula las puntuaciones a los nodos del grafo.
**Lab:** `labs/lab04_lumen_scores.py` · **~20 min** · requiere M2 · oráculos de reputación

### Pasos

1. `python labs/lab04_lumen_scores.py`
2. Lee la salida: nodos ordenados por puntuación, cada uno con una barra `█` y el valor a 4 decimales, luego `PageRank iterations: N`.
3. Si LUMEN no está disponible, el lab imprime una línea `LUMEN error` en vez de fallar — fíjate en la guarda `lumen.ok`.
4. En `courselib/viz.py` estudia `LumenScores` y `by_id()`, que combina `ids` con `scores` para unir los valores PageRank a los id de nodo de M2.

### Qué demuestra

Un mapa id-de-nodo → peso-de-reputación. LUMEN es el oráculo de iteración de potencia EigenTrust/PageRank; estos pesos controlan el tamaño de los nodos en el mapa 3D en vivo.

### Autocomprobación

- [ ] Puedes unir una puntuación LUMEN a un nodo de topología por id
- [ ] Sabes a grandes rasgos por qué las puntuaciones suman ~1,0 (una distribución de probabilidad)

---

## M5 — Mapeo de escenas de oráculos a R3F (avanzado)

**Concepto:** mapea los slugs de los oráculos a metadatos de cámara, acento y primitivas para escenas de Three.js.
**Lab:** `labs/lab05_r3f_scenes.py` · **~30 min** · requiere M2 · React Three Fiber, WebGL

### Pasos

1. `python labs/lab05_r3f_scenes.py`
2. Lee la salida: `Oracle R3F scenes: N`, luego por escena el `slug`, el tipo (`r3f` o `ambient`), la tupla `camera`, el color `accent` y una descripción truncada de la `primitive`.
3. En `courselib/viz.py` estudia `ORACLE_SCENE_META`, `R3FSceneSpec.for_oracle` y `map_graph_to_r3f_scenes`. La tabla de metadatos refleja `alien-monitor/frontend/src/oracleScenes/meta.ts`, así que la spec de Python y el front-end se mantienen sincronizados.
4. Fíjate en `TopologyGraph.oracle_slugs()` — quita el prefijo `oracle-` o coincide con `group == "oracle"`, y luego cada slug busca su cámara/acento/primitiva (con valores por defecto razonables para slugs desconocidos).

### Qué demuestra

Una lista de objetos `R3FSceneSpec` — exactamente la posición de cámara, el acento y la primitiva que un `<Canvas>` de React Three Fiber necesita para renderizar cada oráculo. Esto cierra el ciclo desde la telemetría REST hasta una escena 3D.

### Autocomprobación

- [ ] Puedes rastrear un slug de oráculo hasta su cámara + acento + primitiva
- [ ] Entiendes las escenas `ambient` frente a las escenas `r3f` normales
- [ ] Explicas por qué los metadatos se reflejan desde el `meta.ts` del front-end

---

## Conectar un monitor en vivo

Por defecto los labs corren contra el simulado integrado. Para sondear un alien-monitor real:

```bash
# apunta los labs a cualquier monitor en ejecución (por defecto http://127.0.0.1:9100)
export ALIEN_MONITOR_URL=http://127.0.0.1:9100
python labs/lab01_health_probe.py
```

Cuando el monitor es accesible, `resolve_monitor_url()` omite el simulado y aparece `Live alien-monitor reachable: True`. Los mismos cinco labs visualizan entonces el ecosistema **real** — los modos pasan de `test` a `real`/`universe`, la topología muestra nodos en vivo y LUMEN devuelve puntuaciones PageRank en vivo.

---

## Ejercicios y certificado

Tras los labs, ejecuta las comprobaciones:

```bash
python labs/run_exercises.py             # las cinco comprobaciones de módulo
python labs/run_exercises.py --module m4 # solo un módulo
```

La comprobación de cada módulo (`exercise_m1_health_ok` … `exercise_m5_r3f_mapping`) afirma la propiedad que enseñó el lab — p. ej. m1 afirma `status == "ok"` y un modo válido, m4 afirma `len(scores) == len(ids)`.

Cuando todas las comprobaciones pasan, genera el certificado:

```bash
python labs/run_exercises.py --certificate "Tu Nombre" --lang es   # o en / ru
```

Esto escribe `certificate.html` (el id de credencial deriva del nombre + la fecha). Ábrelo en un navegador y **Imprimir → Guardar como PDF** para una copia en PDF. Pasa todas las comprobaciones de módulo para desbloquear el certificado.

---

## Observabilidad: el bloque Trace

Tras cada lab (~5 min):

1. Ve a la línea `trace (N events)` al final de la salida.
2. Cada lab registra eventos estructurados: M1 registra `health`, M2 un `node` por nodo, M3 `peer`, M4 `lumen_score`, M5 `r3f_scene`.
3. Mapea cada evento a una línea que viste en stdout — la traza es el "log de test unitario" del lab: qué sondeó y qué produjo.

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: courselib` | Ejecuta desde la raíz del repo; los labs añaden el dir padre a `sys.path` |
| `Live alien-monitor reachable: False` | Esperado sin monitor en vivo — el simulado en proceso toma el relevo automáticamente |
| Quieres usar un monitor en vivo | Arranca alien-monitor en `127.0.0.1:9100` o define `ALIEN_MONITOR_URL` |
| Error de LUMEN / puntuaciones vacías | El monitor en vivo no devolvió datos de LUMEN; el lab se protege con `lumen.ok` y sigue |
| Cadenas RU/ES vacías | Define `COURSE_LANG`; comprueba que las claves de `i18n/ru.json` coinciden con `en.json` |
| Fallo de paridad i18n en pytest | Añade la clave que falta a los tres archivos `en/ru/es.json` |
| Colab con código antiguo | Re-ejecuta la celda de setup; fija la rama `main` |

---

Las guías en `docs/` se mantienen a mano — primero EN, luego los espejos RU/ES.
