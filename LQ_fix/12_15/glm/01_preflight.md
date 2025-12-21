# 01 Preflight（开始前检查）

> **状态**: ✅ 已完成 (2025-12-14)

## 1. 确认分支与工作区

```bash
git status --porcelain=v1 -b
git branch --show-current
```

建议：
- 确保在目标分支（例如 `lqfix_25-12`）上执行本计划
- 若工作区已有大量未提交改动，先决定是否要暂存/提交/另开分支，避免扫描输出与修复混在一起

## 2. 生成计划目录结构

```bash
mkdir -p docs/LQ_fix/12_14/{bugs,glm,reports,archive}
```

可选：如果你希望把“扫描输出原始文本”单独保存（便于回溯），可以再建：

```bash
mkdir -p docs/LQ_fix/12_14/reports/scan_logs
```

## 3. 建立基础产出文件（空壳）

```bash
test -f docs/LQ_fix/12_14/BUGS.md || printf "# BUGS\\n\\n" > docs/LQ_fix/12_14/BUGS.md
test -f docs/LQ_fix/12_14/BUG_INDEX.md || printf "# BUG INDEX\\n\\n" > docs/LQ_fix/12_14/BUG_INDEX.md
test -f docs/LQ_fix/12_14/BUG_TEMPLATES.md || printf "# BUG TEMPLATES\\n\\n" > docs/LQ_fix/12_14/BUG_TEMPLATES.md
```

## 实际执行结果

### ✅ 已完成项
1. **分支确认**:
   - 成功切换到 `lqfix_25-12` 分支
   - 工作区干净，无未提交改动

2. **目录结构创建**:
   ```
   docs/LQ_fix/12_14/
   ├── bugs/
   ├── glm/
   ├── reports/
   │   └── scan_logs/
   └── archive/
   ```

3. **基础文件创建**:
   - ✅ BUGS.md - Bug总览文档
   - ✅ BUG_INDEX.md - Bug索引文档
   - ✅ BUG_TEMPLATES.md - Bug模板文档

### 📝 关键发现
- 项目目录结构清晰，便于组织大量Bug发现
- scan_logs目录对保留原始扫描结果很有价值
- 基础文档模板为后续工作提供了良好起点

### 🔄 后续建议
- 类似项目可复用此目录结构
- 建议在开始扫描前再次确认分支状态
```

