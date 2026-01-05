# Answer1：Sprint 1（4 个 skills）“当天文件夹”落盘协议与手工步骤（优化版）

## 核心要求（硬约束）
- 所有产物都落到“当天文件夹”：`<MM_DD>/codex/{intake,plan,report,artifact,daily,todo}/`
- 目录与文件命名必须可预测，方便多个 skill/subagent 并行且不冲突

## 变量约定
- `<MM_DD>`：当天根目录名，例如 `12_30/`
- `<topic>`：短、可复用、`hyphen-case`，例如 `oom-fix` / `paper-rebuttal` / `meeting-xxx`
  - 长度：3-30 字符
  - 字符集：`[a-z0-9-]`（小写字母、数字、连字符）
  - 冲突检测：若 `intake_<topic>.md` 已存在，追加序号如 `oom-fix-2`
- 默认相对路径：从仓库根目录起算（repo root）

## 0) Directory Contract（强制）
推荐结构（你要的）：

```text
12_30/
  codex/
    intake/
    plan/
    report/
    artifact/
    daily/
    todo/
```

### 文件命名规则（统一，避免冲突）
- `intake/`: `intake_<topic>.md`
- `plan/`: `plan_<topic>.md`
- `report/`: `report_<topic>.md`（本轮 Sprint 1 不负责生成，但计划/日更会引用）
- `artifact/`: `manifest_<topic>.json`
- `daily/`: `daily.md`（当天唯一，避免重复）
- `todo/`: `todo.md`（当天唯一；或 `todo_top10.md`）

### 文件覆盖/冲突策略（默认）
- 若目标文件已存在：先输出拟修改点/差异摘要，**等待用户确认**后再覆盖或增量更新
- 若 `<topic>` 未给出：由 agent 提议 1-3 个候选（从输入中抽取），让用户选一个

### 并发控制规则（防止多 agent 写入冲突）
- **daily.md 和 todo.md 特殊处理**：
  - 若目标文件已存在且在 1 分钟内被修改过：视为"有其他 agent 正在写入"
  - 此时改为：输出到 `<MM_DD>/codex/daily/daily_<agent>_<timestamp>.md`
  - 最后由用户或指定的合并者 skill 统一整理
- **按 topic 分文件的 intake/plan/report/manifest**：天然可并行，无需额外控制

---

## 1) Skill：`intake-normalizer`（输出到 `<MM_DD>/codex/intake/`）

### 触发场景（用户会怎么说）
- “把下面这些材料整理成 intake”
- “把这堆想法/日志/任务规范成 `intake_<topic>.md`”

### 输入（最小）
- 原始材料：日志/想法清单/issue/会议记录等
- 可选：`<MM_DD>`、`<topic>`

### 输出
- 文件：`<MM_DD>/codex/intake/intake_<topic>.md`
- 内容字段（固定顺序，空也要保留字段）：

```md
# Intake: <topic>

- Goal:
- Scope:
- Tasks:
  - T1:
  - T2:
- Priority:
- Due:
- Owner:
- Background:
- Details:
- Acceptance / DoD:
- Notes:
- Evidence:
```

### 手工 SOP（你现在怎么做）
- Step 0：确定 `<topic>`（短、可复用）
- Step 1：通读原始材料，提取字段（Goal/Scope/Tasks/Priority/Due/Owner/Background/Details/Acceptance/Notes/Evidence）
- Step 2：按固定字段顺序写入 `intake_<topic>.md`
- Step 3：如果后续会写计划：在 intake 末尾加一句 `Next: plan-md-writer`

---

## 2) Skill：`plan-md-writer`（输出到 `<MM_DD>/codex/plan/`）

### 触发场景
- “基于 intake 生成可执行计划”
- “写一个 `plan_<topic>.md`，带 DoD/Gates/Deliverables/Rollback”

### 输入（最小）
- 当天 intake 文件：`<MM_DD>/codex/intake/intake_<topic>.md`

### 输出
- 文件：`<MM_DD>/codex/plan/plan_<topic>.md`
- 必须块（固定）：

