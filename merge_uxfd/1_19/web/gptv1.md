# gptv1 (Archived Prompt + Review Notes)

> 状态：本仓库已落地一版“UXFD SSOT + runnable demos + registry/atlas 闭环”。本文件保留为历史参考（用于追溯当时的 Prompt 与评审点），但 **不要再把它当成当前仓库的接口定义**。

已落地（当前事实 SSOT）：
- `src/model_factory/X_model/UXFD/FACT_TABLE.md`（事实表 + 产物契约）
- `src/model_factory/X_model/UXFD/OPERATOR_CATALOG.md`（`ALL_SP`/`ALL_FE` key catalog）
- `configs/base/model/tspn_uxfd.yaml`（core base model）
- `configs/demo/uxfd/README.md` + `configs/demo/uxfd/*.yaml`（3 个可跑 demo）
- `configs/config_registry.csv` + `docs/CONFIG_ATLAS.md`（可检索闭环）
- `src/model_factory/X_model/UXFD/README.md`（入口 README + quick validate）

---

你贴的这份 Prompt **方向是对的**（把“上下文加载→再写 README”这条链路固定下来），但里面有几处**容易让 agent 走偏/幻觉**的点。我先逐条“验准—补强”，再给一份“取长补短后的终版 Prompt”（可直接丢给 agent 用）。

---

## 这份 Prompt 哪些点是准确且值得保留的

* **把架构中心锚在 `TSPN_UXFD.py` + 两个算子库文件**，而不是先入为主写 backbone+head，这是最关键的纠偏（保留）。
* **先读代码再写文档**（Step1→Step2）的流程是正确的，能显著降低“文档脱离实现”的风险（保留）。
* 要求 README 必须包含 **Mermaid 数据流图**、以及最后的 **“Agent Context Injection”块**，对后续多 agent 协作非常有用（保留）。

---

## 哪些点可能不准确 / 容易导致幻觉（建议改）

1. **“Signal_processing 负责 STFT/小波/FFT/CWT”**
   这属于“举例式假设”。如果源码里没有 STFT 或 CWT，agent 就会在 README 里**编造算子清单**。
   ✅ 改法：要求 agent **从源码枚举实际算子**，禁止先写“如 STFT、小波”。

2. **“Feature_extract.py 中有 CNN_1D / StatisticalFeatures”等类名**
   同样属于可能不一致的占位符。
   ✅ 改法：把这类示例改成：“列出 Feature_extract.py 中出现的类/注册表项（按源码为准）”。

3. **“请调用 File Fetcher”**
   这是特定平台/特定工具名，并不总存在；换环境就会卡住。
   ✅ 改法：写成与工具无关的动作：*打开并逐行阅读这些文件*（允许 agent 用 `ripgrep/grep/sed` 等）。

4. **缺少“配置体系闭环”要求**
   你仓库的“maintained workflow”是 config-first：入口 `python main.py --config ...`，并且有 `validate_configs / config_inspect / gen_config_atlas / validate_docs` 这种门禁工具链。([GitHub][1])
   但当前 Prompt 只是让写 README + 一个 config 片段，**没有要求产出可运行 demo YAML、注册 registry、让 atlas 可检索** → 很容易写成“漂亮但跑不起来”的文档。
   ✅ 改法：把交付升级为：README + Operator Catalog + 至少 3 个可跑 demo configs + registry + atlas 更新 + 自检命令。

5. **“TSPN Logic(Decision)”表述过泛**
   如果 `TSPN_UXFD` 里并不是“原型网络/逻辑推理”，就会误导。
   ✅ 改法：要求 agent 以“代码事实”描述：到底是 prototype、route、fuse、classifier，还是别的；并给证据定位。

---

## 取长补短：推荐的“终版 Prompt”（直接复制用）

> 下面这版把你原 Prompt 的优点保留，同时补上：**(i) 禁止臆测 + 证据标注**，**(ii) config-first 闭环**，**(iii) 文档/配置/atlas 的 SSOT 流水线**。并显式对齐仓库维护口径。([GitHub][1])

