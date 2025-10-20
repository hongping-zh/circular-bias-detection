import numpy as np

from circular_bias_detector import BiasDetector


def test_detect_bias_minimal():
    # Minimal matrices: 3 time periods, 2 algorithms, 2 constraints
    performance_matrix = np.array([
        [0.80, 0.78],
        [0.82, 0.79],
        [0.83, 0.81],
    ])

    constraint_matrix = np.array([
        [512, 8.0],
        [512, 8.0],
        [512, 8.0],
    ])

    detector = BiasDetector()
    results = detector.detect_bias(
        performance_matrix=performance_matrix,
        constraint_matrix=constraint_matrix,
        algorithm_names=["A", "B"],
    )

    # Basic structure checks
    assert isinstance(results, dict)
    for key in [
        "psi_score",
        "ccs_score",
        "rho_pc_score",
        "overall_bias",
        "confidence",
    ]:
        assert key in results

    # Value sanity checks
    assert 0.0 <= results["ccs_score"] <= 1.0
    assert -1.0 <= results["rho_pc_score"] <= 1.0
