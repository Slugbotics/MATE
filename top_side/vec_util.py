import math


def div_vec(v : tuple[float, float], n : float) -> tuple[float, float]:
    x, y = v
    return (x / n, y / n)

def magnitude(vec : tuple[float, float]) -> float:
    x, y = vec
    return math.sqrt(x * x + y * y)

def dot(a : tuple[float, float], b : tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    return ax * bx + ay * by

