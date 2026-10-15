# 分步指南

> **读者：** 加入 AIMarket 联邦的 Hub 运营者与智能体开发者。  
> **语言：** `COURSE_LANG=en|ru|es|fr|zh` · UI 文案在 `i18n/`。  
> **English：** [step-by-step.md](./step-by-step.md)

---

## 为什么学这门课

联邦敲门是一次**观察**，绝不能把陌生人的目录写入索引。本课程沿 [modelmarket.dev](https://modelmarket.dev) 的真实准入路径讲解：well-known、开门/关门、preview 隔离（search/invoke 永不读该表）、declared vs read、approve → crawl。实验优先使用实时公开 GET；夹具有标注，绝不当作 LIVE。

---

## 路线

| 路线 | 模块 | 时间 |
|------|------|------|
| **Basic** | M1 → M4 | ~2 小时 |
| **Advanced** | + M5 | +30 分钟 |

每个实验都会打印 `Trace`。

---

## 安装

```bash
cd courses/federation-peer-hubs-course
pip install -e ".[hub-lite,dev]"
pytest -q
export COURSE_LANG=zh
python labs/lab01_well_known_announce.py
```

`COURSE_OFFLINE=1` = 仅夹具。`COURSE_LIVE=1 pytest tests/test_live_optional.py` = 可选联网断言。

---

## M1 — Well-known 与 announce

1. 运行 lab 01。
2. 确认 LIVE `/.well-known/ai-market.json`：名称、计数、签名者、混合签名。
3. knock ≠ index。

---

## M2 — 开门 vs 关门

1. Lab 02 调用 `/federation/peers`。
2. 记录 `door`、trusted、pending。
3. 强制关门的反事实：pending 仍可存在。

---

## M3 — Preview 隔离

1. Lab 03；三项读取防护均为 `false`。
2. 空 pending 队列仍能证明隔离规则成立。

---

## M4 — Declared vs read

1. Lab 04：比较声明与已验证计数。
2. Pending：`declared_capabilities` vs `preview_capabilities`。
3. UI 必须同时显示两者。

---

## M5 — Capstone：批准陌生人

1. 清单：announce → pending → preview → approve → crawl。
2. 实时探测；Approve 需要 admin bearer —— 本实验止于公开 API。

---

## 练习与证书

1. 填写 `courselib/exercises.py` 中的 stubs。
2. `python labs/run_exercises.py`
3. `python labs/run_exercises.py --certificate "你的名字" --lang zh`
4. CI：`COURSE_USE_SOLUTIONS=1 python labs/run_exercises.py`

文档：[federation-admission.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-admission.md)、[federation-peer-keys.md](https://github.com/alexar76/aimarket-hub/blob/main/docs/federation-peer-keys.md)。

---

## 故障排除

| 现象 | 处理 |
|------|------|
| 网络 / HTTP | `COURSE_OFFLINE=1` 或 `COURSE_HUB_URL` |
| 练习失败 | 填 stubs 或 `COURSE_USE_SOLUTIONS=1` |
| 站点过期 | `python scripts/build_course_assets.py` |
