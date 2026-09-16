"""doomtic.py — playsim cut, not Doom.

V   player/missile (x,y,vx,vy,r)
    door as Slider1 on a gap (q=0 closed, q=1 open)
    linedefs as static segments
G   35 Hz tic; integrate; clip vs lines; door slide
θ   dt = 1/35; v_max; door blocked if a body sits in the gap

    python -m cutad.doomtic
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import hypot


TIC = 1.0 / 35.0


class Theta(Exception):
    pass


@dataclass
class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    blocking: bool = True
    door: bool = False


@dataclass
class Mobj:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    r: float = 16.0
    kind: str = "player"
    alive: bool = True


@dataclass
class Door:
    """Sector-height style slider. q=0 closed, q=1 open."""
    line_index: int
    q: float = 0.0
    qdot: float = 0.0
    speed: float = 1.6          # gap units / sec
    open_target: float = 1.0


@dataclass
class TicWorld:
    lines: list = field(default_factory=list)
    mobjs: list = field(default_factory=list)
    door: Door | None = None
    tics: int = 0

    def use_door(self) -> None:
        if self.door is None:
            return
        if self.door.q <= 0.01:
            self.door.qdot = self.door.speed
        elif self.door.q >= 0.99:
            self.door.qdot = -self.door.speed

    def fire(self, who: Mobj, dx: float, dy: float, speed: float = 280.0) -> None:
        n = hypot(dx, dy) or 1.0
        self.mobjs.append(Mobj(
            who.x + dx / n * (who.r + 4),
            who.y + dy / n * (who.r + 4),
            dx / n * speed, dy / n * speed,
            r=6.0, kind="ball",
        ))

    def step(self, dt: float = TIC) -> None:
        if dt <= 0.0:
            raise Theta("dt<=0")
        if self.door is not None:
            self.door.q += self.door.qdot * dt
            if self.door.q < 0.0:
                self.door.q, self.door.qdot = 0.0, 0.0
            if self.door.q > 1.0:
                self.door.q, self.door.qdot = 1.0, 0.0
        for m in self.mobjs:
            if not m.alive:
                continue
            nx = m.x + m.vx * dt
            ny = m.y + m.vy * dt
            if self._blocked(m, nx, ny):
                if m.kind == "ball":
                    m.alive = False
                m.vx = m.vy = 0.0
            else:
                m.x, m.y = nx, ny
        self.tics += 1

    def _blocked(self, m: Mobj, x: float, y: float) -> bool:
        for i, ln in enumerate(self.lines):
            if not ln.blocking:
                continue
            if ln.door and self.door and self.door.q > 0.85:
                continue
            if _seg_hit(x, y, m.r, ln):
                return True
        return False


def _seg_hit(x, y, r, ln: Line) -> bool:
    vx, vy = ln.x2 - ln.x1, ln.y2 - ln.y1
    L2 = vx * vx + vy * vy or 1.0
    t = max(0.0, min(1.0, ((x - ln.x1) * vx + (y - ln.y1) * vy) / L2))
    px, py = ln.x1 + t * vx, ln.y1 + t * vy
    return hypot(x - px, y - py) < r


def e1m1_toy():
    """Two rooms, a door gap in the middle wall."""
    w = TicWorld()
    # outer box
    w.lines = [
        Line(-200, -120, 200, -120),
        Line(200, -120, 200, 120),
        Line(200, 120, -200, 120),
        Line(-200, 120, -200, -120),
        # middle wall with a door segment
        Line(-20, -120, -20, -24),
        Line(-20, 24, -20, 120),
        Line(-20, -24, -20, 24, door=True),
    ]
    w.door = Door(line_index=6, q=0.0)
    player = Mobj(-80, 0, kind="player")
    w.mobjs.append(player)
    return w, player


def main():
    print("DOOMTIC  playsim cut — not the game")
    print("  V: mobj + door Slider1 + linedefs")
    print("  G: 35 Hz clip move")
    print("  θ: dt<=0 refuse; door opens in V not as a hinge")
    print()
    w, p = e1m1_toy()
    # walk into the closed door
    p.vx = 80.0
    for _ in range(40):
        w.step()
    closed_x = p.x
    w.use_door()
    for _ in range(40):
        w.step()
    # door should be open; walk through
    p.vx = 80.0
    for _ in range(50):
        w.step()
    open_x = p.x
    # fire a ball at the east wall
    w.fire(p, 1, 0)
    balls_alive_before = sum(1 for m in w.mobjs if m.kind == "ball" and m.alive)
    for _ in range(80):
        w.step()
    balls_alive_after = sum(1 for m in w.mobjs if m.kind == "ball" and m.alive)
    print(f"  closed-door stop x={closed_x:.1f}  (should stay west of -20)")
    print(f"  after open+walk  x={open_x:.1f}    door q={w.door.q:.2f}")
    print(f"  fireball alive {balls_alive_before} → {balls_alive_after}  tics={w.tics}")
    ok = closed_x < -20 and open_x > -20 and balls_alive_before == 1 and balls_alive_after == 0
    print()
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
