"""
2-color Rado numbers for the equation  x1 + a*x2 - x3 = c
(Dwivedi-Tripathi, Integers 20 (2020) #A36; open windows re-posed in
 Integers 25 (2025) #A108, Open Problems item 1).

Definitions (following the paper):
  Rad2(a;c) = least N such that EVERY 2-coloring of [1,N] contains a
  monochromatic solution (x1,x2,x3) of x1 + a*x2 - x3 = c.
  Solutions may repeat values (x1=x2=x3 allowed, cf. their Proposition 1).
  Existence: Rad2(a;c) exists  iff  v2(a) <= v2(c)   (v2 = 2-adic valuation,
  v2(0) = +infinity).

SAT encoding: one Boolean variable per integer i in [1,N] (True = color 1).
For every (x1,x2) in [1,N]^2 with x3 = x1 + a*x2 - c in [1,N], two clauses
forbid monochromatic triples:  (x1 | x2 | x3) & (~x1 | ~x2 | ~x3).
"[1,N-1] has a valid coloring" == SAT; Rad2 = (largest SAT N) + 1.
"""

from pysat.solvers import Cadical195


def v2(n):
    """2-adic valuation; v2(0) = infinity."""
    if n == 0:
        return float("inf")
    n = abs(n)
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def rado_exists(a, c):
    return v2(a) <= v2(c)


def clauses_for(a, c, N):
    # literals deduplicated per clause (x1=x2 etc.) and duplicate clauses
    # removed: semantically identical, and keeps drat-trim happy
    seen = set()
    cls = []
    for x1 in range(1, N + 1):
        # x3 = x1 + a*x2 - c must lie in [1, N]
        lo = 1 - x1 + c
        lo = max(1, -((-lo) // a))  # ceil(lo / a)
        hi = min((N - x1 + c) // a, N)  # x2 must itself lie in [1, N]
        for x2 in range(lo, hi + 1):
            x3 = x1 + a * x2 - c
            key = tuple(sorted({x1, x2, x3}))
            if key in seen:
                continue
            seen.add(key)
            cls.append(list(key))
            cls.append([-v for v in key])
    return cls


def has_valid_coloring(a, c, N, want_model=False):
    """SAT iff there is a 2-coloring of [1,N] with no monochromatic solution."""
    if N <= 0:
        return (True, []) if want_model else True
    s = Cadical195(bootstrap_with=clauses_for(a, c, N))
    ok = s.solve()
    model = s.get_model() if (ok and want_model) else None
    s.delete()
    if want_model:
        witness = None
        if ok:
            witness = [0] * N  # vars absent from the model are unconstrained
            for v in model:
                if 0 < v <= N:
                    witness[v - 1] = 1
        return ok, witness
    return ok


def upper_cap(a, c):
    """Proven upper bounds (Theorem 1) plus margin: search must stop below this."""
    al = v2(a)
    if c == a:
        return 4
    if c < a:
        if a % 2 == 1:
            return (2 * a + 1) * (a - c) + 1
        return (a + a // (2 ** al) + 2) * (a - c) + 1
    return (a + a // (2 ** al)) * (c - a) + 1


def theorem_lower_seed(a, c):
    """Proven lower bounds: [1, seed] is guaranteed SAT (colorable).
    Theorem 2: c < a  ->  Rad2 >= (a+3)(a-c)+1, so SAT at (a+3)(a-c).
    Theorem 6: c > a  ->  Rad2 >= K+1 = ceil((1+c(a+3))/(1+a(a+3))), SAT at K.
    Theorem 8: c = lambda*a - mu, 3<=lambda<=a+1, 1<=mu<=a+1-lambda -> Rad2 >= lambda+mu.
    """
    if c == a:
        return 0
    if c < a:
        return (a + 3) * (a - c)
    K = -(-(1 + c * (a + 3)) // (1 + a * (a + 3))) - 1
    seed = K
    # Theorem 8: c = lambda*a - mu with mu in [1, a+1-lambda], lambda in [3, a+1]
    for lam in range(3, a + 2):
        mu = lam * a - c
        if 1 <= mu <= a + 1 - lam:
            seed = max(seed, lam + mu - 1)
    return seed


def rado_number(a, c, cap_margin=4, verbose=False):
    """Compute Rad2(a;c) exactly. Returns (rad2, witness) where witness is a
    valid coloring of [1, rad2-1] (list of 0/1), or (None, None) if nonexistent."""
    if not rado_exists(a, c):
        return None, None
    cap = upper_cap(a, c) + cap_margin

    lo = theorem_lower_seed(a, c)
    if lo > 0 and not has_valid_coloring(a, c, lo):
        # theoretical seed failed -> encoding vs. theorem mismatch; fall back
        if verbose:
            print(f"  WARNING a={a} c={c}: seed {lo} not SAT, falling back to 0")
        lo = 0
    hi = max(lo + 1, 1)
    while has_valid_coloring(a, c, hi):
        lo = hi
        hi = min(2 * hi, cap)
        if hi >= cap and has_valid_coloring(a, c, cap):
            raise RuntimeError(f"a={a} c={c}: SAT at cap {cap}; contradicts Theorem 1")
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if has_valid_coloring(a, c, mid):
            lo = mid
        else:
            hi = mid
    if lo > 0:
        ok, witness = has_valid_coloring(a, c, lo, want_model=True)
        assert ok, "boundary SAT vanished"
    else:
        witness = []
    return hi, witness
