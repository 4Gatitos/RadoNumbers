"""Mechanical verification of the V-core Core Completeness Lemma (CCL-V).

Proof chain being verified (see the CCL-V draft / structured report):

  LEMMA PAIR (seedless two-distance lemma): P,Q >= 1, v2(P) != v2(Q),
    N >= P+Q+max(P,Q)  =>  no chi:[1,N]->{0,1} has simultaneously
    (no two 1s at distance P) and (no two 0s at distance Q).
    Proof: complement so the 1-avoided distance is W=max; some 1 exists;
    F(x) = x+S (x<=N-S) / x-(W-w) propagates 1s, is total, enters and cycles
    in the window [N-2W+1,N] as the rotation by S=P+Q on Z_{2W}; the orbit
    covers a coset of gcd(S,2W), which divides W since v2(S)=min(v2P,v2Q)
    <= v2(W); two orbit points at exact distance W give a forbidden 1-pair.

  LEMMA VAL: V-shaped window (m>=4 => N >= a+max(t,mu)+1): a split valley
    chi(lam-1) != chi(lam) yields (after complement) 1s avoiding t and 0s
    avoiding mu; v2(t) != v2(mu) (2-adic existence); PAIR(t,mu) refutes.

  LEMMA WINDOW: v2(a)<=v2(t), mu=a-t: no u,v subsets of {0..a}, each with
    no pair at distance t or mu, with u ∪ v = {0..a}.
    Proof: the walk y_{i+1} = y_i+t (if <=a) else y_i-mu closes into a cycle
    of length n = a/gcd(a,t), which is ODD (v2(a)<=v2(t)) and >=3; its edges
    are distance-t/mu pairs inside [0,a]; two independent sets can cover at
    most 2*(n-1)/2 = n-1 < n of its vertices.

  LEMMA INTERIOR: valid chi, equal valley colour g, owner k with
    d_k + a <= N-1 and chi(k) != g: the two length-(a+1) windows
    u(y)=chi(y), v(y)=chi(y+d_k) (y in [1,a+1]) are {t,mu}-independent
    (1s avoid t and mu) and cover (0s avoid d_k) -- contradicting WINDOW.

  THEOREM V-RIGID: N >= lam, m >= 4: every valid colouring has
    chi(lam-1)=chi(lam)=g and every non-outermost owner coloured g;
    the gate is x g^(m-2) y -- at most 3 runs, in the family F.

  COROLLARY CCL-V: at N = Rad2-1 (colourable), any valid colouring's gate
    is in F; with Theorem SA (single-arm), Lemma V0 and m<=3 trivial,
    CCL holds in full and gen = Rad2 on the whole middle band (Theorem E).

Checks below:
  1. PAIR: orbit-certificate replay on all P,Q <= 40 with v2 mismatch
     (threshold and threshold+7), SAT confirmation of infeasibility at the
     exact threshold for P,Q <= 25, and converse feasibility when v2 equal.
  2. WINDOW: odd-cycle construction for all admissible (a,t), a <= 300;
     bipartiteness dichotomy (non-admissible => bipartite => feasible).
  3. V-RIGID + CCL-V at every extremal V-core instance a <= 13 (from the
     project's verified CSVs): hypotheses, valid-gate enumeration by
     SAT+blocking, gate law x g^(m-2) y, |runs| <= 3, colourability.
Run:  python demostracio/verify_vcore_ccl.py [amax_check3=13]
"""
import csv
import sys
from math import gcd
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from rado_core import clauses_for, rado_exists, v2  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402


# ---------- check 1: LEMMA PAIR ----------

def pair_orbit_certificate(P, Q, N):
    W, w = max(P, Q), min(P, Q)
    assert P != Q and v2(P) != v2(Q)
    S, B = P + Q, max(P, Q) - min(P, Q)
    assert B > 0 and N >= S + W and N - 2 * W + 1 >= 1
    g = gcd(S, 2 * W)
    assert W % g == 0, "divisibility step broken"
    for x0 in range(1, N + 1):
        seen, forced = set(), set()
        x = x0
        while x not in seen:
            seen.add(x)
            forced.add(x)
            if x <= N - S:
                assert x + W <= N
                x = x + S
            else:
                assert x - W >= 1
                x = x - B
            assert 1 <= x <= N
        assert any((u + W) in forced for u in forced), (P, Q, N, x0)


def pair_sat(P, Q, N):
    cls = []
    for p in range(1, N + 1):
        if p + P <= N:
            cls.append([-p, -(p + P)])
        if p + Q <= N:
            cls.append([p, p + Q])
    s = Cadical195(bootstrap_with=cls)
    ok = s.solve()
    s.delete()
    return ok


