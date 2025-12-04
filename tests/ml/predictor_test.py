import sys, os
sys.path.insert(0, os.getcwd())

from ml.inference.predictor import Predictor
import numpy as np


class DummyModel:
    def predict(self, x):
        return np.array([[0.7, 0.3]])


def test_predictor_basic():
    pred = Predictor(model=DummyModel())

    features = np.array([0.1, 0.2, 0.3])

    out = pred.predict(features)

    assert "side" in out
    assert "confidence" in out
    assert out["side"] == "buy"
    assert 0.5 < out["confidence"] < 1.0
