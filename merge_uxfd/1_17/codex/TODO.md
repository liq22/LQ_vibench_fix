# UXFD：可解释测试 + LLM（langgraph）结构优化 TODO

更新时间：2026-01-17

## Goal

1) **先保证 UXFD 核心模型可用**：`TSPN_UXFD` 在 vibench（config-first）里可稳定训练/测试，并产出可消费的证据链产物。  
2) **再让 LLM_Explainable_FD_Toolkit 可调用 UXFD**：通过 langgraph 编排“提案→运行→解析→更新”，用 LLM 进行**受控的结构试错**，
自动产出更优的 `model.uxfd.*` 配置组合（以及必要的 `trainer.extensions.*` 开关）。

## Non-Goal（先不做）

- 不做在线网络依赖（restricted network）；不引入必须联网的 AutoML/外部服务。
- 不把 post-run/plot 强耦合进训练；仍优先离线消费稳定产物（`manifest.json`/`metrics.csv`/`predictions.npz`）。

## Definitions（避免歧义）

- “UXFD 模型 work”：至少满足（必须包含一次 UXFD-enabled 的 paper `min.yaml`）
  - 主仓库 smoke 可跑：
    - `python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`
  - UXFD-enabled paper `min.yaml` 可跑 1 epoch（CPU），例如：
    - `python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1`
  - 产物契约：每次 run 的 `<run_dir>/artifacts/manifest.json` 必须存在（`run_dir` 以 manifest 内的 `run_dir` 字段为准）
- “7 个 paper 完整”：WP0 入口完整（工作区层面）= 每个 submodule 存在 `configs/vibench/min.yaml` + `VIBENCH.md`
  - PR 完整 = 需要在各 submodule 仓库内 commit 后，父仓库更新 gitlink 指针
- “可解释测试”：不是“论文级解释算法”；而是**可验证的解释产物与接口契约**（预测、eligibility、可追溯 manifest、debug_state）。

## Current Facts（2026-01-17）

- 7/7 submodules 工作区已存在 `configs/vibench/min.yaml` 与 `VIBENCH.md`（但尚未在 submodule 内提交时，父仓库 PR 不会展示文件级 diff）。
- `TSPN_UXFD` 已支持通过 `model.uxfd.*` 装配（best-effort）：SP2D + Fusion + Fuzzy + OperatorAttention + Logic。
- 证据链产物（best-effort）与工具链可用：`scripts/collect_uxfd_runs.py`、`scripts/uxfd_postrun.py`。

## P0：解释性测试门禁（让“work”可被机器验证）

### P0-1：模块级单元测试（fast, deterministic）

目标：不跑训练也能证明“装配开关不会炸”，并且 shape/返回值稳定。

- [x] `test/test_tspn_uxfd_assembly.py`
  - [x] determinism 约束：CPU-only + 固定 seed + 固定输入 shape（避免 flaky）
    - 建议：`torch.manual_seed(0)` + `torch.use_deterministic_algorithms(True)` + `model.eval()`
    - 固定输入：`x.shape == (B=2, L=128, C=2)`（与 dummy data 的最小配置对齐）
    - 如需要 args fixture：用最小 `SimpleNamespace`（只填 `TSPN_UXFD` 初始化必需字段）
  - [x] `model.uxfd.enable_sp2d=true` 前向 shape 不报错
  - [x] `model.uxfd.fusion.type` 三种模式（`concat|sum|gated`）均可 forward
  - [x] `model.uxfd.fuzzy.enable=true` 时 logits shape 正确、数值有限（no nan/inf）
  - [x] `model.uxfd.logic.enable=true` 同上
  - [x] `model.uxfd.operator_attention.enable=true` 时仍可 forward（并能读到 `get_uxfd_debug_state()`）

DoD：
- ✅ `python -m pytest test/ -k uxfd -q` 通过（无需 GPU/无需下载）

### P0-2：产物契约测试（explainability as artifacts）

目标：把“解释”落到可验证的文件契约（而不是口头承诺）。

- [x] `test/test_run_artifacts_contract.py`
  - [x] 运行一次 dummy smoke（或最小 trainer step）后，`<run_dir>/artifacts/manifest.json` 存在，且满足最小 schema（v1）：
    - 必选字段（始终存在，且为 string；其中 `run_dir`/`run_id`/`timestamp` 必须非空）：
      - `run_dir`, `run_id`, `stage`, `timestamp`, `config_snapshot`, `metrics_path`
      - `paper_id`, `preset_version`, `metrics_csv_logger`, `figures_dir`, `explain_dir`, `distilled_dir`
      - `data_metadata_snapshot`, `eligibility`, `predictions_path`, `explain_summary`
    - 由 `trainer.extensions.*` 决定的可选“非空”字段（仍要求字段存在，但允许为空字符串）：
      - `trainer.extensions.predictions.enable=true` → `predictions_path` 非空且文件存在（建议固定为 `artifacts/predictions.npz`）
      - `trainer.extensions.explain.enable=true` → `eligibility` 非空且文件存在（`artifacts/explain/eligibility.json`）
      - `trainer.extensions.agent.enable=true` → `distilled_dir` 非空且目录存在（`artifacts/distilled/`）
  - [x] `trainer.extensions.predictions.enable=true` 时必出 `artifacts/predictions.npz`
  - [x] `trainer.extensions.explain.enable=true` 时必出 `artifacts/explain/eligibility.json`

DoD：
- ✅ `python -m pytest test/ -k artifacts -q` 通过

