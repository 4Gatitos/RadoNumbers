"""Extended data for the OPEN-SMALLC zone (0 < c < a): push a up to 31 to
expose the piecewise structure before formulating a conjecture."""
import json
import multiprocessing as mp
import time
from pathlib import Path

from rado_core import rado_exists
from sweep import process_pair, WITNESSES, CERTS, RESULTS

if __name__ == "__main__":
    RESULTS.mkdir(exist_ok=True)
    WITNESSES.mkdir(exist_ok=True)
    CERTS.mkdir(exist_ok=True)
    jobs = [(a, c) for a in range(16, 32)
            for c in range(1, a) if rado_exists(a, c)]
    print(f"{len(jobs)} extended small-c pairs", flush=True)
    out = open(RESULTS / "results_smallc_ext.jsonl", "w", encoding="utf-8")
    t0 = time.time()
    with mp.Pool(processes=10) as pool:
        for rec in pool.imap_unordered(process_pair, jobs, chunksize=2):
            out.write(json.dumps(rec) + "\n")
            out.flush()
    out.close()
    print(f"DONE in {time.time()-t0:.0f}s", flush=True)
