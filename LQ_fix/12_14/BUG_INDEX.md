# Bug索引

## 按优先级

### P0 - 致命（7个）
- **BUG-20251214-001**: H5文件句柄关闭时使用裸except [data_factory](bugs/data_factory.md)
- **BUG-20251214-002**: 析构函数中的裸except可能隐藏资源泄漏 [data_factory](bugs/data_factory.md)
- **BUG-20251214-004**: ID选择器中的裸except可能隐藏数据加载错误 [data_factory](bugs/data_factory.md)
- **待记录**: 裸except in `src/configs/deprecated/config_validator.py:380`
- **待记录**: 裸except in `src/data_factory/samplers/del/ID_selector.py:150`
- **待记录**: 裸except in `src/data_factory/samplers/del/ID_selector.py:162`

### P1 - 严重（238个）
- **BUG-20251214-003**: 配置验证中的类型转换使用裸except [configuration](bugs/configuration.md)
- **待记录**: assert语句在配置文件中（可能影响用户输入）
- **待记录**: 大量异常处理不当（131个except Exception）
- **待记录**: 路径硬编码问题（406个）

### P2 - 中等（0个）
（暂无）

### P3 - 轻微（0个）
（暂无）

## 按类型

- **exception_handling**:
  - [data_factory](bugs/data_factory.md) (4个)
  - [configuration](#) (1个)
  - 其他待分类

- **paths**:
  - 硬编码路径问题（406个）
  - 环境变量依赖

- **assertions**:
  - 配置验证中的assert（586个）
  - 测试代码中的assert

## 按日期

- 2025-12-14：
  - BUG-20251214-001 | H5文件句柄关闭时使用裸except | P0 | exception_handling | data_factory
  - BUG-20251214-002 | 析构函数中的裸except可能隐藏资源泄漏 | P0 | exception_handling | data_factory
  - BUG-20251214-003 | 配置验证中的类型转换使用裸except | P1 | exception_handling | configuration
  - BUG-20251214-004 | ID选择器中的裸except可能隐藏数据加载错误 | P0 | exception_handling | data_factory

---

## 索引格式说明
格式：日期 | BUG-ID | 标题 | 优先级 | 类型 | 模块 | 状态
