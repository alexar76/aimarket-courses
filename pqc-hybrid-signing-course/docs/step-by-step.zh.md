# 分步指南 — PQC · 混合签名

> **语言：** `COURSE_LANG=en|ru|es|fr|zh` · [EN](./step-by-step.md) · [RU](./step-by-step.ru.md) · [ES](./step-by-step.es.md) · [FR](./step-by-step.fr.md)

## 为何学这门课

签名是关于**过去**的断言。若干年后被争议的回执，今天就必须能抵抗量子对手。仅用 ML-DSA 替换 Ed25519 会破坏今日互操作。AIMarket Hub 已发布**混合**签名：Ed25519 + ML-DSA-65 — LIVE：[`modelmarket.dev/.well-known/ai-market.json`](https://modelmarket.dev/.well-known/ai-market.json)。切勿把 SIM 当成 LIVE。

## 安装

```bash
pip install -e ".[dev]"
pip install -e ".[pqc,dev]"   # 可选
pytest -q
COURSE_LANG=zh python labs/lab01_why_hybrid.py
```

无 dilithium 时仍可校验 Ed25519、检查 LIVE 字段；PQ 签名会标明跳过 — 绝不伪造成功。

## 模块

| 模块 | 实验 | 要点 |
| --- | --- | --- |
| M1 | `lab01_why_hybrid` | 为何混合；可选 LIVE |
| M2 | `lab02_key_identity` | 双轨道身份；带外固定两钥 |
| M3 | `lab03_sign_receipt` | 签署回执 |
| M4 | `lab04_verify_offline` | 离线校验 |
| M5 | `lab05_hybrid_gate_capstone` | `refuse_single_orbit`（阶段 3） |

## 练习

在 `courselib/exercises.py` 填写 `# YOUR CODE HERE` → `python labs/run_exercises.py` → `--certificate "姓名"`。

## 自检

- [ ] 理解无 `require_pq` 时的降级攻击
- [ ] 离线经典校验可用
- [ ] 门控拒绝单轨道
- [ ] 检查过 LIVE 且未称为 SIM
