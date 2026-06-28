# Guía paso a paso del curso

> **Audiencia:** desarrolladores que protegen agentes conectados por MCP antes o junto con ARGUS / AI-Factory.  
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · cadenas de UI en `i18n/` · esta guía en español.  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

MCP (Model Context Protocol) conecta un agente con servidores de herramientas externos — pero cada *descripción* de herramienta y cada *esquema* JSON es texto controlado por el atacante que el modelo lee como instrucción de confianza. Este curso te enseña a modelar amenazas de esa superficie, escanear estáticamente definiciones de herramientas envenenadas, clasificar servidores por confianza basada en grafos (LUMEN), aplicar allowlists fail-closed del propietario y encadenarlo todo en un gate WARDEN que bloquea un servidor typosquat malicioso. Cada primitiva es un port en Python ejecutable y sin LLM del firewall de producción ARGUS WARDEN, así que lo que aprendes se traslada directamente a código real.

---

## Índice

0. [Por qué este curso](#por-qué-este-curso)
1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 minutos)](#instalación-10-minutos)
3. [M1 — Modelo de amenazas MCP](#m1--modelo-de-amenazas-mcp)
4. [M2 — Escaneo estático y política](#m2--escaneo-estático-y-política)
5. [M3 — Puntuación de confianza LUMEN](#m3--puntuación-de-confianza-lumen)
6. [M4 — Owner-lock y fail-closed](#m4--owner-lock-y-fail-closed)
7. [M5 — Capstone: servidor malicioso](#m5--capstone-servidor-malicioso)
8. [Ejercicios y certificado](#ejercicios-y-certificado)
9. [Observabilidad en cada lab](#observabilidad-en-cada-lab)
10. [Puente: del curso a ARGUS WARDEN](#puente-del-curso-a-argus-warden)
11. [Lista de autocomprobación](#lista-de-autocomprobación)
12. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Oráculos |
|-------|---------|--------|----------|
| **Básico** | M1 → M2 → M3 → M4 | ~2 h | LUMEN (solo M3) |
| **Avanzado** | Básico + capstone M5 | +30 min | LUMEN + cadena WARDEN completa |
| **Puente Factory** | Tras M4 o M5 | +30 min | ARGUS + Hub reales |

Cada lab imprime un bloque `Trace` — trátalo como el registro de auditoría del lab.

---

## Instalación (10 minutos)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/mcp-security-course
pip install -e ".[oracles,dev]"
```

**Desde el monorepo aicom** (recomendado para contribuidores):

```bash
cd courses/mcp-security-course
pip install -e ".[oracles,dev]"
```

LUMEN se resuelve automáticamente desde `oracles/oracles/lumen` al ejecutar dentro del monorepo.

**Clon independiente** sin el monorepo vecino:

```bash
git clone --depth 1 https://github.com/alexar76/oracles.git _deps/oracles
pip install -e _deps/oracles/oracles/lumen
pip install -e ".[oracles,dev]"
```

### Paso 2 — Verificar tests

```bash
pytest -q
```

**Esperado:** paridad de i18n, escaneo estático WARDEN, PageRank LUMEN, ejercicios, smoke imports de labs.

### Paso 3 — Elegir idioma (opcional)

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_threat_model.py
```

### Paso 4 — Alternativa Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/mcp-security-course/) → **Open in Colab** en cualquier lab.
2. Ejecuta la **celda de setup** (clone + pip + porción de oracles).
3. Si lo necesitas, fija `os.environ["COURSE_LANG"] = "es"` en el setup.
4. Ejecuta la celda del lab.

---

## M1 — Modelo de amenazas MCP

**Concepto:** inyección de prompts, envenenamiento de herramientas y vías de exfiltración en MCP.  
**Lab:** `labs/lab01_threat_model.py` · **~15 min** · setup hecho

### Pasos

1. Abre `labs/lab01_threat_model.py` y lee el docstring del módulo.
2. Ejecuta localmente:

   ```bash
   python labs/lab01_threat_model.py
   ```

3. Observa dos escenarios:
   - **Prompt injection** — texto del atacante oculto en una *descripción* de herramienta.
   - **Tool poisoning** — campos del esquema que piden secretos o URLs de exfil.
4. Lee el bloque **trace** — cada superficie de ataque se registra como evento.
5. Revisa `courselib/warden.py` — encuentra `INJECTION_PATTERNS`, `EXFIL_PATTERNS`, `SECRET_PATTERNS` (5 min).

### Autocomprobación

- [ ] Explicas por qué las *descripciones* de herramientas son texto del atacante en el que el modelo confía
- [ ] Distingues entre inyección en el prompt del usuario y envenenamiento de la definición de herramienta

---

## M2 — Escaneo estático y política

**Concepto:** atrapar esquemas de herramientas maliciosos antes de que un agente los ejecute.  
**Lab:** `labs/lab02_static_scan.py` · **~20 min** · requiere M1

### Pasos

1. `python labs/lab02_static_scan.py`
2. Compara las secciones de escaneo **benigno** vs **malicioso**:
   - benigno → puntuación alta, cero o pocos hallazgos de baja severidad;
   - malicioso → puntuación baja, `TOOL_DEF_INJECTION`, `TOOL_DEF_EXFIL`, `TOOL_DEF_SECRET_REQUEST`.
3. Lee los mensajes de los hallazgos — fíjate en qué haystack coincidió (`description` vs esquema JSON).
4. Abre `argus/src/warden/static-scan.ts` en el monorepo — compara la paridad de regex con `courselib/warden.py`.
5. **Ejercicio:** `python labs/run_exercises.py --module m2`

### Autocomprobación

- [ ] El escaneo estático corre sobre la descripción *y* el texto del esquema JSON
- [ ] Un solo hallazgo crítico hunde la puntuación del gate, pero por sí solo no siempre fuerza el bloqueo

---

## M3 — Puntuación de confianza LUMEN

**Concepto:** reputación basada en grafos — PageRank de quién-confía-en-quién sobre servidores MCP.  
**Lab:** `labs/lab03_lumen_score.py` · **~20 min** · requiere `[oracles]` (numpy + lumen)

### Pasos

1. Confirma la instalación: `pip install -e ".[oracles,dev]"`.
2. `python labs/lab03_lumen_score.py`
3. Observa las aristas del grafo de confianza: `hub` → servidores oficiales; typosquat aislado.
4. Inspecciona las puntuaciones clasificadas — `hub` y los servidores oficiales deben superar a `offical-mcp-drainer`.
5. Lee `courselib/lumen.py` — `demo_mcp_trust_graph()` y `score_servers()`.
6. Opcional: abre `oracles/oracles/lumen/lumen/pagerank.py` para el núcleo EigenTrust.
7. **Ejercicio:** `python labs/run_exercises.py --module m3`

### Autocomprobación

- [ ] Las puntuaciones suman 1 (distribución de probabilidad)
- [ ] La confianza transitiva eleva nodos en los que confían nodos de confianza

---

## M4 — Owner-lock y fail-closed

**Concepto:** vincular agentes a allowlists de herramientas aprobadas por el propietario (análogo del owner-lock de Telegram).  
**Lab:** `labs/lab04_owner_lock.py` · **~15 min** · requiere M2

### Pasos

1. `python labs/lab04_owner_lock.py`
2. Verás pasar las herramientas permitidas (`read_file`, `search_docs`); `exec_shell`, `transfer_funds` se bloquean.
3. Fíjate en la demo de **allowlist vacío** — fail-closed, toda herramienta denegada.
4. Lee `OwnerLock` en `courselib/warden.py` — `check_tool()` y `OwnerLockGate`.
5. Lectura cruzada: [argus/docs/channels.md](https://github.com/alexar76/aicom/blob/main/argus/docs/channels.md) § owner-lock de Telegram.
6. **Ejercicio:** `python labs/run_exercises.py --module m4`

### Autocomprobación

- [ ] El allowlist es explícito — las herramientas desconocidas se deniegan, no se permiten en silencio
- [ ] Un allowlist vacío es fail-closed (cero confianza por defecto)

---

## M5 — Capstone: servidor malicioso

**Concepto:** la cadena completa de gates WARDEN bloquea un servidor MCP typosquat envenenado.  
**Lab:** `labs/lab05_warden_capstone.py` · **~30 min** · requiere M1–M4

### Pasos

1. `python labs/lab05_warden_capstone.py`
2. Compara los veredictos:
   - **Servidor oficial benigno** → `allowed`, puntuación compuesta alta;
   - **Typosquat envenenado** → `blocked`, `decided_by` nombra el gate que falló.
3. Orden de gates en el port pedagógico: static-scan → threat-feed → reputation (LUMEN) → owner-lock → pinning.
4. Inspecciona la lista de hallazgos — varios gates pueden contribuir antes del bloqueo.
5. Lee `Warden.vet()` en `courselib/warden.py` — la puntuación compuesta es el producto de las puntuaciones de los gates.
6. **Ejercicio:** `python labs/run_exercises.py --module m5`

### Autocomprobación

- [ ] El threat feed atrapa el id del servidor typosquat (`offical-mcp-drainer`)
- [ ] El static-scan atrapa injection + exfil en las definiciones de herramientas
- [ ] La baja reputación LUMEN contribuye cuando `allow_unknown_servers=False`

---

## Ejercicios y certificado

Tras los labs, ejecuta las comprobaciones DIY:

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "Tu Nombre" --lang es
```

Abre `certificate.html` — Print → Save as PDF desde el navegador. El ID de credencial se deriva del nombre + la fecha.

| Módulo | Comprobación del ejercicio |
|--------|----------------------------|
| M1 | Firma de injection detectada en la herramienta envenenada |
| M2 | Las herramientas benignas no producen hallazgos críticos |
| M3 | Hub supera al typosquat en el grafo de confianza |
| M4 | Owner-lock deniega herramientas fuera del allowlist |
| M5 | El WARDEN completo bloquea el servidor capstone malicioso |

---

## Observabilidad en cada lab

**Concepto:** cada lab registra decisiones en `Trace` — tu rastro de auditoría de eventos de seguridad.

### Pasos (repetir tras cada lab)

1. Desplázate a la sección **trace** en la salida del lab.
2. Mapea los eventos al stdout: hallazgos, puntuaciones de confianza, decisiones de owner-lock, veredictos WARDEN.
3. En M5, correlaciona los eventos `warden_finding` con la lista de hallazgos impresa.

### Autocomprobación

- [ ] El Trace es la «vista previa SIEM» del lab para la seguridad del agente
- [ ] Puedes señalar el gate que bloqueó una conexión

---

## Puente: del curso a ARGUS WARDEN

**Objetivo:** conectar los conceptos del curso con el ARGUS de producción (~30 min).

1. **Lee la documentación de WARDEN** — [argus/docs/security-warden.md](https://github.com/alexar76/aicom/blob/main/argus/docs/security-warden.md)

2. **Mapeo curso → ARGUS**

   | Curso | ARGUS |
   |-------|-------|
   | M2 static-scan | `src/warden/static-scan.ts` |
   | M3 LUMEN | `ReputationGate` + oráculo LUMEN |
   | M4 owner-lock | Owner-lock del canal + allowlist de egress |
   | M5 capstone | Cadena de gates `Warden.create()` |

3. **Ejecuta ARGUS** (opcional, desde el monorepo):

   ```bash
   cd argus && npm install && npm test -- warden
   ```

4. **Seguridad de supply en Hub** — [aimarket-hub/docs/supply-security.md](https://github.com/alexar76/aicom/blob/main/aimarket-hub/docs/supply-security.md)

---

## Lista de autocomprobación

Tras el track básico deberías poder:

- [ ] Ejecutar lab01–lab04 localmente y en Colab
- [ ] Nombrar tres familias de firmas de static-scan (injection, exfil, secrets)
- [ ] Explicar la confianza PageRank sobre un grafo de servidores MCP
- [ ] Describir allowlists fail-closed del propietario
- [ ] Leer un bloque `Trace` y encontrar la herramienta o el gate bloqueado

Tras el track avanzado añade:

- [ ] Ejecutar lab05 y explicar qué gate bloqueó el servidor typosquat
- [ ] Abrir `argus/src/warden/index.ts` y encontrar el orden de gates de producción

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: courselib` | Ejecuta desde la raíz del repo; los labs anteponen el padre a `sys.path` |
| `ImportError: Oracle package 'lumen'` | Instala la porción de oracles o ejecuta desde el monorepo aicom |
| Falta `numpy` | `pip install -e ".[oracles,dev]"` |
| Cadenas RU/ES vacías | Fija `COURSE_LANG`; las claves de `i18n/ru.json` deben coincidir con `en.json` |
| Fallo de pytest por i18n | Añade las claves que faltan a los tres archivos JSON |
| M5 bloquea el servidor benigno | Verifica que el allowlist de owner-lock incluya los nombres de herramientas benignas |
| Código viejo en Colab | Vuelve a ejecutar la celda de setup; fija la rama `main` |

**Problemas con ARGUS:** [argus/README.md](https://github.com/alexar76/aicom/blob/main/argus/README.md)

---

## Regenerar sitio y notebooks

Tras editar labs o i18n:

```bash
python3 scripts/build_course_assets.py
python3 scripts/labs_to_notebooks.py
```

Las guías en `docs/` se mantienen a mano — actualiza EN primero, luego los espejos RU/ES.
