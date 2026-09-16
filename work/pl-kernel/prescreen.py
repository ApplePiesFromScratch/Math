"""prescreen.py — is a theorem even stable on the carrier that asked for it?

Does not prove. Does not reject a theorem of mathematics. It answers:

  are the values the statement names in V?
  are the ops it calls in G, and do they close?
  are the hypotheses θ-legal?
  does the quantifier fit the alphabet we can hold?

Verdicts:
  ADMIT     run the close-test; the statement is well-typed here
  DEFER     symbols fit, but the quantifier outruns the listed V
  REFUSE    a value or op the carrier cannot hold, or θ already fires
            on the hypotheses

    python -m pl.prescreen
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as F
from itertools import product
from typing import Callable


# ── carrier ───────────────────────────────────────────────────────────
@dataclass
class Carrier:
    name: str
    V: tuple
    ops: dict                      # name -> callable
    theta: Callable                # (op_name, *args) -> str|None  reason to refuse
    designated: tuple = ()
    notes: str = ""

    def has_op(self, name: str) -> bool:
        return name in self.ops

    def in_V(self, x) -> bool:
        return x in self.V

    def closes(self, op_name: str):
        op = self.ops[op_name]
        n = 0
        for args in product(self.V, repeat=_arity(op)):
            n += 1
            if self.theta(op_name, *args):
                continue
            try:
                r = op(*args)
            except Exception as e:
                return False, n, f"{op_name}{args} raised {e}"
            if r not in self.V:
                return False, n, f"{op_name}{args}={r} not in V"
        return True, n, ""


def _arity(fn):
    return fn.__code__.co_argcount


# ── theorem request ───────────────────────────────────────────────────
@dataclass
class Request:
    name: str
    ops: tuple                     # op names the statement uses
    quantifier: str                # "all V" | "all R" | "grid" | "point"
    on_values: tuple | None = None # extra constants the statement names
    needs_designated: bool = False
    check: Callable | None = None  # optional: Carrier -> (held, n, note)
    note: str = ""


@dataclass
class Screen:
    theorem: str
    carrier: str
    verdict: str                   # ADMIT / DEFER / REFUSE
    reasons: list = field(default_factory=list)
    close_note: str = ""


# ── screen ────────────────────────────────────────────────────────────
def prescreen(req: Request, car: Carrier) -> Screen:
    reasons = []

    # 1. every named constant in V
    if req.on_values:
        missing = [x for x in req.on_values if not car.in_V(x)]
        if missing:
            return Screen(req.name, car.name, "REFUSE",
                          [f"values not in V: {missing}"])

    # 2. every named op exists
    missing_ops = [o for o in req.ops if not car.has_op(o)]
    if missing_ops:
        return Screen(req.name, car.name, "REFUSE",
                      [f"ops not in G: {missing_ops}"])

    # 2b. named point values must be θ-legal for those ops
    if req.on_values:
        for o in req.ops:
            # unary: θ(op, v). binary: try v as last arg (denominator / isolation)
            reasons_th = []
            ar = _arity(car.ops[o])
            if ar == 1:
                why = car.theta(o, *req.on_values[:1])
                if why:
                    reasons_th.append(f"θ {o}({req.on_values[0]}): {why}")
            elif ar == 2 and len(req.on_values) >= 1:
                why = car.theta(o, F(1), req.on_values[0])
                if why:
                    reasons_th.append(f"θ {o}(..., {req.on_values[0]}): {why}")
            if reasons_th:
                return Screen(req.name, car.name, "REFUSE", reasons_th)

    # 3. quantifier vs alphabet — before close-tests on a tiny listed V
    if req.quantifier == "all R":
        return Screen(req.name, car.name, "DEFER",
                      ["quantifier ranges over unlistable V; "
                       "finite close-test would be FORCED-on-cut only"])
    if req.quantifier == "all V" and len(car.V) == 0:
        return Screen(req.name, car.name, "DEFER",
                      ["V is not a listed alphabet"])

    # 4. every named op closes on this V (θ-legal inputs only)
    for o in req.ops:
        ok, n, why = car.closes(o)
        if not ok:
            return Screen(req.name, car.name, "REFUSE",
                          [f"{o} does not close on {car.name}: {why}"])

    # 4. designation required?
    if req.needs_designated and not car.designated:
        return Screen(req.name, car.name, "REFUSE",
                      ["statement uses designation; this carrier has none"])

    # 6. optional executable probe of the conclusion on this V
    close_note = ""
    if req.check:
        held, n, close_note = req.check(car)
        if not held:
            return Screen(req.name, car.name, "REFUSE",
                          [f"conclusion fails on this V: {close_note}"],
                          close_note)

    return Screen(req.name, car.name, "ADMIT",
                  ["values in V, ops close, θ does not fire on the "
                   "hypotheses, quantifier fits the listed alphabet"],
                  close_note)


# ── example carriers ──────────────────────────────────────────────────
def _not(v):
    return F(1) - v


def _min(a, b):
    return min(a, b)


def _max(a, b):
    return max(a, b)


def _prod(a, b):
    return a * b


def _luk(a, b):
    return max(F(0), a + b - F(1))


def _theta_never(op, *args):
    return None


V2 = (F(0), F(1))
V3 = (F(0), F(1, 2), F(1))

CL2 = Carrier("CL2", V2,
              {"NOT": _not, "AND": _min, "OR": _max},
              _theta_never, designated=(F(1),))

K3 = Carrier("K3", V3,
             {"NOT": _not, "AND": _min, "OR": _max},
             _theta_never, designated=(F(1),))

L3 = Carrier("L3", V3,
             {"NOT": _not, "AND": _luk, "OR": lambda a, b: min(F(1), a + b)},
             _theta_never, designated=(F(1),))

PROD3 = Carrier("PROD3", V3,
                {"NOT": _not, "AND": _prod, "OR": _max},
                _theta_never, designated=(F(1),),
                notes="product AND on a 3-valued alphabet")


# process-calc-shaped: values are Q-pairs encoded as (v,r) on a tiny grid
# For prescreen demo we only need "is 1/2 in V?" style checks on Q-grid.
QGRID = tuple(F(n) for n in range(-3, 4))


def _rate(a, b):
    # treat as scalars here: rate of two numbers is a/b if b!=0
    return a / b


def _theta_rate(op, *args):
    if op == "rate" and args[-1] == 0:
        return "dead isolation"
    if op == "quot" and args[-1] == 0:
        return "pole"
    return None


def _quot(a, b):
    return a / b


PROC = Carrier("PROC-Q-grid", QGRID,
               {"rate": _rate, "quot": _quot, "plus": lambda a, b: a + b,
                "mix": lambda a, b: a * b},
               _theta_rate, designated=(),
               notes="scalar shadow of process calc on a Q grid")


# ── example theorems ──────────────────────────────────────────────────
def _lem(car: Carrier):
    n = 0
    for a in car.V:
        n += 1
        if car.ops["OR"](a, car.ops["NOT"](a)) not in car.designated:
            return False, n, f"OR({a},NOT({a})) not designated"
    return True, n, "LEM holds on all of V"


def _lnc_value(car: Carrier):
    """Value-reading LNC: AND(a,NOT a) == 0."""
    n = 0
    for a in car.V:
        n += 1
        if car.ops["AND"](a, car.ops["NOT"](a)) != F(0):
            return False, n, f"AND({a},NOT({a})) != 0"
    return True, n, "AND(a,¬a)=0 on all of V"


def _and_idem(car: Carrier):
    n = 0
    for a in car.V:
        n += 1
        if car.ops["AND"](a, a) != a:
            return False, n, f"AND({a},{a}) != {a}"
    return True, n, "AND idempotent on V"


THEOREMS = [
    Request("LEM", ("OR", "NOT"), "all V",
            needs_designated=True, check=_lem,
            note="every value or its negation is designated"),
    Request("LNC-value", ("AND", "NOT"), "all V",
            check=_lnc_value,
            note="AND(a,¬a) is the zero of V"),
    Request("AND-idempotent", ("AND",), "all V",
            check=_and_idem),
    Request("1/x at 0", ("quot",), "point",
            on_values=(F(0),),
            note="continuity / definedness at zero"),
    Request("mean value on R", ("rate",), "all R",
            note="exists c in (a,b) with f'(c)=avg"),
    Request("AND is multiplication", ("AND",), "all V",
            note="silent identification with product"),
]


CARRIERS = [CL2, K3, L3, PROD3, PROC]


def run_matrix():
    print("THEOREM PRE-SCREEN")
    print("ADMIT  = well-typed on this carrier; safe to run a close-test")
    print("DEFER  = typed, but the quantifier outruns listed V")
    print("REFUSE = a value/op/θ the carrier cannot hold")
    print()
    print(f"  {'theorem':<24} {'carrier':<14} {'verdict':<8} reason")
    rows = []
    for th in THEOREMS:
        for car in CARRIERS:
            # skip theorems whose ops the carrier lacks without noise
            s = prescreen(th, car)
            rows.append(s)
            reason = s.reasons[0] if s.reasons else ""
            if len(reason) > 62:
                reason = reason[:59] + "..."
            print(f"  {th.name:<24} {car.name:<14} {s.verdict:<8} {reason}")
    print()
    n = {"ADMIT": 0, "DEFER": 0, "REFUSE": 0}
    for r in rows:
        n[r.verdict] += 1
    print(f"  {n['ADMIT']} ADMIT  {n['DEFER']} DEFER  {n['REFUSE']} REFUSE")
    return rows


def main():
    rows = run_matrix()
    # sanity: LEM on CL2 admits and holds; LEM on K3 refuses conclusion
    lem_cl2 = next(r for r in rows if r.theorem == "LEM" and r.carrier == "CL2")
    lem_k3 = next(r for r in rows if r.theorem == "LEM" and r.carrier == "K3")
    prod = next(r for r in rows
                if r.theorem == "AND is multiplication" and r.carrier == "PROD3")
    at0 = next(r for r in rows
               if r.theorem == "1/x at 0" and r.carrier == "PROC-Q-grid")
    mvt = next(r for r in rows
               if r.theorem == "mean value on R" and r.carrier == "PROC-Q-grid")
    ok = (
        lem_cl2.verdict == "ADMIT"
        and lem_k3.verdict == "REFUSE"
        and prod.verdict == "REFUSE"
        and at0.verdict == "REFUSE"   # 0 is in V but θ fires on quot
        and mvt.verdict == "DEFER"
    )
    print()
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
