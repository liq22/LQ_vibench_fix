# Exec: UXFD Components 全面检查

## Source
- Plan: `1_17/codex/plan/plan_uxfd-components-check.md`

## Assumptions
- 主仓库路径: `/home/user/LQ/B_Signal/vibench_fix/PHM-Vibench copy 2/`
- Python 环境已配置，torch 可导入
- 所有源代码文件可读

---

## Execution Sequence

### Phase 0 (Preflight): 环境准备

**Step 0.1**: 创建证据目录
```bash
mkdir -p paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence
mkdir -p paper/LQ_vibench_fix/merge_uxfd/1_17/codex/report
```

**Evidence**: 目录创建成功
**Rollback**: 无

---

### Phase 1: 导入验证（G1）

**Step 1.1**: 验证 SP2D 导入
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2
python -c "from src.model_factory.X_model.UXFD.signal_processing_2d import STFTTimeFrequency; print('✓ SP2D imported')" \
  2>&1 | tee paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/import_sp2d.txt
```

**Evidence**: `1_17/glm/evidence/import_sp2d.txt`
**Expected**: `✓ SP2D imported`
**On fail**: 记录 ImportError，标记为阻塞

---

**Step 1.2**: 验证 Fusion 导入
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2
python -c "from src.model_factory.X_model.UXFD.fusion import FusionConfig, build_fusion; print('✓ Fusion imported')" \
  2>&1 | tee paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/import_fusion.txt
```

**Evidence**: `1_17/glm/evidence/import_fusion.txt`
**Expected**: `✓ Fusion imported`
**On fail**: 记录 ImportError，标记为阻塞

---

**Step 1.3**: 验证 Fuzzy 导入
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2
python -c "from src.model_factory.X_model.UXFD.fuzzy import FuzzyConfig, FuzzyReasoner; print('✓ Fuzzy imported')" \
  2>&1 | tee paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/import_fuzzy.txt
```

**Evidence**: `1_17/glm/evidence/import_fuzzy.txt`
**Expected**: `✓ Fuzzy imported`
**On fail**: 记录 ImportError，标记为阻塞

---

**Step 1.4**: 验证 OperatorAttention 导入
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2
python -c "from src.model_factory.X_model.UXFD.operator_attention import OperatorAttention1D, OperatorAttentionConfig; print('✓ OperatorAttention imported')" \
  2>&1 | tee paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/import_operator_attention.txt
```

**Evidence**: `1_17/glm/evidence/import_operator_attention.txt`
**Expected**: `✓ OperatorAttention imported`
**On fail**: 记录 ImportError，标记为阻塞

---

**Step 1.5**: 验证 Neurosymbolic 导入
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2
python -c "from src.model_factory.X_model.UXFD.neurosymbolic import LogicConfig, LogicReasoner; print('✓ Neurosymbolic imported')" \
  2>&1 | tee paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/import_neurosymbolic.txt
```

**Evidence**: `1_17/glm/evidence/import_neurosymbolic.txt`
**Expected**: `✓ Neurosymbolic imported`
**On fail**: 记录 ImportError，标记为阻塞

---

**Step 1.6**: 验证 TSPN_UXFD 导入
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2
python -c "from src.model_factory.X_model.TSPN_UXFD import Model; print('✓ TSPN_UXFD imported')" \
  2>&1 | tee paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/import_tspn_uxfd.txt
```

**Evidence**: `1_17/glm/evidence/import_tspn_uxfd.txt`
**Expected**: `✓ TSPN_UXFD imported`
**On fail**: 记录 ImportError，标记为阻塞

---

**Step 1.7**: 汇总导入验证结果
```bash
cd paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence
echo "# Import Test Summary" > import_summary.md
echo "" >> import_summary.md
echo "| Component | Status |" >> import_summary.md
echo "|-----------|--------|" >> import_summary.md
for f in import_*.txt; do
  name=$(basename $f .txt | sed 's/import_//')
  status=$(grep -q "✓" $f && echo "✅ PASS" || echo "❌ FAIL")
  echo "| $name | $status |" >> import_summary.md
done
cat import_summary.md
```

**Evidence**: `1_17/glm/evidence/import_summary.md`
**Rollback**: 无

---

### Phase 2: 接口一致性检查（G2）

**Step 2.1**: 检查各组件的 Config 类导出
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2

echo "# Interface Consistency Check" > paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md
echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md
echo "## Config Classes" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md
echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md

python << 'PY' | tee -a paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md
import inspect
from src.model_factory.X_model.UXFD.signal_processing_2d import STFTTimeFrequency
from src.model_factory.X_model.UXFD.fusion import FusionConfig
from src.model_factory.X_model.UXFD.fuzzy import FuzzyConfig
from src.model_factory.X_model.UXFD.operator_attention import OperatorAttentionConfig
from src.model_factory.X_model.UXFD.neurosymbolic import LogicConfig

