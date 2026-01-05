# Skills 生成计划（workflow-to-skill 驱动）

## 术语约定（避免混淆）

| 术语 | 定义 | 示例 |
|------|------|------|
| **Skill 源码目录** | 固定目录，存放可复用的 Agent Skill 定义 | `.codex/skills/<skill-name>/SKILL.md` |
| **产物输出目录** | 动态目录，每天的工作产物 | `<MM_DD>/codex/{intake,plan,report,artifact,daily,todo}/` |

## 当前状态

Sprint 1 四个技能（`intake-normalizer`/`plan-md-writer`/`artifact-manifest-writer`/`daily-vibe-update`）
已存在于 `.codex/skills/`，本轮任务为**验证与更新规格**。

---

## 目标
- 用已落地的元技能 `workflow-to-skill`，把你“真实手工步骤”抽取为一组可复用的 Codex Skills。
- 新技能统一落地到本仓库：`.codex/skills/<skill-name>/SKILL.md`（必要时再加 `scripts/`/`references/`/`assets/`）。

## 约束（默认）
- **先计划后执行**：仅生成计划与草案；在你确认前，不实际生成/修改其它技能文件。
- **安全优先**：默认不做不可逆操作（强推、删除、覆盖大文件、改主分支）；不做全仓格式化噪声变更。
- **技能规范**：每个 `SKILL.md` 的 YAML 头只包含 `name` 和 `description`；触发条件写进 `description`。

## 建议本轮先生成的 Skill 集（可裁剪）
按 `skill_config.md` 的“最小闭环”思路拆成 3 个 Sprint；你可以只选 Sprint 1。

### Sprint 1（L1 地基，强烈建议）
- [ ] `intake-normalizer`：把任意口水输入归一成统一 Intake 字段（Goal/Inputs/Constraints/Items）。
- [ ] `plan-md-writer`：把 Intake 生成可执行 `plan.md`（Tasks/DoD/Gates/Deliverables/Rollback）。
- [ ] `artifact-manifest-writer`：把执行结果写成 `manifest.json`（任务→输入→改动→验证→产物→风险回滚）。
- [ ] `daily-vibe-update`：把当日推进写成日更（Done/Blockers/Next/Evidence）。

### Sprint 2（L0 编排与执行）
- [ ] `plan-md-executor`：读取 `plan.md`，拆成可执行序列（含并行组、回滚点、证据要求）。
- [ ] `vibe-batch-orchestrator`：批量分诊→冲刺→收敛（固定输出：Triage/Sprint/Log/Deliverables/Next）。

### Sprint 3（按需：代码/论文专项）
- [ ] `repo-scout`：定位入口/依赖/关键路径（读代码、找配置、最小复现）。
- [ ] `patch-implementer`：按任务说明做最小改动（MVP 优先，变更可回滚）。
- [ ] `test-and-mre`：最小可复现示例（MRE）+ 单测/冒烟测试建议。
- [ ] `quality-lint-format`：仅对相关文件做 lint/format/static checks（避免全仓噪声）。
- [ ] `bib-cite-guardian`：cite key/bib 一致性检查与修复建议（如你有论文链路）。

## 对每个 Skill 的生成流程（标准作业）
对每个被勾选的 skill，按同一套“抽取→落地→验收”流程：
1) **你提供材料**（推荐用下面的模板；乱序也行）。
2) 我用 `workflow-to-skill` 抽取并输出：SOP 表格 / 分支树（含最小证据）/ 门禁 / 规格 / MVP / `SKILL.md` 草案。
3) **精炼草案**：把可变细节下沉到 `references/`，把确定性步骤脚本化到 `scripts/`（只有确实复用才加）。
4) **落地文件**：写入 `.codex/skills/<skill-name>/SKILL.md`（必要时创建资源目录）。
5) **验收用例**：至少 2 条“输入→期望输出结构”的文本用例；确认触发描述与输出契约稳定。

## 你需要提供的输入（每个 Skill 一份）
复制填写（最少填“手工步骤/验收方式/禁止项”也行）：
- Skill 名称候选（如已确定可留空）：
- 触发场景（用户会怎么说，关键词）：
- 成功标准（做到什么算完成）：
- 输入来源与示例（给 1-2 条真实输入）：
- 手工步骤（Step 0..N；越贴近真实越好）：
- 判断依据/经验规则（如何选A/B、如何判定完成）：
- 验收方式（你通常跑什么命令/看什么文件/看什么信号）：
- 禁止自动做的事（强推/删除/全仓格式化/改主分支等）：

## PHM-Vibench 可选门禁包（如果这些技能要服务本仓库）
如你确认需要把“仓库验收”写进技能门禁，我会默认引用这些（按任务选择其一/多）：
- `python main.py --config configs/demo/00_smoke/dummy_dg.yaml`
- `python -m scripts.validate_configs`
- `python -m pytest test/`

## 需要你确认的点（我收到确认后才开始生成技能）
1) 你本轮要生成哪些 skills（上面勾选即可；默认建议：Sprint 1 四个）。
2) 是否把 “PHM-Vibench 门禁包” 写入这些 skills 的 Quality Gates（是/否；若是，哪些命令）。
3) 每个被选 skill：你是否能提供至少 1 条真实示例输入 + 手工步骤（如果不能，我会用假设先出 v0.1 草案）。

ai 操控tmux 的skill 每个tumx 类似subagent 