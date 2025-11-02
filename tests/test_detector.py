import numpy as np

from circular_bias_detector import BiasDetector


def _toy_data(T=8, K=3, p=2, seed=0):
    rng = np.random.default_rng(seed)
    perf = rng.random((T, K))
    const = rng.random((T, p))
    return perf, const


def test_detect_bias_with_bootstrap_fields_present():
    perf, const = _toy_data()
    det = BiasDetector()
    res = det.detect_bias(
        performance_matrix=perf,
        constraint_matrix=const,
        enable_bootstrap=True,
        n_bootstrap=100,
    )

    # Core keys
    for key in ["psi_score", "ccs_score", "rho_pc_score", "overall_bias", "confidence", "metadata"]:
        assert key in res

    # Bootstrap keys
    for key in [
        "psi_ci_lower",
        "psi_ci_upper",
        "psi_pvalue",
        "ccs_ci_lower",
        "ccs_ci_upper",
        "ccs_pvalue",
        "rho_pc_ci_lower",
        "rho_pc_ci_upper",
        "rho_pc_pvalue",
        "bootstrap_enabled",
        "n_bootstrap",
    ]:
        assert key in res

    assert res["bootstrap_enabled"] is True
    assert res["n_bootstrap"] == 100


def test_generate_report_string():
    perf, const = _toy_data()
    det = BiasDetector()
    res = det.detect_bias(performance_matrix=perf, constraint_matrix=const)
    report = det.generate_report(res)
    assert isinstance(report, str)
    assert "INDICATOR SCORES" in report
