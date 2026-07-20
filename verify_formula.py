"""Universal verifier: given a candidate rad2(a,c) function, test it against
ALL computed band values (midband + fullband) and a batch of fresh
out-of-sample values. Import the candidate as `candidate` from a module named
on the command line, or edit CANDIDATE below.
"""
import csv
import importlib
import sys
from pathlib import Path

BASE = Path(__file__).parent


def load(fname):
    rows = []
    p = BASE / "results" / fname
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows.append({k: int(v) for k, v in r.items()})
    return rows


def test(candidate, rows, name):
    miss = []
    for r in rows:
        try:
            pred = candidate(r["a"], r["c"])
        except Exception as e:
            miss.append((r["a"], r["c"], r["rad2"], f"ERR:{e}"))
            continue
        if pred != r["rad2"]:
            miss.append((r["a"], r["c"], r["rad2"], pred))
    ok = len(rows) - len(miss)
    pct = 100 * ok / len(rows) if rows else 0
    print(f"  {name}: {ok}/{len(rows)} = {pct:.3f}%")
    if miss:
        print(f"    first misses (a,c,true,pred): {miss[:12]}")
    return miss


def oos(candidate):
    """Fresh values a=18..22 across the band, computed live."""
    from rado_core import rado_number, rado_exists
    from sweep import classify

    def ceil_div(p, q):
        return -((-p) // q)
    rows = []
    for a in range(18, 23):
        M = 1 + a * (a + 3)
        c = a + 1
        cmax = a + 1
        while True:
            K = ceil_div(1 + c * (a + 3), M) - 1
            if c >= a * (K + 2):
                break
            cmax = c
            c += 1
        step = max(1, (cmax - a) // 40)
        for c in list(range(a + 1, min(3 * a, cmax) + 1)) + list(range(a + 1, cmax + 1, step)):
            if rado_exists(a, c) and classify(a, c)[0] == "OPEN-MID":
                rad2, _ = rado_number(a, c)
                rows.append({"a": a, "c": c, "rad2": rad2})
    return rows


def main():
    if len(sys.argv) > 1:
        mod = importlib.import_module(sys.argv[1])
        candidate = mod.rad2 if hasattr(mod, "rad2") else mod.candidate
    else:
        from midband_gen import rad2 as candidate
    all_miss = []
    all_miss += test(candidate, load("midband.csv"), "midband a<=24")
    all_miss += test(candidate, load("fullband.csv"), "fullband a=11..16 (complete)")
    print("  computing fresh out-of-sample a=18..22 ...", flush=True)
    all_miss += test(candidate, oos(candidate), "OUT-OF-SAMPLE a=18..22")
    print("VERDICT:", "EXACT (100% everywhere)" if not all_miss
          else f"{len(all_miss)} total misses")


if __name__ == "__main__":
    main()
