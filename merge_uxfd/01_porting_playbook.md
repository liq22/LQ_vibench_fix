# UXFD 移植手册

**目标**: 面向实施者的"从上游文件 → 主仓库目录"映射表 + 可验证的 DoD。

---

## 环境设置

```bash
# 上游仓库（源）
export UXFD_UPSTREAM=/home/user/LQ/B_Signal/Unified_X_fault_diagnosis

# 目标仓库
export VIBENCH_ROOT=$(pwd)  # PHM-Vibench 根目录
```

---

## 预计工作量

| 阶段 | 预计时间 | 依赖 |
|-------|----------|------|
| 阶段 1: SP2D | 2-3 小时 | 无 |
| 阶段 2: Fusion | 1-2 小时 | 阶段 1 |
| 阶段 3: Attention/Fuzzy | 2-4 小时 | 无 |
| 阶段 4: TSPN_UXFD | 3-5 小时 | 阶段 1-3 |
| 阶段 5: Baselines | 1-2 小时 | 可选 |
| **总计** | **1-2 天** | - |

---

## 迁移顺序（按 pilot 依赖）

### 阶段 1: Signal Processing 2D (SP2D) - 基础

| 上游文件 | 目标目录 | 备注 |
|---------------|------------------|-------|
| `$UXFD_UPSTREAM/model/Signal_processing_2D.py` | `src/model_factory/X_model/UXFD/signal_processing_2d/` | 输出约定: BTFC layout |

**DoD (验证命令)**:
> ⚠️ 以当前仓库的最小实现为准：现阶段提供的是 `STFTTimeFrequency`（magnitude-only）。
```bash
# 验证导入
python -c "from src.model_factory.X_model.UXFD.signal_processing_2d import STFTTimeFrequency; print('OK')"

# 验证输出形状 (B, T, F, C)
python -c "
import torch
from src.model_factory.X_model.UXFD.signal_processing_2d.stft_tfr import STFTConfig, STFTTimeFrequency
x = torch.randn(2, 128, 2)  # BLC
y = STFTTimeFrequency(STFTConfig(n_fft=64, hop_length=32))(x)
print(f'Output shape: {y.shape}')  # 期望: (B, T, F, C)
"
```

---

### 阶段 2: Fusion1D2D - 依赖 SP2D

| 上游文件 | 目标目录 | 说明 |
|---------------|------------------|------|
| `$UXFD_UPSTREAM/model/Fusion1D2D.py` | `src/model_factory/X_model/UXFD/fusion/` | 完整版 |
| `$UXFD_UPSTREAM/model/Fusion1D2D_simple.py` | `src/model_factory/X_model/UXFD/fusion/` | 简化版 |

**DoD**:
```bash
python -c "from src.model_factory.X_model.UXFD.fusion import build_fusion; print('OK')"
```

---

### 阶段 3: Attention / Fuzzy - 按需

| 上游文件 | 目标目录 | 优先级 |
|---------------|------------------|----------|
| `$UXFD_UPSTREAM/model/operator_attention.py` | `src/model_factory/X_model/UXFD/operator_attention/` | P1 |
| `$UXFD_UPSTREAM/model/operator_attention_simple.py` | `src/model_factory/X_model/UXFD/operator_attention/` | P1 |
| `$UXFD_UPSTREAM/model/FuzzyLogic.py` | `src/model_factory/X_model/UXFD/fuzzy/` | P1 |
| `$UXFD_UPSTREAM/model/FuzzyLogic_simple.py` | `src/model_factory/X_model/UXFD/fuzzy/` | P1 |
| `$UXFD_UPSTREAM/model/FuzzyLogic_v2.py` | `src/model_factory/X_model/UXFD/fuzzy/` | P1 |
| `$UXFD_UPSTREAM/model/Logic_inference.py` | `src/model_factory/X_model/UXFD/neurosymbolic/` | P1 |

**DoD**:
```bash
python -c "from src.model_factory.X_model.UXFD.operator_attention import OperatorAttention1D; print('OK')"
python -c "from src.model_factory.X_model.UXFD.fuzzy import FuzzyReasoner; print('OK')"
python -c "from src.model_factory.X_model.UXFD.neurosymbolic import LogicReasoner; print('OK')"
```

---

### 阶段 4: TSPN_UXFD - 集成

| 上游文件 | 目标目录 | 说明 |
|---------------|------------------|------|
| `$UXFD_UPSTREAM/model/TSPN.py` | `src/model_factory/X_model/UXFD/tspn/` | 主模型 |
| - | `src/model_factory/X_model/TSPN_UXFD.py` | 主仓库稳定入口（orchestrator；读 `model.uxfd.*`） |

**需要更新 Registry**:
在 `src/model_factory/model_registry.csv` 中确认存在 `model.name=TSPN_UXFD` 的行（入口应指向可被
`model_factory` import 的模块路径；当前仓库使用 `src/model_factory/X_model/TSPN_UXFD.py` 作为稳定入口）。

示例（字段以仓库内 CSV header 为准）：
```csv
model.type,model.name,module_path,args,notes,test_status
X_model,TSPN_UXFD,src/model_factory/X_model/TSPN_UXFD.py,...
```

**DoD**:
```bash
# 最小闭环：跑通任意一个 paper 的 vibench 配置（CPU 1 epoch）
python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1

# 证据链闭环：manifest → CSV
python -m scripts.collect_uxfd_runs --input results --out_dir reports
ls -la reports/uxfd_runs.csv
```

---

### 阶段 5: Baselines (model_collection) - 可选

| 上游文件 | 目标目录 | 注册名建议 |
|---------------|------------------|----------|
| `$UXFD_UPSTREAM/model_collection/ExplainableCNN.py` | `src/model_factory/X_model/baselines/` | `BASE_ExplainableCNN` |

**DoD**:
> ⚠️ 注意：此 DoD 在完成该阶段迁移后才能运行
```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml \
  --override model.name=BASE_ExplainableCNN trainer.num_epochs=1
```

---

## 配置字段更新

每个迁移组件后，对应 YAML 需要更新：

```yaml
model:
  type: "X_model"
  name: "<registered_name>"  # 如 TSPN_UXFD

trainer:
  extensions:
    explain:
      enable: true
      explainer: "timefreq"
    predictions:
      enable: true
    agent:
      enable: true   # LLM-free distillation
```

---

## 验证命令（每阶段运行）

```bash
# 1. 验证配置
python -m scripts.validate_configs

# 2. 检查解析后的配置
python -m scripts.config_inspect --config <yaml>

# 3. 烟雾测试
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1

# 4. pytest
python -m pytest test/ -k "test_name"
```

---

## 常见问题排查

| 问题 | 症状 | 修复 |
|------|------|------|
| Layout 不匹配 | `Expected BLC, got BCL` | 在 `adapters/` 中添加 permute |
| FFT 复数值 | 绘图失败 | 使用 `magnitude_only=True` |
| Registry 找不到 | `Model not found` | 检查 `model_registry.csv` 拼写 |
| Import 失败 | `ModuleNotFoundError` | 检查 `__init__.py` 导出 |

---

## 下一步

- **快速开始**: [00_quickstart.md](00_quickstart.md)
- **待决决策**: [12_27/codex/DECISIONS_NEEDED.md](12_27/codex/DECISIONS_NEEDED.md)
- **原子任务**: [1_7/glm/README.md](1_7/glm/README.md)
- **现状 + TODO（SSOT）**: [1_15/codex/TODO.md](1_15/codex/TODO.md)
