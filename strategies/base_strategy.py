from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import numpy as np
from datetime import datetime

class Strategy(ABC):
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.last_signal = None
        self.position = None
        self.enabled = True
        self.metadata = {}

    def preprocess(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        x = market_data.copy()
        x["timestamp"] = datetime.utcnow().timestamp()
        x["mid"] = (x.get("bid", 0) + x.get("ask", 0)) / 2
        return x

    @abstractmethod
    def generate_signal(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    def postprocess(self, signal: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if signal is None:
            return None
        signal["strategy"] = self.name
        signal["timestamp"] = datetime.utcnow().isoformat()
        self.last_signal = signal
        return signal

    def run(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return None
        d = self.preprocess(market_data)
        s = self.generate_signal(d)
        return self.postprocess(s)

    def update_position(self, position: Dict[str, Any]):
        self.position = position

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def confidence(self, x: float) -> float:
        return max(0.0, min(1.0, float(x)))

    def apply_filters(self, signal: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if signal is None:
            return None
        if "confidence" in signal:
            if signal["confidence"] < self.config.get("min_confidence", 0.1):
                return None
        return signal
