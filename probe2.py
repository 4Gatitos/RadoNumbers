import csv
from collections import defaultdict
from pathlib import Path
from math import gcd, floor

BASE = Path(__file__).parent
rows = []
with open(BASE / "results" / "fullband.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append({k: int(v) for k, v in r.items()})

diag = defaultdict(dict)
for r in rows:
    diag[(r["a"], r["mu"])][r["lam"]] = r

# Extract drop positions & sizes for a=13, several mu; look for Beatty law
for a, mu in [(13, 5), (13, 4), (13, 3), (13, 6), (16, 5), (16, 7)]:
    d = diag[(a, mu)]
    lams = sorted(d)
    drops = []  # (lam, size)
    for i in range(1, len(lams)):
        pv = d[lams[i-1]]["delta"]; cv = d[lams[i]]["delta"]
        if cv < pv:
            drops.append((lams[i], pv - cv))
    # look at interior drops (skip first 3)
    interior = drops[2:] if len(drops) > 2 else drops
    pos = [p for p, s in interior]
    sizes = [s for p, s in interior]
    gaps = [pos[i]-pos[i-1] for i in range(1, len(pos))]
    print(f"a={a} mu={mu} (g=gcd={gcd(a,mu)}): #lam={len(lams)} maxlam={lams[-1]}")
    print(f"  interior drop sizes: {sizes[:16]}")
    print(f"  interior drop gaps : {gaps[:16]}")
    # total delta descended per full period, and period length
    print(f"  Delta0(lam=4)={d.get(4,{}).get('delta','?')}  sum sizes/period ~ a? ")
print()
# Hypothesis: within a period of length a in lam, delta drops by exactly a,
# via two drops of sizes s1,s2 (s1+s2=a) at offsets governed by mu.
# Check: is delta(lam) = C(a,mu) - (a*(lam) - correction) ... i.e. affine minus Beatty?
# Try: delta(a,mu,lam) vs  floor((Lmax - lam)*a/period)-ish
for a, mu in [(13, 5)]:
    d = diag[(a, mu)]
    lams = sorted(d)
    print(f"a={a} mu={mu} full (lam, delta):")
    print("  ", [(l, d[l]["delta"]) for l in lams])
