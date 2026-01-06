# Intake: merge-uxfd

- Goal: 将 `paper/LQ_vibench_fix/merge_uxfd/12_23` 与 `paper/LQ_vibench_fix/merge_uxfd/12_27` 的规划/待办收口为可执行清单，并推进到“至少 1 篇 pilot 可验证跑通”的状态。
- Scope: 仅覆盖 UXFD merge（WP0–WP5）相关事项；当下优先推进 WP0（pilot min.yaml）与 WP1（Copy+Adapter 组件移植）。
- Tasks:
  - T1: 确认 pilot paper（默认建议：`paper/UXFD_paper/1D-2D_fusion_explainable`）。
  - T2: 在 pilot submodule 内新增并补全 `configs/vibench/min.yaml` 与 `VIBENCH.md`（必要时补 `configs/vibench/README.md`）。
  - T3: 跑通 pilot 最小验证：`python main.py --config paper/UXFD_paper/<pilot>/configs/vibench/min.yaml --override trainer.num_epochs=1`，并确认 `<run_dir>/artifacts/manifest.json` 存在。
  - T4: 使用 post-run 检查：`python scripts/uxfd_postrun.py --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml`，确保对“无 run/有 run”都不崩溃且会写 eligibility。
  - T5: 按 Copy+Adapter（先跑通后优化）补齐 pilot 依赖的通用组件：2D 时频（`Signal_processing_2D.py`）、1D↔2D 融合（`Fusion1D2D*.py`），以及按需的 attention/fuzzy/logic。
  - T6: 增强 `TSPN_UXFD` 的工程壳：HookStore wrapper（不改变 forward 结果）、必要的 layout adapters，并在 `src/model_factory/model_registry.csv` 增加可选 hooked 入口。
  - T7: 接入至少 1 个 explainer 的实际执行，产出 `artifacts/explain/summary.json` 并写回 manifest（best-effort，不阻塞训练）。
  - T8: 给 `scripts/collect_uxfd_runs.py` 增加最小单元测试（构造假的 `run/artifacts/manifest.json`，断言输出 CSV 列/值）。
  - T9: 盘点并逐步移植上游 `model_collection` baselines（torch-only 优先；重依赖保持 optional-import 或不注册）。
- Priority: P0=WP0（pilot min.yaml + 跑通证据链）→ P1=WP1（通用组件移植）→ P1b/WP3（HookStore + explain 执行）→ P2（baselines/report 稳定性）。
- Due: TBD
- Owner: TBD
- Background: 12/23 给出算子库补全与 plot/post-run 方案；12/27 将未完成工作与决策点收敛为 SSOT，强调必须先做 WP0 才能真实验证后续移植。
- Details:
  - 约束：保持单入口 `python main.py --config <yaml> [--override ...]`；保持 5-block（environment/data/model/task/trainer）；不新增第 6 个一级 YAML block（开关放 `trainer.extensions.*`）。
  - 策略：Copy + Adapter（先跑通，不追求一次性重构），并用 post-run/manifest 产物作为稳定接口做离线检查与绘图。
  - 关键输入输出约定：1D=BLC，2D=BTFC；`torch.fft.*` 默认采用 magnitude-only（`abs()`）并在 README 明确。
  - 需尽早确认的决策点：是否引入 `UXFD_component/` 目录命名、pilot 选择、`figures/` 输出落位、是否自动写 `artifacts/predictions.npz`、以及 `.gitignore` 是否会吞掉证据样例目录。
- Acceptance / DoD:
  - 至少 1 篇 pilot submodule 内存在 `configs/vibench/min.yaml` + `VIBENCH.md`，且 `min.yaml` 可跑通 1 epoch。
  - 运行后 `<run_dir>/artifacts/manifest.json` 存在；post-run 脚本可运行并在对应 run 下写出 eligibility（若无 run 也不报错）。
  - 若启用 explain：`<run_dir>/artifacts/explain/summary.json` 存在（best-effort：失败不阻塞训练，但必须可审计记录 skip/reason）。
  - `scripts/collect_uxfd_runs.py` 有最小单测覆盖，并能在 CI/本地稳定运行。
- Notes:
  - 任务细化与依赖见原始材料（以原文为准）：`paper/LQ_vibench_fix/merge_uxfd/12_23/TODO_BACKLOG.md`、`paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md`、`paper/LQ_vibench_fix/merge_uxfd/12_27/codex/UNFINISHED_WORK.md`、`paper/LQ_vibench_fix/merge_uxfd/12_27/codex/DECISIONS_NEEDED.md`。
- Evidence:
  - paper/LQ_vibench_fix/merge_uxfd/1_6/codex/intake/intake_merge-uxfd.md
  - paper/LQ_vibench_fix/merge_uxfd/12_23/TODO_BACKLOG.md
  - paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md
  - paper/LQ_vibench_fix/merge_uxfd/12_27/codex/UNFINISHED_WORK.md
  - paper/LQ_vibench_fix/merge_uxfd/12_27/codex/DECISIONS_NEEDED.md

Next: plan-md-writer
