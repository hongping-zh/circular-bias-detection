import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from cbd.adapters.sklearn_adapter import SklearnCBDModel
from cbd.api import detect_bias
from sklearn.metrics import accuracy_score

def test_detect_bias_sanity():
    X, y = make_classification(n_samples=200, n_features=8, random_state=42)
    clf = LogisticRegression(max_iter=1000).fit(X, y)
    model = SklearnCBDModel(clf)

    res = detect_bias(model, X, y, metric=lambda yt, yp: accuracy_score(yt, yp),
                      n_permutations=200, random_state=42)
    assert "observed_metric" in res
    assert 0.0 <= res["p_value"] <= 1.0
    assert "conclusion" in res
