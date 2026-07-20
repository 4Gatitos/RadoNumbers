# Draft: UB-r-gt-d

**status**: complete

## Summary

COMPLETE proof of the upper bound Rad2(a; a-d) <= N := (a+3)d + a - (d-1) = (d+1)a + 2d + 1 for the entire regime r > d (a = 2dq + d + s, 1 <= s <= d-1, q >= 0, existence condition v2(a) <= v2(a-d)). Architecture: any coloring chi of [1,N] with no monochromatic triple and chi(1)=0 must be (i) 2d-periodic on the window [1, a+d+1] (Lemma 2, proved by a +-2d ladder that composes the k=1 pair-constraint with the k=d+1 pair-constraint), (ii) color-flipped on the top block: chi(T+x) = 1-chi(x) for x in [1, a+d+1], T = d(a+1) (Lemma 3), and (iii) its window pattern phi: Z/2d -> {0,1} must be antipodal: phi(rho+d) = 1-phi(rho) (Lemma 4). Three explicit families of triples (multipliers k = d+2, k = d, and the pair k = i, i+1 squeezing one mid-interval cell) then forbid every "s-plateau" pattern in phi (Lemma 5), which forces phi to be s-antiperiodic: phi(m+s) = 1-phi(m) on Z/2d (Lemma 6, a finite combinatorial lemma). Finally, s-antiperiodicity plus antipodality force d to be a period of phi via gcd(d-s, d+s) = gcd(d,s) when v2(s) != v2(d) — and v2(s) != v2(d) is exactly equivalent to the existence condition in this regime — contradicting antipodality (Lemma 7). Hence no valid coloring of [1,N] exists. Strikingly, the 2-adic existence condition is precisely what excludes the unique family of escape patterns, explaining structurally why r = 2d never occurs. The proof was additionally implemented as an executable certificate-producing recipe and validated end-to-end: it produced a machine-verified monochromatic triple on 82,000+ colorings including all SAT-extremal length-(N-1) witnesses extended by one cell and all antipodal periodic tilings, across every in-scope (a,d) with d <= 7, a <= 60; all symbolic range conditions were mechanically replayed for 1769 in-scope parameter pairs (d <= 16, a <= 400).

## Lemma 0 (Setup, solution set, WLOG)

**Statement.** Fix d >= 2 and a with a > d, a = 2dq + r, r = d + s, 1 <= s <= d-1, q >= 0 (regime r > d), c = a - d, and assume the existence condition v2(a) <= v2(c). Put N := (a+3)d + a - (d-1) = (d+1)a + 2d + 1, T := d(a+1), W := a + d + 1; then N = T + W. The solutions (x1,x2,x3) of x1 + a*x2 - x3 = c in [1,N]^3 are exactly the triples (x, k, x + a(k-1) + d) with x, k >= 1 and x + a(k-1) + d <= N. Suppose, for contradiction, chi: [1,N] -> {0,1} contains no monochromatic solution; we may assume chi(1) = 0.

**Proof.** Solving the equation for x3 gives x3 = x1 + a(x2 - 1) + d, so with x = x1, k = x2 the solutions are exactly as stated; conversely every triple (x, k, x + a(k-1) + d) with entries in [1,N] is a solution (entries may repeat, which is allowed). The equation and the property 'monochromatic' are invariant under swapping the two colors, so if chi(1) = 1 replace chi by 1 - chi; this changes neither validity nor the existence of a monochromatic solution. Arithmetic identities: (a+3)d + a - (d-1) = ad + 3d + a - d + 1 = (d+1)a + 2d + 1; T + W = d(a+1) + a + d + 1 = (d+1)a + 2d + 1 = N. Also a = 2dq + d + s == d + s (mod 2d), and a >= d + 1 (q >= 0, s >= 1), so W = a + d + 1 >= 2d + 2 > 2d. (For q >= 1, a >= 3d + 1; the proofs below only use a >= d + 1.) All triples cited in Lemmas 1-5 below were mechanically checked to satisfy x3 = x1 + a(x2-1) + d and 1 <= x1, x2, x3 <= N at the boundary values of all free parameters, for all 1769 in-scope pairs (a,d) with d <= 16, a <= 400 (proof_replayer.py).

