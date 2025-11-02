import numpy as np
import pytest

from circular_bias_detector.core.metrics import (
    compute_psi,
    compute_ccs,
    compute_rho_pc,
)
from circular_bias_detector.core.bootstrap import (
    bootstrap_psi,
    bootstrap_ccs,
    bootstrap_rho_pc,
)


def _toy_data(T=8, K=3, p=2, seed=123):
    rng = np.random.default_rng(seed)
    perf = rng.random((T, K))
    const = rng.random((T, p)) * 10
    return perf, const


def test_bootstrap_psi_structure_and_bounds():
    perf, _ = _toy_data()
    res = bootstrap_psi(perf, n_bootstrap=200, confidence_level=0.90, random_seed=1)
    assert 0.0 <= res["p_value"] <= 1.0
    assert res["ci_lower"] <= res["psi"] <= res["ci_upper"]
    assert res["std_error"] >= 0.0
    assert res["n_bootstrap"] == 200


def test_bootstrap_ccs_structure_and_bounds():
    _, const = _toy_data()
    res = bootstrap_ccs(const, n_bootstrap=200, confidence_level=0.90, random_seed=2)
    assert 0.0 <= res["p_value"] <= 1.0
    assert 0.0 <= res["ccs"] <= 1.0
    assert res["ci_lower"] <= res["ccs"] <= res["ci_upper"]


def test_bootstrap_rho_pc_structure_and_bounds():
    perf, const = _toy_data()
    res = bootstrap_rho_pc(perf, const, n_bootstrap=200, confidence_level=0.90, random_seed=3)
    assert 0.0 <= res["p_value"] <= 1.0
    assert -1.0 <= res["rho_pc"] <= 1.0
    assert res["ci_lower"] <= res["rho_pc"] <= res["ci_upper"]
