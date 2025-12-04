import sys, os
sys.path.insert(0, os.getcwd())

from ml.feature_engineering import FeatureEngineering
import numpy as np


def test_feature_scaling():
    fe = FeatureEngineering()
    x = np.array([1, 2, 3, 4])

    out = fe.normalize(x)

    assert out.min() >= 0
    assert out.max() <= 1
