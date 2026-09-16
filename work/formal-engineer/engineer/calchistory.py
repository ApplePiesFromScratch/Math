"""calchistory.py — taxonomy along the packing order.

Humans did not discover The Derivative. They hired a sequence of
presentations. Each row is V, G, θ, what it closed, what it smuggled.

    python -m engineer.calchistory
"""

ERAS = [
    {
        "when": "c. 350 BCE",
        "name": "Eudoxus / exhaustion",
        "V": "magnitudes + finite polygonal approximations",
        "G": "inscribe, double, compare leftover",
        "theta": "leftover smaller than any given magnitude (no last step named)",
        "closed": "area comparisons that finish as a finite inequality",
        "ghost": "the circle as the last polygon",
        "pack": "θ as a race against a given ε, already — but ε is a magnitude, not a real",
    },
    {
        "when": "c. 250 BCE",
        "name": "Archimedes quadrature",
        "V": "same + method of mechanical theorems (leverage)",
        "G": "balance indivisible slices, then exhaustion to certify",
        "theta": "heuristic G and certified G are different cuts",
        "closed": "parabola segment = 4/3 triangle — certified after the heuristic",
        "ghost": "the slice that 'is' the area (he knew it wasn't the proof)",
        "pack": "two G's for one V: discovery mix vs audit mix",
    },
    {
        "when": "c. 1630",
        "name": "Cavalieri indivisibles",
        "V": "area as a stack of lines; volume as a stack of planes",
        "G": "match slices, conclude the stacks match",
        "theta": "none declared — lines have no thickness",
        "closed": "fast area/volume shortcuts",
        "ghost": "the line as a thin rectangle (thickness 0 hired as V)",
        "pack": "∞ thin things added. first industrial ∞-as-inhabitant",
    },
    {
        "when": "c. 1636",
        "name": "Fermat adequality",
        "V": "polynomials + an increment E that is later dropped",
        "G": "f(x+E) ~ f(x), divide by E, set E=0",
        "theta": "E is and is not zero, in sequence",
        "closed": "max/min of polynomials, tangents",
        "ghost": "E as a number that dies on command",
        "pack": "the first pair (value, increment) with the increment murdered after quot",
    },
    {
        "when": "c. 1637",
        "name": "Descartes algebraic tangent",
        "V": "polynomials, double root as contact",
        "G": "equal-root condition for a line vs a curve",
        "theta": "works where the curve is algebraic enough",
        "closed": "tangents without a disappearing E",
        "ghost": "none new — contact is a multiplicity in V",
        "pack": "the honest algebraic slice. no ∞. limited V",
    },
    {
        "when": "1660s–70s",
        "name": "Barrow / Newton fluxions",
        "V": "fluents (quantities that flow) + fluxions (their speeds)",
        "G": "dot tables, moment o, cancel higher o",
        "theta": "o vanishes after quot; time is the hidden isolator",
        "closed": "product, chain, inverse in practice; kinematics first",
        "ghost": "time as the independent life; o as Fermat's E",
        "pack": "isolation locked to t. unary D is born as a property of a fluent",
    },
    {
        "when": "1670s–84",
        "name": "Leibniz differentials",
        "V": "dx, dy as infinitely small differences",
        "G": "d(xy)=x dy+y dx; dy/dx as a quotient of ghosts",
        "theta": "higher-order dx^n discarded",
        "closed": "the mix we still use; chain as cancellation of dx",
        "ghost": "dx as an inhabitant of the line",
        "pack": "binary rate written as a quotient of two hired points. best notation, worst ontology",
    },
    {
        "when": "1734",
        "name": "Berkeley's audit",
        "V": "the same increments",
        "G": "read the proof and watch E die twice",
        "theta": "you may not use E=0 and E≠0 as one value",
        "closed": "the contradiction in Fermat/Newton/Leibniz bookkeeping",
        "ghost": "named: ghosts of departed quantities",
        "pack": "the first θ-check on the increment. not a calculus. an accounting flag",
    },
    {
        "when": "1797",
        "name": "Lagrange derived function",
        "V": "power series; f' is the coefficient of h",
        "G": "algebra of series, no disappearing E",
        "theta": "the series must exist as an object",
        "closed": "derivative as a coefficient — a slot, not a limit",
        "ghost": "every function is its series (it isn't)",
        "pack": "jet thinking. r lives in the next coefficient. V too small for most f",
    },
    {
        "when": "1820s",
        "name": "Cauchy limit",
        "V": "variables that approach; limit as a new inhabitant of talk",
        "G": "ε-talk without a finished quantifier order",
        "theta": "approach, not arrive",
        "closed": "continuity, integral as limit of sums, respectability",
        "ghost": "the limit as a point the sequence owns",
        "pack": "∞ kept, but dressed as a process. still no last h",
    },
    {
        "when": "1860s–72",
        "name": "Weierstrass ε-δ",
        "V": "R as a completed line (Dedekind / Cauchy reals)",
        "G": "∀ε∃δ formulas",
        "theta": "quantifiers over an unlistable V",
        "closed": "rigour that can fail a function in public",
        "ghost": "R itself as a finished alphabet you can ∀ over",
        "pack": "the technician's fortress. pre-screen: DEFER on the ∀R",
    },
    {
        "when": "1854 / 1902",
        "name": "Riemann / Lebesgue integral",
        "V": "tagged partitions / measurable functions",
        "G": "mesh→0 sums / measure of preimages",
        "theta": "mesh last-step unpaid (Riemann); null sets ignored (Lebesgue)",
        "closed": "area for wilder f",
        "ghost": "the last partition; the null set as 'nothing'",
        "pack": "two integral G's. same leftover problem, different V",
    },
    {
        "when": "1961",
        "name": "Robinson nonstandard",
        "V": "*R, infinitesimals as actual points",
        "G": "transfer, standard part st(·)",
        "theta": "st drops the infinitesimal part — E dies on purpose, named",
        "closed": "Leibniz bookkeeping made a finished algebra",
        "ghost": "milder: the monad is in V by design",
        "pack": "Fermat's E kept as a citizen, then projected. honest μ: *R → R",
    },
    {
        "when": "19th–20th c.",
        "name": "dual numbers / forward AD",
        "V": "R[ε]/ε²=0  or  Q-pairs",
        "G": "Leibniz mix; extract r",
        "theta": "ε²=0 by algebra, not by taking a limit",
        "closed": "exact first channel on the listed maps",
        "ghost": "none required. seed often locked (unary D)",
        "pack": "Lagrange's coefficient without the series religion. our pair is this cut with seed free",
    },
    {
        "when": "now, this cut",
        "name": "rate as ratio of two channels",
        "V": "Q-pairs (v,r); jet when you pay for r2",
        "G": "isolate(value, seed), Leibniz, quot, rate=P.r/G.r",
        "theta": "dead isolator; quot at 0; no Inf",
        "closed": "product, chain, inverse, related rates, Euler, gauge",
        "ghost": "refused — isolation is an argument",
        "pack": "Newton's fluxion minus locked t. Leibniz's dy/dx minus dx-as-point. AD minus locked seed",
    },
]


