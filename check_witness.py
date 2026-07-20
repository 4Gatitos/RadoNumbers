"""
INDEPENDENT witness checker -- deliberately minimal, no SAT machinery.

A witness for "Rad2(a;c) > N" is a 2-coloring of [1,N]. This script verifies
by brute force that NO monochromatic solution of x1 + a*x2 - x3 = c exists
with x1, x2, x3 in [1,N] (values may repeat).

Usage:  python check_witness.py <witness.json>
        where witness.json = {"a": ..., "c": ..., "coloring": [c1, ..., cN]}
Exit 0 and prints OK if valid; exit 1 with the violating triple otherwise.
"""
import json
import sys


def check(a, c, coloring):
    N = len(coloring)
    col = [None] + list(coloring)  # 1-indexed
    for x1 in range(1, N + 1):
        for x2 in range(1, N + 1):
            x3 = x1 + a * x2 - c
            if 1 <= x3 <= N and col[x1] == col[x2] == col[x3]:
                return (x1, x2, x3)
    return None


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    bad = check(data["a"], data["c"], data["coloring"])
    if bad is None:
        print(f"OK: valid 2-coloring of [1,{len(data['coloring'])}] "
              f"for x1 + {data['a']}*x2 - x3 = {data['c']} "
              f"=> Rad2 > {len(data['coloring'])}")
        sys.exit(0)
    print(f"INVALID: monochromatic solution {bad}")
    sys.exit(1)
