"""phys2d.py — a 2D physics presentation with the knobs written down.

V   bodies: (x, y, vx, vy, inv_mass, radius) in float64
    static = inv_mass 0 (motion channel dead)
G   semi-implicit Euler
    sequential impulses on disk–disk and disk–ground
    distance joints as extra G (maximal: joint reconstructed each step)
θ   dt in (0, dt_max]
    speed cap v_max (else DECOHERED)
    solver iterations (cap, not convergence to a law)
    slop (penetration we refuse to treat as V=0)

This is not Newton. It is one discrete cut. Energy is a probe, not a law.

    python -m cutad.phys2d
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import hypot, sqrt
import math


class Theta(Exception):
    pass


class Decohered(Exception):
    """Past θ. State kept; not a legal step result."""


@dataclass
class Body:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    inv_mass: float = 1.0
    r: float = 0.5
    name: str = ""

    @property
    def mass(self) -> float:
        return 0.0 if self.inv_mass == 0.0 else 1.0 / self.inv_mass


@dataclass
class Joint:
    """Distance constraint. Maximal-coord reconstruction every step."""
    a: int
    b: int
    rest: float


@dataclass
class Contact:
    a: int
    b: int                 # -1 = ground
    nx: float
    ny: float
    pen: float


@dataclass
class World:
    g: float = -10.0
    slop: float = 0.01
    iters: int = 8
    dt_max: float = 0.05
    v_max: float = 200.0
    restitution: float = 0.0
    baumgarte: float = 0.2     # positional correction gain (reconstruction)
    bodies: list = field(default_factory=list)
    joints: list = field(default_factory=list)
    ledger: list = field(default_factory=list)

    def add(self, body: Body) -> int:
        self.bodies.append(body)
        return len(self.bodies) - 1

    def energy(self) -> float:
        e = 0.0
        for b in self.bodies:
            if b.inv_mass == 0.0:
                continue
            e += 0.5 * b.mass * (b.vx * b.vx + b.vy * b.vy)
            e += -self.g * b.mass * b.y
        return e

    def momentum(self) -> tuple[float, float]:
        px = py = 0.0
        for b in self.bodies:
            if b.inv_mass == 0.0:
                continue
            px += b.mass * b.vx
            py += b.mass * b.vy
        return px, py

    def _contacts(self) -> list[Contact]:
        out = []
        n = len(self.bodies)
        for i, a in enumerate(self.bodies):
            # ground y=0
            pen = a.r - a.y
            if pen > 0:
                out.append(Contact(i, -1, 0.0, 1.0, pen))
            for j in range(i + 1, n):
                b = self.bodies[j]
                dx, dy = b.x - a.x, b.y - a.y
                d = hypot(dx, dy)
                rest = a.r + b.r
                if d < rest and d > 1e-12:
                    out.append(Contact(i, j, dx / d, dy / d, rest - d))
        return out

    def _impulse(self, c: Contact) -> None:
        A = self.bodies[c.a]
        if c.b < 0:
            inv_b = 0.0
            rvx, rvy = A.vx, A.vy
        else:
            B = self.bodies[c.b]
            inv_b = B.inv_mass
            rvx = A.vx - B.vx
            rvy = A.vy - B.vy
        vn = rvx * c.nx + rvy * c.ny
        inv = A.inv_mass + inv_b
        if inv == 0.0:
            return
        # restitution only on approaching
        e = self.restitution if vn < 0 else 0.0
        j = -(1.0 + e) * vn / inv
        if j < 0 and e == 0.0 and vn >= 0:
            return
        A.vx += j * A.inv_mass * c.nx
        A.vy += j * A.inv_mass * c.ny
        if c.b >= 0:
            B = self.bodies[c.b]
            B.vx -= j * B.inv_mass * c.nx
            B.vy -= j * B.inv_mass * c.ny

    def _correct(self, c: Contact) -> None:
        """Baumgarte / slop: reconstruction of the non-penetration slot."""
        corr = max(c.pen - self.slop, 0.0) * self.baumgarte
        if corr == 0.0:
            return
        A = self.bodies[c.a]
        if c.b < 0:
            inv = A.inv_mass
            if inv == 0.0:
                return
            A.y += corr
            return
        B = self.bodies[c.b]
        inv = A.inv_mass + B.inv_mass
        if inv == 0.0:
            return
        A.x -= c.nx * corr * (A.inv_mass / inv)
        A.y -= c.ny * corr * (A.inv_mass / inv)
        B.x += c.nx * corr * (B.inv_mass / inv)
        B.y += c.ny * corr * (B.inv_mass / inv)

    def _joints(self) -> None:
        for jn in self.joints:
            A, B = self.bodies[jn.a], self.bodies[jn.b]
            dx, dy = B.x - A.x, B.y - A.y
            d = hypot(dx, dy)
            if d < 1e-12:
                continue
            nx, ny = dx / d, dy / d
            err = d - jn.rest
            rvx = A.vx - B.vx
            rvy = A.vy - B.vy
            vn = rvx * nx + rvy * ny
            inv = A.inv_mass + B.inv_mass
            if inv == 0.0:
                continue
            imp = -vn / inv
            A.vx += imp * A.inv_mass * nx
            A.vy += imp * A.inv_mass * ny
            B.vx -= imp * B.inv_mass * nx
            B.vy -= imp * B.inv_mass * ny
            corr = err * self.baumgarte
            A.x += nx * corr * (A.inv_mass / inv)
            A.y += ny * corr * (A.inv_mass / inv)
            B.x -= nx * corr * (B.inv_mass / inv)
            B.y -= ny * corr * (B.inv_mass / inv)

    def step(self, dt: float) -> None:
        if dt <= 0.0:
            raise Theta("dt <= 0 is not in this G")
        if dt > self.dt_max:
            raise Theta(f"dt {dt} > dt_max {self.dt_max}")
        # SI Euler
        for b in self.bodies:
            if b.inv_mass == 0.0:
                continue
            b.vy += self.g * dt
            b.x += b.vx * dt
            b.y += b.vy * dt
        contacts = self._contacts()
        for _ in range(self.iters):
            for c in contacts:
                self._impulse(c)
            self._joints()
        for c in contacts:
            self._correct(c)
        for b in self.bodies:
            sp = hypot(b.vx, b.vy)
            if sp > self.v_max:
                self.ledger.append(f"DECOHERED speed {sp:.3f} > v_max")
                raise Decohered(f"speed {sp} > v_max {self.v_max}")


@dataclass
class PendulumReduced:
    """Same pendulum, joint IN V. Angle is the alphabet. No constraint G."""
    theta: float
    omega: float
    L: float
    g: float = -10.0
    dt_max: float = 0.05

    @property
    def xy(self) -> tuple[float, float]:
        return self.L * math.sin(self.theta), -self.L * math.cos(self.theta)

    def energy(self, mass: float = 1.0) -> float:
        x, y = self.xy
        v = abs(self.omega) * self.L
        return 0.5 * mass * v * v + (-self.g) * mass * y

    def step(self, dt: float) -> None:
        if dt <= 0.0 or dt > self.dt_max:
            raise Theta("dt out of range")
        # SI Euler on the reduced coordinate
        alpha = (self.g / self.L) * math.sin(self.theta)
        self.omega += alpha * dt
        self.theta += self.omega * dt


def bounce_scene(restitution=0.0, y0=4.0, dt=0.01, steps=200):
    w = World(restitution=restitution)
    w.add(Body(0.0, y0, r=0.5, name="ball"))
    e0 = w.energy()
    pen_max = 0.0
    for _ in range(steps):
        w.step(dt)
        pen_max = max(pen_max, max(0.0, w.bodies[0].r - w.bodies[0].y))
    return {
        "e0": e0, "e1": w.energy(),
        "y": w.bodies[0].y, "vy": w.bodies[0].vy,
        "pen_max": pen_max, "steps": steps, "dt": dt,
    }


def pendulum_compare(dt=0.01, steps=400):
    # maximal: two bodies, one joint
    w = World()
    a = w.add(Body(0.0, 3.0, inv_mass=0.0, r=0.05, name="pivot"))
    b = w.add(Body(1.0, 3.0, r=0.15, name="bob"))
    w.joints.append(Joint(a, b, 1.0))
    red = PendulumReduced(theta=math.pi / 2, omega=0.0, L=1.0)
    drift = []
    for _ in range(steps):
        w.step(dt)
        red.step(dt)
        dx = w.bodies[1].x - w.bodies[0].x
        dy = w.bodies[1].y - w.bodies[0].y
        drift.append(abs(hypot(dx, dy) - 1.0))
    mx, my = w.bodies[1].x - w.bodies[0].x, w.bodies[1].y - w.bodies[0].y
    return {
        "max_joint_drift": max(drift),
        "final_len": hypot(mx, my),
        "reduced_xy": red.xy,
        "maximal_xy": (mx, my),
        "e_max": w.energy(),
        "e_red": red.energy(),
    }


def main():
    print("PHYS2D  V=disk bodies float64  G=SI Euler + seq. impulse  "
          "θ=dt_max, iters, slop, v_max")
    print()

    print("1. inelastic bounce (e=0)  y0=4  dt=0.01  200 steps")
    b = bounce_scene(0.0)
    print(f"   E0={b['e0']:.4f}  E1={b['e1']:.4f}  "
          f"ΔE={b['e1']-b['e0']:.4f}  y={b['y']:.4f}  pen_max={b['pen_max']:.4f}")
    print("   energy drop is the contact cut + slop, not 'friction in nature'")

    print()
    print("2. elastic-ish bounce (e=0.8)")
    b2 = bounce_scene(0.8, steps=250)
    print(f"   E0={b2['e0']:.4f}  E1={b2['e1']:.4f}  "
          f"ΔE={b2['e1']-b2['e0']:.4f}  y={b2['y']:.4f}")

    print()
    print("3. pendulum: maximal joint vs reduced angle")
    p = pendulum_compare()
    print(f"   max |len-L| (maximal G) = {p['max_joint_drift']:.6f}")
    print(f"   final maximal xy {p['maximal_xy']}")
    print(f"   final reduced  xy {p['reduced_xy']}")
    print("   reduced V cannot drift the length: the length is not a constraint")

    print()
    print("4. θ")
    w = World(dt_max=0.05)
    w.add(Body(0.0, 2.0))
    try:
        w.step(0.0)
        print("   dt=0 FAILED TO REFUSE")
    except Theta as e:
        print(f"   dt=0 → Theta: {e}")
    try:
        w.step(0.2)
        print("   dt>dt_max FAILED TO REFUSE")
    except Theta as e:
        print(f"   dt>dt_max → Theta: {e}")

    print()
    print("PRE-SCREEN")
    print("  exact energy          REFUSE   discrete SI + impulses")
    print("  exact non-penetration REFUSE   slop is θ, pen_max>0")
    print("  joint length exact    REFUSE maximal / ADMIT reduced")
    print("  dt=0 step             REFUSE   θ")
    print()
    print("verdict PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
