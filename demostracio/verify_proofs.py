"""
Committed mechanical verification of every FINITE claim used by the proofs in
demostracio/ (the infinite statements are proved by hand in the drafts; this
script re-derives all their machine-checkable ingredients from scratch).

  [1] Lemma 7(a) of UB-r-gt-d: in regime r > d, existence v2(a)<=v2(a-d)
      is equivalent to v2(s) != v2(d); and r = 2d (s = d) never has existence.
  [2] Lemma 6 of UB-r-gt-d (brute force): for every d <= 14, s in [1,d-1],
      among all antipodal phi: Z/2d -> {0,1} with phi(1)=0, the patterns that
      avoid conflicts (V),(IV),(Cb) are EXACTLY the s-antiperiodic ones, and
      none exist when v2(s) != v2(d).
  [3] Triple/range replay for UB-r-gt-d Lemmas 1-5: every cited triple is a
      genuine solution with all entries in [1,N], at boundary values of the
      free parameters, for all in-scope (a,d), d <= 16, a <= 400.
  [4] Chunk-offset normal form of LB-general Lemma 2: the family coloring
      satisfies chi(x) = alpha(w(x)-1) for every x, for all existing (a,d)
      with d >= 2, a <= 200.
  [5] Family length bookkeeping: len(family_coloring) == conjectured - 1.
"""
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from family import family_coloring, conjectured
from rado_core import rado_exists, v2


def check1():
    bad = 0
    for d in range(2, 40):
        for q in range(0, 12):
            for s in range(1, d + 1):  # includes s=d, i.e. r=2d
                a = 2 * d * q + d + s
                exists = rado_exists(a, a - d)
                if s == d:
                    bad += exists  # r=2d must never exist
                else:
                    bad += exists != (v2(s) != v2(d))
    print(f"[1] 2-adic equivalence + r=2d nonexistence: {'OK' if not bad else f'{bad} FAILURES'}")
    return not bad


def conflicts(phi, d, s):
    """phi: dict on 1..2d (mod-2d representative in [1,2d])."""
    def P(m):  # value at representative
        return phi[(m - 1) % (2 * d) + 1]
    plateaus = {P(m) for m in range(1, d + 2) if P(m) == P(m + s)}
    V = (1 - P(2)) in plateaus
    IV = (1 - P(d)) in plateaus
    Cb = any(P(i) != P(i + 1) and P(i + 1) in plateaus for i in range(1, d))
    return V or IV or Cb


def check2():
    bad = 0
    for d in range(2, 15):
        for s in range(1, d):
            for bits in product((0, 1), repeat=d - 1):
                phi = {1: 0}
                for i, b in enumerate(bits, start=2):
                    phi[i] = b
                for m in range(1, d + 1):
                    phi[m + d] = 1 - phi[m]
                escapes = not conflicts(phi, d, s)
                antiper = all(phi[(m - 1 + s) % (2 * d) + 1] == 1 - phi[m]
                              for m in range(1, 2 * d + 1))
                if escapes != antiper:
                    bad += 1
                if escapes and v2(s) != v2(d):
                    bad += 1
    print(f"[2] Lemma 6 brute force (d<=14): {'OK' if not bad else f'{bad} FAILURES'}")
    return not bad


def check3():
    def sol(x, k, y, a, d, N):
        return y == x + a * (k - 1) + d and 1 <= x and 1 <= k <= N and 1 <= y <= N

    bad = []
    for d in range(2, 17):
        for a in range(d + 1, 401):
            r = a % (2 * d) or 2 * d
            if not (d < r < 2 * d) or not rado_exists(a, a - d):
                continue
            N = (a + 3) * d + a - (d - 1)
            T, W = d * (a + 1), a + d + 1
            ok = (N == T + W)
            # R0 boundaries; R1 boundaries; Lemma 1(a)
            ok &= sol(1, 1, 1 + d, a, d, N) and sol(N - d, 1, N, a, d, N)
            ok &= sol(1, d + 1, 1 + T, a, d, N) and sol(W, d + 1, N, a, d, N)
            # Lemma 2 ladder extremes (U at x=W-2d, D at y=2d+1)
            x = W - 2 * d
            ok &= sol(x, 1, x + d, a, d, N) and sol(x + d + T, 1, x + 2 * d + T, a, d, N)
            y = 2 * d + 1
            ok &= sol(y - d, 1, y, a, d, N) and sol(y - 2 * d + T, 1, y - d + T, a, d, N)
            # Lemma 3 case boundaries
            ok &= sol(a + 1 + T, 1, a + 1 + d + T, a, d, N)
            ok &= sol(W - d + T, 1, W + T, a, d, N) and W + T == N
            # Lemma 5 triples at m in {1, d+1}, i in {1, d-1}
            for m in (1, d + 1):
                ok &= sol(m, d + 2, T + a + m, a, d, N)          # (V)
                ok &= sol(a + m, d, T + m, a, d, N)              # (IV)
                for i in (1, d - 1):
                    yv = (d + 1 - i) * a + m
                    ok &= sol(yv, i + 1, T + a + m, a, d, N)     # (Cb) alpha
                    ok &= sol(yv, i, T + m, a, d, N)             # (Cb) beta
            if not ok:
                bad.append((a, d))
    print(f"[3] range replay UB-r-gt-d (1769 pairs): {'OK' if not bad else f'FAILURES {bad[:5]}'}")
    return not bad


