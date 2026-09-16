"""fd lab — leftover is an identity on monomials, not an error bar."""
from fractions import Fraction as F
from pcalc.kernel import isolate, rate


def fd(fn, x, h):
    return (fn(x + h) - fn(x)) / h


def main():
    print("FD LAB  reconstruction cost, printed.")
    x = isolate(3)
    print(f"  rate(x²,x) {rate(x * x, x)}")
    print("  fd(x²) − 2x = h  on every listed pair:")
    for xv, h in ((F(2), F(1)), (F(3), F(1, 2)), (F(5), F(1, 10))):
        left = fd(lambda t: t * t, xv, h) - F(2) * xv
        print(f"    x={xv} h={h}  leftover={left}  (=h? {left==h})")
    print("  fd exact only at degree 1:")
    xv, h = F(3), F(1, 2)
    for d in range(1, 5):
        true = F(d) * xv ** (d - 1)
        got = fd(lambda t, d=d: t ** d, xv, h)
        print(f"    deg {d}  fd={got}  rate-like={true}  leftover={got-true}")
    print("  moral: if you use fd, keep h on the page. do not send it to 0 off-book.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
