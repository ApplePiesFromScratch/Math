"""History as presentations — short pack for students."""


def main():
    print("HISTORY LAB  packing order, six beats")
    beats = [
        ("Fermat E", "increment that lives for quot then dies"),
        ("Newton t", "isolator locked to time; unary D born"),
        ("Leibniz dx/dy", "best costume, two hired points"),
        ("Berkeley", "θ-check: E used as 0 and not-0"),
        ("Weierstrass", "unlistable V so the last h is not listed"),
        ("this cut", "seed free, leftover listed, Inf refused"),
    ]
    for i, (n, s) in enumerate(beats, 1):
        print(f"  {i}. {n:<16} {s}")
    print("  exam: you do not need this page. this course does.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
