# Process calculus

A first course with no independent variable, no limits, and no Inf.

```
rate(P, G) = P.r / G.r
```

Two channels under one cut. Isolation is an argument. Mix is Leibniz
because both channels update. A pole is θ. A second derivative is a
later presentation.

This is a map. It is not how variation *is*. It is the smallest G
that still does product, chain, inverse, and related rates.

## Six moves (then stop)

1. A reading is a value and a channel: `(v, r)`.
2. A rate is their ratio under a named isolation.
3. Mix is Leibniz: both slots update.
4. Chain is cancellation of a shared channel.
5. A pole is θ — dead isolator or divisor 0 — not a place.
6. If you need a second derivative, say so: extra slot or extra extract.

Drop: limits, Inf, unary D as a property of f, finite difference as
“the” derivative, Riemann-as-primitive, locked time.

## Run

```
python -m pcalc              # kernel demo
python -m pcalc.lesson01
python -m pcalc.lesson02
python -m pcalc.lesson03
python -m pcalc.lesson04
python -m pcalc.lesson05
python -m pcalc.lesson06
python -m pcalc.worksheet
python -m pcalc.lessons
python -m pcalc.jetlab
python -m pcalc.intlab
python -m pcalc.ratelab
python -m pcalc.fdlab
python -m pcalc.gen
```

What would make this land: `docs/GAMECHANGER.md`

## For a teacher

Standard Calc I hides isolation inside “with respect to x” and hides
θ inside “the limit.” Here both are printed. Numbers that agree with
the standard course (x² at 3 is 6) are the same mix. Numbers that
disagree (fd, locked seed) are other presentations — name them, do
not apologize.
