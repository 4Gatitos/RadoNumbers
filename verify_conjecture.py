"""
OUR conjecture for the OPEN-SMALLC zone (0 < c < a, v2(a) <= v2(c)):

  Let d = a - c and r = a mod 2d taken in [1, 2d].
  Conjecture (July 2026):
      Rad2(1,a,-1;c) = (a+3)(a-c) + a - min(r-1, d-1)      for 2 <= d,
      Rad2(1,a,-1;a-1) = 2a + 2                            (d = 1).

Notes:
  * For a < 2d this reduces to Rad2 = (a+3)(a-c) + c + 1 (the low-c regime).
  * a = 2d (c = d) never satisfies the existence condition, so r != 2d... is
    actually possible for a > 2d; r ranges over [1, 2d].

This script (1) checks the formula against every computed small-c value,
(2) optionally computes fresh out-of-sample values and checks them too.
"""
import json
import sys
from pathlib import Path

from mine_smallc import load_smallc
from rado_core import rado_exists, rado_number

BASE = Path(__file__).parent


def conjecture(a, c):
    d = a - c
    if d == 1:
        return 2 * a + 2
    r = a % (2 * d)
    if r == 0:
        r = 2 * d
    return (a + 3) * d + a - min(r - 1, d - 1)


def check_existing():
    vals = load_smallc()
    bad = []
    for (a, c), v in sorted(vals.items()):
        if conjecture(a, c) != v:
            bad.append((a, c, v, conjecture(a, c)))
    print(f"conjecture vs computed: {len(vals)-len(bad)}/{len(vals)} agree")
    for a, c, v, p in bad:
        print(f"  MISMATCH a={a} c={c}: computed={v} conjectured={p}")
    return not bad


def out_of_sample(a_values):
    print("\nout-of-sample test (predictions made BEFORE computing):")
    total = ok = 0
    for a in a_values:
        for c in range(1, a):
            if not rado_exists(a, c):
                continue
            pred = conjecture(a, c)
            val, witness = rado_number(a, c)
            total += 1
            mark = "OK" if val == pred else "MISMATCH"
            if val == pred:
                ok += 1
            else:
                print(f"  {mark} a={a} c={c}: predicted={pred} computed={val}")
    print(f"out-of-sample: {ok}/{total} predictions correct")
    return ok == total


if __name__ == "__main__":
    good = check_existing()
    if len(sys.argv) > 1 and sys.argv[1] == "oos":
        good &= out_of_sample([33, 34, 35, 37, 38, 39, 41, 43, 45])
    sys.exit(0 if good else 1)
