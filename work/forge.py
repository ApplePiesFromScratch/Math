"""forge.py — generate a presentation, map a foreign one.

The model is not the Q-pair replica. The model is:

    stipulated V + declared G + finite θ  →  forced laws and failures

A new cut is forged by naming the knobs and running the enumerator.
A foreign system is mapped by the same enumerator. That is generation
and cartography. It is not a pencil.

    python -m pl.forge
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product


class Theta(Exception):
    pass


# ── G library (each op is a cut, not an essence) ──────────────────────
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


OPS = {
    "NOT": (1, NOT),
    "AND_min": (2, AND_min),
    "AND_prod": (2, AND_prod),
    "AND_luk": (2, AND_luk),
    "OR_max": (2, OR_max),
    "OR_luk": (2, OR_luk),
}


def parse_V(spec):
    """'0,1' or '0,1/2,1' → tuple of F."""
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "/" in part:
            n, d = part.split("/")
            out.append(F(int(n), int(d)))
        else:
            out.append(F(part))
    return tuple(out)


def closes(V, op):
    arity, fn = op
    for args in product(V, repeat=arity):
        try:
            r = fn(*args)
        except Exception:
            return False, args, "raised"
        if r not in V:
            return False, args, r
    return True, None, None


def lem_holds(V, op_or, op_not, designated):
    _, OR = op_or
    _, nfn = op_not
    for v in V:
        if OR(v, nfn(v)) not in designated:
            return False, v
    return True, None


def lnc_value(V, op_and, op_not):
    _, AND = op_and
    _, nfn = op_not
    for v in V:
        if AND(v, nfn(v)) != F(0):
            return False, v
    return True, None


def idem_and(V, op_and):
    _, AND = op_and
    for v in V:
        if AND(v, v) != v:
            return False, v
    return True, None


class Forge:
    """A generated presentation. Knobs in, receipts out."""

    def __init__(self, name, V_spec, g_names, designated="1"):
        self.name = name
        self.V = parse_V(V_spec)
        self.g_names = list(g_names)
        self.ops = {n: OPS[n] for n in g_names}
        self.designated = tuple(parse_V(designated))
        self.lines = []

    def run(self):
        self.lines = []
        # close-tests
        for n, op in self.ops.items():
            ok, args, got = closes(self.V, op)
            if ok:
                self.lines.append(("FORCED-on-cut", f"{n} closes on V"))
            else:
                self.lines.append(("REFUSE", f"{n} leaves V at {args} → {got}"))
        # law probes if the needed ops exist
        if "NOT" in self.ops:
            or_name = next((n for n in self.g_names if n.startswith("OR_")), None)
            and_name = next((n for n in self.g_names if n.startswith("AND_")), None)
            if or_name:
                ok, w = lem_holds(self.V, self.ops[or_name], self.ops["NOT"], self.designated)
                self.lines.append(
                    ("FORCED-on-cut", "LEM") if ok else ("REFUSE", f"LEM fails at {w}")
                )
            if and_name:
                ok, w = lnc_value(self.V, self.ops[and_name], self.ops["NOT"])
                self.lines.append(
                    ("FORCED-on-cut", "LNC-value") if ok else ("REFUSE", f"LNC-value fails at {w}")
                )
                ok, w = idem_and(self.V, self.ops[and_name])
                self.lines.append(
                    ("FORCED-on-cut", "AND-idempotent") if ok else ("REFUSE", f"AND-idempotent fails at {w}")
                )
        return self

    def report(self) -> str:
        rows = [f"{self.name}  V={list(map(str, self.V))}  G={self.g_names}  "
                f"θ designated={list(map(str, self.designated))}"]
        for tier, msg in self.lines:
            rows.append(f"  [{tier:<13}] {msg}")
        return "\n".join(rows)


def map_foreign(name, V_spec, g_names, designated="1"):
    """Same forger, pointed at someone else's knobs."""
    return Forge(name, V_spec, g_names, designated).run()


def main():
    print("FORGE  generate presentations / map foreign ones")
    print("  the model is the knobs. a replica is one setting.")
    print()

    # historical maps
    cl2 = Forge("CL2", "0,1", ["NOT", "AND_min", "OR_max"]).run()
    l3 = Forge("L3", "0,1/2,1", ["NOT", "AND_luk", "OR_luk"]).run()
    k3 = Forge("K3", "0,1/2,1", ["NOT", "AND_min", "OR_max"]).run()
    prod3 = Forge("PROD3", "0,1/2,1", ["NOT", "AND_prod", "OR_max"]).run()
    # novel: min-AND on four values (not a museum piece)
    v4 = Forge("V4-min", "0,1/3,2/3,1", ["NOT", "AND_min", "OR_max"]).run()

    for f in (cl2, l3, k3, prod3, v4):
        print(f.report())
        print()

    # smash the toy wave-off: one forger, five cuts, including one
    # that was not in the history books
    novel_ok = any("closes" in m for t, m in v4.lines if t == "FORCED-on-cut")
    split = (
        any("LEM" == m and t == "FORCED-on-cut" for t, m in l3.lines)
        and any("LEM fails" in m for t, m in k3.lines)
    )
    prod_leaves = any("AND_prod leaves" in m for t, m in prod3.lines)
    print("generative: V4-min was not an inherited logic. knobs in, table out.")
    print(f"  L3/K3 split on LEM: {split}")
    print(f"  PROD3 product leaves V: {prod_leaves}")
    print(f"  novel V4-min closes its G: {novel_ok}")
    print()
    print("verdict", "PASS" if split and prod_leaves and novel_ok else "FAIL")
    return 0 if (split and prod_leaves and novel_ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
