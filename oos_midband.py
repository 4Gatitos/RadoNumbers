"""Out-of-sample stress test of the middle-band findings for a beyond the
dataset (a = 25..36): the two-sided PIN and the a|c exact formula."""
from rado_core import rado_number, rado_exists
from sweep import classify


def ceil_div(p, q):
    return -((-p) // q)


def main():
    import sys
    A = list(range(25, 33))
    pin_bad, mu0_bad, thm6_bad = [], [], []
    npin = nmu0 = 0
    for a in A:
        M = 1 + a * (a + 3)
        peak = (a * a + 1) // 2
        # representative sample of the band: bottom two rows (lam=2,3, all c),
        # every a|c multiple, and a stride sample of the interior
        cands = set()
        # find band upper edge
        c = a + 1
        cmax = a + 1
        while True:
            K = ceil_div(1 + c * (a + 3), M) - 1
            if c >= a * (K + 2):
                break
            cmax = c
            c += 1
        for c in range(a + 1, min(3 * a, cmax) + 1):   # bottom rows
            cands.add(c)
        for c in range(a + 1, cmax + 1):
            if c % a == 0:                              # all multiples
                cands.add(c)
        for c in range(a + 1, cmax + 1, max(1, (cmax - a) // 20)):  # interior stride
            cands.add(c)
        for c in sorted(cands):
            K = ceil_div(1 + c * (a + 3), M) - 1
            if c >= a * (K + 2) or c <= a:
                continue
            if not (rado_exists(a, c) and classify(a, c)[0] == "OPEN-MID"):
                continue
            rad2, _ = rado_number(a, c)
            lo, hi = K + 1, max(K + 2, peak)
            npin += 1
            if not (lo <= rad2 <= hi):
                pin_bad.append((a, c, rad2, lo, hi))
            if rad2 < lo:
                thm6_bad.append((a, c, rad2, lo))
            if c % a == 0:
                nmu0 += 1
                if rad2 != c // a:
                    mu0_bad.append((a, c, rad2, c // a))
        print(f"  a={a} done ({npin} cumulative)", flush=True)
    print(f"a=25..32 open band (sampled): {npin} points tested")
    print(f"[{'OK' if not thm6_bad else 'FAIL'}] Thm6 lower bound rad2>=K+1: "
          f"{npin-len(thm6_bad)}/{npin}")
    print(f"[{'OK' if not pin_bad else 'FAIL'}] two-sided PIN "
          f"K+1<=rad2<=max(K+2,(a^2+1)/2): {npin-len(pin_bad)}/{npin}")
    if pin_bad:
        print("   PIN violations:", pin_bad[:10])
    print(f"[{'OK' if not mu0_bad else 'FAIL'}] a|c => rad2=c/a: "
          f"{nmu0-len(mu0_bad)}/{nmu0}")
    if mu0_bad:
        print("   a|c violations:", mu0_bad[:10])


if __name__ == "__main__":
    main()
