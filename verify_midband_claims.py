"""Verify the clean sub-results the discovery panel proposed for the middle
band, against ALL computed values (deterministic, my own check)."""
import csv
from pathlib import Path

BASE = Path(__file__).parent


def load():
    with open(BASE / "results" / "midband.csv", encoding="utf-8") as f:
        return [{k: int(v) for k, v in r.items()} for r in csv.DictReader(f)]


def rate(rows, scope, formula):
    inscope = [r for r in rows if scope(r)]
    hits = [r for r in inscope if formula(r) == r["rad2"]]
    return len(hits), len(inscope), [(r["a"], r["c"], r["rad2"], formula(r))
                                     for r in inscope if formula(r) != r["rad2"]][:8]


def main():
    rows = load()
    n = len(rows)
    print(f"{n} middle-band values\n")

    checks = [
        ("Thm6 holds: rad2 >= K+1 everywhere",
         lambda r: True, lambda r: r["rad2"] >= r["Kp1"], "ge"),
        ("NEW: mu==0 (a|c) => rad2 = K+1 = lam  [extends DT Thm 5 to whole band]",
         lambda r: r["mu"] == 0, lambda r: r["Kp1"], "eq"),
        ("check mu==0 => K+1 == lam too",
         lambda r: r["mu"] == 0, lambda r: r["lam"], "eq"),
        ("bottom edge c=a+1 (lam==2,mu==a-1): rad2 = 2a-1",
         lambda r: r["lam"] == 2 and r["c"] == r["a"] + 1,
         lambda r: 2 * r["a"] - 1, "eq"),
        ("bottom edge c=2a-1 (t==a-1,lam==2): rad2 = 2(a-1), a>=5",
         lambda r: r["lam"] == 2 and r["t"] == r["a"] - 1 and r["a"] >= 5,
         lambda r: 2 * (r["a"] - 1), "eq"),
        ("odd-a peak of lam=2 row: c=(3a-1)/2 => rad2 = (a^2+1)/2",
         lambda r: r["lam"] == 2 and r["a"] % 2 == 1 and 2 * r["c"] == 3 * r["a"] - 1,
         lambda r: (r["a"] * r["a"] + 1) // 2, "eq"),
        ("baseline max(K+1, thm8) exact fit",
         lambda r: True, lambda r: max(r["Kp1"], r["thm8"]), "eq"),
        ("rad2==K+1 share (top-of-band)",
         lambda r: True, lambda r: r["Kp1"], "eq"),
    ]
    for name, scope, formula, kind in checks:
        if kind == "ge":
            inscope = [r for r in rows if scope(r)]
            ok = sum(1 for r in inscope if formula(r))
            print(f"[{ok}/{len(inscope)}] {name}")
        else:
            h, tot, miss = rate(rows, scope, formula)
            pct = 100 * h / tot if tot else 0
            print(f"[{h}/{tot} = {pct:.1f}%] {name}")
            if miss:
                print(f"      misses: {miss}")

    # monotonicity of delta in lam for fixed (a, mu)
    from collections import defaultdict
    diag = defaultdict(list)
    for r in rows:
        diag_key = (r["a"], r["mu"])
        diag = diag_key
        diag = (r["a"], r["mu"])
        diag_list = diag
        diag = diag
        diag = diag
    diag = defaultdict(list)
    for r in rows:
        diag[(r["a"], r["mu"])].append((r["lam"], r["rad2"] - r["Kp1"]))
    viol = 0
    tot = 0
    for key, seq in diag.items():
        seq.sort()
        for i in range(1, len(seq)):
            tot += 1
            if seq[i][1] > seq[i - 1][1]:
                viol += 1
    print(f"\ndelta=rad2-(K+1) monotone non-increasing in lam (fixed a,mu): "
          f"{tot-viol}/{tot} = {100*(tot-viol)/tot:.2f}%")


if __name__ == "__main__":
    main()
