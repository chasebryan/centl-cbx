# CENTL-CBX

**CENTL-CBX is the focused proving ground for exact Erdős–Straus research, CBX kernel development, signed-box geometry, survivor-state grammars, recursive entanglement telemetry, and certificate discovery.**

This repository was split from the broader `chasebryan/centl` research tree so CBX can evolve without carrying the full historical CENTL application surface.

## Mission

CBX is an exact research machine for the Erdős–Straus problem. Its job is not to manufacture numerical confidence. Its job is to preserve proof-bearing arithmetic state, expose exact Type-I / Type-II geometry, classify obstruction and survivor structure, and capture certificates reproducibly.

The governing geometry is the full signed-box Type-II space. López Type A/B remains a useful boundary/certificate family, but it does **not** define the whole search ontology.

## Machine contract

The production-equivalent cover ordering remains:

`W -> I -> N -> L`

with lanes evaluated independently for research telemetry:

- **W** — production-equivalent cover
- **I** — governing exact Type-I / full Type-II signed-box geometry
- **N** — independent non-López research lane
- **L** — López A/B boundary diagnostics

No directional annotation, scheduler, heuristic, BEC/BREC label, motif frequency, or statistical score is permitted to create proof authority. Exact arithmetic state remains the only source of pruning and certificate validity.

## Bryan recursive entanglement layer

The Bryan Entanglement Cross is the primitive observational grammar over exact state:

- `-> (+)` constructive forward pressure
- `<- (-)` obstructive backward pressure
- `up (+/-)` expansion that may expose later obstruction
- `down (-/+)` excavation/restriction that may resolve into construction

The Bryan Entanglement Compass is the finite eight-ray composite projection. The **Bryan Recursive Entanglement Calculus (BREC)** is the unbounded binary history language behind both.

CBX now has an exact Lane-I BREC profiler:

```sh
make -C kernel cbx-brec-i cbx-standalone-i
kernel/cbx-brec-i --self-test
kernel/cbx-brec-i --hi 1000000 --i-max 400 --order 4
```

For each defined shift it records

```text
+  <=>  delta_k((p+k)/4) = 0
-  <=>  exact signed-box miss
?  <=>  undefined application stage
```

and streams every observed recursive motif through the selected order instead of collapsing a prime to one of eight directions. Default order 4 is already strictly larger than the eight-ray projection.

The optimized BREC evaluator strips small prime factors before Pollard-rho, collapses the exact targets to `{-1,-p^(-1)}`, evaluates both targets in one signed-box traversal, and avoids inner-loop gcd work when primality/admissibility already determines it. `verify_brec_i.py` cross-checks full finite censuses against the standalone exact Lane-I reference.

Recursive history analysis is available through:

```sh
python3 kernel/analyze_brec.py \
  brec-summary.json \
  --histories brec-histories.tsv \
  --prefix-depth 6
```

It reports exact finite motif occupancy, next-sign continuation counts, anchored prefix cylinders, negative-run escape rates, re-entrant histories, deepest first construction, longest obstruction runs, reversal extrema, and spectrum-conditioned summaries.

For the `k=23` continuation target, exact analyzers compare the two children of an anchored cylinder and reconstruct the fixed target through increasing earlier obstruction ancestry:

```sh
python3 kernel/analyze_brec_cylinder.py \
  brec-histories.tsv \
  --prefix='-----'

python3 kernel/analyze_brec_target.py \
  brec-histories.tsv \
  --target-k 23 \
  --max-prefix-depth 5
```

The cylinder analyzer reconstructs `C=(p+23)/4`, factors it exactly, rebuilds the signed-box support modulo 23, identifies Type-I versus Type-II target hits, measures unit-group saturation, and compares residue/factor structure between `-----+` and `------`.

### Important falsification

The initial exact `p <= 2,000,000` corpus showed Type-I / Type-II target coincidence at `k=23` after all-negative ancestry. That was an exact finite pattern, **not** a theorem. Larger exact witnesses now falsify the extrapolation at every ancestry depth 1 through 5.

Examples include:

