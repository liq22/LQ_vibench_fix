# 文档兼容性检查与更新计划（12_15）

目标：检查并修正下列文档中与当前仓库结构/命令/配置不一致的内容，避免用户按文档执行直接失败或产生误解。

检查范围：
- `README.md`
- `README_CN.md`
- `CLAUDE.md`
- `CLAUDE_CN.md`
- `AGENTS.md`

## 0) 执行状态（已部分落地）

已落地（以仓库当前状态为准）：
- `README.md` / `README_CN.md`：新增离线 smoke run（`configs/demo/00_smoke/dummy_dg.yaml`）；并把配置入口统一指向 `configs/README.md` + config 工具链。
- `CLAUDE.md` / `AGENTS.md` / `CLAUDE_CN.md`：明确分工与“唯一主入口”，去掉 `tests/` 等不存在路径描述。
- `CONTRIBUTING.md`：修正不存在的 `tests/`、`requirements-dev.txt`、`pip install -e .` 等指引，统一到 `test/`。
- `docs/hse-implementation/*`：移除不存在的 `tests/**` 路径引用，并将 paper 级脚本标注为 TODO（计划迁移到 submodule）。

仍待确认/未做（避免越权破坏性变更）：
- `configs/reference/` 的整体迁移（当前仅在文档中标注 legacy/计划删除）。
- `streamlit_app.py` 是否继续作为主 README 推荐入口（当前已降级为实验性 TODO，但功能验收点不清晰）。

## 1) 发现的主要不兼容点（摘要）

### A. demo 描述与配置不一致
- Demo #1/#2：当前配置更接近“可通过 `target_system_id` 调整”的表述；如要固定为 “CWRU→Ottawa”，需要先固化 metadata 的 `Dataset_id` 映射约定（建议策略 A：不在 README 写死 Ottawa）。

### B. 文档引用了不存在/已移动的路径
- `configs/demo/Single_DG/...` 等旧路径已从文档示例中移除/替换。
- `scripts/*`（paper 级脚本）不再作为主仓库入口；HSE 脚本迁移到 paper submodule（主仓库 wrapper 仅做提示）。

### C. CLI 参数不一致
- `--pipeline`（`main.py` 不支持）已从顶层指引中移除/替换为 “YAML 顶层 `pipeline:`” 的说明。

### D. 默认/示例路径硬编码
- `configs/base/environment/base.yaml` 中 `PROJECT_HOME` 当前为 `.`（相对路径）。

## 2) 12_15 更新计划（按优先级）

### P0：阻塞性错误（按文档执行会直接失败）
1. 统一主入口与模板来源（已落地）：
   - 主入口：`python main.py --config <yaml> [--override ...]`
   - 模板来源：`configs/demo/`（离线 smoke demo：`configs/demo/00_smoke/dummy_dg.yaml`）
2. Paper 级脚本入口（未落地；仅文档标注 TODO）：
   - 计划迁移到 paper submodule，主仓库不把其作为“必跑验证”
3. 修正文档里不存在的测试/依赖/路径（已部分落地）：
   - `tests/` → `test/`
   - 删除 `requirements-dev.txt` / `pip install -e .` 等仓库内不存在的指引

### P1：误导性描述（不会立即报错，但会误解实验含义）
1. Demo #1 文案策略（建议持续使用策略 A）：
   - README 不写死 “CWRU→Ottawa”，而是说明 “具体系统由 metadata + target_system_id 决定”
2. Demo #2 文案策略：
   - 保持 “edit target_system_id for multi-system” 的表述即可；如需默认 multi-system，再改 YAML 的 id 列表（需团队确认）

### P2：维护性改进（减少未来再次漂移）
1. 在文档中避免写死 dataset_id→dataset_name 的映射（若该映射依赖 metadata/排序，容易漂移）
2. 新增“文档内路径自检”脚本/命令（可复用 `rg` + 存在性检查）并写入 `docs/LQ_fix/12_15/codex/`

## 3) 交付物

- `docs/LQ_fix/12_15/codex/DEMO6_CHECK_REPORT.md`：6 个 demo 的静态检查结果与问题点
- 本文件：`docs/LQ_fix/12_15/codex/README_COMPAT_PLAN.md`
