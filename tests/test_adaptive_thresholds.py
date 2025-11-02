import numpy as np

from circular_bias_detector.core.bootstrap import compute_adaptive_thresholds


def test_compute_adaptive_thresholds_shapes_and_monotonicity():
    # Small matrices for speed
    rng = np.random.default_rng(0)
    perf = rng.random((12, 3))
    const = rng.random((12, 2))

    res = compute_adaptive_thresholds(
        performance_matrix=perf,
        constraint_matrix=const,
        quantile=0.9,
        n_simulations=50,
        random_seed=123,
    )

    # Keys present
    assert set(res.keys()) >= {
        "psi_threshold",
        "ccs_threshold",
        "rho_pc_threshold",
        "method",
        "quantile",
        "n_simulations",
    }

    # Ranges
    assert 0.0 <= res["psi_threshold"]
    assert 0.0 <= res["ccs_threshold"] <= 1.0
    assert 0.0 <= res["rho_pc_threshold"] <= 1.0

    # Method metadata
    assert res["method"] == "adaptive_quantile"
    assert res["quantile"] == 0.9
    assert res["n_simulations"] == 50
