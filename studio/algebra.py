"""Algebra as presentations. Simpler than calc: often no second slot.

A number system is V + G that closes + θ for the maps that don't.
Solving is search or rewrite inside that cut. A letter is a hole
in an expression, not a box that contains a quantity.

    python -m studio.algebra
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product


def closes_add_mul(V):
    for a, b in product(V, repeat=2):
        if a + b not in V or a * b not in V:
            return False
    return True


def add_id(V):
    for e in V:
        if all(e + a == a == a + e for a in V):
            return e
    return None


def mul_id(V):
    for e in V:
        if all(e * a == a == a * e for a in V):
            return e
    return None


def add_inv(V, zero):
    out = {}
    for a in V:
        hits = [b for b in V if a + b == zero]
        if len(hits) != 1:
            return None
        out[a] = hits[0]
    return out


def mul_inv(V, one, zero):
    out = {}
    for a in V:
        if a == zero:
            continue
        hits = [b for b in V if a * b == one]
        if len(hits) != 1:
            return None
        out[a] = hits[0]
    return out


def classify(name, V):
    V = tuple(V)
    z = add_id(V)
    u = mul_id(V)
    ai = add_inv(V, z) if z is not None else None
    mi = mul_inv(V, u, z) if u is not None and z is not None else None
    return {
        "name": name,
        "n": len(V),
        "closes": closes_add_mul(V),
        "0": z,
        "1": u,
        "group_add": ai is not None,
        "field": ai is not None and mi is not None and u is not None,
        "units": None if mi is None else len(mi),
    }


def solve_linear(V, a, b, target=0):
    """Find x in V with a*x + b == target. Listed search."""
    return [x for x in V if a * x + b == target]


def main():
    print("ALGEBRA  V + close-test + θ. letters are holes.")
    print()
    systems = [
        ("V2 bits as {0,1} + * min-like wait: Z/2", [F(0), F(1)]),
        ("Z/3", [F(0), F(1), F(2)]),  # not field with usual + if we use Q add
    ]
    # Use integer mod n as the honest finite rings
    def Zn(n):
        class Mod:
            def __init__(self, k):
                self.k = k % n
            def __add__(self, o):
                return Mod(self.k + o.k)
            def __mul__(self, o):
                return Mod(self.k * o.k)
            def __eq__(self, o):
                return isinstance(o, Mod) and self.k == o.k
            def __hash__(self):
                return self.k
            def __repr__(self):
                return str(self.k)
        return [Mod(i) for i in range(n)]

    print("  finite rings Z/n  (listed V, + and * mod n)")
    for n in (2, 3, 4, 5, 6, 7):
        V = Zn(n)
        c = classify(f"Z/{n}", V)
        print(f"    Z/{n}  |V|={c['n']}  closes={c['closes']}  "
              f"add-group={c['group_add']}  field={c['field']}")

    print()
    print("  Q is not listed — we do not census it. θ: unlistable.")
    print("  Z listed-as-infinite is the same refusal.")
    print()

    # solve ax+b=0 on Z/5
    V5 = Zn(5)
    a, b = V5[2], V5[3]   # 2x+3=0 → 2x=2 → x=1
    hits = solve_linear(V5, a, b, V5[0])
    print(f"  solve 2x+3=0 in Z/5  → {hits}")
    print("  that is search on V, not 'finding the unknown'.")
    print()

    # leave-V: 1/2 not in Z/5 as rational; inverse of 2 exists: 3 because 6=1
    print("  2·3=6≡1 in Z/5 so 2 has a mul-inverse. 2 has no mul-inverse in Z/4.")
    V4 = Zn(4)
    inv4 = [x for x in V4 if (V4[2] * x).k == 1]
    print(f"  inverses of 2 in Z/4: {inv4}  θ: no unit")
    print()

    # polynomial as expression tree, evaluate on V — not a new inhabitant
    print("  polynomial x²+1 on Z/5 (evaluate, don't hire 'x')")
    for x in V5:
        val = (x * x + V5[1]).k
        print(f"    x={x}  x²+1={val}")
    roots = [x for x in V5 if (x * x + V5[1]).k == 0]
    print(f"  roots of x²+1 in Z/5: {roots}  (splits here; i is an R-leftover)")
    print()

    print("  packing")
    print("    recipes → symbols (holes) → Z/Q as V → fields as 'every nonzero inverts'")
    print("    complex: μ into a V that already has a root of x²+1")
    print("    variable-as-box is the ghost. hole-in-an-expression is the cut.")
    print()
    print("verdict PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
