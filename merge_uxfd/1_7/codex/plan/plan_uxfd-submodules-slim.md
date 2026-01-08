# Plan: uxfd-submodules-slim

## Goal
把 7 个 UXFD paper submodule 收敛为“配置/脚本/文档仓”，将可复用实现统一迁入主仓库 `src/`，并用门禁保证每篇 paper 的 `min.yaml` 持续可跑通。

## Scope
- In:
  - `paper/UXFD_paper/1D-2D_fusion_explainable`
  - `paper/UXFD_paper/Explainable_FD_Toolkit`
  - `paper/UXFD_paper/LLM_Explainable_FD_Toolkit`
  - `paper/UXFD_paper/MOE_explainable`
  - `paper/UXFD_paper/Neuralsymbolic_theory`
  - `paper/UXFD_paper/Paper_fuzzy_XFD`
  - `paper/UXFD_paper/TII_operator_attention`
- Out:
  - 一次性完成所有 paper 的论文级复现与指标对齐（后续按 WP 推进）
  - 未经确认的目录大改名/大重构（保持渐进式）

## Tasks
- [ ] T1 定义“submodule 允许保留文件”白名单 + 目录规范
  - DoD:
    - 形成 1 份可执行规则（白名单 + 例外处理）并写入文档（建议放 `paper/LQ_vibench_fix/merge_uxfd/12_21/codex/submodule_config_conventions.md` 的增补或在各 submodule README/VIBENCH.md 引用）。
  - Dependencies:
    - 无
- [ ] T2 对 7 个 submodule 做 inventory，输出迁移清单
  - DoD:
    - 每个 repo 一页清单：Keep / Move-to-main / Delete / Legal/License notes / Owner。
    - 明确哪些代码属于“可复用实现（必须进主仓库）”，哪些属于“paper 私有参数（留在 YAML）”。
  - Dependencies:
    - T1
- [ ] T3 选 1 篇 pilot 跑通端到端迁移链路（推荐 `1D-2D_fusion_explainable`）
  - DoD:
    - pilot submodule 内存在 `configs/vibench/min.yaml` + `VIBENCH.md`，并可在主仓库根目录跑通 1 epoch。
    - 产物闭环：`<run_dir>/artifacts/manifest.json` 存在；`python -m scripts.collect_uxfd_runs` 可汇总到 CSV。
  - Dependencies:
    - T2
- [ ] T4 将 pilot 的可复用代码迁入主仓库并完成 registry/入口对齐
  - DoD:
    - 迁入后 pilot 仍可跑通；submodule 中对应实现被删除或替换为文档指引（不再双份 SSOT）。
  - Dependencies:
    - T3
- [ ] T5 将规范推广到其余 6 个 submodule（逐个收敛）
  - DoD:
    - 每个 submodule 都只保留配置/脚本/文档；各自 `min.yaml` 均可跑通 1 epoch。
  - Dependencies:
    - T4
- [ ] T6 建立门禁（批量验证 7 个 `min.yaml`）
  - DoD:
    - 有 1 个可重复执行的验证方式：一条命令批量跑（或至少顺序跑）7 个 `min.yaml`，输出每个 paper 的 PASS/FAIL 与 run_dir。
  - Dependencies:
    - T5

## Gates (optional)
- `python -m scripts.validate_configs`（主仓库配置体系不被破坏）
- `python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`（主仓库 smoke 不退化）
- `python -m pytest test/`（如本次变更触及 `src/` 或 `scripts/`）

## Deliverables
- paper/LQ_vibench_fix/merge_uxfd/1_7/codex/intake/intake_uxfd-submodules-slim.md
- paper/LQ_vibench_fix/merge_uxfd/1_7/codex/plan/plan_uxfd-submodules-slim.md

## Rollback
- 若迁移中途破坏任一 paper 的可运行性：优先回退到“submodule 仍保留必要代码”的过渡态，并在主仓库侧加 shim/adapter；待门禁稳定后再继续删除 submodule 代码。

## Execution Log

