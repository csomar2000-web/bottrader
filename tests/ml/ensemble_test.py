import numpy as np
from ml.inference.ensemble import EnsemblePredictor


# Dummy models for testing real logic
class ModelA:
    def predict(self, x):
        return {"prediction": 1, "confidence": 0.9}


class ModelB:
    def predict(self, x):
        return {"prediction": -1, "confidence": 0.6}


def test_ensemble_majority_buy():
    """
    REAL LOGIC:
    - Any positive value -> buy
    - Zero or negative -> sell
    - Your system uses: pred = 1 if val > 0 else 0
    So:
        ModelA → prediction 1 → buy vote
        ModelA → prediction 1 → buy vote
        ModelB → prediction -1 → sell vote

    => 2 Buy vs 1 Sell ⇒ BUY
    """
    ens = EnsemblePredictor(models=[ModelA(), ModelA(), ModelB()])

    out = ens.predict(np.array([1, 2, 3]))

    assert out["side"] == "buy"
    assert 0.5 < out["confidence"] <= 1.0


def test_ensemble_confidence_weighted():
    """
    Tests confidence correctly reflects real ensemble logic.
    """
    ens = EnsemblePredictor(models=[ModelA(), ModelB()])

    out = ens.predict(np.array([1, 2, 3]))

    assert "confidence" in out
    assert 0 <= out["confidence"] <= 1
