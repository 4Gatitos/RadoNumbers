"""
DRAT certification of the UNSAT direction: "every 2-coloring of [1,N] has a
monochromatic solution", i.e. Rad2(a;c) <= N.

Writes the DIMACS CNF, runs CaDiCaL 2.1.3 to produce a DRAT proof, then
verifies the proof with drat-trim. Both binaries were compiled from upstream
sources (arminbiere/cadical rel-2.1.3, marijnheule/drat-trim) with zig cc.
"""
import os
import subprocess
import sys
from pathlib import Path

from rado_core import clauses_for

# Location of the cadical / drat-trim binaries. Override with the RADO_TOOLS
# environment variable; defaults to a local ./tools directory next to this file.
TOOLS = Path(os.environ.get("RADO_TOOLS", Path(__file__).resolve().parent / "tools"))
CADICAL = TOOLS / "cadical.exe"
DRATTRIM = TOOLS / "drat-trim.exe"


def write_dimacs(a, c, N, path):
    cls = clauses_for(a, c, N)
    with open(path, "w") as f:
        f.write(f"c Rad2 upper bound instance: x1 + {a}*x2 - x3 = {c}, interval [1,{N}]\n")
        f.write(f"p cnf {N} {len(cls)}\n")
        for cl in cls:
            f.write(" ".join(map(str, cl)) + " 0\n")
    return len(cls)


def certify_unsat(a, c, N, workdir):
    """Returns (ok, msg). ok=True iff CaDiCaL reports UNSAT and drat-trim VERIFIES."""
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    cnf = workdir / f"rado_a{a}_c{c}_N{N}.cnf"
    proof = workdir / f"rado_a{a}_c{c}_N{N}.drat"
    write_dimacs(a, c, N, cnf)
    r = subprocess.run([str(CADICAL), "-q", "--no-binary", str(cnf), str(proof)],
                       capture_output=True, text=True, timeout=36000)
    if r.returncode != 20:
        return False, f"cadical exit {r.returncode} (expected 20=UNSAT): {r.stdout[-200:]}"
    v = subprocess.run([str(DRATTRIM), str(cnf), str(proof)],
                       capture_output=True, text=True, timeout=36000)
    if "s VERIFIED" not in v.stdout:
        return False, f"drat-trim did not verify: {v.stdout[-300:]}"
    return True, f"UNSAT at N={N} verified by drat-trim (proof {proof.stat().st_size} bytes)"


if __name__ == "__main__":
    a, c, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    ok, msg = certify_unsat(a, c, N, sys.argv[4] if len(sys.argv) > 4 else "certificates")
    print(msg)
    sys.exit(0 if ok else 1)
