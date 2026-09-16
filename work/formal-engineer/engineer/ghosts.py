"""Ghosts: outputs treated as primitive containers or as causes.

A ghost is a value or name that is doing work off-book:
  - treated as an inhabitant that was always there
  - treated as the cause of the operations that produced it
  - used to hide a θ firing
"""

GHOSTS = [
    {
        "name": "∞ as a point in V",
        "what": "the loop had no last pair; a point was hired to finish it",
        "instead": "θ: quantifier unlistable. DEFER or refuse the lift",
        "receipt": "infinity.py |V|=ℝ has no last pair; ℝ∪{∞} adds a G-row",
    },
    {
        "name": "¼ promoted after AND_prod on V3",
        "what": "the op left V; the image was hired as a new primitive",
        "instead": "θ or μ into a V that already lists ¼",
        "receipt": "enum: AND_prod+… closes=NO on V3",
    },
    {
        "name": "the independent variable",
        "what": "a locked seed treated as a thing with its own life",
        "instead": "isolation is an argument of rate(P,G)",
        "receipt": "gauge: four seeds, one ratio",
    },
    {
        "name": "unary derivative as a property of f",
        "what": "the collapsed channel sold as something f has",
        "instead": "a presentation of the same mix with seed locked",
        "receipt": "D kills r; rate keeps r",
    },
    {
        "name": "epicycle as a celestial inhabitant",
        "what": "Fourier leftover hired as a body",
        "instead": "name the slot (G_center / G_stretch) or change isolation",
        "receipt": "2M-epi worsened radius; center+stretch closed both",
    },
    {
        "name": "penetration slop as V=non-penetrating",
        "what": "θ dressed as the alphabet of rigid bodies",
        "instead": "declare slop as θ, or put penetration in V (soft)",
        "receipt": "phys2d pen_max>0 while advertising disjoint V",
    },
    {
        "name": "smaller dt as accuracy",
        "what": "∞ hired as a time inhabitant",
        "instead": "name dt_max; past the wall is decohere",
        "receipt": "dt<=0 and dt>dt_max → Theta",
    },
    {
        "name": "pixels as the game",
        "what": "V_view sold as V_game",
        "instead": "demo hash is the certificate of the tic",
        "receipt": "frame ≠ tic; G_draw must not write V_game",
    },
    {
        "name": "AND as one op",
        "what": "agreement on {0,1} hired as the essence of conjunction",
        "instead": "grow V; min / prod / luk split",
        "receipt": "enum table on V3",
    },
    {
        "name": "singularity as a place on the line",
        "what": "θ at v=0 hired as a point that 'is' infinite",
        "instead": "quot fires θ; channels may still have a rate",
        "receipt": "rate((0,6),(0,1))=6; 1/0 is not a value",
    },
]


def report():
    lines = ["GHOSTS  outputs treated as things, or as causes of the ops"]
    for i, g in enumerate(GHOSTS, 1):
        lines.append(f"  {i:>2}. {g['name']}")
        lines.append(f"      ghost:    {g['what']}")
        lines.append(f"      engineer: {g['instead']}")
        lines.append(f"      receipt:  {g['receipt']}")
    return "\n".join(lines)
