"""Constraint / curvature leftover — ∇∘∇ as a slot, not a spirit."""
from fractions import Fraction as F
from pcalc.jetlab import jet, mul_j, add_j, pow_j


def main():
    print("CURVATURE LAB  leftover of doing d twice")
    print("  flat: second channel of x^n is the ordinary d²")
    x = jet(2, 1, 0)
    j = pow_j(x, 3)
    print(f"  x³ at 2  jet={j}  r2={j[2]}  (6x=12)")
    print()
    print("  constraint: stay on x²+y²=25. first channel already used.")
    print("  second channel of the constraint must stay dead too")
    print("  (differentiate 2x x'+2y y'=0 again) — that leftover is curvature-ish:")
    print("  x'' and y'' are not free; the connection ate a slot.")
    print()
    # numbers: x=3,y=4,x'=2,y'=-3/2
    # d/dt (x x' + y y') = 0 ⇒ x'² + x x'' + y'² + y y'' = 0
    # if we don't introduce x'', the identity fails — leftover
    xp, yp = F(2), F(-3, 2)
    xv, yv = F(3), F(4)
    leftover_if_no_second = xp * xp + yp * yp
    print(f"  x'²+y'² = {leftover_if_no_second}   not zero")
    print("  that remainder is what a connection would soak.")
    print("  moral: curvature is leftover of two isolations stacked")
    print("  on a constraint that only killed the first channel.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
