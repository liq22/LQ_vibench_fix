# 文档兼容性问题报告

## 概述

本文档汇总了在 `docs/LQ_fix/12_15/codex/` 中发现的文档兼容性问题。这些问题会导致用户按照文档执行时遇到失败或产生误解。

## P0级问题（会导致直接失败）

### 1. 路径引用错误

#### 1.1 Demo路径不匹配
**问题**: 文档中引用了不存在的旧版demo路径
```
错误引用: configs/demo/Single_DG/...
实际位置: configs/v0.0.9/demo/... (旧版)
         configs/demo/... (新版)
```

**影响文件**:
- `README.md`
- `CLAUDE.md`
- `README_CN.md`

#### 1.2 脚本路径错误
**问题**: 脚本路径引用不正确
```
错误引用: python scripts/hse_synthetic_demo.py
实际位置: python dev/scripts/hse_synthetic_demo.py
```

**影响文件**:
- `AGENTS.md`
- `CLAUDE.md`

#### 1.3 大小写不一致
**问题**: 文件名大小写不匹配
```
错误引用: configs/README.md
实际文件: configs/readme.md
```

**影响文件**:
- `README.md`
- 多个配置文档

### 2. CLI参数不匹配

#### 2.1 --pipeline参数不存在
**问题**: 文档中使用`--pipeline`参数，但main.py不支持
```
错误示例: python main.py --pipeline Pipeline_02_pretrain_fewshot
实际用法: python main.py --config config.yaml
          (pipeline在YAML内通过pipeline字段指定)
```

**影响文件**:
- `CLAUDE.md`
- `CLAUDE_CN.md`

### 3. 硬编码路径问题

#### 3.1 PROJECT_HOME路径
**问题**: 配置文件中包含硬编码的绝对路径
```yaml
# configs/base/environment/base.yaml
PROJECT_HOME: /home/user/some/absolute/path  # 会误导用户
```

**影响**: 用户直接使用会因路径不存在而失败

## P1级问题（会导致误解）

### 1. Demo描述与配置不一致

#### 1.1 Demo #1 - "CWRU → Ottawa" 问题
**配置文件**: `configs/demo/01_cross_domain/cwru_dg.yaml`
- **文档描述**: "CWRU → Ottawa 跨域诊断"
- **实际配置**: `target_system_id: [1]`（仅指定了单系统）
- **问题**: 无法从配置本身保证使用Ottawa数据集

**影响**: 用户期望看到跨域结果，实际可能只在单域上运行

#### 1.2 Demo #2 - "multi-system" 问题
**配置文件**: `configs/demo/02_cross_system/multi_system_cddg.yaml`
- **文档描述**: "多系统CDDG"
- **实际配置**: `target_system_id: [1]`（单系统）
- **问题**: 描述与实际不符

**影响**: 用户期望多系统实验，实际只是单系统

### 2. Dataset ID映射不明确

**问题**: 文档中提到的dataset_id映射关系不明确
- 文档中直接使用数据集名称（CWRU, Ottawa等）
- 配置中使用system_id（1, 2, 6等）
- 缺少明确的映射说明

## 具体修复建议

### 1. P0级修复（必须）

#### 1.1 更新路径引用
```markdown
# 需要替换的路径映射
configs/demo/Single_DG/ → configs/demo/01_cross_domain/
configs/demo/Multiple_DG/ → configs/demo/02_cross_system/
scripts/ → dev/scripts/
configs/README.md → configs/readme.md
```

#### 1.2 修正CLI示例
```markdown
# 错误示例
python main.py --pipeline Pipeline_02_pretrain_fewshot

# 正确示例
python main.py --config configs/demo/05_pretrain_fewshot/pretrain_hse_then_fewshot.yaml
```

#### 1.3 处理硬编码路径
- 在文档中添加说明：需要根据实际环境修改`PROJECT_HOME`
- 或改用相对路径/环境变量

### 2. P1级修复（建议）

#### 2.1 Demo描述修正策略

**策略A（推荐）**: 修改文档描述
```markdown
Demo #1: 改为"基于target_system_id的域泛化示例"
Demo #2: 改为"单系统CDDG示例"
```

**策略B**: 修改配置以匹配描述
```yaml
# Demo #1 - 如果确实要做CWRU→Ottawa
task:
  target_system_id: [1, 5]  # 1:CWRU, 5:Ottawa
  source_domain_id: [0, 1, 2]  # CWRU的域
  target_domain_id: [0, 1, 2]  # Ottawa的域
```

#### 2.2 添加Dataset映射说明
```markdown
## Dataset ID映射
- System ID 1: CWRU (Case Western Reserve University)
- System ID 2: XJTU (Xi'an Jiaotong University)
- System ID 5: Ottawa (University of Ottawa)
- System ID 6: THU (Tsinghua University)
- System ID 12: JNU (Jinan University)

*注意：映射关系基于metadata_6_11.xlsx，如有变动请参考最新metadata文件*
```

## 修复优先级和时间线

### 立即修复（P0）
1. 更新所有错误的路径引用
2. 修正CLI参数示例
3. 处理硬编码路径问题

### 短期修复（P1）
1. 统一demo描述与配置
2. 添加dataset映射说明
3. 更新README中的快速开始示例

### 长期改进
1. 建立文档一致性检查流程
2. 添加自动化测试验证文档示例
3. 创建文档更新检查清单

## 影响评估

### 用户影响
- **P0问题**: 直接导致用户无法运行示例，影响初体验
- **P1问题**: 导致运行结果与预期不符，影响实验可信度

### 维护影响
- 不一致的文档增加了支持成本
- 错误示例会导致重复的问题报告

## 相关资源

- [原始检查报告](../codex/README_COMPAT_PLAN.md)
- [Demo配置检查](../codex/DEMO6_CHECK_REPORT.md)
- [问题分析计划](../codex/PROBLEM_TASK_PLAN.md)

## 跟踪清单

### 待修复文件
- [ ] `README.md`
- [ ] `README_CN.md`
- [ ] `CLAUDE.md`
- [ ] `CLAUDE_CN.md`
- [ ] `AGENTS.md`
- [ ] `configs/base/environment/base.yaml`

### 待验证Demo
- [ ] `configs/demo/01_cross_domain/cwru_dg.yaml`
- [ ] `configs/demo/02_cross_system/multi_system_cddg.yaml`

---

**最后更新**: 2025-12-15
**状态**: 待修复
**优先级**: P0/P1