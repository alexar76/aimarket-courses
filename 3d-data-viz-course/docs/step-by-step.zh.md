# 分步指南 — 3D Data Visualization with Alien Monitor

> **对象：** 在 AIMarket 生态上构建的开发者。  
> **语言：** `COURSE_LANG=en|ru|es|fr|zh` · UI 文案在 `i18n/`  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md)

---

## 为什么学这门课

Probe alien-monitor API health, topology, and LUMEN reputation — then map oracle scenes to R3F.

实验调用生态的 **LIVE** 沙箱（或同接口的本地路径）。失败要响亮：离线时明确报错或使用文档化的 `[offline]` 模式——绝不伪造成功。

---

## 安装（约 10 分钟）

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/3d-data-viz-course
pip install -e ".[dev]"
pytest -q
export COURSE_LANG=zh
python labs/lab01_health_probe.py
```

Colab：打开[课程站点](https://alexar76.github.io/aimarket-courses/3d-data-viz-course/) → **Open in Colab**。

---

## 模块

| 模块 | 标题 | 实验 |
|------|------|------|
| M1 | Monitor health & modes | `lab01_health_probe` |
| M2 | Topology graph model | `lab02_topology_graph` |
| M3 | Federation reputation | `lab03_reputation_peers` |
| M4 | LUMEN PageRank scores | `lab04_lumen_scores` |
| M5 | R3F oracle scene mapping | `lab05_r3f_scenes` |

---

## 推荐路径

1. 阅读 lab 文档字符串中的概念。
2. 运行 lab（可选 `COURSE_LANG=zh`）。
3. 在 `courselib/exercises.py` 填写 `# YOUR CODE`。
4. `python labs/run_exercises.py --certificate "你的名字"`。

---

## 证书

证书**仅**在 CLI 中、全部练习通过后签发——浏览器勾选无效。

---

## 下一步

回到[学院门户](https://alexar76.github.io/aimarket-courses/)或 [School](https://edu.modelmarket.dev/) 上看 on-ramp 短片。
