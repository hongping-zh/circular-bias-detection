import numpy as np
import os
import matplotlib

from circular_bias_detector import BiasDetector


def test_plot_indicators_smoke(tmp_path):
    # Use non-interactive backend for CI
    matplotlib.use("Agg")

    rng = np.random.default_rng(0)
    perf = rng.random((6, 3))
    const = rng.random((6, 2))

    det = BiasDetector()
    res = det.detect_bias(performance_matrix=perf, constraint_matrix=const)

    out = tmp_path / "indicators.png"
    det.plot_indicators(results=res, save_path=str(out))

    assert out.exists()
    assert out.stat().st_size > 0
