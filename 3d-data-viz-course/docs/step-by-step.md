# Step-by-step course guide

> **Audience:** engineers who want to turn live ecosystem telemetry into 3D visualizations — probing the alien-monitor REST API, modelling its topology as a typed graph, and mapping oracle scenes to React Three Fiber.
> **Languages:** `COURSE_LANG=en|ru|es` · UI strings in `i18n/` · this guide in English.
> **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md)

---

## Why this course

[alien-monitor](https://github.com/alexar76/alien-monitor) is the live 3D map of the AIMarket ecosystem: a Hub, its federation peers, and a constellation of oracles, each rendered as an animated React Three Fiber scene. This course teaches the data layer behind that map. You learn to **probe** the monitor's REST API (`/api/health`, `/api/topology`, `/api/reputation/*`), **model** the responses as typed Python structures, **rank** nodes with the LUMEN PageRank/EigenTrust scores, and finally **map** each oracle slug to the camera, accent colour, and math-primitive metadata that the R3F front-end uses to draw its scene.

Every lab is **deterministic and offline-friendly**: if a live alien-monitor is not running on `127.0.0.1:9100`, each lab auto-starts an in-process mock server with the same REST shape, so the whole course runs with no network and no API keys. Every lab also prints a `Trace` block so behaviour is inspectable rather than magic.

---

## Table of contents

1. [Choose your track](#choose-your-track)
2. [Setup (10 minutes)](#setup-10-minutes)
3. [Module M1 — Monitor health & modes](#module-m1--monitor-health--modes)
4. [Module M2 — Topology graph model](#module-m2--topology-graph-model)
5. [Module M3 — Federation reputation](#module-m3--federation-reputation)
6. [Module M4 — LUMEN PageRank scores](#module-m4--lumen-pagerank-scores)
7. [Module M5 — R3F oracle scene mapping (advanced)](#module-m5--r3f-oracle-scene-mapping-advanced)
8. [Connect a live monitor](#connect-a-live-monitor)
9. [Exercises & certificate](#exercises--certificate)
10. [Observability: the Trace block](#observability-the-trace-block)
11. [Self-check checklist](#self-check-checklist)
12. [Troubleshooting](#troubleshooting)
13. [Next steps](#next-steps)

---

## Choose your track

| Track | Modules | Time | Live monitor | Front-end |
|-------|---------|------|--------------|-----------|
| **Basic** | M1 → M2 → M3 → M4 | ~1.5 h | Mock (auto) | None — pure Python |
| **Advanced** | Basic + M5 | +30 min | Mock or live | Maps to R3F specs |
| **Live bridge** | After M4 or M5 | +30 min | Real alien-monitor | Optional |

The mock server backs every track, so you never need a running monitor to finish the course. Read the [Trace section](#observability-the-trace-block) after each lab — every script prints a `Trace` you can inspect.

---

## Setup (10 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/alexar76/aimarket-courses.git
        cd aimarket-courses/3d-data-viz-course
pip install -e ".[dev]"
```

`[dev]` is the only extra you need — the labs use the Python standard library for HTTP probing, so there are no heavy runtime dependencies. `[dev]` adds `pytest` for the test suite.

### Step 2 — Verify tests

```bash
pytest -q
```

**Expected:** all tests pass (i18n parity across `en/ru/es`, graph parsing, R3F mapping, exercise checks).

### Step 3 — Run the first lab

```bash
python labs/lab01_health_probe.py
python labs/run_exercises.py
```

The first command probes the monitor (mock if none is live); the second runs the DIY checks for all five modules.

### Step 4 — Pick a language (optional)

```bash
export COURSE_LANG=ru   # or es, default en
python labs/lab01_health_probe.py
```

All module titles, concepts, labels, and exercise hints come from `i18n/{en,ru,es}.json`.

### Step 5 — Colab alternative

1. Open the [course site](https://alexar76.github.io/aimarket-courses/3d-data-viz-course/) → **Open in Colab** on any lab.
2. Run the **setup cell** (clone + `pip install -e ".[dev]"`).
3. Set `os.environ["COURSE_LANG"] = "ru"` in the setup cell if needed.
4. Run the lab cell — the mock server runs fine inside Colab.

---

## Module M1 — Monitor health & modes

**Concept:** Probe `/api/health` and understand TEST vs REAL vs UNIVERSE modes.
**Lab:** `labs/lab01_health_probe.py` · **Time:** ~15 min · **Industry map:** observability, SRE

### Steps

1. Open `labs/lab01_health_probe.py` and read the module docstring.
2. Run locally:

   ```bash
   python labs/lab01_health_probe.py
   ```

3. Read the output:
   - `Live alien-monitor reachable: True/False` — whether a real monitor was found on `127.0.0.1:9100`.
   - `result: status=ok mode=test` — the parsed `HealthStatus`. The `mode` is the monitor's data source: `test` (mock fixtures), `real` (live ecosystem), or `universe` (federated multi-hub view).
   - If a mock was used, you'll see the "in-process mock server" note.
   - A `trace` line with the event count.
4. Skim `courselib/viz.py` — find `probe_health`, `HealthStatus`, `monitor_reachable`, `resolve_monitor_url`.

### What it proves / produces

A working REST probe and the `resolve_monitor_url()` pattern (live-or-mock) that **every** later lab reuses.

### Self-check

- [ ] You can explain what `status` and `mode` mean
- [ ] You understand why labs fall back to a mock server

---

## Module M2 — Topology graph model

**Concept:** Parse nodes + links from `/api/topology` into typed graph structures.
**Lab:** `labs/lab02_topology_graph.py` · **Time:** ~20 min · **Prerequisites:** M1 · **Industry map:** graph viz, React Flow

### Steps

1. Run `python labs/lab02_topology_graph.py`.
2. Read the output: node and link counts, then up to six nodes printed as `id`, `group`, 3D `position`, and `status`.
3. Note the `Adjacency list: N directed edges` line — `TopologyGraph.adjacency()` deduplicates edges and drops self-loops, the shape a force-directed renderer consumes.
4. Open `courselib/viz.py` — study `MonitorNode`, `MonitorLink`, `TopologyGraph`, and `Vec3.from_dict`. Notice how `from_api` classmethods defensively coerce raw JSON into typed dataclasses.

### What it proves / produces

A typed in-memory graph (`nodes`, `links`, `adjacency()`, `node_ids()`, `oracle_slugs()`) — the model M4 and M5 build on.

### Self-check

- [ ] You can name the fields of a `MonitorNode`
- [ ] You understand why adjacency is deduplicated and self-loops removed

---

## Module M3 — Federation reputation

**Concept:** Enrich the trust graph with `/api/reputation/peers` from the Hub.
**Lab:** `labs/lab03_reputation_peers.py` · **Time:** ~20 min · **Prerequisites:** M2 · **Industry map:** EigenTrust, federation

### Steps

1. Run `python labs/lab03_reputation_peers.py`.
2. Read the output: `Federation peers: N (mode)` followed by each peer's `name`, `trust_score`, and `url`. A peer with no score prints `—`.
3. Open `courselib/viz.py` — study `ReputationPeer` and `ReputationPeers`. The `trust_score` is `float | None`, so your visualization must handle missing data.

### What it proves / produces

The federation layer of the graph: which external Hubs this monitor trusts, and by how much — the input to colour/size encodings of peer nodes.

### Self-check

- [ ] You can explain a `None` trust score vs a `0.0` score
- [ ] You see how peers extend the M2 topology with federation context

---

## Module M4 — LUMEN PageRank scores

**Concept:** Call `/api/reputation/lumen` and bind scores to graph nodes.
**Lab:** `labs/lab04_lumen_scores.py` · **Time:** ~20 min · **Prerequisites:** M2 · **Industry map:** reputation oracles

### Steps

1. Run `python labs/lab04_lumen_scores.py`.
2. Read the output: nodes sorted by score, each with a `█` bar chart and the score to 4 decimals, then `PageRank iterations: N`.
3. If LUMEN is unavailable the lab prints a `LUMEN error` line instead of crashing — note the `lumen.ok` guard.
4. Open `courselib/viz.py` — study `LumenScores` and `by_id()`, which zips `ids` with `scores` so you can join PageRank values onto the M2 node ids.

### What it proves / produces

A node-id → reputation-weight map. LUMEN is the EigenTrust/PageRank power-iteration oracle; these weights drive node sizing in the live 3D map.

### Self-check

- [ ] You can join a LUMEN score onto a topology node by id
- [ ] You know roughly why the scores sum to ~1.0 (a probability distribution)

---

## Module M5 — R3F oracle scene mapping (advanced)

**Concept:** Map oracle slugs to camera, accent, and primitive metadata for Three.js scenes.
**Lab:** `labs/lab05_r3f_scenes.py` · **Time:** ~30 min · **Prerequisites:** M2 · **Industry map:** React Three Fiber, WebGL

### Steps

1. Run `python labs/lab05_r3f_scenes.py`.
2. Read the output: `Oracle R3F scenes: N`, then per scene the `slug`, kind (`r3f` or `ambient`), `camera` tuple, `accent` colour, and a truncated `primitive` description.
3. Open `courselib/viz.py` — study `ORACLE_SCENE_META`, `R3FSceneSpec.for_oracle`, and `map_graph_to_r3f_scenes`. The metadata table is mirrored from `alien-monitor/frontend/src/oracleScenes/meta.ts`, so the Python spec and the front-end stay in sync.
4. Notice `TopologyGraph.oracle_slugs()` — it strips the `oracle-` prefix or matches `group == "oracle"`, then each slug looks up its camera/accent/primitive (with sensible fallbacks for unknown slugs).

### What it proves / produces

A list of `R3FSceneSpec` objects — exactly the camera position, accent, and primitive a React Three Fiber `<Canvas>` needs to render each oracle. This closes the loop from REST telemetry to a 3D scene.

### Self-check

- [ ] You can trace one oracle slug to its camera + accent + primitive
- [ ] You understand `ambient` scenes vs regular `r3f` scenes
- [ ] You can explain why the metadata is mirrored from the front-end's `meta.ts`

---

## Connect a live monitor

By default the labs run against the built-in mock. To probe a real alien-monitor:

```bash
# point the labs at any running monitor (default is http://127.0.0.1:9100)
export ALIEN_MONITOR_URL=http://127.0.0.1:9100
python labs/lab01_health_probe.py
```

When the monitor is reachable, `resolve_monitor_url()` skips the mock and `Live alien-monitor reachable: True` appears. The same five labs then visualize the **real** ecosystem — modes flip from `test` to `real`/`universe`, the topology shows live nodes, and LUMEN returns live PageRank scores.

---

## Exercises & certificate

After the labs, run the DIY checks:

```bash
python labs/run_exercises.py             # run all five module checks
python labs/run_exercises.py --module m4 # run just one module
```

Each module's check (`exercise_m1_health_ok` … `exercise_m5_r3f_mapping`) asserts the property the lab taught — e.g. m1 asserts `status == "ok"` and a valid mode, m4 asserts `len(scores) == len(ids)`.

Once all checks pass, generate the certificate:

```bash
python labs/run_exercises.py --certificate "Your Name" --lang en   # or ru / es
```

This writes `certificate.html` (credential ID derived from name + date). Open it in a browser and **Print → Save as PDF** for a PDF copy. Pass all module checks to unlock the certificate.

---

## Observability: the Trace block

**Concept:** Every lab records a `Trace` so its behaviour is inspectable, not magic.
**Covered in:** every lab · **Time:** ~5 min after each lab

### Steps (repeat after M1–M5)

1. Scroll to the `trace (N events)` line at the end of the lab output.
2. Each lab logs structured events: M1 logs `health`, M2 logs one `node` per node, M3 logs `peer`, M4 logs `lumen_score`, M5 logs `r3f_scene`.
3. Map each event back to a line you saw in stdout — the trace is the lab's "unit-test log" for what it probed and produced.

### Self-check

- [ ] You can correlate one trace event to one printed result
- [ ] You can name which event type each lab emits

---

## Self-check checklist

After the basic track you should be able to:

- [ ] Run lab01–lab04 locally and in Colab, mock or live
- [ ] Explain `/api/health` modes (test / real / universe)
- [ ] Describe a `MonitorNode` and the adjacency list
- [ ] Distinguish federation peer trust (M3) from LUMEN PageRank (M4)
- [ ] Read a `Trace` block and map events to output

After the advanced track add:

- [ ] Run lab05 and map an oracle slug to its R3F scene spec
- [ ] Explain why `ORACLE_SCENE_META` is mirrored from the front-end

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: courselib` | Run from the repo root; labs prepend the parent dir to `sys.path` |
| `Live alien-monitor reachable: False` | Expected with no live monitor — the in-process mock takes over automatically |
| Want to use a live monitor | Start alien-monitor on `127.0.0.1:9100` or set `ALIEN_MONITOR_URL` |
| LUMEN error / empty scores | Live monitor returned no LUMEN data; the lab guards on `lumen.ok` and keeps running |
| Empty RU/ES strings | Set `COURSE_LANG`; check `i18n/ru.json` keys match `en.json` |
| pytest i18n parity failure | Add the missing key to all three of `en/ru/es.json` |
| Colab running stale code | Re-run the setup cell; pin the `main` branch |

---

## Next steps

- **See it rendered:** clone [alien-monitor](https://github.com/alexar76/alien-monitor) and open its 3D map — the camera/accent/primitive you produced in M5 are exactly what its R3F scenes consume.
- **Go live:** point the labs at a running monitor via `ALIEN_MONITOR_URL` and re-run M1–M5 against the real ecosystem.
- **Extend the model:** add a new oracle slug to `ORACLE_SCENE_META`, mirror it in the front-end's `meta.ts`, and watch M5 pick it up.
- **Explore the ecosystem:** the [aicom](https://github.com/alexar76/aicom) monorepo hosts the Hub, oracles, and the rest of the AIMarket platform this course visualizes.

Guides in `docs/` are hand-maintained — update EN first, then the RU/ES mirrors.
