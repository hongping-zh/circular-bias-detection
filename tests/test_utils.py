import os
import json
import numpy as np
import pandas as pd
import pytest

from circular_bias_detector.utils import (
    validate_matrices,
    create_synthetic_data,
    save_results_json,
    load_results_json,
    validate_and_clean_data,
)


def test_validate_matrices_happy_path():
    perf = np.random.rand(5, 2)
    const = np.random.rand(5, 1)
    validate_matrices(perf, const)  # Should not raise


def test_validate_matrices_errors():
    perf = np.random.rand(1, 2)  # T < 2
    const = np.random.rand(1, 1)
    with pytest.raises(ValueError):
        validate_matrices(perf, const)

    perf = np.random.rand(3, 2)
    const = np.random.rand(2, 1)  # T mismatch
    with pytest.raises(ValueError):
        validate_matrices(perf, const)

    perf = np.array([[np.nan, 0.1], [0.2, 0.3]])
    const = np.random.rand(2, 1)
    with pytest.raises(ValueError):
        validate_matrices(perf, const)


def test_create_synthetic_data_shapes_and_bias_effect(tmp_path):
    perf, const = create_synthetic_data(n_time_periods=15, n_algorithms=4, n_constraints=2, bias_intensity=0.0, random_seed=1)
    assert perf.shape == (15, 4)
    assert const.shape == (15, 2)

    # With bias, constraints should correlate more with mean performance
    perf_b, const_b = create_synthetic_data(n_time_periods=30, n_algorithms=3, n_constraints=2, bias_intensity=0.8, random_seed=2)
    mean_perf = perf_b.mean(axis=1)
    mean_const = const_b.mean(axis=1)
    corr = np.corrcoef(mean_perf, mean_const)[0, 1]
    assert abs(corr) > 0.3


def test_results_json_roundtrip(tmp_path):
    results = {
        "psi_score": 0.12,
        "ccs_score": 0.91,
        "rho_pc_score": -0.23,
        "overall_bias": False,
        "confidence": 0.33,
    }
    out = tmp_path / "results.json"
    save_results_json(results, str(out))
    loaded = load_results_json(str(out))
    # Parity check
    for k in results:
        assert loaded[k] == results[k]


def test_validate_and_clean_data_basic():
    df = pd.DataFrame(
        {
            "time_period": [1, 2, 2, 4],
            "algorithm": ["A", "A", "A", "A"],
            "performance": [0.8, np.nan, 0.85, -0.1],
            "constraint_compute": [512, 512, 512, 512],
            "constraint_memory": [8.0, 8.0, 8.0, 8.0],
        }
    )

    cleaned, report = validate_and_clean_data(
        df,
        performance_cols=["performance"],
        constraint_cols=["constraint_compute", "constraint_memory"],
        auto_fix=True,
    )

    assert cleaned["performance"].isnull().sum() == 0
    assert (cleaned["performance"] >= 0).all()
    assert report["summary"]["total_issues_found"] >= 1
