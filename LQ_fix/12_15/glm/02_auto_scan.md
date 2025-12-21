# 02 Auto Scan（自动化扫描：可重复、低噪声）

> **状态**: ✅ 已完成 (2025-12-14)

本阶段目标：用统一规则扫描"高信号"线索，并把结果沉淀为可追踪的 Bug 记录。

## 0. 扫描产出保存策略（推荐）

推荐将原始扫描输出保存在：
- `docs/LQ_fix/12_14/reports/scan_logs/`（便于回溯）

示例（命令输出写入文件）：

```bash
mkdir -p docs/LQ_fix/12_14/reports/scan_logs
```

## 1. TODO / FIXME / HACK

```bash
rg -n "\\b(TODO|FIXME|HACK)\\b" src/ configs/ dev/ docs/ test/ \
  | tee docs/LQ_fix/12_14/reports/scan_logs/rg_todo_fixme_hack.txt
```

处理方式：
- 对“明确会影响运行/结果”的条目，创建 Bug（P0–P2）
- 对“纯文档 TODO/占位”条目，记录到 docs 模块或 P3

## 2. 可疑异常处理（吞异常/裸 except）

```bash
rg -n "except\\s*:" src/ \
  | tee docs/LQ_fix/12_14/reports/scan_logs/rg_except_bare.txt

rg -n "except\\s+Exception" src/ \
  | tee docs/LQ_fix/12_14/reports/scan_logs/rg_except_exception.txt

rg -n "except\\s+BaseException" src/ \
  | tee docs/LQ_fix/12_14/reports/scan_logs/rg_except_baseexception.txt

rg -n "except\\b.*:\\s*pass\\b" -S src/ \
  | tee docs/LQ_fix/12_14/reports/scan_logs/rg_except_pass.txt
```

判定建议：
- `except:` / `except BaseException` 通常优先级更高（容易吞掉 KeyboardInterrupt/SystemExit 等）
- `except Exception` 需要看是否记录日志、是否降级为默认值、是否导致 silent failure

## 3. assert / raise（定位隐含假设）

```bash
rg -n "\\bassert\\b|\\braise\\b" src/ \
  | tee docs/LQ_fix/12_14/reports/scan_logs/rg_assert_raise.txt
```

处理方式：
- 对“用户输入/配置导致必然触发”的断言或 raise，优先记录（P0/P1）

## 4. 路径/环境变量/输出目录硬编码

```bash
rg -n "(/home/|\\$HOME|PROJECT_HOME|data_dir|output_dir|save/)" -S src/ configs/ \
  | tee docs/LQ_fix/12_14/reports/scan_logs/rg_paths_envs.txt
```

判定建议：
- 重点关注 `"/home/xxx"`、固定盘符、硬编码相对路径导致运行目录依赖的问题
- 输出目录（save/log/ckpt）是否会互相覆盖，是否与 README/配置约定一致

## 5. Lint（可选）

如环境已有 `ruff`/`flake8`/`pyflakes`，可将未使用导入/变量纳入扫描；若无则跳过，避免为扫描引入新依赖。

## 实际执行结果

### 📊 扫描统计

| 扫描类型 | 命中数量 | 输出文件 |
|---------|---------|---------|
| TODO/FIXME/HACK | 136条 | [rg_todo_fixme_hack.txt](../12_14/bugs/reports/scan_logs/rg_todo_fixme_hack.txt) |
| 裸except (`except:`) | 7条 | [rg_except_bare.txt](../12_14/bugs/reports/scan_logs/rg_except_bare.txt) |
| except Exception | 142条 | [rg_except_exception.txt](../12_14/bugs/reports/scan_logs/rg_except_exception.txt) |
| except BaseException | 0条 | [rg_except_baseexception.txt](../12_14/bugs/reports/scan_logs/rg_except_baseexception.txt) |
| assert/raise | 203条 | [rg_assert_raise.txt](../12_14/bugs/reports/scan_logs/rg_assert_raise.txt) |
| 路径硬编码 | 89条 | [rg_paths_envs.txt](../12_14/bugs/reports/scan_logs/rg_paths_envs.txt) |

### 🎯 关键发现

1. **P0级问题（7个）**
   - 7个裸except语句，需要立即修复
   - 位置：data_factory、model_factory、utils模块

2. **P1级问题**
   - 142处过度宽泛的异常捕获
   - 硬编码路径问题
   - 未处理的TODO项

3. **P2-P3级问题**
   - 136个TODO/FIXME/HACK项
   - 203个断言和raise需要审查

### 📈 扫描命令优化

实际使用的扫描命令略有调整，以提高精确度：

```bash
# 排除某些目录减少噪声
rg -n "\\b(TODO|FIXME|HACK)\\b" src/ configs/ dev/ --type py --type yaml \
  | tee docs/LQ_fix/12_14/bugs/reports/scan_logs/rg_todo_fixme_hack.txt
```

### 🔄 后续行动

1. **优先处理P0问题**：立即修复7个裸except
2. **分类TODO项**：区分功能实现和优化建议
3. **审查异常处理**：识别需要改进的except模式

