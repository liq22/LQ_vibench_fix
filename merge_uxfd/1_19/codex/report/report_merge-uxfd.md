# Report: merge-uxfd (1_19)

Generated at: 2026-01-19T14:23:26+08:00

## Summary

- UXFD merge verification gates executed on repo-shipped dummy data (CPU).
- Smoke run and UXFD-enabled paper pilot run both succeed and emit `config_snapshot.yaml` + `artifacts/manifest.json`.
- Unit tests pass (includes UXFD assembly + artifact contract tests).
- Global strict post-run gate fails on historical runs that predate `config_snapshot.yaml`; strict gate passes when pinned to new run dirs only.
- Git commits cannot be created in this agent environment because `.git/` is read-only; use the submodule checklist to commit on your machine.

## Environment

- Python: 3.10.0
- Platform: Linux-5.15.0-139-generic-x86_64-with-glibc2.31

## Gates (commands + results)

### Gate0: Smoke (repo demo)

Command:
```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
```

Result: ✅ success

Key outputs:
- `results/demo/dummy_dg_smoke/metadata_dummy.csv/M_M_01_ISFM/T_DGclassification_19_142426/iter_0/config_snapshot.yaml`
- `results/demo/dummy_dg_smoke/metadata_dummy.csv/M_M_01_ISFM/T_DGclassification_19_142426/iter_0/artifacts/manifest.json`
- `results/demo/dummy_dg_smoke/metadata_dummy.csv/M_M_01_ISFM/T_DGclassification_19_142426/iter_0/test_result_0.csv`

Notes:
- `predictions.npz` not produced (not enabled in demo config) → confusion matrix plot is expected to skip.

### Gate1: Tests

Command:
```bash
python -m pytest test/
```

Result: ✅ 18 passed

### Gate2: UXFD-enabled pilot (paper min config)

Command:
```bash
python main.py --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml --override trainer.num_epochs=1
```

Result: ✅ success

Key outputs:
- `results/uxfd/pilot/1D-2D_fusion_explainable/metadata_dummy.csv/M_TSPN_UXFD/T_DGclassification_19_142428/iter_0/config_snapshot.yaml`
- `results/uxfd/pilot/1D-2D_fusion_explainable/metadata_dummy.csv/M_TSPN_UXFD/T_DGclassification_19_142428/iter_0/artifacts/manifest.json`
- `results/uxfd/pilot/1D-2D_fusion_explainable/metadata_dummy.csv/M_TSPN_UXFD/T_DGclassification_19_142428/iter_0/artifacts/predictions.npz`
- `results/uxfd/pilot/1D-2D_fusion_explainable/metadata_dummy.csv/M_TSPN_UXFD/T_DGclassification_19_142428/iter_0/test_result_0.csv`

### Gate3: Collect manifests → CSV

Command:
```bash
python -m scripts.collect_uxfd_runs --input results --out_dir reports
```

Result: ✅ success (CSV generated at `reports/uxfd_runs.csv`)

Note:
- `reports/uxfd_runs.csv` is a generated artifact; do not commit it unless you explicitly want it tracked.

### Gate4: Post-run checks + plotting (strict)

Global strict (all historical runs):
```bash
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml
```
Result: ❌ exit=1

Reason:
- historical runs (pre-merge) are missing `config_snapshot.yaml`, which is required by strict gate.

Strict for new runs only (pinned run_dirs):
```bash
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/uxfd_postrun_gate_new_runs.yaml
```
Result: ✅ success

Plots:
- smoke run: learning curve OK; confusion matrix skipped (no predictions)
- pilot run: learning curve OK; confusion matrix OK

## Submodule merge status

- `paper/UXFD_paper/*` and `paper/LQ_vibench_fix` contain untracked WP0 / documentation files that must be committed inside each submodule repo.
- Checklist & exact commands: `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/submodule_changes.txt`

## LLM / Autotune (fallback)

- `langgraph` is not installed in this environment, so a pure-Python fallback loop is used.
- Contract (schema): `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/llm_tool_contract.json`
- Orchestrator: `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/fallback_orchestrator.py`

Verified command (budget=1):
```bash
python paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/fallback_orchestrator.py \
  --paper_id 1D-2D_fusion_explainable \
  --config paper/UXFD_paper/1D-2D_fusion_explainable/configs/vibench/min.yaml \
  --budget 1 \
  --seed 0 \
  --output_root results/uxfd/autotune \
  --leaderboard_csv paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/uxfd_autotune_leaderboard.csv
```

Outputs:
- leaderboard: `paper/LQ_vibench_fix/merge_uxfd/1_19/codex/artifact/uxfd_autotune_leaderboard.csv`
- best run_dir (example): `results/uxfd/autotune/1D-2D_fusion_explainable/20260119_143147_00/.../iter_0`

## Risks / Open issues

- Strict post-run cannot be used “globally” unless you either:
  - (A) re-run/repair historical runs to include `config_snapshot.yaml`, or
  - (B) pin strict gate to a curated set of “new runs” (current approach), or
  - (C) relax required fields in strict gate (not recommended for CI).

## Repo Optimization (SSOT + Demo Closure)

Changes (comment-driven):
- Added `configs/base/model/tspn_uxfd.yaml` and `configs/demo/uxfd/` runnable demos, and indexed them via `configs/config_registry.csv`.
- Regenerated `docs/CONFIG_ATLAS.md` from registry.
- Added SSOT docs: `src/model_factory/X_model/UXFD/FACT_TABLE.md` and `src/model_factory/X_model/UXFD/OPERATOR_CATALOG.md`.
- Updated `src/model_factory/X_model/UXFD/README.md` to include quick-validate + SSOT pointers.
- Refined `test/test_run_artifacts_contract.py` to distinguish required keys vs optional-empty fields.

Validation (post-change):
```bash
python -m scripts.validate_configs   # [OK] 10/10
python -m scripts.validate_docs      # [OK] 115 files scanned
python -m pytest test/test_tspn_uxfd_assembly.py test/test_run_artifacts_contract.py -q  # 8 passed
```

UXFD demo smoke (SP2D + predictions):
```bash
python main.py --config configs/demo/uxfd/10_smoke_tspn_uxfd_sp2d.yaml --override trainer.num_epochs=1
```

Key outputs (example run_dir):
- `results/demo/uxfd/tspn_uxfd_sp2d/metadata_dummy.csv/M_TSPN_UXFD/T_DGclassification_19_150611/iter_0/config_snapshot.yaml`
- `results/demo/uxfd/tspn_uxfd_sp2d/metadata_dummy.csv/M_TSPN_UXFD/T_DGclassification_19_150611/iter_0/artifacts/manifest.json`
- `results/demo/uxfd/tspn_uxfd_sp2d/metadata_dummy.csv/M_TSPN_UXFD/T_DGclassification_19_150611/iter_0/artifacts/predictions.npz`
