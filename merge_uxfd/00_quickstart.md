# UXFD 快速开始（30 分钟指南）

**目标**: 将 UXFD 上游合并到 PHM-Vibench，实现配置优先的可复现性。
**边界**: 7 篇 paper → submodule（个性化配置），可复用代码 → 主仓库（通用能力）。

---

## 30 秒快速检查

你是否需要：
- [ ] 只了解 UXFD 是什么 → 读 "What/Why"
- [ ] 快速验证环境 → 读 "How: 3 个命令"
- [ ] 实际迁移代码 → 读 [01_porting_playbook.md](01_porting_playbook.md)
- [ ] 查看待决决策 → 读 [12_27/codex/DECISIONS_NEEDED.md](12_27/codex/DECISIONS_NEEDED.md)

---

## Where: 路径映射

```bash
# 设置环境变量（替代硬编码路径）
export UXFD_UPSTREAM=/home/user/LQ/B_Signal/Unified_X_fault_diagnosis
export VIBENCH_ROOT=$(pwd)  # PHM-Vibench 根目录

# 上游 → 目标映射：
$UXFD_UPSTREAM/model/Signal_processing.py    → src/model_factory/X_model/UXFD/signal_processing_1d/
$UXFD_UPSTREAM/model/Signal_processing_2D.py → src/model_factory/X_model/UXFD/signal_processing_2d/
$UXFD_UPSTREAM/model/Fusion1D2D*.py          → src/model_factory/X_model/UXFD/fusion/
$UXFD_UPSTREAM/model/FuzzyLogic*.py          → src/model_factory/X_model/UXFD/fuzzy/
$UXFD_UPSTREAM/model/operator_attention*.py  → src/model_factory/X_model/UXFD/operator_attention/
$UXFD_UPSTREAM/model/TSPN*.py                → src/model_factory/X_model/UXFD/tspn/
```

---

## How: 最小可跑（3 个命令）

### 1. 预检查（必须先通过）

```bash
# 烟雾测试：验证环境正常
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
```

**预期输出**: 训练运行完成，无错误。

---

### 2. （可选）运行 Pilot（1 个 epoch 快速验证）

```bash
# 注意：当前仓库的 WP0 尚未补齐（多数 submodule 内还没有 configs/vibench/min.yaml）。
# 当某个 paper submodule 提供了 min.yaml 后，再用下面命令跑 pilot：
python main.py --config paper/UXFD_paper/<paper_id>/configs/vibench/min.yaml --override trainer.num_epochs=1
```

**预期输出**:
- 训练完成 1 个 epoch
- 输出目录包含 `artifacts/` 子目录

---

### 3. 检查产物

```bash
# 方式 A：用 collect 脚本做“闭环验证”（推荐）
python -m scripts.collect_uxfd_runs --input results --out_dir reports
ls -la reports/uxfd_runs.csv

# 方式 B：直接查找最近写出的 manifest.json（不依赖固定 run_dir 名称）
find results save -path "*/artifacts/manifest.json" -print 2>/dev/null | tail -n 5
```

**预期输出**: `reports/uxfd_runs.csv` 存在，且能找到至少 1 个 `artifacts/manifest.json`。

---

## Troubleshooting: 决策树

```
报错
 ├─ 有 "shape" 或 "layout" → 检查 `src/model_factory/X_model/UXFD/**` 下的布局约定/适配器
 ├─ 有 "ImportError" → 运行 python -m scripts.config_inspect --config <yaml>
 ├─ 有 "ModuleNotFoundError" → git submodule update --init --recursive
 └─ 其他 → 查阅 [01_porting_playbook.md](01_porting_playbook.md)
```

**详细对照表**：

| 症状 | 可能原因 | 修复方法 |
|------|----------|----------|
| `Shape 错误 (BLC vs BCL)` | 张量布局不匹配 | 检查 `src/model_factory/X_model/UXFD/**` 的布局约定/适配器 |
| `FFT magnitude 缺失` | 绘图时复数无法显示 | 使用 `Signal_processing_2D` 的 `magnitude_only=True` |
| `ImportError: No module named` | 模块未正确注册 | 运行 `python -m scripts.config_inspect --config <yaml>` |
| `Registry 找不到` | 模型未在 registry 中注册 | 检查 `src/model_factory/model_registry.csv` |
| `ModuleNotFoundError` | submodule 未初始化 | 运行 `git submodule update --init --recursive` |

---

## 核心约束（不可违反）

1. **单一入口不变**: `python main.py --config <yaml> [--override ...]`
2. **5-block 不变**: `environment/data/model/task/trainer`
3. **不新增第 6 个 block**: 扩展开关放在 `trainer.extensions.*`
4. **主仓库 demos/tests 不依赖 paper submodule**: `python main.py --config configs/demo/00_smoke/dummy_dg.yaml` 与 `pytest test/` 应可离线运行（pilot 例外）

---

## 下一步

- **完整迁移指南**: [01_porting_playbook.md](01_porting_playbook.md) - 文件逐个迁移
- **待决决策**: [12_27/codex/DECISIONS_NEEDED.md](12_27/codex/DECISIONS_NEEDED.md) - 需要拍板的事项
- **问题追踪**: [1_7/glm/README.md](1_7/glm/README.md) - 7 篇 paper 的原子任务分解
- **现状 + TODO（SSOT）**: [1_15/codex/TODO.md](1_15/codex/TODO.md)

---

## 7 篇 Paper 列表

> ⚠️ **Submodule 初始化**
>
> 如点击 Paper 链接后出现 404 或目录不存在：
> ```bash
> git submodule update --init --recursive
> ```

| Paper | 说明 | 优先级 |
|-------|------|--------|
| [1D-2D_fusion_explainable](../../UXFD_paper/1D-2D_fusion_explainable) | 1D-2D 融合可解释 | P0 (Pilot) |
| [Explainable_FD_Toolkit](../../UXFD_paper/Explainable_FD_Toolkit) | 可解释故障诊断工具包 | P0 (基础设施) |
| [LLM_Explainable_FD_Toolkit](../../UXFD_paper/LLM_Explainable_FD_Toolkit) | LLM 增强可解释工具包 | P1 |
| [MOE_explainable](../../UXFD_paper/MOE_explainable) | MoE 可解释方法 | P1 |
| [Paper_fuzzy_XFD](../../UXFD_paper/Paper_fuzzy_XFD) | 模糊逻辑可解释 | P1 |
| [Neuralsymbolic_theory](../../UXFD_paper/Neuralsymbolic_theory) | 神经符号理论 | P1 |
| [TII_operator_attention](../../UXFD_paper/TII_operator_attention) | 算子注意力机制 | P1 |
