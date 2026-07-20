"""Out-of-sample check of Conjecture 1 (= q=0 case of our formula) beyond the
computed grid: open-window pairs with a > 15, all with existence, none proven
in the literature. Predicted BEFORE computing: Rad2 = (a+3)(a-c)+1."""
import time

from rado_core import rado_number, rado_exists
from check_witness import check

# (a, c) open cases: a odd with t=c mod a in [1,a-3] and c > -a(a-t-2)/2,
# or a even with a not dividing c (existence-filtered). All outside the grid.
CASES = [(17, -4), (21, -4), (33, -4), (21, -16), (18, -4), (14, -6),
         (26, -2), (18, -16)]

if __name__ == "__main__":
    ok = 0
    for a, c in CASES:
        assert rado_exists(a, c), (a, c)
        pred = (a + 3) * (a - c) + 1
        t0 = time.time()
        val, wit = rado_number(a, c)
        good = val == pred and check(a, c, wit) is None
        ok += good
        print(f"a={a:2d} c={c:4d}: predicted={pred} computed={val} "
              f"witness_ok={check(a, c, wit) is None} ({time.time()-t0:.1f}s)",
              flush=True)
    print(f"{ok}/{len(CASES)} out-of-sample predictions correct")
