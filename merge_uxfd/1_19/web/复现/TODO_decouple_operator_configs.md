# TODO: decouple-uxfd-operator-configs

> 目标：把 UXFD“算子/装配配置”从主实验 YAML 解耦出来，主 config 只负责挑选 preset + 少量 override。

## P0 (必须先做，打通机制)
- [ ] P0-0 代码改造：`base_configs.<block>` 支持 list[str]
  - DoD: `src/configs/config_utils.load_config()` 能解析 list，并按顺序 merge；旧 YAML（string）保持兼容。
  - 验证: `python -m scripts.validate_configs`
- [ ] P0-1 目录与命名：建立 preset 目录
  - Deliverable: `configs/presets/uxfd/operators/`（含 README 说明格式/顺序/覆盖规则）
- [ ] P0-2 产出 3 个 demo preset
  - `uxfd_demo_min.yaml`（不启用 UXFD）
  - `uxfd_demo_sp2d.yaml`（SP2D + fusion + predictions）
  - `uxfd_demo_full.yaml`（sp2d + fusion + fuzzy + operator-attention + logic）
- [ ] P0-3 demo configs 变薄（仅选择 preset）
  - 修改：`configs/demo/uxfd/00_smoke_tspn_uxfd.yaml`、`configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml`、`configs/demo/uxfd/20_smoke_tspn_uxfd_full.yaml`
  - DoD: 三个 demo 都可跑通；`10_smoke` 必须产出 `manifest.json` + `predictions.npz`

## P1 (paper 对齐：7 个模块装配进核心模型)
- [ ] P1-0 为 7 个 paper 各生成一个 preset
  - Deliverable: `configs/presets/uxfd/operators/<paper_id>.yaml`
  - 约束: preset 文件只写 `model.*` 子树（避免污染 environment/data/task/trainer）
- [ ] P1-1 更新 7 个 submodule 的 `min.yaml` 引用 preset（submodule 内提交）
  - 文件: `paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml`
  - DoD: `python main.py --config paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml --override trainer.num_epochs=1` 至少抽样 2 个通过

## P2 (LLM 试错/自动化配置搜索)
- [ ] P2-0 更新 LLM 合约：优先输出 `preset_id` + 白名单 overrides
  - 建议白名单: `model.uxfd.*` + 少量训练超参（如 `trainer.learning_rate`）
- [ ] P2-1 在 `LLM_Explainable_FD_Toolkit` / fallback orchestrator 里实现：
  - 输入：任务描述 + 可选 preset 候选集
  - 输出：`--config <min.yaml> --override ...`（不生成 Python 代码）
  - DoD: budget=3 的 trial loop 能跑通并产出 leaderboard CSV

## Evidence / Commands
- `python -m scripts.validate_configs`
- `python -m scripts.validate_docs`
- `python -m pytest test/test_tspn_uxfd_assembly.py test/test_run_artifacts_contract.py -q`
- `python main.py --config configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml --override trainer.num_epochs=1`
