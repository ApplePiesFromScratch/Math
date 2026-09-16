import sys
from studio import algebra, logic, calc


def main():
    print("STUDIO")
    print()
    algebra.main()
    print()
    logic.main()
    print()
    calc.main()
    print()
    print("verdict PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