```md
# Plan: <topic>

## Goal
...

## Scope
- In:
- Out:

## Tasks
- [ ] T1 ...
  - DoD:
  - Dependencies:
- [ ] T2 ...
  - DoD:
  - Dependencies:

## Gates (optional)
- Gate1:
- Gate2:

## Deliverables
- <MM_DD>/codex/report/report_<topic>.md
- <MM_DD>/codex/artifact/manifest_<topic>.json
- (if needed) <MM_DD>/codex/daily/daily.md

## Rollback
- ...

## Execution Log
- (leave blank)
```

### 手工 SOP（你现在怎么做）
- Step 0：打开 `intake_<topic>.md`
- Step 1：把 Tasks 改写成“可执行动作”（动词开头）
- Step 2：为每个任务补 DoD（可验证）
- Step 3：写 Gates（可选，不强制也列出来）
- Step 4：写 Deliverables（必须落到当天文件夹内的具体路径）
- Step 5：写 Rollback（失败怎么退）
- Step 6：保存为 `plan_<topic>.md`

---

## 3) Skill：`artifact-manifest-writer`（输出到 `<MM_DD>/codex/artifact/`）

### 触发场景
- “把本轮改动/命令/结果写成 manifest”
- “生成 `manifest_<topic>.json`，并把 deliverables 指向当天目录”

### 输入（最小）
- 当天材料：改了哪些文件、跑了哪些命令、结果是什么
- 可选：plan/report 路径（作为证据链接）

### 输出
- 文件：`<MM_DD>/codex/artifact/manifest_<topic>.json`
- Schema（必须字段；内容可为空但 key 必须在）：

```json
{
  "run_id": "",
  "date": "<MM_DD>",
  "mode": "mixed",
  "topic": "",
  "tasks": [],
  "inputs": {},
  "changes": { "files_changed": [], "summary": "" },
  "commands": [],
  "verification": { "gates_passed": [], "gates_failed": [], "results": "" },
  "deliverables": [],
  "risks": "",
  "rollback": "",
  "next_backlog": []
}
```

### 手工 SOP（你现在怎么做）
- Step 0：收集当天材料：改了哪些文件、跑了哪些命令、结果是什么
- Step 1：把“改动”写成 `changes.files_changed[]`
- Step 2：把“命令”写进 `commands[]`
- Step 3：把“结果/验证”写进 `verification`
- Step 4：把“产物路径”写进 `deliverables[]`（必须是当天目录下）
- Step 5：写 `risks/rollback/next_backlog`
- Step 6：保存为 `manifest_<topic>.json`

---

## 4) Skill：`daily-vibe-update`（输出到 `<MM_DD>/codex/daily/` + `<MM_DD>/codex/todo/`）

### 触发场景
- “生成今天的日更 + 明日 todo”
- “把今天 Done/Blockers/Next/Evidence 写成 daily.md + todo.md”

### 输入（最小）
- 当天碎片进度（Done/Blockers/Next 的素材）
- 可选：report/manifest 路径（作为 Evidence）

### 输出
- 日更：`<MM_DD>/codex/daily/daily.md`
- 明日 todo：`<MM_DD>/codex/todo/todo.md`
- `daily.md` 必须块（固定）：

```md
# Daily <MM_DD>

## Summary
...

## Done
- ...

## Evidence
- <MM_DD>/codex/report/report_<topic>.md
- <MM_DD>/codex/artifact/manifest_<topic>.json

## Blockers
- ...

## Next
- See: <MM_DD>/codex/todo/todo.md
```

### 手工 SOP（你现在怎么做）
- Step 0：汇总当天 Done（必须对应产物或可验证结果）
- Step 1：列 Evidence（指向当天目录下的 report/manifest/关键文件/关键命令）
- Step 2：列 Blockers（原因+需要什么）
- Step 3：生成 Next（明日 Top5/Top10）写进 `todo/todo.md`
- Step 4：在 `daily.md` 里引用 `todo.md` 和 manifest/report 的路径

**todo 文件模板（固定）**

```md
# Todo (Next) for 12_31

## Top 10
1) ...
2) ...
3) ...
```

---

## 2) 给多个 skill / subagent 的“写入规则”（避免冲突）

* `daily.md`：当天只允许**一个合并者**写（建议 `daily-vibe-update`）
* `todo.md`：当天只允许**一个合并者**写（建议 `daily-vibe-update`）
* `intake_<topic>.md / plan_<topic>.md / report_<topic>.md / manifest_<topic>.json`：按 topic 分文件，**天然可并行**

---
