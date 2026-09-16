# Propagation Logic

One operator. Three knobs. Many presentations.

```
P / G → Q
```

You pick a value alphabet **V**, a family of operations **G**, and a
coherence bound **θ**. The slash is isolation: Q is what you get when
you read P under G. Change a knob and the forced laws change. That is
the whole model.

This site is a map of those cuts. It is not a claim that the universe
is a carrier, or that logic and gravity are “the same thing.” A name
introduces structure. It does not uncover essence.

It is also not a pencil. One replica (exact-Q pairs, first channel)
is a small V. The *model* is the knobs: they map existing formal
systems and they generate new ones. Waving the generator off because
one replica is small is the geocentrist move — scoring a new isolation
as a trick inside the old alphabet. `python -m pl.forge` emits CL2,
L3, K3, a product cut that leaves V3, and a four-value cut that was
not in the museum. Same forger. Knobs in, table out.

---

## The three knobs

| knob | question | when it refuses |
|---|---|---|
| **V** | What values may appear? | input not in the alphabet |
| **G** | What may be done to them? | the map’s image leaves V |
| **θ** | What counts as accepted, and what happens otherwise? | guard, budget, designated set, live-channel test |

If a sentence cannot name all three, it is not a claim yet.

Two presentations that agree on a small V are not one operator. Grow V
and look for a split. A label that changes no knob is a comment. Work
that happened and does not appear on the ledger is an accounting
failure.

---

## The model in one page

1. State a presentation: V, G, θ.
2. Run the maps. If an output leaves V, do not append a point. Fire θ
   or run a **registered** migration μ: V_old → V_new.
3. Every claim names a falsifier and a cut. Tier is computed
   (FORCED-on-cut, EMPIRICAL, DEFER, UNPAID). It is not authored.
4. Guards, reconfiguration, and μ cost the same book as a step.
   isolate (paying the first cut) is the floor and stays unpriced.
   Growing V mid-run is not free.

That is enough to read every example below. Each example is a
different presentation of the same slash.

---

## Example 1 — Classical bits (CL2)

```
V = {0, 1}
G = NOT v = 1−v;  AND = min;  OR = max
θ = designated {1}
```

On this alphabet AND-as-min and AND-as-product **agree**. LEM holds:
OR(v, NOT v) = 1 for both bits. The Liar has no home: no v with
NOT(v) = v.

This is not “what truth is.” It is what this cut forces.

---

## Example 2 — Two three-valued cuts (L3 vs K3)

Same V, different G. That is the lesson.

```
V = {0, ½, 1}          both
θ = designated {1}     both
```

| | L3 | K3 |
|---|---|---|
| AND | max(0, a+b−1) | min |
| OR | min(1, a+b) | max |
| AND(½,½) | 0 | ½ |
| OR(½, NOT ½) | 1 | ½ |
| LEM | holds | fails |

Call them both “three-valued logic” and you have a comment. Grow
nothing: they already split. Product-AND on the same V yields
½×½ = ¼, which is **not in V**. That op is not in G unless you
change the alphabet (and pay μ).

---

## Example 3 — Rate as a ratio (process calculus)

```
V = pairs (v, r) with v, r exact rationals
G = Leibniz mix;  rate(P, G) = P.r / G.r
θ = G.r ≠ 0 to form a rate;  divisor.v ≠ 0 to divide
```

There is no independent variable with a life of its own. Isolation is
the second argument.

At x = 3, seed 1: `x*x` is `(9, 6)`, rate = 6.  
Change the seed to 2: `(9, 12)`, rate = 6.  
Seed ½: `(9, 3)`, rate = 6.

Same mix, other presentation: lock the seed at 1 and collapse r to a
value (unary D). The number 6 agrees. The channel is gone.

Finite difference of x² is 6+h. It never equals 6 on a listed h. That
op reconstructs a slot this V already carries.

0/0 as *values* refuses divide. 0/0 as *live channels*
`rate((0,6),(0,1))` is 6.

A certificate on the grid `values={±1..±4}, seeds={1,2,½,−1}` for
`z ↦ z²` reports value 6, 32/32, FORCED-on-cut, with a falsifier:
exhibit a seed that changes the rate.

**This replica's V** is exact Q and one channel. Plus, times, divide,
chain, inverse live here. Floats, roots, negative powers, and a
second derivative are other presentations (other V, paid μ). That is
the scope of *this setting*, not the scope of the model. The model
forges settings.

---

## Example 4 — Sky maps (geo / helio)

