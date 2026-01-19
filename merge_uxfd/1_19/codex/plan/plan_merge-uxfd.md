# Plan: merge-uxfd (v2)

更新时间：2026-01-19

## Goal
以最小风险完成 UXFD 合并的人工 review + submodule 合并，并建立“可解释=可验证产物”的测试与门禁，使后续 LLM（LangGraph 风格）结构试错优化可在受控边界内运行与回滚。

## Assumptions / Notes
- Submodule 真实文件级 diff 只能在 submodule 仓库内 review/commit；父仓库 PR 只能看到 gitlink 更新。
- 当前环境可能未安装 `langgraph`；必须提供纯 Python fallback loop（后续再迁移到 langgraph）。
- “UXFD 模型 work”的验收必须包含一次 **UXFD-enabled** 的 `paper/.../configs/vibench/min.yaml` 跑通，并满足 `<run_dir>/artifacts/manifest.json` 契约。

## Scope
- In:
  - 父仓库核心实现与证据链闭环（`TSPN_UXFD` / `manifest.json` / `predictions.npz` / collect / postrun）
  - 7 个 paper submodules 的 WP0 入口文件提交与父仓库 gitlink 更新
  - 可解释测试门禁（装配单测 + 产物契约测试 + strict postrun）
  - LLM 工具契约与 fallback orchestrator（不依赖 `langgraph`）
- Out:
  - 在线依赖安装/外部 AutoML（restricted network）
  - 训练/绘图强耦合重构（仍以离线产物消费为主）

## Quick Validate（建议在 Review 前跑一遍）

```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
python -m pytest test/ -k 'uxfd or artifacts' -q
python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1
python -m scripts.collect_uxfd_runs --input results --out_dir reports
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml
```

## Tasks（按执行顺序）

- [ ] T0 Setup & Gap Filling（确保门禁文件齐全）
  - DoD:
    - 目录存在：`paper/LQ_vibench_fix/merge_uxfd/1_19/codex/{intake,plan,report,artifact}`
    - 关键门禁测试文件存在（若缺失则补齐后再进入 T1）：
      - `test/test_tspn_uxfd_assembly.py`
      - `test/test_run_artifacts_contract.py`
    - strict post-run 配置可用（跨日期复用是刻意的）：
      - `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml`
  - Dependencies: 无

- [ ] T1 父仓库人工 Review（代码 + 契约 + 文档口径）
  - DoD:
    - `git diff --stat` 与 `git diff` 审阅完毕，确认“可解释=可验证产物”契约无歧义：
      - `src/model_factory/X_model/TSPN_UXFD.py`
      - `src/Pipeline_01_default.py`
      - `src/task_factory/Default_task.py`
      - `src/trainer_factory/extensions/manifest.py`
      - `scripts/collect_uxfd_runs.py`
    - 确认测试的 determinism 约束与覆盖面：
      - `test/test_tspn_uxfd_assembly.py`
      - `test/test_run_artifacts_contract.py`
    - 确认文档不过度承诺且可复现：
      - `paper/LQ_vibench_fix/merge_uxfd/README.md`
      - `paper/LQ_vibench_fix/merge_uxfd/1_15/codex/TODO.md`
      - `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/README.md`
      - `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/TODO.md`
  - Dependencies: T0

- [ ] T2 Submodule Review + Commit（7 个 paper WP0 入口）
  - DoD:
    - 对每个 `paper/UXFD_paper/<paper_id>/`：
      - `git diff` 审阅 `configs/vibench/min.yaml` 与 `VIBENCH.md`
      - `min.yaml` 必须满足：`model.name: TSPN_UXFD` 且至少启用一次 UXFD（例如 `model.uxfd.enable_sp2d=true`）
      - `VIBENCH.md` 必须给出可复制运行命令（至少 1 条）
      - `git add configs/vibench/min.yaml VIBENCH.md && git commit -m "Add vibench min config + mapping doc"` 完成
    - 覆盖 7/7：`1D-2D_fusion_explainable`, `Explainable_FD_Toolkit`, `LLM_Explainable_FD_Toolkit`, `MOE_explainable`,
      `Neuralsymbolic_theory`, `Paper_fuzzy_XFD`, `TII_operator_attention`
    - 若因权限/环境限制无法提交：把 `git status -sb` 与文件路径清单写入
      `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/submodule_changes.txt` 供人工提交
  - Dependencies: T1

- [ ] T3 Submodule Review + Commit（`paper/LQ_vibench_fix`）+ 父仓库 gitlink 更新
  - DoD:
    - `cd paper/LQ_vibench_fix && git diff` 审阅并提交（包含 `merge_uxfd/`）
    - 回到父仓库更新 gitlinks：`git add paper/LQ_vibench_fix paper/UXFD_paper/* && git commit -m "Update UXFD paper submodule pointers"`
  - Dependencies: T2

- [ ] T4 Gates + Evidence（把“work”变成可追溯记录）
  - DoD:
    - Gate0 smoke：`python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`
    - Gate1 tests：`python -m pytest test/`
    - Gate2 UXFD-enabled：`python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1`
    - Gate3 toolchain：`python -m scripts.collect_uxfd_runs --input results --out_dir reports`
    - Gate4 strict post-run：`python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml`
    - 报告落盘（命令、时间、关键输出路径）：`paper/LQ_vibench_fix/merge_uxfd/1_19/codex/report/report_merge-uxfd.md`
  - Dependencies: T3

- [ ] T5 LLM Tool Contract + Fallback Orchestrator（不依赖 langgraph）
  - DoD:
    - tool contract（JSON schema 或等价约束）落盘到：
      - `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/llm_tool_contract.json`
      - overrides 白名单：仅允许 `model.uxfd.*` 与少量 `trainer.*`（如 `trainer.num_epochs` 上限）
    - fallback orchestrator（纯 Python loop）落盘到：
      - `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/fallback_orchestrator.py`
      - 必须实现：propose → run (`python main.py ... --override ...`) → parse (`manifest.json`) → score → update best → stop
    - 把设计与最小示例写入报告：`paper/LQ_vibench_fix/merge_uxfd/1_19/codex/report/report_merge-uxfd.md`
  - Dependencies: T4

- [ ] T6 LangGraph 引入决策与迁移路径（可选）
  - DoD:
    - 明确 `langgraph` 是否可在目标环境安装（联网策略/依赖版本/CI）
    - 若可：给出从 fallback loop → langgraph 的节点映射（propose/run/parse/decide）与接口不变性要求
  - Dependencies: T5

## Gates (optional)
- Gate0 (smoke): `python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`
- Gate1 (tests): `python -m pytest test/`
- Gate2 (config schema): `python -m scripts.validate_configs`
- Gate3 (postrun strict): `python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml`

## Deliverables
- `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/intake/intake_merge-uxfd.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/plan/plan_merge-uxfd.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/report/report_merge-uxfd.md` (TBD by T4/T5)
- `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/manifest_merge-uxfd.json` (TBD by T4)
- `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/submodule_changes.txt` (optional fallback by T2)
- `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/llm_tool_contract.json` (TBD by T5)
- `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/fallback_orchestrator.py` (TBD by T5)

## Rollback
- 若 submodule 合并过程中出现不确定性：撤销父仓库 gitlink 更新 commit，仅保留父仓库文档与测试；submodule 各自保留未 push 的 commit，待确认后再合并。
- 若门禁失败：优先回退到“仅 WP0 入口 + smoke 可跑”的最小状态，暂不强推 strict postrun gate。

## Execution Log
- 
