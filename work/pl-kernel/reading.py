"""Readings, mix, rate, θ."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F


class Theta(Exception):
    """Input is not in the domain of this op. Not a value."""


class LeavesV(Exception):
    """Input is not in V = Q."""


def Q(x) -> F:
    if isinstance(x, F):
        return x
    if isinstance(x, bool):
        raise LeavesV("bool is not Q")
    if isinstance(x, int):
        return F(x)
    raise LeavesV(f"not in Q: {type(x).__name__}")


@dataclass(frozen=True)
class Reading:
    """Value + channel under one isolation. Arithmetic is Leibniz mix."""

    v: F
    r: F

    def __repr__(self) -> str:
        return f"Reading({self.v}, {self.r})"

    def _other(self, o) -> "Reading":
        if isinstance(o, Reading):
            return o
        return Reading(Q(o), F(0))

    def __add__(self, o):
        o = self._other(o)
        return Reading(self.v + o.v, self.r + o.r)

    def __radd__(self, o):
        return self._other(o) + self

    def __sub__(self, o):
        o = self._other(o)
        return Reading(self.v - o.v, self.r - o.r)

    def __rsub__(self, o):
        return self._other(o) - self

    def __mul__(self, o):
        o = self._other(o)
        return Reading(self.v * o.v, self.r * o.v + self.v * o.r)

    def __rmul__(self, o):
        return self._other(o) * self

    def __truediv__(self, o):
        o = self._other(o)
        if o.v == 0:
            raise Theta("quot: denominator v=0")
        return Reading(
            self.v / o.v,
            (self.r * o.v - self.v * o.r) / (o.v * o.v),
        )

    def __rtruediv__(self, o):
        return self._other(o) / self

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise LeavesV("pow only for integer n >= 0 on this V")
        out = Reading(F(1), F(0))
        for _ in range(n):
            out = out * self
        return out

    def __neg__(self):
        return Reading(-self.v, -self.r)


def isolate(value, seed=1) -> Reading:
    """Pay a cut. seed is the isolation scale. seed=0 is a constant."""
    return Reading(Q(value), Q(seed))


def rate(top: Reading, bottom: Reading) -> F:
    """Binary comparison. Isolation is the second argument."""
    if not isinstance(top, Reading) or not isinstance(bottom, Reading):
        raise TypeError("rate takes two Readings")
    if bottom.r == 0:
        raise Theta("rate: isolation channel r=0")
    return top.r / bottom.r


def relate(P: Reading, S: Reading) -> Reading:
    """P against S as readings. Scalar form of a binary isolation."""
    return P - S
