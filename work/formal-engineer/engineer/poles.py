"""Singularities: where V breaks if you insist the op is total."""
from fractions import Fraction as F


def quot(a, b):
    if b == 0:
        raise ValueError("θ: divisor not live")
    return a / b


def report():
    lines = ["POLES / BREAKS"]
    lines.append("  V = Q. G includes quot. θ: divisor ≠ 0.")
    try:
        quot(F(1), F(0))
        fired = False
    except ValueError:
        fired = True
    lines.append(f"  1/0 → θ fired: {fired}   (not a value called Inf)")
    lines.append("  technician: draw a vertical asymptote and call it a place")
    lines.append("  engineer: the map is partial; the graph does not contain that x")
    lines.append("  live channels at 0/0 values are a different G (rate), not quot")
    lines.append("  introducing Inf so quot can be total is hiring a ghost")
    return "\n".join(lines)
