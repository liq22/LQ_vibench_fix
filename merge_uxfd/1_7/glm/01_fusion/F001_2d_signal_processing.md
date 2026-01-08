# F001: 2D 时频转换组件移植

**所属 Paper**: 📘 1D-2D_fusion_explainable
**分类**: 组件移植
**优先级**: P0
**依赖**: 无

---

## 背景

### 现状描述
- pilot paper (`1D-2D_fusion_explainable`) 需要 1D 信号转换为 2D 时频图
- 当前主仓库已有 1D 信号处理（BLC 格式），需要扩展到 2D（BTFC 格式）

### 为什么需要合并
- pilot 的核心功能依赖 1D→2D 转换
- 融合模块需要 2D 特征作为输入

### 当前问题
- 源文件位置不明确
- 输入输出格式需要适配主仓库约定

---

## 合并任务分解

### 子任务 1: 定位源文件
- [ ] 在 `paper/UXFD_paper/1D-2D_fusion_explainable/` 中搜索 `Signal_processing_2D.py` 或类似文件
- [ ] 识别 2D 时频转换的核心函数
- [ ] 记录函数签名和参数

**验收标准**: 找到源文件并记录函数清单

### 子任务 2: 适配输入输出格式
- [ ] 输入适配：1D BLC (Batch, Length, Channel) → 2D 转换函数
- [ ] 输出适配：确保输出为 BTFC (Batch, Time, Freq, Channel) 格式
- [ ] 添加 magnitude-only 处理：使用 `torch.fft.abs()` 处理复数输出

**验收标准**: 转换函数能正确处理 BLC → BTFC

### 子任务 3: 移植到主仓库
- [ ] 创建 `src/model_factory/X_model/UXFD/signal_processing_2d.py`
- [ ] 移植核心转换函数
- [ ] 添加单元测试

**验收标准**: 文件存在且测试通过

---

## 选项

### 选项 A: Copy + Adapter（推荐 ★）
- **描述**: 复制源文件代码，添加适配层处理格式转换
- **优点**: 快速，保持原代码结构
- **缺点**: 需要维护适配层

### 选项 B: 重写实现
- **描述**: 参考源逻辑，用主仓库风格重写
- **优点**: 代码风格统一
- **缺点**: 耗时，可能引入 bug

---

## 与其他 Paper 的依赖关系
- **依赖自**: 无
- **输出到**: F002 (融合模块依赖 2D 特征)

---

## 验收标准
- **功能验收**: 能将 1D 信号转换为 2D 时频图
- **代码验收**: 通过 `pytest test/test_signal_processing_2d.py`
- **文档验收**: 函数有 docstring 说明输入输出格式

---

## 确认
- [ ] 选项 A - Copy + Adapter
- [ ] 选项 B - 重写实现

**结论**: _____ (待填写)
**备注**: _____
