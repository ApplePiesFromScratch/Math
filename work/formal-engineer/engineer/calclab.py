"""calclab.py — a first worksheet that never mentions limits.

Not the whole of analysis. A generated practice cut:
V = Q-pairs, G = mix + rate, θ = live isolation.
Problems are polynomials. Answers are rates. Isolation is printed
as the second argument so nobody grows an independent variable.

    python -m engineer.calclab
"""
from fractions import Fraction as F


def isolate(v, k=1):
    return (F(v), F(k))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0] * b[0], a[1] * b[0] + a[0] * b[1])


def rate(p, g):
    if g[1] == 0:
        raise ValueError("θ: dead isolation")
    return p[1] / g[1]


def pow_n(x, n):
    out = isolate(1, 0)
    for _ in range(n):
        out = mul(out, x)
    return out


def worksheet():
    x = isolate(3)
    rows = []
    rows.append(("x² at 3", rate(pow_n(x, 2), x), F(6)))
    rows.append(("x³ at 3", rate(pow_n(x, 3), x), F(27)))
    rows.append(("x⁵ at 3", rate(pow_n(x, 5), x), F(405)))
    rows.append(("2x+1 at 3", rate(add(mul(isolate(2, 0), x), isolate(1, 0)), x), F(2)))
    y = isolate(3, 2)
    rows.append(("x² at 3 seed 2 (gauge)", rate(pow_n(y, 2), y), F(6)))
    z = isolate(0, 1)
    w = isolate(0, 6)
    rows.append(("rate of two dead *values*, live channels", rate(w, z), F(6)))
    return rows


def main():
    print("CALCLAB  generated worksheet — no limits, no Inf, no independent x")
    print("  isolation is an argument. rate is a ratio of channels.")
    print()
    ok = True
    for name, got, want in worksheet():
        hit = got == want
        ok &= hit
        print(f"  {name:<48} {str(got):<8} {'ok' if hit else 'BAD '+str(want)}")
    print()
    print("  next knob: add a 2-jet V if you need a second channel.")
    print("  that is a new presentation, not 'the rest of calculus'.")
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