### P0-3：离线可解释检查门禁（post-run）

目标：把“混淆矩阵/学习曲线可画”变成可复现门禁。

- [ ] 给每个 paper 的 `min.yaml` 统一约定：是否默认打开 `trainer.extensions.predictions.enable`（建议默认打开）
- [ ] 为 CI/回归准备“严格门禁配置”（跨日期复用是刻意的）：
  - canonical：`paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_strict.yaml`
  - 1_17 便捷副本：`paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml`（已落盘）

DoD：
- `python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml`
  对“新产生的 runs”检查通过（历史 runs 可单独归档/忽略）

## P1：把 UXFD 暴露为可被 LangGraph 调用的“工具”

### P1-1：确定依赖与落位（先做可用的最小闭环）

- [ ] 确认运行环境是否已安装 `langgraph`：
  - `python -c "import langgraph; print(langgraph.__version__)"`（若失败：先提供纯 python fallback 版 orchestrator）
- [ ] 约定放置位置（推荐在 submodule 内，避免主仓库引入新依赖）：
  - `paper/UXFD_paper/LLM_Explainable_FD_Toolkit/tools/uxfd/`（示例）

DoD：
- 能在 LLM toolkit 中 `import` 到“run vibench + parse manifest”的工具函数

### P1-2：定义工具契约（LLM 只能改可控参数）

目标：LLM 只能在白名单内试错，避免写坏仓库/跑飞超参。

- [ ] 设计 `UXFDConfigProposal`（JSON schema 或 pydantic）：
  - 必须字段：`paper_id`, `base_config_path`, `overrides`（仅允许 `model.uxfd.*` 与少量 trainer 参数）
  - 白名单示例：
    - `model.uxfd.enable_sp2d`
    - `model.uxfd.sp2d.n_fft`, `model.uxfd.sp2d.hop_length`
    - `model.uxfd.fusion.type`
    - `model.uxfd.fuzzy.enable`, `model.uxfd.fuzzy.logit_scale`
    - `model.uxfd.operator_attention.enable`, `model.uxfd.operator_attention.operators`
    - `model.uxfd.logic.enable`, `model.uxfd.logic.logit_scale`
    - `trainer.num_epochs`（上限）、`trainer.seed`、`trainer.extensions.*`
- [ ] 统一输出：每次 run 必须返回 `manifest.json` 路径 + 关键指标（可从 `test_result_*.csv` 或 metrics.csv 解析）

DoD：
- 给 1 个 paper（`LLM_Explainable_FD_Toolkit` 对应的 min config）跑通 “提案→执行→解析→评分” 一轮

### P1-3：LangGraph 工作流（最小可用图）

节点建议：
- `propose_config`：LLM 基于当前 best 与失败原因给出下一组 overrides
- `run_experiment`：执行 `python main.py --config <min.yaml> --override ...`
- `collect_evidence`：读 `<run_dir>/artifacts/manifest.json` + 汇总指标（并写入 leaderboard CSV）
- `decide_next`：停止条件（budget/无提升/异常）与“更新 best config”

DoD：
- 一个 CLI：`python -m <llm_toolkit>.tools.uxfd.optimize --paper_id ... --budget 10`
- 产物：
  - `results/uxfd/autotune/<paper_id>/...`
  - `reports/uxfd_autotune_<paper_id>.csv`（每次试错一行）
  - `best_config_overrides.yaml`（可直接复制进最终 config）

## P2：LLM 试错优化策略（可解释 + 可回滚）

### P2-1：定义搜索空间与先验（减少无效试错）

- [ ] 搜索空间 v1（建议从开关开始，再调连续参数）：
  - 开关：`enable_sp2d`, `fusion.type`, `fuzzy.enable`, `operator_attention.enable`, `logic.enable`
  - 连续参数：`fuzzy.logit_scale`、`logic.logit_scale`（范围建议 0.1–2.0）
  - STFT：`n_fft`（16–256，受 in_dim 上限约束）、`hop_length`（n_fft/2 附近）
- [ ] 先验规则（LLM 提案时强制遵守）：
  - 先跑 baseline（全部关闭）→ 再逐个打开单模块 → 再组合（避免 combinatorial 爆炸）
  - 每次只改 1–2 个因子（便于归因）

### P2-2：评分函数（多目标、可解释）

- [ ] 主指标：`test_acc_*` 或 `test_total_loss`（按任务类型选择）
- [ ] 次指标：运行稳定性（无 exception）、产物完整性（manifest/predictions）
- [ ] 解释性日志：
  - 把每次提案的“改动原因/预期收益”写入一列（LLM 输出的短 rationale）
  - 把 `get_uxfd_debug_state()`（如果可用）写入 distilled summary（LLM-free）

### P2-3：回滚与复现

- [ ] “最优结构”必须能复现：固定 seed + 固定 config snapshot + 固定 overrides
- [ ] 输出 `best_overrides.yaml` + `reproduce.sh`

## Deliverables

- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/TODO.md`（本文件）
- （后续落地后）新增/完善测试文件：`test/test_tspn_uxfd_assembly.py`、`test/test_run_artifacts_contract.py`
- （后续落地后）LLM toolkit 内的 langgraph orchestrator + CLI（建议放在 submodule 内）

## Evidence（落地后如何验收）

```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
python -m scripts.validate_configs
python -m pytest test/
python -m scripts.collect_uxfd_runs --input results --out_dir reports
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml
```
