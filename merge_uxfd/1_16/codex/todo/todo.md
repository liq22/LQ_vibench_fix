# Todo 1_16

## Top
- [ ] 在 7 个 `paper/UXFD_paper/<paper_id>/` submodule 内分别提交 `configs/vibench/min.yaml` 与 `VIBENCH.md`
- [ ] 父仓库更新 7 个 submodule gitlink 指针并产出可 review 的 PR diff
- [ ] 用严格配置复查 post-run：`paper/LQ_vibench_fix/merge_uxfd/12_23/uxfd_postrun_config_strict.yaml`
- [ ] 统一各 paper 的 `trainer.extensions.predictions.enable` 策略（确保混淆矩阵等绘图可用）
- [ ] 清理“历史 runs 缺 config_snapshot”的策略（重跑 / 补写 / 忽略老 run）

## Notes
- submodule 文件级 diff 不会出现在父仓库，除非先在 submodule 仓库 commit。
