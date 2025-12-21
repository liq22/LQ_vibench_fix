# HSE 脚本迁移 & Streamlit UI 整理计划（12_15）

## 0) 决策输入（来自确认）

- 模板来源：统一指向 `configs/demo/`（不再推荐 `configs/reference/`）。
- HSE synthetic demo：属于另外的 paper 工作流，迁移到 paper submodule（方案B）。
- Streamlit UI：当前无完善可视化且存在 bug；需要明确为 TODO，避免主流程混乱。

## 1) 问题分析

### A. `configs/reference/` 即将删除导致的歧义
- 多处文档把 `configs/reference/` 当作“模板/权威配置”，但该目录后续会删除/迁移。
- 需要把“模板/入口”的单一信息源收敛到 `configs/demo/`，避免用户照文档执行失败。

### B. `dev/scripts/hse_synthetic_demo.py` 的定位不清
- 当前主仓库内并不存在 `hse_synthetic_demo.py`（历史文档/外部工程引用会造成误导）。
- 主仓库的“可运行示例”应以 `configs/demo/*` 为准（例如 `05_pretrain_fewshot`、`06_pretrain_cddg`）。
- 若需要 synthetic demo / pipeline03 等论文级脚本，建议在 paper submodule 中维护并在主仓库只保留指向说明（避免入口混乱）。

### C. `streamlit_app.py` 的可用性与预期不匹配
- 文档描述为“可视化 UI”，但当前实现偏“配置编辑 + 启动”，曲线/预测详情未实现。
- 需要把其定位明确为“实验性 TODO”（不作为主流程验收项），并给出后续补全可视化的拆解任务。

## 2) 目标与作用说明（方案B）

### HSE 脚本迁移的目的
- 将 paper 级脚本/流水线与主仓库 demo/入口解耦，避免：
  - 文档/CLI 入口漂移；
  - 用户把 paper 代码当成“主流程必跑步骤”。

### 保留（deprecation wrapper）的作用
- 保留原路径的“提示入口”，避免历史文档/旧命令静默失效；
- 明确告知脚本已迁移，并指向 submodule 初始化说明与替代 demo。

## 3) 执行计划（TODO 列表）

### P0（本次已执行）
- 将主仓库模板推荐统一为 `configs/demo/`。
- 修正文档中对 HSE/Streamlit 的定位：标注 TODO/实验性，避免“照抄即挂”。

### P1（后续开发 TODO）
- 在 paper submodule 内补齐/维护：
  - synthetic demo
  - pipeline03 集成测试
  - paper 级配置与运行脚本
- 主仓库侧：
  - `docs/hse-implementation/` 迁移/下线（或只保留“跳转到 submodule”页面）
  - Streamlit UI：补齐训练曲线/结果加载/图表渲染（明确依赖 `save/` 或 `results/` 的产物结构）

## 4) 本次变更记录（已落地）

- 文档收敛到 `configs/demo/`：`README.md`、`README_CN.md`、`AGENTS.md`、`CLAUDE.md`、`configs/README.md`
- HSE 文档消歧义与 TODO 标注：`docs/hse-implementation/README.md`、`docs/hse-implementation/core-components.md`、`docs/hse-implementation/pipeline-guide.md`
- README 中 Streamlit 描述明确为实验性 TODO：`README.md`、`README_CN.md`
