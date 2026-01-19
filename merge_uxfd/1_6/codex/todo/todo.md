# Todo 1_6

## Top
- [ ] 拍板关键决策点：`paper/LQ_vibench_fix/merge_uxfd/12_27/codex/DECISIONS_NEEDED.md`
- [ ] 确认 pilot paper（默认建议：`paper/UXFD_paper/1D-2D_fusion_explainable`）
- [ ] 在 pilot submodule 内新增并补全 `configs/vibench/min.yaml` 与 `VIBENCH.md`
- [ ] 跑通 1 epoch 并确认 `<run_dir>/artifacts/manifest.json` 存在：`python main.py --config paper/UXFD_paper/<pilot>/configs/vibench/min.yaml --override trainer.num_epochs=1`
- [ ] 记录并可视化 resolved config（便于排查字段来源）：`python -m scripts.config_inspect --config paper/UXFD_paper/<pilot>/configs/vibench/min.yaml --override trainer.num_epochs=1`
- [ ] 校验配置 schema（避免后续 config 进 CI 才报错）：`python -m scripts.validate_configs`
- [ ] 跑 post-run 检查（不改训练流程）：`python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml`
- [ ] 汇总 runs（manifest → CSV）：`python -m scripts.collect_uxfd_runs --input <output_root> --out_dir reports/`
- [ ] 启动 WP1（Copy+Adapter）：优先移植 `Signal_processing_2D.py` 与 `Fusion1D2D*.py`（按 pilot 真实依赖裁剪）
- [ ] 增强 `TSPN_UXFD` 工程壳（HookStore/layout adapters/registry 入口，且默认不改变行为）
- [ ] 接入至少 1 个 explainer 的实际执行，产出 `artifacts/explain/summary.json` 并写回 manifest（best-effort）
- [ ] 给 `scripts/collect_uxfd_runs.py` 增加最小单测（构造假的 `run/artifacts/manifest.json`，断言 CSV 列/值）

## Notes
- 未完成 SSOT：`paper/LQ_vibench_fix/merge_uxfd/12_27/codex/UNFINISHED_WORK.md`
- 执行细化：`paper/LQ_vibench_fix/merge_uxfd/12_23/TODO_BACKLOG.md`、`paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md`
