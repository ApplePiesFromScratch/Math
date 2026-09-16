"""calcexplore.py — more plays before a calc repo.

Questions, not slogans:
  does the d2 stencil survive a quartic?
  is the integral a second extract or a second V?
  related rates: two channels, one situation
  inverse: forced by mix+quot, or a new law?
  smallest G that still does product + chain + inverse

    python -m engineer.calcexplore
"""
from __future__ import annotations

from fractions import Fraction as F


def P(v, r=0):
    return (F(v), F(r))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0] * b[0], a[1] * b[0] + a[0] * b[1])


def quot(a, b):
    if b[0] == 0:
        raise ValueError("θ quot")
    return (a[0] / b[0], (a[1] * b[0] - a[0] * b[1]) / (b[0] * b[0]))


def rate(p, g):
    if g[1] == 0:
        raise ValueError("θ rate")
    return p[1] / g[1]


def pow_n(x, n):
    out = P(1, 0)
    for _ in range(n):
        out = mul(out, x)
    return out


def val_pow(x, n):
    return x ** n


def play():
    lines = ["CALC EXPLORE"]
    findings = []

    # ── 1. quartic kills stencil coincidence ────────────────────────
    x0 = F(2)
    h = F(1, 2)
    d2_true = F(4) * F(3) * (x0 ** 2)          # d²/dx² x^4 = 12 x² = 48
    stencil = (val_pow(x0 + h, 4) - 2 * val_pow(x0, 4) + val_pow(x0 - h, 4)) / (h * h)
    j = pow_n(P(x0, 1), 4)
    # pair has no r2; rebuild second channel by isolating the rate
    # cheaper: finite second via two rates? skip — use known 12 x²
    lines.append("1. quartic vs central d2 stencil")
    lines.append(f"   true d2 of x^4 at 2          {d2_true}")
    lines.append(f"   stencil h={h}                 {stencil}")
    lines.append(f"   they split                   {stencil != d2_true}")
    findings.append(stencil != d2_true)

    # ── 2. inverse is mix+quot, not a new tablet ────────────────────
    x = P(3, 1)
    inv = quot(P(1, 0), x)
    lines.append("2. inverse")
    lines.append(f"   rate(1/x, x) at 3            {rate(inv, x)}   want {-F(1, 9)}")
    findings.append(rate(inv, x) == -F(1, 9))

    # ── 3. related rates: one situation, two channels ───────────────
    # x² + y² = 25, x=3, y=4, rate(x,t)=2  → rate(y,t)=?
    # 2x x' + 2y y' = 0 ⇒ y' = -x x' / y
    xt = P(3, 2)
    # y as a reading whose value is 4; channel unknown — solve
    # from add(pow x, pow y) constant ⇒ rate(sum, t)=0
    # we have x; construct y channel from the constraint
    yv = F(4)
    # d/dt (x²+y²)=0 = 2x x' + 2y y' 
    yp = -(xt[0] * xt[1]) / yv
    yt = P(yv, yp)
    s = add(pow_n(xt, 2), pow_n(yt, 2))
    lines.append("3. related rates  x²+y²=25, x=3 y=4  x'=2")
    lines.append(f"   y'                           {yp}   want {-F(3, 2)}")
    lines.append(f"   rate(x²+y², t)               {rate(s, P(0, 1))}   "
                 f"(t isolated as seed 1 dummy)")
    # isolate t as dummy with r=1, values unused — s.r should be 0
    lines.append(f"   constraint channel is dead   {s[1] == 0}")
    findings.append(yp == -F(3, 2) and s[1] == 0)

    # ── 4. integral as telescope of increments, listed partition ────
    # area under 2x from 0 to 3: exact 9
    # partition n boxes of width 1: left/right/mid
    def boxes(n, kind):
        w = F(3) / n
        tot = F(0)
        for i in range(n):
            if kind == "left":
                xi = w * i
            elif kind == "right":
                xi = w * (i + 1)
            else:
                xi = w * i + w / 2
            tot += (F(2) * xi) * w
        return tot
    exact = F(9)
    lines.append("4. integral of 2x on [0,3] — listed partitions, not n→∞")
    for n in (1, 3, 6):
        L, R, M = boxes(n, "left"), boxes(n, "right"), boxes(n, "mid")
        lines.append(f"   n={n}  left={L}  right={R}  mid={M}  exact={exact}")
    lines.append(f"   mid n=1 already exact for linear? {boxes(1,'mid')==exact}")
    findings.append(boxes(1, "mid") == exact)
    findings.append(boxes(3, "left") != exact)

    # ── 5. smallest G ───────────────────────────────────────────────
    # need: isolate, add, mul (Leibniz), quot, rate
    # do NOT need: limits, Inf, unary D, fd, integrals as primitives
    lines.append("5. smallest G that still does product+chain+inverse")
    lines.append("   keep:  isolate, add, Leibniz-mul, quot, rate")
    lines.append("   drop:  limits, Inf, unary D, fd, Riemann primitive")
    lines.append("   integral, if needed, is a listed telescope — other G")
    lines.append("   second channel, if needed, is jet V — other V")

    # ── 6. what 'simpler to learn' can actually mean ────────────────
    lines.append("6. pedagogy cut (not yet a repo)")
    lines.append("   1. two channels under one cut")
    lines.append("   2. rate is their ratio")
    lines.append("   3. mix is Leibniz because both channels update")
    lines.append("   4. chain is cancellation of a shared channel")
    lines.append("   5. a pole is θ, not a place")
    lines.append("   6. a second derivative is a second slot or a stencil")
    lines.append("   stop. that is a course. the rest is other presentations.")

    return lines, findings


def main():
    lines, findings = play()
    print("\n".join(lines))
    print()
    print("findings", findings)
    print("verdict", "PASS" if all(findings) else "FAIL")
    return 0 if all(findings) else 1


if __name__ == "__main__":
    raise SystemExit(main())