## Lemma 1 (Basic pair constraints R0, R1)

**Statement.** (a) chi(d+1) = 1. (b) R0: there is no x in [1, N-d] with chi(x) = chi(x+d) = 0. (c) R1: there is no x in [1, W] with chi(x) = chi(x+T) = 1.

**Proof.** (b) For x in [1, N-d], (x, 1, x+d) is a solution (x3 = x + a*0 + d). If chi(x) = chi(x+d) = 0, then since chi(1) = 0 the triple (x, 1, x+d) is monochromatic of color 0 — contradiction. (a) Apply (b) with x = 1: the triple (1, 1, 1+d) is a solution (1+d <= N), and chi(1) = 0, so chi(d+1) = 0 would make it monochromatic; hence chi(d+1) = 1. (c) For x in [1, W], (x, d+1, x+T) is a solution: x + a((d+1)-1) + d = x + ad + d = x + d(a+1) = x + T, and x + T <= W + T = N. If chi(x) = chi(x+T) = 1, then since chi(d+1) = 1 by (a), the triple (x, d+1, x+T) is monochromatic of color 1 — contradiction.

## Lemma 2 (Window periodicity)

**Statement.** There is a function phi: Z/2d -> {0,1} such that chi(x) = phi(x mod 2d) for every x in [1, W] (W = a+d+1). Moreover phi(1) = 0 and phi(d+1) = 1.

**Proof.** Claim U (up-step): if chi(x) = 0 and 1 <= x <= W - 2d, then chi(x + 2d) = 0. Proof: (i) chi(x) = 0 and x + d <= W <= N imply chi(x+d) = 1 by R0. (ii) x + d in [1, W], so R1 gives chi(x + d + T) = 0. (iii) Apply R0 at position x + d + T: it lies in [1, N - d] because (x + d + T) + d = x + 2d + T <= W + T = N (using x <= W - 2d); since chi(x + d + T) = 0, R0 gives chi(x + 2d + T) = 1. (iv) Apply R1 at position x + 2d in [1, W]: since chi(x + 2d + T) = 1, R1 forces chi(x + 2d) = 0. QED U.

Claim D (down-step): if chi(y) = 0 and 2d + 1 <= y <= W, then chi(y - 2d) = 0. Proof: (i) R0 at y - d (>= d+1 >= 1, and (y-d) + d = y <= N): chi(y) = 0 forces chi(y - d) = 1. (ii) R1 at y - d in [1, W]: chi(y - d + T) = 0. (iii) R0 at y - 2d + T (>= T + 1 >= 1, and (y - 2d + T) + d = y - d + T <= W + T = N): chi(y - d + T) = 0 forces chi(y - 2d + T) = 1. (iv) R1 at y - 2d in [1, W]: chi(y - 2d + T) = 1 forces chi(y - 2d) = 0. QED D.

Class constancy: fix rho in [1, 2d]. The members of the class {x == rho (mod 2d)} inside [1, W] are z_j = rho + 2dj, j = 0, ..., t (nonempty since rho <= 2d < W... indeed 2d <= W - 1). Suppose some member z_i has chi(z_i) = 0. Applying D repeatedly from z_i (each intermediate member is <= W and >= 2d + 1 while j >= 1) gives chi(z_j) = 0 for all j <= i, in particular chi(z_0) = chi(rho) = 0. Applying U repeatedly from z_0 (the step from z_j to z_{j+1} needs z_j <= W - 2d, which holds exactly when z_{j+1} <= W, i.e. whenever z_{j+1} is a member) gives chi(z_j) = 0 for all j <= t. Hence either all members are 0 or none is; i.e. chi is constant on each class inside [1, W]. Define phi(rho) := that constant. Then phi(1) = chi(1) = 0 and phi(d+1) = chi(d+1) = 1 by Lemma 1(a) (both positions lie in [1, W]).

## Lemma 3 (Flip on the top block)

