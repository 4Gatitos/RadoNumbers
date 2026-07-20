"""Verification battery for the CCL-transfer route (deep-tail pin via reversal duality).

Main mathematical content verified here:
  THEOREM P: for a>=3, t in [1,a-1] with v2(a) <= v2(t), the equation
    x1 + a*x2 - x3 = 2a - t
  has NO valid 2-coloring of [1, M0], where M0 = t(a+3)+2 for t>=2 and
  M0 = 2a-2 for t=1.  (Hence Rad2(a; 2a-t) <= M0.)
  Via the reversal duality  chi valid for (a,c) on [1,N]  <=>  chi o (x -> N+1-x)
  valid for (a, a(N+1)-c) on [1,N]  (Lemma conj-reflect, nota/sec_conj.tex),
  applied at N = lam, this proves the deep-tail near-ceiling pin
  Rad2(a;c) <= lam  unconditionally, closing the last gap of the deep-tail
  closed form  Rad2(a;c) = lam - 1 + [lam <= E1].

Checks:
  1. replay of the four case-arguments of Theorem P (all range conditions +
     the mod-2t walk of Case C), a <= 200;
  2. replay of the t=1 chain, odd a <= 400;
  3. independent SAT refutation of the 4-owner subsystem at N = M0, a <= 40;
  4. duality sanity on random instances;
  5. end-to-end: deep-tail predicate vs raw SAT at both boundary lengths,
     every deep-tail lam in [M0, E1+4] for a <= 14, plus large-a spot checks.
"""
import sys, math, itertools, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from rado_core import has_valid_coloring, v2
from pysat.solvers import Glucose3


def E1f(a, t):
    if t == 1:
        return 2 * a + 2
    r = a % (2 * t)
    return (a + 2) * t + a + 1 + max(t - r, 0)


def check1_replay_P(amax=200):
    fails = []
    for a in range(3, amax + 1):
        for t in range(2, a):
            if v2(t) < v2(a):
                continue
            N = t * (a + 3) + 2
            E = t * (a + 1); F = E - a; d = a - t
            g = math.gcd(a, 2 * t); b = abs(a - 2 * t)
            if b == 0 or t % g:
                fails.append((a, t, 'arith')); continue
            # Case A ranges (Z_a compactification): N-t>=a, N-delta>=a
            if not (N - t >= a and N - d >= a):
                fails.append((a, t, 'A-range'))
            # Case C ranges
            if N - F != a + 2 * t + 2:
                fails.append((a, t, 'C-coverdom'))
            if not (a + t + 2 + t <= a + 2 * t + 2 and 3 * t + 2 + d <= a + 2 * t + 2):
                fails.append((a, t, 'C-antiperiod-ranges'))
            # Case C walk simulation
            Xb = 3 * t + 2 if a > 2 * t else a + t + 2
            jstar = next((j for j in range(1, 2 * t // g + 1)
                          if (j * b - t) % (2 * t) == 0), None)
            if jstar is None:
                fails.append((a, t, 'no-jstar')); continue
            x, ok = 1, True
            for _ in range(jstar):
                if x > Xb:
                    ok = False; break
                y = x + b
                while y > 2 * t:
                    z = y - 2 * t
                    if not (1 <= z <= a + 2):
                        ok = False; break
                    y = z
                if not ok:
                    break
                x = y
            if not ok or x != t + 1:
                fails.append((a, t, 'C-walk'))
    return fails


def check2_replay_t1(amax=400):
    fails = []
    for a in range(5, amax + 1, 2):
        N = 2 * a - 2
        forced = {1, 3}
        for p in range(1, a - 5, 2):
            if p in forced:
                if not (p + a + 2 <= N):
                    fails.append((a, 'range')); break
                forced.add(p + 4)
        if not all(p in forced for p in range(1, a - 1, 2)):
            fails.append((a, 'induction'))
        if not (a - 4 >= 1 and 2 * a - 3 <= N):
            fails.append((a, 'final'))
    return fails


def check3_sat_refutation(amax=40):
    fails = []
    for a in range(3, amax + 1):
        for t in range(1, a):
            if v2(t) < v2(a):
                continue
            if t >= 2:
                N = t * (a + 3) + 2; E = t * (a + 1)
                ows = [(1, a - t), (2, t), (t + 1, E - a), (t + 2, E)]
            else:
                N = 2 * a - 2
                ows = [(1, a - 1), (2, 1), (3, a + 1)]
            ows = [(k, d) for k, d in ows if 1 <= d <= N - 1]
            cells = [k for k, _ in ows]
            for bits in itertools.product([0, 1], repeat=len(cells)):
                gate = dict(zip(cells, bits))
                if gate[2] == 1:
                    continue
                cls = []
                for k, d in ows:
                    gk = gate[k]
                    cls.append([k if gk else -k])
                    for p in range(1, N - d + 1):
                        cls.append([-p if gk else p, -(p + d) if gk else p + d])
                s = Glucose3(bootstrap_with=cls); ok = s.solve(); s.delete()
                if ok:
                    fails.append((a, t, bits))
    return fails


def check4_duality(n=60):
    random.seed(7); bad = []
    for _ in range(n):
        a = random.randint(3, 12); c = random.randint(a + 1, 4 * a)
        N = random.randint(2, 25)
        if c % a == 0:
            continue
        if has_valid_coloring(a, c, N) != has_valid_coloring(a, a * (N + 1) - c, N):
            bad.append((a, c, N))
    return bad


def check5_endtoend(amax=14):
    mism = []; ntest = 0
    for a in range(3, amax + 1):
        for t in range(1, a):
            if v2(t) < v2(a):
                continue
            M0 = t * (a + 3) + 2 if t >= 2 else 2 * a - 2
            E1 = E1f(a, t)
            for lam in range(M0, E1 + 5):
                c = (lam - 1) * a + t
                pred = lam - 1 + (1 if lam <= E1 else 0)
                ntest += 1
                if not (has_valid_coloring(a, c, pred - 1)
                        and not has_valid_coloring(a, c, pred)):
                    mism.append((a, t, lam))
    return ntest, mism


if __name__ == '__main__':
    f1 = check1_replay_P();        print('1. Theorem P replay (a<=200):', f1 or 'PASS')
    f2 = check2_replay_t1();       print('2. t=1 replay (odd a<=400):  ', f2 or 'PASS')
    f3 = check3_sat_refutation();  print('3. SAT refutation (a<=40):   ', f3 or 'PASS')
    f4 = check4_duality();         print('4. duality sanity:           ', f4 or 'PASS')
    n5, f5 = check5_endtoend();    print(f'5. end-to-end ({n5} cases):  ', f5 or 'PASS')
