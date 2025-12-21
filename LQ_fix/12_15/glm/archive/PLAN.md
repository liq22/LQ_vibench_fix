# PHM-Vibench Bug 识别与 README 歧义修复统一计划（2025-12-14）

## 目标与范围

### 总目标
- 系统性识别并文档化仓库中的问题（Bug/不一致/潜在风险），形成可执行的修复清单与优先级建议。

### 范围
- **代码与配置相关问题**：仅做“识别 + 记录 + 复现/定位线索”，不在本计划内直接改动逻辑代码。
- **文档一致性问题（README/链接/路径）**：允许进行“文档修正”，因为这类问题本质上就是文档 bug，且不会改变训练/模型逻辑。

### 当前分支
- `lqfix_25-12`

## 产出（Deliverables）

- `docs/LQ_fix/12_14/BUGS.md`：Bug 总览（按优先级/模块汇总）
- `docs/LQ_fix/12_14/BUG_INDEX.md`：Bug 索引（可按 ID 快速跳转）
- `docs/LQ_fix/12_14/BUG_TEMPLATES.md`：Bug 报告模板（字段规范）
- `docs/LQ_fix/12_14/bugs/*.md`：分模块记录（configuration/data_factory/model_factory/task_factory/trainer_factory/pipelines/utils/docs）
- `docs/LQ_fix/12_14/glm/`：具体可执行操作步骤（runbook）
- `docs/LQ_fix/12_14/reports/BUG_SUMMARY.md`：统计与建议（数量分布、P0/P1 列表、修复路线）
- `docs/LQ_fix/12_14/archive/`：归档（旧版本文档、临时记录等）

## 目录结构（统一口径）

```
docs/LQ_fix/12_14/
├── README.md
├── PLAN.md
├── BUGS.md
├── BUG_INDEX.md
├── BUG_TEMPLATES.md
├── bugs/
│   ├── configuration.md
│   ├── data_factory.md
│   ├── model_factory.md
│   ├── task_factory.md
│   ├── trainer_factory.md
│   ├── pipelines.md
│   ├── utils.md
│   └── docs.md
├── glm/
│   ├── README.md
│   ├── 01_preflight.md
│   ├── 02_auto_scan.md
│   ├── 03_manual_review.md
│   └── 04_triage_and_docs.md
├── reports/
│   └── BUG_SUMMARY.md
└── archive/
```

## Bug 分类标准

### 优先级
- **P0（致命）**：崩溃/数据损坏/训练不可用/结果目录写错导致覆盖等
- **P1（严重）**：核心功能不可用但有绕过方案，或会显著影响结论可信度
- **P2（中等）**：功能受限、默认配置不合理、边界条件错误
- **P3（轻微）**：体验/日志/命名/文档问题

### 类型
- 配置错误（schema/默认值/override 解析等）
- 数据加载问题（路径/reader/内存/切分）
- 模型构建/注册问题（registry、权重加载）
- 任务/训练流程问题（batch 格式、loss/metric）
- 管道问题（`src/Pipeline_*.py` 的多阶段/继承）
- 性能/资源问题（显存、CPU、IO）
- 文档不一致（README/链接/路径/示例命令）

## 执行计划（建议 5–8 天）

### Day 1：准备与规范化
1. 固化目录结构与产出文件名（避免中途改口径）
   - `mkdir -p docs/LQ_fix/12_14/{bugs,glm,reports,archive}`
2. 定义 Bug ID 与状态流转（写入 `BUG_TEMPLATES.md`）
   - 推荐：`BUG-20251214-001` 形式
   - 状态：`open` → `triaged` → `verified` → `fix_planned` / `won't_fix` → `fixed`

### Day 2–3：自动化扫描（低成本广覆盖）
建议使用 `rg`（ripgrep）做可重复的规则扫描，重点减少噪声：

1. 标记性注释
   - `rg -n "\\b(TODO|FIXME|HACK)\\b" src/ configs/ dev/ docs/ test/`
2. 可疑异常处理（优先抓“吞异常/裸 except”）
   - `rg -n "except\\s*:" src/`
   - `rg -n "except\\s+Exception" src/`
   - `rg -n "except\\s+BaseException" src/`
   - `rg -n "except\\b.*:\\s*pass\\b" -S src/`
3. 断言与显式抛错（用于定位隐式假设）
   - `rg -n "\\bassert\\b|\\braise\\b" src/`
4. 配置与路径关键字（硬编码路径、默认路径、ENV）
   - `rg -n "(/home/|\\$HOME|PROJECT_HOME|data_dir|output_dir|save/)" -S src/ configs/`

> 说明：未使用导入/变量建议用 lint 工具完成（ruff/flake8/pyflakes），若环境未安装，先不强行做，避免为了扫描而引入新依赖。

### Day 3–4：手动审查（高价值模块）
按影响面/耦合度优先：

1. **配置系统**：`src/configs/`（重点：`config_utils.py`、override 机制、默认值、错误提示）
2. **数据工厂**：`src/data_factory/`（reader 注册、路径解析、h5 读写/缓存）
3. **模型工厂**：`src/model_factory/`（registry、一致命名、checkpoint 兼容）
4. **任务工厂**：`src/task_factory/`（DG/CDDG/FS/GFS/pretrain 的 batch 格式、loss/metric）
5. **训练器工厂**：`src/trainer_factory/`（Lightning 参数、日志/ckpt 路径、resume）
6. **管道**：`src/Pipeline_*.py`（多阶段配置继承、输出目录组织）

### Day 4–5：文档化与索引
1. 将问题归档到对应 `bugs/*.md`
2. `BUG_INDEX.md` 做可检索索引（ID → 文件/段落）
3. `BUGS.md` 汇总 P0/P1 清单并给修复顺序建议

### Day 6–8：复核与汇总报告
1. 对 P0/P1 做最小复现（尽量用现有 demo 配置/最小 epoch）
2. 输出 `reports/BUG_SUMMARY.md`（数量分布、风险、建议）

## 已执行：根目录 README 歧义修复（记录）

已完成对根目录 `README.md` / `README_CN.md` 的一致性修复，核心包括：
- 将错误的 `scripts/` 路径改为实际存在的 `dev/scripts/`
- “项目结构”改为与仓库一致的高层结构（去掉不存在的 `scripts/`、`main_dummy.py`、`benchmark.py` 等）
- 修正贡献指南/Streamlit prompt/测试指南等内部链接
- 修正 GitHub Issues 链接指向
- 补齐 README 引用但缺失的文档：`docs/custom_dataset.md`、`docs/testing.md`

验证方法（示例）：
- 扫描 README 中相对链接是否都能解析到仓库文件（排除图片与外链）