**Statement.** For every x in [1, W]: chi(T + x) = 1 - chi(x). Consequently chi(T + x) = 1 - phi(x mod 2d) on the top block [T+1, N], which together with the window covers [1, W] and [T+1, T+W] = [T+1, N].

**Proof.** Case chi(x) = 1: R1 at x in [1, W] directly forbids chi(x + T) = 1, so chi(T + x) = 0.

Case chi(x) = 0 and x <= a + 1: (i) x + d <= a + d + 1 = W <= N, so R0 gives chi(x + d) = 1. (ii) R1 at x + d in [1, W] gives chi(x + d + T) = 0. (iii) Apply R0 at position x + T: it lies in [1, N-d] because (x + T) + d = x + d + T <= (a+1) + d + T = N; since chi(x + d + T) = 0, R0 forbids chi(x + T) = 0; hence chi(x + T) = 1.

Case chi(x) = 0 and a + 2 <= x <= W: (i) x - d >= a + 2 - d >= 1 (a >= d + 1... indeed a >= d - 1 suffices) and R0 at x - d forbids chi(x - d) = 0 = chi(x); hence chi(x - d) = 1. (ii) R1 at x - d in [1, W] gives chi(x - d + T) = 0. (iii) R0 at x - d + T (with (x - d + T) + d = x + T <= W + T = N) forbids chi(x + T) = 0; hence chi(x + T) = 1.

In all cases chi(T + x) = 1 - chi(x); by Lemma 2 chi(x) = phi(x mod 2d) for x in [1, W].

## Lemma 4 (Antipodality of the window pattern)

**Statement.** phi(rho + d) = 1 - phi(rho) for every rho in Z/2d.

**Proof.** It suffices to prove it for rho in [1, d] (the pairs {rho, rho + d} partition Z/2d). For such rho, both positions rho and rho + d lie in [1, 2d], and 2d <= W, so chi(rho) = phi(rho) and chi(rho + d) = phi(rho + d).

Not both 0: if phi(rho) = phi(rho + d) = 0 then chi(rho) = chi(rho + d) = 0 with rho <= N - d, contradicting R0.

Not both 1: if phi(rho) = phi(rho + d) = 1 then by Lemma 3, chi(T + rho) = 0 and chi(T + rho + d) = 0 (both rho and rho + d are in [1, W]). Position T + rho is in [1, N - d] since T + rho + d <= T + 2d <= T + W = N. So R0 is violated at T + rho — contradiction.

Hence exactly one of phi(rho), phi(rho + d) is 0, i.e. phi(rho + d) = 1 - phi(rho).

## Lemma 5 (Plateau conflict triples)

**Statement.** Call m in [1, d+1] an s-plateau of color kappa if phi(m) = phi(m + s) = kappa (indices mod 2d; note m + s <= 2d, so no wrap occurs). Then: (V) there is no s-plateau of color 1 - phi(2); (IV) there is no s-plateau of color 1 - phi(d); (Cb) there is no pair (i, m) with i in [1, d-1], phi(i) != phi(i+1), and m an s-plateau of color phi(i+1).

**Proof.** Throughout, use: chi = phi on [1, W] (Lemma 2), chi(T + x) = 1 - phi(x) for x in [1, W] (Lemma 3), phi(rho + d) = 1 - phi(rho) (Lemma 4), and a == d + s (mod 2d), so phi(a + m) = phi(d + s + m) = 1 - phi(m + s).

(V): Suppose phi(m) = phi(m + s) = 1 - phi(2) =: kappa for some m in [1, d+1]. Consider the triple (m, d+2, T + a + m). It is a solution: m + a((d+2) - 1) + d = m + (d+1)a + d = m + T + a, and T + a + m <= T + a + d + 1 = N; entries >= 1. Colors: chi(m) = phi(m) = kappa (m <= d + 1 <= W). chi(d+2) = phi(d+2) = 1 - phi(2) = kappa (d + 2 <= W). chi(T + (a + m)) = 1 - phi(a + m) = 1 - (1 - phi(m + s)) = phi(m + s) = kappa (a + m <= a + d + 1 = W, so Lemma 3 applies). The triple is monochromatic — contradiction.

