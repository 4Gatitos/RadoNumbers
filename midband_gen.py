"""Exact generator for Rad2(a;c) on the middle band a < c < a(K+2).
Assembled by the generator panel; verified independently (see verify_formula.py).
"""

"""EXACT generator for Rad2(a;c) on the middle band  a < c < a(K+2),
K = ceil((1+c(a+3))/(1+a(a+3))) - 1,  for the equation  x1 + a*x2 - x3 = c.

Assembled from four independent route reports (all 100%-verified individually):

  LAYER 1 (theorem, proven):    a | c  ->  Rad2 = c/a  ((m,m,m) monochromatic).
  LAYER 2 (Route D top layer):  closed-form pin predicate for the deep tail
      lam >= t(a+3)+2 (t>=2)  /  lam >= 2a-2 (t=1):
      Rad2 = lam - 1 + [lam <= E1(a,t)],
      E1 = 2a+2 (t=1);  E1 = (a+2)t + a + 1 + max(t - (a mod 2t), 0) (t>=2).
  LAYER 3 (Route B core):       exact per-N decision + monotone search.
      decide(N): the owner/window reformulation reduces coloring-existence to
      2-SAT once the colors of the O(N/a) window multipliers are fixed; sweep
      the O(m^2) one-color-contiguous-block window assignments (the canonical
      extremal family, = Route A's hot^i cold^* hot^l family closed under
      color flip), each decided exactly by unit propagation + iterative-Tarjan
      2-SAT.  Rad2 = first UNSAT N, found by doubling climb + binary search
      from the PROVEN lower bound K+1 (Dwivedi-Tripathi Theorem 6).
  GUARD (existence):            v2(a) > v2(c)  ->  Rad2 does not exist (None).

Soundness: a True answer of decide() is witness-backed (a 2-SAT model IS a
valid coloring), so layer 3 can never overshoot Rad2.  Exactness rests on the
completeness of the contiguous-block window family (layer 3) and the pin
predicate (layer 2) -- both massively machine-verified, neither proven.

Stdlib only.  No SAT solver.  Polynomial in a (N = O(a^2) on the band).
"""


