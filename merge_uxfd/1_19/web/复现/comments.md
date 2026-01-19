这份计划切中了当前 UXFD 工程化的核心痛点：**配置爆炸与复用性差**。

将“模型算子装配（Model Assembly）”与“实验环境配置（Experiment Context）”解耦，是实现 LLM 安全调用和大规模消融实验的前提。

以下是我的 **Comments（评审意见）** 和 **优化后的执行计划**。

---

### 1. Comments (评审意见)

1. **架构设计的正确性 (Soundness)**:
* **Composition > Inheritance**: 提议的 `base_configs: list[str]` 实际上是实现了配置的**组合模式**，优于单纯的树状继承。这对于 UXFD 这种“同一个骨架，换不同的器官（算子）”的场景非常合适。
* **Backward Compatibility**: 保持对旧 YAML（`base_configs` 为 string）的兼容性至关重要，这在计划中被考虑到了，值得肯定。


2. **遗漏点与风险 (Gaps & Risks)**:
* **Merge Order (覆盖优先级)**: 计划中提到了“递归 merge”，但必须明确 **优先级定义**。
* 推荐标准：`Current YAML` > `base_configs[-1]` (列表最后一个) > ... > `base_configs[0]`。必须在代码注释和文档中写死这一规则，防止“算子 A 覆盖了算子 B”的意外。


* **Preset 可见性**: 仅仅建立文件夹是不够的。LLM 或用户如何知道有哪些 preset 可用？
* *建议*: 增加一个自动生成 `docs/PRESET_CATALOG.md` 的步骤（类似算子目录）。


* **Config Inspection (调试困难)**: 引入多层叠加后，用户很难直观看到最终生效的配置。
* *建议*: 必须强化 `scripts/config_inspect.py`，支持 `--resolve` 参数，打印出 merge 后的完整 JSON/YAML，用于 debug。




3. **LLM 交互优化**:
* Preset 机制不仅是为了变薄 YAML，更是为了给 LLM 提供 **“高层语义工具”**。
* *未来展望*: LLM 不需要知道 `n_fft` 是多少，它只需要选择 `preset: "high_freq_resolution"`。



---

### 2. 优化后的执行计划 (Optimized Execution Plan)

我将任务细化为 **Infrastructure (T0-T1)**, **Content (T2-T4)**, 和 **Tooling (T5-T6)** 三个阶段。

#### Phase 1: Infrastructure & Core Logic (T0 - T1)

* **T0: 定义 Preset 规范与目录结构**
* 创建 `configs/presets/uxfd/operators/README.md`，定义 YAML 必须包含 `model.uxfd` 或 `model.feature_extractor` 字段，**禁止**包含 `trainer` 或 `data` 字段（强制隔离）。


* **T1: 改造 `config_utils.py` (核心)**
* 修改 `load_config` 函数：
* 检查 `base_configs` 类型。
* 若是 `list`，遍历加载 -> `recursive_merge`。
* **关键**: 编写单元测试 `test/test_config_composition.py`，验证 `list` 顺序覆盖逻辑是否符合预期。





#### Phase 2: Preset Migration & Verification (T2 - T4)

* **T2: 制作 "Golden Presets" (基准预设)**
* `configs/presets/uxfd/operators/default_1d.yaml` (基础 1D 流)
* `configs/presets/uxfd/operators/learnable_wavelet.yaml` (对应 Paper TON)
* `configs/presets/uxfd/operators/fusion_attention.yaml` (对应 Paper TIFN)


* **T3: 瘦身 Demo Configs**
* 重构 `configs/demo/uxfd/` 下的文件，移除大段 `model` 定义，改为引用上述 preset。
* **验证**: 运行 `python main.py --config configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml`，确保结果与重构前一致（Bit-exact verification 如果可能，或者至少结构一致）。


* **T4: Paper Submodules 注入**
* 利用 `File Fetcher` 无法直接 push 到 submodule 的限制，策略改为：
* 先在父仓库 `configs/presets/uxfd/papers/` 下建立 7 个 paper 的 preset。
* 在 submodule 的 `min.yaml` 中使用 **相对路径** (`../../../../../configs/presets/...`) 引用父仓库的 preset。
* *Benefit*: 这样父仓库可以统一管理所有 paper 的算子配置，submodule 只保留入口。





#### Phase 3: Tooling & Documentation (T5 - T6)

* **T5: 增强 `config_inspect**`
* 实现 `python -m scripts.config_inspect --resolve --config ...`，输出最终合并后的配置树。


* **T6: 自动生成目录与 SSOT**
* 更新 `src/model_factory/X_model/UXFD/FACT_TABLE.md`，自动扫描 `configs/presets/` 生成表格。



