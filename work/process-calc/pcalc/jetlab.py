"""Jet lab — second channel as a paid slot, not a limit of first channels."""
from fractions import Fraction as F
from pcalc.kernel import isolate, rate


def jet(v, r=1, r2=0):
    return (F(v), F(r), F(r2))


def add_j(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul_j(a, b):
    return (
        a[0] * b[0],
        a[1] * b[0] + a[0] * b[1],
        a[2] * b[0] + 2 * a[1] * b[1] + a[0] * b[2],
    )


def pow_j(x, n):
    out = jet(1, 0, 0)
    for _ in range(n):
        out = mul_j(out, x)
    return out


def stencil_d2(fn, x, h):
    return (fn(x + h) - 2 * fn(x) + fn(x - h)) / (h * h)


def main():
    print("JET LAB  r2 is a slot. stencil is another extract.")
    x = jet(2, 1, 0)
    for n in (2, 3, 4):
        j = pow_j(x, n)
        print(f"  x^{n} at 2  (v,r,r2)={j}")
    print()
    print("  stencil leftover vs jet r2 at x=2")
    for n, h in ((3, F(1, 2)), (4, F(1, 2)), (4, F(1, 8))):
        j = pow_j(jet(2, 1, 0), n)
        st = stencil_d2(lambda t, n=n: t ** n, F(2), h)
        print(f"  deg {n} h={h}  jet r2={j[2]}  stencil={st}  split={st != j[2]}")
    print("  moral: pay for r2 or name the leftover. do not say 'the second derivative'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
