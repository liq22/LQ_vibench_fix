# 刘垓计划：全仓库清晰化与上手体验（12_15）

目标：系统性清理 `src/configs|data|model|task|trainer` 及 `docs/` 中“过时/有歧义/不清楚”的内容，形成**单一主入口**与**可维护的文档分层**，确保新同学 30 分钟内可完成最小跑通与定位扩展点。

本计划只定义“要做什么、按什么顺序做、验收什么”；具体逐项修复建议按模块分批确认后执行。

## 1) 范围与方法

### 范围
- 代码文档：`src/**/README*.md`、`src/**/CLAUDE*.md`、`src/readme.md`
- 配置文档：`src/configs/*.md`、`configs/readme.md`、`configs/*.yaml`
- 运行入口与参数：`main.py`、`src/Pipeline_*.py`
- 数据与 reader 示例：`src/data_factory/reader/*.py`
- 仓库文档：`docs/**/*.md`（含历史文档）

### 方法（可重复）
- 自动扫描（规则见 `docs/LQ_fix/12_15/codex/scan_logs/rg_liugai_*.txt`）：
  - 过时路径：`configs/demo/Single_DG|Multiple_DG|Pretraining|GFS`、`configs/reference`
  - 过时脚本：`scripts/`、`script/`
  - 过时 CLI：`--pipeline`、`--config_path`、`--fs_config_path`
  - 硬编码路径：`/home/`、`C:\`
- 手工抽查：入口文档（README/CLAUDE/AGENTS）+ 每个 factory 的 README 关键段落。

#### 如何理解“自动化扫描” vs “逐步人工检查”
- 自动化扫描（`rg` 规则 + 保存 `scan_logs/`）适合做“全量粗筛”：快速定位过时路径、硬编码、TODO/FIXME、旧 CLI flag 等“可被正则稳定捕获”的问题，并可复用为后续回归门禁。
- 人工检查适合做“语义核验”：判断某个字段/示例命令是否真实可跑、某段描述是否会误导、某处耦合是否被说明清楚（这些往往需要理解 loader/factory 的真实消费逻辑，单纯正则无法判定）。
- 实战建议：先扫描得到候选清单（可 review/可量化），再按模块人工逐条确认与修复（可避免遗漏，也避免“扫描命中但其实没问题”的误改）。

## 2) 当前主要问题（摘要）

### A. “单一主入口”不一致（最影响上手）
- 同一仓库里同时存在多套入口叙述：`main.py --config ...` vs `python -m src.Pipeline_* --config_path ...` vs `main.py --pipeline ...`（见扫描日志）。
- 结果：用户不知道哪套是“当前支持/维护”的。

### B. 配置路径体系漂移（计划删除 reference 后更严重）
- 大量文档仍引用 `configs/demo/Single_DG/...` 这类旧路径；同时 `configs/reference/` 即将删除/迁移，导致“模板来源”歧义。

### C. 代码/配置存在硬编码绝对路径
- `configs/default.yaml`、`configs/base/data/*.yaml`、部分 pipeline/reader 里出现 `/home/...` 等硬编码（对外发布会直接误导）。

### D. docs 的“维护状态”不清晰
- `docs/past/` 已存在，但仍有不少历史/外部工程文档散落在 `docs/` 根下（如 HPC/统一度量/旧 quickstart），且未统一标注“历史/外部仓库”。

### E. 数据 reader 示例代码混入本机路径
- 多个 `RM_*.py` 文件包含硬编码 `file_path=/home/...` 或 `test_reader(metadata_path=...)` 等本机测试片段，容易被误认为“必需配置/官方路径”。

## 3) 清晰化标准（需要达成的“仓库契约”）

### 3.1 入口契约（必须唯一）
- **唯一主入口**：`python main.py --config <yaml> [--override key=value ...]`
- Pipeline 选择：由 YAML 顶层 `pipeline:` 决定（不在主 README 里推广 `--pipeline`）
- `python -m src.Pipeline_*` 仅作为开发调试入口：放到 `docs/past/` 或在文档显式标注“开发用/可能不稳定”

### 3.2 配置契约（模板来源唯一）
- **模板来源**：`configs/demo/`（你已确认）
- `configs/reference/`：计划删除/迁移到 paper submodule；主文档不再依赖

### 3.3 路径契约（无硬编码）
- 对外文档/默认配置不得出现开发机绝对路径：
  - 用 `/path/to/...` 占位符
  - 或用 `configs/local/local.yaml` 机制覆盖（本仓库已有合并逻辑）

### 3.4 文档分层契约（可维护）
- `README(.md|_CN.md)`：只放“上手/6 demos/数据路径怎么配/常见问题”
- `docs/`：维护中的功能文档（每篇必须含“适用版本/维护状态”）
- `docs/past/`：历史文档（只保留参考价值，默认不保证可运行）
- `paper/` submodule：论文级脚本/配置/流水线（与主仓库解耦）

## 4) 执行路线图（分阶段）

### P0（上手不踩坑，1–2 天）
1. **统一入口叙述**：把 `src/readme.md`、`src/utils/CLAUDE.md`、`src/configs/CLAUDE.md` 中的旧入口/旧路径改为主入口契约。
2. **模板来源收敛**：所有文档 “start from …” 统一指向 `configs/demo/`。
3. **硬编码路径清理（对外）**：
   - `configs/default.yaml` 标注为 `local.sample` 或移动到 `configs/v0.0.9/local/`；主文档不再引用。
   - `configs/base/data/*.yaml` 将 `data_dir` 改为 `/path/to/PHM-Vibench`（或要求用户用 local override）。
4. **明显误导的代码默认值**：pipeline argparse 默认 config_path 不应指向开发机绝对路径。

验收：
- 新用户只看 README 能找到唯一运行命令，并且 repo 内所有“示例路径”都存在且无 `/home/...`。

### P1（消除歧义，1 周）
1. **doc 分层标注**：为 `docs/` 根下历史/外部工程文档统一加顶部 banner（“历史/外部仓库/不保证可运行”），或移动到 `docs/past/`。
2. **模块 README 统一模板**（configs/data/model/task/trainer/utils）：
   - “我是谁/对外入口/最小可运行示例/常见坑/扩展方式/相关配置”
3. **数据 ID 映射说明统一**：
   - 明确 `task.target_system_id` 来自 metadata 的 `Dataset_id` 列，避免写死 Ottawa=5 之类映射。

验收：
- 文档中不再出现同一概念多种叫法（system_id/dataset_id/target_system_id 混用而无定义）。

### P2（减少未来漂移，持续）
1. **加入文档自检脚本**（本地/CI 均可跑）：
   - 扫描禁用模式：硬编码路径、删除目录引用、过时 CLI flag
2. **建立“变更门禁”**：
   - 修改入口/配置目录结构必须同步更新：README + configs/readme.md + 对应模块 README

验收：
- 新增/修改文档不会再引入 `configs/reference`/`scripts/`/`--pipeline` 等过时引用。

## 5) 具体待办清单（按模块）

> 下面每条建议都对应扫描结果，修复时建议“一次只改一个模块”，便于回滚与 review。

### configs / config system
- `src/configs/CLAUDE.md`：更新 `PRESET_TEMPLATES` 与示例路径（当前仍大量引用 `configs/demo/Single_DG/...`）。
- `src/configs/config_utils.py`：自检/示例字符串里仍含旧路径（影响读者理解）。
- `configs/default.yaml`：硬编码环境变量与数据路径（建议改为 sample 或移出主流程）。

### pipelines / CLI
- `src/Pipeline_01_default.py`：argparse 默认 `config_path` 存在开发机绝对路径。
- `src/readme.md`：已按“主入口契约”更新为 `python main.py --config ...`；保留 `python -m src.Pipeline_*` 仅作为开发/调试路径说明。

### data_factory
- `src/data_factory/reader/*.py`：清理/隔离本机 `file_path=/home/...` 的测试片段（放入 `if __name__ == "__main__":` 且使用占位符，或迁移到 `dev/`）。
- `src/data_factory/CLAUDE.md`：更新示例配置路径（当前仍引用旧 demo）。

### model_factory / task_factory / trainer_factory
- 模块 README 中引用 `configs/reference/*` 的内容：改为 demo 或标注迁移到 paper submodule。

### docs
- `docs/HPC.md`：大量集群绝对路径，建议移动到 `docs/past/` 或添加“特定环境文档”banner。
- `docs/past/*`：补充统一“历史文档不保证可运行”的 header（可用脚本批量加）。

## 6) 输出物（用于后续逐项修复）

- 扫描日志：`docs/LQ_fix/12_15/codex/scan_logs/rg_liugai_*.txt`
- 本计划：`docs/LQ_fix/12_15/codex/LIUGAI_PLAN.md`

## 7) 建议的执行顺序（给 Codex/人工 review）

1. 先做 P0（入口/路径/硬编码）并只动少量关键文件；
2. 再做 P1（文档分层/术语统一）并一次只处理一个模块；
3. 最后做 P2（自动化门禁），用脚本/CI 防止回归。
