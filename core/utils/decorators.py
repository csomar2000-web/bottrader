import time
from functools import wraps

def time_execution(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        s = time.time()
        r = fn(*a, **kw)
        print(f"{fn.__name__} executed in {time.time()-s:.4f}s")
        return r
    return wrapper
