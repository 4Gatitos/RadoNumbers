"""
Phase C: analysis of the sweep results.

1. Integrity: all witnesses verified, all DRAT certificates verified,
   all literature-proven zones match their formulas (continuous validation).
2. Verdict on Conjecture 1 and Conjecture 2 over the grid.
3. Pattern mining in the no-conjecture zones (OPEN-SMALLC, OPEN-MID):
   compare against candidate closed forms.
"""
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent


def ceil_div(p, q):
    return -((-p) // q)


def load():
    recs = []
    with open(BASE / "results" / "results.jsonl", encoding="utf-8") as f:
        for line in f:
            recs.append(json.loads(line))
    return [r for r in recs if r.get("zone") != "NONEXISTENT"]


def main():
    recs = load()
    print(f"{len(recs)} computed pairs\n")

    # --- integrity -------------------------------------------------------
    errors = [r for r in recs if "error" in r]
    bad_wit = [r for r in recs if not r.get("witness_ok", True)]
    bad_drat = [r for r in recs if r.get("drat_verified") is False]
    mismatch_proven = [r for r in recs if r["zone"] in ("P1", "T3R1", "T4", "T5", "T7R2")
                       and r.get("match") is False]
    print(f"errors={len(errors)}  bad_witness={len(bad_wit)}  "
          f"bad_drat={len(bad_drat)}  proven_zone_mismatches={len(mismatch_proven)}")
    for r in (errors + bad_wit + bad_drat + mismatch_proven)[:20]:
        print("  PROBLEM:", {k: r[k] for k in ("a", "c", "zone", "rad2", "predicted") if k in r})

    by_zone = defaultdict(list)
    for r in recs:
        by_zone[r["zone"]].append(r)
    print("\npairs per zone:", {z: len(v) for z, v in sorted(by_zone.items())})

    # --- Conjecture 1 ----------------------------------------------------
    c1 = by_zone.get("C1", [])
    c1_bad = [r for r in c1 if r["rad2"] != r["predicted"]]
    print(f"\nCONJECTURE 1  (c<=0: Rad2 = (a+3)(a-c)+1): "
          f"{len(c1)-len(c1_bad)}/{len(c1)} agree")
    for r in c1_bad[:20]:
        print(f"  COUNTEREXAMPLE: a={r['a']} c={r['c']} rad2={r['rad2']} "
              f"conjectured={r['predicted']}")

    # --- Conjecture 2 ----------------------------------------------------
    c2 = by_zone.get("C2", [])
    c2_bad = [r for r in c2 if r["rad2"] != r["predicted"]]
    print(f"\nCONJECTURE 2  (c>=a(K+2): Rad2 = K+1): "
          f"{len(c2)-len(c2_bad)}/{len(c2)} agree")
    for r in c2_bad[:20]:
        print(f"  COUNTEREXAMPLE: a={r['a']} c={r['c']} rad2={r['rad2']} "
              f"conjectured={r['predicted']}")

    # --- OPEN-SMALLC pattern ---------------------------------------------
    sc = sorted(by_zone.get("OPEN-SMALLC", []), key=lambda r: (r["a"], r["c"]))
    print(f"\nOPEN-SMALLC (0<c<a, no conjecture in the paper): {len(sc)} values")
    hits = defaultdict(int)
    rows = []
    for r in sc:
        a, c, v = r["a"], r["c"], r["rad2"]
        base = (a + 3) * (a - c)
        cands = {
            "(a+3)(a-c)+1": base + 1,
            "(a+3)(a-c)+2": base + 2,
            "(a+3)(a-c)+1+ceil(c/?)": None,  # placeholder
        }
        for name, val in cands.items():
            if val == v:
                hits[name] += 1
        rows.append((a, c, v, v - base))
    print("candidate formula hits:", dict(hits))
    print("  a  c  Rad2  Rad2-(a+3)(a-c)")
    for a, c, v, d in rows:
        print(f"  {a:2d} {c:3d} {v:5d}  {d:+d}")

    # --- OPEN-MID pattern -------------------------------------------------
    om = sorted(by_zone.get("OPEN-MID", []), key=lambda r: (r["a"], r["c"]))
    print(f"\nOPEN-MID (a<c<a(K+2), no conjecture): {len(om)} values")
    agree_K1 = 0
    diffs = defaultdict(int)
    for r in om:
        a, c, v = r["a"], r["c"], r["rad2"]
        K = ceil_div(1 + c * (a + 3), 1 + a * (a + 3)) - 1
        # Theorem 8 lower bound
        t8 = 0
        for lam in range(3, a + 2):
            mu = lam * a - c
            if 1 <= mu <= a + 1 - lam:
                t8 = max(t8, lam + mu)
        best_lb = max(K + 1, t8)
        if v == K + 1:
            agree_K1 += 1
        diffs[v - best_lb] += 1
    print(f"  equal to K+1 (Conjecture-2 formula): {agree_K1}/{len(om)}")
    print(f"  Rad2 - max(K+1, Thm8-LB) distribution: {dict(sorted(diffs.items()))}")
    # dump for eyeballing
    with open(BASE / "results" / "open_mid.csv", "w") as f:
        f.write("a,c,rad2,K+1,t_mod_a\n")
        for r in om:
            a, c, v = r["a"], r["c"], r["rad2"]
            K = ceil_div(1 + c * (a + 3), 1 + a * (a + 3)) - 1
            f.write(f"{a},{c},{v},{K+1},{c % a}\n")
    with open(BASE / "results" / "open_smallc.csv", "w") as f:
        f.write("a,c,rad2,base=(a+3)(a-c),delta\n")
        for a, c, v, d in rows:
            f.write(f"{a},{c},{v},{(a+3)*(a-c)},{d}\n")
    print("\nCSVs written to results/open_mid.csv and results/open_smallc.csv")


if __name__ == "__main__":
    main()
