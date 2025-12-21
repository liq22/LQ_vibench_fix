你是该仓库的核心代码维护 Agent（偏工程化 + 论文复现友好）。
目标：对 PHM-Vibench 的 src/model_factory 做一次“可组合、可注册、可校验、可复现、可扩展”的升级，
并把 SOTA 时间序列/PHM 模型抽象为 Embedding / Backbone / TaskHead，整合进 ISFM 模块。

========================
A. 必读与约束（强制）
========================
1) 在修改任何目录前：先读取离你最近的 AGENTS.md（repo 根、configs/、src/*_factory/ 可能都有）。
2) schema 统一使用 Pydantic（不要引入 Hydra/OmegaConf 以外的新配置体系）。
3) 不新增任何 “latex 导出脚本”（不新增 scripts/export_latex.py）。
4) 若 docs/recipes/PAPER_REPRO.md 已存在：只做“清晰度与一致性”改造，不改变其核心内容：
   - 统一命令风格（同样的 --config / override 写法）
   - 明确固定 seed、固定 output_dir 的写法
   - 明确数据缓存/环境/版本/日志 checklist
   - 确保 recipe 被 README 与 configs/README.md 正确链接到（不要藏角落）
5) config 的单一事实源：configs/config_registry.csv + 自动生成 docs（如已有 scripts/gen_config_atlas.py 等工具就复用）。
   新增/调整 model config 时：必须更新 registry（id/category/path/description/pipeline/...）。
6) 允许新增极少量脚本（如 model_inspect.py），但必须：
   - 命名清晰、帮助信息完整、README 有入口
   - 有最小单测覆盖（pytest）
7) 修改 CLAUDE.md：作为“人类协作指南 + agent 约束说明”，与分层 AGENTS.md 互补，不重复堆字。

========================
B. 你要交付的最终成果（验收清单）
========================
[结构]
- src/model_factory/ 下形成清晰的三层结构：
  embeddings/  backbones/  heads/  （以及 isfm/ 或 isfm_builder.py）
- 统一输出 ModelOutput（dict 或 dataclass），至少含 pred/repr/aux（repr/aux 可为空）

[能力]
- ISFM（Industrial Signal Foundation Model）可用 config 组合：
  embedding + backbone + head
- 至少内置 4 个 Embedding、4 个 Backbone、6 个 Head（轻量实现即可，重点是接口统一）
- 至少提供 5 个可跑 demo config（含 smoke/dummy 数据）
  - 分类：InceptionTime 或 ROCKET baseline
  - 预测：PatchTST-like、iTransformer-like
  - ISFM-minimal：可组合示例
  - 额外：RUL head 最小示例（能在 dummy 上跑通即可）
- foundation models（TimesFM/Chronos/Moirai/MOMENT）以 “Wrapper/Adapter” 形式接入（可选依赖），不重写外部模型；
  wrapper 只做依赖检测与 I/O 适配，保持仓库可离线最小运行。

[文档（本科生友好）]
- src/model_factory/README.md：
  - 解释：模型=Embedding+Backbone+Head
  - 3 条最常用命令（train/eval/inspect）
  - “如何新增一个模型组件（3 步）”
- configs/model/README.md：
  - 列出所有模型 config（按任务/复杂度分组）
  - 对每个模型：适用场景、输入输出、计算开销大致级别
- 根 README.md 与 configs/README.md 必须链接到 docs/recipes/PAPER_REPRO.md（如果存在）
- 分层 AGENTS.md：repo 根 + configs/ + src/model_factory/ 至少三处
  - 每个写：setup、常用命令、测试命令、风格规范、禁止事项

[测试与CI]
- pytest：至少 1 个 “构建+前向” 单测覆盖 ISFM-minimal
- pytest：至少 1 个 “config 校验/registry 对齐” 单测（复用已有 validate/config_tools）
- CI 工作流如已存在：扩展而非新起炉灶

========================
C. 实施步骤（按顺序做，不要跳）
========================
Step 0：现状审计（只读）
- 列出 src/model_factory 当前入口函数、已有模型、输出格式、与 task_factory 的接口契约
- 列出当前 config 中 model 字段写法与路径（在哪些 yaml）

Step 1：定义接口契约（先写 schema + type）
- 定义 Pydantic：
  - EmbeddingConfig / BackboneConfig / HeadConfig / ISFMConfig
- 定义抽象基类或 Protocol：
  - BaseEmbedding.forward(x, mask=None, meta=None) -> Tokens
  - BaseBackbone.forward(tokens, token_mask=None, meta=None) -> Hidden
  - BaseHead.forward(hidden, meta=None) -> pred
- 定义统一 ModelOutput（包含 pred/repr/aux）

Step 2：搭建 registry 与 builder
- 在 model_factory 内建立 registry（按 name -> class）
- 实现 build_embedding/build_backbone/build_head
- 实现 build_isfm（由 cfg 组装三件套）

Step 3：落地最小可运行组件（轻量即可）
Embedding 至少实现：
- RawConvEmbed（新手友好）
- PatchEmbed（对齐 PatchTST/MOMENT）
- VarTokenEmbed（对齐 iTransformer 思路）
- SpectralEmbed（FFT/STFT 或可学习滤波器，最小版）
Backbone 至少实现：
- TransformerEncoderBackbone
- InvertedTransformerBackbone（实现最小 iTransformer-like）
- SSMBackbone（可极简；或先留接口+占位实现）
- FoundationWrapperBackbone（统一 wrapper 接口，内部可路由 TimesFM/Chronos/Moirai/MOMENT）
Head 至少实现：
- ClsHead / RegHead / ForecastHead / RULHead / AnomalyHead / DomainHead（domain 可先最小版）

Step 4：补齐 demo configs + registry 条目
- 在 configs/ 下新增（或调整）model 配置文件，全部登记到 configs/config_registry.csv
- 每个 demo 都要能在离线 dummy 数据上跑通（冒烟级别）

Step 5：新增/完善 model_inspect 工具（如确有必要）
- 功能：给定 config，打印：
  - 模型组件树（embedding/backbone/head）
  - 参数量、输入输出 shape、设备与 dtype
  - 一次前向的输出 keys
- 必须配 README 入口 + pytest 覆盖

Step 6：PAPER_REPRO 对齐（不新增 latex 导出）
- 如果 docs/recipes/PAPER_REPRO.md 已存在：
  - 只做命令风格统一、seed/output_dir 写法明确、checklist 完整、并确保 README 链接可达

Step 7：AGENTS.md + CLAUDE.md
- 分层 AGENTS.md：补齐 setup/常用命令/测试/风格/禁止事项
- CLAUDE.md：写“协作与agent约束”，与 AGENTS.md 互补（不要重复）

========================
D. 质量红线（出现即返工）
========================
- 模型输出格式不统一（某些模型返回 tuple，某些返回 dict）
- 新增模型必须改动大量 task 代码（说明接口设计失败）
- demo config 跑不通或 registry 未登记
- 文档只有“开发者视角”，没有新手路径
- PAPER_REPRO 链接找不到或命令写法前后不一致
