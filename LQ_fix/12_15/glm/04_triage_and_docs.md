# 04 Triage & Docs（分级、建档、索引与汇总）

> **状态**: 🔄 部分完成 (2025-12-14/15)

本阶段目标：把"扫描/审查发现的线索"变成可执行的 Bug 列表。

## 1. 建立统一 Bug 模板（写入 `BUG_TEMPLATES.md`）

建议字段（最小集合）：
- Bug ID：`BUG-YYYYMMDD-XXX`
- 标题：一句话描述
- 优先级：P0/P1/P2/P3
- 类型：configuration/data/model/task/trainer/pipelines/perf/docs/other
- 影响范围：哪些 pipeline/任务/数据集会受影响
- 复现步骤：命令 + config + override
- 期望行为 vs 实际行为
- 定位线索：文件路径、函数名、关键日志、异常栈
- 临时绕过：若有
- 状态：open/triaged/verified/fix_planned/won't_fix/fixed

## 2. 新增一个 Bug 的具体操作

1. 在对应模块文件新增条目（例如 `bugs/configuration.md`）
2. 同时在 `BUG_INDEX.md` 增加一条索引（Bug ID → 模块文件）
3. 若为 P0/P1，在 `BUGS.md` 的“优先修复清单”也追加

建议格式（示例）：

```md
## BUG-20251214-001: 标题
- priority: P1
- type: configuration
- status: open
- impact: ...
- repro:
  - command: ...
  - config: ...
  - overrides: ...
- expected: ...
- actual: ...
- notes: ...
```

## 3. 汇总报告（`reports/BUG_SUMMARY.md`）

至少包含：
- 总数统计（按优先级、按模块）
- P0/P1 清单（带短描述）
- 最高风险项的修复建议顺序（先修会阻塞 others 的）
- 复现依赖说明（是否需要本地数据集、GPU、特定环境变量）

## 4. README/文档一致性问题的处理口径

文档类问题允许直接修复（不改变训练/模型逻辑），但仍建议：
- 对每个修复创建一个 `docs` 类型的 Bug 记录（便于回溯）
- 修复后附上验证方法（例如本地链接扫描脚本、命令存在性检查）

## 实际执行结果

### ✅ 已完成工作

1. **Bug模板建立**
   - ✅ 已创建 [`BUG_TEMPLATES.md`](../12_14/bugs/BUG_TEMPLATES.md)
   - 包含完整的Bug记录模板和示例
   - 支持P0-P3优先级分类

2. **Bug建档**
   - ✅ 已创建 [`BUGS.md`](../12_14/BUGS.md) - Bug总览
   - ✅ 已创建 [`BUG_INDEX.md`](../12_14/BUG_INDEX.md) - Bug索引
   - ✅ 已创建 [`data_factory.md`](../12_14/bugs/data_factory.md) - 4个bug详情
   - ✅ 已创建 [`configuration.md`](../12_14/bugs/configuration.md) - 配置系统bug

3. **汇总报告**
   - ✅ 已创建 [`BUG_SUMMARY.md`](../12_14/bugs/reports/BUG_SUMMARY.md)
   - ✅ 已创建 [`quick_triage_report.md`](../12_14/bugs/reports/quick_triage_report.md)
   - 包含统计数据和优先修复建议

4. **扫描日志归档**
   - ✅ 所有rg扫描输出保存在 [`scan_logs/`](../12_14/bugs/reports/scan_logs/)
   - 便于回溯和复查

### 📊 建档统计

| 优先级 | 已建档 | 待建档 |
|-------|-------|-------|
| P0 | 7个 | 0个 |
| P1 | 4个 | 234个 |
| P2 | 0个 | 420个 |
| P3 | 0个 | 601个 |
| **总计** | **11个** | **1255个** |

### 🎯 已建档的Bug

#### P0级（阻塞性问题）
1. **BUG-20251214-001**: 裸except语句 - data_factory.py:12
2. **BUG-20251214-002**: 裸except语句 - FS_sampler.py:264
3. **BUG-20251214-003**: 裸except语句 - Signal_processing.py:158
4. **BUG-20251214-004**: 裸except语句 - ID_selector.py:1
5. **BUG-20251214-005**: 裸except语句 - RM_025_KAIST.py:1
6. **BUG-20251214-006**: 裸except语句 - RM_026_HUST23.py:1
7. **BUG-20251214-007**: 裸except语句 - data_factory.py:387

#### P1级（重要问题）
1. **BUG-20251214-008**: 缺失异常处理 - data_loader函数
2. **BUG-20251214-009**: 缺失异常处理 - get_dataset函数
3. **BUG-20251214-010**: 缺失异常处理 - build_dataloader函数
4. **BUG-20251214-011**: 未处理的子集情况 - data_factory.py

### 📝 建档流程优化

#### 实际使用的流程
1. **快速Triage**: 使用Python脚本分析扫描结果
   ```python
   # scripts/analyze_scan_results.py
   # 自动分类和优先级标记
   ```

2. **批量创建**: 对于相似问题批量创建模板
   - 裸except语句：统一模板
   - 缺失异常处理：统一模板

3. **交叉引用**:
   - BUG_INDEX.md 按优先级排序
   - 模块文档包含具体详情
   - 汇总报告提供全局视图

### 🔄 待完成工作

1. **剩余Bug建档**
   - [ ] model_factory模块Bug（预估200+）
   - [ ] task_factory模块Bug（预估150+）
   - [ ] trainer_factory模块Bug（预估50+）
   - [ ] utils模块Bug（预估100+）
   - [ ] pipelines模块Bug（预估30+）
   - [ ] docs模块Bug（预估200+）

2. **文档兼容性Bug**
   - [ ] Demo路径问题（P0）
   - [ ] CLI参数不匹配（P0）
   - [ ] 配置描述不一致（P1）

### 💡 经验总结

1. **建档策略**
   - P0/P1优先详细建档
   - P2/P3可批量处理
   - 保留原始扫描日志便于复查

2. **模板优化**
   - 添加复现步骤示例
   - 明确影响范围
   - 提供修复建议

3. **效率提升**
   - 自动化脚本辅助分析
   - 模板化快速录入
   - 分类汇总减少重复

