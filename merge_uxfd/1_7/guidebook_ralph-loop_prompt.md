# Guidebook: `/ralph-wiggum:ralph-loop` Prompt (UXFD docs → SSOT)

用途：将 UXFD 合并/迁移文档整理为“新人 30 分钟上手”的 SSOT 文档集，并明确如何把
`/home/user/LQ/B_Signal/Unified_X_fault_diagnosis` 合理并入当前仓库的 `src/model_factory/`。

> 直接复制下面整段内容到 `claude code` 里执行即可。

---

```text
/ralph-wiggum:ralph-loop
你是一个“仓库合并文档整理 + 上手指南”专用工程师。你的任务不是写一堆长文，而是把 UXFD 合并/迁移的文档整理到足够清晰，让一个完全不了解仓库的新同学在 30 分钟内能：
1) 明白要把 /home/user/LQ/B_Signal/Unified_X_fault_diagnosis 合并到当前仓库的哪里（src/model_factory/...）
2) 知道最小可跑通的验证路径（pilot + min.yaml + 1 epoch + manifest）
3) 知道下一步按什么顺序迁移哪些文件/模块（Copy + Adapter），以及每一步的 DoD/门禁
4) 不需要阅读旧的“12_23 这种超长计划”也能开始干活

背景与约束（必须遵守）：
- 当前仓库是 config-first：入口只用 `python main.py --config <yaml> [--override key=value ...]`。
- 不新增 YAML 第 6 个一级 block；开关放 `trainer.extensions.*`。
- 迁移策略：Copy + Adapter（先跑通、再优化），避免一次性重构。
- 目标落位：可复用实现统一到主仓库 `src/model_factory/`（优先 `src/model_factory/X_model/UXFD_component/**` 及其 registry 体系）。
- paper submodule（paper/UXFD_paper/*）只保留 YAML 配置、实验脚本、说明文档（VIBENCH.md/README），不放核心实现。
- 文档必须避免写死绝对路径：用 `export UXFD_UPSTREAM=/home/user/LQ/B_Signal/Unified_X_fault_diagnosis` 这类环境变量表达。
- 你可以保留旧文档作为 archive，但必须提供“新人只看这 2~3 份文档就够”的入口索引。

你要产出的最终交付（SSOT，必须落盘）：
A) `paper/LQ_vibench_fix/merge_uxfd/README.md`：更新成“唯一入口索引”，首屏就告诉新人：从哪里开始、3 个最短命令、最小 DoD。
B) `paper/LQ_vibench_fix/merge_uxfd/00_quickstart.md`：一页 Quickstart（<= 120 行）：
   - What/Why：一句话目标 + 迁移边界
   - Where：上游 repo 与主仓库落位（路径图 + 简短说明）
   - How：最小跑通步骤（pilot/min.yaml/1 epoch/manifest/postrun/collect）
   - Troubleshooting：常见坑（shape/layout、fft magnitude、依赖缺失、registry 找不到）
C) `paper/LQ_vibench_fix/merge_uxfd/01_porting_playbook.md`：可执行迁移手册（面向实现者）：
   - “从上游哪个文件 -> 主仓库哪个目录/模块”的映射表（必须表格化）
   - 迁移顺序（按 pilot 依赖）：SP2D -> Fusion1D2D -> (attention/fuzzy/logic as-needed) -> HookStore -> explain summary
   - 每步 DoD（可验证：命令/文件/日志关键字）
   - 需要更新的 registries/配置字段（列点）
D) 旧文档处置：在 `paper/LQ_vibench_fix/merge_uxfd/12_23/ops_library_completion_plan.md` 等旧文档顶部加“Deprecated/Archive + 指向新 SSOT 文档”的短提示（不删内容，但避免新人走弯路）。

质量门禁（每轮循环必须自检，直到满足）：
- 新文档必须是“拷贝就能跑”的命令（路径正确、引用文件存在）。
- 新文档中不得出现旧路径 `paper/UXFD_paper/merge_uxfd/...`（现在都在 `paper/LQ_vibench_fix/merge_uxfd/...`）。
- Quickstart 必须 <= 120 行；Playbook 允许更长但要结构清晰，表格优先。
- README 必须给出“新人只看哪 2~3 个文件”的最短阅读路径。
- 文档中的 DoD 必须可验证（例如 manifest 路径、config_inspect、validate_configs、collect_uxfd_runs 输出等）。
- 你每轮输出都要给：1) 你改了哪些文件；2) 为什么；3) 还差什么没满足（用 checklist）。

执行方法（循环策略）：
1) 先扫描现有 merge_uxfd 文档树，找出重复/冲突/过长/依赖上下文的部分，写出“信息架构”重组方案（最多 10 行）。
2) 先写 A+B（README + Quickstart），再写 C（Playbook），最后做 D（旧文档顶部加 deprecate 指针）。
3) 每写完一个文件，立刻用 ripgrep 检查旧路径引用、断链、行数等。
4) 如果出现不确定（例如 pilot 应该选哪篇、UXFD_component 是否最终命名），先在 README/Playbook 用“Decision Needed”小节列出来，并指向 `paper/LQ_vibench_fix/merge_uxfd/12_27/codex/DECISIONS_NEEDED.md`，不要瞎定。

你不需要在这一轮真正迁移代码；你的核心产出是“让新人能开干”的清晰文档与执行手册。
开始执行，直到上述门禁全部通过为止。
```

