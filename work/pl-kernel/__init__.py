"""Propagation Logic v0.3 — presentations, not terrain.

P / G → Q

V, G, θ are the knobs. isolate is unpriced. Guards and μ are not.
"""
from pl.reading import LeavesV, Reading, Theta, isolate, rate, relate
from pl.certify import Certificate, certify, finite_difference, tier
from pl.migrate import (
    ChannelPreservationError,
    Decohered,
    Ledger,
    Runtime,
    V2,
    V3,
    QPAIR,
)

__all__ = [
    "Certificate",
    "ChannelPreservationError",
    "Decohered",
    "LeavesV",
    "Ledger",
    "QPAIR",
    "Reading",
    "Runtime",
    "Theta",
    "V2",
    "V3",
    "certify",
    "finite_difference",
    "isolate",
    "rate",
    "relate",
    "tier",
]
__version__ = "0.3.0"
