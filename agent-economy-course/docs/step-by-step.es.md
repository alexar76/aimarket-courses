# Guía paso a paso del curso

> **Audiencia:** desarrolladores que construyen sobre AIMarket Protocol v2 — descubrimiento federado, escrow, canales de pago, recibos firmados y capabilities de agente de pago.
> **Idioma de labs:** `COURSE_LANG=en|ru|es` · cadenas de UI en `i18n/` · esta guía en español.
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md)

---

## Por qué este curso

La mayoría de los tutoriales de «agentes» se quedan en llamar a un modelo. Este curso trata la capa de encima: cómo un agente **encuentra** una capability que no posee, **paga** por ella sin una transacción en blockchain por cada llamada, **confía** en el resultado mediante un recibo firmado, y cómo un proveedor **publica** una API medida que otros agentes pueden comprar. Esa es la economía de AIMarket Protocol v2 — descubrimiento, escrow, canales, reputación, monetización — y construyes una porción funcional de extremo a extremo.

Cada lab corre contra un **hub-lite embebido** (un hub FastAPI en el mismo proceso), así que el flujo económico es HTTP real, no un mock — pero **sin dinero real** y sin clones de git hasta el capstone. Cada lab imprime un registro de eventos `Trace` para que la historia descubrir → pagar → invocar → recibo sea inspeccionable, no magia.

---

## Índice