(IV): Suppose phi(m) = phi(m + s) = 1 - phi(d) for some m in [1, d+1]. Consider the triple (a + m, d, T + m). It is a solution: (a + m) + a(d - 1) + d = da + d + m = T + m <= N; entries >= 1. Colors: chi(a + m) = phi(a + m) = 1 - phi(m + s) = phi(d) (a + m <= W). chi(d) = phi(d) (d <= W). chi(T + m) = 1 - phi(m) = 1 - (1 - phi(d)) = phi(d) (m <= W). Monochromatic of color phi(d) — contradiction.

(Cb): Suppose i in [1, d-1] with phi(i) != phi(i+1) =: kappa, and m in [1, d+1] with phi(m) = phi(m + s) = kappa. Let y := (d + 1 - i)a + m. Then 1 <= 2a + 1 <= y <= da + d + 1 = T + 1 <= N. Two triples through y:
  alpha := (y, i+1, T + a + m): a solution since y + a i + d = (d+1)a + m + d = T + a + m <= N (m <= d+1).
  beta := (y, i, T + m): a solution since y + a(i - 1) + d = da + m + d = T + m <= N.
Colors of the known cells: chi(i) = phi(i) = 1 - kappa and chi(i+1) = phi(i+1) = kappa (i + 1 <= d <= W). chi(T + a + m) = 1 - phi(a + m) = phi(m + s) = kappa (a + m <= W). chi(T + m) = 1 - phi(m) = 1 - kappa (m <= W). Now chi(y) is either kappa — making alpha monochromatic of color kappa — or 1 - kappa — making beta monochromatic of color 1 - kappa. Either way a monochromatic solution exists — contradiction.

## Lemma 6 (Rigidity: phi must be s-antiperiodic)

**Statement.** Let phi: Z/2d -> {0,1} be antipodal (phi(rho + d) = 1 - phi(rho)) with phi(1) = 0, and suppose none of (V), (IV), (Cb) of Lemma 5 occurs. Then phi(m + s) = 1 - phi(m) for ALL m in Z/2d (phi is s-antiperiodic).

**Proof.** First, if phi(m*) = phi(m* + s) for some m* in Z/2d (representative m* in [1, 2d]), then there is an s-plateau with index in [1, d+1]: if m* in [1, d+1] take m = m*; if m* in [d+2, 2d] take m = m* - d in [2, d]: by antipodality phi(m) = 1 - phi(m*) and phi(m + s) = 1 - phi(m* + s), so phi(m) = phi(m + s), an in-range s-plateau (of the opposite color).

Now suppose, for contradiction, some plateau exists; by the above the set K of colors of in-range s-plateaus (m in [1, d+1]) is nonempty. Since (V) does not occur, no in-range plateau has color 1 - phi(2); hence K = {kappa} with kappa := phi(2). Since (IV) does not occur, 1 - phi(d) is not in K, so phi(d) = kappa.

Case kappa = 1: then phi(1) = 0 != 1 = phi(2), so i = 1 (legal since d >= 2 gives 1 <= d - 1) is a transition with phi(i+1) = kappa, and an in-range plateau of color kappa exists — (Cb) occurs, contradiction.

Case kappa = 0: then phi(2) = phi(d) = 0 (and phi(1) = 0). Sub-claim: phi == 0 on [1, d]. Otherwise let j be minimal in [1, d] with phi(j) = 1; then 3 <= j <= d - 1. Since phi(d) = 0, let i be minimal in [j, d-1] with phi(i + 1) = 0; by minimality phi(i) = 1 (for i = j directly; for i > j all of phi(j..i) equal 1). Then i in [1, d-1], phi(i) != phi(i+1) = 0 = kappa, and an in-range plateau of color kappa exists — (Cb) occurs, contradiction. So phi == 0 on [1, d], hence by antipodality phi == 1 on [d+1, 2d]. But then m = d + 1 in [1, d+1] satisfies phi(d+1) = 1 and phi(d + 1 + s) = 1 (since d + 2 <= d + 1 + s <= 2d because 1 <= s <= d-1): an in-range plateau of color 1, so 1 in K = {0} — contradiction.

