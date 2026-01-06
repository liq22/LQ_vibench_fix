# Intake: review-unconfirmed-changes

- Goal: 复盘并处理本次未确认的工作区改动（保留/回滚/拆分），恢复到“可解释、可验证、可提交”的状态。
- Scope:
  - In: 裸 `except:` 清理、文档路径对齐、`.codex/skills` 新增、`paper/LQ_vibench_fix` 子模块脏状态处理、验证门禁梳理。
  - Out: 任何新的功能开发/算法改动；安装依赖/联网下载（除非后续明确确认）。
- Tasks:
  - T1: 盘点并分组当前改动（主仓库 vs submodule；代码 vs 文档 vs skills），输出清单与意图说明。
  - T2: 与用户确认每一组改动的处置（保留/回滚/拆分），给出最小回滚命令。
  - T3: 执行确认后的回滚/保留操作，确保工作区达到目标状态（clean 或仅剩已确认改动）。
  - T4: 运行可用的验证门禁（schema/编译），并记录 `torch` 缺失导致的阻塞项。
  - T5: 产出交付物：report + manifest（记录改动/命令/结果/回滚）。
- Priority: P0
- Due: TBD
- Owner: TBD
- Background:
  - 用户反馈：上文修改未经确认；希望先落盘 Intake/Plan 再推进。
- Details:
  - 主仓库当前 `git status` 显示改动/新增文件包含：
    - 修改：`.gitmodules`、`app/gui.py`、`dev/del/TwoStageController.py`、`docs/custom_dataset.md`、`docs/v0.1.0/done/*`、`examples/config_usage.py`、`src/Pipeline_01_default.py`、`src/configs/*`、`src/data_factory/*`、`src/model_factory/ISFM/M_03_ISFM.py`、`src/utils/CLAUDE.md` 等。
    - 新增：`.codex/skills/*`（`README.md` + 多个 skill 目录）。
  - Submodule `paper/LQ_vibench_fix/` 当前存在 modified/untracked（例如 `LQ_fix/12_23/codex/model_factory_fix.md` 修改；`LQ_fix/TODO.md` 与 `LQ_fix/skill/` 新增）。
  - 验证现状：
    - `python -m scripts.validate_configs` ✅ 通过（7/7）
    - `python main.py --config configs/demo/00_smoke/dummy_dg.yaml` ❌ 缺少 `torch`
    - `python -m pytest test/` ❌ 缺少 `torch`
    - `python -m compileall -q src scripts app examples` ✅ 通过
- Acceptance / DoD:
  - A1: 用户对每一组改动（代码/文档/skills/submodule）给出明确“保留/回滚”决策并被执行。
  - A2: 工作区达到目标：`git status --porcelain` 为空，或仅剩用户确认要保留的改动。
  - A3: 记录至少 1 条可复现验证门禁结果（schema/编译）；若 `torch` 缺失，记录阻塞与建议。
  - A4: 产出 report 与 manifest，路径在当天目录下。
- Notes:
  - 本次落盘目录：`paper/LQ_vibench_fix/LQ_fix/12_31/`
- Evidence:
  - git: `git status --porcelain`, `git diff --stat`
  - cmds: `python -m scripts.validate_configs`, `python -m compileall -q src scripts app examples`
  - blocked: `python main.py --config configs/demo/00_smoke/dummy_dg.yaml`（needs `torch`）, `python -m pytest test/`（needs `torch`）

Next: plan-md-writer

