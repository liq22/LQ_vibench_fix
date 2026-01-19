# Plan: UXFD Components 全面检查

**创建日期**: 2026-01-17
**负责人**: Claude
**优先级**: P0（合并前验证）

---

## 目标

对 PHM-Vibench 主仓库中的 UXFD 组件进行全面检查，确保：
1. 所有组件代码存在且可导入
2. 组件接口一致（Config 类 + 实现）
3. TSPN_UXFD 集成正确
4. 配置开关映射正确
5. 无潜在运行时错误

---

## 组件清单

| 组件 | 路径 | 状态 | 优先级 |
|------|------|------|--------|
| SP2D (Signal Processing 2D) | `src/model_factory/X_model/UXFD/signal_processing_2d/` | ✅ 已实现 | P0 |
| Fusion | `src/model_factory/X_model/UXFD/fusion/` | ✅ 已实现 | P0 |
| Fuzzy | `src/model_factory/X_model/UXFD/fuzzy/` | ✅ 已实现 | P1 |
| OperatorAttention | `src/model_factory/X_model/UXFD/operator_attention/` | ✅ 已实现 | P1 |
| Neurosymbolic/Logic | `src/model_factory/X_model/UXFD/neurosymbolic/` | ✅ 已实现 | P1 |
| TSPN_UXFD (Orchestrator) | `src/model_factory/X_model/TSPN_UXFD.py` | ✅ 已实现 | P0 |

---

## Tasks（按执行顺序）

### Task 1: 导入验证（Phase 0 - Preflight）

**目标**: 确保所有 UXFD 组件可被成功导入

**步骤**:
1. 验证 `UXFD/__init__.py` 存在
2. 验证各子模块 `__init__.py` 存在且导出正确
3. 运行 Python 导入测试

**验证命令**:
```bash
# 主仓库根目录
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2

# 导入测试
python -c "from src.model_factory.X_model.UXFD.signal_processing_2d import STFTTimeFrequency; print('✓ SP2D')"
python -c "from src.model_factory.X_model.UXFD.fusion import FusionConfig, build_fusion; print('✓ Fusion')"
python -c "from src.model_factory.X_model.UXFD.fuzzy import FuzzyConfig, FuzzyReasoner; print('✓ Fuzzy')"
python -c "from src.model_factory.X_model.UXFD.operator_attention import OperatorAttention1D, OperatorAttentionConfig; print('✓ OperatorAttention')"
python -c "from src.model_factory.X_model.UXFD.neurosymbolic import LogicConfig, LogicReasoner; print('✓ Neurosymbolic')"
python -c "from src.model_factory.X_model.TSPN_UXFD import Model; print('✓ TSPN_UXFD')"
```

**预期输出**: 所有导入成功，无 ImportError

**证据**: 记录每个导入的输出

**回滚**: 无（只读操作）

---

### Task 2: 接口一致性检查

**目标**: 确保所有组件遵循统一的接口模式

**步骤**:
1. 检查每个组件是否有 `*Config` dataclass
2. 检查每个组件是否有主要的 `nn.Module` 类
3. 检查 `__init__.py` 的 `__all__` 导出

**验证内容**:

| 组件 | Config 类 | Main 类 | __all__ |
|------|-----------|---------|---------|
| SP2D | `STFTConfig` | `STFTTimeFrequency` | ✓ |
| Fusion | `FusionConfig` | `build_fusion()` | ✓ |
| Fuzzy | `FuzzyConfig` | `FuzzyReasoner` | ✓ |
| OperatorAttention | `OperatorAttentionConfig` | `OperatorAttention1D` | ✓ |
| Neurosymbolic | `LogicConfig` | `LogicReasoner` | ✓ |

**证据**: 复制每个 `__init__.py` 的内容到检查报告

**回滚**: 无（只读操作）

---

### Task 3: TSPN_UXFD 集成检查

**目标**: 确保所有组件在 TSPN_UXFD 中正确集成

**步骤**:
1. 检查 TSPN_UXFD.py 中的 import 语句
2. 验证各组件的启用开关（`_get_attr` 调用）
3. 验证组件初始化逻辑
4. 验证 forward 逻辑中的组件调用

**检查点**:

| 开关 | 代码路径 | 状态 |
|------|----------|------|
| `model.uxfd.enable_sp2d` | 第 49 行 | ✓ |
| `model.uxfd.fuzzy.enable` | 第 50 行 | ✓ |
| `model.uxfd.operator_attention.enable` | 第 51-53 行 | ✓ |
| `model.uxfd.logic.enable` | 第 54 行 | ✓ |

**验证命令**:
```bash
# 检查 TSPN_UXFD.py 中的关键行
grep -n "_get_attr.*enable" /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2/src/model_factory/X_model/TSPN_UXFD.py
```

**证据**: 记录 grep 结果

**回滚**: 无（只读操作）

