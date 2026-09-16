"""calccensus.py — combinatorics of calculus presentations.

A calculus world is not 'the derivative'. It is

    V_kind × isolate × mix × extract × θ

We run every cheap world on a listed grid of polynomials and
points. Worlds that agree on V2-sized grids can still split
when V grows (higher jet, another seed, a pole).

Unlistable: all maps R→R, all h→0 sequences. Those are ∞.
Listed: Q-pairs, 2-jets, seeds in a finite set, h in a finite set.

    python -m engineer.calccensus
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product


# ── tiny AD on two V's ───────────────────────────────────────────────
def pair(v, r):
    return (F(v), F(r))


def jet(v, r, r2):
    return (F(v), F(r), F(r2))


def add_p(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul_p(a, b):
    return (a[0] * b[0], a[1] * b[0] + a[0] * b[1])


def add_j(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul_j(a, b):
    # (fg)'' = f''g + 2f'g' + fg''
    return (
        a[0] * b[0],
        a[1] * b[0] + a[0] * b[1],
        a[2] * b[0] + 2 * a[1] * b[1] + a[0] * b[2],
    )


def pow_p(x, n):
    out = pair(1, 0)
    for _ in range(n):
        out = mul_p(out, x)
    return out


def pow_j(x, n):
    out = jet(1, 0, 0)
    for _ in range(n):
        out = mul_j(out, x)
    return out


# ── extracts ─────────────────────────────────────────────────────────
def extract_rate(p, g):
    if g[1] == 0:
        raise ValueError("dead")
    return p[1] / g[1]


def extract_unary(p, g):
    # lock: pretend g.r was 1; report p.r scaled as if seed 1
    # technician D: just take p.r (seed already baked in)
    return p[1]


def extract_fd(fn_val, x, h):
    return (fn_val(x + h) - fn_val(x)) / h


# ── grid ─────────────────────────────────────────────────────────────
POINTS = [F(2), F(3), F(-1), F(4)]
SEEDS = [F(1), F(2), F(1, 2), F(-3)]
HS = [F(1), F(1, 2), F(1, 8), F(1, 64)]
POLYS = {
    "x2": lambda n: n,
    "x3": lambda n: n,  # degree tag
}


def poly_val(degree, x):
    return x ** degree


def poly_d1(degree, x):
    return F(degree) * (x ** (degree - 1))


def poly_d2(degree, x):
    if degree < 2:
        return F(0)
    return F(degree) * F(degree - 1) * (x ** (degree - 2))


def report():
    lines = ["CALC CENSUS  presentations of 'the derivative'"]
    lines.append("")

    # 1. capacity of the *settings*, not of maps R→R
    lines.append("  setting space (listed knobs)")
    v_kinds = ("pair", "jet2", "scalar+fd")
    isolates = ("seed-arg", "seed-locked-1")
    mixes = ("leibniz",)
    extracts = ("rate", "unary-r", "fd-h")
    worlds = list(product(v_kinds, isolates, mixes, extracts))
    lines.append(f"  V_kind {len(v_kinds)} × isolate {len(isolates)} × "
                 f"mix {len(mixes)} × extract {len(extracts)} = "
                 f"{len(worlds)} named worlds")
    lines.append("  (mix stays Leibniz; other mixes are a later knob)")

    # 2. rate vs unary vs fd on the polynomial grid
    lines.append("")
    lines.append("  agreement on degree 2,3 at listed points/seeds/h")
    rate_ok = unary_gauge = fd_exact = 0
    rate_n = unary_n = fd_n = 0
    splits = []

    for deg in (2, 3):
        for x0 in POINTS:
            want = poly_d1(deg, x0)
            for k in SEEDS:
                rate_n += 1
                p = pow_p(pair(x0, k), deg)
                g = pair(x0, k)
                got = extract_rate(p, g)
                if got == want:
                    rate_ok += 1
                else:
                    splits.append(("rate", deg, x0, k, got, want))
                unary_n += 1
                u = extract_unary(p, g)
                # unary equals want only when seed=1
                if u == want:
                    unary_gauge += 1
            for h in HS:
                fd_n += 1
                got = extract_fd(lambda t, d=deg: poly_val(d, t), x0, h)
                if got == want:
                    fd_exact += 1

    lines.append(f"  rate  == d1          {rate_ok}/{rate_n}")
    lines.append(f"  unary-r == d1        {unary_gauge}/{unary_n}   "
                 f"(only the seed-1 slice)")
    lines.append(f"  fd(h) == d1          {fd_exact}/{fd_n}   "
                 f"(0 on this grid — leftover is a power of h)")

    # 3. jet second channel vs fd of fd
    lines.append("")
    lines.append("  second channel")
    jet_ok = fd2_ok = 0
    jet_n = fd2_n = 0
    for deg in (2, 3):
        for x0 in POINTS:
            want2 = poly_d2(deg, x0)
            jet_n += 1
            j = pow_j(jet(x0, 1, 0), deg)
            if j[2] == want2:
                jet_ok += 1
            for h in HS:
                fd2_n += 1
                # fd of fd: ([f(x+h)-f(x)]/h - [f(x)-f(x-h)]/h)/h
                f = lambda t, d=deg: poly_val(d, t)
                mid = (f(x0 + h) - f(x0 - h)) / (2 * h)
                # second: (f(x+h) - 2f(x) + f(x-h))/h²
                got2 = (f(x0 + h) - 2 * f(x0) + f(x0 - h)) / (h * h)
                if got2 == want2:
                    fd2_ok += 1
    lines.append(f"  jet r2 == d2         {jet_ok}/{jet_n}")
    lines.append(f"  stencil d2 == d2     {fd2_ok}/{fd2_n}")

    # 4. chain cancellation vs stacked unary
    lines.append("")
    lines.append("  chain")
    # y = x^2, q = y^3 = x^6 at 2; d1 = 6 x^5 = 192
    x = pair(2, 1)
    y = pow_p(x, 2)
    q = pow_p(y, 3)  # wrong — pow_p(y,3) is y as base with y's channel
    # q as function of x: (x^2)^3 = x^6
    q_on_x = pow_p(x, 6)
    want_qx = poly_d1(6, F(2))
    r_qx = extract_rate(q_on_x, x)
    r_qy = extract_rate(q, y)
    r_yx = extract_rate(y, x)
    cancel = r_qy * r_yx
    lines.append(f"  rate(x^6, x) at 2              {r_qx}  want {want_qx}")
    lines.append(f"  rate(y^3,y)*rate(y,x)          {cancel}")
    lines.append(f"  cancellation holds             {cancel == r_qx}")
    # unary stacked without rescaling
    u_q = q[1]
    u_y = y[1]
    lines.append(f"  unary stacked q.r * y.r        {u_q * u_y}  "
                 f"(not a rate; seed baked twice)")

    # 5. pole
    lines.append("")
    lines.append("  pole")
    try:
        extract_rate(pair(1, 0), pair(0, 0))
        dead = False
    except ValueError:
        dead = True
    live00 = extract_rate(pair(0, 6), pair(0, 1))
    lines.append(f"  rate through r=0               θ={dead}")
    lines.append(f"  rate((0,6),(0,1))              {live00}")

    # 6. possibility that we refuse to finish
    lines.append("")
    lines.append("  unlistable (refused)")
    lines.append("  all maps R→R                  |R|^|R|")
    lines.append("  all h in (0,1]                 no last h")
    lines.append("  Newton iterates to √            loop, not a map in this G")
    lines.append("  sin/sqrt on V=Q                 not in G")

    # 7. mix variants on channels — only two cheap ones besides Leibniz
    lines.append("")
    lines.append("  other mixes (toy, listed V=pairs)")
    # value-only mix: channels stay 0 — extract_rate dead
    a, b = pair(3, 1), pair(3, 1)
    val_only = (a[0] * b[0], F(0))
    try:
        extract_rate(val_only, a)
        val_ok = True
    except ValueError:
        val_ok = False
    # add channels only (forget Leibniz cross terms)
    add_ch = (a[0] * b[0], a[1] + b[1])
    r_add = extract_rate(add_ch, a)
    r_lei = extract_rate(mul_p(a, b), a)
    lines.append(f"  value-only mix then rate       {'lives' if val_ok else 'θ dead channel'}")
    lines.append(f"  add-channels mix on x*x at 3   {r_add}   Leibniz {r_lei}")
    lines.append(f"  they split                     {r_add != r_lei}")

    return lines, {
        "rate_ok": rate_ok == rate_n,
        "fd_exact": fd_exact,
        "jet_ok": jet_ok == jet_n,
        "chain": cancel == r_qx,
        "split_mix": r_add != r_lei,
    }


def main():
    lines, meta = report()
    print("\n".join(lines))
    print()
    ok = meta["rate_ok"] and meta["fd_exact"] == 0 and meta["jet_ok"] and meta["chain"] and meta["split_mix"]
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
