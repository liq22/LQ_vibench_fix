# 需要确认的决策点（12_27）

这些点如果不先确认，后续容易返工；建议尽早拍板。

---

## 1) UXFD 组件目录命名（是否引入 `UXFD_component/`）

现状：
- 代码当前已有：`src/model_factory/X_model/UXFD/`
- 12_23 README 提到未来“组件区统一命名为 `src/model_factory/X_model/UXFD_component/` 并用 shim 逐步淘汰 UXFD/”
  - 见：@`paper/LQ_vibench_fix/merge_uxfd/12_23/README.md`

结论（已拍板）：
- 保持 `src/model_factory/X_model/UXFD/` 不动（KISS），不引入 `UXFD_component/` 并行目录，避免口径分裂。

---

## 2) pilot paper 选择（WP0）

结论（已拍板）：
- pilot：`paper/UXFD_paper/1D-2D_fusion_explainable`
- 同时已补齐 7 篇 paper 的 `configs/vibench/min.yaml` + `VIBENCH.md`

备注：
- 当前仓库的最小装配已覆盖：`signal_processing_2d` / `fusion` / `operator_attention` / `fuzzy` / `logic`（best-effort）。

---

## 3) post-run / 绘图产物落位

当前脚本默认：
- 产物检查 + 绘图：`scripts/uxfd_postrun.py`
- 绘图输出：`<run_dir>/figures/`
- 审计输出：`<run_dir>/artifacts/plots/plot_eligibility.json`

需确认：
- `figures/` 是否作为统一绘图输出目录（建议保持）。

参考：@`paper/LQ_vibench_fix/merge_uxfd/12_23/plot_factory_migration_plan.md`

---

## 4) 是否需要自动落盘 `predictions.npz`（用于混淆矩阵等）

结论（已拍板，KISS）：
- 通过配置开关按需启用：`trainer.extensions.predictions.enable=true`
- 默认不强制开启（避免侵入 demos/tests）；paper 的 `min.yaml` 可以按需开启以支持混淆矩阵等离线绘图。

---

## 5) `.gitignore` 与证据样例目录

现状：
- `.gitignore` 的 `results/` 规则会忽略 `paper/LQ_vibench_fix/merge_uxfd/12_22/results/**`（样例证据链文件可能无法被跟踪）
- `.gitignore` 已不再忽略维护中的测试目录：`test/`（允许跟踪 `test/**/*.py`）

需确认：
- 样例证据链是否要纳入版本控制；如果要，需要改目录名或增加反忽略规则。
