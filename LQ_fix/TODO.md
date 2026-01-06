# TODO（汇总入口）

本文件是 `paper/LQ_vibench_fix/LQ_fix/` 的 TODO 汇总入口：只保留“当前要做什么 + 指向详细队列”的最小信息。

## 详细队列（Source of Truth）
- 状态追踪与优先级：`paper/LQ_vibench_fix/LQ_fix/12_15/glm/TODO_STATUS.md`
- TODO/FIXME/HACK 逐条清单（按文件/行号）：`paper/LQ_vibench_fix/LQ_fix/12_15/codex/TODO_QUEUE.md`
- Bug 识别项目总览：`paper/LQ_vibench_fix/LQ_fix/12_14/BUGS.md`
- Bug 索引：`paper/LQ_vibench_fix/LQ_fix/12_14/BUG_INDEX.md`
- Skills 生成路线图：`paper/LQ_vibench_fix/LQ_fix/skill/plan.md`
- 当天落盘协议（intake/plan/artifact/daily/todo）：`paper/LQ_vibench_fix/LQ_fix/skill/answer1.md`

## 本周优先（建议）
（从 `12_15/glm/TODO_STATUS.md` 摘要；做完后在原文件里勾选/更新）

### P0 / 阻塞
- [ ] 文档兼容性问题修复（P0级路径问题）
  - [ ] 修正 `AGENTS.md` 中的脚本路径
  - [ ] 统一 demo 配置与描述
  - [ ] 修复 CLI 参数示例
- [ ] 裸 `except` 清理（P0，7 处：见 `paper/LQ_vibench_fix/LQ_fix/12_15/glm/TODO_STATUS.md`）

### P1 / 重要
- [ ] 手动审查剩余模块（model_factory / task_factory / trainer_factory / utils / pipelines）
- [ ] 补齐剩余模块的 bug 文档（见 `paper/LQ_vibench_fix/LQ_fix/12_15/glm/TODO_STATUS.md` “待创建的模块文档”）

## Skills / 工作流 TODO（可选）
- [ ] 继续 Sprint 2：`plan-md-executor`、`vibe-batch-orchestrator`（见 `paper/LQ_vibench_fix/LQ_fix/skill/plan.md`）
- [ ] 将“当天文件夹协议”应用到后续记录（`<MM_DD>/codex/...`），并用 `daily-vibe-update` 产出 `daily.md` + `todo.md`

## 决策点（需要你拍板）
- [ ] Demo 描述策略：A 修改文档描述（推荐） / B 修改配置匹配描述
- [ ] 异常处理标准：是否统一异常类型/是否需要统一装饰器
- [ ] TODO 清理策略：时间线 + 保留/删除标准

