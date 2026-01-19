# Intake: uxfd-merge

- Goal: 确认 UXFD 合并“最小闭环”已具备，并回答“7 个 paper 目前是否完整”，同时把当天证据链与后续动作收敛到 `1_16/codex/`。
- Scope:
  - 主仓库：核心模型口径（`TSPN_UXFD`）、产物闭环（manifest/predictions/explain/distill）、collect/post-run 工具链。
  - 7 个 paper submodules：仅验证 WP0 入口文件是否齐全（`configs/vibench/min.yaml` + `VIBENCH.md`）。
  - 文档：SSOT（`1_15/codex/TODO.md`）与入口索引（`merge_uxfd/README.md`）保持一致；历史目录仅归档。
- Tasks:
  - T1: 验证 7 个 paper submodules 是否都有 `configs/vibench/min.yaml` 与 `VIBENCH.md`（工作区存在性 + 计数）。
  - T2: 明确“完整”的定义与边界（WP0 完整 vs. 可合并 PR 完整）。
  - T3: 记录可复现证据：configs/tests/collect/post-run 通过的命令与预期输出。
  - T4: 列出 submodule 提交流程（每个 submodule 内提交 → 父仓库更新 gitlink）。
- Priority: P0
- Due: TBD
- Owner: TBD
- Background:
  - 合并目标是保持 config-first：统一入口 `python main.py --config <yaml> [--override ...]`。
  - 7 篇 paper 作为 git submodule 维护其 paper-specific 入口与说明；主仓库只保留可复用通用代码。
- Details:
  - “7 个 paper 完整（WP0）”定义：每个 submodule 目录下存在 `configs/vibench/min.yaml` 与 `VIBENCH.md`，并能通过
    `python main.py --config ... --override trainer.num_epochs=1` 跑 1 epoch（至少 1 个 pilot 已验证）。
  - “可合并 PR 完整”额外要求：上述文件需要在各自 submodule 仓库内提交（否则父仓库 diff 只显示 submodule dirty）。
- Acceptance / DoD:
  - `find paper/UXFD_paper -path "*/configs/vibench/min.yaml" | wc -l` → 7
  - `find paper/UXFD_paper -maxdepth 2 -name "VIBENCH.md" | wc -l` → 7
  - `python -m scripts.validate_configs` → `[OK] ... passed schema validation.`
  - `python -m pytest test/` → 全部通过
  - `python -m scripts.collect_uxfd_runs --input results --out_dir reports` → 生成 `reports/uxfd_runs.csv`
- Notes:
  - submodule 变更必须在 submodule 仓库内提交；父仓库只能更新 gitlink 指针。
  - `scripts.collect_uxfd_runs.py` 的 `--input` 需要显式传参（本仓库默认输出到 `results/`）。
- Evidence:
  - `paper/LQ_vibench_fix/merge_uxfd/1_16/codex/report/report_uxfd-merge.md`
  - `paper/LQ_vibench_fix/merge_uxfd/1_16/codex/artifact/manifest_uxfd-merge.json`

Next: plan-md-writer
