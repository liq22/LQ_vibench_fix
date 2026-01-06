# UXFD 合并文档索引

## 文档结构
- `12_18temp/`: 最初规划文档（历史存档）
- `12_21/`: 最终实施文档（当前版本）
- `12_22/`: 本次实现产物整理 + 失败分析报告
- `12_23/`: 信号处理/特征提取/逻辑推理算子库补全计划（待确认后实施）
- `12_27/`: 未完成工作/决策点/下一步顺序
- `1_6/`: 2026-01-06 的 codex 整理（intake/daily/todo）

## 快速导航

### 🎯 核心文档
- **[最终计划](12_18temp/codex/final_plan.md)**: UXFD 合并的完整决策文档
- **[逐步操作](12_21/codex/step_by_step_ops.md)**: 可执行的详细步骤
- **[配置规范](12_21/codex/submodule_config_conventions.md)**: submodule 配置文件规范
- **[本次落地整理](12_22/README.md)**: 脚本/产物样例/失败分析（2025-12-22）
- **[Final Plan 复盘+TODO](12_22/status_review_and_todos.md)**: 对照 final plan 的完成度与剩余任务
- **[算子库补全计划](12_23/ops_library_completion_plan.md)**: 12/23 待确认的实现计划（确认后再改代码）
- **[未完成工作整理（handoff）](12_27/README.md)**: 12/27 集中整理的未完成事项/下一步顺序/决策点
- **[1_6 日更与待办](1_6/codex/daily/daily.md)**: 2026-01-06 的整理入口（含 next）
- **[分支差异分析](#分支差异分析)**: lq_merge_UXFD vs origin/main (2026-01-06)

### 📋 技术文档
- [模型对齐方案](12_21/codex/model_alignment_plan.md): TSPN_UXFD 设计
- [对比模型集成](12_21/codex/model_collection_integration_plan.md): 基线模型移植
- [Manifest 规范](12_21/codex/manifest_to_csv_spec.md): 证据链索引格式

### 📝 模板
- [VIBENCH 映射模板](12_21/codex/VIBENCH_MAPPING_TEMPLATE.md): 每篇 paper 的使用指南

## 执行顺序
1. 阅读 `final_plan.md` 了解整体方案
2. 按照 `step_by_step_ops.md` 执行具体步骤
3. 参考各技术文档进行专项实施

## 文件说明

### 12_18temp/codex/
- `init_plan.md`: 最初的规划草案，已标记为收敛版本
- `final_plan.md`: 最终的完整执行计划（SSOT）

### 12_21/codex/
- `step_by_step_ops.md`: 详细的逐步操作指南，本科生可照做
- `submodule_config_conventions.md`: submodule 内配置文件的写作规范
- `model_alignment_plan.md`: 如何保持与上游模型的范式一致
- `model_collection_integration_plan.md`: 对比基线模型的集成方案
- `manifest_to_csv_spec.md`: manifest.json 转换为 CSV 的规范
- `VIBENCH_MAPPING_TEMPLATE.md`: 每篇 paper 的 VIBENCH.md 模板

### 12_22/
- `scripts_and_outputs.md`: 本次新增脚本/产物清单（以及如何复现）
- `failures_report.md`: `pytest test/` 失败与问题分析（含修复建议）
- `results/`: 一次 smoke run 的“证据链闭环”样例（小文件，可直接打开）

## 7 篇 Paper 列表
1. `paper/UXFD_paper/1D-2D_fusion_explainable` - 1D-2D 融合可解释
2. `paper/UXFD_paper/Explainable_FD_Toolkit` - 可解释故障诊断工具包
3. `paper/UXFD_paper/LLM_Explainable_FD_Toolkit` - LLM 增强的可解释工具包
4. `paper/UXFD_paper/MOE_explainable` - MoE 可解释方法
5. `paper/UXFD_paper/Paper_fuzzy_XFD` - 模糊逻辑可解释方法
6. `paper/UXFD_paper/Neuralsymbolic_theory` - 神经符号理论
7. `paper/UXFD_paper/TII_operator_attention` - 算子注意力机制

## 联系方式
如有疑问，请参考各文档中的详细说明或查看项目主 README。

---

## 分支差异分析

**更新时间**: 2025-12-27 ~ 2026-01-06

**对比分支**: `lq_merge_UXFD` vs `origin/main`

### 概览

| 项目 | 值 |
|------|-----|
| 当前分支 | `lq_merge_UXFD` |
| 对比分支 | `origin/main` |
| 共同祖先 | `bcf6c66` (origin/main 的 HEAD) |
| 领先提交数 | 38 个提交 |
| 文件变更 | 138 files changed, 8611 insertions(+), 3180 deletions(-) |

### 分支关系图

```
origin/main (bcf6c66)
    │
    └── lq_merge_UXFD (38 commits ahead)
         ├── UXFD 合并相关 (ad25d09 ~ 53d2141) - 2025-12-22
         ├── lqfix_25-12 合并 (6350b29 ~ 911ce6d) - 2025-12-25
         └── gitlink 修复 (31044e8) - 2026-01-06
```

### 主要变更类别

#### 1. 新增模块 (核心功能)

| 模块 | 路径 | 说明 |
|------|------|------|
| explain_factory | `src/explain_factory/` | 可解释性工厂（GradCAM、条件判断、元数据读取） |
| Pipeline_05 | `src/Pipeline_05_default_w_explain.py` | 带可解释性的默认管道 |
| UXFD 组件 | `src/model_factory/X_model/UXFD/` | 信号处理1D/2D、融合、模糊逻辑、算子注意力 |
| UXFD 基线 | `src/model_factory/X_model/baselines/` | ExplainableCNN 等基线模型 |

#### 2. 新增子模块 (8个 UXFD paper + 1个 LQ)

| 子模块 | 说明 |
|--------|------|
| 1D-2D_fusion_explainable | 1D-2D 融合可解释 |
| Explainable_FD_Toolkit | 可解释故障诊断工具包 |
| LLM_Explainable_FD_Toolkit | LLM 增强的可解释工具包 |
| MOE_explainable | MoE 可解释方法 |
| Paper_fuzzy_XFD | 模糊逻辑可解释方法 |
| Neuralsymbolic_theory | 神经符号理论 |
| TII_operator_attention | 算子注意力机制 |
| LQ_vibench_fix | LQ 修复子模块 |

#### 3. 新增脚本

| 文件 | 用途 |
|------|------|
| `scripts/collect_uxfd_runs.py` | UXFD 运行结果收集 |
| `scripts/uxfd_postrun.py` | UXFD 运行后处理 |

#### 4. 删除的测试文件 (8个)

- `test/test_batch_metadata_processing.py`
- `test/test_end_to_end_integration.py`
- `test/test_multi_task_integration_comprehensive.py`
- `test/test_multi_task_phm_comprehensive.py`
- `test/test_multi_task_rul_validation.py`
- `test/test_parameter_consistency.py`
- `test/test_regression_backward_compatibility.py`
- `test/test_task_specific_metrics.py`

> **注意**: 这些测试文件被删除可能影响测试覆盖率，需确认是否有替代测试。

#### 5. 新增配置/工具

- `.codex/skills/` - Claude Code 技能定义
- `.claude/commands/` - Claude 命令定义
- `.vscode/settings.json` - AI 工具集成设置
- `GEMINI.md` - Gemini 配置文档
- `CONTRIBUTING_CN.md` - 中文贡献指南

### 风险提示

1. **测试覆盖率下降**: 8个测试文件被删除
2. **子模块依赖**: 新增9个子模块需正确初始化
3. **文档分叉**: 大量规划文档需维护和更新
4. **合并复杂度**: 包含来自 lqfix_25-12 分支的合并

### 后续操作建议

1. 运行 `pytest test/` 确认剩余测试通过
2. 执行 `git submodule update --init --recursive` 初始化子模块
3. 确认规划文档与实现状态一致
4. 评估是否将 UXFD 功能合并到主分支
