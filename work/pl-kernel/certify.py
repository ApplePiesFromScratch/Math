"""Certificates: scope, tier, falsifier."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import product
from typing import Callable
import json

from pl.reading import LeavesV, Reading, Theta, isolate, rate, Q


def tier(discharged: int, scope: int | None) -> str:
    if scope in (None, 0):
        return "UNPAID"
    if discharged == scope:
        return "FORCED-on-cut"
    if discharged > 0:
        return "EMPIRICAL"
    return "UNPAID"


@dataclass
class Certificate:
    statement: str
    value: str
    ok: bool
    discharged: int
    scope: int
    tier: str
    falsifier: str
    cut: str
    gauge_ok: bool
    fd_last: str | None
    fd_steps: int | None

    def as_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


DEFAULT_VALUES = (-4, -3, -2, -1, 1, 2, 3, 4)
DEFAULT_SEEDS = (1, 2, F(1, 2), -1)


def finite_difference(f_scalar, x, h=F(1, 1024)) -> F:
    x, h = Q(x), Q(h)
    if h == 0:
        raise Theta("fd: h=0")
    return (f_scalar(x + h) - f_scalar(x)) / h


def certify(
    fn: Callable[[Reading], Reading],
    at=None,
    values=DEFAULT_VALUES,
    seeds=DEFAULT_SEEDS,
    vs_fd: bool = True,
) -> Certificate:
    """Gauge-check fn on a declared grid and return a certificate.

    fn maps a Reading to a Reading. `value` is rate(fn(x), x) at `at`
    with seed 1. ok requires the ratio independent of seed on every
    live grid point.
    """
    if at is None:
        at = next(v for v in values if v != 0)
    x0 = isolate(at, 1)
    r0 = rate(fn(x0), x0)

    discharged = 0
    scope = 0
    gauge_ok = True
    for v, k in product([Q(v) for v in values], [Q(k) for k in seeds]):
        scope += 1
        z = isolate(v, k)
        try:
            r = rate(fn(z), z)
            r1 = rate(fn(isolate(v, 1)), isolate(v, 1))
        except Theta:
            continue
        discharged += 1
        if r != r1:
            gauge_ok = False

    fd_last = fd_steps = None
    if vs_fd:
        def f_at(t):
            return fn(isolate(t, 1)).v

        last = None
        h = Q(1)
        steps = 0
        for steps in range(1, 16):
            try:
                last = (f_at(Q(at) + h) - f_at(Q(at))) / h
            except (Theta, LeavesV, ZeroDivisionError):
                break
            if last == r0:
                break
            h = h / 2
        fd_last = str(last) if last is not None else None
        fd_steps = steps

    ok = gauge_ok and discharged > 0
    return Certificate(
        statement=f"rate(fn(x), x) at x={at} is {r0}; gauge on declared grid",
        value=str(r0),
        ok=ok,
        discharged=discharged,
        scope=scope,
        tier=tier(discharged if gauge_ok else 0, scope) if ok else "UNPAID",
        falsifier=(
            "exhibit v,k on the grid with "
            "rate(fn(isolate(v,k)), isolate(v,k)) != rate(..., seed=1)"
        ),
        cut=f"values={list(values)} seeds={list(map(str, seeds))}",
        gauge_ok=gauge_ok,
        fd_last=fd_last,
        fd_steps=fd_steps,
    )