Angular-only geocentrism plus “add a circle” is complete on the
circle. That carrier cannot fail. Distance is the grown V.

| presentation | G | receipt |
|---|---|---|
| one circle about Earth | uniform angle | large longitude error; distance constant (the lie that closed V) |
| deferent + sun-locked epicycle | add paths | retrogrades appear; radius still leaves V |
| same two circles, renamed “Tycho” | comment | **identical table** |
| `rate(Mars_geo, Sun_geo)` | binary isolation | heliocentric kinematics of two already-paid channels |
| Mars e on that rate | entity on the leftover slot | ~25° → ~3.8° |
| Copernican 2M epicycle | extra circle | a little longitude, **worse** radius |
| equation of center + stretch | warp the angle slot and the radial slot | both gates close; no second circle |

The epicycle was Fourier-by-hand of an angle warp. Naming `G_center`
and `G_stretch` is two ops on two slots. They are not interchangeable:
center alone closes angle and leaves radius; stretch alone does the
reverse.

---

## Example 5 — Physics engines

“Newton” is the advertisement. Integrator, contact, and coordinates
are G.

```
V0   rigid poses, or reduced joint coordinates
G0   unconstrained step + project onto contacts
θ0   dt_max, iteration cap, penetration slop
```

Semi-implicit Euler vs RK4 are two time-G’s. Maximal coordinates
reconstruct joints every step (drift). Reduced coordinates *are* the
joint. Hard contact claims non-penetration as V and spends slop (θ
dressed as V). Soft contact puts penetration in V as a spring. PBD
throws the force slot away. “Just use a smaller dt” is putting ∞ in V.

Pre-screen: exact energy on any listed discrete engine — REFUSE.
Exact joint length — ADMIT on reduced, REFUSE on maximal.

---

## Example 6 — The video-game carrier

A game is not the pixels.

```
V_game   official state the rules may mention
G_tic    (V_game, V_in) → V_game     at a declared tick
θ_game   legal poses, tick budget, designated win/dead
```

A demo hash is the certificate. If a layer must run for the hash to
match, that layer was in the game.

| era | V added | note |
|---|---|---|
| Pong (1972) | ball + two sliders + score | paddles are Slider1, not rigid bodies |
| Breakout (1976) | bricks that **leave** V | empty set designated win |
| Pac-Man (1980) | a **graph**, not a plane | first popular wrong-alphabet cut |
| Doom-class (1993) | linedefs + sector-height sliders | a door is already Slider1; do not upgrade it to PhysX |

Renderer, audio, window size are other carriers. If `G_draw` writes
`V_game` (GPU ragdoll as official pose), you merged cuts and demos
die. Frame ≠ tic.

---

## Example 7 — Migration and the ledger

When V changes mid-run, state does not teleport.

```
V2 {0,1}  --μ embed-->  V3 {0,½,1}  --μ open dead r-->  (v, r=0)
```

A live channel `(v, r≠0)` has no slot in V3. That is
`ChannelPreservationError`, not a silent drop.

Costs on the **same** ledger as a step (stipulated, not derived):

| kind | price |
|---|---|
| STEP | 1 |
| GUARD | 1/4 (even when it passes) |
| RECONFIG | 2 |
| MIGRATE | per map |
| REIFY | 1 |

Silent one step costs 1. Guard + reconfig + μ + step costs more.
If the total exceeds θ_max, the process decoheres. It does not
complete for free.

---

## How to read a new model on this site

1. Name V, G, θ.
2. Say what agrees with an existing presentation on a small V.
3. Grow V or change G until they split — or admit they are one G.
4. Pre-screen theorems: values in V? ops in G? hypotheses θ-legal?
   quantifier listable? Conclusion on the listed cut?
5. ADMIT means well-typed; run the close-test. DEFER means the ∀
   outruns the cut. REFUSE means this carrier cannot hold the sentence.

Examples of that gate: LEM ADMIT on CL2, REFUSE on K3.
`1/x` at 0 REFUSE (0 may sit in V; quot is unstable there).
Mean-value on ℝ DEFER (unlistable V).

---

## What this site is not

- A religion, a floor, or a theory of everything.
- Easier than a first calculus course (not claimed).
- A replacement for JAX, PhysX, or a shipped game engine.
- A proof that Newton, Ptolemy, or Frege were “wrong about reality.”
  They were maps. Some maps leave V when you grow the alphabet.

Replica, receipt, ledger line — or it did not happen.
