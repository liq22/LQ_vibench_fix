# 1_17/codex（UXFD：可解释测试 + LLM 优化方案）

本目录用于把“可解释的测试门禁（tests）”与“LLM 试错优化 UXFD 结构（langgraph orchestration）”的 TODO 方案收敛到一处。

- TODO（主文档）：`paper/LQ_vibench_fix/merge_uxfd/1_17/codex/TODO.md`
- Intake（收口输入）：`paper/LQ_vibench_fix/merge_uxfd/1_17/codex/intake/intake_merge_uxfd.md`
- Plans（避免计划分散）：
  - `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/plan/plan_uxfd-components-check.md`
  - `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/plan/plan_merge_uxfd.md`

## Quick Validate（复制粘贴）

```bash
# 1) 主仓库 smoke
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1

# 2) UXFD 相关单测（落地后应保持 green）
python -m pytest test/ -k 'uxfd or artifacts' -q

# 3) 至少 1 个 UXFD-enabled paper min config（WP0）
python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1

# 4) 离线检查（post-run）
# 宽松扫历史 runs（推荐用于开发期）
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml

# （可选）严格门禁（用于 CI/回归；历史 runs 可能因缺少产物而失败）
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml
```