```text
# Agent Execution Prompt: TSPN_UXFD Neural-Symbolic Context → SSOT Docs + Runnable Configs

Role: 代码事实驱动的 Research Engineer & Technical Writer
Language: 中文
Goal: 让后续所有 Agent 都能“按事实维护”TSPN_UXFD 神经符号架构；产出可运行配置与唯一事实文档（SSOT）。

## 0) 维护口径（必须遵守）
本仓库 maintained workflow 是 config-first：
- 入口：python main.py --config <yaml> [--override key=value ...]
- 模板：configs/demo/（复制到 configs/experiments/ 作为本地变体）
- 工具链：scripts.validate_configs / scripts.config_inspect / scripts.gen_config_atlas / scripts.validate_docs
（以上口径不得违背；所有文档必须链接到 configs/README.md、configs/demo/、docs/CONFIG_ATLAS.md）

## 1) 必读输入（逐行阅读，禁止跳过）
A. src/model_factory/X_model/TSPN_UXFD.py
B. src/model_factory/X_model/Signal_processing.py
C. src/model_factory/X_model/Feature_extract.py
D. src/model_factory/X_model/UXFD/README.md（现状评估）
E. configs/README.md、configs/demo/**、configs/config_registry.csv、docs/CONFIG_ATLAS.md

## 2) 反幻觉硬约束（不满足即失败）
- 禁止臆测：不得先写“STFT/CWT/小波/FFT/某某类名”，除非它们确实出现在代码中。
- 所有关键陈述必须带证据定位：
  格式：[evidence] path/to/file.py:L123-L145
  （行号以你本地仓库为准；如果你无法拿到行号，就用“关键函数名+上下文片段”作为替代，并标 TODO:LINE）
- 文档里给出的任何配置字段名/默认值/可选项，都必须来自源码或现有 YAML 的证据。
- 输出必须可运行：至少提供 3 个 runnable demo YAML，并能用统一入口运行。

## 3) Step 1 — 架构事实表（先事实，后写作）
输出一个 “FACT_TABLE.md”（可放在 docs/ 或临时输出里），包含：

(1) TSPN_UXFD 的配置入口
- TSPN_UXFD 从哪里读取 config？字段路径是什么？（比如 model.args.xxx —— 以源码为准）
- 它如何实例化 Signal_processing/Feature_extract？（类名/工厂/registry）

(2) 数据流（forward）
- 原始信号张量形状/维度约定（若可推断）
- Signal_processing 的输出是什么（张量/字典/多分支）
- Feature_extract 的输入输出是什么（embedding/特征向量/多尺度）
- 最终 decision/head 是什么（分类器/原型/路由融合/逻辑模块 —— 按事实命名）

(3) 算子与特征清单（源码枚举）
- Signal_processing.py：列出所有可用算子/变换/模块（按源码真实出现的函数/类/注册项分组）
- Feature_extract.py：列出所有提取器/特征模块
对每项给出：输入/输出、关键参数、是否可学习/可微（能从代码判断则写，否则 TODO:VERIFY）

## 4) Step 2 — 产出可运行 Demo Config（先跑通，再写 README）
新增目录（若已存在则复用）：
- configs/demo/uxfd/

至少新增 3 个可运行 YAML（名称建议含序号，便于 atlas 排序）：
- 00_smoke_tspn_uxfd.yaml：最小链路（尽量可复用现有 dummy/smoke 的 data/task/trainer）
- 10_diag_symbolic_chain.yaml：典型“信号处理→特征→决策”的神经符号链
- 20_diag_with_route_or_xai.yaml：打开路由/解释/证据输出（若代码支持）

要求：
- 每个 YAML 都能直接运行：
  python main.py --config <yaml>
- 提供 2~3 个推荐 override 示例（不复制 YAML 做消融）：
  python main.py --config <yaml> --override model.args.xxx=... trainer.num_epochs=1

并更新：
- configs/config_registry.csv（登记这 3 个 demo）
- 运行 scripts.gen_config_atlas 使 docs/CONFIG_ATLAS.md 可检索到它们

## 5) Step 3 — 重写 SSOT README（面向用户，不讲“backbone”叙事）
重写：src/model_factory/X_model/UXFD/README.md
结构必须包含：

1) 一句话定义：TSPN_UXFD 是“神经符号算子图编排器”，不是 backbone+head（并给证据）
2) Mermaid 架构图：必须体现三个文件的真实交互（节点命名以代码事实为准）
3) 模块说明（Code Mapping）：
   - Signal_processing：列出真实算子类别/代表项
   - Feature_extract：列出真实提取器/特征模块
   - TSPN_UXFD：解释它如何组装、路由、融合、输出（按事实）
4) “如何配置”只暴露少数旋钮：
   - 旋钮必须来自真实字段（来自 Step1 的 FACT_TABLE）
   - 链接到 configs/demo/uxfd/ 的 3 个 YAML，并给运行命令
5) FAQ：没有 backbone 的原因 / 如何做消融 / 如何打印最终展开配置与算子图
6) README 末尾加入 “Agent Context Injection” 块：
   - 用 10~15 行，告诉未来 Agent 修改入口在哪些文件/哪些关键函数/哪些字段最危险
   - 明确禁止：不要凭空添加不存在的算子；新增算子必须同步 Operator Catalog + demo config + registry + atlas

README 顶部必须有相对链接区：
- ../../../../configs/README.md
- ../../../../configs/demo/uxfd/
- ../../../../docs/CONFIG_ATLAS.md

## 6) Step 4 — 生成算子手册（面向开发者）
新增：src/model_factory/X_model/UXFD/OPERATOR_CATALOG.md
- 从源码枚举所有 Signal/Feature 模块（与 FACT_TABLE 一致）
- 每个条目：用途、输入输出、关键参数、配置字段映射、最小示例 override

## 7) 自检命令（必须执行并记录结果）
python -m scripts.validate_configs
python -m scripts.config_inspect --config configs/demo/uxfd/00_smoke_tspn_uxfd.yaml --override trainer.num_epochs=1
python -m scripts.gen_config_atlas && git diff --exit-code docs/CONFIG_ATLAS.md
python -m scripts.validate_docs

## 8) 最终交付清单（输出 diff 摘要）
- src/model_factory/X_model/UXFD/README.md（重写）
- src/model_factory/X_model/UXFD/OPERATOR_CATALOG.md（新增）
- configs/demo/uxfd/*.yaml（新增 ≥3）
- configs/config_registry.csv（更新）
- docs/CONFIG_ATLAS.md（更新）
- FACT_TABLE.md（新增：架构证据表）
```

---

如果你想再“更稳一点”，我建议你把 **Step 1 的 FACT_TABLE** 作为硬门禁：README 里每一句关键描述都必须能指回 FACT_TABLE 的证据条目（否则就标 TODO:VERIFY），这样后面再复杂的 UXFD 扩展也不容易被 agent 写歪。([GitHub][1])

[1]: https://github.com/PHMbench/PHM-Vibench/tree/lq_merge_UXFD "GitHub - PHMbench/PHM-Vibench at lq_merge_UXFD"
