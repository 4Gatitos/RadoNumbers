"""Test the exact self-similarity: rad2(a, c+a^2) vs rad2(a, c), and whether
S = delta + lam is period-a. These are the candidate EXACT structural laws."""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
rows = []
for fn in ("fullband.csv", "midband.csv"):
    p = BASE / "results" / fn
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows.append({k: int(v) for k, v in r.items()})

val = {(r["a"], r["c"]): r["rad2"] for r in rows}

# (1) self-similarity rad2(a, c+a^2) - rad2(a,c)
diff = defaultdict(int)
n = 0
for (a, c), v in val.items():
    if (a, c + a * a) in val:
        diff[val[(a, c + a * a)] - v] += 1
        n += 1
print(f"rad2(a, c+a^2) - rad2(a,c) distribution over {n} pairs: {dict(sorted(diff.items()))}")

# (2) S = delta + lam periodic with period a? test S(lam+a) - S(lam) per (a,mu)
diag = defaultdict(dict)
for r in rows:
    diag[(r["a"], r["mu"])][r["lam"]] = r["delta"]
sdiff = defaultdict(int)
m = 0
for (a, mu), d in diag.items():
    for lam in d:
        if lam + a in d:
            S1 = d[lam] + lam
            S2 = d[lam + a] + (lam + a)
            sdiff[S2 - S1] += 1
            m += 1
print(f"S=delta+lam: S(lam+a)-S(lam) over {m} pairs: {dict(sorted(sdiff.items()))}")

# (3) restrict self-similarity to the STEEP region (delta >= a): is it exactly 0?
steep = defaultdict(int)
ns = 0
dmap = {(r["a"], r["c"]): r["delta"] for r in rows}
for (a, c), v in val.items():
    if (a, c + a * a) in val and dmap[(a, c)] >= a:
        steep[val[(a, c + a * a)] - v] += 1
        ns += 1
print(f"self-sim on steep region (delta>=a), {ns} pairs: {dict(sorted(steep.items()))}")