Both cases are impossible, so no s-plateau exists anywhere in Z/2d, i.e. phi(m + s) = 1 - phi(m) for all m. (Brute-force corroboration: for every d <= 16, every antipodal phi with phi(1) = 0 avoiding all three conflicts is s-antiperiodic — proof_replayer.py, necklace.py.)

## Lemma 7 (2-adic obstruction, existence criterion, and conclusion of the Theorem)

**Statement.** (a) In the regime r > d, the existence condition v2(a) <= v2(a - d) is equivalent to v2(s) != v2(d). (b) If v2(s) != v2(d), then no phi: Z/2d -> {0,1} can be simultaneously antipodal and s-antiperiodic. (c) THEOREM: for every d >= 2, q >= 0, s in [1, d-1] with v2(s) != v2(d) (equivalently, whenever Rad2(a; a-d) exists and r > d), every 2-coloring of [1, N], N = (a+3)d + a - (d-1), contains a monochromatic solution of x1 + a*x2 - x3 = a - d; i.e. Rad2(a; a - d) <= (a+3)d + a - (d-1).

**Proof.** (a) Write v := v2(d), w := v2(s), a = 2dq + d + s, a - d = 2dq + s, and note v2(2dq) >= v + 1 whenever q >= 1 (if q = 0 the term is absent). If w < v: v2(d + s) = w and v2(2dq) >= v + 1 > w, so v2(a) = w; likewise v2(a - d) = min-argument gives v2(a-d) = w. Hence v2(a) = v2(a - d): existence holds. If w > v: v2(d + s) = v < v2(2dq), so v2(a) = v; and v2(a - d) >= min(v+1, w) >= v + 1 > v2(a): existence holds (strictly). If w = v: write d = g d', s = g s' with g = gcd(d, s); then v2(g) = v and d', s' are both odd, so v2(d + s) >= v + 1 and hence v2(a) >= v + 1; but v2(a - d) = v2(2dq + s) = v (since v2(2dq) >= v+1 > v = v2(s)). So v2(a) > v2(a - d): existence FAILS. This proves the equivalence.

(b) Suppose phi is antipodal and s-antiperiodic: phi(x + d) = 1 - phi(x) and phi(x + s) = 1 - phi(x) for all x in Z/2d. Composing, phi(x + (d + s)) = phi(x) and phi(x + (d - s)) = phi(x): both d + s and d - s are periods. The set P of periods of phi is a subgroup of Z/2d, so P contains the subgroup generated by d - s and d + s, which is generated by h := gcd(d - s, d + s, 2d). With g = gcd(d, s), d = g d', s = g s': gcd(d - s, d + s) = g * gcd(d' - s', d' + s'), and gcd(d' - s', d' + s') divides both 2d' and 2s', hence divides 2 gcd(d', s') = 2. Since v2(s) != v2(d), d' and s' have opposite parities, so d' + s' is odd, so gcd(d' - s', d' + s') is odd, hence equals 1. Thus gcd(d - s, d + s) = g, and h = gcd(g, 2d) = g (g divides d). So g in P, and since g | d, also d in P: phi(x + d) = phi(x). But antipodality says phi(x + d) = 1 - phi(x) — contradiction.

(c) Assembly: Suppose chi: [1, N] -> {0,1} has no monochromatic solution; WLOG chi(1) = 0 (Lemma 0). Lemmas 1-4 produce the antipodal window pattern phi with phi(1) = 0. Since chi is assumed valid, none of the conflicts (V), (IV), (Cb) of Lemma 5 can occur (each produces an explicit monochromatic solution inside [1, N]). By Lemma 6, phi is s-antiperiodic. By (a)+(b), this contradicts the existence condition. Hence no such chi exists, and Rad2(a; a - d) <= N = (a+3)d + a - (d-1). Combined with the (separately verified) extremal family coloring of [1, N-1], this pins Rad2(a; a-d) = (a+3)d + a - min(r-1, d-1) in the whole regime r > d.

