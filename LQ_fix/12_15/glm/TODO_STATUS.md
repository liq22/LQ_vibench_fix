# TODO状态追踪 - 2025-12-14/15

## 12_14 已完成 ✅

### 扫描和分析
- [x] 自动化扫描执行（rg命令）
- [x] 扫描结果分类和统计
- [x] P0级bug识别和建档（7个）
- [x] 快速triage分析报告生成
- [x] data_factory模块bug记录（4个）

### 文档建设
- [x] BUG_SUMMARY报告生成
- [x] BUG_INDEX索引创建
- [x] GLM框架建立
- [x] Bug建档模板创建

## 12_15 已完成 ✅

### 文档兼容性检查
- [x] 文档路径一致性检查
- [x] 6个demo配置验证
- [x] CLI参数匹配性检查

### TODO条目整理
- [x] TODO/FIXME/HACK条目整理（43项）
  - Python: 38项
  - YAML: 5项
- [x] 问题分析与任务定义
- [x] 文档兼容性修复计划制定

## 进行中的TODO 🚧

### 高优先级
- [ ] 文档兼容性问题修复（P0级路径问题）
  - [ ] 修正 `AGENTS.md` 中的脚本路径
  - [ ] 统一 demo 配置与描述
  - [ ] 修复 CLI 参数示例
- [ ] 完善P0级bug文档细节
  - [ ] 添加具体修复建议
  - [ ] 评估影响范围

### 中优先级
- [ ] 手动审查剩余模块（5个）
  - [ ] model_factory 模块
  - [ ] task_factory 模块
  - [ ] trainer_factory 模块
  - [ ] utils 模块
  - [ ] pipelines 模块

## 待完成的TODO 📋

### Bug修复相关
- [ ] **P0级修复**（阻塞性问题）
  - [ ] 修复7个裸except语句
    - src/data_factory/data_factory.py:12
    - src/data_factory/data_factory.py:387
    - src/data_factory/samplers/del/ID_selector.py:1
    - src/data_factory/reader/RM_025_KAIST.py:1
    - src/data_factory/reader/RM_026_HUST23.py:1
    - src/data_factory/samplers/FS_sampler.py:264
    - src/model_factory/X_model/Signal_processing.py:158
  - [ ] 修复导入错误路径
  - [ ] 统一异常处理模式

- [ ] **P1级修复**（重要问题）
  - [ ] 修正过度宽泛的异常捕获
  - [ ] 改进错误消息
  - [ ] 添加缺失的异常处理

### 文档兼容性修复
- [ ] **路径问题**
  - [ ] 更新所有 `configs/demo/Single_DG/...` 引用
  - [ ] 统一脚本路径（`scripts/` → `dev/scripts/`）
  - [ ] 修正大小写问题（`README.md` vs `readme.md`）
  - [ ] 更新CLI参数示例（移除`--pipeline`）

- [ ] **Demo配置问题**
  - [ ] Demo #1: 修正"CWRU → Ottawa"描述或配置
  - [ ] Demo #2: 修正"multi-system"配置
  - [ ] 添加dataset_id映射说明

### TODO/FIXME/HACK处理（43项）
- [ ] **高优先级项**（影响功能）
  - [ ] TSPN.py中的6个TODO（逻辑实现）
  - [ ] E_02_HSE_rec.py中的5个TODO（重构功能）
  - [ ] 各ISFM模型的prediction任务处理

- [ ] **中优先级项**（代码质量）
  - [ ] 信号处理模块TODO项
  - [ ] 数据集采样器TODO项
  - [ ] 配置文件中的TODO项

- [ ] **低优先级项**（优化建议）
  - [ ] 代码注释完善
  - [ ] 性能优化TODO
  - [ ] 文档补充TODO

## Bug文档完善

### 待创建的模块文档
- [ ] [`../12_14/bugs/model_factory.md`](../12_14/bugs/model_factory.md)
- [ ] [`../12_14/bugs/task_factory.md`](../12_14/bugs/task_factory.md)
- [ ] [`../12_14/bugs/trainer_factory.md`](../12_14/bugs/trainer_factory.md)
- [ ] [`../12_14/bugs/pipelines.md`](../12_14/bugs/pipelines.md)
- [ ] [`../12_14/bugs/utils.md`](../12_14/bugs/utils.md)
- [ ] [`../12_14/bugs/docs.md`](../12_14/bugs/docs.md)

### 需要更新的文档
- [ ] 更新 [`../12_14/BUGS.md`](../12_14/BUGS.md) 添加新发现
- [ ] 更新 [`../12_14/BUG_INDEX.md`](../12_14/BUG_INDEX.md) 添加新条目
- [ ] 完善 [`BUG_TEMPLATES.md`](../12_14/bugs/BUG_TEMPLATES.md) 使用说明

## 持续改进项

### 自动化
- [ ] 添加pre-commit hooks检查裸except
- [ ] 集成更多静态分析工具
- [ ] 建立CI/CD中的bug扫描流程

### 流程优化
- [ ] 制定bug修复优先级标准
- [ ] 建立定期扫描机制
- [ ] 创建bug修复跟踪模板

## 数据统计

### Bug分布（按优先级）
- **P0**: 7个（0.55%）- 需要立即修复
- **P1**: 238个（18.8%）- 高优先级
- **P2**: 420个（33.2%）- 中等优先级
- **P3**: 601个（47.5%）- 低优先级/建议

### TODO分布（按模块）
- **model_factory**: 13项
  - TSPN.py: 6项
  - Signal_processing.py: 4项
  - 其他: 3项
- **ISFM模块**: 8项
  - M_01/M_02/M_03: 各2项
  - E_02_HSE_rec.py: 5项
- **data_factory**: 7项
  - data_factory.py: 3项
  - 其他文件: 4项
- **其他模块**: 15项

## 决策点

### 需要确认的问题
1. **Demo描述策略**
   - [ ] 选择策略A：修改文档描述（推荐）
   - [ ] 选择策略B：修改配置以匹配描述

2. **异常处理标准**
   - [ ] 定义具体的异常类型使用规范
   - [ ] 确定是否需要统一的异常处理装饰器

3. **TODO清理策略**
   - [ ] 设定TODO清理时间线
   - [ ] 确定保留/删除标准

---

**更新频率**: 每日更新
**下次更新**: 2025-12-16
**负责人**: @liq22