"""Minimal quickstart demo for circular-bias-detection."""

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from cbd.adapters.sklearn_adapter import SklearnCBDModel
from cbd.api import detect_bias

def main():
    X, y = make_classification(n_samples=500, n_features=10, random_state=0)
    clf = LogisticRegression(max_iter=1000).fit(X, y)
    model = SklearnCBDModel(clf)

    result = detect_bias(
        model, X, y,
        metric=lambda yt, yp: accuracy_score(yt, yp),
        n_permutations=500,
        random_state=0,
        return_permutations=False
    )
    print("Observed metric:", result["observed_metric"])
    print("p-value:", result["p_value"])
    print("Conclusion:", result["conclusion"])

if __name__ == "__main__":
    main()
