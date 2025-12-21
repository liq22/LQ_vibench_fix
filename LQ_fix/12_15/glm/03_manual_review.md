# 03 Manual Review（手动审查：按模块检查点）

> **状态**: 🔄 部分完成 (2025-12-14/15)

本阶段目标：补齐自动化扫描覆盖不到的问题（设计缺陷、流程错配、边界条件）。

## 1. 配置系统（`src/configs/`）

检查点：
- `load_config`/override 的优先级是否清晰，错误信息是否能指向具体 key
- 关键字段缺失时的行为：报错/默认值/静默跳过
- 配置路径解析是否依赖当前工作目录（CWD）

建议输出：
- 记录到 `docs/LQ_fix/12_14/bugs/configuration.md`

## 2. 数据工厂（`src/data_factory/`）

检查点：
- reader/registry 是否能根据配置正确找到数据集实现
- `data_dir` / metadata / h5 文件的拼接逻辑是否与 README/示例一致
- 大数据集是否存在内存峰值风险（一次性读入、缓存策略）

建议输出：
- 记录到 `docs/LQ_fix/12_14/bugs/data_factory.md`

## 3. 模型工厂（`src/model_factory/`）

检查点：
- 模型 name/type/backbone/head 的 registry 命名是否一致（配置里能否直观表达）
- checkpoint 加载：strict 与兼容策略、缺失 key 的提示
- 依赖导入是否会造成循环引用/隐式副作用

建议输出：
- 记录到 `docs/LQ_fix/12_14/bugs/model_factory.md`

## 4. 任务工厂（`src/task_factory/`）

检查点：
- 不同任务（DG/CDDG/FS/GFS/pretrain）对 batch 格式的假设是否一致
- loss/metric 的 key 命名是否统一（影响日志/绘图）
- 多任务权重/采样策略是否可能导致训练不稳定或统计失真

建议输出：
- 记录到 `docs/LQ_fix/12_14/bugs/task_factory.md`

## 5. 训练器工厂（`src/trainer_factory/`）

检查点：
- 训练设备（cpu/cuda）配置路径与默认值是否合理
- 日志与 checkpoint 输出目录是否符合约定且不会覆盖
- resume/seed/reproducibility 是否能落到实际效果（例如 seed 是否真的传递到各处）

建议输出：
- 记录到 `docs/LQ_fix/12_14/bugs/trainer_factory.md`

## 6. 管道（`src/Pipeline_*.py`）

检查点：
- 多阶段 pipeline 的 config 继承/覆盖是否易理解且可复现
- stage1 → stage2 的产出传递是否显式（路径、ckpt 名称、metadata）
- pipeline 入口的错误提示是否足够（用户能否迅速定位是 data/model/task/trainer 哪一层）

建议输出：
- 记录到 `docs/LQ_fix/12_14/bugs/pipelines.md`

## 7. 文档与示例（`README*`, `docs/`）

检查点：
- 文档中出现的路径/目录是否真实存在
- 示例命令是否能跑到“至少启动并跑完一个最小流程”（若需要数据则说明前置条件）
- FAQ/贡献指南/脚本路径是否与仓库结构一致

建议输出：
- 记录到 `docs/LQ_fix/12_14/bugs/docs.md`

## 实际执行结果

### ✅ 已完成审查

1. **配置系统**
   - ✅ 已创建 [`configuration.md`](../12_14/bugs/configuration.md)
   - 发现：配置路径处理良好，override机制清晰

2. **数据工厂**
   - ✅ 已创建 [`data_factory.md`](../12_14/bugs/data_factory.md)
   - 发现：4个P0/P1级bug，主要是异常处理问题

3. **文档兼容性**（12_15新增）
   - ✅ 已完成6个demo配置检查
   - 发现：Demo描述与配置不一致问题
   - 详见：[`DOCS_COMPATIBILITY.md`](DOCS_COMPATIBILITY.md)

### 🔄 进行中

以下模块仍需详细审查：
- [ ] **模型工厂** - 待创建 `model_factory.md`
- [ ] **任务工厂** - 待创建 `task_factory.md`
- [ ] **训练器工厂** - 待创建 `trainer_factory.md`
- [ ] **管道系统** - 待创建 `pipelines.md`
- [ ] **通用工具** - 待创建 `utils.md`
- [ ] **文档与示例** - 待创建 `docs.md`

### 📋 审查发现总结

#### 高优先级发现
1. **裸except语句**（P0）
   - 7个位置需要立即修复
   - 主要集中在数据加载和文件操作

2. **Demo配置问题**（P1）
   - Demo #1: "CWRU → Ottawa"描述不准确
   - Demo #2: "multi-system"实际为单系统

#### 中优先级发现
1. **异常处理模式**
   - 142处`except Exception`需要审查
   - 建议使用更具体的异常类型

2. **硬编码路径**
   - 配置文件中的绝对路径需要处理
   - 建议使用环境变量或相对路径

### 📝 审查方法

使用了以下方法进行审查：
1. **静态分析**：基于rg扫描结果的深度分析
2. **配置验证**：实际加载demo配置文件验证
3. **文档对比**：对比文档描述与实际配置
4. **代码追踪**：跟踪关键执行路径

### 🎯 经验教训

1. **扫描局限性**
   - 自动化扫描难以发现语义层面的不一致
   - 需要结合手动审查发现设计问题

2. **Demo重要性**
   - Demo是用户的第一印象，必须保证准确性
   - 建议添加自动化测试验证demo可运行性

3. **文档一致性**
   - 文档与代码必须同步更新
   - 建议建立文档检查流程

