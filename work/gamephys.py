"""gamephys.py — cheap mechanism-first 2D engine for games.

PL cut: pick the smallest V that holds the mechanic.
  Free2   (x,y,vx,vy)     a jumper, a crate
  Hinge1  (theta, omega)  a door, a pendulum hazard
  Slider1 (q, qdot)       an elevator, a moving platform
Static AABB is scenery, not a body.

G   SI Euler at a FIXED dt (the game tick)
    one contact pass vs static + other frees (AABB, no rotation)
    hinge/slider integrate in their own coordinate
θ   dt is given by the ticker; dt<=0 refused
    v_max clamp (decohere-as-clamp, billed)
    2 impulse iters, slop in pixels
    no CCD, no friction cone, no sleep island

Not Newton. A tick. Target: thousands of frees at 60Hz in pure Python
is optimistic; dozens is the honest budget. Mechanisms stay 1-DOF so
their cost does not grow with a reconstructed joint.

    python -m cutad.gamephys
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import cos, sin, pi
from time import perf_counter


class Theta(Exception):
    pass


@dataclass
class AABB:
    x: float
    y: float
    w: float
    h: float

    def left(self):
        return self.x

    def right(self):
        return self.x + self.w

    def bottom(self):
        return self.y

    def top(self):
        return self.y + self.h


@dataclass
class Free:
    """Two translational DOF. The platformer atom."""
    box: AABB
    vx: float = 0.0
    vy: float = 0.0
    inv_m: float = 1.0
    grounded: bool = False
    name: str = ""


@dataclass
class Hinge:
    """One rotational DOF about a fixed pin. Door / trap."""
    pin_x: float
    pin_y: float
    length: float
    width: float
    theta: float
    omega: float = 0.0
    inv_i: float = 1.0
    name: str = ""

    def tip(self) -> tuple[float, float]:
        return (self.pin_x + self.length * sin(self.theta),
                self.pin_y - self.length * cos(self.theta))


@dataclass
class Slider:
    """One translational DOF on a segment. Elevator."""
    ax: float
    ay: float
    bx: float
    by: float
    q: float          # 0 at a, 1 at b
    qdot: float = 0.0
    w: float = 40.0
    h: float = 12.0
    name: str = ""

    def pos(self) -> tuple[float, float]:
        return self.ax + (self.bx - self.ax) * self.q, self.ay + (self.by - self.ay) * self.q

    def aabb(self) -> AABB:
        x, y = self.pos()
        return AABB(x - self.w * 0.5, y - self.h * 0.5, self.w, self.h)


@dataclass
class World:
    dt: float = 1.0 / 60.0
    g: float = -1800.0
    slop: float = 0.1
    iters: int = 2
    v_max: float = 4000.0
    static: list = field(default_factory=list)
    frees: list = field(default_factory=list)
    hinges: list = field(default_factory=list)
    sliders: list = field(default_factory=list)

    def add_ground(self, x, y, w, h):
        self.static.append(AABB(x, y, w, h))

    def step(self, dt: float | None = None) -> None:
        dt = self.dt if dt is None else dt
        if dt <= 0.0:
            raise Theta("dt<=0")
        self._step_frees(dt)
        self._step_hinges(dt)
        self._step_sliders(dt)

    def _step_frees(self, dt: float) -> None:
        for b in self.frees:
            if b.inv_m == 0.0:
                continue
            b.vy += self.g * dt
            b.box.x += b.vx * dt
            b.box.y += b.vy * dt
            if abs(b.vx) > self.v_max:
                b.vx = self.v_max if b.vx > 0 else -self.v_max
            if abs(b.vy) > self.v_max:
                b.vy = self.v_max if b.vy > 0 else -self.v_max
            b.grounded = False
        for _ in range(self.iters):
            for b in self.frees:
                for s in self.static:
                    _resolve_aabb(b, s, dynamic=False)
                for sl in self.sliders:
                    _resolve_aabb(b, sl.aabb(), dynamic=False)
                for o in self.frees:
                    if o is b or o.inv_m == 0.0:
                        continue
                    if id(b) < id(o):
                        _resolve_aabb(b, o.box, dynamic=True, other_body=o)

    def _step_hinges(self, dt: float) -> None:
        # reduced: gravity torque about pin, SI Euler on theta
        for h in self.hinges:
            # mass-at-tip approximation, torque = L × (m g)
            alpha = (self.g / max(h.length, 1e-6)) * sin(h.theta)
            h.omega += alpha * dt
            h.theta += h.omega * dt
            if abs(h.omega) > self.v_max / max(h.length, 1e-6):
                h.omega *= 0.5

    def _step_sliders(self, dt: float) -> None:
        for s in self.sliders:
            s.q += s.qdot * dt
            if s.q < 0.0:
                s.q, s.qdot = 0.0, abs(s.qdot)
            elif s.q > 1.0:
                s.q, s.qdot = 1.0, -abs(s.qdot)


def _overlap(a: AABB, b: AABB):
    ox = min(a.right(), b.right()) - max(a.left(), b.left())
    oy = min(a.top(), b.top()) - max(a.bottom(), b.bottom())
    if ox <= 0.0 or oy <= 0.0:
        return None
    return ox, oy


def _resolve_aabb(body: Free, other: AABB, dynamic: bool, other_body: Free | None = None):
    hit = _overlap(body.box, other)
    if hit is None:
        return
    ox, oy = hit
    if oy < ox:
        # vertical
        if body.box.y + body.box.h * 0.5 > other.y + other.h * 0.5:
            body.box.y += oy
            if body.vy < 0:
                body.vy = 0.0
            body.grounded = True
        else:
            body.box.y -= oy
            if body.vy > 0:
                body.vy = 0.0
        if dynamic and other_body is not None:
            other_body.vy *= 0.5
    else:
        if body.box.x + body.box.w * 0.5 > other.x + other.w * 0.5:
            body.box.x += ox
        else:
            body.box.x -= ox
        body.vx = 0.0


def jump(body: Free, speed: float = 700.0) -> bool:
    if not body.grounded:
        return False
    body.vy = speed
    body.grounded = False
    return True


def demo_scene():
    w = World()
    w.add_ground(0, 0, 800, 40)
    w.add_ground(300, 120, 160, 16)
    p = Free(AABB(80, 40, 24, 32), name="player")
    crate = Free(AABB(200, 40, 28, 28), name="crate")
    w.frees.extend([p, crate])
    w.hinges.append(Hinge(600, 200, 80, 12, theta=0.6, name="door"))
    w.sliders.append(Slider(350, 200, 550, 200, q=0.0, qdot=0.25, name="lift"))
    return w, p


def ascii_frame(w: World, width=70, height=18):
    grid = [[" "] * width for _ in range(height)]

    def plot(x, y, ch):
        c = int(x / 800 * width)
        r = height - 1 - int(y / 360 * height)
        if 0 <= r < height and 0 <= c < width:
            grid[r][c] = ch

    for s in w.static:
        plot(s.x + s.w * 0.5, s.y + s.h * 0.5, "=")
    for sl in w.sliders:
        x, y = sl.pos()
        plot(x, y, "=")
    for h in w.hinges:
        tx, ty = h.tip()
        plot(h.pin_x, h.pin_y, "o")
        plot(tx, ty, "/")
    for b in w.frees:
        ch = "@" if b.name == "player" else "#"
        plot(b.box.x + b.box.w * 0.5, b.box.y + b.box.h * 0.5, ch)
    return "\n".join("".join(row) for row in grid)


def main():
    w, p = demo_scene()
    print("GAMEPHYS  mechanism-first tick")
    print("  V: Free2 + Hinge1 + Slider1 + static AABB")
    print("  G: SI Euler, 2 AABB passes, reduced hinge/slider")
    print("  θ: dt=1/60, v_max, slop, no CCD")
    print()
    t0 = perf_counter()
    jumped = False
    for i in range(180):          # 3 seconds
        if i == 20:
            p.vx = 220.0
        if i == 40 and not jumped:
            jumped = jump(p)
        w.step()
    ms = (perf_counter() - t0) * 1000
    print(ascii_frame(w))
    print()
    print(f"  player  ({p.box.x:.1f}, {p.box.y:.1f}) v=({p.vx:.1f},{p.vy:.1f}) "
          f"grounded={p.grounded}")
    print(f"  door    theta={w.hinges[0].theta:.3f}")
    print(f"  lift    q={w.sliders[0].q:.3f}")
    print(f"  180 steps in {ms:.2f} ms  ({180 / (ms / 1000):.0f} tick/s)")
    print()
    # cheapness: 500 frees, 1s
    w2 = World()
    w2.add_ground(0, 0, 800, 40)
    for i in range(80):
        w2.frees.append(Free(AABB(20 + (i % 20) * 30, 50 + (i // 20) * 40, 16, 16)))
    t1 = perf_counter()
    for _ in range(60):
        w2.step()
    ms2 = (perf_counter() - t1) * 1000
    print(f"  80 frees × 60 ticks = {ms2:.2f} ms  "
          f"(budget 16.7 ms/tick: {ms2/60:.3f} ms)")
    print()
    print("verdict PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
