# 分步指南 — AI Agent Orchestration

> **对象：** 在 AIMarket 生态上构建的开发者。  
> **语言：** `COURSE_LANG=en|ru|es|fr|zh` · UI 文案在 `i18n/`  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md)

---

## 为什么学这门课

Hands-on Python course on AI agent orchestration patterns and agent economy.

实验调用生态的 **LIVE** 沙箱（或同接口的本地路径）。失败要响亮：离线时明确报错或使用文档化的 `[offline]` 模式——绝不伪造成功。

---

## 安装（约 10 分钟）

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/orchestration-course
pip install -e ".[dev]"
pytest -q
export COURSE_LANG=zh
python labs/lab01_agent_and_tool.py
```

Colab：打开[课程站点](https://alexar76.github.io/aimarket-courses/orchestration-course/) → **Open in Colab**。

---

## 模块

| 模块 | 标题 | 实验 |
|------|------|------|
| M1 | m1 | `lab01_agent_and_tool` |
| M2 | m2 | `lab02_topologies` |
| M3 | m3 | `lab03_handoff` |
| M4 | m4 | `lab04_discover_invoke` |
| M5 | m5 | `lab05_state_context` |
| M6 | m6 | `lab06_guardrails` |
| M7 | m7 | `lab07_receipt_verify` |
| M8 | m8 | `lab08_metered_economy` |
| M9 | m9 | — |

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

**在真实枢纽上：** 设置 `COURSE_HUB_URL=https://modelmarket.dev`，用 `courselib.economy.connect()` 代替 `embedded_sandbox()`——同样的 `discover`、`invoke`、`hire` 直接在线运行。付费调用用一个密钥支付：在 [modelmarket.dev/start](https://modelmarket.dev/start?lang=zh) 获取并用 USDC 充值（最低 $0.01），设置 `COURSE_API_KEY=aimk_…`，它作为 `X-API-Key` 发送，每次调用从预付余额扣款。没有密钥时，付费调用返回 `payment_required` 并列出付款方式。

回到[学院门户](https://alexar76.github.io/aimarket-courses/)或 [School](https://edu.modelmarket.dev/) 上看 on-ramp 短片。
