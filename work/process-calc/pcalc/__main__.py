from pcalc.kernel import isolate, rate

def main():
    x = isolate(3)
    print("process calculus kernel")
    print(f"  x = {x}")
    print(f"  x² = {x*x}   rate {rate(x*x, x)}")
    print(f"  1/x = {1/x}   rate {rate(1/x, x)}")
    y = isolate(3, 2)
    print(f"  seed 2: rate(x²,x) {rate(y*y, y)}   (gauge)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
