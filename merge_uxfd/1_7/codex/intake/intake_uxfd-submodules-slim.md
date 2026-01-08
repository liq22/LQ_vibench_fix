# Intake: uxfd-submodules-slim

- Goal: 将 7 个 UXFD paper submodule 收敛为“只承载实验入口”的轻量仓库（YAML 配置/实验脚本/说明文档），把可复用代码与算子实现统一迁入主仓库 `src/`，降低重复与漂移，并保证每篇 paper 仍可一键复现实验。
- Scope:
  - In: `paper/UXFD_paper/*`（7 个 submodule）目录结构瘦身与规范化；把“通用/可复用”的模型/算子/工具代码迁入主仓库；更新各 paper 的 `min.yaml`/脚本/文档以依赖主仓库实现。
  - Out: 立刻做论文级复现/指标对齐的全面回归；一次性重构所有模型（保持 Copy+Adapter 的渐进策略）。
- Tasks:
  - T1: 定义 submodule 允许保留的文件白名单（例如：`configs/**`、`scripts/**`、`README*`、`VIBENCH.md`、`LICENSE`、`CITATION.cff`、`assets/figures/**`）。
  - T2: 对 7 个 submodule 做 inventory（逐仓库列出：应保留/应迁移/可删除/需保留为 legacy reference 的项），形成迁移清单。
  - T3: 在主仓库为“可复用实现”确定落位与注册策略（优先 `src/model_factory/X_model/UXFD_component/**` + 现有 registry），并明确“paper 个性化参数只放 submodule configs”。
  - T4: 迁移代码到主仓库（按依赖优先级分批：先 pilot 必需模块），并在 submodule 侧删除对应代码或改为文档指引/薄 wrapper（如确实需要）。
  - T5: 统一每个 submodule 的最小实验入口（建议固定为 `configs/vibench/min.yaml` + `VIBENCH.md`），并提供 `python main.py --config ...` 的可运行验证命令。
  - T6: 建立“兼容性门禁”（每次主仓库改动后快速验证 7 个 submodule 的 `min.yaml` 至少能跑通 1 epoch，并产出 `manifest.json`）。
- Priority: P0=定义白名单+inventory → P1=pilot（1 篇）先跑通迁移链路 → P2=推广到剩余 6 篇 + CI 门禁。
- Due: TBD
- Owner: LQ
- Background:
  - 当前 7 个 paper repo 结构各异，存在重复实现与漂移风险；将复用代码集中到主仓库可降低维护成本，并让配置成为唯一入口（config-first）。
  - 风险在于：submodule 不再“自包含可运行”，必须通过文档与门禁保证复现路径清晰且不会被主仓库变更破坏。
- Details:
  - 合理性判断：该策略总体合理，前提是建立清晰的接口边界与回归门禁：
    - submodule 只负责：实验配置（YAML）、运行脚本（调用主仓库入口）、paper 说明文档（VIBENCH.md/README）。
    - 主仓库负责：所有可复用 Python 代码（模型/算子/训练扩展/数据适配/解释与报告工具）。
  - 兼容性策略建议：
    - 先选 1 篇 pilot（建议 `paper/UXFD_paper/1D-2D_fusion_explainable`）跑通“迁移前→迁移后”的闭环，再复制规范到其余 6 篇。
    - 对必须保留的 paper 私有逻辑：优先参数化进入 YAML；确实无法参数化的，集中到主仓库并通过 `model.preset`/registry 区分。
  - 版本追溯建议：每个 submodule 的 `VIBENCH.md` 记录“验证时使用的主仓库 commit hash + 子模块 commit hash”，并在 `manifest.json`（或 config snapshot）中写入 `git describe` 信息（如已有）。
- Acceptance / DoD:
  - 7 个 submodule 均存在 `configs/vibench/min.yaml` 与 `VIBENCH.md`，且均可在主仓库根目录通过 `python main.py --config <...> --override trainer.num_epochs=1` 跑通（至少 1 epoch）。
  - submodule 目录中不再包含可复用核心实现（模型/算子主逻辑），对应实现已在主仓库 `src/` 有单一来源（SSOT）。
  - 至少有 1 个自动/半自动门禁脚本可批量验证 7 个 `min.yaml`（失败可定位到具体 paper/config）。
- Notes:
  - 迁移要避免一次性“大重构”，遵循 Copy+Adapter（先跑通后优化）。
  - 若某 paper repo 有必须保留的第三方代码/许可证限制，需要在 inventory 阶段标注并单独处理（可能 Out-of-scope）。
- Evidence:
  - paper/LQ_vibench_fix/merge_uxfd/1_7/codex/intake/intake_uxfd-submodules-slim.md
  - paper/LQ_vibench_fix/merge_uxfd/12_21/codex/submodule_config_conventions.md
  - paper/LQ_vibench_fix/merge_uxfd/12_23/TODO_BACKLOG.md

Next: plan-md-writer
