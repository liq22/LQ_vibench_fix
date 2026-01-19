# UXFD Merge：现状 + TODO（SSOT）

更新时间：2026-01-15

## 30 秒验收检查

当前 UXFD 合并是否“最小闭环”完成：

- [x] smoke 可跑：`python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`
- [x] collect 可用：`python -m scripts.collect_uxfd_runs --input results --out_dir reports`（输出：`reports/uxfd_runs.csv`）
- [x] post-run 可用：`python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml`
- [x] 至少 1 个 pilot 完成：`1D-2D_fusion_explainable` 的 `min.yaml` 已跑通 1 epoch
- [x] 主仓库 tests 通过：`python -m pytest test/`
- [x] 核心模型口径就绪：P0-2 的口径要求满足（paper configs 统一走 `TSPN_UXFD`）
  - 已实现（best-effort）：`TSPN_UXFD` orchestrator（`src/model_factory/X_model/TSPN_UXFD.py`）
    - `model.uxfd.enable_sp2d=true`：启用 2D STFT 分支（`src/model_factory/X_model/UXFD/signal_processing_2d/`）
    - `model.uxfd.fusion.type=concat|sum|gated`：1D/2D 特征融合（`src/model_factory/X_model/UXFD/fusion/`）
    - `model.uxfd.fuzzy.enable=true` + `model.uxfd.fuzzy.logit_scale`：fuzzy logits residual（`src/model_factory/X_model/UXFD/fuzzy/`）
    - `model.uxfd.operator_attention.enable=true`：operator-attention 预处理（`src/model_factory/X_model/UXFD/operator_attention/`）
    - `model.uxfd.logic.enable=true`：logic logits residual（`src/model_factory/X_model/UXFD/neurosymbolic/`）
  - 已实现（best-effort）：`trainer.extensions.predictions.enable=true` → `artifacts/predictions.npz`（用于 post-run 绘图）
  - 已实现（best-effort）：`trainer.extensions.agent.enable=true` → `artifacts/distilled/summary.json`（LLM-free）

## 证据（可复现验证命令）

> 目的：避免文档里出现“已完成但不可验证”的 [x]。
>
> 最近一次完整验证：2026-01-16（本机离线环境）。

核心路径存在性（示例）：

```bash
test -f src/model_factory/X_model/TSPN_UXFD.py
test -d src/model_factory/X_model/UXFD/fusion
test -d src/model_factory/X_model/UXFD/fuzzy
test -d src/model_factory/X_model/UXFD/operator_attention
test -d src/model_factory/X_model/UXFD/neurosymbolic
test -f scripts/collect_uxfd_runs.py
```

7 个 paper 入口文件存在性（注意：submodule 内部文件需要在 submodule repo 内提交）：

```bash
find paper/UXFD_paper -path "*/configs/vibench/min.yaml" | wc -l  # 期望：7
find paper/UXFD_paper -maxdepth 2 -name "VIBENCH.md" | wc -l      # 期望：7
```

至少 1 个 pilot 可跑（示例）：

```bash
python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1
```

## 目标口径（强约束）

1) **单一入口**：`python main.py --config <yaml> [--override key=value ...]`
2) **一个核心模型**：所有 paper configs 统一使用 `model.type: X_model` + `model.name: TSPN_UXFD`
3) **可装配模块**：7 篇 paper 的差异通过“核心模型的模块装配 + 配置”表达
4) **主仓库离线自洽**：主仓库 demos/tests 不依赖任何 paper submodule 初始化

## 当前现状（What works now）

- 主仓库 smoke 可跑（dummy demo），且会写出 `artifacts/manifest.json` 等证据链文件（best-effort）。
- `scripts/collect_uxfd_runs.py` 可扫描 `<root>/**/artifacts/manifest.json` 并导出 `reports/uxfd_runs.csv`。
  - 说明：脚本的 `--input` 默认值可能与本仓库实际输出目录不一致；本仓库 demos/pilots 默认写到 `results/`，建议显式传参
    `--input results`（不要依赖隐式默认值）。
- `paper/UXFD_paper/*` submodules 已补齐 vibench 入口文件：`configs/vibench/min.yaml` + `VIBENCH.md`。
- `TSPN_UXFD` 已支持可装配插槽：SP2D/Fusion/Fuzzy/OperatorAttention/Logic（best-effort）。
- `.gitignore` 已允许跟踪 `test/**/*.py`，collect 工具的最小单测可纳入回归。

