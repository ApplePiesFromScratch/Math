"""Units lab — the rate number follows the isolator, not 'the function'."""
from pcalc.kernel import isolate, rate


def main():
    print("UNITS LAB  metres vs centimetres")
    print("  same stick. two isolators.")
    m = isolate(3)          # 3 m, seed 1 m
    print(f"  length in m     {m}  rate(m², m) = {rate(m * m, m)}")
    cm = isolate(300)       # 3 m written as 300 cm
    print(f"  length in cm    {cm}  rate(cm², cm) = {rate(cm * cm, cm)}")
    print("  6 per metre vs 600 per centimetre — not a disagreement.")
    print("  you changed who you isolated. the pair is not 'the derivative of area'.")
    print("  exam English: d(A)/d(m) vs d(A)/d(cm). both legal. different G-arguments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
