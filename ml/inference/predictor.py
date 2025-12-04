import numpy as np
from typing import Dict, Any
import joblib
from core.utils import timestamp

class Predictor:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        keys = sorted(features.keys())
        x = np.array([features[k] for k in keys], dtype=float).reshape(1, -1)
        y = self.model.predict(x)[0]
        c = self.confidence(x)
        return {
            "prediction": float(y),
            "confidence": float(c),
            "timestamp": timestamp(),
            "features_used": len(keys)
        }

    def confidence(self, x):
        p = self.model.predict_proba(x)[0] if hasattr(self.model, "predict_proba") else None
        if p is None:
            return 0.5
        return max(p)
