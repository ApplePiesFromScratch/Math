"""Cost of pretending V is infinite.

Finite V: |V|^k evaluations, done.
Unlistable V: the same loop does not terminate. That is not 'more
accurate'. It is an unpaid quantifier. Putting ∞ in V as a point
does not finish the loop; it adds a row you then have to define G on.
"""
from __future__ import annotations

from time import perf_counter

from engineer.enum import closes
from engineer.ops import AND_prod, parse_V


def finite_cost(n_values: int, arity=2) -> dict:
    V = tuple(range(n_values))  # stand-in alphabet of size n

    def add(a, b):
        return (a + b) % n_values  # closes by construction

    t0 = perf_counter()
    pairs = n_values ** arity
    ok = True
    for a in V:
        for b in V:
            if add(a, b) not in V:
                ok = False
    ms = (perf_counter() - t0) * 1000
    return {"n": n_values, "pairs": pairs, "ms": ms, "closes": ok}


def report():
    lines = ["INFINITY COST",
             "  finite V: count the pairs. unlistable V: the count has no last pair."]
    for n in (2, 3, 10, 50, 200):
        r = finite_cost(n)
        lines.append(f"  |V|={n:<4} pairs={r['pairs']:<8} {r['ms']:.3f} ms  closes={r['closes']}")
    lines.append("  |V|=ℝ        pairs=unlistable     loop has no last step")
    lines.append("  |V|=ℝ∪{∞}    still unlistable     plus a new row for every op at ∞")
    # product on a grown finite V that product leaves
    V3 = parse_V("0,1/2,1")
    leaves = not closes(V3, (2, AND_prod))
    lines.append(f"  AND_prod on V3 leaves V: {leaves}  (¼ is the ghost people promote to a new point)")
    lines.append("  engineer move: fire θ or register μ into a V that holds ¼")
    lines.append("  technician move: say 'in the reals it works' — unpaid lift")
    return "\n".join(lines)
