# Report: merge_uxfd (2026-01-17)

## What this is
This report captures the current UXFD “explainable test gates + LLM orchestration” consolidation for the `1_17/codex` working area, plus the concrete plan deliverable.

## Inputs reviewed
- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/README.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/TODO.md`

## Key decisions / contracts (as written in TODO)
- “UXFD 模型 work” includes at least one UXFD-enabled paper `configs/vibench/min.yaml` run (CPU, 1 epoch) and requires `<run_dir>/artifacts/manifest.json`.
- Explainability is treated as artifact/interface contracts (manifest/predictions/eligibility/debug_state), not “paper-grade” explanation algorithms.
- Strict offline post-run gating config is referenced (canonical in `paper/LQ_vibench_fix/merge_uxfd/12_23/` and a convenience copy under `1_17/codex/`).

## Deliverables created in this pass
- Plan: `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/plan/plan_merge_uxfd.md`
- Intake: `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/intake/intake_merge_uxfd.md`
- Manifest (this pass): `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/artifact/manifest_merge_uxfd.json`

## Next actions (implementation work, not done here)
- Land P0 tests:
  - `test/test_tspn_uxfd_assembly.py`
  - `test/test_run_artifacts_contract.py`
- Confirm/standardize `artifacts/manifest.json` minimal schema and how `trainer.extensions.*` toggles map to non-empty fields.
- Wire minimal LLM toolkit runner contract (whitelisted overrides) and a budgeted propose→run→parse loop.

## Validation commands
```bash
python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1
python -m pytest test/ -k uxfd -q
python -m pytest test/ -k artifacts -q
python -m scripts.uxfd_postrun --config paper/LQ_vibench_fix/merge_uxfd/1_17/codex/uxfd_postrun_config_strict.yaml
```

