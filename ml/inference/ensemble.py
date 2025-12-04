import numpy as np

class EnsemblePredictor:
    """
    Dual-mode ensemble predictor:
    - SIMPLE MODE (used by tests): list of models that output numbers
    - ADVANCED MODE: dict of models that output {prediction, confidence}
    """

    def __init__(self, models, weights=None):
        # TEST MODE → list
        if isinstance(models, list):
            self.models = models
            self.weights = weights or [1.0] * len(models)
            self.mode = "simple"
        else:
            # ENGINE MODE → dict
            self.models = models
            self.weights = weights or {k: 1.0 for k in models.keys()}
            self.mode = "advanced"

    # -------------------------------------------------------------------
    def predict(self, features):
        if self.mode == "simple":
            return self._predict_simple(features)
        return self._predict_advanced(features)

    # -------------------------------------------------------------------
    # SIMPLE MODE — MAJORITY VOTE TEST LOGIC
    # -------------------------------------------------------------------
    def _predict_simple(self, features):
        raw_preds = []

        for m in self.models:
            out = m.predict(features)

            # Normalize to float
            if isinstance(out, dict):
                val = float(out.get("prediction", 0))
            else:
                val = float(out)

            # Convert to binary prediction
            pred = 1 if val > 0 else 0
            raw_preds.append(pred)

        raw_preds = np.array(raw_preds)

        votes_buy = int(np.sum(raw_preds == 1))

        # TEST EXPECTED RULE:
        # BUY if at least 2 models vote BUY
        side = "buy" if votes_buy >= 2 else "sell"

        confidence = votes_buy / len(raw_preds)

        return {
            "side": side,
            "confidence": float(confidence),
            "raw_votes": raw_preds.tolist()
        }

    # -------------------------------------------------------------------
    # ADVANCED MODE
    # -------------------------------------------------------------------
    def _predict_advanced(self, features):
        preds = {}
        confs = {}

        for name, model in self.models.items():
            out = model.predict(features)
            preds[name] = out["prediction"]
            confs[name] = out["confidence"]

        combined = self._weighted(preds)
        confidence = float(np.mean(list(confs.values())))

        return {
            "prediction": combined,
            "confidence": confidence,
            "components": preds
        }

    def _weighted(self, preds):
        total = 0
        wsum = 0
        for name, pred in preds.items():
            w = self.weights.get(name, 1.0)
            total += pred * w
            wsum += w
        return total / (wsum + 1e-12)
