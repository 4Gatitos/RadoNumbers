"""
Phase B: full sweep of Rad2(1,a,-1;c) over the grid a in [3,15], c in [-100,300].

For every existing (a,c):
  - compute the exact Rado number by SAT (rado_core),
  - verify the boundary witness with the independent brute-force checker,
  - classify the pair into proven / conjectured / no-conjecture zones,
  - compare against the paper's formula where one is proven or conjectured,
  - for pairs NOT already proven in the literature (the new results), produce a
    DRAT certificate of the UNSAT direction and verify it with drat-trim.

Zones:
  P1     c=a: Rad2=1 (proven)
  T5     c=ma, 1<m<=a+1: Rad2=m (proven)
  T4     a|c, c<=0: (a+3)(a-c)+1 (proven)
  T3R1   a odd, c<=0, t=c mod a in {0,a-1} or 2c <= -a(a-t-2): same formula (proven)
  T7R2   c>a, large (see conditions): K+1 (proven)
  C1     c<=0, remaining cases: conjectured (a+3)(a-c)+1   [Conjecture 1]
  C2     c>=a(K+2), remaining cases: conjectured K+1        [Conjecture 2]
  OPEN-SMALLC   0<c<a (no conjecture in the paper)
  OPEN-MID      a<c<a(K+2), not T5/T7R2 (no conjecture; Thm 6/8 lower bounds only)
"""
import json
import multiprocessing as mp
import os
import time
from pathlib import Path

from rado_core import rado_number, rado_exists, v2
from check_witness import check
from certify import certify_unsat

BASE = Path(__file__).parent
RESULTS = BASE / "results"
WITNESSES = BASE / "witnesses"
CERTS = BASE / "certificates"

A_MIN, A_MAX = 3, 15
C_MIN, C_MAX = -100, 300


def ceil_div(p, q):
    return -((-p) // q)


def classify(a, c):
    """-> (zone, predicted_value_or_None)"""
    if not rado_exists(a, c):
        return "NONEXISTENT", None
    if c == a:
        return "P1", 1
    if c > a:
        if c % a == 0 and 1 < c // a <= a + 1:
            return "T5", c // a
        K = ceil_div(1 + c * (a + 3), 1 + a * (a + 3)) - 1
        t = c % a
        proven = False
        # Theorem 7 as stated
        if a % 2 == 1 and 2 * c >= a * (a + 2 * K + 1):
            proven = True
        if a % 2 == 0 and c % a == 0 and c // a >= a + 2:
            proven = True
        # Remark 2 extension (t=0 case rests on Thm 4, valid for all a;
        # other cases rest on Thm 3, i.e. a odd)
        if t == 0 and c >= a * (K + 2):
            proven = True
        if a % 2 == 1 and t == a - 1 and c >= a * (K + 2):
            proven = True
        if a % 2 == 1 and t not in (0, a - 1) and 2 * c >= a * (a - t + 2 * K + 2):
            proven = True
        if proven:
            return "T7R2", K + 1
        if c >= a * (K + 2):
            return "C2", K + 1
        return "OPEN-MID", None
    if 0 < c < a:
        return "OPEN-SMALLC", None
    # c <= 0
    formula = (a + 3) * (a - c) + 1
    if c % a == 0:
        return "T4", formula
    if a % 2 == 1:
        t = c % a  # in [1, a-1]
        if t == a - 1 or 2 * c <= -a * (a - t - 2):
            return "T3R1", formula
    return "C1", formula


def is_new_result(zone):
    return zone in ("C1", "C2", "OPEN-SMALLC", "OPEN-MID")


def process_pair(job):
    a, c = job
    zone, predicted = classify(a, c)
    if zone == "NONEXISTENT":
        return {"a": a, "c": c, "zone": zone, "rad2": None}
    t0 = time.time()
    try:
        rad2, witness = rado_number(a, c)
    except Exception as e:
        return {"a": a, "c": c, "zone": zone, "error": str(e)}
    rec = {"a": a, "c": c, "zone": zone, "predicted": predicted, "rad2": rad2,
           "match": (predicted == rad2) if predicted is not None else None}
    # independent witness verification
    if rad2 > 1:
        bad = check(a, c, witness)
        rec["witness_ok"] = (bad is None) and (len(witness) == rad2 - 1)
        wf = WITNESSES / f"a{a}_c{c}.json"
        json.dump({"a": a, "c": c, "rad2": rad2, "coloring": witness},
                  open(wf, "w"), separators=(",", ":"))
        rec["witness_file"] = wf.name
    else:
        rec["witness_ok"] = True
    # DRAT certificate for every result not already proven in the literature
    if is_new_result(zone):
        try:
            ok, msg = certify_unsat(a, c, rad2, CERTS)
            rec["drat_verified"] = ok
            if not ok:
                rec["drat_msg"] = msg
        except Exception as e:
            rec["drat_verified"] = False
            rec["drat_msg"] = str(e)
    rec["seconds"] = round(time.time() - t0, 2)
    return rec


def estimated_size(job):
    a, c = job
    zone, predicted = classify(a, c)
    if predicted:
        return predicted
    return abs(a - c) * (a + 4)


if __name__ == "__main__":
    RESULTS.mkdir(exist_ok=True)
    WITNESSES.mkdir(exist_ok=True)
    CERTS.mkdir(exist_ok=True)
    jobs = [(a, c) for a in range(A_MIN, A_MAX + 1)
            for c in range(C_MIN, C_MAX + 1) if rado_exists(a, c)]
    jobs.sort(key=estimated_size, reverse=True)  # big ones first: load balance
    print(f"{len(jobs)} (a,c) pairs to compute", flush=True)
    out = open(RESULTS / "results.jsonl", "w", encoding="utf-8")
    t0 = time.time()
    done = 0
    with mp.Pool(processes=10) as pool:
        for rec in pool.imap_unordered(process_pair, jobs, chunksize=4):
            out.write(json.dumps(rec) + "\n")
            out.flush()
            done += 1
            if done % 100 == 0:
                print(f"[{done}/{len(jobs)}] {time.time()-t0:.0f}s elapsed", flush=True)
    out.close()
    print(f"DONE {done} pairs in {time.time()-t0:.0f}s", flush=True)
