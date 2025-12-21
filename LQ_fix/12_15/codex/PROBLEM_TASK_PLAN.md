# 分析问题 - 设置任务 - 制定计划（12_15）

本文件用于把“发现的问题”转成“可执行任务”，并给出 12_15 的更新计划与验收标准。

## 1. 分析问题（Problem Analysis）

### 1.1 文档与仓库现状不一致（会误导/导致命令失败）

检查范围：
- `README.md`、`README_CN.md`
- `CLAUDE.md`、`CLAUDE_CN.md`
- `AGENTS.md`

主要问题：
1. **Demo 语义与配置不一致**
   - Demo #1 文档写 “CWRU → Ottawa”，但 `configs/demo/01_cross_domain/cwru_dg.yaml` 只显式指定 `target_system_id: [1]` + domain split，无法从配置本身保证“Ottawa”。
   - Demo #2 文档写 “multi-system”，但 `configs/demo/02_cross_system/multi_system_cddg.yaml` 只配置了 `target_system_id: [1]`（单系统）。
2. **路径/文件名不兼容**
   - 文档中存在旧版路径（如 `configs/demo/Single_DG/...`、`configs/demo/Multiple_DG/...`），当前仓库对应内容在 `configs/v0.0.9/demo/...` 或 `configs/demo/...`。
   - 历史文档中存在 `configs/readme.md`/`configs/README.md` 混用；当前维护入口已统一为 `configs/README.md`（`configs/readme.md` 标注为 legacy）。
   - HSE / Pipeline_03 等 paper 级 `scripts/*` 不属于主仓库入口，需迁移到 paper submodule（避免与主程序/主 demo 混淆）。
3. **CLI 参数不一致**
   - 历史文档曾出现 `python main.py --pipeline ...` 示例，但当前 `main.py` 不支持 `--pipeline`（pipeline 由 YAML 内 `pipeline:` 字段决定）；现已在顶层指引中移除该示例。
4. **硬编码环境路径**
   - `configs/base/environment/base.yaml` 中 `PROJECT_HOME` 为开发机绝对路径，容易误导使用者（文档应说明需要按机器修改或建议用相对/环境变量策略）。

### 1.2 6 个 demo 的“配置级”检查结论

对象：
- `configs/demo/01_cross_domain/cwru_dg.yaml`
- `configs/demo/02_cross_system/multi_system_cddg.yaml`
- `configs/demo/03_fewshot/cwru_protonet.yaml`
- `configs/demo/04_cross_system_fewshot/cross_system_tspn.yaml`
- `configs/demo/05_pretrain_fewshot/pretrain_hse_then_fewshot.yaml`
- `configs/demo/06_pretrain_cddg/pretrain_hse_cddg.yaml`

静态结论：
- 6/6 均可 `load_config()` 成功合并 `base_configs`，并具备 `environment/data/model/task/trainer` 五段结构。
- 其中 Demo #1/#2 存在“描述/命名与配置语义不一致”的文档级问题（见上）。

## 2. 设置任务（Task Definition）

### T1：修正文档中“会直接失败”的内容（P0）

覆盖文件：
- `README.md`、`README_CN.md`
- `CLAUDE.md`、`CLAUDE_CN.md`
- `AGENTS.md`

范围：
- 修正路径（旧 demo → `configs/v0.0.9/demo/...` 或 `configs/demo/...`）
- 移除/降级 paper 级脚本入口（HSE 论文级脚本计划迁移到 paper submodule；主仓库不作为必跑验证入口）
- 明确 maintained configs 文档入口（`configs/README.md`；`configs/readme.md` 仅 legacy 备注）
- 修正文档示例命令参数（移除/替换 `--pipeline`）

### T2：修正文档中“语义误导”的 demo 描述（P1）

重点：
- Demo #1：CWRU→Ottawa 的表述与配置不一致
- Demo #2：multi-system 的表述与配置不一致

输出形式（两种可选策略，需你确认采用哪一种）：
- 策略 A（推荐）：调整文档措辞，不再写死 “CWRU→Ottawa / multi-system”，改为“DG/CDDG 示例（具体系统由 metadata + target_system_id 决定）”
- 策略 B：调整 YAML，使之确实对应文档描述（前提是 dataset_id 映射稳定且团队认可）

### T3：对 6 个 demo 做“可运行性”检查清单（P1）

说明：
- 由于缺少数据集/环境不确定，默认只做“结构校验 + 关键字段一致性校验”，不强行跑训练。
- 若你提供可用数据路径与最小运行约束，可升级为“最小运行验证（num_epochs=1）”。

## 3. 制定计划（Execution Plan）

### Step 1：补充 12_15 文档修复清单（本目录已具备）
- 计划入口：`docs/LQ_fix/12_15/codex/README_COMPAT_PLAN.md`
- demo 检查入口：`docs/LQ_fix/12_15/codex/DEMO6_CHECK_REPORT.md`

### Step 2：执行 P0 文档修复（让命令/路径不再报错）
- 新增离线 smoke demo（不依赖下载数据）：`configs/demo/00_smoke/dummy_dg.yaml`
- 修正 `CLAUDE.md` / `CLAUDE_CN.md` 的 demo 路径与 `--pipeline` 示例（主入口统一为 `python main.py --config ...`）
- 修正 `README.md` / `README_CN.md` 的配置入口指向（统一到 `configs/README.md` + config 工具链）

### Step 3：执行 P1 文档语义修复（避免误导）
- Demo #1 / #2 的文案按“策略 A/B”修正
- 若采用策略 B，同步修改对应 YAML，并在文档中写清 dataset_id 的来源与约束

### Step 4：输出“6 demo 的 bug 清单 + 建议”
- 将 demo 的问题点汇总为 checklist（每项包含：文件、字段、影响、建议）

## 4. 验收标准（Acceptance Criteria）

### 文档一致性
- 文档中的仓库内路径（configs/docs/dev/scripts）均存在且可点击打开
- README 中 6 个 demo 命令与当前 `main.py` 的参数体系一致

### demo 语义一致性
- Demo #1/#2 的“标题/描述”与配置一致（要么改文档，要么改配置）

## 5. 当前状态与下一步

当前：
- 计划与检查报告已输出到 `docs/LQ_fix/12_15/codex/`（见 `README.md`）。

下一步：
- 默认按策略 A（推荐）：README 不写死 Ottawa / multi-system；用 “metadata + target_system_id 决定” 的表述保持可复现与不误导。