1. [Elige tu track](#elige-tu-track)
2. [Instalación (10 min)](#instalación-10-min)
3. [M1 — Resumen de Protocol v2](#m1--resumen-de-protocol-v2)
4. [M2 — SDK e integración con Hub](#m2--sdk-e-integración-con-hub)
5. [M3 — Escrow y canales de pago](#m3--escrow-y-canales-de-pago)
6. [M4 — Reputación y confianza](#m4--reputación-y-confianza)
7. [M5 — Publicar una capability](#m5--publicar-una-capability)
8. [M6 — Capstone: ciclo de agente de pago (avanzado)](#m6--capstone-ciclo-de-agente-de-pago-avanzado)
9. [Ejercicios y certificado](#ejercicios-y-certificado)
10. [Observabilidad en cada lab](#observabilidad-en-cada-lab)
11. [Puente: del curso al hub de producción](#puente-del-curso-al-hub-de-producción)
12. [Lista de autocomprobación](#lista-de-autocomprobación)
13. [Problemas frecuentes](#problemas-frecuentes)

---

## Elige tu track

| Track | Módulos | Tiempo | Dependencias | Hub |
|-------|---------|--------|--------------|-----|
| **Hub-lite** | M1 → M5 | ~2 h | `[hub-lite,dev]` | Hub-lite embebido (en proceso) |
| **Avanzado** | Hub-lite + M6 | +1 h | `[sandbox,dev]` | AIMarket Hub completo + SDK `aimarket-agent` |
| **Producción** | Tras M5 o M6 | +30 min | Tus keys | Hub de federación real |

Las labs M1–M5 solo necesitan `[hub-lite]` (~5 MB, wheels de pip puras). El capstone M6 añade el extra `[sandbox]` (~50 MB, clona por git el SDK `aimarket-agent` y `aimarket-hub`). Tras cada lab revisa el bloque `Trace`.

---

## Instalación (10 min)

### Paso 1 — Clonar e instalar

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/agent-economy-course
pip install -e ".[hub-lite,dev]"
```

Para el capstone (M6) añade el extra sandbox:

```bash
pip install -e ".[sandbox,dev]"
```

Requiere **Python 3.11+**. Al desarrollar dentro del monorepo `aicom`, el sandbox autodescubre los paquetes hermanos `aimarket-agent/` y `aimarket-hub/` — no hace falta clonar por git en local.

### Paso 2 — Verificar tests

```bash
pytest -q
```

En el monorepo, ejecuta desde el directorio del curso con `PYTHONPATH` definido:

```bash
cd courses/agent-economy-course
PYTHONPATH=. python3 -m pytest -q
```

**Esperado:** pasan los tests de protocol, hub-lite, trust, ejercicios y paridad de i18n. Los tests de economy/capstone solo corren si el SDK `aimarket-agent` es importable; si no, se omiten limpiamente.

### Paso 3 — Elige idioma (opcional)

```bash
export COURSE_LANG=es   # o ru, por defecto en
python labs/lab01_protocol_overview.py
```

`COURSE_LANG` cambia las cadenas impresas de cada lab (títulos, etiquetas de campos, pistas) según los catálogos `i18n/{en,ru,es}.json`. El código, los IDs de capability y los comandos no cambian.

### Paso 4 — Alternativa Colab

1. Abre el [sitio del curso](https://alexar76.github.io/aimarket-courses/agent-economy-course/) → **Open in Colab** en cualquier lab.
2. Ejecuta la **celda de setup** (clone + pip).
3. Si lo necesitas, pon `os.environ["COURSE_LANG"] = "es"` en la celda de setup.
4. Ejecuta la celda del lab.

---

## M1 — Resumen de Protocol v2

**Concepto:** capacidades, recibos y descubrimiento federado empiezan en `/.well-known/ai-market.json`.
**Lab:** `labs/lab01_protocol_overview.py` · **~15 min**

### Pasos

1. Lee el docstring al inicio del archivo del lab.
2. `python labs/lab01_protocol_overview.py`
3. Qué hace el lab:
   - Arranca el hub-lite embebido en proceso (~2 s).
   - Pide `/.well-known/ai-market.json` y lo valida con `validate_well_known`.
   - Pide el manifest y lo valida con `validate_manifest`.
   - Imprime el nombre de una herramienta de ejemplo y su `price_per_call_usd`.
4. Revisa `courselib/protocol.py` — validación estructural alineada con las formas de `aimarket-protocol/schemas/`.

### Autocomprobación

- [ ] Sabes nombrar el punto de entrada de descubrimiento (`/.well-known/ai-market.json`)
- [ ] Entiendes qué comprueba `validate_well_known` frente a `validate_manifest`

**Ejercicio (M1):** añade una comprobación de campo en `validate_well_known` — `python labs/run_exercises.py --module m1`

---

## M2 — SDK e integración con Hub

**Concepto:** registrar, descubrir e invocar una capability de pago en un hub real; recibir un recibo firmado.
**Lab:** `labs/lab02_hub_discover.py` · **~20 min** · requiere M1

### Pasos

1. `python labs/lab02_hub_discover.py`
2. Sigue el flujo:

   ```
   discover("translate") → invoke(prod-translate, translate.multi@v2) → receipt
   ```

3. Lee los campos: `success`, `price`, `served by` y el `nonce` del recibo. Esto refleja una llamada de federación de producción sin clonar `aimarket-hub`.
4. Confirma que los eventos `discover` e `invoke` aparecen en el bloque trace.

### Autocomprobación

- [ ] El descubrimiento devuelve metadatos de capability (`product_id`/`capability_id`, precio)
- [ ] La invocación devuelve un resultado estructurado más un recibo con nonce

**Ejercicio (M2):** descubre `summarize` e invócalo — `python labs/run_exercises.py --module m2`

---

## M3 — Escrow y canales de pago

**Concepto:** retener fondos hasta la entrega; transmitir micropagos sin una transacción on-chain por cada llamada.
**Lab:** `labs/lab03_escrow_channel.py` · **~20 min** · requiere M2

### Pasos

1. `python labs/lab03_escrow_channel.py`
2. Sigue el ciclo de vida:
   - **Abre** un canal prefinanciado con `budget_usd=0.25`.
   - **Invoca** `summarize@v1` a través de él.
   - **Cierra** el canal e inspecciona `spent` frente a `refund`.
3. Dos ideas:
   - **Canal de pago** — agrupa micropagos sin txs on-chain por llamada.
   - **Escrow** — fondos retenidos hasta la entrega; el presupuesto no usado se reembolsa al cerrar.

Hub-lite expone `/ai-market/v2/channel/open` y `/close` para enseñar el patrón. El ciclo completo del SDK en M6 usa el stack de escrow real del hub.

### Autocomprobación

- [ ] Sabes nombrar el ciclo: abrir → invocar → cerrar → reembolso
- [ ] Un canal amortiza muchas llamadas contra un presupuesto único frente a un 402 por llamada

**Ejercicio (M3):** abre un canal de `$1.00` y ciérralo — `python labs/run_exercises.py --module m3`

---

## M4 — Reputación y confianza

**Concepto:** los recibos firmados hacen verificables las llamadas de pago y alimentan un grafo de reputación estilo LUMEN.
**Lab:** `labs/lab04_reputation_trust.py` · **~25 min** · requiere M2

### Pasos

1. `python labs/lab04_reputation_trust.py`
2. Observa dos verificaciones:
   - Un recibo genuino verifica `True` y **sube** la puntuación de confianza del producto.
   - Una copia tras `tamper_receipt(..., price_usd=0.0)` verifica `False` y la **baja**.
3. Lee los bloques de construcción:
   - `courselib.trust.sign_receipt` / `verify_receipt` — recibos didácticos HMAC-SHA256 (stdlib, la misma idea que en producción).
   - `TrustGraph` — ajustes de puntuación estilo LUMEN en memoria.
   - Hub `/ai-market/v2/trust/record` — demo del hook de confianza federada.

### Autocomprobación

- [ ] Explicas por qué un precio alterado falla la verificación
- [ ] Ves cómo las llamadas verificadas frente a las alteradas mueven la puntuación de confianza en sentidos opuestos

**Ejercicio (M4):** firma tu propio recibo con un secreto personalizado y verifícalo — `python labs/run_exercises.py --module m4`

---

## M5 — Publicar una capability

**Concepto:** lanzar una API medida que otros agentes pueden comprar — el lado **proveedor** de la economía.
**Lab:** `labs/lab05_publish_capability.py` · **~20 min** · requiere M2

### Pasos

1. `python labs/lab05_publish_capability.py`
2. Flujo del proveedor:
   - `register_capability("prod-course", "sentiment.metered@v1", 0.007, ...)`.
   - Vuelve a pedir el manifest y observa crecer el número de herramientas (`before → after`).
   - `discover("sentiment")` encuentra la nueva capability.
   - `invoke` como consumidor y lee el precio + el nonce del recibo.
3. Confirma los eventos `register`, `manifest`, `discover` e `invoke` en el trace.

### Autocomprobación

- [ ] Registras una capability con precio y descripción
- [ ] Demuestras que tras el registro es descubrible e invocable

**Ejercicio (M5):** registra una capability personalizada e invócala — `python labs/run_exercises.py --module m5`

---

## M6 — Capstone: ciclo de agente de pago (avanzado)

**Concepto:** un ciclo `hire()` autónomo completo vía el SDK real `aimarket-agent`.
**Lab:** `labs/lab06_paid_capability_capstone.py` · **~45 min** · requiere `[sandbox]` (~50 MB, instalar una vez)

### Pasos

1. Instala el extra sandbox una vez (en Colab reutiliza la sesión si labs anteriores ya lo instalaron):

   ```bash
   pip install -e ".[sandbox,dev]"
   ```

2. `python labs/lab06_paid_capability_capstone.py`
3. Sigue el ciclo completo:

   ```
   discover → open channel → invoke → signed receipt → settle → bill of materials
   ```

   El lab arranca un AIMarket Hub local + un Factory stub en hilos de fondo, luego llama a `econ.hire("translate text to multiple languages")` con un presupuesto de `$3.00`. **Sin dinero real.**
4. Lee el bill of materials: tarea, éxito, ID del canal, total gastado, versión del protocolo, capabilities por paso y listados ACEX en vivo.

> Si el SDK `aimarket-agent` **no** está instalado, el lab lo detecta vía `sdk_available()` y se omite limpiamente con una pista — no se cae. Las labs 1–5 y todos los ejercicios funcionan sin él.

### Autocomprobación

- [ ] Sabes nombrar el ciclo completo: discover → channel → invoke → receipt → settle
- [ ] Entiendes que el capstone es el único lab que necesita `[sandbox]`

**Ejercicio (M6):** ejecuta el ciclo `hire()` completo en el sandbox, o la comprobación de invoke de pago vía hub-lite — `python labs/run_exercises.py --module m6`

---

## Ejercicios y certificado

Cada módulo mapea 1:1 a una comprobación DIY autocontenida (`m1`…`m6`). Ejecuta una:

```bash
python labs/run_exercises.py --module m3
```

Ejecuta todas:

```bash
python labs/run_exercises.py
```

Imprime `✓` o `✗` por módulo. Cuando pasan **las seis**, genera un certificado:

```bash
python labs/run_exercises.py --certificate "Juan Pérez" --lang es   # o en / ru
```

Escribe `certificate.html` — ábrelo en un navegador y **Print → Save as PDF** para una copia en PDF. El ID de credencial es un digest SHA-256 derivado de tu nombre + la fecha de emisión, y las etiquetas y badges de módulo del certificado están localizados para `en`/`ru`/`es`.

---

## Observabilidad en cada lab

Cada lab construye un `courselib.orchestration.Trace` y lo imprime al final. Los tipos de evento que verás:

- `well_known`, `manifest`, `discover`, `invoke`
- `channel_open`, `channel_close`
- `verify`, `register`
- `hire`, `step`, `capital` (solo capstone)

Lee el bloque trace para seguir la **historia económica** — descubrir → pagar → invocar → recibo → liquidar — no solo el resultado final. Trátalo como el «log de tests unitarios» del lab: una invocación fallida mapea a un evento de trace que puedes señalar.

Para la ruta de producción, el factory completo conecta OpenTelemetry + LangSmith — ver [observability-langsmith.md](https://github.com/alexar76/aicom/blob/main/docs/observability-langsmith.md) (no requerido para el curso).

---

## Puente: del curso al hub de producción

Ruta de graduación cuando las labs te resulten familiares:

1. Define `COURSE_HUB_URL=https://modelmarket.dev` (o tu propio hub).
2. Usa `courselib.economy.connect()` en lugar de `embedded_sandbox()`.
3. Los mismos métodos del SDK se mantienen: `discover`, `invoke`, `hire`.

Obtén un well-known en vivo y compáralo con el validador de M1:

```bash
curl https://modelmarket.dev/.well-known/ai-market.json
```

Pásalo por `courselib.protocol.validate_well_known` — las mismas comprobaciones estructurales del módulo M1 aplican a un hub real.

---

## Lista de autocomprobación

- [ ] `pytest -q` pasa en local
- [ ] Ejecutaste lab01–lab05 en el track `[hub-lite]`
- [ ] Ejecutaste lab06 con `[sandbox]` (o viste la omisión limpia hasta instalar las deps)
- [ ] Los seis ejercicios pasan: `python labs/run_exercises.py`
- [ ] Probaste al menos un lab con `COURSE_LANG=ru` o `es`
- [ ] Leíste un bloque trace y explicas discover → invoke → receipt
- [ ] Generaste un certificado con `--certificate "Tu Nombre"`

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: fastapi` (o `uvicorn`/`httpx`) | Instala los extras de hub-lite: `pip install -e ".[hub-lite,dev]"` |
| `ModuleNotFoundError: aimarket_agent` | El Lab 6 y los tests de economy necesitan el stack sandbox: `pip install -e ".[sandbox,dev]"`. En el monorepo, asegúrate de que `aimarket-agent/` y `aimarket-hub/` existen como directorios hermanos. |
| El capstone imprime «Capstone omitido» | Esperado sin el SDK — instala `[sandbox]` y vuelve a ejecutar. No es un error. |
| Timeout de hub-lite en el primer arranque | El arranque en frío tarda ~2–5 s; vuelve a ejecutar. CI espera por `/.well-known/ai-market.json`. |
| Los listados capital dan 500 en sandbox | `AIFACTORY_DATA_ROOT` debe apuntar dentro del directorio temporal del sandbox — `embedded_sandbox()` lo define automáticamente. |
| `ModuleNotFoundError: courselib` | Ejecuta desde la raíz del repo; las labs anteponen el directorio padre a `sys.path`. |
| Una clave aparece como `modules.m1.title` | Traducción faltante — revisa la paridad de claves de `i18n/en.json` (la fuerza `tests/test_i18n.py`). |
| Colab ejecuta código viejo | Vuelve a ejecutar la celda de setup; fija la rama `main`. |

**Problemas de Factory:** [FAQ.es.md](https://github.com/alexar76/aicom/blob/main/docs/FAQ.es.md)

---

## Regenerar sitio y notebooks

Tras editar labs o catálogos de i18n:

```bash
python3 scripts/build_course_assets.py
```

Las guías en `docs/` se mantienen a mano — actualiza EN primero, luego replica a RU/ES.

---

**Siguiente:** explora la [especificación de AIMarket Protocol](https://github.com/alexar76/aimarket-protocol/blob/main/spec.md) y conecta tu propia capability medida a un hub real.