def gen(a, c):
    """Exact Rad2(a;c) on the middle band a < c < a(K+2).

    Returns None if Rad2 does not exist (v2(a) > v2(c)); raises ValueError
    outside the middle band."""
    # ---------------- band arithmetic and guards ----------------
    if a < 2 or c <= a:
        raise ValueError("need a >= 2 and c > a (middle band)")
    A = 1 + a * (a + 3)
    K1 = -(-(1 + c * (a + 3)) // A)          # K+1: proven lower bound (DT Thm 6)
    K = K1 - 1
    if c >= a * (K + 2):
        raise ValueError("(a=%d, c=%d) above the middle band" % (a, c))

    def v2(n):
        k = 0
        while n % 2 == 0:
            n //= 2
            k += 1
        return k

    if v2(a) > v2(c):
        return None                          # Rad2(a;c) does not exist

    lam = -(-c // a)                         # ceil(c/a)
    mu = lam * a - c                         # in [0, a-1]
    t = a - mu                               # = c mod a  (when mu > 0)

    # ---------------- layer 1: degenerate theorem  a | c ----------------
    if mu == 0:
        return c // a

    # ---------------- layer 2: Route D top-layer closed form ----------------
    import os as _os
    _use_l2 = not _os.environ.get("MIDBAND_NO_L2")
    if _use_l2 and ((t >= 2 and lam >= t * (a + 3) + 2) or (t == 1 and lam >= 2 * a - 2)):
        if t == 1:
            E1 = 2 * a + 2
        else:
            r = a % (2 * t)
            E1 = (a + 2) * t + a + 1 + max(t - r, 0)
        return lam - 1 + (1 if lam <= E1 else 0)

    # ---------------- layer 3: Route B exact decision core ----------------
    e = c - a

    def owner_list(N):
        """(owners, zero): owners = [(k, d)] with k in [1,N], d = |a(k-1)-e| <= N-1;
        zero=True iff some k in [1,N] has shift 0."""
        klo = max(1, -(-(e - N + 1) // a) + 1)
        khi = min(N, (e + N - 1) // a + 1)
        out = []
        zero = False
        for k in range(klo, khi + 1):
            s = a * (k - 1) - e
            if s == 0:
                zero = True
            else:
                d = abs(s)
                if d <= N - 1:
                    out.append((k, d))
        return out, zero

    def assignments(m, hint):
        """All 0/1 vectors of length m in which the 1s or the 0s form one
        contiguous block (the canonical extremal window family)."""
        seen = set()
        out = []
        for pol in (1, 0):
            for lo in range(m):
                for hi in range(lo + 1, m + 1):
                    v = [1 - pol] * m
                    for p in range(lo, hi):
                        v[p] = pol
                    tv = tuple(v)
                    if tv not in seen:
                        seen.add(tv)
                        out.append(tv)
        for v in ((0,) * m, (1,) * m):
            if v not in seen:
                seen.add(v)
                out.append(v)
        if hint is not None and hint in seen:
            out.remove(hint)
            out.insert(0, hint)
        return out

    def check_assignment(N, ow, colors):
        """Is there a valid coloring of [1,N] whose restriction to the window
        is `colors`?  Exact 2-SAT; literal encoding lit(v,val) = 2*v + val."""
        m = len(ow)
        # window-local conflict filter (owners are consecutive integers)
        for i, (k, d) in enumerate(ow):
            g = colors[i]
            if d < m:
                for p in range(m - d):
                    if colors[p] == g and colors[p + d] == g:
                        return False
        dist = ([], [])                      # forbidden distances per color class
        for i, (k, d) in enumerate(ow):
            dist[colors[i]].append(d)
        unit_of = {ow[i][0]: colors[i] for i in range(m)}

        def neighbors(lit):
            v, val = lit >> 1, lit & 1
            res = []
            for d in dist[val]:
                w = v + d
                if w <= N:
                    res.append(2 * w + (1 - val))
                w = v - d
                if w >= 1:
                    res.append(2 * w + (1 - val))
            if v in unit_of and val != unit_of[v]:
                res.append(2 * v + unit_of[v])
            return res

        # unit propagation from the window constants (sound early rejection)
        forced = {}
        stack = []
        for k, g in unit_of.items():
            forced[k] = g
            stack.append(2 * k + g)
        ok = True
        while stack and ok:
            lit = stack.pop()
            for nl in neighbors(lit):
                nv, nval = nl >> 1, nl & 1
                if nv in forced:
                    if forced[nv] != nval:
                        ok = False
                        break
                else:
                    forced[nv] = nval
                    stack.append(nl)
        if not ok:
            return False

        # full 2-SAT: iterative Tarjan SCC on the implication graph (nodes 2..2N+1)
        index = {}
        low = {}
        comp = {}
        onstk = {}
        cstack = []
        counter = [0]
        ncomp = [0]
        for root in range(2, 2 * N + 2):
            if root in index:
                continue
            work = [(root, iter(neighbors(root)))]
            index[root] = low[root] = counter[0]
            counter[0] += 1
            cstack.append(root)
            onstk[root] = True
            while work:
                node, it = work[-1]
                advanced = False
                for nb in it:
                    if nb not in index:
                        index[nb] = low[nb] = counter[0]
                        counter[0] += 1
                        cstack.append(nb)
                        onstk[nb] = True
                        work.append((nb, iter(neighbors(nb))))
                        advanced = True
                        break
                    elif onstk.get(nb):
                        if index[nb] < low[node]:
                            low[node] = index[nb]
                if advanced:
                    continue
                work.pop()
                if work:
                    pn = work[-1][0]
                    if low[node] < low[pn]:
                        low[pn] = low[node]
                if low[node] == index[node]:
                    while True:
                        w = cstack.pop()
                        onstk[w] = False
                        comp[w] = ncomp[0]
                        if w == node:
                            break
                    ncomp[0] += 1
        for v in range(1, N + 1):
            if comp[2 * v] == comp[2 * v + 1]:
                return False
        return True

    hint_box = [None]

    def decide(N):
        if N <= 1:
            return True
        ow, zero = owner_list(N)
        if zero:
            return False
        if not ow:
            return True
        for asg in assignments(len(ow), hint_box[0]):
            if check_assignment(N, ow, asg):
                hint_box[0] = asg
                return True
        return False

    # monotone search for the first non-colorable N, from the proven K+1
    if not decide(K1):
        return K1
    lo = K1
    step = 1
    cap_guard = 4 * max(K1 + 2, (a * a + 1) // 2) + 64   # safety only
    while True:
        cand = lo + step
        if cand > cap_guard:
            raise RuntimeError("search exceeded safety cap - conjectured band bound broken")
        if decide(cand):
            lo = cand
            step *= 2
        else:
            hi = cand
            break
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if decide(mid):
            lo = mid
        else:
            hi = mid
    return hi


def rad2(a, c):
    return gen(a, c)
