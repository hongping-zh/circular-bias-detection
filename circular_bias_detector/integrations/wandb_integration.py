from __future__ import annotations
from typing import Optional, Dict, Any, List


def wandb_log_results(results: Dict[str, Any], tables: Optional[Dict[str, Any]] = None, prefix: str = "cbd") -> None:
    """
    Log Circular Bias Detection results to Weights & Biases (W&B).

    Parameters:
    - results: dict returned by BiasDetector.detect_bias() or similar structured output
    - tables: optional mapping {table_name: data} where data can be:
        - list[dict]: converted to wandb.Table automatically
        - tuple(headers: list[str], rows: list[list])
    - prefix: metric prefix to group logs (default: 'cbd')
    """
    try:
        import wandb  # type: ignore
    except Exception as e:
        print(f"[wandb_log_results] W&B not available: {e}")
        return

    metrics = {}
    for key in ("psi_score", "ccs_score", "rho_pc_score", "confidence"):
        if key in results:
            try:
                metrics[f"{prefix}/{key}"] = float(results[key])
            except Exception:
                pass
    if "overall_bias" in results:
        metrics[f"{prefix}/overall_bias"] = 1.0 if bool(results["overall_bias"]) else 0.0

    # Optional bootstrap stats
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
        wandb.log(metrics)

    if tables:
        for name, data in tables.items():
            try:
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    # auto infer columns
                    cols = sorted({k for row in data for k in row.keys()})
                    wb_table = wandb.Table(columns=cols)
                    for row in data:
                        wb_table.add_data(*[row.get(c) for c in cols])
                    wandb.log({f"{prefix}/{name}": wb_table})
                elif isinstance(data, tuple) and len(data) == 2:
                    headers, rows = data  # type: ignore
                    wb_table = wandb.Table(columns=list(headers))
                    for r in rows:
                        wb_table.add_data(*list(r))
                    wandb.log({f"{prefix}/{name}": wb_table})
                else:
                    # fallback: log raw object
                    wandb.log({f"{prefix}/{name}": data})
            except Exception as e:
                print(f"[wandb_log_results] Failed to log table '{name}': {e}")
