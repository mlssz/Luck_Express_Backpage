"""
Base utils for backpage
"""
import math
import threading

degree = math.pi / 180

def compute_distance(A: "tuple", B: "tuple") -> "float":
    """Compute distance between rental and lessee."""
    x1, y1 = A
    x2, y2 = B

    distance = 6378.138 * 2 * math.asin(math.sqrt(
        math.pow(math.sin((x1 * degree -x2 * degree) / 2), 2)
        + math.cos(x1 * degree) * math.cos(x2 * degree)
        * math.pow(math.sin((y1 * degree - y2 * degree) / 2), 2)
    )) * 1000

    return distance

def _setInterval(inc, func, params):
    if func(*params):
        setInterval(inc, func, params)

def setInterval(inc, func, params):
    """
    loop func in a new threading until the value of func returned is False.
    """
    threading.Timer(inc, _setInterval, (inc, func, params)).start()
