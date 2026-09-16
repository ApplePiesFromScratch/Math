#!/usr/bin/env python3
"""PROCESS.py — standalone cut to get back here.

Stdlib only. Copy this file. Run it. The rest of the repo is a view.

    python PROCESS.py

================================================================
STANCE
================================================================
A name introduces structure. It does not uncover essence.
Nouns compress. Compression is not ontology.
isolate is unpriced (floor). Guards, μ, and reconfig are not.
Frame ≠ tic. View must not write V_game.
Infinity and extra circles are θ dressed as V.

================================================================
KNOBS (only these)
================================================================
V     alphabet the presentation returns
G     maps allowed on V (isolation lives here)
θ     admission / refusal / budget
constant:  P / G → Q

================================================================
FIVE GUARDRAILS
================================================================
1. No named V, G, θ          → not a claim yet
2. Two presentations agree   → grow V before calling them one G
3. Step leaves V             → fire θ or run registered μ
4. Label changes no knob     → comment (no insight, no cost)
5. Work happened             → ledger line or the ledger is lying

================================================================
THIS FILE HOLDS
================================================================
Reading + isolate + rate + mix     exact Q forward AD
Certificate / certify              grid + gauge + falsifier
Ledger + Guard + μ + Runtime       v0.3 metageneration
Prescreen                          ADMIT / DEFER / REFUSE
INSIGHTS / PATH / FILES            the map back

Not in this file (other V's, still maps):
  phys2d, gamephys, doomtic, pong, breakout, sky machines.
  They obey the same knobs. Rebuild from PATH + GUARDRAILS.

================================================================
NON-CLAIMS
================================================================
This is not how variation, the sky, or games *are*.
Load prices are stipulated.
FORCED-on-cut does not lift off the cut.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from fractions import Fraction as F
from itertools import product
from typing import Any, Callable
import json
import sys


# ══════════════════════════════════════════════════════════════════════
# REFUSALS
# ══════════════════════════════════════════════════════════════════════
class Theta(Exception):
    """Not in domain. Not a value."""


class Decohered(Exception):
    """Ledger past θ. State may exist; result is not legal."""


class ChannelPreservationError(Theta):
    """Live channel would be orphaned by μ."""


class LeavesV(Exception):
    """Input not in declared V."""


# ══════════════════════════════════════════════════════════════════════
# V = Q
# ══════════════════════════════════════════════════════════════════════
def Q(x) -> F:
    if isinstance(x, F):
        return x
    if isinstance(x, bool):
        raise LeavesV("bool is not Q")
    if isinstance(x, int):
        return F(x)
    raise LeavesV(f"not in Q: {type(x).__name__}")


# ══════════════════════════════════════════════════════════════════════
# READING + RATE  (process-calc / cutad kernel)
# ══════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Reading:
    """Value + channel under one isolation. Mix is Leibniz."""
    v: F
    r: F

    def __repr__(self):
        return f"Reading({self.v}, {self.r})"

    def _o(self, o):
        return o if isinstance(o, Reading) else Reading(Q(o), F(0))

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
            raise Theta("quot: v=0")
        return Reading(self.v / o.v, (self.r * o.v - self.v * o.r) / (o.v * o.v))

    def __rtruediv__(self, o):
        return self._o(o) / self

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise LeavesV("pow: n integer >= 0")
        out = Reading(F(1), F(0))
        for _ in range(n):
            out = out * self
        return out

    def __neg__(self):
        return Reading(-self.v, -self.r)


def isolate(value, seed=1) -> Reading:
    """Pay a cut. seed=0 is a constant. Floor: unpriced."""
    return Reading(Q(value), Q(seed))


def rate(top: Reading, bottom: Reading) -> F:
    if not isinstance(top, Reading) or not isinstance(bottom, Reading):
        raise TypeError("rate takes two Readings")
    if bottom.r == 0:
        raise Theta("rate: isolation r=0")
    return top.r / bottom.r


# ══════════════════════════════════════════════════════════════════════
# CERTIFICATE
# ══════════════════════════════════════════════════════════════════════
def tier(discharged, scope) -> str:
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

    def as_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def certify(fn, at=3, values=(-4, -3, -2, -1, 1, 2, 3, 4),
            seeds=(1, 2, F(1, 2), -1)) -> Certificate:
    x0 = isolate(at, 1)
    r0 = rate(fn(x0), x0)
    discharged = scope = 0
    gauge_ok = True
    for v, k in product([Q(v) for v in values], [Q(k) for k in seeds]):
        scope += 1
        try:
            r = rate(fn(isolate(v, k)), isolate(v, k))
            r1 = rate(fn(isolate(v, 1)), isolate(v, 1))
        except Theta:
            continue
        discharged += 1
        if r != r1:
            gauge_ok = False
    ok = gauge_ok and discharged > 0
    return Certificate(
        statement=f"rate(fn(x),x) at {at} is {r0}; gauge on declared grid",
        value=str(r0),
        ok=ok,
        discharged=discharged,
        scope=scope,
        tier=tier(discharged if gauge_ok else 0, scope) if ok else "UNPAID",
        falsifier="exhibit v,k on the grid where rate depends on seed",
        cut=f"values={list(values)} seeds={list(map(str, seeds))}",
        gauge_ok=gauge_ok,
    )


# ══════════════════════════════════════════════════════════════════════
# LEDGER  (v0.3 — metageneration on the same book)
# ══════════════════════════════════════════════════════════════════════
STEP, GUARD, RECONFIG, MIGRATE, REIFY = (
    "STEP", "GUARD", "RECONFIG", "MIGRATE", "REIFY",
)
PRICE = {STEP: F(1), GUARD: F(1, 4), RECONFIG: F(2), MIGRATE: F(1), REIFY: F(1)}


@dataclass
class Line:
    kind: str
    amount: F
    note: str


@dataclass
class Ledger:
    theta: F = F(32)
    lines: list = field(default_factory=list)

    @property
    def total(self) -> F:
        return sum((ln.amount for ln in self.lines), F(0))

    def charge(self, kind: str, amount, note: str = "") -> None:
        amt = amount if isinstance(amount, F) else F(amount)
        if amt < 0:
            raise Theta("no negative metageneration")
        self.lines.append(Line(kind, amt, note))
        if self.total > self.theta:
            raise Decohered(f"ledger {self.total} > θ {self.theta}")


# ══════════════════════════════════════════════════════════════════════
# CARRIER + μ
# ══════════════════════════════════════════════════════════════════════
@dataclass
class Carrier:
    name: str
    contains: Callable[[Any], bool]
    has_channel: bool = False

    def live_channel(self, state) -> bool:
        if not self.has_channel or not isinstance(state, tuple) or len(state) < 2:
            return False
        return state[1] != 0


def _in_v2(x):
    return x in (F(0), F(1), 0, 1)


def _in_v3(x):
    return x in (F(0), F(1, 2), F(1), 0, 1)


def _in_pair(x):
    return isinstance(x, tuple) and len(x) == 2


V2 = Carrier("V2", _in_v2)
V3 = Carrier("V3", _in_v3)
QPAIR = Carrier("QPAIR", _in_pair, has_channel=True)


@dataclass
class Migration:
    src: str
    dst: str
    fn: Callable
    cost: F
    note: str


def _pair_to_v3(x):
    v, r = x
    if r != 0:
        raise ChannelPreservationError("live r cannot enter V3")
    if v not in (F(0), F(1, 2), F(1)):
        raise Theta(f"{v} not in V3")
    return v


MAPS = {
    ("V2", "V3"): Migration("V2", "V3", lambda x: F(x), F(1, 2), "embed"),
    ("V3", "QPAIR"): Migration("V3", "QPAIR", lambda x: (F(x), F(0)), F(1), "open dead r"),
    ("QPAIR", "V3"): Migration("QPAIR", "V3", _pair_to_v3, F(2), "drop dead r"),
    ("V2", "V2"): Migration("V2", "V2", lambda x: x, F(0), "id"),
    ("V3", "V3"): Migration("V3", "V3", lambda x: x, F(0), "id"),
    ("QPAIR", "QPAIR"): Migration("QPAIR", "QPAIR", lambda x: x, F(0), "id"),
}


def lookup(src, dst) -> Migration:
    m = MAPS.get((src, dst))
    if m is None:
        raise Theta(f"no μ {src}→{dst}")
    return m


@dataclass
class Runtime:
    carrier: Carrier
    state: Any
    ledger: Ledger = field(default_factory=Ledger)

    def guard(self, ok: bool, note: str) -> bool:
        self.ledger.charge(GUARD, PRICE[GUARD], note)
        return ok

    def step(self, fn, note="step"):
        self.ledger.charge(STEP, PRICE[STEP], note)
        out = fn(self.state)
        if not self.carrier.contains(out):
            raise Theta(f"step left {self.carrier.name}: {out}")
        self.state = out
        return out

    def reconfigure(self, dst: Carrier, reason: str) -> None:
        self.ledger.charge(RECONFIG, PRICE[RECONFIG], reason)
        mig = lookup(self.carrier.name, dst.name)
        if not self.guard(
            not (self.carrier.live_channel(self.state) and not dst.has_channel),
            f"preserve {self.carrier.name}→{dst.name}",
        ):
            raise ChannelPreservationError(
                f"live channel in {self.carrier.name} has no slot in {dst.name}"
            )
        self.ledger.charge(MIGRATE, mig.cost, mig.note)
        new = mig.fn(self.state)
        if not dst.contains(new):
            raise Theta(f"μ({self.state})={new} not in {dst.name}")
        self.carrier, self.state = dst, new


# ══════════════════════════════════════════════════════════════════════
# PRESCREEN
# ══════════════════════════════════════════════════════════════════════
def prescreen(ops_in_G, values_in_V, theta_legal, quantifier, conclusion_holds=True):
    """Tiny gate. Full matrix lives in cutad.prescreen."""
    if not values_in_V:
        return "REFUSE", "value not in V"
    if not ops_in_G:
        return "REFUSE", "op not in G"
    if not theta_legal:
        return "REFUSE", "θ on hypotheses"
    if quantifier == "all R":
        return "DEFER", "unlistable V"
    if not conclusion_holds:
        return "REFUSE", "conclusion fails on listed V"
    return "ADMIT", "typed on this cut"


# ══════════════════════════════════════════════════════════════════════
# MAP BACK  (insights + path + files)
# ══════════════════════════════════════════════════════════════════════
INSIGHTS = [
    ("knobs-three", "Every system here is V,G,θ. P/G→Q is constant."),
    ("name-introduces-structure", "A name installs a cut. G1=Tycho-circles was a comment."),
    ("and-not-one-op", "min/prod/luk agree on V2; prod leaves V3."),
    ("derivative-not-one-op", "unary D vs rate(P,G) vs fd=6+h."),
    ("rate-is-ratio", "Isolation is an argument. Gauge holds across seeds."),
    ("zero-over-zero", "quot refuses; rate((0,6),(0,1))=6."),
    ("fd-reconstructs", "h rebuilds a discarded channel."),
    ("certificate", "statement, cut, discharged/scope, tier, falsifier."),
    ("accuracy-is-channel", "e on rate(M,S) 25°→3.8°; extra circles on locked seed worse."),
    ("heliocentric-is-binary-rate", "rate(Mars_geo,Sun_geo) of already-paid channels."),
    ("epicycle-is-fourier", "G_center warps angle; G_stretch warps radius."),
    ("slop-is-theta", "Hard contact claims a V it does not hold."),
    ("maximal-vs-reduced", "Joint in V vs reconstructed each step."),
    ("smaller-dt-is-infinity", "Unnamed smaller dt puts ∞ in V."),
    ("video-game-carrier", "V_game+G_tic(V_in)+θ_game. View must not write the tic."),
    ("pong-is-sliders", "1972 already mechanism-first."),
    ("breakout-leaves-V", "Bricks leave V; empty set designated."),
    ("doom-door-slider", "Sector height is Slider1. Not PhysX."),
    ("state-migration", "V change only by registered μ."),
    ("metageneration-on-ledger", "GUARD/RECONFIG/MIGRATE are line items."),
    ("reification-pathological", "The cut does not get to be the room."),
]

PATH = [
    ("pong", 1972, "built", "ball+2 sliders"),
    ("breakout", 1976, "built", "bricks leave V"),
    ("invaders", 1978, "listed", "formation mechanism"),
    ("asteroids", 1979, "listed", "torus wrap"),
    ("pacman", 1980, "listed", "graph V — plane is wrong"),
    ("platformer", 1981, "gamephys", "Free2+jump"),
    ("doom-class", 1993, "doomtic", "linedefs+sector sliders"),
]

FILES = {
    "this": "PROCESS.py",
    "kernel": ["cutad/reading.py", "cutad/certify.py", "cutad/migrate.py"],
    "docs": [
        "docs/GUARDRAILS.md", "docs/PL_V03.md", "docs/OPERATOR_GUIDE.md",
        "docs/GAME_CARRIER.md", "docs/GAME_HISTORY_PL.md", "docs/PHYSICS_ENGINES.md",
        "insights.json",
    ],
}


def dump_map() -> str:
    return json.dumps(
        {"insights": INSIGHTS, "path": PATH, "files": FILES, "prices": {k: str(v) for k, v in PRICE.items()}},
        indent=2,
    )


# ══════════════════════════════════════════════════════════════════════
def selfcheck() -> int:
    fails = 0

    def ok(name, cond):
        nonlocal fails
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        fails += not cond

    x = isolate(3)
    ok("rate(x*x,x)=6", rate(x * x, x) == 6)
    ok("gauge", rate(isolate(3, 2) ** 2, isolate(3, 2)) == 6)
    ok("0/0 channels", rate(isolate(0, 6), isolate(0, 1)) == 6)
    try:
        rate(x, isolate(3, 0))
        ok("θ dead isolation", False)
    except Theta:
        ok("θ dead isolation", True)
    c = certify(lambda z: z * z, at=3)
    ok("cert 6 FORCED-on-cut", c.ok and c.value == "6" and c.tier == "FORCED-on-cut")

    rt = Runtime(V2, F(1))
    rt.reconfigure(V3, "grow")
    ok("μ V2→V3", rt.carrier.name == "V3" and rt.state == F(1))
    live = Runtime(QPAIR, (F(1), F(3)))
    try:
        live.reconfigure(V3, "drop live")
        ok("preserve live r", False)
    except ChannelPreservationError:
        ok("preserve live r", True)
    silent = Runtime(V2, F(1))
    silent.step(lambda s: s)
    loud = Runtime(V2, F(1))
    loud.guard(True, "g")
    loud.reconfigure(V3, "grow")
    ok("meta costs more than a step", loud.ledger.total > silent.ledger.total)
    tight = Runtime(V2, F(1), Ledger(theta=F(2)))
    try:
        tight.reconfigure(V3, "blow")
        ok("decohere over θ", False)
    except Decohered:
        ok("decohere over θ", True)

    v, r = prescreen(True, True, False, "all V")
    ok("prescreen θ", v == "REFUSE")
    v, r = prescreen(True, True, True, "all R")
    ok("prescreen defer", v == "DEFER")
    return fails


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    if argv[1:] == ["map"]:
        print(dump_map())
        return 0
    print("PROCESS.py  V/G/θ kernel + ledger + μ + map")
    print("  copy this file. run it. that is enough to get back here.")
    print()
    n = selfcheck()
    print()
    print(f"  insights {len(INSIGHTS)}  path {len(PATH)}  prices { {k: str(v) for k,v in PRICE.items()} }")
    print("verdict", "PASS" if n == 0 else "FAIL")
    return n


if __name__ == "__main__":
    raise SystemExit(main())
