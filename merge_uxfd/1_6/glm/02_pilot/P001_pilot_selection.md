# P001: pilot paper 选择

**分类**: pilot 配置 | **优先级**: P0 | **依赖**: 无

---

## 背景

### WP0 目标
选择一篇 pilot paper，作为 UXFD merge 的第一个验证目标，跑通最小配置（`min.yaml` + 1 epoch）。

### 候选来源
`paper/UXFD_paper/` 下的 submodule 列表（从 `.gitmodules` 获取）

---

## 选项

### 选项 A: `1D-2D_fusion_explainable`（推荐 ★）

**特征**:
- 涉及 1D + 2D 融合
- 包含可解释性组件

**组件需求预估**:
- `Signal_processing_2D.py` - 2D 时频转换
- `Fusion1D2D*.py` - 1D↔2D 融合
- explainer 相关组件

**优点**:
- 功能覆盖全面，能验证 WP1 组件移植的完整性
- 是建议的默认 pilot（见 12_23 文档）

**缺点**:
- 组件依赖较多，WP1 工作量较大

---

### 选项 B: 其他 pilot（请指定）

**候选**:
- `Explainable_FD_Toolkit`
- `LLM_Explainable_FD_Toolkit`
- `MOE_explainable`
- `Paper_fuzzy_XFD`
- `TII_operator_attention`

**需要评估**:
- 该 pilot 的最小组件依赖是什么？
- 是否有现成的配置文件可作为 `min.yaml` 基础？

---

## 影响分析

| 方面 | 选项 A | 选项 B |
|------|--------|--------|
| WP0 复杂度 | 中等 | 取决于选择 |
| WP1 组件覆盖 | 全面（2D+fusion+explain） | 取决于选择 |
| 验证完整性 | 高 | 取决于选择 |

---

## 建议

**推荐选项 A**：`1D-2D_fusion_explainable`

**理由**:
1. 文档中已作为建议默认 pilot
2. 功能覆盖全面，能充分验证 Copy+Adapter 策略
3. 融合场景是 UXFD 的核心应用场景

---

## 确认

- [ ] 选项 A - `1D-2D_fusion_explainable`
- [ ] 选项 B - _____ (请填写)

**结论**: _____ (待填写)

**备注**: 如选 B，需补充说明该 pilot 的最小组件依赖。
