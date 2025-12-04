import sys, os
sys.path.insert(0, os.getcwd())

from core.utils.math_utils import safe_divide, normalize
from core.utils.time_utils import now_utc, timestamp
from core.utils.decorators import time_execution

print("Safe divide:", safe_divide(10, 2))
print("Safe divide zero:", safe_divide(10, 0))
print("Time now:", now_utc())
print("Timestamp:", timestamp())

@time_execution
def slow_fn():
    total = 0
    for i in range(1000000):
        total += i
    return total

print("Slow fn:", slow_fn())
