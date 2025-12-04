import numpy as np

def safe_divide(a, b, default=0.0):
    try:
        return a / b if b else default
    except:
        return default

def normalize(v):
    arr = np.array(v, dtype=float)
    mn, mx = np.min(arr), np.max(arr)
    if mx - mn == 0:
        return arr * 0
    return (arr - mn) / (mx - mn)

def returns(prices):
    p = np.array(prices, dtype=float)
    return np.diff(p) / p[:-1]

def exp_smooth(values, alpha=0.3):
    result = [values[0]]
    for v in values[1:]:
        result.append(alpha * v + (1 - alpha) * result[-1])
    return result
