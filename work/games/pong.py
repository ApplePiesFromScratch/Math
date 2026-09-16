"""Pong — 1972 playsim replica.

V_game  ball (x,y,vx,vy), paddle y × 2, score L/R, serve flag, tic
V_in    {up, down, none} per side this tick
G_tic   SI Euler, wall bounce, paddle english, miss → score + serve
θ       court bounds; paddle clamp; dt=1/60; first-to-N designated

View (ASCII) reads V_game and must not write it.

    python -m cutad.games.pong
"""
from __future__ import annotations

from dataclasses import dataclass


class Theta(Exception):
    pass


W, H = 80.0, 40.0
PADDLE_H = 8.0
PADDLE_X_L = 2.0
PADDLE_X_R = 78.0
BALL_R = 0.6
PADDLE_SPEED = 48.0
BALL_SPEED = 36.0
DT = 1.0 / 60.0
WIN = 11


@dataclass
class PongInput:
    left: int = 0    # -1 down, 0 none, +1 up
    right: int = 0


@dataclass
class Pong:
    ball_x: float = W / 2
    ball_y: float = H / 2
    ball_vx: float = BALL_SPEED
    ball_vy: float = BALL_SPEED * 0.3
    pad_l: float = H / 2
    pad_r: float = H / 2
    score_l: int = 0
    score_r: int = 0
    tics: int = 0
    serving: bool = False

    def designated(self) -> str | None:
        if self.score_l >= WIN:
            return "left"
        if self.score_r >= WIN:
            return "right"
        return None

    def hash(self) -> tuple:
        return (
            round(self.ball_x, 4), round(self.ball_y, 4),
            round(self.ball_vx, 4), round(self.ball_vy, 4),
            round(self.pad_l, 4), round(self.pad_r, 4),
            self.score_l, self.score_r, self.tics,
        )

    def step(self, inp: PongInput, dt: float = DT) -> None:
        if dt <= 0.0:
            raise Theta("dt<=0")
        if self.designated():
            return
        self.pad_l = _clamp(self.pad_l + inp.left * PADDLE_SPEED * dt)
        self.pad_r = _clamp(self.pad_r + inp.right * PADDLE_SPEED * dt)
        self.ball_x += self.ball_vx * dt
        self.ball_y += self.ball_vy * dt
        if self.ball_y < BALL_R:
            self.ball_y = BALL_R
            self.ball_vy = abs(self.ball_vy)
        elif self.ball_y > H - BALL_R:
            self.ball_y = H - BALL_R
            self.ball_vy = -abs(self.ball_vy)
        self._paddles()
        if self.ball_x < 0.0:
            self.score_r += 1
            self._serve(+1)
        elif self.ball_x > W:
            self.score_l += 1
            self._serve(-1)
        self.tics += 1

    def _paddles(self) -> None:
        if self.ball_vx < 0 and abs(self.ball_x - PADDLE_X_L) <= 1.2:
            if abs(self.ball_y - self.pad_l) <= PADDLE_H / 2 + BALL_R:
                self.ball_x = PADDLE_X_L + 1.2
                self.ball_vx = abs(self.ball_vx) * 1.05
                off = (self.ball_y - self.pad_l) / (PADDLE_H / 2)
                self.ball_vy = off * BALL_SPEED
        elif self.ball_vx > 0 and abs(self.ball_x - PADDLE_X_R) <= 1.2:
            if abs(self.ball_y - self.pad_r) <= PADDLE_H / 2 + BALL_R:
                self.ball_x = PADDLE_X_R - 1.2
                self.ball_vx = -abs(self.ball_vx) * 1.05
                off = (self.ball_y - self.pad_r) / (PADDLE_H / 2)
                self.ball_vy = off * BALL_SPEED

    def _serve(self, direction: int) -> None:
        self.ball_x = W / 2
        self.ball_y = H / 2
        self.ball_vx = BALL_SPEED * direction
        self.ball_vy = BALL_SPEED * 0.25 * direction


def _clamp(y: float) -> float:
    lo = PADDLE_H / 2
    hi = H - PADDLE_H / 2
    return lo if y < lo else hi if y > hi else y


def ai_right(g: Pong) -> int:
    if g.ball_y > g.pad_r + 1:
        return 1
    if g.ball_y < g.pad_r - 1:
        return -1
    return 0


def draw(g: Pong) -> str:
    cols, rows = 41, 21
    grid = [[" "] * cols for _ in range(rows)]

    def cell(x, y):
        c = int(x / W * (cols - 1))
        r = rows - 1 - int(y / H * (rows - 1))
        return r, c

    for r in range(rows):
        mid = cols // 2
        grid[r][mid] = "·"
    for name, y, colx in (("L", g.pad_l, PADDLE_X_L), ("R", g.pad_r, PADDLE_X_R)):
        r0, c = cell(colx, y)
        half = max(1, int(PADDLE_H / H * rows / 2))
        for dr in range(-half, half + 1):
            rr = r0 + dr
            if 0 <= rr < rows:
                grid[rr][c] = "|"
    br, bc = cell(g.ball_x, g.ball_y)
    if 0 <= br < rows and 0 <= bc < cols:
        grid[br][bc] = "o"
    board = "\n".join("".join(row) for row in grid)
    win = g.designated()
    tail = f"  {g.score_l}  -  {g.score_r}   tic {g.tics}"
    if win:
        tail += f"   WIN {win}"
    return board + "\n" + tail


def rally_demo(n=240):
    """Left AI tracks too; deterministic probe."""
    g = Pong()
    h0 = g.hash()
    for _ in range(n):
        inp = PongInput(left=ai_right(g) if False else _ai_left(g),
                        right=ai_right(g))
        g.step(inp)
    return g, h0


def _ai_left(g: Pong) -> int:
    if g.ball_y > g.pad_l + 1:
        return 1
    if g.ball_y < g.pad_l - 1:
        return -1
    return 0


def main():
    print("PONG  V=ball+2 sliders+score  G=60Hz bounce  θ=court, first-to-11")
    print()
    g, h0 = rally_demo(180)
    print(draw(g))
    g2 = Pong()
    for _ in range(180):
        g2.step(PongInput(left=_ai_left(g2), right=ai_right(g2)))
    print()
    print(f"  demo hash match (same AI inputs): {g.hash() == g2.hash()}")
    print(f"  start hash {h0} → not equal after play: {h0 != g.hash()}")
    # miss probe: park right paddle away, shoot right
    miss = Pong(ball_x=70, ball_y=20, ball_vx=40, ball_vy=0, pad_r=4)
    before = miss.score_l
    for _ in range(40):
        miss.step(PongInput())
    scored = miss.score_l == before + 1
    print(f"  miss awards left: {scored}  score {miss.score_l}-{miss.score_r}")
    try:
        Pong().step(PongInput(), dt=0.0)
        theta_ok = False
    except Theta:
        theta_ok = True
    print(f"  θ dt=0: {theta_ok}")
    ok = g.hash() == g2.hash() and scored and theta_ok
    print()
    print("verdict", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
