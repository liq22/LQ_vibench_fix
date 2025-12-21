# Configuration 模块 Bug

## 概述
本文档记录 configuration（配置系统）相关的 Bug。

---

## BUG-20251214-003: 配置验证中的类型转换使用裸except

- **优先级**: P1
- **类型**: configuration
- **标签**: exception-handling, config-validation
- **状态**: open
- **模块**: configuration
- **文件**: `src/configs/deprecated/config_validator.py:375,380`
- **发现时间**: 2025-12-14 16:23:29

### 问题描述
在配置验证的类型转换函数中使用裸except，可能隐藏 ValueError、OverflowError 等异常，并返回硬编码默认值，导致错误配置被静默接受。

### 代码位置
```python
# src/configs/deprecated/config_validator.py:373-376, 378-381
try:
    return str(int(float(str(current_value))))
except:
    return "1"

try:
    return str(float(current_value))
except:
    return "0.1"
```

### 期望行为
应该捕获具体的异常类型，并根据不同情况提供更合适的默认值或直接报错/提示。

### 实际行为
所有异常都被捕获并返回硬编码默认值。

### 影响范围
- 配置验证过程（尤其是当 deprecated validator 路径仍被调用时）
- 可能导致错误配置进入训练/推理流程

### 修复建议
```python
if expected_type == int:
    try:
        return str(int(float(str(current_value))))
    except (ValueError, TypeError, OverflowError):
        return "1"
elif expected_type == float:
    try:
        return str(float(current_value))
    except (ValueError, TypeError, OverflowError):
        return "0.1"
```

---

*最后更新：2025-12-14*

