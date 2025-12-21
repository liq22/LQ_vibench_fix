# PHM-Vibench Bug总览

## 快速导航
- [Bug索引](BUG_INDEX.md)
- [Bug模板](bugs/BUG_TEMPLATES.md)
- [扫描结果](bugs/reports/quick_triage_report.md)
- [扫描日志](bugs/reports/scan_logs/)

## 优先级统计
- **已建档 Bug**：4个（`BUG-20251214-001` ~ `BUG-20251214-004`）
- **P0（致命）**：3个（已建档）
- **P1（严重）**：1个（已建档）
- **扫描候选**：见 `bugs/reports/quick_triage_report.md`

## 模块分布
- [Data Factory](bugs/data_factory.md)：3个（已记录）
- [Configuration](bugs/configuration.md)：1个（已记录）
- [Model Factory](#)：0个（待记录）
- [Task Factory](#)：0个（待记录）
- [Trainer Factory](#)：0个（待记录）
- [Pipelines](#)：0个（待记录）
- [Utils](#)：0个（待记录）
- [Docs](#)：0个（待记录）

## 关键发现

### 1. 异常处理不当（最严重）
- **7个P0级裸except**：可能隐藏关键异常，导致静默失败
- **131个except Exception**：捕获过于宽泛，影响调试
- 影响文件：H5DataDict.py、config_validator.py、ID_selector.py等

### 2. 路径硬编码问题（406个）
- 大量硬编码的 `/home/` 路径
- 环境变量依赖：`PROJECT_HOME`、`VBENCH_HOME`等
- 影响可移植性和部署

### 3. 配置问题
- **586个assert语句**：其中部分在用户配置路径上
- 配置验证不当可能导致运行时错误

## 立即需要关注的问题

1. **H5文件句柄管理**（P0）
   - 文件关闭异常被静默忽略
   - 可能导致资源泄漏

2. **ID选择器错误处理**（P0）
   - 数据采样过程中的异常被忽略
   - 影响训练数据质量

3. **配置验证类型转换**（P1）
   - 类型转换失败时返回错误默认值
   - 可能导致配置错误

## 修复优先级建议

1. **第一批（P0）**：修复所有裸except，添加适当的异常处理和日志
2. **第二批（P1）**：改进配置验证，处理路径硬编码问题
3. **第三批**：优化assert语句，添加更友好的错误提示

## 统计图表

```
问题类型分布：
- 异常处理：138个 (裸except: 7, except Exception: 131)
- 断言语句：586个
- 路径问题：406个
- TODO/FIXME：136个
```

---

*最后更新：2025-12-14*
*扫描工具：ripgrep (rg)*
*分析工具：quick_triage.py*
