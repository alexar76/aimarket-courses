# Guía paso a paso del curso

> **Audiencia:** desarrolladores que se integran con el pipeline de AI-Factory — endpoints públicos de estado, el catálogo de productos publicados y el flujo de etapas del orquestador.
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · cadenas de UI en `i18n/` · esta guía en español.
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

AI-Factory convierte una idea de una línea en un producto publicado recorriendo etapas orquestadas: **research → design → build → test → ship**. Cada etapa tiene un agente responsable (analyst, architect, developer, QA, devops), y la fábrica expone una pequeña **API pública** para que cualquiera pueda observar el pipeline en marcha y ver qué ha publicado.

El curso estudia esa API desde fuera hacia dentro. Sondeas los mismos dos endpoints públicos que usa la página de inicio, recorres la máquina de estados del orquestador de `IDEA_RECEIVED` a `COMPLETED` y terminas con un capstone de sondeo — **sin necesidad de una fábrica en marcha**. Cada lab recurre a un **mock embebido de la fábrica** en `127.0.0.1`, así que todo el curso funciona sin conexión. Apunta una variable de entorno a una fábrica en vivo y los mismos labs leen datos reales.

Cada lab imprime un bloque `Trace`: la orquestación se registra, no es magia.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (5 min)](#instalación-5-min)
3. [M1 — Visión general del pipeline](#m1--visión-general-del-pipeline)
4. [M2 — API de estado del pipeline](#m2--api-de-estado-del-pipeline)
5. [M3 — Catálogo de productos publicados](#m3--catálogo-de-productos-publicados)
6. [M4 — Flujo de etapas del orquestador](#m4--flujo-de-etapas-del-orquestador)
7. [M5 — Capstone: sondeo de la fábrica](#m5--capstone-sondeo-de-la-fábrica)
8. [Fábrica en vivo vs mock embebido](#fábrica-en-vivo-vs-mock-embebido)
9. [Observabilidad — el Trace en cada lab](#observabilidad--el-trace-en-cada-lab)
10. [Ejercicios y certificado](#ejercicios-y-certificado)
11. [Puente: del curso a AI-Factory](#puente-del-curso-a-ai-factory)
12. [Lista de autocomprobación](#lista-de-autocomprobación)
13. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Fábrica en vivo |
|-------|---------|--------|------------------|
| **Básico** | M1 → M2 → M3 → M4 | ~1,5 h | No — mock embebido |
| **Avanzado** | Básico + capstone M5 | +30 min | Opcional (`COURSE_FACTORY_URL`) |
| **Puente Factory** | Tras M5 | +30 min | Sí — fábrica real + Hub |

Nunca *necesitas* una fábrica en vivo: M2, M3 y M5 arrancan un mock automáticamente cuando ninguna está disponible. El campo `source` en la salida indica quién respondió (`mock` o `live`).

---

## Instalación (5 min)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/ai-factory-course
pip install -e ".[factory,dev]"
```

El extra `[factory]` trae `fastapi` + `uvicorn` — son el motor del mock embebido al que recurren M2/M3/M5. `[dev]` añade `pytest`. Se requiere Python 3.11+.

### Paso 2 — Verificar tests

```bash
pytest -q
```

**Esperado:** todos los tests pasan — paridad i18n en `en/ru/es`, el cliente de fábrica y el recorrido del orquestador, las comprobaciones de ejercicios y un smoke de los cinco labs.

### Paso 3 — Ejecutar el primer lab

```bash
python labs/lab01_pipeline_overview.py
```

Verás las cinco fases del pipeline mapeadas a agentes, luego un bloque `trace` y después una pista de ejercicio "Tu turno".

### Paso 4 — Elegir idioma (opcional)

```bash
export COURSE_LANG=es   # o ru; por defecto en
python labs/lab01_pipeline_overview.py
```

Títulos, etiquetas y pistas cambian de idioma; el código, los nombres de estado (`COMPLETED`) y las rutas de endpoint quedan en inglés. Orden de resolución: argumento explícito → `COURSE_LANG` → fallback a inglés.

### Paso 5 — Alternativa en Colab

Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/ai-factory-course/) → **Open in Colab** en cualquier lab → ejecuta la celda de setup (clone + `pip install -e ".[factory,dev]"`) → opcionalmente fija `os.environ["COURSE_LANG"] = "es"`, luego ejecuta la celda del lab.

---

## M1 — Visión general del pipeline

**Concepto:** research → design → build → test → ship como etapas orquestadas, cada una con su agente responsable.
**Lab:** `labs/lab01_pipeline_overview.py` · **~15 min** · instalación hecha

### Pasos

1. Abre `labs/lab01_pipeline_overview.py` y lee el docstring.
2. Ejecuta: `python labs/lab01_pipeline_overview.py`
3. Lee la tabla de **cinco fases**: cada línea es `fase → agente → estado`, p. ej. `research → analyst → MARKET_RESEARCHED`, hasta `ship → devops → COMPLETED`.
4. Abre `courselib/factory.py` y busca `PIPELINE_PHASES` — la tupla exacta que imprime el lab (es el mapa pedagógico; el grafo real del orquestador llega en M4).

### Qué demuestra

La fábrica no es una caja negra: existe un mapeo fijo e inspeccionable de cada fase de negocio al agente que la posee y al estado que deja. Cada línea `fase` también se registra como evento de trace.

### Autocomprobación

- [ ] Nombras las cinco fases en orden
- [ ] Sabes qué agente posee cada fase

---

## M2 — API de estado del pipeline

**Concepto:** el heartbeat de la página de inicio — `GET /api/public/pipeline-status` devuelve los contadores *en el pipeline* vs *publicado*.
**Lab:** `labs/lab02_pipeline_status.py` · **~15 min** · requiere M1

### Pasos

1. Ejecuta: `python labs/lab02_pipeline_status.py`
2. Lee tres líneas: **En el pipeline**, **Publicado** y **Fuente de datos**.
3. Mira el valor de `Fuente de datos` — `mock` (mock arrancado por ti) o `live` (si `COURSE_FACTORY_URL` apunta a una fábrica accesible).
4. Abre `courselib/factory.py` → `FactoryClient.get_pipeline_status()` para ver el único `GET` HTTP detrás.

### Qué demuestra

Un endpoint público de heartbeat basta para responder "¿está ocupada la fábrica y cuánto ha publicado?" — los mismos números que muestra la landing. El mock devuelve un determinista 4 en pipeline / 2 publicado para que el lab sea reproducible sin conexión.

### Autocomprobación

- [ ] Lees "en el pipeline" vs "publicado" en la salida
- [ ] Sabes si tu ejecución usó `mock` o `live`

---

## M3 — Catálogo de productos publicados

**Concepto:** `GET /ai-market/products` lista los productos `COMPLETED` y sus capacidades.
**Lab:** `labs/lab03_products_catalog.py` · **~15 min** · requiere M2

### Pasos

1. Ejecuta: `python labs/lab03_products_catalog.py`
2. Lee el conteo de **Productos publicados** y los primeros productos: `id: name (N caps)`.
3. Cada producto lleva `capabilities` — id más `price_per_call_usd`. Revisa `MOCK_PRODUCTS` en `courselib/factory.py` (`demo-analytics`, `demo-orchestrator`).
4. El trace registra un evento `products` más un evento `product` por cada elemento listado.

### Qué demuestra

Lo que la fábrica publica se vuelve un catálogo de marketplace: cada producto expone capacidades invocables y con precio. Es el puente entre "el pipeline terminó algo" y "puedes llamarlo" (ver la sección "Puente").

### Autocomprobación

- [ ] `count` coincide con el número de productos listados
- [ ] Puedes señalar un id de capacidad y su precio por llamada

---

## M4 — Flujo de etapas del orquestador

**Concepto:** el orquestador es una máquina de estados; recórrela de `IDEA_RECEIVED` a `COMPLETED`.
**Lab:** `labs/lab04_orchestrator_stages.py` · **~20 min** · requiere M1

### Pasos

1. Ejecuta: `python labs/lab04_orchestrator_stages.py`
2. Lee la **Ruta del orquestador** — cada línea es `STATE  agent=<quién>`, de `IDEA_RECEIVED` a `COMPLETED`.
3. Las transiciones vienen de `config/pipeline_flow.json` **en el monorepo** cuando existe; en modo standalone el lab usa el `agent_flow` de respaldo en `courselib/factory.py`.
4. Abre `walk_to_ship()` y `next_state()` en `courselib/factory.py` — fíjate en el límite `max_steps`, que detiene el recorrido en `COMPLETED`/`DEPLOYED_PRODUCTION` y evita bucles infinitos.

### Qué demuestra

El mapa de fases de M1 está respaldado por una tabla de transiciones real. Cada arista `STATE → (agent, next_state)` se registra como evento `transition`, así que toda la ruta es auditable.

### Autocomprobación

- [ ] La ruta empieza en `IDEA_RECEIVED` y llega a `COMPLETED`
- [ ] Explicas por qué termina el recorrido (el límite de bucle)

---

## M5 — Capstone: sondeo de la fábrica

**Concepto:** un sondeo de extremo a extremo — heartbeat + catálogo + fases — contra una fábrica en vivo o el mock embebido.
**Lab:** `labs/lab05_factory_capstone.py` · **~20 min** · requiere M2–M4 · track: avanzado

### Pasos

1. Ejecuta: `python labs/lab05_factory_capstone.py`
2. Lee el resultado combinado: `in_pipeline=… shipped=…`, el `count` del catálogo y su `source`, luego las cinco `phases`.
3. Abre `probe_factory()` en `courselib/factory.py` — reutiliza un único `factory_client()` para ambos endpoints y adjunta la lista de fases. Son los labs del track básico compuestos en una sola llamada.
4. Re-ejecuta con `COURSE_FACTORY_URL` para ver cómo `source` pasa de `mock` a `live`.

### Qué demuestra

Puedes verificar la salud e inventariar una fábrica en un solo viaje de ida y vuelta, y la forma de la respuesta es idéntica venga de un despliegue real o del mock local — el contrato de integración es estable.

### Autocomprobación

- [ ] Nombras la cadena: status → products → phases en un sondeo
- [ ] Explicas la distinción `source ∈ {live, mock}`

---

## Fábrica en vivo vs mock embebido

Cada lab en red (M2, M3, M5) usa `factory_client()`, que:

1. Lee una URL base de `COURSE_FACTORY_URL` (o `AIFACTORY_URL` / `FACTORY_PUBLIC_URL`).
2. Si está definida **y accesible**, habla con esa fábrica en vivo; la salida muestra `source: live`.
3. Si no, arranca un **mock embebido en FastAPI** en un puerto libre de `127.0.0.1`, espera a `/api/health` y sirve datos deterministas; la salida muestra `source: mock`.

Apuntar a una fábrica en vivo:

```bash
export COURSE_FACTORY_URL=https://your-factory.example
python labs/lab02_pipeline_status.py    # ahora lee contadores reales
```

Las comprobaciones de ejercicios (`prefer_live=False`) siempre usan el mock para pasar sin conexión y en CI.

---

## Observabilidad — el Trace en cada lab

**Concepto:** cada lab registra lo que hizo para que el comportamiento sea inspeccionable, no magia.
**Dónde:** en los cinco labs vía el helper `Trace` · **~5 min** tras cada lab

### Pasos (tras M1–M5)

1. Baja al bloque `trace (N events):` al final de la salida.
2. Mapea cada evento a una línea que viste encima — una entrada `phase`/`transition`/`product`/`pipeline_status`/`capstone` por acción.
3. Compara entre labs: M1 registra cinco eventos `phase`; M4 uno `transition` por salto de estado; M5 un único evento `capstone` consolidado.

### Autocomprobación

- [ ] El trace es el "log de test unitario" del lab: qué hizo el sondeo
- [ ] Correlacionas una línea impresa con un evento de trace

---

## Ejercicios y certificado

Cada lab termina con una pista "Tu turno". Ejecuta la comprobación correspondiente:

```bash
python labs/run_exercises.py --module m1     # un módulo
python labs/run_exercises.py                 # todos → ✓/✗ por módulo
```

Las comprobaciones por módulo viven en `courselib/exercises.py` (p. ej., M1 verifica las cinco fases en orden; M4 que el recorrido empieza en `IDEA_RECEIVED` y llega a `COMPLETED`).

Cuando las cinco pasen, genera un certificado:

```bash
python labs/run_exercises.py --certificate "Tu Nombre" --lang es
```

Esto escribe `certificate.html`; ábrelo y **Print → Save as PDF**. El ID de credencial es un SHA-256 de nombre + fecha de emisión (estable para el mismo nombre en el mismo día). Banderas: `--lang ru`/`es` para un certificado localizado, `-o path.html` para elegir el archivo, `--skip-check` solo si debes generar sin re-ejecutar las comprobaciones.

---

## Puente: del curso a AI-Factory

**Objetivo:** ejecutar los mismos sondeos contra el pipeline *real* (~30 min).

1. **Arranca la fábrica** (desde la raíz del monorepo):

   ```bash
   docker compose up -d app
   # → http://localhost:9080
   ```

2. **Apunta los labs hacia ella:**

   ```bash
   export COURSE_FACTORY_URL=http://localhost:9080
   python labs/lab05_factory_capstone.py    # source: live
   ```

3. **Envía una idea** — sigue [USER_GUIDE.es.md](https://github.com/alexar76/aicom/blob/main/docs/USER_GUIDE.es.md), sección "Tus primeros 15 minutos": `/admin/login` → **New product** → **Pipeline** y observa cómo la tira de etapas avanza por los estados reales que recorriste en M4.

4. **Mapeo curso → fábrica:**

   | Curso | Factory |
   |-------|---------|
   | M1 fases | Tira de etapas del pipeline (agentes reales) |
   | M2 estado | `/api/public/pipeline-status` de la home |
   | M3 catálogo | Productos publicados en `/ai-market/products` |
   | M4 flujo de etapas | `config/pipeline_flow.json` del orquestador |
   | M5 capstone | Un sondeo contra el despliegue en vivo |

5. **Invoca una capacidad publicada** — cuando un producto está `COMPLETED`, sus capacidades se llaman vía el Hub: [hub-integration-guide.md](https://github.com/alexar76/aicom/blob/main/docs/hub-integration-guide.md).

---

## Lista de autocomprobación

Tras el track básico deberías poder:

- [ ] Ejecutar lab01–lab04 en local (y en Colab)
- [ ] Nombrar las cinco fases y el agente que posee cada una
- [ ] Leer "en el pipeline" vs "publicado" de `pipeline-status`
- [ ] Explicar `source ∈ {live, mock}` y cómo decide `COURSE_FACTORY_URL`
- [ ] Recorrer el orquestador de `IDEA_RECEIVED` a `COMPLETED` y explicar el límite de bucle

Tras el track avanzado añade:

- [ ] Ejecutar lab05 y describir status → products → phases en un sondeo
- [ ] Apuntar un lab a una fábrica en vivo y ver `source: live`
- [ ] Generar un certificado con `--certificate "<nombre>" --lang <en|ru|es>`

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: courselib` | Ejecuta desde la raíz del repo; los labs anteponen el directorio padre a `sys.path` |
| El mock "did not become ready" | Conflicto de puerto o falta el extra `[factory]` — reinstala `pip install -e ".[factory,dev]"` |
| `source` siempre `mock` cuando esperas `live` | `COURSE_FACTORY_URL` sin definir o inaccesible; el cliente recurre al mock en silencio |
| Error de import de `fastapi`/`uvicorn` | Instalaste sin `[factory]`; ese extra aporta el servidor mock |
| Cadenas RU/ES vacías | Define `COURSE_LANG`; las claves ausentes recurren al inglés (nunca rompen) |
| Fallo de paridad i18n en pytest | Una clave existe en un catálogo pero no en los tres — añádela a `en.json`, `ru.json`, `es.json` |
| Colab con código viejo | Re-ejecuta la celda de setup para volver a clonar `main` |

**Problemas de la fábrica:** [FAQ.es.md](https://github.com/alexar76/aicom/blob/main/docs/FAQ.es.md)

---

## Regenerar sitio y notebooks

Tras editar labs o `i18n/`:

```bash
python3 scripts/build_course_assets.py
```

Las guías en `docs/` se mantienen a mano — primero EN, luego los espejos RU/ES.
