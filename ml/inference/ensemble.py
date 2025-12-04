import numpy as np
from typing import Dict, Any
from core.utils import timestamp

class EnsemblePredictor:
    def __init__(self, models: Dict[str, Any], weights: Dict[str, float]):
        self.models = models
        self.weights = weights

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        preds = {}
        confs = {}

        for name, model in self.models.items():
            r = model.predict(features)
            preds[name] = r["prediction"]
            confs[name] = r["confidence"]

        combined = self._weighted(preds)
        conf = self._combined_confidence(confs)

        return {
            "prediction": combined,
            "confidence": conf,
            "components": preds,
            "timestamp": timestamp()
        }

    def _weighted(self, preds: Dict[str, float]):
        nums = []
        dens = 0
        for name, pred in preds.items():
            w = self.weights.get(name, 1.0)
            nums.append(pred * w)
            dens += w
        return sum(nums) / (dens + 1e-12)

    def _combined_confidence(self, confs: Dict[str, float]):
        arr = np.array(list(confs.values()))
        return float(arr.mean())
