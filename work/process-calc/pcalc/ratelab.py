"""Related-rates / implicit lab — one situation, several isolations."""
from pcalc.kernel import isolate, rate


def main():
    print("RATE LAB  no extra chapter. same kernel.")
    print()
    print("  implicit: x² + y² = 25, x=3, y=4, isolate t with x'=2")
    x = isolate(3, 2)
    # y' from 2x x' + 2y y' = 0
    yp = -(x.v * x.r) / 4
    y = isolate(4, yp)
    s = x * x + y * y
    print(f"  y'={yp}  (x²+y²)={s}  rate(s, dummy-t)={s.r}")
    print()
    print("  parametric: x=t², y=t³ at t=5")
    t = isolate(5)
    px, py = t * t, t ** 3
    print(f"  rate(y,x)={rate(py, px)}  rate(y,t)/rate(x,t)={rate(py, t)/rate(px, t)}")
    print()
    print("  isolate the output: y=x² at 3")
    x = isolate(3)
    print(f"  rate(x, x²)={rate(x, x * x)}  = 1/rate(x²,x)")
    print("  moral: related, implicit, parametric, inverse isolation — one knob.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
