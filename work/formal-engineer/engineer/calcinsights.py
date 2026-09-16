"""calcinsights.py — hunt, don't teach.

    python -m engineer.calcinsights
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product


def P(v, r=0):
    return (F(v), F(r))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0] * b[0], a[1] * b[0] + a[0] * b[1])


def quot(a, b):
    if b[0] == 0:
        raise ValueError("θ")
    return (a[0] / b[0], (a[1] * b[0] - a[0] * b[1]) / (b[0] * b[0]))


def rate(p, g):
    if g[1] == 0:
        raise ValueError("θ")
    return p[1] / g[1]


def pow_n(x, n):
    out = P(1, 0)
    for _ in range(n):
        out = mul(out, x)
    return out


def fd(fn, x, h):
    return (fn(x + h) - fn(x)) / h


INS = []


def note(title, body, hold):
    INS.append((hold, title, body))


def hunt():
    # A. rate(f,f) is 1 whenever the channel lives
    hits = miss = 0
    for v, k in product([F(2), F(3), F(-4), F(1, 5)], [F(1), F(2), F(-1)]):
        f = pow_n(P(v, k), 3)
        if f[1] == 0:
            continue
        hits += rate(f, f) == 1
        miss += rate(f, f) != 1
    note("rate(f,f)=1", f"live self-rate {hits} hits, {miss} misses", miss == 0 and hits > 0)

    # B. rate(f,g)*rate(g,f)=1  inverse isolations
    inv_ok = 0
    inv_n = 0
    for v, k, m in product([F(2), F(3)], [F(1), F(2)], [F(1), F(3)]):
        x = P(v, k)
        y = pow_n(x, 2)  # live if x live
        # re-read y with a different seed on x already baked
        inv_n += 1
        if rate(y, x) * rate(x, y) == 1:
            inv_ok += 1
    note("rate(f,g)*rate(g,f)=1", f"{inv_ok}/{inv_n}", inv_ok == inv_n)

    # C. rate(f,x)/rate(g,x) == rate(f,g)   change of isolation
    co_ok = co_n = 0
    for v, k in product([F(2), F(3), F(5)], [F(1), F(2)]):
        x = P(v, k)
        f = pow_n(x, 3)
        g = pow_n(x, 2)
        co_n += 1
        if rate(f, x) / rate(g, x) == rate(f, g):
            co_ok += 1
    note("rate(f,x)/rate(g,x)=rate(f,g)", f"{co_ok}/{co_n}", co_ok == co_n)

    # D. fd exact iff f linear on the step (polynomial test)
    exact_when = []
    for deg in range(1, 6):
        x, h = F(3), F(1, 2)
        true = F(deg) * x ** (deg - 1)
        got = fd(lambda t, d=deg: t ** d, x, h)
        exact_when.append((deg, got == true, got - true))
    note("fd exact only at deg 1",
         " ".join(f"d{d}:{'Y' if e else 'n('+str(err)+')'}" for d, e, err in exact_when),
         exact_when[0][1] and not any(e for d, e, err in exact_when[1:]))

    # E. midpoint integral exact for deg <= 1; simpson-ish not here
    def mid(deg, n, a=F(0), b=F(3)):
        w = (b - a) / n
        tot = F(0)
        for i in range(n):
            xi = a + w * i + w / 2
            tot += (xi ** deg) * w
        return tot

    def exact_int(deg, a=F(0), b=F(3)):
        return (b ** (deg + 1) - a ** (deg + 1)) / F(deg + 1)

    mid_exact = [(d, n, mid(d, n) == exact_int(d))
                 for d in range(0, 4) for n in (1, 2, 3)]
    note("midpoint exactness",
         " ".join(f"deg{d}n{n}:{'Y' if e else 'n'}" for d, n, e in mid_exact),
         all(e for d, n, e in mid_exact if d <= 1) and
         not any(e for d, n, e in mid_exact if d == 3 and n == 1))

    # F. isolate the OUTPUT: rate(x, f) is 1/rate(f,x)
    x = P(3, 1)
    f = pow_n(x, 2)
    note("isolate the output",
         f"rate(x, x²)={rate(x, f)}  1/rate(x²,x)={1/rate(f, x)}",
         rate(x, f) == 1 / rate(f, x))

    # G. constant has dead channel — cannot isolate it
    c = P(7, 0)
    dead = False
    try:
        rate(c, c)
    except ValueError:
        dead = True
    note("cannot isolate a constant", "rate(c,c) θ", dead)

    # H. scaling isolation scales both channels; ratio invariant
    x1, xk = P(3, 1), P(3, 5)
    note("seed is a unit, not a fact",
         f"rate(x²,x) seed1={rate(pow_n(x1,2),x1)} seed5={rate(pow_n(xk,2),xk)}",
         rate(pow_n(x1, 2), x1) == rate(pow_n(xk, 2), xk))

    # I. product of rates ≠ rate of product
    x = P(3, 1)
    f, g = pow_n(x, 2), pow_n(x, 3)
    note("rate(f,x)*rate(g,x) vs rate(fg,x)",
         f"{rate(f,x)*rate(g,x)} vs {rate(mul(f,g),x)}  "
         f"Leibniz {rate(f,x)*g[0]+f[0]*rate(g,x)}",
         rate(f, x) * rate(g, x) != rate(mul(f, g), x)
         and rate(mul(f, g), x) == rate(f, x) * g[0] + f[0] * rate(g, x))

    # J. three-link chain
    x = P(2, 1)
    y = pow_n(x, 2)
    z = pow_n(y, 2)          # x^4
    w = pow_n(z, 2)          # x^8
    note("three-link chain multiplies",
         f"rate(w,x)={rate(w,x)}  product={rate(w,z)*rate(z,y)*rate(y,x)}",
         rate(w, x) == rate(w, z) * rate(z, y) * rate(y, x))

    # K. fd leftover for x² is exactly h
    leftovers = []
    for x, h in product([F(2), F(5)], [F(1), F(1, 3), F(1, 10)]):
        leftovers.append(fd(lambda t: t * t, x, h) - F(2) * x == h)
    note("fd(x²)−2x = h exactly",
         f"{sum(leftovers)}/{len(leftovers)}",
         all(leftovers))

    # L. two isolations of the SAME pair — rate independent of who is 'x'
    # already B. deepen: three readings of one situation
    t = P(0, 1)  # dummy time
    # situation: a=2t, b=3t at t-value unused; channels 2 and 3
    a, b = P(10, 2), P(15, 3)
    note("two channels of one dummy",
         f"rate(a,t)={rate(a,t)} rate(b,t)={rate(b,t)} rate(a,b)={rate(a,b)}",
         rate(a, t) / rate(b, t) == rate(a, b) == F(2, 3))

    return INS


def main():
    rows = hunt()
    print("CALC INSIGHTS")
    print()
    n_ok = 0
    for hold, title, body in rows:
        n_ok += bool(hold)
        print(f"  [{'HOLD' if hold else 'SPLIT'}] {title}")
        print(f"          {body}")
    print()
    print(f"  {n_ok}/{len(rows)} held")
    print("verdict", "PASS" if n_ok == len(rows) else "FAIL")
    return 0 if n_ok == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
