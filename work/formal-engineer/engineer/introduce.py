"""Introduction and change: turn one knob, read the new table.

Introduction of a value, a connective, or a designated set is G of
the meta-carrier. It is not discovering a pre-existing essence.
"""
from engineer.enum import enumerate_cuts


def report():
    lines = ["INTRODUCTION / CHANGE"]
    specs = [
        ("introduce nothing (V2)", "0,1"),
        ("introduce ½ (V3)", "0,1/2,1"),
        ("introduce thirds (V4)", "0,1/3,2/3,1"),
    ]
    for title, spec in specs:
        V, rows = enumerate_cuts(spec)
        close = [r for r in rows if r["closes"]]
        lem_y = sum(1 for r in close if r["LEM"])
        lines.append(f"  {title:<28} |V|={len(V)}  closing G={len(close)}  "
                     f"of those LEM holds on {lem_y}")
    lines.append("  V2: min and product coincide — technician says AND is AND")
    lines.append("  V3: they split. introduction of ½ was the experiment.")
    lines.append("  change G only (same V3): L3 LEM holds, K3 LEM fails")
    lines.append("  change θ only (designate {½,1} on K3 tables): LP, LEM returns, LNC goes")
    lines.append("  that last row is not a new essence. it is θ.")
    return "\n".join(lines)
