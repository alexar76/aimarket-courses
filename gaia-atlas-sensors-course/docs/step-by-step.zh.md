# 课程分步指南

> **受众：** 在向 Hub SKU 收费之前，将物理世界传感器接入 GAIA / ATLAS 的开发者与运营者。  
> **语言：** `COURSE_LANG=en|ru|es|fr|zh` · UI 文案在 `i18n/` · 本指南为中文。  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md)

---

## 为什么学这门课

GAIA 将经证明的 IoT 读数暴露为 Hub 能力（`gaia.weather.read@v1`、`gaia.fleet.status@v1` 等）。ATLAS 把同一机队变成运营者地图（`atlas.nearest.read@v1`）。难点不在 HTTP，而在**诚实性**（Open-Meteo ≠ 实地测站；SIM ≠ LIVE）与**许可证**（商业轨道仅允许 CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY）。本课程通过面向线上沙箱的实验同时教授这两点：

| 服务 | URL |
|------|-----|
| GAIA | https://iot.modelmarket.dev |
| ATLAS | https://atlas.modelmarket.dev |

实验在可达时调用 live API；离线时打印清晰的 `[offline]` 行，并且**绝不编造读数**。

权威文档：[LIVE-RELAYS.md](https://github.com/alexar76/gaia/blob/main/docs/LIVE-RELAYS.md) · [add-gaia-atlas-sensor.md](https://github.com/alexar76/aicom/blob/main/docs/add-gaia-atlas-sensor.md)

---

## 目录

1. [选择学习路径](#选择学习路径)
2. [安装（10 分钟）](#安装10-分钟)
3. [模块 M1 — 什么是 LIVE 中继](#模块-m1--什么是-live-中继)
4. [模块 M2 — 许可证与商业轨道](#模块-m2--许可证与商业轨道)
5. [模块 M3 — 机队与图钉诚实性](#模块-m3--机队与图钉诚实性)
6. [模块 M4 — ATLAS 运营者地图](#模块-m4--atlas-运营者地图)
7. [模块 M5 — 顶点项目：添加传感器](#模块-m5--顶点项目添加传感器)
8. [练习与证书](#练习与证书)
9. [自检清单](#自检清单)
10. [故障排除](#故障排除)

---

## 选择学习路径

| 路径 | 模块 | 时间 | 网络 |
|------|------|------|------|
| **基础** | M1 → M2 → M3 → M4 | ~2 小时 | 可选 |
| **进阶** | 基础 + M5 | +30 分钟 | 可选 live 机队计数 |
| **运维桥接** | M5 之后 | +30 分钟 | Live GAIA + ATLAS + Recipe A |

---

## 安装（10 分钟）

### 步骤 1 — 克隆并安装

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

**在 aicom 单体仓库中：**

```bash
cd courses/gaia-atlas-sensors-course
pip install -e ".[dev]"
```

### 步骤 2 — 验证测试

```bash
pytest -q
```

**预期：** i18n 五语对齐、licence/honesty 单元测试、练习题解、实验导入冒烟。若 GAIA 不可达或设置了 `COURSE_SKIP_NETWORK=1`，网络测试会自动跳过。

### 步骤 3 — 选择语言（可选）

```bash
export COURSE_LANG=zh
python labs/lab01_live_vs_sim.py
```

### 步骤 4 — Live 端点

```bash
export COURSE_GAIA_URL=https://iot.modelmarket.dev
export COURSE_ATLAS_URL=https://atlas.modelmarket.dev
```

---

## 模块 M1 — 什么是 LIVE 中继

**概念：** HTTPS 允许列表、失败即离线、绝不编造读数。  
**实验：** `labs/lab01_live_vs_sim.py` · **时间：** ~20 分钟

### 步骤

1. 阅读 docstring — 教学对 `om-wx-01`（LIVE）与 `ws-01`（SIM）。
2. 运行 `python labs/lab01_live_vs_sim.py`。
3. 确认离线 `classify_mode` 断言在无网络时也能通过。
4. 在线时查看 `/health` 设备数与两侧 weather invoke。
5. 浏览 `courselib/sensors.py`。

### 自检

- [ ] 仅当机队设备设置了 `source` 时才为 LIVE
- [ ] 不会把 `ws-01` 标成 LIVE

---

## 模块 M2 — 许可证与商业轨道

**概念：** 仅 CC0 / CC BY / OGL / PD。  
**实验：** `labs/lab02_licence_gate.py` · **时间：** ~20 分钟

### 步骤

1. 运行实验并阅读内嵌 pass/fail 表。
2. **通过：** OpenAQ、USGS/NWS PD、Safecast CC0、FIRMS、UK OGL。
3. **失败：** AirNow（需 assent）、OpenSky、ADSBx、PurpleAir、BY-NC。

### 自检

- [ ] 能背出 pass-bar 许可家族
- [ ] 知道 AirNow 是 Hold，不是「几乎上线」

---

## 模块 M3 — 机队与图钉诚实性

**概念：** Open-Meteo ≠ 测站；公共 AIS ≠ 自有边缘。  
**实验：** `labs/lab03_honesty_claims.py` · **时间：** ~20 分钟

### 自检

- [ ] 会拒绝「Open-Meteo 是实地测站」
- [ ] 诚实离线策略 = fail-loud、不扣费

---

## 模块 M4 — ATLAS 运营者地图

**概念：** nearest、distance、mode/source。  
**实验：** `labs/lab04_atlas_map_read.py` · **时间：** ~20 分钟

### 步骤

1. 先做离线 payload 形状断言。
2. 在线：在柏林附近（`52.52, 13.41`）调用 `atlas.nearest.read@v1`。
3. 查看 ATLAS `/health` 的 `stations`。

---

## 模块 M5 — 顶点项目：添加传感器

**概念：** Recipe A — licence → kind → YAML → 重新部署 GAIA→ATLAS → honesty。  
**实验：** `labs/lab05_add_sensor_capstone.py` · **时间：** ~25 分钟

### 自检

- [ ] 重新部署顺序：先 GAIA 再 ATLAS
- [ ] LIVE 需要 `GAIA_ENABLE_LIVE=1` 与真实 `source`

---

## 练习与证书

学生桩：`courselib/exercises.py`（`# YOUR CODE HERE`）。  
参考解：`courselib/exercise_solutions.py`。

```bash
python labs/run_exercises.py
python labs/run_exercises.py --certificate "张三" --lang zh
```

浏览器勾选**不会**签发证书。

---

## 自检清单

- [ ] M1：用 `source` 区分 LIVE / SIM
- [ ] M2：pass-bar；AirNow Hold
- [ ] M3：honesty 分类器
- [ ] M4：nearest 形状 + live 读取
- [ ] M5：Recipe A 顺序 + 机队计数
- [ ] 练习已填；CLI 证书成功

---

## 故障排除

| 现象 | 处理 |
|------|------|
| `[offline] … unreachable` | 检查网络，或继续离线——单元路径仍可教学 |
| `SensorsError: HTTP …` | 检查 `capability_id` 与 `device_id` |
| pytest 网络测试 skip | 离线属正常；去掉 `COURSE_SKIP_NETWORK` 可跑 live |
| 全部 exercises 失败 | 填写 stubs——设计如此 |
| 语言不对 | `COURSE_LANG` ∈ `en,ru,es,fr,zh` |

环境变量：`COURSE_GAIA_URL`、`COURSE_ATLAS_URL`、`COURSE_LANG`、`COURSE_SKIP_NETWORK=1`。
