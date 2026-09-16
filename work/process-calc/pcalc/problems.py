"""Executable side-by-side set."""
from fractions import Fraction as F
from pcalc.kernel import isolate, rate
from pcalc.jetlab import jet, pow_j
from pcalc.fdlab import fd


def main():
    print("PROBLEMS  standard vs process")
    x = isolate(3)
    rows = [
        ("P1 x²", rate(x * x, x), F(6)),
        ("P2 x²·x³", rate((x * x) * (x ** 3), x), F(405)),
        ("P3 chain x=2", rate((isolate(2) ** 2) ** 3, isolate(2)), F(192)),
        ("P4 1/x", rate(1 / x, x), F(-1, 9)),
    ]
    ok = True
    for n, g, w in rows:
        hit = g == w
        ok &= hit
        print(f"  {n:<20} process={str(g):<8} standard={w}  {'agree' if hit else 'NO'}")
    x2 = isolate(3)
    print(f"  P2 trap product-of-slopes {rate(x2*x2,x2)*rate(x2**3,x2)}  (not 405)")
    print(f"  P6 fd h=1/2 {fd(lambda t: t*t, F(3), F(1,2))}  leftover "
          f"{fd(lambda t: t*t, F(3), F(1,2))-6}")
    print(f"  P8 jet r2 x^4 at 2 {pow_j(jet(2,1,0),4)[2]}")
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
