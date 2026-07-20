"""
Parametric family of extremal colorings for the small-c zone (d = a-c >= 2).

With a = 2dq + r, r in [1, 2d-1] (r = 2d never satisfies existence):

  r <= d:  runs (alternating 1-run/0-run, starting with a 1-run):
           [d]*(2q+1)  +  d x ( [d+r] + [d]*(2q-1) )   with the LAST group
           extended to (2q+1); the [d+r] runs land on 0-positions.
  r > d:   s = r - d;
           [d]*(2q+2) + [s] + (d-1) x ( [d]*(2q+1) + [s] ) + [d]*(2q+2) + [s]

Total length is exactly N* = (a+3)d + a - min(r-1, d-1) - 1 (proved by
algebra in RESULTATS.md once the family is validated).
"""
from check_witness import check


def family_runs(a, d):
    two_d = 2 * d
    q, r = divmod(a, two_d)
    assert 1 <= r <= two_d - 1, "r=2d never exists"
    if r <= d:
        runs = [d] * (2 * q + 1)
        for i in range(d):
            runs.append(d + r)
            runs += [d] * ((2 * q - 1) if i < d - 1 else (2 * q + 1))
    else:
        s = r - d
        runs = [d] * (2 * q + 2) + [s]
        for _ in range(d - 1):
            runs += [d] * (2 * q + 1) + [s]
        runs += [d] * (2 * q + 2) + [s]
    return runs


def family_coloring(a, d):
    col = []
    bit = 1
    for run in family_runs(a, d):
        col += [bit] * run
        bit ^= 1
    return col


def conjectured(a, c):
    d = a - c
    r = a % (2 * d) or 2 * d
    if d == 1:
        return 2 * a + 2
    return (a + 3) * d + a - min(r - 1, d - 1)


if __name__ == "__main__":
    import sys
    from rado_core import rado_exists

    amax = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    total = ok = 0
    for a in range(5, amax + 1):
        for d in range(2, a - 0):
            c = a - d
            if c < 1 or not rado_exists(a, c):
                continue
            col = family_coloring(a, d)
            want = conjectured(a, c) - 1
            good_len = (len(col) == want)
            good_val = (check(a, c, col) is None)
            total += 1
            if good_len and good_val:
                ok += 1
            else:
                print(f"FAIL a={a} d={d}: len={len(col)} want={want} "
                      f"valid={good_val}", flush=True)
    print(f"family valid: {ok}/{total} (a <= {amax})")