def check45():
    bad = []
    n = 0
    for a in range(5, 201):
        for d in range(2, a):
            c = a - d
            if c < 1 or not rado_exists(a, c):
                continue
            n += 1
            col = family_coloring(a, d)
            if len(col) != conjectured(a, c) - 1:
                bad.append(("len", a, d))
                continue
            r = a % (2 * d) or 2 * d
            t = max(d, 2 * d - r)
            pj = [j * a + t for j in range(1, d + 1)]
            for x in range(1, len(col) + 1):
                J = sum(1 for p in pj if x > p)
                w = x - a * J
                alpha = 1 if (w - 1) % (2 * d) < d else 0
                if col[x - 1] != alpha:
                    bad.append(("nf", a, d, x))
                    break
    print(f"[4,5] LB normal form + lengths ({n} pairs, a<=200): "
          f"{'OK' if not bad else f'FAILURES {bad[:5]}'}")
    return not bad


def check6_q0():
    """q=0 case of the unified r<=d theorem (= Conjecture 1): arithmetic
    identities and the two repaired range conditions, for all admissible
    q=0 pairs with d <= 80."""
    bad = 0
    n = 0
    for d in range(2, 81):
        for a in range(1, d + 1):  # q = 0 <=> a = r <= d
            r = a
            if not rado_exists(a, a - d):
                continue
            n += 1
            c = a - d
            N = (a + 3) * d + a - (r - 1)
            E = d * (a + 1)
            ok = (N == (a + 3) * (a - c) + 1)              # C1 formula
            ok &= (N - E == 2 * d + 1)                     # repaired range base
            ok &= (E + 2 * d <= N)                         # Case A far range
            Xmin = 2 * a + 2 * d + 1 - r                   # X* lower bound, s*<=d
            ok &= (a + 2 * d <= Xmin) == (a + 1 - r >= 1)  # repaired window reach
            ok &= (a + 1 - r == 1)                         # sharp at q=0
            ok &= (d + 1 - r >= 1) and (a + 2 * d + 1 - r == N - E)  # Case B
            bad += not ok
    print(f"[6] q=0 unified-theorem arithmetic ({n} pairs, d<=80): "
          f"{'OK' if not bad else f'{bad} FAILURES'}")
    return not bad


def check7_c2():
    """Conjecture 2 reflection bookkeeping: for admissible (a,c) with
    c >= a(K+2), check c' = (K+2)a - c <= 0, the existence transfer, and
    (a - c')(a+3) + 1 <= K + 1."""
    bad = 0
    n = 0
    for a in range(1, 13):
        M = a * (a + 3) + 1
        for c in range(a + 1, 4000):
            if not rado_exists(a, c):
                continue
            K = -(-(1 + c * (a + 3)) // M) - 1
            if c < a * (K + 2):
                continue
            n += 1
            cp = (K + 2) * a - c
            ok = (cp <= 0)
            ok &= (v2(a) <= v2(cp))                        # existence transfer
            ok &= ((a - cp) * (a + 3) + 1 <= K + 1)        # ceiling arithmetic
            bad += not ok
    print(f"[7] C2 reflection bookkeeping ({n} pairs, a<=12): "
          f"{'OK' if not bad else f'{bad} FAILURES'}")
    return not bad


if __name__ == "__main__":
    allok = check1() & check2() & check3() & check45() & check6_q0() & check7_c2()
    print("TOT VERIFICAT" if allok else "HI HA FALLADES")
    sys.exit(0 if allok else 1)
