"""Emit a problem from knobs. Start of the exercise generator."""
from fractions import Fraction as F
from pcalc.kernel import isolate, rate


def emit(degree=2, at=3, seed=1, extract="rate"):
    x = isolate(at, seed)
    f = x ** degree
    want = rate(f, x)
    lines = [
        f"PROBLEM  V=pair  isolate x={at} seed={seed}  f=x^{degree}  extract={extract}",
        f"  reading x = {x}",
        f"  reading f = {f}",
    ]
    if extract == "rate":
        lines.append(f"  answer rate(f,x) = {want}")
    elif extract == "fd":
        h = F(1, 2)
        fd = ((F(at) + h) ** degree - F(at) ** degree) / h
        lines.append(f"  fd(h={h}) = {fd}  leftover vs rate = {fd - want}")
    return "\n".join(lines), want


def main():
    print("GENERATOR  knobs in, problem out")
    print()
    for deg, at, seed, ext in (
        (2, 3, 1, "rate"),
        (2, 3, 2, "rate"),
        (3, 2, 1, "rate"),
        (2, 3, 1, "fd"),
        (5, 3, 1, "rate"),
    ):
        text, _ = emit(deg, at, seed, ext)
        print(text)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
