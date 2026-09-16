"""Technician vs engineer — same job, different bookkeeping."""

ROWS = [
    ("AND on bits",
     "AND is AND",
     "min and prod coincide on V2; grow V before identity"),
    ("LEM fails",
     "the logic is defective",
     "this G + this θ on this V; L3 next door holds LEM"),
    ("1/x blows up",
     "there is a singularity there",
     "quot is partial; θ at 0; do not hire Inf"),
    ("need higher accuracy",
     "take dt → 0 / n → ∞",
     "name the leftover slot or pay μ into a richer V"),
    ("new system",
     "add axioms until it feels right",
     "forge: knobs in, close-table out"),
    ("rename the center",
     "now it is heliocentric",
     "if G did not change, the error table will not either"),
    ("work happened",
     "that's just setup",
     "GUARD / RECONFIG / μ on the same ledger as STEP"),
]


def report():
    lines = ["TECHNICIAN vs ENGINEER"]
    lines.append(f"  {'job':<22} {'technician':<32} engineer")
    for job, tech, eng in ROWS:
        lines.append(f"  {job:<22} {tech:<32} {eng}")
    return "\n".join(lines)
