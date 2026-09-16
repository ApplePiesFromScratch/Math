from fractions import Fraction as F
from pcalc.kernel import isolate, rate


def main():
    print("WORKSHEET  answers are rates. isolation is printed.")
    x = isolate(3)
    rows = [
        ("x²", rate(x * x, x), 6),
        ("x³", rate(x ** 3, x), 27),
        ("x⁵", rate(x ** 5, x), 405),
        ("2x+1", rate(2 * x + 1, x), 2),
        ("1/x", rate(1 / x, x), F(-1, 9)),
        ("(2x+1)(x²)", rate((2 * x + 1) * (x * x), x),
         rate(2 * x + 1, x) * 9 + 7 * rate(x * x, x)),
    ]
    ok = True
    for name, got, want in rows:
        hit = got == want
        ok &= hit
        print(f"  {name:<16} {str(got):<12} {'ok' if hit else 'BAD'}")
    y = isolate(3, 2)
    print(f"  gauge seed 2     {rate(y * y, y)}")
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
