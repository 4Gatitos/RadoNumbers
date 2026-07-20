"""Complete (untruncated) middle-band data for a few small a, so the Beatty
staircases are visible over their whole extent (band goes up to c ~ a^3)."""
import json
import multiprocessing as mp
from pathlib import Path

from rado_core import rado_number, rado_exists
from sweep import classify

BASE = Path(__file__).parent
A_LIST = [11, 12, 13, 14, 16]


def ceil_div(p, q):
    return -((-p) // q)


def process(job):
    a, c = job
    if not rado_exists(a, c) or classify(a, c)[0] != "OPEN-MID":
        return None
    rad2, _ = rado_number(a, c)
    M = 1 + a * (a + 3)
    K = ceil_div(1 + c * (a + 3), M) - 1
    return {"a": a, "c": c, "rad2": rad2, "K": K, "Kp1": K + 1,
            "delta": rad2 - (K + 1), "t": c % a, "lam": ceil_div(c, a),
            "mu": ceil_div(c, a) * a - c}


if __name__ == "__main__":
    jobs = []
    for a in A_LIST:
        M = 1 + a * (a + 3)
        c = a + 1
        while True:
            K = ceil_div(1 + c * (a + 3), M) - 1
            if c >= a * (K + 2):
                break
            jobs.append((a, c))
            c += 1
    print(f"{len(jobs)} full-band pairs (a in {A_LIST})", flush=True)
    recs = []
    with mp.Pool(10) as pool:
        for r in pool.imap_unordered(process, jobs, chunksize=16):
            if r:
                recs.append(r)
    recs.sort(key=lambda r: (r["a"], r["c"]))
    with open(BASE / "results" / "fullband.jsonl", "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    keys = ["a", "c", "rad2", "K", "Kp1", "delta", "t", "lam", "mu"]
    with open(BASE / "results" / "fullband.csv", "w", encoding="utf-8") as f:
        f.write(",".join(keys) + "\n")
        for r in recs:
            f.write(",".join(str(r[k]) for k in keys) + "\n")
    print(f"done: {len(recs)} OPEN-MID values", flush=True)
