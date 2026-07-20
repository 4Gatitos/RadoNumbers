"""
Pattern mining for the OPEN-SMALLC zone (0 < c < a).

Views:
 1. delta(a, c) = Rad2 - (a+3)(a-c) pivot table (rows a, cols c).
 2. Diagonal view d = a-c: delta as a function of a for each fixed d.
 3. Hypothesis tests:
    H1 (low regime): delta = c+1 for c <= some breakpoint(a).
    H2 (diagonals): for fixed d, delta is constant on residue classes a mod m
       for the smallest m in {1,2,4,6,8,...,2d+2} that fits.
"""
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent


def load_smallc():
    vals = {}
    for fname in ("results.jsonl", "results_smallc_ext.jsonl"):
        p = BASE / "results" / fname
        if not p.exists():
            continue
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            if r.get("zone") == "OPEN-SMALLC" and r.get("rad2"):
                vals[(r["a"], r["c"])] = r["rad2"]
    return vals


def main():
    vals = load_smallc()
    A = sorted({a for a, _ in vals})
    print(f"{len(vals)} small-c values, a in {A}\n")

    # integrity of extended batch
    ext_bad = []
    for fname in ("results_smallc_ext.jsonl",):
        p = BASE / "results" / fname
        if p.exists():
            for line in open(p, encoding="utf-8"):
                r = json.loads(line)
                if r.get("error") or r.get("witness_ok") is False or r.get("drat_verified") is False:
                    ext_bad.append(r)
    print(f"extended-batch integrity problems: {len(ext_bad)}")
    for r in ext_bad[:8]:
        print("  ", {k: r.get(k) for k in ("a", "c", "rad2", "error", "drat_msg")})

    # --- pivot on d = a - c ------------------------------------------------
    print("\ndelta = Rad2 - (a+3)(a-c), rows a, cols d = a-c:")
    dmax = max(a - c for a, c in vals)
    print("  a\\d " + "".join(f"{d:5d}" for d in range(1, dmax + 1)))
    for a in A:
        row = []
        for d in range(1, dmax + 1):
            c = a - d
            row.append(f"{vals[(a,c)] - (a+3)*d:5d}" if (a, c) in vals and c > 0 else "    .")
        print(f"  {a:3d} " + "".join(row))

    # --- H1: delta = c+1 in the low-c regime --------------------------------
    print("\nH1: delta == c+1 (i.e. Rad2 = (a+3)(a-c)+c+1). Where does it hold?")
    for a in A:
        cs = sorted(c for aa, c in vals if aa == a)
        marks = "".join("Y" if vals[(a, c)] - (a + 3) * (a - c) == c + 1 else "." for c in cs)
        print(f"  a={a:2d}: c={cs[0]}..{cs[-1]}  {marks}")

    # --- H2: per-diagonal residue fits --------------------------------------
    print("\nH2: for fixed d=a-c, smallest modulus m with delta constant per a mod m:")
    for d in range(1, dmax + 1):
        pts = sorted((a, vals[(a, a - d)]) for a, c in vals if a - c == d and c > 0)
        pts = [(a, v - (a + 3) * d) for a, v in pts]
        if len(pts) < 4:
            continue
        found = None
        for m in (1, 2, 4, 6, 8, 12):
            classes = defaultdict(set)
            for a, delta in pts:
                # try delta - a, delta, delta - c as the residue-class invariant
                classes[a % m].add(delta - a)
            if all(len(s) == 1 for s in classes.values()):
                found = (m, {r: s.pop() for r, s in sorted(classes.items())}, "delta-a")
                break
            classes = defaultdict(set)
            for a, delta in pts:
                classes[a % m].add(delta)
            if all(len(s) == 1 for s in classes.values()):
                found = (m, {r: s.pop() for r, s in sorted(classes.items())}, "delta")
                break
        n = len(pts)
        if found:
            m, table, kind = found
            print(f"  d={d:2d} ({n} pts): {kind} constant per a mod {m}: {table}")
        else:
            print(f"  d={d:2d} ({n} pts): no simple fit; data: {pts}")


if __name__ == "__main__":
    main()
