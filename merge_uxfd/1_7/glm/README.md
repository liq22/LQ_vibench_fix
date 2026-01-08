# GLM 1_7 - UXFD Paper 合并任务分解

**目的**: 将 7 个 UXFD Paper 的合并任务拆分为可独立确认的原子问题，便于逐项执行和追踪。

**使用方式**:
- 每个问题独立成文件，包含：背景 → 子任务分解 → 选项 → 验收标准
- 确认后填写 `DECISION.md` 汇总结论

**问题分类**:
- [01_fusion/](01_fusion/) - 📘 1D-2D_fusion_explainable (3个问题)
- [02_toolkit/](02_toolkit/) - 🟢 Explainable_FD_Toolkit (3个问题)
- [03_llm_toolkit/](03_llm_toolkit/) - 🟣 LLM_Explainable_FD_Toolkit (3个问题)
- [04_moe/](04_moe/) - 🟠 MOE_explainable (3个问题)
- [05_fuzzy/](05_fuzzy/) - 🩷 Paper_fuzzy_XFD (3个问题)
- [06_neuro_symbolic/](06_neuro_symbolic/) - 🟦 Neuralsymbolic_theory (3个问题)
- [07_operator_attention/](07_operator_attention/) - 🔴 TII_operator_attention (3个问题)

---

## 问题索引

| ID | 问题 | 所属 Paper | 优先级 | 状态 |
|----|------|-----------|--------|------|
| F001 | 2D 时频转换组件移植 | 1D-2D_fusion | P0 | 待确认 |
| F002 | 1D↔2D 融合模块移植 | 1D-2D_fusion | P0 | 待确认 |
| F003 | 三层对齐机制实现 | 1D-2D_fusion | P1 | 待确认 |
| T001 | 统一可解释性 API 设计 | Explainable_FD_Toolkit | P0 | 待确认 |
| T002 | 评估指标协议实现 | Explainable_FD_Toolkit | P1 | 待确认 |
| T003 | 模型适配器实现 | Explainable_FD_Toolkit | P1 | 待确认 |
| L001 | 结构化解释→自然语言映射 | LLM_Explainable_FD_Toolkit | P1 | 待确认 |
| L002 | 对话系统实现 | LLM_Explainable_FD_Toolkit | P2 | 待确认 |
| L003 | 幻觉防护机制 | LLM_Explainable_FD_Toolkit | P1 | 待确认 |
| M001 | 统计特征驱动路由移植 | MOE_explainable | P1 | 待确认 |
| M002 | 专家激活分析实现 | MOE_explainable | P2 | 待确认 |
| M003 | 路径签名生成实现 | MOE_explainable | P2 | 待确认 |
| Z001 | 模糊规则库构建 | Paper_fuzzy_XFD | P1 | 待确认 |
| Z002 | 模糊推理引擎移植 | Paper_fuzzy_XFD | P1 | 待确认 |
| Z003 | 神经-模糊融合实现 | Paper_fuzzy_XFD | P2 | 待确认 |
| S001 | 四层架构验证 | Neuralsymbolic_theory | P1 | 待确认 |
| S002 | 神经-符号约束实现 | Neuralsymbolic_theory | P2 | 待确认 |
| S003 | 评估体系实现 | Neuralsymbolic_theory | P2 | 待确认 |
| O001 | 算子空间理论验证 | TII_operator_attention | P1 | 待确认 |
| O002 | 物理约束注意力实现 | TII_operator_attention | P2 | 待确认 |
| O003 | 可解释性度量实现 | TII_operator_attention | P2 | 待确认 |

---

## 执行顺序（推荐）

### Wave 1: 基础设施（无依赖，可并行）
- F001, T001, M001, Z001, S001, O001

### Wave 2: 核心功能（Wave 1 依赖）
- F002, T002, T003, L001, M002, Z002, S002, O002

### Wave 3: 集成与验证（Wave 2 依赖）
- F003, L002, L003, M003, Z003, S003, O003

---

## 依赖关系图

```
F001 → F002 → F003
T001 → T002
T001 → T003 → L001 → L002/L003
M001 → M002/M003
Z001 → Z002 → Z003
S001 → S002/S003
O001 → O002 → O003
```

---

## 决策记录

确认后的结论将汇总到 `DECISION.md`。
