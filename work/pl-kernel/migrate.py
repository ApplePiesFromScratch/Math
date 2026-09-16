"""migrate.py — state migration maps + metageneration on the ledger.

When V changes mid-execution, state does not teleport. A registered
map μ: V_src → V_dst runs, or θ fires. The map, the guard that
decided to reconfigure, and the reconfiguration choice itself are
line items on the same ledger as the step. They are not free.

    python -m pl.migrate
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as F
from typing import Any, Callable


class Theta(Exception):
    pass


class Decohered(Exception):
    pass


class ChannelPreservationError(Theta):
    """Live channel would be orphaned by μ. Not a scalar Theta."""
    pass


# ── ledger ────────────────────────────────────────────────────────────
# kinds billed on the primary execution ledger (not a sidecar)
STEP = "STEP"
GUARD = "GUARD"
RECONFIG = "RECONFIG"
MIGRATE = "MIGRATE"
REIFY = "REIFY"


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
            raise Theta("ledger does not take negative metageneration")
        self.lines.append(Line(kind, amt, note))
        if self.total > self.theta:
            raise Decohered(f"ledger {self.total} > θ {self.theta}")


# default prices (stipulated — they are G of the budget carrier)
PRICE = {
    STEP: F(1),
    GUARD: F(1, 4),       # a θ-check, pass or fail
    RECONFIG: F(2),       # choosing a new presentation
    MIGRATE: F(1),        # running μ
    REIFY: F(1),
}


# ── carriers as named alphabets ───────────────────────────────────────
@dataclass
class Carrier:
    name: str
    contains: Callable[[Any], bool]
    note: str = ""
    has_channel: bool = False

    def live_channel(self, state) -> bool:
        if not self.has_channel:
            return False
        if isinstance(state, tuple) and len(state) >= 2:
            return state[1] != 0
        return False


def _in_v2(x) -> bool:
    return x in (F(0), F(1), 0, 1)


def _in_v3(x) -> bool:
    return x in (F(0), F(1, 2), F(1), 0, 1, 0.5)


def _in_q_pairs(x) -> bool:
    return isinstance(x, tuple) and len(x) == 2


def _in_q_triples(x) -> bool:
    return isinstance(x, tuple) and len(x) == 3


V2 = Carrier("V2", _in_v2, "{0,1}")
V3 = Carrier("V3", _in_v3, "{0,1/2,1}")
QPAIR = Carrier("QPAIR", _in_q_pairs, "(v,r)", has_channel=True)
QJET2 = Carrier("QJET2", _in_q_triples, "(v,r,r2)", has_channel=True)


# ── migration maps ────────────────────────────────────────────────────
@dataclass
class Migration:
    src: str
    dst: str
    fn: Callable[[Any], Any]
    cost: F = PRICE[MIGRATE]
    note: str = ""


def _id(x):
    return x


def _v2_to_v3(x):
    return F(x)


def _v3_to_pair(x):
    # value kept; channel starts dead (constant) — billed, not smuggled
    return (F(x), F(0))


def _pair_to_jet(x):
    v, r = x
    return (v, r, F(0))


def _pair_to_v3(x):
    v, r = x
    if r != 0:
        raise ChannelPreservationError("live r cannot enter scalar V3")
    if v not in (F(0), F(1, 2), F(1)):
        raise Theta(f"{v} not in V3")
    return v


MAPS = {
    ("V2", "V3"): Migration("V2", "V3", _v2_to_v3, F(1, 2), "embed bits in V3"),
    ("V3", "QPAIR"): Migration("V3", "QPAIR", _v3_to_pair, F(1), "open a dead channel"),
    ("QPAIR", "QJET2"): Migration("QPAIR", "QJET2", _pair_to_jet, F(1), "allocate r2"),
    ("QPAIR", "V3"): Migration("QPAIR", "V3", _pair_to_v3, F(2), "drop channel if dead"),
    ("V2", "V2"): Migration("V2", "V2", _id, F(0), "identity"),
    ("V3", "V3"): Migration("V3", "V3", _id, F(0), "identity"),
    ("QPAIR", "QPAIR"): Migration("QPAIR", "QPAIR", _id, F(0), "identity"),
}


def lookup(src: str, dst: str) -> Migration:
    m = MAPS.get((src, dst))
    if m is None:
        raise Theta(f"no migration {src} → {dst}")
    return m


# ── runtime ───────────────────────────────────────────────────────────
@dataclass
class Runtime:
    carrier: Carrier
    state: Any
    ledger: Ledger = field(default_factory=Ledger)

    def guard(self, ok: bool, note: str) -> bool:
        """θ-check. Costs even when it passes."""
        self.ledger.charge(GUARD, PRICE[GUARD], note)
        return ok

    def step(self, fn: Callable[[Any], Any], note: str = "step") -> Any:
        self.ledger.charge(STEP, PRICE[STEP], note)
        out = fn(self.state)
        if not self.carrier.contains(out):
            # do not silently grow V; caller must reconfigure
            raise Theta(f"step left {self.carrier.name}: {out}")
        self.state = out
        return out

    def reconfigure(self, dst: Carrier, reason: str) -> None:
        """V_src → V_dst only through registered μ. Guard + map both pay."""
        self.ledger.charge(RECONFIG, PRICE[RECONFIG], reason)
        mig = lookup(self.carrier.name, dst.name)
        allowed = self.guard(
            not (self.carrier.live_channel(self.state) and not dst.has_channel),
            f"channel-preserve {self.carrier.name}→{dst.name}",
        )
        if not allowed:
            raise ChannelPreservationError(
                f"live channel in {self.carrier.name} has no slot in {dst.name}"
            )
        self.ledger.charge(MIGRATE, mig.cost, mig.note)
        new = mig.fn(self.state)
        if not dst.contains(new):
            raise Theta(f"μ({self.state})={new} not in {dst.name}")
        self.carrier = dst
        self.state = new


def and_prod(a, b):
    return F(a) * F(b)


def main():
    print("MIGRATION + METAGENERATION")
    print("  guards and reconfiguration share the step ledger")
    print()

    # 1. product AND on V2 is stable; same op on V3 leaves V
    rt = Runtime(V2, F(1))
    rt.guard(V2.contains(rt.state), "state in V2")
    rt.step(lambda s: and_prod(s, F(1)), "AND-prod on V2")
    print(f"  after V2 step  state={rt.state}  ledger={rt.ledger.total}  "
          f"lines={[ln.kind for ln in rt.ledger.lines]}")

    # grow V because we want ½ in the alphabet
    rt.reconfigure(V3, "admit midpoint")
    print(f"  migrated V2→V3  state={rt.state}  ledger={rt.ledger.total}")

    # 2. AND-prod(½,½)=¼ leaves V3 — guard sees it, reconfigure to pairs? 
    #    ¼ is not a pair. This path REFUSES. Honest: enlarge V or change G.
    left = False
    try:
        rt.step(lambda s: and_prod(F(1, 2), F(1, 2)), "AND-prod ½∧½")
    except Theta as e:
        left = True
        print(f"  V3 product leaves V → Theta: {e}")
        rt.ledger.charge(GUARD, PRICE[GUARD], "caught leave-V")

    # 3. open a channel instead (different slot): V3 → QPAIR
    rt2 = Runtime(V3, F(1, 2), Ledger(theta=F(16)))
    rt2.reconfigure(QPAIR, "need a rate slot")
    print(f"  V3→QPAIR  state={rt2.state}  ledger={rt2.ledger.total}")

    # dropping a LIVE channel back to V3 must refuse
    live = Runtime(QPAIR, (F(1), F(3)))
    dropped = False
    try:
        live.reconfigure(V3, "try to collapse live r")
    except Theta as e:
        dropped = True
        print(f"  drop live channel → Theta: {e}")

    # dead channel may drop
    dead = Runtime(QPAIR, (F(1), F(0)), Ledger(theta=F(16)))
    dead.reconfigure(V3, "drop dead channel")
    print(f"  drop dead channel  state={dead.state}  ledger={dead.total if hasattr(dead,'total') else dead.ledger.total}")

    # 4. metageneration is not zero: compare a silent step vs guarded+reconfig
    silent = Runtime(V2, F(1))
    silent.step(lambda s: s)
    print(f"  silent one step     ledger={silent.ledger.total}")
    loud = Runtime(V2, F(1))
    loud.guard(True, "pre")
    loud.reconfigure(V3, "grow")
    loud.step(lambda s: s)
    print(f"  guard+reconfig+step ledger={loud.ledger.total}  "
          f"kinds={[ln.kind for ln in loud.ledger.lines]}")

    # 5. budget wall
    wall = False
    tight = Runtime(V2, F(1), Ledger(theta=F(2)))
    try:
        tight.guard(True, "g1")
        tight.reconfigure(V3, "will blow θ")
    except Decohered as e:
        wall = True
        print(f"  θ wall on reconfig → Decohered: {e}")

    ok = (
        left and dropped and wall
        and rt2.state == (F(1, 2), F(0))
        and dead.state == F(1)
        and loud.ledger.total > silent.ledger.total
        and GUARD in {ln.kind for ln in loud.ledger.lines}
        and RECONFIG in {ln.kind for ln in loud.ledger.lines}
        and MIGRATE in {ln.kind for ln in loud.ledger.lines}
    )
    print()
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
