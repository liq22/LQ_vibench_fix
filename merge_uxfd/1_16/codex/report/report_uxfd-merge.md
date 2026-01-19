# Report: uxfd-merge (1_16)

## Question
7 个 UXFD paper 目前完整吗？

## Answer (definition-based)
- **WP0 入口完整（工作区层面）**：是。7/7 submodules 均存在 `configs/vibench/min.yaml` 与 `VIBENCH.md`。
- **“可合并 PR 完整”**：尚未。上述文件属于 submodule，需要在各 submodule 仓库内提交；父仓库只能更新 gitlink 指针。

## Verification (commands + expected outputs)

### 1) 入口文件计数
```bash
find paper/UXFD_paper -path "*/configs/vibench/min.yaml" | wc -l  # 期望：7
find paper/UXFD_paper -maxdepth 2 -name "VIBENCH.md" | wc -l      # 期望：7
```

### 2) 逐个文件存在性（示例）
```bash
ls -la paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml
ls -la paper/UXFD_paper/1D-2D_fusion_explainable/VIBENCH.md
```

### 3) 主仓库健康检查
```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
python -m scripts.validate_configs
python -m pytest test/
```

### 4) UXFD 工具链闭环
```bash
python -m scripts.collect_uxfd_runs --input results --out_dir reports
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_example.yaml
```

## Notes
- `scripts.collect_uxfd_runs.py` 的 `--input` 建议显式传 `results`（不要依赖脚本默认值）。
- 严格门禁 post-run 可能因历史 runs 缺少 `config_snapshot.yaml` 而失败；需要重新跑新 pipeline 或制定清理策略。
