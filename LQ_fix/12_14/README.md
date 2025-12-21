# PHM-Vibench Bug识别项目 (2025-12-14/15)

## 项目说明
本目录包含PHM-Vibench项目的Bug识别和文档化工作。GLM（Granular Level Manual）框架已迁移至 `12_15/glm/`。

## 📍 重要更新
GLM框架已迁移到新位置：[`../12_15/glm/`](../12_15/glm/)

## 快速导航

### 🎯 核心文档（在12_15）
- [GLM核心文档](../12_15/glm/00_CORE_DOCUMENT.md) - 项目总览和导航
- [TODO状态追踪](../12_15/glm/TODO_STATUS.md) - 待办事项状态
- [文档兼容性报告](../12_15/glm/DOCS_COMPATIBILITY.md) - 兼容性问题汇总

### 📋 Bug文档（本目录）
- [BUGS.md](BUGS.md) - Bug总览
- [BUG_INDEX.md](BUG_INDEX.md) - Bug索引
- [BUG_TEMPLATES.md](bugs/BUG_TEMPLATES.md) - Bug模板

### 🔍 模块Bug详情
- [data_factory](bugs/data_factory.md) - 4个已记录Bug
- [configuration](bugs/configuration.md) - 配置系统Bug
- [model_factory](bugs/model_factory.md) - 待完成
- [task_factory](bugs/task_factory.md) - 待完成
- [trainer_factory](bugs/trainer_factory.md) - 待完成
- [pipelines](bugs/pipelines.md) - 待完成
- [utils](bugs/utils.md) - 待完成
- [docs](bugs/docs.md) - 待完成

### 📊 报告
- [BUG_SUMMARY](bugs/reports/BUG_SUMMARY.md) - 分析报告
- [快速Triage报告](bugs/reports/quick_triage_report.md) - 分析报告
- [扫描日志](bugs/reports/scan_logs/) - 原始扫描输出

## 目录结构
```
docs/LQ_fix/
├── 12_14/                       # 本目录
│   ├── README.md                 # 本文件
│   ├── BUGS.md                   # Bug总览
│   ├── BUG_INDEX.md              # Bug索引
│   ├── bugs/                     # Bug详情
│   │   ├── BUG_TEMPLATES.md      # 模板
│   │   ├── data_factory.md       # ✅ 已完成
│   │   ├── configuration.md      # ✅ 已完成
│   │   └── reports/              # 报告
│   │       └── scan_logs/        # 扫描日志
│   └── codex/                    # 保留的codex部分
├── 12_15/                        # 新位置
│   └── glm/                      # GLM框架（从12_14迁移）
│       ├── 00_CORE_DOCUMENT.md   # 核心文档
│       ├── TODO_STATUS.md        # TODO追踪
│       ├── DOCS_COMPATIBILITY.md # 兼容性报告
│       ├── 01-04_*.md           # GLM流程文档
│       └── archive/              # 旧计划归档
```

## 当前进度

### ✅ 已完成（12_14）
- [x] Bug扫描（1266个潜在问题）
- [x] P0级Bug识别（7个）
- [x] data_factory模块Bug记录（4个）
- [x] 配置系统Bug记录
- [x] 扫描报告生成

### ✅ 已完成（12_15）
- [x] 文档兼容性检查
- [x] 6个demo配置验证
- [x] TODO/FIXME/HACK条目整理（43项）
- [x] GLM框架迁移

### 🔄 进行中
- [ ] 剩余模块Bug记录
- [ ] 文档兼容性问题修复

## 统计数据

### Bug分布
- **P0**: 7个（裸except语句）
- **P1**: 238个（异常处理、配置问题）
- **P2**: 420个（代码质量）
- **P3**: 601个（文档、优化）

### 已建档
- **总Bug数**: 1266
- **已记录**: 11个（7个P0 + 4个P1）
- **待记录**: 1255个

## 重要说明
- **Git分支**: `lqfix_25-12`
- **项目范围**: 仅进行Bug识别和文档化，不修复代码
- **工具链**: ripgrep, Python静态分析
- **框架**: GLM (Granular Level Manual)

## 相关链接
- [项目根目录](../../../README.md)
- [12_15工作文档](../12_15/codex/)
- [原始计划归档](../12_15/glm/archive/)

---

*最后更新: 2025-12-15*