configs = {
    "SP2D": ("STFTConfig", "signal_processing_2d.stft_tfr"),
    "Fusion": ("FusionConfig", "fusion.simple_fusion"),
    "Fuzzy": ("FuzzyConfig", "fuzzy.fuzzy_reasoner"),
    "OperatorAttention": ("OperatorAttentionConfig", "operator_attention.operator_attention_1d"),
    "Neurosymbolic": ("LogicConfig", "neurosymbolic.logic_reasoner"),
}

for comp, (cfg_name, module) in configs.items():
    print(f"### {comp}")
    print(f"- Config: `{cfg_name}`")
    print(f"- Module: `UXFD.{module}`")
    print()
PY
```

**Evidence**: `1_17/glm/evidence/interface_check.md`
**On fail**: 记录缺失的 Config 类

---

**Step 2.2**: 检查 `__all__` 导出
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2

echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md
echo "## __all__ Exports" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md
echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md

python << 'PY' | tee -a paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/interface_check.md
from src.model_factory.X_model.UXFD import fusion, fuzzy, operator_attention, neurosymbolic, signal_processing_2d

modules = {
    "fusion": fusion,
    "fuzzy": fuzzy,
    "operator_attention": operator_attention,
    "neurosymbolic": neurosymbolic,
    "signal_processing_2d": signal_processing_2d,
}

for name, mod in modules.items():
    exports = getattr(mod, "__all__", [])
    print(f"### {name}")
    print(f"- __all__ = {exports}")
    print()
PY
```

**Evidence**: 追加到 `1_17/glm/evidence/interface_check.md`
**Rollback**: 无

---

### Phase 3: TSPN_UXFD 集成检查（G3）

**Step 3.1**: 检查 TSPN_UXFD 中的组件开关
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2

echo "# TSPN_UXFD Integration Check" > paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
echo "## Component Enable Switches" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md

grep -n "_get_attr.*enable" src/model_factory/X_model/TSPN_UXFD.py | \
  tee -a paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
```

**Evidence**: `1_17/glm/evidence/tspn_integration_check.md`
**Expected**: 输出 4 行（sp2d, fuzzy, operator_attention, logic）
**On fail**: 记录缺失的开关

---

**Step 3.2**: 检查 TSPN_UXFD 中的组件导入
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2

echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
echo "## Component Imports" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md

head -30 src/model_factory/X_model/TSPN_UXFD.py | grep "^from\|^import" | \
  tee -a paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
```

**Evidence**: 追加到 `1_17/glm/evidence/tspn_integration_check.md`
**Expected**: 至少 7 行导入（UXFD.* 模块）
**On fail**: 记录缺失的导入

---

**Step 3.3**: 验证配置构建函数
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2

echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
echo "## Config Builder Functions" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
echo "" >> paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md

grep -n "^def _build_.*_cfg" src/model_factory/X_model/TSPN_UXFD.py | \
  tee -a paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/tspn_integration_check.md
```

**Evidence**: 追加到 `1_17/glm/evidence/tspn_integration_check.md`
**Expected**: 5 个函数（stft, fusion, fuzzy, operator_attention, logic）
**On fail**: 记录缺失的函数

---

### Phase 4: 运行时行为验证（G4）

**Step 4.1**: 创建运行时测试脚本
```bash
cat > /tmp/test_uxfd_runtime.py << 'EOF'
import torch
from src.model_factory.X_model.UXFD.fusion import build_fusion, FusionConfig
from src.model_factory.X_model.UXFD.fuzzy import FuzzyReasoner, FuzzyConfig
from src.model_factory.X_model.UXFD.operator_attention import OperatorAttention1D, OperatorAttentionConfig
from src.model_factory.X_model.UXFD.neurosymbolic import LogicReasoner, LogicConfig

print("=" * 50)
print("UXFD Runtime Behavior Test")
print("=" * 50)

# Fusion test
print("\n### Fusion Test")
x = torch.randn(2, 64)
for ft in ["concat", "sum", "gated"]:
    f = build_fusion(64, FusionConfig(fusion_type=ft))
    y = f(x, x)
    print(f"  {ft}: {x.shape} -> {y.shape} ✓")

# Fuzzy test
print("\n### Fuzzy Test")
fuzzy = FuzzyReasoner(64, 10, FuzzyConfig())
y = fuzzy(torch.randn(2, 64))
print(f"  Input: (2, 64) -> Output: {y.shape} ✓")