## Gaps
- No substantive mathematical gaps: every lemma above has a complete proof with explicit triples and range checks. Two points a referee should double-check, both mechanically corroborated: (1) the ~30 linear range inequalities (each verified symbolically in the proofs and replayed mechanically at boundary parameter values for all 1769 in-scope pairs (a,d), d <= 16, a <= 400, via proof_replayer.py); (2) Lemma 6's case analysis (independently brute-forced over all 2^(d-1) antipodal patterns for every d <= 16: the escapes are exactly the s-antiperiodic patterns, and none exist when v2(s) != v2(d)).
- Scope restrictions inherited from the task, not gaps in this proof: the companion regime r <= d is not treated here (its formula has min(r-1,d-1) = r-1 and a different extremal family), and the matching lower bound (validity of the family coloring at N-1) is taken as the separately machine-verified result mentioned in the task brief.
- Historical note for the writeup: an alternative earlier reduction (endgame at chi(a+1)) is subsumed: the endgame triple (d+1, d+2, N) is exactly conflict (V) at m = d+1, so no case split on chi(a+1) is needed in the final proof.

## Computational checks
- Sanity of the target: full constraint system UNSAT at N and SAT at N-1 confirmed by SAT solver (pysat/Minisat22) for all in-scope (a,d) with d <= 6, a <= 60, plus 12 explicit q=0 cases (d < a < 2d) — files sat_tools.py, and the q=0 spot-check in the session log.
- Structural lemma discovery/validation on real extremal colorings: for 34 cases (d <= 6), ALL valid colorings of [1, N-1] (up to 100,000 SAT models each, chi(1)=0-normalized) satisfy: window periodicity on [1, a+d] (one shorter than the length-N version, exactly as the ladder ranges predict), antipodality of phi, the flip chi(T+x) = 1-chi(x), and family phase phi(s+1) = 0 — verify_lemmas.py.
- Full mechanical replay of every arithmetic identity and range condition cited in Lemmas 0-5 (each cited triple satisfies x3 = x1 + a(x2-1) + d with all entries in [1,N], at boundary values of x, y, m, i), for all 1769 in-scope (a,d) with d <= 16, a <= 400 including q = 0 — proof_replayer.py.
- Lemma 6 brute force: for every (d, s), d <= 16, enumeration of all 2^(d-1) antipodal phi with phi(1)=0 confirms: patterns escaping conflicts (V), (IV), (Cb) are exactly the s-antiperiodic ones, they exist iff v2(s) = v2(d), and therefore none exist under the existence condition — necklace.py, proof_replayer.py; escape<->v2 equivalence violations: none.
- End-to-end executable proof: recipe.py implements the proof as a deterministic procedure that, given ANY 2-coloring of [1, N], follows the lemma chain and outputs a concrete verified monochromatic triple. It succeeded (verified triple every time, no fallback search) on 82,078 colorings: 11,520 random/structured over 192 cases (d <= 8), and 70,558 independent over 63 cases (d <= 7): every SAT-extremal valid coloring of [1, N-1] (up to 300/case) extended by both values of chi(N), the extremal family in both polarities with both extensions, all 2^(d-1) antipodal 2d-periodic tilings (these survive to Lemma 5/6, the deepest layer), and biased random colorings — recipe.py, test_recipe_independent.py.
- Formula consistency with the project repo: N = (d+1)a + 2d + 1 equals family.conjectured(a, a-d) in the regime r > d for 720 parameter combinations (d <= 16, q <= 5) — checked against family.py.
- Exploratory evidence retained for the record: exhaustive enumeration of ALL valid colorings at N-1 for (a,d) = (7,2), (11,2), (11,3) showing the rigid frame + free slack bits (enum_colorings.py, analyze_invariants.py); forcing-length profiles (forcing_profile.py); minimal multiplier subsets per case (map_ksets.py, minimal_k.py); unit-propagation traces that guided the lemma discovery (up_prover.py, trace_crux.py, zone_view.py).
