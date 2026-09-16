# Side-by-side problem book (Calc I slice)

Same numbers when the mix agrees. Split labeled when it should.

## P1. Power

**Standard:** Differentiate \(x^2\) at \(x=3\).  
**Process:** `x = isolate(3); rate(x*x, x)`  
**Both:** 6

## P2. Product

**Standard:** \(\frac{d}{dx}(x^2\cdot x^3)\) at 3.  
**Process:** `rate((x*x)*(x**3), x)`  
**Both:** 405  
**Trap:** product of slopes 6·27=162 is a different G.

## P3. Chain

**Standard:** \(y=x^2,\ w=y^3\), find \(dw/dx\) at \(x=2\).  
**Process:** `rate(w,x)` and `rate(w,y)*rate(y,x)`  
**Both:** 192

## P4. Inverse

**Standard:** \(\frac{d}{dx}(1/x)\) at 3.  
**Process:** `rate(1/x, x)`  
**Both:** \(-1/9\)

## P5. Related rates

**Standard:** \(x^2+y^2=25\), \(x=3,y=4\), \(dx/dt=2\), find \(dy/dt\).  
**Process:** second reading; constraint channel dead.  
**Both:** \(-3/2\)

## P6. Finite difference (SPLIT)

**Standard:** often “approaches 6.”  
**Process:** `fd(h=1/2)` of \(x^2\) at 3 is \(13/2\), leftover \(h=1/2\).  
**Do not agree** until someone hires ∞.

## P7. Units (SPLIT of the *number*)

**Standard:** “the derivative of A=ℓ².”  
**Process:** isolate metres → 6; isolate centimetres → 600.  
**Exam:** write dA/dℓ with the unit named.

## P8. Second derivative (SPLIT of extract)

**Standard:** \(d^2/dx^2(x^4)\) at 2 is 48.  
**Process:** jet r2=48; stencil h=1/2 gives 97/2.  
**Agree** only if they use the jet/rules, not the stencil.

## P9. Integral leftover (SPLIT of extract)

**Standard:** \(\int_0^3 2x\,dx=9\).  
**Process:** mid n=1 is 9; left n=1 is 0.  
**Agree** on mid/antiderivative. Left Riemann is another extract.

## P10. FTC

**Standard:** \(F' = f\).  
**Process:** `rate(x*x, x)` vs integrand `2x` on listed x.  
**Both:** agree on this grid.
