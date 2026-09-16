"""Six moves. Each prints the cut, one computation, one moral."""
from __future__ import annotations
import sys
from pcalc.kernel import Theta, isolate, rate


def lesson01():
    print("MOVE 1  a reading is (value, channel)")
    print("  isolate(3) pays a cut. seed defaults to 1.")
    x = isolate(3)
    c = isolate(3, 0)
    print(f"  live  {x}")
    print(f"  dead  {c}   a constant is a reading with r=0")
    print("  moral: two slots. not a number that also has a slope.")


def lesson02():
    print("MOVE 2  rate is a ratio of two channels")
    x = isolate(3)
    print(f"  rate(x, x)  {rate(x, x)}     isolate yourself → 1")
    print(f"  rate(x², x) {rate(x * x, x)}")
    y = isolate(3, 2)
    print(f"  same at seed 2: {rate(y * y, y)}     gauge: seed is a unit")
    print("  moral: isolation is the second argument. there is no independent x.")


def lesson03():
    print("MOVE 3  mix is Leibniz because both slots update")
    x = isolate(3)
    f, g = x * x, x ** 3
    print(f"  f=x² {f}  g=x³ {g}")
    print(f"  f·g = x⁵ {f * g}")
    print(f"  rate(fg,x) {rate(f * g, x)}")
    print(f"  rate(f,x)·g.v + f.v·rate(g,x) = "
          f"{rate(f, x) * g.v + f.v * rate(g, x)}")
    print(f"  product of rates {rate(f, x) * rate(g, x)}  ← different G")
    print("  moral: multiplying slopes forgets the values.")


def lesson04():
    print("MOVE 4  chain is cancellation of a shared channel")
    x = isolate(2)
    y = x * x
    w = y ** 3
    print(f"  y=x² {y}  w=y³ {w}")
    print(f"  rate(w,x) {rate(w, x)}")
    print(f"  rate(w,y)·rate(y,x) {rate(w, y) * rate(y, x)}")
    print(f"  rate(x,w) {rate(x, w)}  ← isolate the output")
    print("  moral: dy/dx was two rates with dx cancelled. the costume is optional.")


def lesson05():
    print("MOVE 5  a pole is θ, not a place")
    x = isolate(3)
    print(f"  rate(1/x, x) {rate(1 / x, x)}")
    try:
        rate(x, isolate(3, 0))
        print("  FAILED to refuse dead isolator")
    except Theta as e:
        print(f"  dead isolator → {e}")
    print(f"  rate((0,6),(0,1)) {rate(isolate(0, 6), isolate(0, 1))}")
    print("  moral: 0/0 as values is quot-θ. 0/0 as live channels is still a rate.")
    print("  do not hire Inf so the map can look total.")


def lesson06():
    print("MOVE 6  second derivative is another presentation")
    print("  this kernel has one channel. x⁴ at 2:")
    x = isolate(2)
    print(f"  rate(x⁴, x) {rate(x ** 4, x)}   that is first channel only")
    print("  a jet V adds r2. a stencil extract approximates r2 and leftover grows with degree.")
    print("  related rates do not need r2. circle x²+y²=25, x=3 y=4 x'=2:")
    # y' = -x x' / y
    yp = -(3 * 2) / 4
    print(f"  y' = {yp}")
    print("  moral: stop the first course here. more slots are more V, not missing pieces.")


LESSONS = {
    "1": lesson01, "01": lesson01,
    "2": lesson02, "02": lesson02,
    "3": lesson03, "03": lesson03,
    "4": lesson04, "04": lesson04,
    "5": lesson05, "05": lesson05,
    "6": lesson06, "06": lesson06,
}


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    if len(argv) > 1 and argv[1] in LESSONS:
        LESSONS[argv[1]]()
        return 0
    for k in ("1", "2", "3", "4", "5", "6"):
        LESSONS[k]()
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
