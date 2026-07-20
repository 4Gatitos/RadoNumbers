"""Probe the exact staircase structure of delta = rad2-(K+1) along fixed (a,mu)
diagonals, to test whether it admits a Beatty/floor closed form."""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent


def load():
    with open(BASE / "results" / "midband.csv", encoding="utf-8") as f:
        return [{k: int(v) for k, v in r.items()} for r in csv.DictReader(f)]


def main():
    rows = load()
    diag = defaultdict(list)
    for r in rows:
        diag[(r["a"], r["mu"])].append((r["lam"], r["rad2"], r["Kp1"],
                                        r["rad2"] - r["Kp1"], r["c"]))
    for (a, mu) in [(13, 5), (13, 4), (13, 6), (11, 3), (17, 5), (16, 5)]:
        seq = sorted(diag.get((a, mu), []))
        if not seq:
            continue
        deltas = [d for (_, _, _, d, _) in seq]
        lams = [l for (l, _, _, _, _) in seq]
        # decrement sizes between consecutive lam
        decs = [deltas[i - 1] - deltas[i] for i in range(1, len(deltas))]
        print(f"a={a} mu={mu}: lam {lams[0]}..{lams[-1]}")
        print(f"  delta: {deltas}")
        print(f"  decrements: {decs}")
        print(f"  distinct decrements: {sorted(set(decs))}")
    # Focus: for a=13,mu=5, check if delta(lam) = round/floor formula.
    a, mu = 13, 5
    seq = sorted(diag[(a, mu)])
    print(f"\nDetailed a={a} mu={mu} (slope mu/a = {mu}/{a}):")
    print("  lam  c   rad2  K+1  delta   mu*(something)?")
    for (l, rad2, kp1, d, c) in seq[:25]:
        print(f"  {l:3d} {c:4d} {rad2:4d} {kp1:4d} {d:5d}")


if __name__ == "__main__":
    main()
