# Daily 1_16

## Summary
确认 7 个 UXFD paper（WP0 入口）在工作区已齐全，并把当天验证命令与证据链整理落盘到 `1_16/codex/`。

## Done
- 验证 7 个 paper submodules 均存在 `configs/vibench/min.yaml` 与 `VIBENCH.md`（工作区存在性 + 计数为 7/7）
- 复跑主仓库验证命令：`python -m scripts.validate_configs`、`python -m pytest test/`、`python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`
- 复跑 UXFD 工具链：`python -m scripts.collect_uxfd_runs --input results --out_dir reports`、`python -m scripts.uxfd_postrun --config ...example.yaml`
- 针对“文档过度承诺/不可验证”问题，补齐 `TODO.md` 的证据与表述口径（best-effort + 可验证命令）

## Evidence
- `paper/LQ_vibench_fix/merge_uxfd/1_16/codex/report/report_uxfd-merge.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_16/codex/artifact/manifest_uxfd-merge.json`
- `paper/LQ_vibench_fix/merge_uxfd/README.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_15/codex/TODO.md`

## Blockers
- 7 个 paper 的入口文件目前在各 submodule 工作区存在，但需要在各自 submodule 仓库内提交后，父仓库 PR 才能展示文件级 diff。
- 历史 runs 可能缺 `config_snapshot.yaml` 等产物（严格门禁 post-run 会失败）；需通过重新跑新 pipeline 或清理策略解决。

## Next
- See: `paper/LQ_vibench_fix/merge_uxfd/1_16/codex/todo/todo.md`
