"""Smallest G: isolate, add, Leibniz-mul, quot, rate."""
from __future__ import annotations
from fractions import Fraction as F


class Theta(Exception):
    pass


def Q(x):
    return x if isinstance(x, F) else F(x)


class Reading:
    __slots__ = ("v", "r")

    def __init__(self, v, r):
        self.v, self.r = Q(v), Q(r)

    def __repr__(self):
        return f"({self.v}, {self.r})"

    def _o(self, o):
        return o if isinstance(o, Reading) else Reading(o, 0)

    def __add__(self, o):
        o = self._o(o)
        return Reading(self.v + o.v, self.r + o.r)

    def __radd__(self, o):
        return self._o(o) + self

    def __sub__(self, o):
        o = self._o(o)
        return Reading(self.v - o.v, self.r - o.r)

    def __rsub__(self, o):
        return self._o(o) - self

    def __mul__(self, o):
        o = self._o(o)
        return Reading(self.v * o.v, self.r * o.v + self.v * o.r)

    def __rmul__(self, o):
        return self._o(o) * self

    def __truediv__(self, o):
        o = self._o(o)
        if o.v == 0:
            raise Theta("quot: divisor value 0")
        return Reading(self.v / o.v, (self.r * o.v - self.v * o.r) / (o.v * o.v))

    def __rtruediv__(self, o):
        return self._o(o) / self

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise Theta("pow: n integer >= 0")
        out = Reading(1, 0)
        for _ in range(n):
            out = out * self
        return out

    def __neg__(self):
        return Reading(-self.v, -self.r)


def isolate(value, seed=1) -> Reading:
    return Reading(value, seed)


def rate(top: Reading, bottom: Reading) -> F:
    if bottom.r == 0:
        raise Theta("rate: isolator channel is dead")
    return top.r / bottom.r
