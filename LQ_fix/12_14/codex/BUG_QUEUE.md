# Bug Queue（逐个确认修复）

说明：
- 本清单用于“你确认一个，我修一个”的节奏推进。
- 详情记录仍保存在 `docs/LQ_fix/12_14/bugs/`（这里做汇总与修复入口）。

## P0（建议优先确认）

- [ ] **BUG-20251214-001**：H5 关闭时裸 `except`（`src/data_factory/H5DataDict.py:34`）
  - 详情：`docs/LQ_fix/12_14/codex/bugs/BUG-20251214-001.md`
- [ ] **BUG-20251214-002**：`__del__` 裸 `except` 吞资源清理失败（`src/data_factory/H5DataDict.py:85`）
  - 详情：`docs/LQ_fix/12_14/codex/bugs/BUG-20251214-002.md`
- [ ] **BUG-20251214-004**：ID_selector 多处裸 `except` 影响采样正确性（`src/data_factory/samplers/del/ID_selector.py:106`）
  - 详情：`docs/LQ_fix/12_14/codex/bugs/BUG-20251214-004.md`

## P1（P0 完成后确认）

- [ ] **BUG-20251214-003**：配置类型转换裸 `except` 返回硬编码默认值（`src/configs/deprecated/config_validator.py:370`）
  - 详情：`docs/LQ_fix/12_14/codex/bugs/BUG-20251214-003.md`

## 候选问题（先不修，等待你点名）

来源：`docs/LQ_fix/12_14/bugs/reports/quick_triage_report.md`

- `except_exception_py`（175）：优先看 `src/Pipeline_03_multitask_pretrain_finetune.py`、`src/utils/evaluation/ZeroShotEvaluator.py`
- `paths_envs_py`（254）+ `paths_envs_yaml`（230）：硬编码 `/home/`、`/mnt/`、环境变量依赖
- `assert_raise_py`（614）：区分“用户可触发断言”与“开发期断言”

