# Exact two-colour Rado numbers of x₁ + a·x₂ − x₃ = c

Verification package and computations accompanying the note

> J. Sherzad Colet, *Exact two-colour Rado numbers of x₁ + ax₂ − x₃ = c:
> the window 0 < c < a and two conjectures of Dwivedi and Tripathi* (2026) —
> **[SherzadColet-RadoNumbers-2026.pdf](SherzadColet-RadoNumbers-2026.pdf)**
> (LaTeX sources in [`nota/`](nota/)).

For integers a ≥ 1 and c, Rad₂(a;c) is the least N such that every
2-colouring of {1,…,N} contains a monochromatic solution of
x₁ + a·x₂ − x₃ = c (repeated values allowed); it exists iff ν₂(a) ≤ ν₂(c).
The equation was studied by Dwivedi and Tripathi in *Integers* **20** (2020),
\#A36, who asked for the remaining exact values (*Integers* **25** (2025),
\#A108).

## Results

| zone | Rad₂(a;c) | status |
|---|---|---|
| c ≤ 0 | (a+3)(a−c)+1 | proved (their Conjecture 1) |
| 0 < c < a, d=1 | 2a+2 | proved |
| 0 < c < a, d≥2 | (a+3)d + a − min(r−1, d−1) | proved |
| c = a | 1 | Dwivedi–Tripathi |
| a < c < a(K+2), a∣c | c/a | proved |
| a < c < a(K+2), a∤c | no closed form; exact algorithm | announced, proofs in preparation |
| c ≥ a(K+2) | K+1 | proved (their Conjecture 2) |

Here d = a−c, r ≡ a (mod 2d) with r ∈ [1,2d], and
K = ⌈(1+c(a+3))/(1+a(a+3))⌉ − 1. See the note for precise statements.

## Every computed value is certified

For each computed pair (a,c) with Rad₂(a;c) = N:

- **Lower bound** (Rad₂ > N−1): `witnesses/a{a}_c{c}.json` contains an
  explicit valid 2-colouring of [1, N−1]. Check it without trusting any code
  in this repository:

  ```
  python check_witness.py witnesses/a7_c-6.json
  ```

  (`check_witness.py` is a ~30-line brute-force loop; it can be rewritten
  from scratch in a few minutes.)

- **Upper bound** (Rad₂ ≤ N): `certificates/rado_a{a}_c{c}_N{N}.cnf` is the
  CNF encoding (two clauses per solution triple of the equation) and
  `certificates/rado_a{a}_c{c}_N{N}.drat` a DRAT proof of its
  unsatisfiability, produced by CaDiCaL 2.1.3 and checkable with the
  standard verifier:

  ```
  drat-trim certificates/rado_a7_c-6_N131.cnf certificates/rado_a7_c-6_N131.drat
  ```

  yielding `s VERIFIED`. The CNF can be regenerated independently; two
  separately written encoders are included (`rado_core.py`,
  `reverify_all.py`).

## Repository layout

| path | contents |
|---|---|
| `nota/` | the note (LaTeX sources and PDF) |
| `rado_core.py` | SAT encoding and exact search (CaDiCaL via `python-sat`) |
| `check_witness.py` | independent brute-force witness checker |
| `certify.py` | DRAT emission and verification |
| `validate_known.py` | reproduces all 42 values proved in the 2020 paper |
| `sweep.py`, `oos_c1.py`, … | computation scripts (grids, out-of-sample tests) |
| `witnesses/`, `certificates/` | per-value certificates (see above) |
| `results/` | all computed values (`results.jsonl`, `midband.csv`, `fullband.csv`) |
| `demostracio/` | working notes and proofs for the middle-band results |
| `demostracio/verify_proofs.py` | reproduces every finite check used in the proofs |
| `midband_gen.py` | exact polynomial-time generator for the middle band |
| `verify_formula.py` | tests any candidate value function against all data |

## Requirements

Python ≥ 3.10 with `python-sat` (`pip install python-sat`). The
`drat-trim` verifier is a single C file,
[github.com/marijnheule/drat-trim](https://github.com/marijnheule/drat-trim).

## Contact

Jan Sherzad Colet — jansherzadcolet@gmail.com
