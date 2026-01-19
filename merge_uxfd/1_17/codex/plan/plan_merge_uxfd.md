# Plan: merge_uxfd

## Goal
Make UXFD “works” verifiable via explainability-as-artifacts test gates, then enable controlled LLM-driven UXFD structure trials via a LangGraph-style orchestrator.

## Scope
- In:
  - Deterministic unit + artifacts-contract tests for UXFD assembly and outputs.
  - Minimal tool contract to run vibench, parse `manifest.json`, and score trials (offline).
  - Strict offline post-run gate config for explainability checks.
- Out:
  - Any online network dependency or external AutoML service.
  - Coupling plotting/post-run into training (prefer offline consumption).
  - “Paper-grade” explanation algorithms beyond artifact/interface contracts.

## Tasks
- [ ] T1 Define “UXFD works” contract and baseline run
  - DoD:
    - `python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1` runs end-to-end.
    - One paper `configs/vibench/min.yaml` can run at least 1 epoch on CPU and produces a non-empty `artifacts/manifest.json` (path + required fields documented).
  - Dependencies:
    - Output directory convention (`environment.output_dir` / `save/`) and where `artifacts/` is written today.

- [ ] T2 Add fast UXFD assembly unit tests (no training)
  - DoD:
    - `test/test_tspn_uxfd_assembly.py` added and covers key `model.uxfd.*` toggles (SP2D/Fusion/Fuzzy/Logic/OperatorAttention) with stable forward shapes.
    - `python -m pytest test/ -k uxfd -q` passes without GPU/downloads.
  - Dependencies:
    - A minimal model instantiation path for `TSPN_UXFD` that is deterministic under CPU.

- [ ] T3 Add artifacts contract tests (“explainability” as files)
  - DoD:
    - `test/test_run_artifacts_contract.py` added and verifies `artifacts/manifest.json` schema essentials and gated outputs (e.g., `predictions.npz`, `explain/eligibility.json` when enabled).
    - `python -m pytest test/ -k artifacts -q` passes.
  - Dependencies:
    - Stable artifact writer behavior and a minimal run configuration (dummy or 1-step trainer).

- [ ] T4 Add strict offline post-run gate config
  - DoD:
    - A strict post-run config exists and can be executed offline via `python -m scripts.uxfd_postrun --config <strict.yaml>` on newly generated runs.
    - The gate clearly distinguishes “new runs” vs “historical runs” handling.
  - Dependencies:
    - `scripts/uxfd_postrun.py` accepts the config path and emits pass/fail with actionable errors.

- [ ] T5 Expose UXFD runner as an LLM-tool + minimal LangGraph workflow
  - DoD:
    - A proposal schema (JSON schema / pydantic) restricts overrides to a whitelist (mostly `model.uxfd.*` plus bounded trainer knobs).
    - A CLI can run “propose → run → collect evidence → decide next” for 1 paper with a fixed budget and produces:
      - `reports/uxfd_autotune_<paper_id>.csv` (one row per trial),
      - `best_config_overrides.yaml`,
      - `reproduce.sh` (fixed seed + captured snapshot/overrides).
  - Dependencies:
    - `LLM_Explainable_FD_Toolkit` repo integration point (prefer submodule-local to avoid adding deps to this repo).

## Gates (optional)
- `python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`
- `python -m scripts.validate_configs`
- `python -m pytest test/`
- `python -m scripts.uxfd_postrun --config <strict.yaml>`

## Deliverables
- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/plan/plan_merge_uxfd.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/report/report_merge_uxfd.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/artifact/manifest_merge_uxfd.json`

## Rollback
- Revert added tests/configs and disable any new gates; keep `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/` documents as drafts if implementation work is postponed.

## Execution Log