## submodule 提交注意事项（重要）

本目录里列出的 7 篇 paper 都是 git submodule：

- 如果你在父仓库的 PR diff 里看不到 `paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml` 等文件：这是正常的。
- 需要在每个 submodule 仓库内分别提交文件改动，然后父仓库只更新 gitlink 指针。

## Paper 入口文件状态（WP0）

> 结论：当前工作区中，7 个 submodule 已补齐 `configs/vibench/min.yaml` 与 `VIBENCH.md`。
> 注意：这些文件属于 submodule 仓库，必须在各自 submodule 内提交；父仓库 diff 只能看到 gitlink/dirty 状态。

| paper_id | `configs/vibench/min.yaml` | `VIBENCH.md` | 优先级 | 预计工时 |
|---|---|---|---|---|
| `1D-2D_fusion_explainable` | 已创建 | 已创建 | P0（Pilot） | 2–3h |
| `Explainable_FD_Toolkit` | 已创建 | 已创建 | P0 | 2–3h |
| `LLM_Explainable_FD_Toolkit` | 已创建 | 已创建 | P1 | 2–4h |
| `MOE_explainable` | 已创建 | 已创建 | P1 | 2–4h |
| `Paper_fuzzy_XFD` | 已创建 | 已创建 | P1 | 2–4h |
| `Neuralsymbolic_theory` | 已创建 | 已创建 | P1 | 2–4h |
| `TII_operator_attention` | 已创建 | 已创建 | P1 | 2–4h |

## P0 阻塞（先解锁“真实验证闭环”）

### P0-1：补齐 paper submodule 的入口文件（WP0，已完成）

在 `paper/UXFD_paper/<paper_id>/` 内落地：

- `configs/vibench/min.yaml`（最小可跑；建议 1 epoch）
- `VIBENCH.md`（该 paper 如何用 vibench 复现的唯一入口说明）

建议按步骤执行（避免遗漏）：

1) 创建目录结构：`paper/UXFD_paper/<paper_id>/configs/vibench/`
2) 编写 `configs/vibench/min.yaml`（5-block；默认不依赖 submodule 额外代码）
3) 编写 `VIBENCH.md`（一键命令 + metadata 要求 + 产物规范 + 常见坑）
4) 跑 DoD 命令，确认产物闭环可收集

DoD（已通过）：

- `python main.py --config paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml --override trainer.num_epochs=1` 可跑通

参考模板/规范：

- `paper/LQ_vibench_fix/merge_uxfd/12_21/codex/VIBENCH_MAPPING_TEMPLATE.md`
- `paper/LQ_vibench_fix/merge_uxfd/12_21/codex/submodule_config_conventions.md`

### P0-2：核心模型装配口径落地（Core Model Contract）

口径要求：

- paper configs 不再各自定义“入口模型名”，统一走 `TSPN_UXFD`
- paper 差异通过 `model.*` 配置选择要装配的模块（SP2D/Fusion/Fuzzy/Attention 等）

计划文档：

- `paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md`

## P0 阻塞依赖图

```
            ┌─────────────────┐
            │   P0-1: WP0     │
            │ (Pilot 入口)    │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │   P0-2: 核心模型  │
            │   装配口径落地    │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │  P1: 算子库补齐   │
            └─────────────────┘
```

## P1（核心能力）：算子库补齐 + 装配实现

### P1-1：补齐 `src/model_factory/X_model/UXFD/**` 的可复用模块

目标：

- 能支撑至少一个 paper 的最小 config 跑通（不追求一次性重构）
- 迁移策略：Copy + Adapter（先跑通，再收敛）

### P1-2：把 `TSPN_UXFD` 从 alias 升级为 orchestrator

目标：

- 默认行为不变（与 `TSPN.py` 一致）
- 当配置启用模块时，装配对应 `UXFD/**` 组件并完成前向

## P2（保持推进）：plot/post-run（不弃用）

计划文档（继续维护）：

- `paper/LQ_vibench_fix/merge_uxfd/12_23/plot_factory_migration_plan.md`

落地建议：

- 优先离线脚本（基于 `manifest.json`/`metrics.csv`），避免耦合训练/模型内部

## 归档口径（避免文档分裂）

- 各日期目录（`12_18temp/`, `12_21/`, `12_22/`, `12_27/`, `1_6/`, `1_7/`）以“历史参考”为主。
- TODO/现状只在本文件维护；其他文件如仍出现 TODO，应改为链接指向本文件。
