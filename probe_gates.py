"""For every band witness (a<=15), extract the gate vector (colors of the
active multiplier window) and test membership in the canonical family
(ones contiguous or zeros contiguous). Informs the completeness proof shape."""
import json
from pathlib import Path

from sweep import classify
from rado_core import rado_exists

BASE = Path(__file__).parent


def gate_of(a, c, coloring):
    N = len(coloring)
    e = c - a
    klo = max(1, -(-(e - N + 1) // a) + 1)
    khi = min(N, (e + N - 1) // a + 1)
    ks = []
    for k in range(klo, khi + 1):
        s = a * (k - 1) - e
        if s != 0 and abs(s) <= N - 1:
            ks.append(k)
    return tuple(coloring[k - 1] for k in ks)


def canonical(v):
    if len(set(v)) <= 1:
        return True
    for pol in (0, 1):
        idx = [i for i, x in enumerate(v) if x == pol]
        if idx and idx[-1] - idx[0] + 1 == len(idx):
            return True
    return False


def main():
    tot = can = 0
    bad = []
    for p in (BASE / "witnesses").glob("*.json"):
        w = json.load(open(p, encoding="utf-8"))
        a, c = w["a"], w["c"]
        if c <= a or not rado_exists(a, c):
            continue
        if classify(a, c)[0] != "OPEN-MID":
            continue
        g = gate_of(a, c, w["coloring"])
        tot += 1
        if canonical(g):
            can += 1
        else:
            bad.append((a, c, "".join(map(str, g))))
    print(f"witness gates in canonical family: {can}/{tot}")
    for b in bad[:12]:
        print("  NON-CANONICAL:", b)


if __name__ == "__main__":
    main()
