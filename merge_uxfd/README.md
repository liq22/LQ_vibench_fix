# UXFD 合并文档（PHM-Vibench）

本目录是 UXFD 上游合并到 PHM‑Vibench 的“入口索引页”（面向新人/交接）。主仓库仍以单一入口运行：
`python main.py --config <yaml> [--override key=value ...]`。

---

## 30 秒理解 UXFD 合并现状

- **目标**：将 UXFD 上游能力并入 PHM‑Vibench（config-first）
- **核心模型**：`TSPN_UXFD`（建议所有 paper configs 统一使用）
- **当前状态**：主仓库 smoke 可跑；7 个 paper submodules 已补齐最小入口（`configs/vibench/min.yaml` + `VIBENCH.md`）
- **下一步**：继续把 paper 差异收敛为 `TSPN_UXFD` 的可装配插槽（按 `model.uxfd.*` 配置启用）

---

## 优先级概览

```
P0（已完成）: WP0 入口文件 + 核心模型装配口径
   ↓
P1（核心）: 提升上游一致性（算子库/实现细节）
   ↓
P2（推进）: plot/post-run（不阻塞）
```

---

## 🚀 新人从这里开始（建议顺序）

**只读这 2–3 个文件（30 分钟上手）**：

1. **[00_quickstart.md](00_quickstart.md)**：复制粘贴命令，跑通 smoke + 产物检查
2. **[01_porting_playbook.md](01_porting_playbook.md)**：面向实施者的迁移顺序 + DoD
3. （可选）**[12_27/codex/DECISIONS_NEEDED.md](12_27/codex/DECISIONS_NEEDED.md)**：需要拍板的决策点
4. （实施者）**[1_15/codex/TODO.md](1_15/codex/TODO.md)**：现状 + TODO（SSOT）

---

## ⚠️ 重要现状（避免踩坑）

- 合并口径已收敛：**一个核心模型**（`model.name=TSPN_UXFD`）+ **7 篇 paper 通过配置装配模块**（详见
  [1_15/codex/TODO.md](1_15/codex/TODO.md)、[12_23/ops_lipletion_plan.md](12_23/ops_lipletion_plan.md)（短版）与
  [12_23/ops_library_completion_plan.md](12_23/ops_library_completion_plan.md)（长版）。
- `paper/UXFD_paper/*` submodules 的 vibench 入口文件已补齐：每篇均提供 `configs/vibench/min.yaml` 与 `VIBENCH.md`。
- 目前可用的最小闭环是：跑 `configs/demo/00_smoke/dummy_dg.yaml` → 自动生成 `artifacts/manifest.json`
  → 用 `scripts/collect_uxfd_runs.py` 汇总成 CSV（含 `predictions_path`）。
- 如果你在 review/合并里看不到 submodule 内的文件级 diff：这是正常的。**submodule 的改动需要在 submodule 仓库内提交**，
  父仓库只更新 gitlink 指针。
- submodule 入口约定（后续新增/修订时参考）：参考
  [12_21/codex/VIBENCH_MAPPING_TEMPLATE.md](12_21/codex/VIBENCH_MAPPING_TEMPLATE.md) 与
  [12_21/codex/submodule_config_conventions.md](12_21/codex/submodule_config_conventions.md)（submodule 列表见
  [paper/UXFD_paper/README.md](../../UXFD_paper/README.md)）。

---

## 最小 DoD 清单（当前仓库状态：已满足）

- [x] 预检查命令通过
  ```bash
  python main.py --config configs/demo/00_smoke/dummy_dg.yaml
  python -m scripts.validate_configs
  python -m pytest test/
  ```
- [x] 7 个 paper submodule 均提供可跑入口：`paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml`
- [x] 7 个 `min.yaml` 均可跑 1 epoch（CPU）
- [x] 产物闭环存在：`config_snapshot.yaml`、`artifacts/manifest.json`、`artifacts/data_metadata_snapshot.json`
  - 可选：`artifacts/explain/eligibility.json`（`trainer.extensions.explain.enable=true`）
  - 可选：`artifacts/predictions.npz`（`trainer.extensions.predictions.enable=true`）
  - 可选：`artifacts/distilled/summary.json`（`trainer.extensions.agent.enable=true`，LLM-free）