---

### 3. Agent Execution Prompt (Phase 1 Focus)

这是给 Agent 的第一阶段指令，专注于代码改造和基础目录建设。

```markdown
**Role**: Core Infrastructure Engineer
**Language**: Chinese
**Goal**: 改造配置加载系统，支持基于 List 的配置组合 (Composition)，并建立 UXFD Preset 目录结构。

**Context**:
当前 `config_utils.load_config` 仅支持单继承 (`base_configs` 为字符串)。我们需要支持多重组合 (`base_configs` 为列表)，以便将 UXFD 的算子配置从主实验配置中解耦。

**Task 1: 代码改造 (src/configs/config_utils.py)**
1.  读取 `src/configs/config_utils.py`。
2.  修改加载逻辑：
    -   如果 `config['base_configs']` 是 list，则按顺序遍历。
    -   创建一个空的 `base_config` 字典。
    -   循环中：`current_base = load_config(path); base_config = recursive_merge(base_config, current_base)`。
    -   最后将当前 config merge 到 `base_config` 上。
    -   *注意*: 保持对 str 类型的兼容（视为单元素 list）。
3.  **约束**: 必须确保列表后元素的配置覆盖前元素，且当前文件的配置优先级最高。

**Task 2: 单元测试 (test/test_config_composition.py)**
1.  创建一个新的测试文件。
2.  构造 3 个临时 YAML：
    -   `base_A.yaml`: `{a: 1, b: 2}`
    -   `base_B.yaml`: `{b: 3, c: 4}`
    -   `main.yaml`: `{base_configs: [base_A.yaml, base_B.yaml], c: 5, d: 6}`
3.  断言加载 `main.yaml` 后的结果为 `{a: 1, b: 3, c: 5, d: 6}` (验证 merge 顺序和覆盖逻辑)。
4.  运行测试确保护航。

**Task 3: 建立 Preset 目录**
1.  创建目录 `configs/presets/uxfd/operators/`。
2.  创建 `configs/presets/uxfd/operators/README.md`，写入以下规范：
    -   **Scope**: 仅存放 `model` 相关配置 (UXFD 算子、特征提取器)。
    -   **Forbidden**: 禁止包含 `data`, `trainer`, `environment` 顶级字段。
    -   **Naming**: 建议使用 `op_<name>.yaml` 或 `paper_<name>.yaml`。

**Output**:
- 显示修改后的 `config_utils.py` diff。
- 显示测试通过的日志。
- 确认目录创建成功。

```

### 优化计划：解耦 UXFD 的算子/装配配置

#### **目标与现状问题总结**

* 现有问题是 UXFD 的“算子配置”直接嵌入在主实验 YAML 配置中，导致配置的可读性差，且不利于智能体进行试错。
* 需要通过解耦来优化，使得 **UXFD 配置文件** 仅包含 **数据、环境、任务、训练** 相关信息，而算子的选择通过单独的 **preset** 文件完成。

#### **核心设计思路**

* **利用现有的 `base_configs` 机制**，实现 YAML 配置叠加，并通过 **递归合并**使得不同配置可以叠加在一起，简化主配置文件的结构。
* **算子预设（preset）** 文件将仅包括与模型算子相关的字段，这样主配置文件的可读性大大提升，同时保持灵活性。

### **方案细节与步骤**

#### **P0 (必须先做，打通机制)**

##### **P0-0 代码改造：`base_configs.<block>` 支持 list[str]**

* 需要修改 `load_config()`，使得支持 `base_configs` 中的块按顺序叠加多个 YAML 配置。

  * **目标**：`base_configs` 中的 **model** 和其它字段可以用 list 列表的方式引入多个配置文件，并递归合并内容。
  * **验证**：使用 `python -m scripts.validate_configs` 来验证是否能正确加载和合并。

##### **P0-1 目录与命名：建立 preset 目录**

* **创建目录结构**：在 `configs/presets/uxfd/operators/` 下建立文件夹，用于存放 UXFD 相关的 preset 配置文件。

  * **Preset 文件格式**：每个文件只包含与 **signal_processing**、**feature_extractor**、**fusion** 等相关的字段。
  * **示例格式**：

    ```yaml
    model:
      signal_processing_configs:
        - "I"
        - "FFT"
      feature_extractor_configs:
        - "Mean"
        - "Std"
      uxfd:
        enable_sp2d: true
        sp2d:
          n_fft: 128
          hop_length: 64
    ```

##### **P0-2 产出 3 个 demo preset**

