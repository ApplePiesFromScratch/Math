"""worlds.py — how many logics a listed V actually holds.

Play first. The 350k figure is a hunch about one slice:
associative AND × associative OR × any unary NOT on V3
= |Assoc|² × 3³. We compute |Assoc|, then the slice, then
which of those worlds satisfy LEM / LNC / DeMorgan / idem.
Combinations that leave V are excluded by construction
(only maps V^k→V). 'Unstable when combined' here means
the *laws* fail, not that a new ghost value appears —
unless G smuggles an op that does not land in V.

V4/V5: |Bin| = n^(n²) is not iterable. We report the
capacity and census only the cheap slices (unary, comm
count = n^(n(n+1)/2), chain min/max, luk on the chain).

    python -m engineer.worlds
"""
from __future__ import annotations

from collections import Counter
from itertools import product

from engineer.census import (
    all_binary,
    all_unary,
    annihilator,
    apply_bin,
    apply_un,
    associative,
    commutative,
    identity,
    involution,
)


def collect_assoc(n):
    return [op for op in all_binary(n) if associative(op, n)]


def collect_invol(n):
    return [u for u in all_unary(n) if involution(u, n)]


def designated(n):
    return {n - 1}


def lem_ok(AND, OR, NOT, n):
    des = designated(n)
    return all(apply_bin(OR, n, v, apply_un(NOT, v)) in des for v in range(n))


def lnc_ok(AND, OR, NOT, n):
    return all(apply_bin(AND, n, v, apply_un(NOT, v)) == 0 for v in range(n))


def idem_and(AND, n):
    return all(apply_bin(AND, n, a, a) == a for a in range(n))


def demorgan(AND, OR, NOT, n):
    for a, b in product(range(n), repeat=2):
        left = apply_un(NOT, apply_bin(AND, n, a, b))
        right = apply_bin(OR, n, apply_un(NOT, a), apply_un(NOT, b))
        if left != right:
            return False
    return True


def classify_worlds(n, ands, ors, nots):
    """Every (AND,OR,NOT) from the lists. Signature = 4 bits."""
    tallies = Counter()
    examples = {}
    for AND, OR, NOT in product(ands, ors, nots):
        sig = (
            lem_ok(AND, OR, NOT, n),
            lnc_ok(AND, OR, NOT, n),
            idem_and(AND, n),
            demorgan(AND, OR, NOT, n),
        )
        tallies[sig] += 1
        examples.setdefault(sig, (AND, OR, NOT))
    return tallies, examples


def raw_capacity(n):
    unary = n ** n
    binary = n ** (n * n)
    comm = n ** (n * (n + 1) // 2)
    return {"n": n, "unary": unary, "binary": binary, "commutative_only": comm}


def chain_family(n):
    """The cheap known family on a chain: min, max, luk-and, luk-or."""
    # values 0..n-1 stand for k/(n-1)
    def vmin(a, b):
        return min(a, b)

    def vmax(a, b):
        return max(a, b)

    def luk_and(a, b):
        return max(0, a + b - (n - 1))

    def luk_or(a, b):
        return min(n - 1, a + b)

    def pack(fn):
        return tuple(fn(a, b) for a in range(n) for b in range(n))

    return {
        "min": pack(vmin),
        "max": pack(vmax),
        "luk_and": pack(luk_and),
        "luk_or": pack(luk_or),
    }


def product_leaves(n):
    """k/(n-1) * j/(n-1) lands in V iff the product of indices is a multiple."""
    # encode v = i/(n-1); product value = i*j/(n-1)². In V iff (n-1) | i*j
    # and the result index is i*j/(n-1).
    missing = []
    for i, j in product(range(n), repeat=2):
        num = i * j
        den = n - 1
        if den == 0:
            continue
        if num % den != 0:
            missing.append((i, j, num / den))
    return missing


def report():
    lines = ["WORLDS  capacity, then the slices we can finish"]
    for n in (2, 3, 4, 5):
        cap = raw_capacity(n)
        leaves = product_leaves(n)
        lines.append(
            f"  n={n}  unary={cap['unary']:,}  "
            f"binary={cap['binary']:,}  "
            f"comm-maps={cap['commutative_only']:,}  "
            f"product-cells-leaving={len(leaves)}"
        )

    lines.append("")
    lines.append("  V3 slice (computed, not guessed)")
    assoc3 = collect_assoc(3)
    invol3 = collect_invol(3)
    un3 = 3 ** 3
    slice_all_not = len(assoc3) * len(assoc3) * un3
    slice_invol = len(assoc3) * len(assoc3) * len(invol3)
    lines.append(f"  |Assoc(V3)|            {len(assoc3)}")
    lines.append(f"  |Invol(V3)|            {len(invol3)}")
    lines.append(f"  Assoc×Assoc×any NOT    {slice_all_not:,}   "
                 f"({len(assoc3)}²×{un3})")
    lines.append(f"  Assoc×Assoc×Invol      {slice_invol:,}")

    # law table on the involutive slice (15k-ish — finishes)
    tallies, _ = classify_worlds(3, assoc3, assoc3, invol3)
    lines.append("  law signatures on Assoc×Assoc×Invol  "
                 "(LEM, LNC, AND-idem, DeMorgan)")
    for sig, c in sorted(tallies.items(), key=lambda kv: -kv[1]):
        bits = "".join("Y" if b else "n" for b in sig)
        lines.append(f"    {bits}   {c:,}")

    # chain family on n=2..5 always closes
    lines.append("")
    lines.append("  chain family (min,max,luk) closes for every listed n")
    for n in (2, 3, 4, 5):
        fam = chain_family(n)
        ands = [fam["min"], fam["luk_and"]]
        ors = [fam["max"], fam["luk_or"]]
        nots = [tuple((n - 1) - a for a in range(n))]
        t, _ = classify_worlds(n, ands, ors, nots)
        lines.append(f"    n={n}  2×2×1 chain worlds, signatures {dict(t)}")

    lines.append("")
    lines.append("  interpolation: V3 Assoc×Assoc×Invol worlds that are")
    lines.append("  not the museum pair (min+max+NOT, luk+luk+NOT) still exist.")
    lines.append("  those extra signatures are generated logics.")
    lines.append("  V4 binary 4^16 = 4,294,967,296 — do not enumerate.")
    lines.append("  constrain G (assoc / monotone / chain family) or you")
    lines.append("  hired ∞ as a loop.")
    return lines, {
        "assoc3": len(assoc3),
        "slice": slice_all_not,
        "invol_slice": slice_invol,
        "signatures": len(tallies),
    }


def main():
    lines, meta = report()
    print("\n".join(lines))
    print()
    ok = meta["assoc3"] == 113 and meta["slice"] == 113 * 113 * 27
    print(f"  hunch 350k vs computed Assoc×Assoc×NOT = {meta['slice']:,}")
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
