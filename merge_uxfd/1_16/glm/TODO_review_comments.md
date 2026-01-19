# 1_15/codex/TODO.md 变更批判性 Review

**Review 日期**: 2026-01-16
**Review 对象**: `merge_uxfd/1_15/codex/TODO.md` 的 git diff

---

## Update（2026-01-16：已按建议修复）

本 Review 的主要问题（“过度承诺 / 不可验证 / submodule 语义不清”）已在后续改动中修复。

证据与落盘：
- `merge_uxfd/1_15/codex/TODO.md`（已加入可复现验证命令与验证日期）
- `merge_uxfd/1_16/codex/report/report_uxfd-merge.md`
- `merge_uxfd/1_16/codex/artifact/manifest_uxfd-merge.json`

---

## 总体评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 真实性 | ✅ 已验证 | 关键路径与入口文件可复现验证 |
| 准确性 | ✅ 已收敛 | 描述绑定真实开关/真实路径（best-effort） |
| 可追溯性 | ✅ 已补齐 | 增加验证命令 + 验证日期 + 证据文件 |

---

## 🔴 严重问题

### 1. 未经验证的代码路径声明

**行 13-20**: 添加 6 条进展，声称以下路径存在：

```markdown
- `src/model_factory/X_model/UXFD/fusion/`
- `src/model_factory/X_model/UXFD/fuzzy/`
- `src/model_factory/X_model/UXFD/operator_attention/`
- `src/model_factory/X_model/UXFD/neurosymbolic/`
- `trainer.extensions.predictions.enable=true`
- `trainer.extensions.agent.enable=true`
```

**问题**:
- 这些目录/配置真的存在吗？
- 未提供可复现证据时，读者无法判断“已实现”还是“计划中”

**建议修复**:
```markdown
- 逐条绑定：配置开关 + 代码路径 +（可选）最小验证命令
- 在 TODO.md 增加“证据（可复现验证命令）”小节，避免 [x] 不可验证
```

**修复后状态**: ✅ 已在 `merge_uxfd/1_15/codex/TODO.md` 增补“证据（可复现验证命令）”，并完成路径存在性验证。

---

### 2. 过度承诺：TSPN_UXFD 能力描述

**行 36**:
```markdown
- TSPN_UXFD 已支持可装配插槽：SP2D/Fusion/Fuzzy/OperatorAttention/Logic（best-effort）
```

**问题**:
- “支持哪些模块”需要绑定到明确的配置开关与代码路径，否则容易产生过度承诺
- "best-effort" 若不补充验证口径，会变成不可追溯的表述

**建议修复**:
```markdown
- 逐条列出模块与开关（例如 `model.uxfd.*` / `trainer.extensions.*`），并给出对应实现路径
- 如仍有未落地模块，应明确标注为“计划中”（并链接到计划文档）
```

**修复后状态**: ✅ `merge_uxfd/1_15/codex/TODO.md` 已改为“best-effort + 开关 + 路径”的可验证描述；核心实现位于
`src/model_factory/X_model/TSPN_UXFD.py`。

---

### 3. Paper 入口状态声明缺乏证据

**行 52**:
```markdown
> 结论：当前 7 个 submodule 已补齐 `configs/vibench/min.yaml` 与 `VIBENCH.md`（WP0 done）
```

**问题**:
- 主仓库 git diff 只显示 submodule 为 `-dirty`
- 无法验证具体文件是否真的存在
- 没有"何时验证、谁验证"的记录

**建议修复**:
```markdown
> 结论：当前 7 个 submodule 已补齐入口文件（WP0 done）
>
> 验证命令：
> ```bash
> find paper/UXFD_paper -path "*/configs/vibench/min.yaml" | wc -l  # 期望: 7
> find paper/UXFD_paper -maxdepth 2 -name "VIBENCH.md" | wc -l      # 期望: 7
> ```
>
> 验证日期：2026-01-16
```

**修复后状态**: ✅ 已在 `merge_uxfd/1_15/codex/TODO.md` 增加计数验证命令，并明确“WP0 完整 vs 可合并 PR 完整”的差异
（submodule 需在各自仓库内提交）。

---

## 🟡 中等问题

### 4. collect 脚本路径混淆

**行 32-33**:
```markdown
- `scripts/collect_uxfd_runs.py` 可扫描 `results/**/artifacts/manifest.json`
  并导出 `reports/uxfd_runs.csv`（默认参数是 `--input save`，本仓库建议显式用 `--input results`）
```

**问题**:
- 上游默认是 `--input save`
- 本仓库改为 `--input results`
- 没有解释为什么不同（是本仓库的特殊性？）

**建议**: 添加简短说明，如"本仓库使用 `results/` 作为输出目录"

**修复后状态**: ✅ 已补充说明：不要依赖脚本默认值；本仓库建议显式传参 `--input results`。

---

### 5. 表格状态更新时间线缺失

**行 43-49**: 表格状态从"缺失"→"已创建"

**问题**:
- 没有说明这些文件是什么时候创建的
- 无法追踪完成时间线

**建议**: 在表格或章节头部添加"最后更新：YYYY-MM-DD"

---

### 6. DoD "已通过"缺乏证据

**行 67**:
```markdown
DoD（已通过）：
```

**问题**:
- 没有记录哪个 paper 跑通了
- 没有记录跑通的日期
- 无法追溯验证结果

**建议**:
```markdown
DoD（已通过）：
- 验证日期：2026-01-15
- 验证 paper：1D-2D_fusion_explainable
- 命令：`python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1`
```

---

## 🟢 轻微问题

### 7. 进展条目格式不统一

**行 14-19**: 有的进展有路径 `见 src/...`，有的没有

**建议**: 统一格式，或为每个进展添加验证命令

---

## 需要验证的声明汇总

在提交前，请验证以下路径是否存在：

| 声称的路径 | 验证命令 | 状态 |
|-----------|----------|------|
| `src/model_factory/X_model/UXFD/fusion/` | `ls -la src/model_factory/X_model/UXFD/fusion/` | ✅ |
| `src/model_factory/X_model/UXFD/fuzzy/` | `ls -la src/model_factory/X_model/UXFD/fuzzy/` | ✅ |
| `src/model_factory/X_model/UXFD/operator_attention/` | `ls -la src/model_factory/X_model/UXFD/operator_attention/` | ✅ |
| `src/model_factory/X_model/UXFD/neurosymbolic/` | `ls -la src/model_factory/X_model/UXFD/neurosymbolic/` | ✅ |
| `scripts/collect_uxfd_runs.py` | `ls -la scripts/collect_uxfd_runs.py` | ✅ |
| `paper/UXFD_paper/*/configs/vibench/min.yaml` | `find paper/UXFD_paper -path "*/configs/vibench/min.yaml" | wc -l` | ✅（7） |

---

## 建议的修复优先级

| 优先级 | 问题 | 影响文件 |
|--------|------|----------|
| P0 | 区分"已实现"vs"计划中" | TODO.md 行 13-20, 36 |
| P0 | 添加验证命令和日期 | TODO.md 行 52, 67 |
| P1 | 解释 collect 脚本路径差异 | TODO.md 行 32-33 |
| P2 | 统一进展条目格式 | TODO.md 行 14-19 |

---

## 结论

本 Review 指出的问题已按建议修复：`TODO.md` 已收敛为“可验证口径”（best-effort + 开关 + 路径 + 证据 + 日期）。
