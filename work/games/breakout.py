"""Breakout — Pong plus a finite brick set that leaves V.

V_game  ball, one slider, bricks[], score, tic
G_tic   bounce on walls/paddle/brick; brick removed on hit
θ       dt=1/60; empty bricks designated win; ball below floor lose

    python -m cutad.games.breakout
"""
from __future__ import annotations

from dataclasses import dataclass, field


class Theta(Exception):
    pass


W, H = 80.0, 40.0
DT = 1.0 / 60.0
PADDLE_W, PADDLE_Y = 12.0, 3.0
BRICK_W, BRICK_H = 8.0, 2.0


@dataclass
class Brick:
    x: float
    y: float
    alive: bool = True


@dataclass
class Breakout:
    ball_x: float = W / 2
    ball_y: float = 8.0
    ball_vx: float = 22.0
    ball_vy: float = 28.0
    pad_x: float = W / 2
    bricks: list = field(default_factory=list)
    score: int = 0
    tics: int = 0
    lives: int = 3

    def __post_init__(self):
        if not self.bricks:
            self.bricks = [
                Brick(6 + col * (BRICK_W + 1), 28 + row * (BRICK_H + 1))
                for row in range(4) for col in range(8)
            ]

    def designated(self) -> str | None:
        if all(not b.alive for b in self.bricks):
            return "win"
        if self.lives <= 0:
            return "lose"
        return None

    def hash(self) -> tuple:
        alive = tuple(i for i, b in enumerate(self.bricks) if b.alive)
        return (round(self.ball_x, 3), round(self.ball_y, 3),
                round(self.pad_x, 3), alive, self.score, self.lives, self.tics)

    def step(self, move: int = 0, dt: float = DT) -> None:
        if dt <= 0.0:
            raise Theta("dt<=0")
        if self.designated():
            return
        self.pad_x = min(W - PADDLE_W / 2, max(PADDLE_W / 2, self.pad_x + move * 50 * dt))
        self.ball_x += self.ball_vx * dt
        self.ball_y += self.ball_vy * dt
        if self.ball_x < 1:
            self.ball_x, self.ball_vx = 1, abs(self.ball_vx)
        if self.ball_x > W - 1:
            self.ball_x, self.ball_vx = W - 1, -abs(self.ball_vx)
        if self.ball_y > H - 1:
            self.ball_y, self.ball_vy = H - 1, -abs(self.ball_vy)
        if (abs(self.ball_y - PADDLE_Y) < 1.2
                and abs(self.ball_x - self.pad_x) < PADDLE_W / 2 + 0.6
                and self.ball_vy < 0):
            self.ball_y = PADDLE_Y + 1.2
            self.ball_vy = abs(self.ball_vy)
            self.ball_vx += (self.ball_x - self.pad_x) * 2
        for b in self.bricks:
            if not b.alive:
                continue
            if (b.x <= self.ball_x <= b.x + BRICK_W
                    and b.y <= self.ball_y <= b.y + BRICK_H):
                b.alive = False
                self.ball_vy *= -1
                self.score += 1
                break
        if self.ball_y < 0:
            self.lives -= 1
            self.ball_x, self.ball_y = self.pad_x, 8.0
            self.ball_vx, self.ball_vy = 22.0, 28.0
        self.tics += 1


def main():
    print("BREAKOUT  V=ball+slider+bricks  G=hit leaves V  θ=win empty / lose lives")
    g = Breakout()
    n0 = sum(1 for b in g.bricks if b.alive)
    for _ in range(400):
        mv = 1 if g.ball_x > g.pad_x + 1 else -1 if g.ball_x < g.pad_x - 1 else 0
        g.step(mv)
    n1 = sum(1 for b in g.bricks if b.alive)
    g2 = Breakout()
    for _ in range(400):
        mv = 1 if g2.ball_x > g2.pad_x + 1 else -1 if g2.ball_x < g2.pad_x - 1 else 0
        g2.step(mv)
    print(f"  bricks {n0} → {n1}  score={g.score}  lives={g.lives}  tics={g.tics}")
    print(f"  hash match {g.hash() == g2.hash()}")
    print(f"  designated {g.designated()}")
    ok = n1 < n0 and g.hash() == g2.hash()
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
