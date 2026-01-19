from __future__ import annotations

import argparse
import csv
import json
import os
import random
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


DEFAULT_ALLOWED_PREFIXES = (
    "model.uxfd.",
    "trainer.extensions.",
    "trainer.seed",
    "trainer.num_epochs",
    "environment.output_dir",
)


@dataclass(frozen=True)
class TrialResult:
    trial_id: str
    run_dir: str
    manifest_path: str
    score: float
    metrics: Dict[str, float]
    overrides: List[str]


def _now_id() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def _safe_parse_float(v: object) -> Optional[float]:
    try:
        return float(v)  # type: ignore[arg-type]
    except Exception:
        return None


def _validate_overrides(overrides: Iterable[str], allowed_prefixes: Tuple[str, ...]) -> List[str]:
    cleaned: List[str] = []
    for item in overrides:
        s = str(item).strip()
        if not s or "=" not in s:
            raise ValueError(f"Invalid override (expected key=value): {s!r}")
        key = s.split("=", 1)[0].strip()
        if not any(key.startswith(p) or key == p for p in allowed_prefixes):
            raise ValueError(f"Override not allowed by prefix whitelist: {key!r}")
        cleaned.append(s)
    return cleaned


def _discover_latest_manifest(root_dir: Path) -> Optional[Path]:
    manifests = list(root_dir.glob("**/artifacts/manifest.json"))
    if not manifests:
        return None
    manifests.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return manifests[0]


def _load_metrics_from_manifest(manifest: Dict[str, object]) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    inline = manifest.get("metrics_inline")
    if isinstance(inline, dict):
        for k, v in inline.items():
            fv = _safe_parse_float(v)
            if fv is not None:
                metrics[str(k)] = fv
    return metrics


def _score_from_metrics(metrics: Dict[str, float]) -> float:
    # Higher is better.
    for k, v in metrics.items():
        if "test_acc" in k:
            return float(v)
    for k in ("test_total_loss", "test_loss", "test_Dummy_Data_loss"):
        if k in metrics:
            return -float(metrics[k])
    # Default: no metrics -> worst score
    return float("-inf")


class OptimizationLoop:
    def __init__(
        self,
        *,
        paper_id: str,
        config_path: str,
        output_root: str,
        budget: int,
        seed: int = 0,
        allowed_prefixes: Tuple[str, ...] = DEFAULT_ALLOWED_PREFIXES,
    ) -> None:
        self.paper_id = paper_id
        self.config_path = config_path
        self.output_root = Path(output_root)
        self.budget = int(budget)
        self.seed = int(seed)
        self.allowed_prefixes = allowed_prefixes
        random.seed(self.seed)

        self.trials: List[TrialResult] = []

    def propose_trial(self, i: int) -> List[str]:
        # Fallback (no LLM): small structured exploration of the UXFD toggles.
        candidates = [
            ("model.uxfd.enable_sp2d", ["true"]),
            ("model.uxfd.fusion.type", ["concat", "sum", "gated"]),
            ("model.uxfd.fuzzy.enable", ["false", "true"]),
            ("model.uxfd.fuzzy.logit_scale", ["0.5", "1.0"]),
            ("model.uxfd.operator_attention.enable", ["false", "true"]),
            ("model.uxfd.logic.enable", ["false", "true"]),
        ]

        overrides: List[str] = []
        # Always keep runs fast/deterministic by default.
        overrides.append("trainer.num_epochs=1")
        overrides.append(f"trainer.seed={self.seed}")

        # Change 1-2 factors per trial for attribution.
        k = 1 if i == 0 else 2
        chosen = random.sample(candidates, k=k)
        for key, values in chosen:
            overrides.append(f"{key}={random.choice(values)}")

        # Ensure isolated output dir per trial.
        trial_id = f"{_now_id()}_{i:02d}"
        overrides.append(f"environment.output_dir={self.output_root}/{self.paper_id}/{trial_id}")
        return overrides

    def execute_trial(self, overrides: List[str]) -> TrialResult:
        overrides = _validate_overrides(overrides, self.allowed_prefixes)
        cmd = ["python", "main.py", "--config", self.config_path]
        for ov in overrides:
            cmd.extend(["--override", ov])

        proc = subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=os.environ.copy(),
        )

        # Try to locate the produced manifest under output_dir.
        out_dir = None
        for ov in overrides:
            if ov.startswith("environment.output_dir="):
                out_dir = ov.split("=", 1)[1].strip()
                break
        root = Path(out_dir) if out_dir else self.output_root
        mp = _discover_latest_manifest(root)
        if mp is None:
            raise RuntimeError(f"Trial produced no manifest under {root} (exit={proc.returncode})\n{proc.stdout}")

        manifest = json.loads(mp.read_text(encoding="utf-8"))
        metrics = _load_metrics_from_manifest(manifest)
        score = _score_from_metrics(metrics)

        return TrialResult(
            trial_id=str(mp.parents[1].name),
            run_dir=str(manifest.get("run_dir", str(mp.parents[1]))),
            manifest_path=str(mp),
            score=float(score),
            metrics=metrics,
            overrides=overrides,
        )

    def run(self) -> TrialResult:
        best: Optional[TrialResult] = None
        for i in range(self.budget):
            overrides = self.propose_trial(i)
            result = self.execute_trial(overrides)
            self.trials.append(result)
            if best is None or result.score > best.score:
                best = result
        assert best is not None
        return best

    def write_leaderboard(self, out_csv: Path) -> None:
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        cols = ["trial_id", "score", "run_dir", "manifest_path", "overrides"]
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for t in self.trials:
                w.writerow(
                    {
                        "trial_id": t.trial_id,
                        "score": t.score,
                        "run_dir": t.run_dir,
                        "manifest_path": t.manifest_path,
                        "overrides": " ".join(t.overrides),
                    }
                )


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Fallback UXFD config optimization loop (no langgraph required).")
    p.add_argument("--paper_id", required=True)
    p.add_argument("--config", required=True, help="Base YAML config used by vibench entrypoint.")
    p.add_argument("--budget", type=int, default=3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--output_root", default="results/uxfd/autotune")
    p.add_argument("--leaderboard_csv", default="reports/uxfd_autotune.csv")
    args = p.parse_args(argv)

    loop = OptimizationLoop(
        paper_id=args.paper_id,
        config_path=args.config,
        output_root=args.output_root,
        budget=args.budget,
        seed=args.seed,
    )
    best = loop.run()
    loop.write_leaderboard(Path(args.leaderboard_csv))

    print("[autotune] best score:", best.score)
    print("[autotune] best run_dir:", best.run_dir)
    print("[autotune] best manifest:", best.manifest_path)
    print("[autotune] best overrides:")
    for ov in best.overrides:
        print("  -", ov)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

