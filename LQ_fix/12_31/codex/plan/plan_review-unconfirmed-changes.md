# Plan: review-unconfirmed-changes

## Goal
将本次未确认的工作区改动按意图拆分并处理（保留/回滚），恢复到可解释、可验证的状态，并落盘报告与证据清单。

## Scope
- In:
  - 盘点主仓库与 submodule 的改动分组
  - 与用户确认保留/回滚策略并执行
  - 运行可用门禁并记录 `torch` 缺失阻塞
- Out:
  - 新增功能开发/大规模重构
  - 安装依赖/联网操作（除非用户明确授权）

## Tasks
- [ ] T1 生成“改动分组清单 + 意图”草案
  - DoD: `paper/LQ_vibench_fix/LQ_fix/12_31/codex/report/report_review-unconfirmed-changes.md` 至少列出：主仓库修改/新增文件列表、submodule 状态、每组改动的理由/风险。
  - Dependencies: None
- [ ] T2 与用户确认每组改动的处置（保留/回滚/拆分）
  - DoD: 每组改动都有明确决策；对回滚给出具体命令（含 submodule 处理命令）。
  - Dependencies: T1
- [ ] T3 按确认结果执行回滚/保留，并让工作区达到目标状态
  - DoD: `git status --porcelain` 达到预期（clean 或仅剩确认保留项）；submodule 状态符合预期。
  - Dependencies: T2
- [ ] T4 运行验证门禁并记录结果/阻塞
  - DoD: 在 report 中记录：
    - `python -m scripts.validate_configs` 结果
    - `python -m compileall -q src scripts app examples` 结果
    - `torch` 缺失导致 smoke/pytest 无法运行的说明（若仍缺失）
  - Dependencies: T3
- [ ] T5 生成 `manifest_review-unconfirmed-changes.json`
  - DoD: manifest 包含：变更文件、执行命令、验证结果、回滚点、下一步 backlog。
  - Dependencies: T4

## Gates (optional)
- `python -m scripts.validate_configs`
- `python -m compileall -q src scripts app examples`
- (requires `torch`) `python main.py --config configs/demo/00_smoke/dummy_dg.yaml`
- (requires `torch`) `python -m pytest test/`

## Deliverables
- paper/LQ_vibench_fix/LQ_fix/12_31/codex/report/report_review-unconfirmed-changes.md
- paper/LQ_vibench_fix/LQ_fix/12_31/codex/artifact/manifest_review-unconfirmed-changes.json
- (if needed) paper/LQ_vibench_fix/LQ_fix/12_31/codex/daily/daily.md

## Rollback
- 主仓库回滚：`git restore <paths>` 或 `git restore .`（需用户确认）
- Submodule 回滚：进入 `paper/LQ_vibench_fix/` 后 `git restore .`；如需清理未跟踪文件，`git clean -fd` 属破坏性操作，需二次确认
- 若仅需取消空白改动：优先最小化恢复（例如仅恢复 `.gitmodules`）

## Execution Log
- (leave blank)

