"""All computable G-combinations that close on a listed V."""
from __future__ import annotations

from itertools import product

from engineer.ops import POOL, parse_V


def closes(V, spec):
    arity, fn = spec
    for args in product(V, repeat=arity):
        try:
            r = fn(*args)
        except Exception:
            return False
        if r not in V:
            return False
    return True


def lem(V, OR, NOT, designated):
    _, orf = OR
    _, nf = NOT
    return all(orf(v, nf(v)) in designated for v in V)


def lnc(V, AND, NOT):
    _, af = AND
    _, nf = NOT
    return all(af(v, nf(v)) == 0 for v in V)


def idem(V, AND):
    _, af = AND
    return all(af(v, v) == v for v in V)


def enumerate_cuts(V_spec="0,1/2,1", designated="1"):
    V = parse_V(V_spec)
    des = parse_V(designated)
    nots = [n for n, s in POOL.items() if s[0] == 1]
    ands = [n for n in POOL if n.startswith("AND_")]
    ors = [n for n in POOL if n.startswith("OR_")]
    rows = []
    for n, a, o in product(nots, ands, ors):
        g = [n, a, o]
        closing = all(closes(V, POOL[name]) for name in g)
        if not closing:
            rows.append({
                "G": g, "closes": False,
                "LEM": None, "LNC": None, "idem": None,
                "why": "an op leaves V",
            })
            continue
        rows.append({
            "G": g, "closes": True,
            "LEM": lem(V, POOL[o], POOL[n], des),
            "LNC": lnc(V, POOL[a], POOL[n]),
            "idem": idem(V, POOL[a]),
            "why": "",
        })
    return V, rows


def report(V_spec="0,1/2,1"):
    V, rows = enumerate_cuts(V_spec)
    close = [r for r in rows if r["closes"]]
    leave = [r for r in rows if not r["closes"]]
    lines = [
        f"ENUMERATION  V={list(map(str, V))}  "
        f"candidate G-triples={len(rows)}  close={len(close)}  leave={len(leave)}",
    ]
    lines.append(f"  {'G':<36} {'close':<6} LEM  LNC  idem")
    for r in rows:
        g = "+".join(r["G"])
        if r["closes"]:
            lines.append(
                f"  {g:<36} {'yes':<6} "
                f"{'Y' if r['LEM'] else 'n':<4} "
                f"{'Y' if r['LNC'] else 'n':<4} "
                f"{'Y' if r['idem'] else 'n'}"
            )
        else:
            lines.append(f"  {g:<36} {'NO':<6} —    —    —     {r['why']}")
    return "\n".join(lines), rows
