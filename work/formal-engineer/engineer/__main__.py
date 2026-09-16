"""python -m engineer [enum|infinity|introduce|ghosts|poles|contrast]"""
from __future__ import annotations
import sys

from engineer.enum import report as enum_report
from engineer.infinity import report as inf_report
from engineer.introduce import report as intro_report
from engineer.ghosts import report as ghost_report
from engineer.poles import report as pole_report
from engineer.contrast import report as contrast_report
from engineer.census import report as census_report


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    cmd = argv[1] if len(argv) > 1 else "all"
    bits = {
        "enum": lambda: enum_report("0,1/2,1")[0],
        "infinity": inf_report,
        "introduce": intro_report,
        "ghosts": ghost_report,
        "poles": pole_report,
        "contrast": contrast_report,
        "census": lambda: "\n".join(census_report()[0]),
    }
    if cmd in ("-h", "--help"):
        print(__doc__)
        return 0
    order = list(bits) if cmd == "all" else [cmd]
    if cmd not in bits and cmd != "all":
        print("unknown", cmd)
        return 1
    for name in order:
        print(bits[name]())
        print()
    # cheap self-check
    _, rows = __import__("engineer.enum", fromlist=["enumerate_cuts"]).enumerate_cuts("0,1/2,1")
    close = sum(1 for r in rows if r["closes"])
    leave = sum(1 for r in rows if not r["closes"])
    print(f"self-check  V3 triples close={close} leave={leave}")
    print("verdict", "PASS" if close and leave else "FAIL")
    return 0 if close and leave else 1


if __name__ == "__main__":
    raise SystemExit(main())
