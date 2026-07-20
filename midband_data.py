"""
Rich dataset for the OPEN middle band  a < c < a(K+2).

For every existing (a,c) with c > a that classify() puts in OPEN-MID, compute
Rad2 exactly and record a feature vector for pattern mining:
  a, c, rad2, K, K+1 (= DT Theorem 6 lower bound),
  delta = rad2 - (K+1),
  t = c mod a, m_floor = c // a,
  lam, mu   (c = lam*a - mu with mu in [0, a-1], i.e. lam = ceil(c/a)),
  thm8 lower bound (max over valid (lambda,mu) of lambda+mu),
  v2(a), v2(c), gcd(a,c),
  Xexpr = (1 + c*(a+3)) mod (1 + a*(a+3))   (ceiling remainder structure).
Runs multiprocessed; writes results/midband.jsonl and a flat CSV.
"""
import json
import multiprocessing as mp
from pathlib import Path

from rado_core import rado_number, rado_exists, v2
from sweep import classify
from math import gcd

BASE = Path(__file__).parent
A_MIN, A_MAX = 3, 24


def ceil_div(p, q):
    return -((-p) // q)


def features(a, c, rad2):
    M = 1 + a * (a + 3)
    K = ceil_div(1 + c * (a + 3), M) - 1
    t = c % a
    lam = ceil_div(c, a)          # c = lam*a - mu, mu in [0, a-1]
    mu = lam * a - c
    # Theorem 8 lower bound: c = lambda*a - mu, 3<=lambda<=a+1, 1<=mu<=a+1-lambda
    t8 = 0
    for L in range(3, a + 2):
        MU = L * a - c
        if 1 <= MU <= a + 1 - L:
            t8 = max(t8, L + MU)
    return {
        "a": a, "c": c, "rad2": rad2, "K": K, "Kp1": K + 1,
        "delta": rad2 - (K + 1),
        "t": t, "m_floor": c // a, "lam": lam, "mu": mu,
        "thm8": t8, "v2a": v2(a), "v2c": v2(c), "gcd": gcd(a, c),
        "Xrem": (1 + c * (a + 3)) % M,
    }


def process(job):
    a, c = job
    zone, _ = classify(a, c)
    if zone != "OPEN-MID":
        return None
    try:
        rad2, _ = rado_number(a, c)
    except Exception as e:
        return {"a": a, "c": c, "error": str(e)}
    return features(a, c, rad2)


def size_hint(job):
    a, c = job
    return abs(c - a) * (a + 4)


if __name__ == "__main__":
    (BASE / "results").mkdir(exist_ok=True)
    jobs = []
    for a in range(A_MIN, A_MAX + 1):
        # middle band lives between c = a and c = a(K+2); K grows with c, so
        # scan a generous c-range and let classify() filter to OPEN-MID.
        for c in range(a + 1, 40 * a + 60):
            if rado_exists(a, c):
                jobs.append((a, c))
    jobs.sort(key=size_hint, reverse=True)
    print(f"{len(jobs)} candidate pairs to classify+compute", flush=True)
    recs = []
    with mp.Pool(10) as pool:
        for r in pool.imap_unordered(process, jobs, chunksize=8):
            if r is not None:
                recs.append(r)
    recs.sort(key=lambda r: (r["a"], r["c"]))
    with open(BASE / "results" / "midband.jsonl", "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    keys = ["a", "c", "rad2", "K", "Kp1", "delta", "t", "m_floor", "lam",
            "mu", "thm8", "v2a", "v2c", "gcd", "Xrem"]
    with open(BASE / "results" / "midband.csv", "w", encoding="utf-8") as f:
        f.write(",".join(keys) + "\n")
        for r in recs:
            if "error" not in r:
                f.write(",".join(str(r[k]) for k in keys) + "\n")
    errs = [r for r in recs if "error" in r]
    print(f"OPEN-MID computed: {len(recs)-len(errs)}  errors: {len(errs)}", flush=True)