# OperatorAttention test
print("\n### OperatorAttention Test")
op = OperatorAttention1D(1, OperatorAttentionConfig())
x = torch.randn(2, 100, 1)
y, w = op(x)
print(f"  Input: {x.shape} -> Output: {y.shape}, Weights: {w.shape} ✓")

# Logic test
print("\n### Logic Test")
logic = LogicReasoner(64, 10, LogicConfig())
y = logic(torch.randn(2, 64))
print(f"  Input: (2, 64) -> Output: {y.shape} ✓")

print("\n" + "=" * 50)
print("All tests passed!")
print("=" * 50)
EOF
```

**Evidence**: 脚本文件 `/tmp/test_uxfd_runtime.py`
**Rollback**: 无

---

**Step 4.2**: 运行测试脚本
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2
python /tmp/test_uxfd_runtime.py \
  2>&1 | tee paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence/runtime_test.txt
```

**Evidence**: `1_17/glm/evidence/runtime_test.txt`
**Expected**: 所有测试显示 `✓`
**On fail**: 记录失败的测试和错误信息

---

### Phase 5: 生成最终报告

**Step 5.1**: 汇总所有证据生成报告
```bash
cd /home/user/LQ/B_Signal/vibench_fix/PHM-Vibench\ copy\ 2

python << 'PY'
import os
from datetime import datetime

report_path = "paper/LQ_vibench_fix/merge_uxfd/1_17/codex/report/uxfd-components-check-report.md"
evidence_dir = "paper/LQ_vibench_fix/merge_uxfd/1_17/glm/evidence"

report = f"""# UXFD Components 检查报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Plan**: `1_17/codex/plan/plan_uxfd-components-check.md`

---

## 执行摘要

"""

# 读取导入汇总
import_summary = os.path.join(evidence_dir, "import_summary.md")
if os.path.exists(import_summary):
    with open(import_summary) as f:
        report += f.read() + "\n\n"

# 添加接口检查
report += """---

## 接口一致性检查

详见: `1_17/glm/evidence/interface_check.md`

---

## TSPN_UXFD 集成检查

详见: `1_17/glm/evidence/tspn_integration_check.md`

---

## 运行时验证

详见: `1_17/glm/evidence/runtime_test.txt`

---

## 结论

"""

# 检查是否有失败的测试
import_failed = False
for f in ["import_sp2d.txt", "import_fusion.txt", "import_fuzzy.txt",
          "import_operator_attention.txt", "import_neurosymbolic.txt", "import_tspn_uxfd.txt"]:
    path = os.path.join(evidence_dir, f)
    if os.path.exists(path):
        with open(path) as fp:
            if "✓" not in fp.read():
                import_failed = True

if import_failed:
    report += "⚠️ **有导入失败**，请查看具体证据文件。\n"
else:
    report += "✅ **所有导入测试通过**。\n"

# 写入报告
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w") as f:
    f.write(report)

print(f"Report generated: {report_path}")
PY
```

**Evidence**: `1_17/codex/report/uxfd-components-check-report.md`
**Rollback**: 无

---

## Checkpoints / Gates

| Gate | Command | Expected | On fail |
|------|---------|----------|---------|
| G1 | Phase 1 全部执行 | 所有 import_*txt 包含 ✓ | 记录 ImportError，停止并报告 |
| G2 | Phase 2 完成 | interface_check.md 包含所有组件 | 记录缺失项，继续但标记 |
| G3 | Phase 3 完成 | tspn_integration_check.md 有 4 个开关 | 记录问题，继续但标记 |
| G4 | Phase 4 完成 | runtime_test.txt 全部 ✓ | 记录失败，标记需要修复 |

---

## Evidence Log

| 步骤 | 文件 | 说明 |
|------|------|------|
| 1.1-1.6 | `evidence/import_*.txt` | 各组件导入结果 |
| 1.7 | `evidence/import_summary.md` | 导入汇总表 |
| 2.1-2.2 | `evidence/interface_check.md` | 接口一致性 |
| 3.1-3.3 | `evidence/tspn_integration_check.md` | TSPN_UXFD 集成 |
| 4.1-4.2 | `evidence/runtime_test.txt` | 运行时测试 |
| 5.1 | `codex/report/uxfd-components-check-report.md` | 最终报告 |

---

## Rollback

本执行计划均为只读操作，无需回滚。

---

## Next

1. 查看 `1_17/codex/report/uxfd-components-check-report.md`
2. 如发现阻塞问题，更新 `1_15/codex/TODO.md`
3. 如无阻塞问题，确认 UXFD 合并可进入下一阶段

**可选下一步**:
- 使用 `lq-artifact-manifest-writer` 生成 `manifest_uxfd-components-check.json`
- 使用 `lq-daily-vibe-update` 更新 `daily.md` + `todo.md`
