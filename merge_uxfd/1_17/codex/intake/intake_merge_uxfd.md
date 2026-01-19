# Intake: merge_uxfd (UXFD explainable tests + LLM orchestration)

## Source
- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/README.md`
- `paper/LQ_vibench_fix/merge_uxfd/1_17/codex/TODO.md`

## Goal
- Make `TSPN_UXFD` reliably runnable in PHM-Vibench (config-first) with stable, machine-checkable evidence artifacts.
- Enable `LLM_Explainable_FD_Toolkit` to run controlled UXFD structure trials via a LangGraph-style propose→run→parse→update loop.

## Scope
- In:
  - Deterministic “explainability-as-artifacts” test gates (unit + contract).
  - Minimal tool contract + orchestrator to run vibench, parse manifest, and score trials.
  - Strict offline post-run gate config for explainability checks (no network).
- Out:
  - Any online dependencies / external AutoML services.
  - Making plotting/post-run tightly coupled to training (prefer offline consumption).
  - “Paper-grade” explainability algorithms beyond artifact/interface contracts.

## Current Facts (as of 2026-01-17)
- 7/7 paper submodules have `configs/vibench/min.yaml` and `VIBENCH.md` in the working tree.
- `TSPN_UXFD` supports assembly via `model.uxfd.*` toggles (best-effort): SP2D, Fusion, Fuzzy, OperatorAttention, Logic.
- Evidence tooling exists (best-effort): `scripts/collect_uxfd_runs.py`, `scripts/uxfd_postrun.py`.

## Proposed Work (high-level)
- P0: Add explainability test gates to make “UXFD works” machine-verifiable.
- P1: Expose “run vibench + parse manifest” as a toolkit tool callable from LangGraph (or fallback orchestrator).
- P2: Define safe search space, scoring, and rollback for LLM-driven structure trials.

## Suggested Validation Gates
- `python main.py --config configs/demo/00_smoke/dummy_dg.yaml --override trainer.num_epochs=1`
- `python -m pytest test/ -k uxfd -q`
