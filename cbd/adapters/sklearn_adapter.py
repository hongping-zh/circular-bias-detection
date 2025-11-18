"""Adapter to wrap scikit-learn estimators into the CBDModel protocol."""
from typing import Any
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
import numpy as np

class SklearnCBDModel:
    """
    Simple wrapper that adapts scikit-learn estimators to CBDModel protocol.

    Example:
        from sklearn.linear_model import LogisticRegression
        model = SklearnCBDModel(LogisticRegression().fit(X_train, y_train))
    """
    def __init__(self, estimator: BaseEstimator):
        if not hasattr(estimator, "predict"):
            raise ValueError("Estimator must implement predict()")
        self._estimator = estimator

    def predict(self, X):
        return self._estimator.predict(X)

    def predict_proba(self, X):
        if hasattr(self._estimator, "predict_proba"):
            return self._estimator.predict_proba(X)
        raise AttributeError("Underlying estimator has no predict_proba")
