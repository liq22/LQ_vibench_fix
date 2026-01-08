# A001: figures/ 统一输出目录

**分类**: 产物与输出 | **优先级**: P1 | **依赖**: 无

---

## 背景

### 当前状态
- post-run 脚本：`scripts/uxfd_postrun.py`
- 绘图输出默认：`<run_dir>/figures/`
- 审计输出：`<run_dir>/artifacts/plots/plot_eligibility.json`

### 参考文档
`paper/LQ_vibench_fix/merge_uxfd/12_23/plot_factory_migration_plan.md`

---

## 问题

是否将 `figures/` 作为统一的绘图输出目录？

---

## 选项

### 选项 A: 保持 `<run_dir>/figures/`（推荐 ★）

**结构**:
```
<run_dir>/
├── artifacts/
│   ├── manifest.json
│   └── plots/
│       └── plot_eligibility.json
├── figures/
│   ├── confusion_matrix.png
│   ├── eligibility.png
│   └── ...
└── checkpoints/
```

**优点**:
- 图片文件与 JSON 审计文件分离，结构清晰
- 符合"图片放 figures，元数据放 artifacts"的语义

**缺点**:
- 多一个顶层目录

---

### 选项 B: 统一到 `<run_dir>/artifacts/figures/`

**结构**:
```
<run_dir>/
├── artifacts/
│   ├── manifest.json
│   ├── plots/
│   │   └── plot_eligibility.json
│   └── figures/
│       ├── confusion_matrix.png
│       └── ...
└── checkpoints/
```

**优点**:
- 所有产物集中在 `artifacts/` 下

**缺点**:
- 需要修改 `scripts/uxfd_postrun.py` 的默认输出路径
- 可能影响现有 run 的兼容性

---

## 影响分析

| 方面 | 选项 A | 选项 B |
|------|--------|--------|
| 路径修改 | 无 | 需要 |
| 语义清晰度 | 高 | 中等 |
| 兼容性 | 保持当前 | 需调整 |

---

## 建议

**推荐选项 A**：保持 `<run_dir>/figures/`

**理由**:
1. 当前脚本已按此设计，修改成本 > 收益
2. figures/ 与 artifacts/ 分离符合常见惯例（图片 vs 元数据）

---

## 确认

- [ ] 选项 A - 保持 `<run_dir>/figures/`
- [ ] 选项 B - 统一到 `<run_dir>/artifacts/figures/`

**结论**: _____ (待填写)

**备注**: _____
