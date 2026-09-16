"""census.py — every closing op on a listed V, counted.

Not a sample. The whole set of functions V×V→V and V→V.
On V2 there are 16 binary maps. On V3 there are 3^9 = 19683.
The technician inherits two of them and calls them AND and OR.
The engineer counts.

    python -m engineer.census
"""
from __future__ import annotations

from itertools import product


def elems(n):
    return tuple(range(n))


def all_binary(n):
    """Each op is a tuple of n*n results, row-major."""
    V = elems(n)
    cells = n * n
    for raw in product(V, repeat=cells):
        yield raw


def all_unary(n):
    V = elems(n)
    for raw in product(V, repeat=n):
        yield raw


def apply_bin(op, n, a, b):
    return op[a * n + b]


def apply_un(op, a):
    return op[a]


def commutative(op, n):
    return all(apply_bin(op, n, a, b) == apply_bin(op, n, b, a)
               for a, b in product(range(n), repeat=2))


def associative(op, n):
    return all(
        apply_bin(op, n, apply_bin(op, n, a, b), c)
        == apply_bin(op, n, a, apply_bin(op, n, b, c))
        for a, b, c in product(range(n), repeat=3)
    )


def idempotent(op, n):
    return all(apply_bin(op, n, a, a) == a for a in range(n))


def identity(op, n, e):
    return all(apply_bin(op, n, e, a) == a and apply_bin(op, n, a, e) == a
               for a in range(n))


def annihilator(op, n, z):
    return all(apply_bin(op, n, z, a) == z and apply_bin(op, n, a, z) == z
               for a in range(n))


def involution(u, n):
    return all(apply_un(u, apply_un(u, a)) == a for a in range(n))


def fixed_points(u, n):
    return [a for a in range(n) if apply_un(u, a) == a]


def monotone_bin(op, n):
    """a<=a' and b<=b' ⇒ op(a,b)<=op(a',b') with the chain order 0<1<…"""
    for a, b, ap, bp in product(range(n), repeat=4):
        if a <= ap and b <= bp:
            if apply_bin(op, n, a, b) > apply_bin(op, n, ap, bp):
                return False
    return True


def census_binary(n):
    total = 0
    comm = assoc = both = idem = 0
    monoids_top = 0   # identity = n-1 (the '1')
    and_like = 0      # comm, assoc, id=1, ann=0, idem
    for op in all_binary(n):
        total += 1
        c = commutative(op, n)
        a = associative(op, n)
        i = idempotent(op, n)
        comm += c
        assoc += a
        both += c and a
        idem += i
        if identity(op, n, n - 1):
            monoids_top += a and c
        if (c and a and i and identity(op, n, n - 1)
                and annihilator(op, n, 0)):
            and_like += 1
    return {
        "n": n,
        "binary_maps": total,
        "commutative": comm,
        "associative": assoc,
        "semigroups_comm": both,
        "idempotent": idem,
        "comm_monoids_id1": monoids_top,
        "and_like": and_like,
    }


def census_unary(n):
    total = 0
    invol = 0
    invol_no_fix = 0
    invol_mid_fix = 0
    for u in all_unary(n):
        total += 1
        if involution(u, n):
            invol += 1
            fp = fixed_points(u, n)
            if not fp:
                invol_no_fix += 1
            if n == 3 and fp == [1]:
                invol_mid_fix += 1
    return {
        "n": n,
        "unary_maps": total,
        "involutions": invol,
        "involutions_no_fix": invol_no_fix,
        "involutions_only_mid_fix": invol_mid_fix,
    }


def v2_and_prod_same():
    """min and product as functions on {0,1}."""
    # encode 0,1
    mn = tuple(min(a, b) for a in range(2) for b in range(2))
    pr = tuple(a * b for a in range(2) for b in range(2))
    return mn == pr, mn, pr


def report():
    lines = ["CENSUS  every map V^k → V on a listed alphabet"]
    u2 = census_unary(2)
    b2 = census_binary(2)
    u3 = census_unary(3)
    b3 = census_binary(3)
    same, mn, pr = v2_and_prod_same()
    lines.append(f"  V2 unary maps          {u2['unary_maps']:>7}   "
                 f"involutions {u2['involutions']}  "
                 f"no fixed point {u2['involutions_no_fix']}")
    lines.append(f"  V2 binary maps         {b2['binary_maps']:>7}   "
                 f"comm {b2['commutative']}  assoc {b2['associative']}  "
                 f"comm-semigroups {b2['semigroups_comm']}")
    lines.append(f"  V2 AND-like            {b2['and_like']:>7}   "
                 f"(comm, assoc, idem, id=1, ann=0)")
    lines.append(f"  min == product on V2   {same}   tables {mn} {pr}")
    lines.append(f"  V3 unary maps          {u3['unary_maps']:>7}   "
                 f"involutions {u3['involutions']}  "
                 f"no-fix {u3['involutions_no_fix']}  "
                 f"only-mid-fix {u3['involutions_only_mid_fix']}")
    lines.append(f"  V3 binary maps         {b3['binary_maps']:>7}   "
                 f"comm {b3['commutative']}  assoc {b3['associative']}  "
                 f"comm-semigroups {b3['semigroups_comm']}")
    lines.append(f"  V3 AND-like            {b3['and_like']:>7}")
    lines.append("  the museum handed you two of those AND-likes and a story.")
    lines.append("  the engineer has the rest of the table.")
    return lines, {"u2": u2, "b2": b2, "u3": u3, "b3": b3, "min_eq_prod": same}


def main():
    lines, data = report()
    print("\n".join(lines))
    ok = (
        data["b2"]["binary_maps"] == 16
        and data["b3"]["binary_maps"] == 19683
        and data["min_eq_prod"]
        and data["b2"]["and_like"] >= 1
        and data["u2"]["involutions_no_fix"] == 1  # classical NOT
    )
    print()
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
