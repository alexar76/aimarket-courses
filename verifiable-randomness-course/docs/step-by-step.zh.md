# 分步指南 — Verifiable Randomness & Cryptographic Time

> **对象：** 在 AIMarket 生态上构建的开发者。  
> **语言：** `COURSE_LANG=en|ru|es|fr|zh` · UI 文案在 `i18n/`  
> **English:** [step-by-step.md](./step-by-step.md) · **Русский:** [step-by-step.ru.md](./step-by-step.ru.md) · **Español:** [step-by-step.es.md](./step-by-step.es.md) · **Français:** [step-by-step.fr.md](./step-by-step.fr.md)

---

## 为什么学这门课

Build and break biased lotteries — then verify proofs offline from 80 bytes.

实验调用生态的 **LIVE** 沙箱（或同接口的本地路径）。失败要响亮：离线时明确报错或使用文档化的 `[offline]` 模式——绝不伪造成功。

---

## 安装（约 10 分钟）

```bash
git clone https://github.com/alexar76/aimarket-courses.git
cd aimarket-courses/verifiable-randomness-course
pip install -e ".[dev]"
pytest -q
export COURSE_LANG=zh
python labs/lab01_platon_chaos.py
```

Colab：打开[课程站点](https://alexar76.github.io/aimarket-courses/verifiable-randomness-course/) → **Open in Colab**。

---

## 模块

| 模块 | 标题 | 实验 |
|------|------|------|
| M1 | Chaos VRF with Platon | `lab01_platon_chaos` |
| M2 | VDF time with Chronos | `lab02_chronos_vdf` |
| M3 | ECVRF & Sortes | `lab03_sortes_ecvrf` |
| M4 | Time-lock RSW with Aestus | `lab04_aestus_timelock` |
| M5 | Commit–reveal & bias attacks | `lab05_commit_reveal` |
| M6 | On-chain verification | `lab06_onchain_consumer` |

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