- [x] `scripts/collect_uxfd_runs.py` 能生成 `reports/uxfd_runs.csv`
- [x] `scripts/uxfd_postrun.py` 可离线检查并绘图（学习曲线/混淆矩阵）

---

## 快速命令（当前仓库“可直接复制运行”）

```bash
# 1) smoke：验证环境+入口（离线可跑）
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1

# 2) 汇总：扫描所有 runs 的 manifest.json → CSV
python -m scripts.collect_uxfd_runs --input results --out_dir reports
ls -la reports/uxfd_runs.csv

# 3) post-run：离线检查 + 绘图（不集成到 main.py）
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml
# （严格门禁版，可用于 CI/回归）：fail_on_missing_required=true
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_strict.yaml
```

```bash
# pilot：任意一个 paper 的最小配置跑 1 个 epoch
python main.py --config paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml --override trainer.num_epochs=1
```

---

## 文档结构（SSOT）

> 只有下表中的文档被视为“维护中”；其余文件/目录默认视为归档（历史参考）。

| 文件 | 用途 | 面向对象 |
|------|------|----------|
| **[00_quickstart.md](00_quickstart.md)** | 1 页复制粘贴指南 | 所有人 |
| **[01_porting_playbook.md](01_porting_playbook.md)** | 迁移映射表 + DoD | 实施者 |
| **[1_15/codex/TODO.md](1_15/codex/TODO.md)** | 现状 + TODO（SSOT） | 实施者 |
| **[12_23/ops_lipletion_plan.md](12_23/ops_lipletion_plan.md)** | 收敛执行清单（短版；兼容历史命名） | 实施者 |
| **[12_23/ops_library_completion_plan.md](12_23/ops_library_completion_plan.md)** | 算子库补齐 + 核心模型装配计划（维护中） | 实施者 |
| **[12_23/plot_factory_migration_plan.md](12_23/plot_factory_migration_plan.md)** | plot/post-run 迁移计划（维护中，不弃用） | 实施者 |
| **[12_27/codex/DECISIONS_NEEDED.md](12_27/codex/DECISIONS_NEEDED.md)** | 待决决策 | 负责人 |
| **[1_7/glm/README.md](1_7/glm/README.md)** | 7 篇 paper 的原子任务分解 | 任务跟踪 |

---

## 归档文档（历史参考）

> ⚠️ 以下文档保留供参考，但已被上面的 SSOT 文档取代：

| 目录 | 说明 | 状态 |
|------|------|------|
| [12_18temp/](12_18temp/) | 初始规划文档 | 归档 |
| [12_21/](12_21/) | 实施细节（模板/规范） | 归档 |
| [12_22/](12_22/) | 本次落地整理 + 失败分析 | 归档 |
| [12_27/](12_27/) | 大部分为历史参考；`12_27/codex/DECISIONS_NEEDED.md` 仍维护 | 部分维护 |
| [1_6/](1_6/) | 日更与待办（2026-01-06） | 归档 |

---

## 7 篇 Paper 列表（submodules）

> 如点击后目录不存在：先执行 `git submodule update --init --recursive`。

| Paper | 说明 | 优先级 |
|-------|------|--------|
| [1D-2D_fusion_explainable](../../UXFD_paper/1D-2D_fusion_explainable) | 1D-2D 融合可解释 | P0 (Pilot) |
| [Explainable_FD_Toolkit](../../UXFD_paper/Explainable_FD_Toolkit) | 可解释故障诊断工具包 | P0 (基础设施) |
| [LLM_Explainable_FD_Toolkit](../../UXFD_paper/LLM_Explainable_FD_Toolkit) | LLM 增强可解释工具包 | P1 |
| [MOE_explainable](../../UXFD_paper/MOE_explainable) | MoE 可解释方法 | P1 |
| [Paper_fuzzy_XFD](../../UXFD_paper/Paper_fuzzy_XFD) | 模糊逻辑可解释 | P1 |
| [Neuralsymbolic_theory](../../UXFD_paper/Neuralsymbolic_theory) | 神经符号理论 | P1 |
| [TII_operator_attention](../../UXFD_paper/TII_operator_attention) | 算子注意力机制 | P1 |

---

## 分支差异（如何自助查看）

这些数字很容易过时，建议用命令实时查看：

```bash
git status
git log --oneline --decorate -n 20
git diff --stat origin/main..HEAD
```
