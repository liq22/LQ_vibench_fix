# 12_22（本次实现产物整理）

> ⚠️ **归档（历史参考）**
>
> 本目录用于保留 2025-12-22 的落地整理与样例产物；现状/后续 TODO 请以 SSOT 为准：
> `paper/LQ_vibench_fix/merge_uxfd/1_15/codex/TODO.md`

本目录用于把“本次 UXFD merge 的新增脚本/产物样例/失败问题”集中落盘，避免打扰主仓库 `docs/`。

## 快速导航

- 脚本与产物清单：`paper/LQ_vibench_fix/merge_uxfd/12_22/scripts_and_outputs.md`
- 失败与问题分析：`paper/LQ_vibench_fix/merge_uxfd/12_22/failures_report.md`
- Final plan 执行复盘 + TODO：`paper/LQ_vibench_fix/merge_uxfd/12_22/status_review_and_todos.md`
- 上游项目缺口分析 + 集成计划：`paper/LQ_vibench_fix/merge_uxfd/12_22/upstream_gap_analysis_and_plan.md`
- 证据链样例（小文件）：`paper/LQ_vibench_fix/merge_uxfd/12_22/results/README.md`

## 复现命令（最小闭环）

```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
python -m scripts.collect_uxfd_runs --input results --out_dir reports
```
