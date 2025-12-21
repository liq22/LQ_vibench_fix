# Bug Fix Plan（基于 2025-12-14 优化扫描）

本计划面向“把候选问题逐步转化为可验证修复”，按优先级分批推进；默认不一次性扫全仓库逐条改，避免引入大范围回归。

## 0. 修复前准备（一次性）

1. 固化扫描基线（用于回归对比）
   - 保留：`docs/LQ_fix/12_14/bugs/reports/scan_logs/`
   - 保留：`docs/LQ_fix/12_14/bugs/reports/quick_triage_report.md`
2. 统一 Bug 记录口径
   - 模板：`docs/LQ_fix/12_14/bugs/BUG_TEMPLATES.md`
   - 已建档：`docs/LQ_fix/12_14/bugs/data_factory.md`、`docs/LQ_fix/12_14/bugs/configuration.md`

## 1. Batch-1：P0 修复（裸 except）

目标：消除 `src/` 内所有裸 `except:`，至少做到“捕获具体异常 + 记录日志 + 明确继续/中断策略”。

### 1.1 逐项修复清单

1. `src/data_factory/H5DataDict.py:40`
   - 场景：关闭 H5 句柄
   - 建议：捕获 `(OSError, ValueError)` 等，并记录 warning；必要时确保 `self.h5f` 状态归零

2. `src/data_factory/H5DataDict.py:89`
   - 场景：`__del__` 中清理资源
   - 建议：避免吞异常；最少记录到 logger 或 `sys.stderr`；避免在解释器退出阶段做复杂 IO

3. `src/data_factory/samplers/del/ID_selector.py:123,150,162`
   - 场景：采样/索引/数据读取关键路径
   - 建议：
     - 如果异常意味着采样结果不可用：应 raise（或转换为明确的自定义异常）
     - 如果可降级：记录 error + 附带上下文（文件、索引范围、当前 system/domain 等）

4. `src/configs/deprecated/config_validator.py:375,380`
   - 场景：配置值类型转换 fallback
   - 建议：仅捕获 `(ValueError, TypeError, OverflowError)`，并给出明确提示；同时确认该 deprecated validator 是否仍在主路径被调用（若已弃用，可降级优先级但仍建议修）

### 1.2 验证方式（每修一个文件都做）

- 运行最小单元检查：
  - `python -m compileall src/`
- 若有可跑的最小 demo（不依赖数据或使用 dummy 配置），优先跑 1 次确保不 crash
- 重跑扫描确认裸 except 数量下降：
  - 重新生成 `rg_except_bare_py.txt` 并对比行数

## 2. Batch-2：路径硬编码（/home、/mnt、固定输出目录）

目标：把“环境相关路径”从代码/配置中抽离，避免换机器不可运行。

### 2.1 处理策略

- **代码层**：集中到一个 path resolver（已有 `src/utils/config/path_standardizer.py`，优先复用/扩展）
- **配置层**：统一使用相对路径或环境变量（例如 `PROJECT_HOME`）+ 清晰默认值
- **文档层**：README/demo config 给出“可复制”的路径示例，不写开发者本地绝对路径

### 2.2 执行步骤

1. 对 `paths_envs_py` Top 文件做逐条确认（优先 `src/` 与 `configs/`）
2. 将确属硬编码的路径改为：
   - 配置项（优先），或
   - `Path(PROJECT_HOME) / ...`（次选），或
   - 相对仓库路径（仅限不涉及运行产出/用户数据的路径）
3. 对 `configs/` 中出现的绝对路径，提供默认示例与注释说明（例如用户应改为自己的数据目录）

## 3. Batch-3：`except Exception` 过宽捕获（175 条）

目标：减少 silent failure；把异常处理变成“可观察、可定位”。

### 3.1 优先处理顺序

1. `src/Pipeline_03_multitask_pretrain_finetune.py`
2. `src/utils/evaluation/ZeroShotEvaluator.py`
3. `src/data_factory/reader/utils.py`

### 3.2 统一改造准则

- 禁止 `except Exception: pass`
- 必须包含：
  - 记录异常类型与上下文（关键参数、文件/数据集、batch 元信息）
  - 明确选择：`raise` 还是降级为默认值（并记录“降级发生”）

## 4. Batch-4：assert/raise 的可用性风险（614 条）

目标：避免“用户输入可触发断言导致直接崩溃”，同时保留开发期断言的价值。

执行原则：
- `src/` 中用于用户配置校验的 `assert` → 改为显式校验并抛出 `ValueError`/`KeyError` 等带信息异常
- 保留测试/开发用 assert（例如 `dev/` 内部验证脚本）但避免混入主路径

## 5. 交付节奏建议

每个 batch 单独一个 PR/提交组：
- Batch-1（P0）优先合入
- Batch-2/3/4 按风险与工作量拆分

同时维护：
- `docs/LQ_fix/12_14/bugs/reports/BUG_SUMMARY.md`：每批修复后更新统计
- `docs/LQ_fix/12_14/bugs/reports/quick_triage_report.md`：每批修复后重新生成并留存

