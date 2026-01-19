# gv1 (Applied): UXFD SSOT + Runnable Demos + Gates

本文件是对 `gptv1.md`（Prompt/评审）里“配置优先 + 反幻觉 + SSOT 闭环”建议的 **落地版摘要**：给人/LLM 作为后续维护的“唯一事实入口 + 最小门禁”。

## 当前仓库的 UXFD 核心模型（Core Contract）

- 统一入口模型：`model.type: X_model` + `model.name: TSPN_UXFD`
- 实现入口：`src/model_factory/X_model/TSPN_UXFD.py`
- 1D 基础可组合算子/特征 key 来自 `src/model_factory/X_model/TSPN.py` 的 `ALL_SP` / `ALL_FE`
- UXFD 装配开关来自 `model.uxfd.*`（由 `TSPN_UXFD` 装配）

SSOT：
- `src/model_factory/X_model/UXFD/FACT_TABLE.md`
- `src/model_factory/X_model/UXFD/OPERATOR_CATALOG.md`

## Runnable Demos（最小复现实例）

入口索引：`configs/demo/uxfd/README.md`

- Minimal（不启用 UXFD 模块）：`configs/demo/uxfd/00_smoke_tspn_uxfd.yaml`
- UXFD-enabled（SP2D + fusion + predictions）：`configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml`
- UXFD-enabled（sp2d + fusion + fuzzy + operator-attention + logic）：`configs/demo/uxfd/20_smoke_tspn_uxfd_full.yaml`

## 产物契约（Explainability Contract）

目标：让工具链稳定消费 run_dir 的产物与索引。

- `<run_dir>/config_snapshot.yaml`
- `<run_dir>/artifacts/manifest.json`（best-effort 写入，不应 crash 训练）
- 可选：`<run_dir>/artifacts/predictions.npz`（由 `trainer.extensions.predictions.enable=true` 控制）

实现：`src/trainer_factory/extensions/manifest.py`

## 最小门禁（Quick Validate）

```bash
python -m scripts.validate_configs
python -m scripts.validate_docs
python -m pytest test/test_tspn_uxfd_assembly.py test/test_run_artifacts_contract.py -q

python main.py --config configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml --override trainer.num_epochs=1
```

## 反幻觉维护规则（给后续 Agent）

- 配置字段名必须来自现有 YAML / 实现代码（禁止发明 `model.uxfd.signal_processing` 这类不存在字段）。
- 算子与特征清单以 `src/model_factory/X_model/UXFD/OPERATOR_CATALOG.md` 为准（它从 `ALL_SP/ALL_FE` 导出）。
- 任何“已支持/已实现”的声明必须能被上面的门禁命令验证（能跑通 demo + 产生 manifest）。
