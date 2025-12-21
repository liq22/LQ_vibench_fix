# 执行记录（12_15）

本目录用于记录 12_15 的“清晰化/可上手/可复现”改造实际落地情况（以仓库当前状态为准）。

## 1) 已落地（与仓库一致）

### A. config SSOT + 工具链（registry → atlas → inspect → validate）
- 扩展 `configs/config_registry.csv`（追加列，不破坏原列）。
- 新增 `docs/config_registry_schema.md`（解释新增列格式）。
- 新增 `scripts/gen_config_atlas.py` + 生成 `docs/CONFIG_ATLAS.md`。
- 新增 `scripts/config_inspect.py`（resolved/sources/targets/sanity）。
- 新增 pydantic schema：`src/config_schema/*`；新增 `scripts/validate_configs.py`。

### B. “30 秒可跑”离线 smoke demo（无需下载数据）
- 新增 `data/raw/Dummy_Data/*.csv` + 复用 `data/metadata_dummy.csv`。
- 新增 `configs/demo/00_smoke/dummy_dg.yaml`（CPU 友好；用于真实端到端冒烟）。

### C. configs/ README 体系（模板 + 复制可用命令）
- 新增 `configs/README.md`、`configs/base/README.md`、`configs/demo/README.md`。
- 新增 `configs/base/{environment,data,model,task,trainer}/README.md`（固定结构模板）。
- 新增各 demo 子目录 README（`configs/demo/*/README.md`）。

### D. 顶层文档与贡献指引消歧义
- `README.md` / `README_CN.md`：新增离线 smoke 命令；统一指向 `configs/README.md` 与 config 工具链。
- `CONTRIBUTING.md`：修正不存在的 `tests/`、`requirements-dev.txt`、`pip install -e .` 等指引，统一到 `test/` + `dev/test_history`（可选）。
- `docs/testing.md`：把 `dev/test_history` 明确为 legacy runner（可选）。
- `docs/hse-implementation/*`：移除不存在的 `tests/**` 路径引用，并把 paper 级脚本标注为 TODO（计划迁移到 submodule）。

### E. CI 与最小单测
- 新增 `.github/workflows/config_tools_ci.yml`：
  - `python -m scripts.validate_configs`
  - `python -m scripts.gen_config_atlas` + `git diff --exit-code docs/CONFIG_ATLAS.md`
  - `python -m scripts.config_inspect ...`
  - `pytest -q test/test_config_tools.py`
- 新增 `test/test_config_tools.py`（validate/inspect/atlas 的最小保障）。

## 2) 当前建议的复核命令（本机）

```bash
python -m scripts.validate_configs
python -m scripts.config_inspect --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
python -m scripts.gen_config_atlas && git diff --exit-code docs/CONFIG_ATLAS.md
python -m pytest -q test/test_config_tools.py
```

## 3) 未落地/待确认（仍是 TODO）

- `configs/reference/` 是否整体迁移到 paper submodule（当前已在文档标注“legacy / planned removal”，但未做目录迁移）。
- `streamlit_app.py` 可视化能力：当前文档标注实验性，但功能仍未形成“稳定验收点”；是否保留在主 README、或迁移到 submodule，需要团队确认。
