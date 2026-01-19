# 12_23（算子库补全计划）

本目录用于在开始大规模代码移植前，先把“WP0 submodule(min.yaml) 驱动验证 + WP1 算子库移植（含融合/路由）+ HookStore + 最小单测”写清楚，并让你确认后再动手实现。

**说明（维护状态）**：本目录的两份计划文档仍然维护中：
- `ops_library_completion_plan.md`：算子库补齐 + 核心模型装配（v2.0）
- `plot_factory_migration_plan.md`：plot/post-run 迁移计划（不弃用）

## 核心文档

- 执行计划：`paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md`（算子库补全主计划）
- 收敛执行清单（短版；兼容历史命名）：`paper/LQ_vibench_fix/merge_uxfd/12_23/ops_lipletion_plan.md`
- 历史 TODO 清单：`paper/LQ_vibench_fix/merge_uxfd/12_23/TODO_BACKLOG.md`（已被 SSOT TODO 取代）

## 配套计划（plot/post-run）

- Plot 目录迁移计划：`paper/LQ_vibench_fix/merge_uxfd/12_23/plot_factory_migration_plan.md`（plot/ → offline 工具 + 可选 src/plot_factory）
- Post-run 检查+绘图脚本：`scripts/uxfd_postrun.py`（推荐 `python -m scripts.uxfd_postrun`）
- Post-run 配置示例（宽松扫历史 runs）：`paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml`
- Post-run 配置示例（严格门禁/回归）：`paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_strict.yaml`

## TODO（SSOT）

- 现状与后续 TODO：`paper/LQ_vibench_fix/merge_uxfd/1_15/codex/TODO.md`

## 文件依赖关系（简图）

`paper/LQ_vibench_fix/merge_uxfd/12_23/README.md`
├── `paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md` ←── `paper/LQ_vibench_fix/merge_uxfd/12_23/TODO_BACKLOG.md`
└── `paper/LQ_vibench_fix/merge_uxfd/12_23/plot_factory_migration_plan.md` → `scripts/uxfd_postrun.py` + `uxfd_postrun_config_*.yaml`

说明（命名变更）：
- 本目录中的“UXFD_component”属于当时的重构提案；当前主仓库实际落位仍以 `src/model_factory/X_model/UXFD/` 为准。
- 在没有明确决策前，不要同时维护 `UXFD/` 与 `UXFD_component/` 两套目录，避免重复实现与文档口径分裂。