```text
p =  5,151,841   early history -++-+   k23 Type-I-only
p =  8,243,281   early history ---++   k23 Type-I-only
p = 18,766,609   early history -----   k23 Type-I-only
p = 27,211,969   early history -----   k23 Type-I-only
```

The surviving exact reduction is sharper: conditional on the known `q=23` Type-II miss normal form, **Type-I-only rescue occurs exactly for the same-class valuation-two thin defects `5^2` and `14^2`.**

The exact guards are:

```sh
python3 research/verify_k3_brec_obstruction_normal_form.py
python3 research/verify_k23_typei_companion_patterns.py
python3 research/verify_k23_brec_ancestry_falsifiers.py
```

The `k=3` lemma is itself exact: for Mordell-hard primes, the Type-I and Type-II targets coincide modulo 3, and a `k=3` BREC miss occurs iff every prime divisor of `(p+3)/4` is `1 mod 3`.

Research notes:

- [`research/K3-BREC-OBSTRUCTION-NORMAL-FORM.md`](research/K3-BREC-OBSTRUCTION-NORMAL-FORM.md)
- [`research/K23-BREC-TWO-TARGET-COINCIDENCE.md`](research/K23-BREC-TWO-TARGET-COINCIDENCE.md)
- [`research/BREC-LANE-I-RECURSIVE-CORRIDOR.md`](research/BREC-LANE-I-RECURSIVE-CORRIDOR.md)
- [`kernel/BREC-ES-APPLICATION.md`](kernel/BREC-ES-APPLICATION.md)

The GitHub Actions **BREC recursive engine** workflow can be launched manually with a chosen `hi`, `i_max`, recursion `order`, and segment size. Pull requests exercise the exact corridor through `p <= 2,000,000`, `k <= 80`, with recursion order 8. A separate **k23 BREC companion exact checks** workflow freezes the exact q23 companion residue classification together with explicit larger falsifiers, preventing the finite two-million coincidence from being accidentally promoted later.

BREC annotates what exact arithmetic did. It does not decide whether the arithmetic is true.

## Repository layout

```text
kernel/       executable CBX research kernel, BREC engine, analyzers, verifiers
research/     exact theorem modules, falsifiers, state grammars, frontier notes
docs/         architecture, migration, and machine contracts
.github/      CI and parameterized finite research workflows
```

## Current research direction

The active program is converting the realized h169 survivor laboratory from a loose product of residue/mode coordinates into an exact dependency grammar while exposing both obstructive and constructive recursive histories. Current work includes:

- full Type-II geometry made primary over López boundary telemetry;
- exact k27 survivor grammar and factor-mode selectors;
- k31 BARE/FULL_QR normal form;
- k35 valuation/branch coupling;
- Route-B k47 THIN/FULL_QR normal form;
- ten-reservoir odd-support separation through k55;
- later-phase feedback into earlier survivor modes;
- executable theorem-state propagation;
- BREC Lane-I recursive motif telemetry beyond the finite Cross/Compass projections;
- anchored BREC corridor cylinders that retain absolute shift ancestry;
- exact finite BREC-versus-standalone equivalence verification;
- optimized small-prime stripping, collapsed `{-1,-p^(-1)}` targets, and one-pass dual-target signed-box evaluation;
- exact signed-box reconstruction inside the `k=23` obstruction cylinder;
- exact `k=3` obstruction normal form;
- exhaustive `q=23` Type-I companion classification across the six Type-II defect states;
- permanent explicit falsifiers for false BREC ancestry-coincidence extrapolations;
- parameterized preserved BREC census artifacts for repeatable theorem hunting.

## Provenance

The initial CBX corpus is being migrated from:

`github.com/chasebryan/centl` branch `agent/cbx-kernel`

Historical CENTL material remains there. New CBX-focused research should land here.

## Claim boundary

Erdős–Straus remains open. The current system is a **candidate decomposition framework / developing decomposition mechanism**, not yet a closed decomposition method or proof of the conjecture.

---

Free Computation Foundation  
Good maths should be free. Free for science.
