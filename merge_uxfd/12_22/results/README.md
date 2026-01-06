# 结果样例（smoke run）

本目录保存一次 `dummy_dg` smoke run 的“小文件样例”，用于展示证据链闭环：

- `config_snapshot_smoke.yaml`: 该次 run 的最终配置快照
- `manifest_smoke_test.json`: 该次 run 的 `manifest.json`（stage=test）
- `test_result_smoke.csv`: 测试指标 CSV
- `uxfd_runs_smoke.csv`: 使用 `collect_uxfd_runs.py` 汇总得到的 runs 表（CSV）

注意：
- 这些只是样例文件（便于快速打开查看字段），不是长期存储全部实验结果的地方。
- 真正的 run 目录仍在 `results/` 或你配置的 `environment.output_dir` 下。