# continued packing — late line through present
LATER = [
    {
        "when": "1844 / 1900",
        "name": "Grassmann to Gibbs vectors",
        "V": "oriented magnitudes; then arrows in R^3",
        "G": "wedge / cross / div / curl as packed products",
        "theta": "dimension 3 hides the associator; lose grade",
        "closed": "physics bookkeeping in 3D",
        "ghost": "the vector as a little arrow that is the quantity",
        "pack": "channels bundled into a tuple. isolation now has a direction",
    },
    {
        "when": "1880–1900",
        "name": "Ricci / covariant derivative",
        "V": "tensors on a manifold; connection as extra G",
        "G": "∇_X Y; Christoffel correction",
        "theta": "without a connection there is no unique directional rate",
        "closed": "rate on curved V; parallel transport",
        "ghost": "the connection coefficients as nature's numbers",
        "pack": "ordinary d was a flat connection in costume. curvature is leftover of ∇∘∇",
    },
    {
        "when": "1899–1920s",
        "name": "Cartan forms",
        "V": "graded algebra of dx^i; k-forms",
        "G": "d, ∧, pullback; Stokes as the integral G",
        "theta": "d∘d=0 is the law; not optional mix",
        "closed": "div/grad/curl are one d on different grades",
        "ghost": "dx^i as Leibniz's dx, now a basis element",
        "pack": "the mix becomes graded. chain is pullback. best 20th-c notation",
    },
    {
        "when": "1900–20s",
        "name": "Fréchet / Gâteaux",
        "V": "maps between Banach spaces",
        "G": "linear map that approximates; directional limit",
        "theta": "the linear map must exist in the operator V",
        "closed": "calculus of variations, PDE linearization",
        "ghost": "the derivative is an operator that f owns",
        "pack": "unary D lifted off R. seed locked in a direction v",
    },
    {
        "when": "1930s–50s",
        "name": "Sobolev / Schwartz distributions",
        "V": "linear functionals on test functions",
        "G": "differentiate the functional; weak d",
        "theta": "test class is the real V; the 'function' is a ghost of evaluation",
        "closed": "Heaviside has a derivative; PDEs with corners",
        "ghost": "the delta as a function on the line",
        "pack": "move d onto a friendlier V instead of repairing f. engineer move",
    },
    {
        "when": "1944–60s",
        "name": "Itô / Stratonovich",
        "V": "semimartingales; quadratic variation is a new slot",
        "G": "two mixes: Itô (0) and Stratonovich (Leibniz)",
        "theta": "which mix you picked is part of the presentation",
        "closed": "SDEs, Kalman, options",
        "ghost": "dW·dW=dt as a fact about nature",
        "pack": "the first time mix itself visibly splits. Leibniz is not forced",
    },
    {
        "when": "1967–80s",
        "name": "Synthetic differential geometry",
        "V": "ring with nilpotents D={ε | ε²=0} in a topos",
        "G": "every map is 'smooth'; Kock-Lawvere axiom",
        "theta": "classical logic fails (no excluded middle on D)",
        "closed": "Leibniz + infinitesimals without *R",
        "ghost": "mild: the line is a tiny thickened point",
        "pack": "dual numbers as the whole geometry. LEM dies so ε can live",
    },
    {
        "when": "1970–86",
        "name": "Reverse-mode AD / backprop",
        "V": "computational graph; pair pulled backward",
        "G": "chain as adjoint, one seed at the output",
        "theta": "tape / graph must be the V; control flow is θ",
        "closed": "gradient of a scalar at thousands of inputs, one pass",
        "ghost": "the gradient as what the network 'learns'",
        "pack": "isolate the OUTPUT (we already hit this). industrial scale",
    },
    {
        "when": "1990s–2010s",
        "name": "DEC / discrete exterior calculus",
        "V": "cochains on a mesh; k-forms live on k-cells",
        "G": "coboundary as d; discrete Stokes exact on the mesh",
        "theta": "the mesh is V; refine is μ not a limit inside V",
        "closed": "structure-preserving EM, fluids",
        "ghost": "the fine mesh as the continuum",
        "pack": "integral theorems exact before any ∞. leftover is the mesh choice",
    },
    {
        "when": "2014–",
        "name": "JAX / torch autodiff stacks",
        "V": "float tensors + graph or tracing",
        "G": "forward + reverse + vmap + jit as one G-family",
        "theta": "float ε, nan, tracing vs Python, batch",
        "closed": "ML, differentiable physics, implicit layers",
        "ghost": "float as Q; nan as Inf; 'the gradient' as one object",
        "pack": "AD as infrastructure. seed policy hidden in the API (grad vs jvp)",
    },
    {
        "when": "2018–",
        "name": "Neural ODE / differentiable simulators",
        "V": "parameters + state of a solver",
        "G": "differentiate through the integrator; adjoint in time",
        "theta": "solver tolerances, stiffness — slop as θ again",
        "closed": "learn a vector field; invert a physics engine",
        "ghost": "the ODE as the law; the solver as invisible",
        "pack": "physics-engine presentation with the rate slot aimed at parameters",
    },
    {
        "when": "2024–26",
        "name": "this cut (rate as ratio)",
        "V": "Q-pairs; jets when paid; finite listed grids",
        "G": "isolate(value, seed), Leibniz, rate=P.r/G.r",
        "theta": "dead isolator; listed leftover; no Inf inhabitant",
        "closed": "the course without locked t, without dx-as-point, without ∀R",
        "ghost": "refused",
        "pack": "unpacks Newton/Leibniz/AD/backprop as isolation policy. calculus worlds become enumerable",
    },
]


def main():
    print("CALC HISTORY  packed in the order humans packed it")
    print()
    all_eras = ERAS[:-1] + LATER
    for i, e in enumerate(all_eras, 1):
        print(f"{i:>2}. {e['when']:<16} {e['name']}")
        print(f"    V     {e['V']}")
        print(f"    G     {e['G']}")
        print(f"    θ     {e['theta']}")
        print(f"    closed {e['closed']}")
        print(f"    ghost  {e['ghost']}")
        print(f"    pack   {e['pack']}")
        print()
    print(f"{len(all_eras)} presentations. none of them is The Calculus.")
    print("verdict PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