* 创建 3 个基础的 **UXFD demo preset** 文件，以便后续加载：

  * `uxfd_demo_min.yaml`: 最小化配置，仅包含信号处理和特征提取。
  * `uxfd_demo_sp2d.yaml`: 包含 **SP2D** 以及特征融合配置。
  * `uxfd_demo_full.yaml`: 完整配置，包含 **SP2D** + **Fusion** + **Operator-Attention** + **Logic**。

##### **P0-3 demo configs 变薄（仅选择 preset）**

* 将现有的 **`configs/demo/uxfd/00_smoke_tspn_uxfd.yaml`** 和其他类似的 YAML 配置文件**变薄**，只保留与 **preset** 和少量 override 参数相关的配置：

  * **目标**：通过引用 `base_configs` 和 preset，减少主配置文件中的冗余内容。

#### **P1 (paper 对齐：7 个模块装配进核心模型)**

##### **P1-0 为 7 个 paper 各生成一个 preset**

* 对于每个论文模块（例如 **TON**、**DEN**、**TIFN** 等），生成一个相应的 preset 文件，存放在 `configs/presets/uxfd/operators/` 下。

  * **目标**：每个 preset 文件只包含特定论文所需要的算子配置（例如小波、SP2D、融合层等），以避免与数据/任务等模块的混合。

##### **P1-1 更新 7 个 submodule 的 `min.yaml` 引用 preset**

* 在 **7 个子模块**（如 `paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml`）中引用这些 **preset 文件**，并且测试每个子模块的配置是否能正常运行。

  * **验证**：使用 `python main.py --config paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml --override trainer.num_epochs=1` 测试是否能够正确运行。

#### **P2 (LLM 试错/自动化配置搜索)**

##### **P2-0 更新 LLM 合约：优先输出 `preset_id` + 白名单 overrides**

* 为 **LLM 合约**设置 **preset_id** 作为输入项，并允许 LLM 根据问题描述选择合适的 preset（如：“我有多源数据” -> 选择 TIFN 配置）。

  * **目标**：让 LLM 输出 `preset_id`，并根据用户需求生成少量的 `overrides`。

##### **P2-1 在 `LLM_Explainable_FD_Toolkit` / fallback orchestrator 实现**

* 在 LLM 工具链中实现：根据任务描述和 preset 候选集选择配置并自动执行，不生成 Python 代码。

  * **验证**：使得 LLM 能够通过 **trial loop** 生成配置并产出结果。

---

### **执行计划详细步骤：**

1. **P0-0** 代码改造：

   * 修改 `src/configs/config_utils.load_config()` 支持 **list[str]** 叠加多个 YAML 文件。
   * 验证：`python -m scripts.validate_configs` 是否通过。

2. **P0-1** 目录与命名：

   * 在 `configs/presets/uxfd/operators/` 下创建目录并定义 **preset 文件格式**。

3. **P0-2** 产出 3 个 demo preset：

   * 创建 **最小配置**、**SP2D 配置**、**完整配置**的 YAML 文件。

4. **P0-3** demo configs 变薄：

   * 现有的 demo 配置文件（如 `10_smoke_tspn_uxfd.yaml`）修改为引用 **preset**。

5. **P1-0** 为 7 个 paper 各生成一个 preset：

   * 为每个子模块生成一个对应的 preset 文件，存放在 `configs/presets/uxfd/operators/`。

6. **P1-1** 更新 7 个 submodule 的 `min.yaml` 引用 preset：

   * 修改 `paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml` 文件，确保其引用对应的 preset。

7. **P2-0** 更新 LLM 合约：优先输出 `preset_id`：

   * 更新 LLM 合约，使其根据任务描述选择合适的 preset 文件。

8. **P2-1** 在 LLM 工具链实现：

   * 在 `LLM_Explainable_FD_Toolkit` / fallback orchestrator 中实现自动选择 preset 和生成配置。

---

### **完成标志 (DoD)**：

* `base_configs.model` 支持 **list 叠加**，并且 `python -m scripts.validate_configs` 通过。
* `configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml` 变薄后能正常运行，并生成 **manifest.json**。
* 至少 1 个 **paper submodule** 的 `min.yaml` 能成功引用 preset 并通过测试。

---

### **风险与注意事项**：

* **preset 叠加顺序**：后面的 fragment 会覆盖前面的同名字段，因此需要确保顺序正确。
* **submodule 变更**：每个 submodule 需要单独提交变更，确保不会影响主仓库的其他部分。

这个计划的核心目标是优化配置的结构，让用户可以通过更简洁的 YAML 文件来运行 **UXFD 实验**，并能够通过 **LLM** 自动选择和配置适当的 preset。
