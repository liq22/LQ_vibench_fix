# 6 个 demo 配置检查报告（12_15）

检查目标：
- 6 个 demo YAML 是否存在、能否通过 `load_config()` 合并 base_configs
- 是否存在明显“描述/命名与配置不一致”的 bug

检查对象（v0.1.0 demo）：
1. `configs/demo/01_cross_domain/cwru_dg.yaml`
2. `configs/demo/02_cross_system/multi_system_cddg.yaml`
3. `configs/demo/03_fewshot/cwru_protonet.yaml`
4. `configs/demo/04_cross_system_fewshot/cross_system_tspn.yaml`
5. `configs/demo/05_pretrain_fewshot/pretrain_hse_then_fewshot.yaml`
6. `configs/demo/06_pretrain_cddg/pretrain_hse_cddg.yaml`

## 1) 静态加载结果

结论：6/6 均可被 `src/configs/config_utils.load_config()` 成功加载，且具备 `environment/data/model/task/trainer` 五个必需段。

## 2) 发现的 demo 级问题（bug/不一致）

### Demo #1 `configs/demo/01_cross_domain/cwru_dg.yaml`
- 早期版本标题/文档写 “CWRU → Ottawa”，但配置本身只体现 `target_system_id + domain split`，无法保证 “Ottawa”
- 已将 README/README_CN 与 demo 文件头部描述修正为“单系统 + domain split”的 DG 示例，避免硬编码 Ottawa

建议（后续可选）：
- 若确实要提供 “CWRU → Ottawa” 的跨系统 demo，需要先明确并固化 metadata 中 `Dataset_id` 映射来源，再调整 `task.target_system_id` 并补充说明。

### Demo #2 `configs/demo/02_cross_system/multi_system_cddg.yaml`
- 默认 `task.target_system_id: [1]` 实际只选了单系统；多系统需要用户自行扩展 id 列表
- 已将 demo 文件头部描述修正为“可通过 target_system_id 调整为 multi-system”，避免误导

### Demo #3 `configs/demo/03_fewshot/cwru_protonet.yaml`
- 未显式覆盖 `environment`，因此会继承 `configs/base/environment/base.yaml`（`project: demo_project`、`output_dir: results/demo`）

建议（可选）：
- 为 demo 增加独立 `environment.project/output_dir`，便于结果区分。

### Demo #4 `configs/demo/04_cross_system_fewshot/cross_system_tspn.yaml`
- 配置自洽（GFS task + 目标系统列表 + `num_epochs: 1`），无明显结构性问题。

### Demo #5 `configs/demo/05_pretrain_fewshot/pretrain_hse_then_fewshot.yaml`
- 文件名/标题含 “two-stage”，但 YAML 本身不含 `stages`，Pipeline_02 会按“单阶段模式”运行（该点在 YAML 注释中已说明）

建议：
- 文档侧避免称其为“two-stage”，除非补全 `stages` 或提供 second-stage 配置。

### Demo #6 `configs/demo/06_pretrain_cddg/pretrain_hse_cddg.yaml`
- 使用 `Pipeline_01_default` 运行 `pretrain` 任务，静态上可加载且结构自洽。
- 是否逻辑上应切到 `Pipeline_02_pretrain_fewshot` 取决于你们对“pretrain”任务的统一入口约定（需团队确认）。

## 3) README 里的 6 个 demo 命令是否有“明显 bug”

命令格式本身是可用的：
- `python main.py --config <yaml> --override trainer.num_epochs=1 --override data.num_workers=0`

README/README_CN 中 Demo #1/#2 的“语义描述”已与配置对齐。
