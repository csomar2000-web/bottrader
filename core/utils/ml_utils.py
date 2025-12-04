import numpy as np
from datetime import datetime, timezone

def ema(series, span=10):
    return np.array(pd.Series(series).ewm(span=span).mean())

def moving_average(series, window=10):
    return np.convolve(series, np.ones(window)/window, mode='valid')

def zscore(series, window=20):
    s = pd.Series(series)
    return ((s - s.rolling(window).mean()) / s.rolling(window).std()).fillna(0).values

def rolling_volatility(series, window=20):
    s = pd.Series(series)
    return s.pct_change().rolling(window).std().fillna(0).values

def pct_change(series):
    return np.diff(series) / series[:-1]

def timestamp():
    return datetime.now(timezone.utc).isoformat()
