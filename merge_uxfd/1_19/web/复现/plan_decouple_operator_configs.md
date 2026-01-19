# Plan: decouple-uxfd-operator-configs

## Goal
- 让 UXFD 的“模型算子/装配配置”从主实验 YAML 中解耦出来：主 config 只负责 environment/data/task/trainer + 选择一个“UXFD 算子 preset”，并可用少量 override 做试错。
- 让 7 个 paper 模块都能复用 **同一个核心模型**（`model.type: X_model` + `model.name: TSPN_UXFD`），差异只来自“算子 preset + 少量开关”。

## Why (现状问题)
- 当前 UXFD 的关键差异分散在多个 YAML 的 `model.*` 子树里（`signal_processing_configs` / `feature_extractor_configs` / `model.uxfd.*`），主 config 既要写实验编排又要写“算子编排”，可读性差且不利于 LLM 做安全试错。
- `paper/LQ_vibench_fix/merge_uxfd/1_19/web/复现/g.md` 中提到的 `_base_` 继承方式不是本仓库的配置机制；本仓库已维护的组合机制是 `base_configs`（见 `src/configs/config_utils.py`）。

## Design (推荐方案：不改模型，只改配置加载器)

### 核心思路
- 复用现有 `base_configs` 的“多 YAML 叠加 + 递归 merge”能力（`ConfigWrapper.update()` 是递归合并）。
- 扩展 `src/configs/config_utils.load_config()`：允许 `base_configs.<block>` 的值为 **list[str]**，按顺序叠加多个 YAML fragment。

### 约定（UXFD preset 文件格式）
新增目录（建议）：
- `configs/presets/uxfd/operators/`

每个 preset YAML 只包含与模型算子相关的字段（避免污染其它 block）：
```yaml
model:
  signal_processing_configs:
    layer1: ["I", "FFT"]
  feature_extractor_configs: ["Mean", "Std"]
  uxfd:
    enable_sp2d: true
    sp2d:
      n_fft: 128
      hop_length: 64
    fusion:
      type: "gated"
```

主实验 YAML 通过 list 叠加 base model + preset：
```yaml
base_configs:
  model:
    - "configs/base/model/tspn_uxfd.yaml"
    - "configs/presets/uxfd/operators/uxfd_demo_sp2d.yaml"
```

### 可选增强（后续）
- 给 preset 加 `id` / `description` / `version` 元数据（不参与模型构建，仅用于工具链）。
- 为 LLM 工具链提供 “preset id → preset path” 映射表（白名单）。

## Scope
- In:
  - `base_configs` 支持 list 叠加（先从 `model` block 开始；最好对所有 block 通用）。
  - 新增/沉淀 UXFD preset YAML（demo + 7 papers）。
  - 更新 demo configs / paper min.yaml 引用 preset。
  - 更新 UXFD SSOT（`src/model_factory/X_model/UXFD/FACT_TABLE.md`）说明 preset 机制。
- Out (本阶段不做):
  - 不引入新的 YAML 继承语法（如 `_base_`），避免自造生态。
  - 不修改 `TSPN_UXFD` 的装配逻辑（仅让配置更清晰）。

## Tasks (high-level)
- T0: 设计与落盘目录/命名规范（preset 文件格式、命名、versioning）。
- T1: 扩展 `src/configs/config_utils.load_config()`：`base_configs` 支持 list[str]。
- T2: 新增 `configs/presets/uxfd/operators/` 下的 demo preset（min / sp2d / full）。
- T3: 将 `configs/demo/uxfd/*.yaml` 改为使用 preset（主 YAML 变薄）。
- T4: 为 7 个 paper submodule 各生成一个 preset，并将各自 `paper/UXFD_paper/<paper>/configs/vibench/min.yaml` 改为引用 preset（submodule 需要人工提交）。
- T5: 更新 SSOT：`src/model_factory/X_model/UXFD/FACT_TABLE.md` / `src/model_factory/X_model/UXFD/README.md` 补充“preset 机制 + 示例”。
- T6: 更新 LLM 合约（如 `llm_tool_contract.json`）：优先让 LLM 输出 `preset_id` + 少量 `overrides`（白名单字段）。

## DoD (完成判定)
- `base_configs.model` 支持 list 叠加，且 `python -m scripts.validate_configs` 通过。
- `configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml` 变薄后仍可跑通，并产出 `<run_dir>/artifacts/manifest.json`。
- 至少 1 个 paper submodule 的 `min.yaml` 成功改为引用 preset 并可跑通（其余可批量推进）。

## Gates (建议门禁)
- `python -m scripts.validate_configs`
- `python -m scripts.validate_docs`
- `python -m pytest test/test_tspn_uxfd_assembly.py test/test_run_artifacts_contract.py -q`
- `python main.py --config configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml --override trainer.num_epochs=1`

## Risks / Notes
- preset 叠加顺序是 contract：后面的 fragment 覆盖前面的同名字段（递归 merge）。
- paper submodule 变更需要在各 submodule 内单独提交（本环境 `.git/` 可能只读）。
