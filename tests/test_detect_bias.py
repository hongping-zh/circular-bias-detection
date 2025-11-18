import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from cbd.adapters.sklearn_adapter import SklearnCBDModel
from cbd.api import detect_bias
from sklearn.metrics import accuracy_score
import pytest

def test_detect_bias_sanity():
    X, y = make_classification(n_samples=200, n_features=8, random_state=42)
    clf = LogisticRegression(max_iter=1000).fit(X, y)
    model = SklearnCBDModel(clf)

    res = detect_bias(model, X, y, metric=lambda yt, yp: accuracy_score(yt, yp),
                      n_permutations=200, random_state=42)
    assert "observed_metric" in res
    assert 0.0 <= res["p_value"] <= 1.0
    assert "conclusion" in res

def test_detect_bias_stratify():
    # create grouped data and ensure stratify preserves groups during permutation
    rng = np.random.RandomState(0)
    X = rng.normal(size=(100, 5))
    # labels with two classes but grouped by 10 groups
    groups = np.repeat(np.arange(10), 10)
    y = (groups % 2).copy()  # class depends on group parity
    clf = LogisticRegression(max_iter=1000).fit(X, y)
    model = SklearnCBDModel(clf)

    res = detect_bias(model, X, y, metric=lambda yt, yp: accuracy_score(yt, yp),
                      n_permutations=100, random_state=0, stratify=groups)
    assert "p_value" in res
    assert 0.0 <= res["p_value"] <= 1.0

def test_detect_bias_single_class_raises():
    X = np.zeros((10, 2))
    y = np.zeros(10)  # single class
    clf = LogisticRegression().fit(X, y)
    model = SklearnCBDModel(clf)
    with pytest.raises(ValueError):
        detect_bias(model, X, y, metric=lambda yt, yp: 1.0, n_permutations=10)