from __future__ import annotations
from typing import Dict, Any, Optional
import json
from datetime import datetime

SEVERITY_LEVELS = {
    "none": {
        "label": "No Bias Detected",
        "recommendation": "No immediate action required. Continue monitoring in routine QA.",
    },
    "warning": {
        "label": "Warning",
        "recommendation": "Review evaluation setup and recent changes. Consider running a negative-control and parameter stability checks.",
    },
    "critical": {
        "label": "Critical",
        "recommendation": "Block deployment. Audit data splits, leakage, and evaluation protocol. Roll back to last passing version and open an incident.",
    },
}


def _infer_severity(results: Dict[str, Any], warn_threshold: float = 0.6, critical_threshold: float = 0.8) -> str:
    detected = bool(results.get("overall_bias", False))
    confidence = float(results.get("confidence", 0.0))
    if detected and confidence >= critical_threshold:
        return "critical"
    if detected or confidence >= warn_threshold:
        return "warning"
    return "none"


def build_model_card_markdown(
    results: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
    warn_threshold: float = 0.6,
    critical_threshold: float = 0.8,
) -> str:
    """
    Build a Markdown model card snippet summarizing Circular Bias Detection results.
    Compatible with common model card formats (e.g., Hugging Face Hub).
    """
    md = []
    meta = metadata or {}
    ts = datetime.utcnow().isoformat()
    sev = _infer_severity(results, warn_threshold, critical_threshold)
    sev_info = SEVERITY_LEVELS[sev]

    psi = results.get("psi_score")
    ccs = results.get("ccs_score")
    rho = results.get("rho_pc_score")
    conf = results.get("confidence")

    psi_p = results.get("psi_pvalue")
    ccs_p = results.get("ccs_pvalue")
    rho_p = results.get("rho_pc_pvalue")

    md.append("## Circular Bias Detection (CBD) Summary")
    md.append("")
    md.append(f"- Timestamp (UTC): {ts}")
    if meta.get("model_name"): md.append(f"- Model: {meta['model_name']}")
    if meta.get("dataset_name"): md.append(f"- Dataset: {meta['dataset_name']}")
    if meta.get("run_id"): md.append(f"- Run ID: {meta['run_id']}")

    md.append("")
    md.append("### Results")
    md.append(f"- PSI (Parameter Stability): {psi:.4f}  ") if psi is not None else None
    md.append(f"- CCS (Constraint Consistency): {ccs:.4f}  ") if ccs is not None else None
    md.append(f"- ρ_PC (Performance-Constraint): {rho:+.4f}  ") if rho is not None else None
    if conf is not None:
        md.append(f"- Overall decision: {'Bias detected' if results.get('overall_bias') else 'No bias'}  ")
        md.append(f"- Confidence: {conf:.1%}  ")

    if psi_p is not None or ccs_p is not None or rho_p is not None:
        md.append("")
        md.append("#### Statistical Significance (if bootstrap enabled)")
        if psi_p is not None: md.append(f"- PSI p-value: {psi_p:.3g}")
        if ccs_p is not None: md.append(f"- CCS p-value: {ccs_p:.3g}")
        if rho_p is not None: md.append(f"- ρ_PC p-value: {rho_p:.3g}")

    md.append("")
    md.append("### Severity & Recommendation")
    md.append(f"- Severity: **{sev_info['label']}**")
    md.append(f"- Recommended Action: {sev_info['recommendation']}")

    md.append("")
    md.append("### Notes")
    md.append("- CBD combines PSI, CCS, and ρ_PC to assess circular reasoning risk in evaluation.")
    md.append("- For best practice, attach the full report and indicator plots as artifacts.")

    return "\n".join(md)


def build_model_card_json(
    results: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
    warn_threshold: float = 0.6,
    critical_threshold: float = 0.8,
) -> str:
    """
    Build a JSON model card fragment capturing CBD results in a machine-readable way.
    """
    sev = _infer_severity(results, warn_threshold, critical_threshold)
    payload = {
        "cbd": {
            "timestamp_utc": datetime.utcnow().isoformat(),
            "results": {
                "psi": results.get("psi_score"),
                "ccs": results.get("ccs_score"),
                "rho_pc": results.get("rho_pc_score"),
                "overall_bias": bool(results.get("overall_bias", False)),
                "confidence": results.get("confidence"),
                "bootstrap": {
                    "psi_pvalue": results.get("psi_pvalue"),
                    "ccs_pvalue": results.get("ccs_pvalue"),
                    "rho_pc_pvalue": results.get("rho_pc_pvalue"),
                    "psi_ci": [results.get("psi_ci_lower"), results.get("psi_ci_upper")],
                    "ccs_ci": [results.get("ccs_ci_lower"), results.get("ccs_ci_upper")],
                    "rho_pc_ci": [results.get("rho_pc_ci_lower"), results.get("rho_pc_ci_upper")],
                },
            },
            "severity": sev,
            "recommendation": SEVERITY_LEVELS[sev]["recommendation"],
            "metadata": metadata or {},
        }
    }
    return json.dumps(payload, indent=2)


def save_model_card(
    results: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
    path: str = "MODEL_CARD_CBD.md",
    format: str = "md",
    warn_threshold: float = 0.6,
    critical_threshold: float = 0.8,
) -> str:
    """
    Generate and save a model card attachment summarizing CBD results.
    Returns the path written.
    """
    if format.lower() == "md":
        content = build_model_card_markdown(results, metadata, warn_threshold, critical_threshold)
    elif format.lower() == "json":
        content = build_model_card_json(results, metadata, warn_threshold, critical_threshold)
    else:
        raise ValueError("Unsupported format. Use 'md' or 'json'.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
