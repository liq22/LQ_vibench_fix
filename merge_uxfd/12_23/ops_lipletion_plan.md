# ops_lipletion_plan.md（收敛执行清单｜短版）

> 说明：该文件名为历史拼写（`lipletion`）；保留该路径以兼容既有链接与交接口径。

本文件的定位是 **“短版可执行清单（Ops / Merge Completion）”**：只保留验收口径、执行顺序与关键证据链路径；
具体实现细节与算子迁移细拆请看 `ops_library_completion_plan.md`。

## 单一入口（强约束）

所有训练/验证统一通过：`python main.py --config <yaml> [--override key=value ...]`。

## 核心模型口径（强约束）

- 所有 paper configs 统一使用：`model.type: X_model` + `model.name: TSPN_UXFD`
- paper 差异通过 `model.uxfd.*` 与 `trainer.extensions.*` 装配开关表达（不引入第二套入口模型名）

## 30 秒验收（本仓库最小闭环）

```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
python -m scripts.validate_configs
python -m pytest test/
python -m scripts.collect_uxfd_runs --input results --out_dir reports
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml
```

## 证据链产物（run_dir）

训练完成后应能在 `<run_dir>/` 找到：

- `config_snapshot.yaml`（resolved config）
- `artifacts/manifest.json`（证据索引）
- `artifacts/data_metadata_snapshot.json`（best-effort）

按需启用（由配置开关控制）：

- `artifacts/explain/eligibility.json`（`trainer.extensions.explain.enable=true`）
- `artifacts/predictions.npz`（`trainer.extensions.predictions.enable=true`）
- `artifacts/distilled/summary.json`（`trainer.extensions.agent.enable=true`，LLM-free）

## Paper 子模块（WP0：入口规范）

每个 `paper/UXFD_paper/<paper_id>/` 需要提供：

- `configs/vibench/min.yaml`（最小可跑；建议 1 epoch）
- `VIBENCH.md`（映射/复现说明唯一入口）

验证命令：

```bash
python main.py --config paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml --override trainer.num_epochs=1
```

## 仍维护的详细计划（不要弃用）

- 算子库补齐 + 核心模型装配（长版）：`paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md`
- plot/post-run 迁移计划（长版，不弃用）：`paper/LQ_vibench_fix/merge_uxfd/12_23/plot_factory_migration_plan.md`

## TODO（SSOT）

现状与后续 TODO 只在这里维护：`paper/LQ_vibench_fix/merge_uxfd/1_15/codex/TODO.md`。
