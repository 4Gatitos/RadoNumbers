"""Mine the middle-band dataset for structure in delta = Rad2 - (K+1)."""
import csv
from collections import defaultdict, Counter
from pathlib import Path

BASE = Path(__file__).parent


def load():
    rows = []
    with open(BASE / "results" / "midband.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: int(v) for k, v in r.items()})
    return rows


def main():
    rows = load()
    print(f"{len(rows)} middle-band values\n")

    # 1. delta distribution overall and per a
    dall = Counter(r["delta"] for r in rows)
    print("delta distribution (rad2 - (K+1)):",
          dict(sorted(dall.items())[:12]), "...\n")
    zero = sum(1 for r in rows if r["delta"] == 0)
    print(f"delta == 0 (Rad2 = K+1, DT Thm 6 bound is tight): "
          f"{zero}/{len(rows)} = {100*zero/len(rows):.1f}%\n")

    # 2. where is delta != 0? split by proximity to the lower edge c = a
    print("Among delta != 0, how close is c to a?  (band edge effect)")
    near = Counter()
    for r in rows:
        if r["delta"] != 0:
            # measure position of c in the band via lam = ceil(c/a)
            near[r["lam"]] += 1
    print("  count of delta!=0 by lam=ceil(c/a):", dict(sorted(near.items())[:12]))
    biglam = [r for r in rows if r["delta"] != 0 and r["lam"] >= 5]
    print(f"  delta!=0 with lam>=5 (well inside the band): {len(biglam)}")
    print("  sample:", [(r["a"], r["c"], r["delta"], r["Xrem"]) for r in biglam[:15]])

    # 3. hypothesis: delta != 0 only when Xrem == 0 (exact ceiling) OR lam small
    print("\nHypothesis A: for lam >= 5, delta != 0  <=>  Xrem == 0")
    bad = 0
    for r in rows:
        if r["lam"] >= 5:
            pred = (r["Xrem"] == 0)
            if (r["delta"] != 0) != pred:
                bad += 1
    tot = sum(1 for r in rows if r["lam"] >= 5)
    print(f"  fits {tot-bad}/{tot}")
    # what delta value when Xrem==0, lam>=5 ?
    xz = Counter(r["delta"] for r in rows if r["lam"] >= 5 and r["Xrem"] == 0)
    print("  delta values when Xrem==0 & lam>=5:", dict(xz))
    xnz = Counter(r["delta"] for r in rows if r["lam"] >= 5 and r["Xrem"] != 0)
    print("  delta values when Xrem!=0 & lam>=5:", dict(xnz))

    # 4. the edge layer: fix small lam, look at delta as function of (a, mu, t)
    print("\nEdge layer lam in {2,3,4}: delta by lam:")
    for L in (2, 3, 4):
        sub = [r for r in rows if r["lam"] == L]
        dc = Counter(r["delta"] for r in sub)
        print(f"  lam={L}: {len(sub)} pts, delta dist {dict(sorted(dc.items()))}")

    # 5. Refined: maybe Rad2 = max(K+1, thm8)+[Xrem==0]? test the unified guess
    print("\nHypothesis B: Rad2 = max(K+1, thm8) + (1 if Xrem==0 else 0), for lam>=3")
    bad = []
    for r in rows:
        if r["lam"] >= 3:
            pred = max(r["Kp1"], r["thm8"]) + (1 if r["Xrem"] == 0 else 0)
            if pred != r["rad2"]:
                bad.append(r)
    tot = sum(1 for r in rows if r["lam"] >= 3)
    print(f"  fits {tot-len(bad)}/{tot}")
    print("  misfits sample:", [(r["a"], r["c"], r["rad2"],
          max(r["Kp1"], r["thm8"]) + (r["Xrem"] == 0)) for r in bad[:15]])


if __name__ == "__main__":
    main()
