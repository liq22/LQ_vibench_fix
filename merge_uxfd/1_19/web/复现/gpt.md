本目录用于“复现视角”的方案收敛：把论文理解转为 **可装配的 UXFD 配置**，并让配置对人/LLM 都足够清晰。

当前结论：仅靠把 `model.signal_processing_configs` / `model.feature_extractor_configs` / `model.uxfd.*` 全写进主实验 YAML，可读性与可维护性都偏差；建议把“算子/装配配置”拆成独立 preset 文件，主 config 只负责选择 preset + 少量 override。

落地方案（plan + tasks）：
- `paper/LQ_vibench_fix/merge_uxfd/1_19/web/复现/plan_decouple_operator_configs.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_19/web/复现/TODO_decouple_operator_configs.md`

备注：
- `paper/LQ_vibench_fix/merge_uxfd/1_19/web/复现/g.md` 里的 `_base_` 继承写法不是本仓库机制；本仓库以 `base_configs`（`src/configs/config_utils.py`）做组合加载。