def check1():
    n_orb = n_sat = n_conv = 0
    for P in range(1, 41):
        for Q in range(1, 41):
            if P == Q:
                continue
            N0 = P + Q + max(P, Q)
            if v2(P) != v2(Q):
                pair_orbit_certificate(P, Q, N0)
                pair_orbit_certificate(P, Q, N0 + 7)
                n_orb += 1
                if P <= 25 and Q <= 25:
                    assert not pair_sat(P, Q, N0), (P, Q)
                    n_sat += 1
            else:
                assert pair_sat(P, Q, 3 * (P + Q)), (P, Q)
                n_conv += 1
    print(f"check1 PAIR: orbit replay {n_orb}, SAT-unsat {n_sat}, "
          f"converse-feasible {n_conv} -- all OK")


# ---------- check 2: LEMMA WINDOW ----------

def window_bipartite(a, t):
    mu = a - t
    col = [None] * (a + 1)
    for s0 in range(a + 1):
        if col[s0] is not None:
            continue
        col[s0] = 0
        stack = [s0]
        while stack:
            y = stack.pop()
            for z in (y + t, y - t, y + mu, y - mu):
                if 0 <= z <= a:
                    if col[z] is None:
                        col[z] = 1 - col[y]
                        stack.append(z)
                    elif col[z] == col[y]:
                        return False
    return True


def check2(amax=300):
    cnt = 0
    for a in range(3, amax + 1):
        for t in range(1, a):
            mu = a - t
            g1 = gcd(a, t)
            n = a // g1
            if v2(a) <= v2(t):
                assert 2 * t != a
                assert n % 2 == 1 and n >= 3, (a, t, n)
                cyc, y = [], t
                for _ in range(n):
                    cyc.append(y)
                    y = y + t if y + t <= a else y - mu
                assert y == cyc[0] and len(set(cyc)) == n, (a, t)
                for u, w in zip(cyc, cyc[1:] + cyc[:1]):
                    assert abs(u - w) in (t, mu) and 0 <= u <= a and 0 <= w <= a
                assert not window_bipartite(a, t), (a, t)
            else:
                assert n % 2 == 0, (a, t)
                assert window_bipartite(a, t), (a, t)
            cnt += 1
    print(f"check2 WINDOW: odd-cycle/bipartite dichotomy verified on {cnt} "
          f"(a,t) pairs, a<={amax}")


# ---------- check 3: V-RIGID + CCL-V at extremal N ----------

def load_pairs(amax):
    pairs = {}
    for fn in ("fullband.csv", "midband.csv"):
        with open(REPO / "results" / fn, newline="") as f:
            for row in csv.DictReader(f):
                a, c, r = int(row["a"]), int(row["c"]), int(row["rad2"])
                if a <= amax:
                    pairs[(a, c)] = r
    return pairs


def in_band(a, c):
    if c <= a or c % a == 0 or not rado_exists(a, c):
        return False
    t = c % a
    lam = -(-c // a)
    return lam <= (a + t) * (a + 3) + 2


def check3(amax=13):
    pairs = load_pairs(amax)
    n_v = 0
    for (a, c), rad2 in sorted(pairs.items()):
        if not in_band(a, c):
            continue
        N = rad2 - 1
        if N < 1:
            continue
        t, mu = c % a, a - c % a
        lam = -(-c // a)
        ks = [(k, abs(a * k - c)) for k in range(1, N + 1)
              if 1 <= abs(a * k - c) <= N - 1]
        m = len(ks)
        pos = [k for k, d in ks]
        if not (N >= lam and m >= 4 and (lam - 1) in pos and lam in pos):
            continue
        n_v += 1
        # hypotheses used by the proof
        assert v2(a) <= v2(t) and v2(t) != v2(mu)
        assert N >= a + max(t, mu) + 1, (a, c)
        iv = pos.index(lam - 1)
        # enumerate all valid gates
        s = Cadical195(bootstrap_with=clauses_for(a, c, N))
        gates = []
        while s.solve():
            model = s.get_model()
            colr = {v: 1 for v in model if 0 < v}
            gate = tuple(1 if colr.get(k, 0) else 0 for k in pos)
            gates.append(gate)
            s.add_clause([-k if gate[i] else k for i, k in enumerate(pos)])
        s.delete()
        assert gates, (a, c, "extremal N uncolourable?!")
        for gate in gates:
            g = gate[iv]
            assert gate[iv + 1] == g, (a, c, gate, "VAL violated")
            assert all(gate[x] == g for x in range(1, m - 1)), \
                (a, c, gate, "interior law violated")
            runs = 1 + sum(1 for x in range(1, m) if gate[x] != gate[x - 1])
            assert runs <= 3, (a, c, gate)
    print(f"check3 V-RIGID/CCL-V: {n_v} extremal V-core instances (a<={amax}); "
          f"all valid gates of form x g^(m-2) y, all in F -- OK")


if __name__ == "__main__":
    check1()
    check2()
    check3(int(sys.argv[1]) if len(sys.argv) > 1 else 13)
    print("ALL CHECKS PASS")
