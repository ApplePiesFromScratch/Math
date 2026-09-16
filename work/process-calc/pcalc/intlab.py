"""Integral lab — listed partitions. Leftover is the answer's twin."""
from fractions import Fraction as F


def boxes(fn, a, b, n, kind):
    w = (b - a) / n
    tot = F(0)
    for i in range(n):
        lo = a + w * i
        if kind == "left":
            xi = lo
        elif kind == "right":
            xi = lo + w
        elif kind == "mid":
            xi = lo + w / 2
        else:
            xi = lo
            tot += (fn(lo) + fn(lo + w)) * w / 2
            continue
        tot += fn(xi) * w
    return tot


def main():
    print("INTEGRAL LAB  no n→∞. leftover stays on the page.")
    a, b = F(0), F(3)

    def f(x):
        return F(2) * x

    exact = F(9)
    print("  2x on [0,3]  exact=9")
    for n in (1, 3, 6):
        print(f"  n={n}  left={boxes(f,a,b,n,'left')}  "
              f"right={boxes(f,a,b,n,'right')}  "
              f"mid={boxes(f,a,b,n,'mid')}  "
              f"trap={boxes(f,a,b,n,'trap')}")
    print(f"  mid n=1 exact? {boxes(f,a,b,1,'mid')==exact}")

    def g(x):
        return x * x

    exact2 = F(8) / 3
    print("  x² on [0,2]  exact=8/3")
    a2, b2 = F(0), F(2)
    for n in (1, 2, 4):
        m = boxes(g, a2, b2, n, "mid")
        t = boxes(g, a2, b2, n, "trap")
        print(f"  n={n}  mid={m} err={m-exact2}  trap={t} err={t-exact2}")
    print("  moral: mid of a linear is exact at n=1. deg 2 leftover is signed and exact.")
    print("  hiring ∞ hides those two sentences.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
