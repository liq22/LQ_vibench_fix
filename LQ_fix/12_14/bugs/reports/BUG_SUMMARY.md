# Bug Summary（优化扫描后，全仓库候选问题概览）

生成时间：2025-12-14

## 1. 扫描范围与方法

本次为“优化后扫描”，重点降低噪声：
- 代码扫描：仅扫描 `src/`、`dev/`、`test/` 的 Python 文件（`-tpy`）
- 配置扫描：仅扫描 `configs/` 的 YAML 文件（`-tyaml`）
- 扫描输出保存在：`docs/LQ_fix/12_14/bugs/reports/scan_logs/`
- 由 `docs/LQ_fix/12_14/bugs/quick_triage.py` 生成汇总报告：`docs/LQ_fix/12_14/bugs/reports/quick_triage_report.md`

## 2. 统计结果（候选问题）

候选总数：1324

- `todo_py`: 38
- `todo_yaml`: 5
- `except_bare_py`: 8（其中 `src/` 的 7 条按 P0 处理；`dev/del/` 的 1 条视作低优先级候选）
- `except_exception_py`: 175
- `except_baseexception_py`: 0
- `assert_raise_py`: 614
- `paths_envs_py`: 254
- `paths_envs_yaml`: 230

> 说明：上述为“候选问题”而非已确认 bug；仍需按模块逐条确认可达路径、触发条件、影响面。

## 3. 已建档 Bug（截至目前）

已建档 4 个：
- `BUG-20251214-001` / `BUG-20251214-002` / `BUG-20251214-004`：见 `docs/LQ_fix/12_14/bugs/data_factory.md`
- `BUG-20251214-003`：见 `docs/LQ_fix/12_14/bugs/configuration.md`

## 4. P0（最高优先级）候选清单

来自 `except_bare_py`，位于 `src/` 中的裸 `except:`（静默吞异常风险最高）：
- `src/configs/deprecated/config_validator.py:375`
- `src/configs/deprecated/config_validator.py:380`
- `src/data_factory/H5DataDict.py:40`
- `src/data_factory/H5DataDict.py:89`
- `src/data_factory/samplers/del/ID_selector.py:123`
- `src/data_factory/samplers/del/ID_selector.py:150`
- `src/data_factory/samplers/del/ID_selector.py:162`

## 5. 主要风险面（P1/P2 候选）

### 5.1 过宽异常捕获（`except Exception`）

数量：175（需重点看是否“吞异常/不记录/返回默认值导致 silent failure”）

Top 热点文件（详见 `quick_triage_report.md`）：
- `src/Pipeline_03_multitask_pretrain_finetune.py`
- `src/utils/evaluation/ZeroShotEvaluator.py`
- `src/data_factory/reader/utils.py`

### 5.2 路径硬编码/环境变量依赖

- Python：254
- YAML：230

典型风险：
- 硬编码 `/home/...`、`/mnt/...`，导致在他人环境无法运行
- 输出目录（`save/`）与配置/README 约定不一致导致覆盖/难以定位产出

### 5.3 assert/raise 使用

数量：614（需区分“测试/开发期断言”与“用户可触发断言导致崩溃”）

建议关注：
- `src/configs/config_utils.py`（配置解析与覆盖逻辑）
- `src/Pipeline_03_multitask_pretrain_finetune.py`（pipeline 多阶段流程）

## 6. 下一步（修复计划入口）

修复计划已整理在：
- `docs/LQ_fix/12_14/codex/BUG_FIX_PLAN.md`