---

### Task 4: 配置构建函数检查

**目标**: 确保所有 `_build_*_cfg` 函数正确

**步骤**:
1. 检查 `_build_stft_cfg` (第 164-187 行)
2. 检查 `_build_fusion_cfg` (第 190-204 行)
3. 检查 `_build_fuzzy_cfg` (第 207-221 行)
4. 检查 `_build_operator_attention_cfg` (第 224-240 行)
5. 检查 `_build_logic_cfg` (第 243-257 行)

**验证要点**:
- 每个函数都有默认值处理
- 每个函数都有参数验证
- 每个函数都返回正确的 Config 类型

**证据**: 记录每个函数的签名和返回值类型

**回滚**: 无（只读操作）

---

### Task 5: 运行时行为验证

**目标**: 创建最小测试用例验证组件行为

**步骤**:
1. 创建 SP2D 测试（输入张量 → 输出形状验证）
2. 创建 Fusion 测试（concat/sum/gated）
3. 创建 Fuzzy 测试（前向传播）
4. 创建 OperatorAttention 测试（权重返回）
5. 创建 Logic 测试（前向传播）

**测试脚本**:
```python
import torch
from src.model_factory.X_model.UXFD.fusion import build_fusion, FusionConfig
from src.model_factory.X_model.UXFD.fuzzy import FuzzyReasoner, FuzzyConfig
from src.model_factory.X_model.UXFD.operator_attention import OperatorAttention1D, OperatorAttentionConfig
from src.model_factory.X_model.UXFD.neurosymbolic import LogicReasoner, LogicConfig

# Fusion test
x = torch.randn(2, 64)
for ft in ["concat", "sum", "gated"]:
    f = build_fusion(64, FusionConfig(fusion_type=ft))
    y = f(x, x)
    print(f"Fusion {ft}: {x.shape} -> {y.shape}")

# Fuzzy test
fuzzy = FuzzyReasoner(64, 10, FuzzyConfig())
y = fuzzy(torch.randn(2, 64))
print(f"Fuzzy: (2, 64) -> {y.shape}")

# OperatorAttention test
op = OperatorAttention1D(1, OperatorAttentionConfig())
x = torch.randn(2, 100, 1)
y, w = op(x)
print(f"OperatorAttention: {x.shape} -> {y.shape}, weights: {w.shape}")

# Logic test
logic = LogicReasoner(64, 10, LogicConfig())
y = logic(torch.randn(2, 64))
print(f"Logic: (2, 64) -> {y.shape}")
```

**证据**: 记录每个测试的输出

**回滚**: 无（独立测试脚本）

---

## Dependencies（依赖关系）

```
Task 1 (导入验证)
    ↓
Task 2 (接口检查) ← ─ ─
    ↓                 │
Task 3 (集成检查) ─ ─ ─
    ↓
Task 4 (配置检查)
    ↓
Task 5 (运行时验证)
```

---

## DoD（Definition of Done）

- [ ] Task 1 完成：所有组件导入成功
- [ ] Task 2 完成：接口一致性验证通过
- [ ] Task 3 完成：TSPN_UXFD 集成检查通过
- [ ] Task 4 完成：配置构建函数检查通过
- [ ] Task 5 完成：运行时测试全部通过
- [ ] 检查报告已生成：`1_17/codex/report/uxfd-components-check-report.md`

---

## Gates（检查点）

| Gate | 命令 | 预期 | 失败处理 |
|------|------|------|----------|
| G1 | 导入测试脚本 | 所有导入成功 | 记录 ImportError，停止并报告 |
| G2 | 接口检查脚本 | 所有组件有 Config + Main 类 | 记录缺失项，继续但标记 |
| G3 | TSPN_UXFD 检查 | 所有开关正确映射 | 记录问题，继续但标记 |
| G4 | 运行时测试 | 所有测试通过 | 记录失败，标记需要修复 |

---

## Evidence（证据要求）

| 证据 | 类型 | 存储位置 |
|------|------|----------|
| 导入测试输出 | 文本 | `1_17/glm/evidence/import_test.txt` |
| 接口检查表 | Markdown | `1_17/glm/evidence/interface_check.md` |
| TSPN_UXFD 检查结果 | Markdown | `1_17/glm/evidence/tspn_integration_check.md` |
| 运行时测试输出 | 文本 | `1_17/glm/evidence/runtime_test.txt` |
| 最终报告 | Markdown | `1_17/codex/report/uxfd-components-check-report.md` |

---

## Rollback（回滚计划）

本检查计划均为只读操作，无需回滚。

---

## Next（后续行动）

1. 完成检查后，生成 `1_17/codex/report/uxfd-components-check-report.md`
2. 如发现阻塞问题，更新 `1_15/codex/TODO.md`
3. 如无阻塞问题，确认 UXFD 合并可进入下一阶段
