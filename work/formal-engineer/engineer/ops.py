"""Candidate operations. Each is a cut, not an essence."""
from fractions import Fraction as F


def NOT(v):
    return F(1) - v


def AND_min(a, b):
    return min(a, b)


def AND_prod(a, b):
    return a * b


def AND_luk(a, b):
    return max(F(0), a + b - F(1))


def OR_max(a, b):
    return max(a, b)


def OR_luk(a, b):
    return min(F(1), a + b)


def OR_prod(a, b):
    return a + b - a * b


POOL = {
    "NOT": (1, NOT),
    "AND_min": (2, AND_min),
    "AND_prod": (2, AND_prod),
    "AND_luk": (2, AND_luk),
    "OR_max": (2, OR_max),
    "OR_luk": (2, OR_luk),
    "OR_prod": (2, OR_prod),
}


def parse_V(spec):
    out = []
    for p in spec.split(","):
        p = p.strip()
        if "/" in p:
            n, d = p.split("/")
            out.append(F(int(n), int(d)))
        else:
            out.append(F(p))
    return tuple(out)
