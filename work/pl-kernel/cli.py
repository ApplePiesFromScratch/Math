"""CLI: python -m pl [demo|cert|vs-fd|migrate|map]."""
from __future__ import annotations

from fractions import Fraction as F
import sys

from pl.certify import certify, finite_difference
from pl.reading import Q, Theta, isolate, rate


def demo() -> None:
    print("PL v0.3  P/G→Q   V=Q-pairs  G=mix+rate  θ=live isolation")
    x = isolate(3)
    print(f"  rate(x*x, x)  {rate(x * x, x)}")
    print(f"  rate(x**5, x) {rate(x ** 5, x)}")
    print(f"  rate(1/x, x)  {rate(1 / x, x)}")
    for k in (1, 2, F(1, 2)):
        z = isolate(3, k)
        print(f"  seed={k}  rate(x*x,x)={rate(z * z, z)}")
    try:
        rate(x, isolate(3, 0))
    except Theta as e:
        print(f"  θ  {e}")


def main(argv=None) -> int:
    argv = list(sys.argv if argv is None else argv)
    cmd = argv[1] if len(argv) > 1 else "demo"
    if cmd in ("-h", "--help"):
        print("usage: python -m pl [demo|cert|vs-fd|migrate|map]")
        return 0
    if cmd == "cert":
        print(certify(lambda z: z ** 3 + 2 * z, at=3).as_json())
        return 0
    if cmd == "vs-fd":
        print("exact", rate(isolate(3) ** 2, isolate(3)))
        for h in (1, F(1, 2), F(1, 8), F(1, 64)):
            print(" fd", h, finite_difference(lambda t: Q(t) * Q(t), 3, h))
        return 0
    if cmd == "migrate":
        from pl.migrate import main as m
        return m()
    if cmd == "map":
        from PROCESS import dump_map
        print(dump_map())
        return 0
    demo()
    return 0
