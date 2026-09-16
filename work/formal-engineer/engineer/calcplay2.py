"""calcplay2.py — more hunts.

    python -m engineer.calcplay2
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product


def P(v, r=0):
    return (F(v), F(r))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


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


INS = []


def note(title, body, hold):
    INS.append((hold, title, body))


def hunt():
    # 1. Euler: x * rate(x^n, x) = n * x^n
    e_ok = e_n = 0
    for n, v, k in product(range(1, 6), [F(2), F(3), F(1, 2)], [F(1), F(2)]):
        x = P(v, k)
        f = pow_n(x, n)
        e_n += 1
        e_ok += (x[0] * rate(f, x) == F(n) * f[0])
    note("Euler  x·rate(x^n,x)=n·x^n", f"{e_ok}/{e_n}", e_ok == e_n)

    # 2. rate of sum is sum of rates (channels add)
    x = P(3, 1)
    f, g = pow_n(x, 2), pow_n(x, 3)
    note("rate(f+g,x)=rate(f,x)+rate(g,x)",
         f"{rate(add(f, g), x)} = {rate(f, x)+rate(g, x)}",
         rate(add(f, g), x) == rate(f, x) + rate(g, x))

    # 3. quotient rule is just quot+rate
    q = quot(f, g)
    want = (rate(f, x) * g[0] - f[0] * rate(g, x)) / (g[0] * g[0])
    note("quot rule is not extra",
         f"{rate(q, x)} vs {want}",
         rate(q, x) == want)

    # 4. parametric: rate(y,x)=rate(y,t)/rate(x,t)
    t = P(5, 1)
    px, py = pow_n(t, 2), pow_n(t, 3)     # x=t², y=t³
    note("parametric slope",
         f"rate(y,x)={rate(py, px)}  y'/x'={rate(py,t)/rate(px,t)}",
         rate(py, px) == rate(py, t) / rate(px, t))

    # 5. unit change on the isolator: scale v and r together
    # measure x in "halves": X = 2x, so X.v=6, if x.v=3 seed 1 then X seed 2
    x = P(3, 1)
    X = P(6, 2)            # same isolation, new unit
    note("change of unit on x",
         f"rate(x²,x)={rate(pow_n(x,2),x)}  rate(X²,X)={rate(pow_n(X,2),X)}",
         rate(pow_n(x, 2), x) == 6 and rate(pow_n(X, 2), X) == 6)
    # wait X² at X=6 is 2*6=12 if X is the variable. That's rate wrt X not x.
    # insight: rate depends on which unit you isolate — 12 vs 6
    note("unit change *does* change the rate",
         f"wrt x: {rate(pow_n(x,2),x)}  wrt 2x: {rate(pow_n(X,2),X)}",
         rate(pow_n(x, 2), x) != rate(pow_n(X, 2), X))

    # 6. trapezoid leftover on x² vs mid
    def trap(n, a=F(0), b=F(2)):
        w = (b - a) / n
        tot = F(0)
        for i in range(n):
            lo = a + w * i
            hi = lo + w
            tot += (lo * lo + hi * hi) * w / 2
        return tot

    def mid(n, a=F(0), b=F(2)):
        w = (b - a) / n
        tot = F(0)
        for i in range(n):
            xi = a + w * i + w / 2
            tot += (xi * xi) * w
        return tot

    exact = F(8) / 3    # ∫0^2 x² = 8/3
    note("trap vs mid on x² [0,2] n=1",
         f"trap={trap(1)} mid={mid(1)} exact={exact}  "
         f"trap-err={trap(1)-exact} mid-err={mid(1)-exact}",
         trap(1) != exact and mid(1) != exact)

    # 7. homogeneous: f(λx) channel vs λ
    # skip — no λ-slot unless we isolate λ
    lam = P(2, 1)
    xconst = P(3, 0)
    # f = (λx)^2 = λ² x², isolate λ
    f_lam = pow_n(mul(lam, xconst), 2)
    note("isolate the scale λ, x frozen",
         f"f=(λx)² at λ=2 x=3  rate(f,λ)={rate(f_lam, lam)} want 2λ x²={2*lam[0]*xconst[0]**2}",
         rate(f_lam, lam) == 2 * lam[0] * xconst[0] ** 2)

    # 8. dead output, live isolator: constant function
    x = P(3, 1)
    c = P(4, 0)
    note("constant function rate 0, not θ",
         f"rate(c,x)={rate(c, x)}",
         rate(c, x) == 0)

    # 9. live output, dead isolator is the only θ
    th = False
    try:
        rate(P(4, 2), P(3, 0))
    except ValueError:
        th = True
    note("θ is dead *isolator*, not dead output",
         "rate(live, dead-x) θ", th)

    # 10. binomial vs pair: (x+h)² − x² all /h
    x, h = F(5), F(2)
    binom = (2 * x + h)
    note("(x+h)²−x² over h = 2x+h",
         f"{binom}  fd={((x+h)**2-x**2)/h}",
         binom == ((x + h) ** 2 - x ** 2) / h == 2 * x + h)

    # 11. rate(1/f, x) = -rate(f,x)/f²
    x = P(3, 1)
    f = pow_n(x, 2)
    inv = quot(P(1, 0), f)
    note("rate(1/f,x)=-rate(f,x)/f²",
         f"{rate(inv, x)} vs {-rate(f, x)/(f[0]*f[0])}",
         rate(inv, x) == -rate(f, x) / (f[0] * f[0]))

    # 12. you cannot recover a jet from one pair
    # same pair (9,6) is x² at 3 seed 1 AND also  something else?
    # (9,6) = x² at 3, seed 1. Also 3x at 3 seed 2? 3x at 3 seed 2 is (9,6) YES
    a = pow_n(P(3, 1), 2)          # x²
    b = mul(P(3, 0), P(3, 2))      # 3·x with x isolated seed 2
    note("same pair, two situations",
         f"x² seed1={a}  3x seed2={b}  equal={a==b}  "
         f"rate wrt (3,1)={rate(a,P(3,1))} rate wrt (3,2)={rate(b,P(3,2))}",
         a == b and rate(a, P(3, 1)) != rate(b, P(3, 2)))

    return INS


def main():
    rows = hunt()
    print("CALC PLAY 2")
    print()
    ok = 0
    for hold, title, body in rows:
        ok += bool(hold)
        print(f"  [{'HOLD' if hold else 'SPLIT'}] {title}")
        print(f"          {body}")
    print()
    print(f"  {ok}/{len(rows)} held")
    print("verdict", "PASS" if ok == len(rows) else "FAIL")
    return 0 if ok == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
