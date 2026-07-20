"""
Phase A validation gate: reproduce every exact value proved in
Dwivedi-Tripathi (Integers 20 (2020) #A36) that our grid touches.

Sources for expected values:
  P1:  c = a                                    -> Rad2 = 1
  T3+R1 (a odd): c<=0 with t=c mod a in {0,a-1}, or c <= -a(a-t-2)/2
                                                -> Rad2 = (a+3)(a-c)+1
  T4:  a | c, c <= 0                            -> Rad2 = (a+3)(a-c)+1
  T5:  c = m*a, 1 < m <= a+1                    -> Rad2 = m
  T7+R2: c > a large (see conditions)           -> Rad2 = K+1,
         K = ceil((1+c(a+3))/(1+a(a+3))) - 1
  Extra values proved in the paper's Remark 2: Rad2(1,3,-1;1)=14, Rad2(1,3,-1;2)=9.
"""
import json
import time

from rado_core import rado_number, rado_exists
from check_witness import check

CASES = [
    # (a, c, expected)
    # a = 3 (odd): T3+R1 covers ALL c <= 0; paper also proves c=1 -> 14, c=2 -> 9
    (3, -5, 49), (3, -4, 43), (3, -3, 37), (3, -2, 31), (3, -1, 25), (3, 0, 19),
    (3, 1, 14), (3, 2, 8), (3, 3, 1),
    # T5 multiples: c = m*a, 1 < m <= a+1
    (3, 6, 2), (3, 9, 3), (3, 12, 4),
    (4, 8, 2), (4, 12, 3), (4, 16, 4), (4, 20, 5),
    (5, 10, 2), (5, 15, 3), (5, 20, 4), (5, 25, 5), (5, 30, 6),
    # P1
    (4, 4, 1), (5, 5, 1), (7, 7, 1),
    # T4: a | c, c <= 0
    (4, 0, 29), (4, -4, 57), (4, -8, 85),
    (5, 0, 41), (5, -5, 81), (5, -10, 121),
    (6, 0, 55), (6, -6, 109), (6, -12, 163),
    (7, 0, 71), (7, -7, 141),
    # T3+R1, a odd, c not multiple of a:
    (5, -1, 49),   # t=4=a-1 -> any c<=0
    (5, -2, 57),   # t=3, need c <= -a(a-t-2)/2 = 0
    (5, -3, 65),   # t=2, need c <= -5(1)/2 -> c <= -2.5 OK
    (7, -1, 81),   # t=6=a-1
    (7, -6, 131),  # t=1, need c <= -7(4)/2=-14? NO -> not in validation, see below
    # T7+R2: a=3, t=0, c >= a(K+2)
    (3, 60, 19),   # K=ceil(361/19)-1=18, a(K+2)=60 <= 60 OK -> Rad2=19
    (3, 120, 38),  # K=ceil(721/19)-1=37, a(K+2)=117 <= 120 -> Rad2=38
]

# (7,-6): t=1 requires c <= -a(a-t-2)/2 = -14, so c=-6 is NOT proven -> it is
# an OPEN case (Conjecture 1 predicts 10*13+1=131). Keep it in the run but
# report it separately as a first taste of new territory.
OPEN_TASTE = {(7, -6): 131}

if __name__ == "__main__":
    fails = []
    t0 = time.time()
    results = {}
    for a, c, expected in CASES:
        t1 = time.time()
        val, witness = rado_number(a, c)
        dt = time.time() - t1
        results[(a, c)] = val
        # independent witness check
        wit_ok = True
        if val is not None and val > 1:
            wit_ok = check(a, c, witness) is None and len(witness) == val - 1
        tag = "open-case!" if (a, c) in OPEN_TASTE else ""
        status = "OK " if (val == expected and wit_ok) else "FAIL"
        if (a, c) in OPEN_TASTE:
            status = f"NEW(conj={OPEN_TASTE[(a,c)]})"
        print(f"{status} a={a:2d} c={c:4d}  Rad2={val}  expected={expected}  "
              f"witness_ok={wit_ok}  ({dt:.1f}s) {tag}", flush=True)
        if (a, c) not in OPEN_TASTE and (val != expected or not wit_ok):
            fails.append((a, c, val, expected))
    print(f"\nTotal time {time.time()-t0:.1f}s")
    if fails:
        print(f"VALIDATION FAILED on {len(fails)} cases: {fails}")
    else:
        print("VALIDATION PASSED: all proven values reproduced exactly, "
              "all witnesses independently verified.")
