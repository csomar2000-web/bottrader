# import numpy as np
# import pandas as pd
# from typing import Dict, Any
# from core.utils import ema, moving_average, zscore, rolling_volatility, pct_change


# class FeatureEngineering:
#     """
#     Feature engineering module
#     Compatible with both the engine and test suite.
#     """

#     def __init__(self, cfg: Dict[str, Any] = None):
#         self.cfg = cfg or {}

#     # ---------------------------------------------------------------------
#     # TEST SUITE EXPECTED FUNCTION
#     # ---------------------------------------------------------------------
#     def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
#         df = df.copy()

#         closes = df["close"].values
#         df["returns"] = np.concatenate([[0], pct_change(closes)])
#         df["ma_fast"] = moving_average(closes, 5)
#         df["ma_slow"] = moving_average(closes, 20)
#         df["ema_10"] = ema(closes, span=10)
#         df["ema_20"] = ema(closes, span=20)
#         df["volatility"] = rolling_volatility(closes, 20)
#         df["zscore"] = zscore(closes, 20)

#         df.fillna(0, inplace=True)
#         return df

#     # ---------------------------------------------------------------------
#     # STANDARDIZE VECTOR FOR ML (test expects this!)
#     # ---------------------------------------------------------------------
#     def normalize(self, x):
#         x = np.asarray(x, dtype=float)
#         mn, mx = np.min(x), np.max(x)
#         return (x - mn) / (mx - mn + 1e-12)

#     # ---------------------------------------------------------------------
#     # ADVANCED ENGINE FEATURES
#     # ---------------------------------------------------------------------
#     def technical(self, df: pd.DataFrame) -> pd.DataFrame:
#         df = df.copy()
#         df["return"] = df["close"].pct_change()
#         df["ema_fast"] = df["close"].ewm(span=12).mean()
#         df["ema_slow"] = df["close"].ewm(span=26).mean()
#         df["macd"] = df["ema_fast"] - df["ema_slow"]
#         df["signal"] = df["macd"].ewm(span=9).mean()
#         df["rsi"] = self.rsi(df["close"], 14)
#         df["atr"] = self.atr(df, 14)
#         df["vol"] = df["return"].rolling(20).std()
#         df["zclose"] = zscore(df["close"].values)
#         df["mom_5"] = df["close"].pct_change(5)
#         df["mom_10"] = df["close"].pct_change(10)
#         return df.fillna(0)

#     def microstructure(self, df: pd.DataFrame) -> pd.DataFrame:
#         df = df.copy()
#         df["spread"] = df["ask"] - df["bid"]
#         df["mid"] = (df["ask"] + df["bid"]) / 2
#         df["imbalance"] = df["bid_volume"] / (
#             df["ask_volume"] + df["bid_volume"] + 1e-9
#         )
#         return df.fillna(0)

#     def sentiment(self, sentiment: Dict[str, float]) -> Dict[str, float]:
#         return {
#             "sent_score": sentiment.get("score", 0),
#             "sent_volume": sentiment.get("volume", 0),
#             "sent_trend": sentiment.get("trend", 0),
#         }

#     def onchain(self, metrics: Dict[str, float]) -> Dict[str, float]:
#         return {
#             "whale_flow": metrics.get("whale_flow", 0),
#             "exchange_in": metrics.get("exchange_in", 0),
#             "exchange_out": metrics.get("exchange_out", 0),
#         }

#     def regime(self, r: str) -> Dict[str, int]:
#         return {
#             "regime_trend": int(r == "trend"),
#             "regime_range": int(r == "range"),
#             "regime_high_vol": int(r == "high_volatility"),
#             "regime_low_vol": int(r == "low_volatility"),
#         }

#     # ------------------------ Indicators ------------------------
#     def rsi(self, series: pd.Series, period: int) -> pd.Series:
#         diff = series.diff()
#         up = diff.clip(lower=0).ewm(com=period - 1).mean()
#         down = -diff.clip(upper=0).ewm(com=period - 1).mean()
#         rs = up / (down + 1e-9)
#         return 100 - (100 / (1 + rs))

#     def atr(self, df: pd.DataFrame, period: int) -> pd.Series:
#         high_low = df["high"] - df["low"]
#         high_close = (df["high"] - df["close"].shift()).abs()
#         low_close = (df["low"] - df["close"].shift()).abs()
#         tr = high_low.combine(high_close, max).combine(low_close, max)
#         return tr.ewm(span=period).mean()

#     # ------------------- Feature Vector Builder -------------------
#     def build_feature_vector(self, df, sentiment, onchain, regime):
#         t = df.iloc[-1].to_dict()
import numpy as np
import pandas as pd
from typing import Dict, Any
from core.utils import ema, moving_average, zscore, rolling_volatility, pct_change


class FeatureEngineering:

    def __init__(self, cfg=None):
        self.cfg = cfg or {}

    # REQUIRED BY TEST SUITE
    def add_features(self, df):
        df = df.copy()
        closes = df["close"].values

        df["returns"] = np.concatenate([[0], pct_change(closes)])
        df["ma_fast"] = moving_average(closes, 5)
        df["ma_slow"] = moving_average(closes, 20)
        df["ema_10"] = ema(closes, 10)
        df["ema_20"] = ema(closes, 20)
        df["volatility"] = rolling_volatility(closes, 20)
        df["zscore"] = zscore(closes, 20)

        df.fillna(0, inplace=True)
        return df

    # REQUIRED FOR TESTS
    def normalize(self, x):
        x = np.asarray(x, dtype=float)
        mn, mx = np.min(x), np.max(x)
        return (x - mn) / (mx - mn + 1e-12)

    # --- extra engine functions -----------------------------

    def rsi(self, series, period):
        diff = series.diff()
        up = diff.clip(lower=0).ewm(com=period - 1).mean()
        down = -diff.clip(upper=0).ewm(com=period - 1).mean()
        rs = up / (down + 1e-9)
        return 100 - (100 / (1 + rs))

    def atr(self, df, period):
        hl = df["high"] - df["low"]
        hc = (df["high"] - df["close"].shift()).abs()
        lc = (df["low"] - df["close"].shift()).abs()
        tr = hl.combine(hc, max).combine(lc, max)
        return tr.ewm(span=period).mean()

    def build_feature_vector(self, df, sentiment, onchain, regime):
        t = df.iloc[-1].to_dict()
        return {
            **t,
            "sent_score": sentiment.get("score", 0),
            "sent_volume": sentiment.get("volume", 0),
            "sent_trend": sentiment.get("trend", 0),
            "whale_flow": onchain.get("whale_flow", 0),
            "exchange_in": onchain.get("exchange_in", 0),
            "exchange_out": onchain.get("exchange_out", 0),
            "regime_trend": int(regime == "trend"),
            "regime_range": int(regime == "range"),
            "regime_high_vol": int(regime == "high_volatility"),
            "regime_low_vol": int(regime == "low_volatility"),
        }
