# N001: UXFD → UXFD_component/ 是否重命名

**分类**: 命名与目录结构 | **优先级**: P1 | **依赖**: 无

---

## 背景

### 现状
- 代码当前已有：`src/model_factory/X_model/UXFD/`
- 12_23 README 提到未来"组件区统一命名为 `src/model_factory/X_model/UXFD_component/`"
- 参考文档：`paper/LQ_vibench_fix/merge_uxfd/12_23/README.md`

### 提出重命名的原因
- `UXFD_component/` 名称更能体现"组件集合"的语义
- 与 `UXFD/`（原始论文代码）做区分，避免混淆

---

## 选项

### 选项 A: 保持 `UXFD/` 不动（推荐 ★）

**实施**:
- 目录名保持：`src/model_factory/X_model/UXFD/`
- 新增组件继续放入此目录

**优点**:
- KISS 原则，避免 rename 引入的工程工作
- 不影响现有 import/registry/文档

**缺点**:
- 目录名语义不够精确（"组件集合" vs "原论文代码"）

---

### 选项 B: 执行 UXFD → UXFD_component/ 重命名

**实施**:
1. 目录重命名：`UXFD/` → `UXFD_component/`
2. 批量更新 import 语句
3. 更新 registry 注册表
4. 更新文档中的路径引用

**优点**:
- 命名更清晰，语义更准确

**缺点**:
- 工程工作量大（import/registry/文档 需同步更新）
- 增加 merge conflict 风险

---

## 影响分析

| 方面 | 选项 A (保持) | 选项 B (重命名) |
|------|-------------|----------------|
| 工程量 | 无 | 中等 |
| 风险 | 低 | 中等 |
| 语义清晰度 | 一般 | 高 |

---

## 建议

**推荐选项 A**：保持 `UXFD/` 不动

**理由**:
1. 当前阶段重点是 WP0（跑通 pilot），不应被目录命名阻塞
2. `UXFD/` 虽然不够精确，但已在使用，理解成本可接受
3. 如确需重命名，可在 WP0 完成后作为独立任务处理

---

## 确认

- [ ] 选项 A - 保持 `UXFD/`
- [ ] 选项 B - 重命名为 `UXFD_component/`

**结论**: _____ (待填写)

**备注**: _____
