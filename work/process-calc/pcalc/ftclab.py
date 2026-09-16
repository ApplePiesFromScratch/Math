"""FTC lab — rate of a listed running sum vs the integrand."""
from fractions import Fraction as F
from pcalc.kernel import isolate, rate


def running_mid(fn, a, x, n):
    """Midpoint telescope from a to x in n boxes. Value only."""
    if x == a:
        return F(0)
    w = (x - a) / n
    tot = F(0)
    for i in range(n):
        xi = a + w * i + w / 2
        tot += fn(xi) * w
    return tot


def main():
    print("FTC LAB  two extracts, one grid. no ∞.")
    print("  F(x) = midpoint sum of 2t from 0 to x, n=1 (exact on linears)")
    print("  integrand f(x)=2x. claim: rate(F,x) == f(x) on listed x.")
    ok = True
    for xv in (F(1), F(2), F(3), F(5)):
        # F as a reading: value = exact integral  x², channel via isolate x
        x = isolate(xv)
        Fread = x * x          # antiderivative of 2x is x²
        # running mid n=1 of 2t from 0 to xv is exactly xv²
        mid = running_mid(lambda t: F(2) * t, F(0), xv, 1)
        r = rate(Fread, x)
        fx = F(2) * xv
        hit = mid == Fread.v and r == fx
        ok &= hit
        print(f"  x={xv}  mid={mid}  F={Fread}  rate(F,x)={r}  f(x)={fx}  "
              f"{'ok' if hit else 'SPLIT'}")
    print("  moral: FTC here is 'rate of this antiderivative equals integrand'.")
    print("  the Riemann story is another extract. they agree on this grid.")
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
