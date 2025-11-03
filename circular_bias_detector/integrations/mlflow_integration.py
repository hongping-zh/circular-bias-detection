from __future__ import annotations
from typing import Optional, Dict


def mlflow_log_results(results: Dict, artifacts: Optional[Dict[str, str]] = None, prefix: str = "cbd") -> None:
    """
    Log Circular Bias Detection results to MLflow.

    Parameters:
    - results: dict returned by BiasDetector.detect_bias() or similar structured output
    - artifacts: optional mapping {artifact_name: file_path} to upload
    - prefix: metric prefix to group logs (default: 'cbd')
    """
    try:
        import mlflow  # type: ignore
    except Exception as e:
        # Soft-fail: user may not have mlflow installed in all environments
        print(f"[mlflow_log_results] MLflow not available: {e}")
        return

    metrics = {}
    # Core indicators
    for key in ("psi_score", "ccs_score", "rho_pc_score"):
        if key in results:
            metrics[f"{prefix}/{key}"] = float(results[key])
    # Overall decision
    if "overall_bias" in results:
        metrics[f"{prefix}/overall_bias"] = 1.0 if bool(results["overall_bias"]) else 0.0
    if "confidence" in results:
        metrics[f"{prefix}/confidence"] = float(results["confidence"])
    # Optional bootstrap statistics
    for key in (
        "psi_ci_lower","psi_ci_upper","psi_pvalue",
        "ccs_ci_lower","ccs_ci_upper","ccs_pvalue",
        "rho_pc_ci_lower","rho_pc_ci_upper","rho_pc_pvalue",
    ):
        if key in results:
            try:
                metrics[f"{prefix}/{key}"] = float(results[key])
            except Exception:
                pass

    if metrics:
        mlflow.log_metrics(metrics)

    # Upload artifacts if provided
    if artifacts:
        for name, path in artifacts.items():
            try:
                mlflow.log_artifact(path, artifact_path=f"{prefix}_artifacts/{name}")
            except Exception as e:
                print(f"[mlflow_log_results] Failed to log artifact '{name}': {e}")
