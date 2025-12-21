# Data Factory 模块 Bug

## 概述
本文档记录 data_factory 模块相关的 Bug。

---

## BUG-20251214-001: H5文件句柄关闭时使用裸except

- **优先级**: P0
- **类型**: data
- **标签**: exception-handling, resource-leak
- **状态**: open
- **模块**: data_factory
- **文件**: `src/data_factory/H5DataDict.py:40`
- **发现时间**: 2025-12-14 16:23:29

### 问题描述
在关闭HDF5文件句柄时使用了裸except语句，可能会隐藏重要的异常信息，导致文件句柄泄漏或其他问题未被及时发现。

### 代码位置
```python
# src/data_factory/H5DataDict.py:38-41
try:
    self.h5f.close()
except:
    pass  # 忽略关闭时的异常
```

### 期望行为
应该捕获特定的异常类型（如OSError、ValueError），并至少记录日志以便调试。

### 实际行为
使用裸except捕获所有异常（包括SystemExit、KeyboardInterrupt），完全静默忽略。

### 影响范围
- 所有使用HDF5数据集的操作
- 可能导致文件句柄泄漏
- 难以调试文件关闭相关的问题

### 复现步骤
1. 使用包含无效或损坏的HDF5文件
2. 尝试关闭文件句柄
3. 异常被静默忽略

### 修复建议
```python
import logging

try:
    self.h5f.close()
except (OSError, ValueError) as e:
    logging.warning(f"Failed to close HDF5 file {self.h5_file}: {e}")
```

---

## BUG-20251214-002: 析构函数中的裸except可能隐藏资源泄漏

- **优先级**: P0
- **类型**: data
- **标签**: exception-handling, resource-leak
- **状态**: open
- **模块**: data_factory
- **文件**: `src/data_factory/H5DataDict.py:89`
- **发现时间**: 2025-12-14 16:23:29

### 问题描述
在析构函数中使用裸except，当资源清理失败时完全静默，可能导致资源泄漏。

### 代码位置
```python
# src/data_factory/H5DataDict.py:87-90
def __del__(self):
    """析构函数，确保文件被关闭"""
    try:
        self.close()
    except:
        pass  # 忽略析构时的异常
```

### 期望行为
应该记录析构时的错误，或使用atexit.register确保资源清理。

### 实际行为
所有异常都被静默忽略。

### 影响范围
- 对象生命周期结束时
- 可能导致HDF5文件未正确关闭
- 影响其他进程访问文件

### 修复建议
```python
import logging
import traceback

def __del__(self):
    """析构函数，确保文件被关闭"""
    try:
        self.close()
    except Exception as e:
        # 使用logging而不是print，避免在析构函数中的IO操作
        try:
            logging.error(f"Error closing HDF5 file in __del__: {type(e).__name__}: {e}")
        except:
            # 如果连logging都失败了，至少记录到sys.stderr
            import sys
            print(f"Error closing HDF5 file in __del__: {type(e).__name__}: {e}", file=sys.stderr)
```

---

## BUG-20251214-004: ID选择器中的裸except可能隐藏数据加载错误

- **优先级**: P0
- **类型**: data
- **标签**: exception-handling, data-integrity
- **状态**: open
- **模块**: data_factory
- **文件**: `src/data_factory/samplers/del/ID_selector.py:123,150,162`
- **发现时间**: 2025-12-14 16:23:29

### 问题描述
在ID选择器的多个关键位置使用裸except，可能隐藏数据加载、索引创建等严重错误。

### 代码位置
```python
# 多个位置的裸except
except:
    # 处理异常但不记录
```

### 期望行为
应该记录异常类型和上下文，特别是数据加载相关的错误。

### 实际行为
异常被完全忽略，可能导致静默失败。

### 影响范围
- ID采样器的正常工作
- 可能导致采样结果不正确
- 影响训练数据的质量

### 修复建议
```python
import logging

except Exception as e:
    logging.error(f"Error in ID selector at {function_name}: {type(e).__name__}: {e}")
    # 根据情况决定是继续还是重新抛出
```

---

*最后更新：2025-12-14*
