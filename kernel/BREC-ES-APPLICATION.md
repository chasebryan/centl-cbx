# BREC application contract for CBX / Erdős–Straus

**Status:** experimental exact telemetry contract  
**BREC base:** Bryan Recursive Entanglement Calculus v1.0  
**Application identity:** `CBX-Lane-I-shift-history-v1`  
**Scope:** finite CBX Lane-I research only

The Bryan Recursive Entanglement Calculus (BREC) is used in CBX as a language for **exactly observed search-state histories**. It does not replace the Erdős–Straus arithmetic, the CBX lanes, or the production-equivalent verdict order.

The invariant order remains:

```text
W -> I -> N -> L
```

BREC sits downstream of exact arithmetic and records what the arithmetic did.

## 1. Exact Lane-I state

For a Mordell-hard prime `p` and an admissible shift

```text
k = 3 mod 4,
C = (p + k) / 4,
gcd(k,p) = 1,
```

CBX evaluates the existing exact signed-box predicate

```text
delta_k(C) = 0.
```

The BREC application map is frozen for this application version:

```text
+  <=>  delta_k(C) = 0      exact constructive Lane-I certificate
-  <=>  delta_k(C) != 0     exact obstructive Lane-I miss at this shift
?  <=>  stage undefined     not a BREC sign
```

`?` is deliberately not identified with `-`. BREC v1.0 distinguishes the exhaustive formal binary history space from an application whose operators can be partial. An undefined CBX stage therefore breaks observed motif continuity.

## 2. Recursive history

For each fixed prime `p`, order admissible Lane-I shifts increasingly:

```text
3, 7, 11, 15, 19, ...
```

The evaluated signs form an observed word

```text
w_p = sigma_3 sigma_7 sigma_11 ...
```

with each defined `sigma_k` in `{+,-}`.

This is an application of the canonical BREC recursion

```text
E_empty = E
E_(w sigma) = T_sigma(E_w)
```

to exact Lane-I outcomes. The CBX engine does **not** claim that changing one observed sign causes the next sign. The ordering is a research axis over exact shift evaluations, not a physical causal assertion.

## 3. Cross and Compass projections

The Bryan Entanglement Cross is the primitive four-direction projection:

```text
right   -> +
left    -> -
up      -> +-
down    -> -+
```

The Bryan Entanglement Compass adds the four three-stage composites:

```text
UL -> +--
UR -> ++-
DL -> --+
DR -> -++
```

These eight labels are projections of the recursive history space. They are not the limit of the search language.

At depth 3 the complete BREC layer also contains

```text
+++
+-+
-+-
---
```

and at depth 4 there are 16 distinct formal words. `cbx-brec-i` therefore defaults to `--order 4`, making the first implementation explicitly larger than the eight-ray projection.

## 4. Streaming recursive closure

For one observed sign sequence, CBX does not materialize an exponential binary tree. It streams the exact sequence and counts every contiguous observed motif through depth `N`.

For each new defined sign `sigma`, the engine updates all suffixes

```text
sigma
... sigma   (depth 2)
... sigma   (depth 3)
...
... sigma   (depth N)
```

in `O(N)` time per evaluated stage.

This preserves the BREC address of every observed finite local history while keeping the profiler practical for large finite censuses.

The formal BREC space through order `N` still contains

```text
2^(N+1) - 1
```

histories including the empty word. CBX reports both that formal cardinality and the motifs actually observed in the finite corpus.

## 5. Exact signatures

With `--histories FILE`, each prime receives a finite application signature containing:

```text
p
spectrum
stage count
defined / undefined count
positive / negative count
bias = positives - negatives
reversal count
polarity parity
initial polarity
terminal polarity
first constructive k
full + / - / ? history
```

Reversal count is computed only across adjacent defined stages. An undefined stage resets adjacency, so CBX never invents a `+-` or `-+` transition across a missing evaluation.

## 6. Optimized exact evaluator

The BREC profiler contains exact optimization experiments while retaining the existing standalone Lane-I engine as the finite reference implementation.

### Small-prime stripping

Before a residual reaches the shared Miller–Rabin / Pollard-rho factorizer, `cbx-brec-i` removes a fixed prefix of small prime factors through 97.

Lane I visits consecutive values of `C` as `k` advances by 4, so small factors occur frequently. Stripping them before Pollard-rho reduces expensive residual work without changing the factorization.

### Admissible target collapse

For an admitted Lane-I stage,

```text
4C = p + k,
gcd(p,k) = 1.
```

Modulo `k`,

```text
4C = p,
C = p * 4^(-1).
```

Therefore

```text
C^(-1) = 4 * p^(-1),
-4^(-1) * C^(-1) = -p^(-1)  (mod k).
```

Also, any common divisor of `C` and `k` divides

```text
4C - k = p,
```

so admissibility already implies

```text
gcd(C,k) = 1.
```

The two exact signed-box targets can therefore be evaluated directly as

```text
{-1, -p^(-1)} mod k
```

with one modular inverse of `p`, rather than separately computing `C^(-1)` and `4^(-1)` and rechecking `gcd(C,k)`.

### One-pass dual-target signed-box traversal

The reference `delta_k(C)` test can traverse the same signed box once for `-1` and again for the Type-I target.

The BREC profiler computes the collapsed pair `{-1,-p^(-1)}` first and performs one recursive signed-box traversal whose leaf condition accepts either exact target.

### Prime admissibility shortcut

Every BREC census target `p` is already proven prime. Thus

```text
gcd(k,p) = 1  <=>  k mod p != 0.
```

When `p > K`, every positive shift `k <= K` is automatically coprime to `p`, so the inner loop performs no gcd or modulo test at all. The summary records how many stage checks used this shortcut and how many required a prime-modulus test.

### Reference equivalence

`cbx-brec-i --self-test` compares optimized factorization and collapsed-target evaluation against the shared exact implementation on fixed samples.

For a full finite census, `verify_brec_i.py` compares the optimized BREC engine against `cbx-standalone-i` and requires exact agreement on:

```text
hard-prime count
total stage visits
undefined/coprime skips
defined factorizations
constructive hit count
A/B/C constructive spectrum counts
```

These optimizations remain local to `cbx-brec-i` until equivalence and benchmark evidence justify promotion into the common kernel.

## 7. Commands

Build:

```sh
make -C kernel cbx-brec-i cbx-standalone-i
```

Self-test exact equivalence:

```sh
kernel/cbx-brec-i --self-test
```

Finite depth-4 census:

```sh
kernel/cbx-brec-i \
  --hi 1000000 \
  --i-max 400 \
  --order 4
```

Preserve per-prime recursive histories:

```sh
kernel/cbx-brec-i \
  --hi 1000000 \
  --i-max 400 \
  --order 8 \
  --histories brec-histories.tsv \
  > brec-summary.json
```

Verify the optimized census against the standalone exact reference:

```sh
kernel/cbx-standalone-i \
  --hi 1000000 \
  --i-max 400 \
  > standalone-summary.json

python3 kernel/verify_brec_i.py \
  standalone-summary.json \
  brec-summary.json
```

Analyze the recursive structure:

```sh
python3 kernel/analyze_brec.py \
  brec-summary.json \
  --histories brec-histories.tsv
```

The analyzer reports absent/present motifs through the selected depth, exact next-sign continuation counts, negative-run escape rates, re-entrant histories, deepest first constructive shifts, longest obstructive runs, reversal extrema, and spectrum-conditioned summaries.

Supported recursive motif order is currently `1..16`.

The GitHub Actions workflow `BREC recursive engine` also supports manual dispatch. A manual run accepts `hi`, `i_max`, `order`, and `segment`, performs both the optimized and reference censuses, verifies exact equivalence, analyzes the histories, and preserves the manifest/results as a workflow artifact.

## 8. Corridor interpretation

The first coordinates of a BREC Lane-I word align exactly with the current fixed-shift corridor:

```text
coordinate 1 -> k=3
coordinate 2 -> k=7
coordinate 3 -> k=11
coordinate 4 -> k=15
coordinate 5 -> k=19
coordinate 6 -> k=23
...
```

Thus a prefix such as

```text
-----+
```

means exact misses at `3,7,11,15,19` followed by a construction at `23` for that prime. A prefix of all `-` signs is a simultaneous finite corridor obstruction, not a counterexample.

For any grade with `p > K`, every shift is automatically admissible and the observed history is genuinely binary with no `?` stages. This makes high-prime finite corpora especially clean for BREC prefix-cylinder analysis.

## 9. Research questions opened by this engine

The useful questions are now richer than “which k hits most often?” Examples include:

- Which exact obstructive prefixes most often precede a construction?
- Are re-entrant histories such as `+-+` or `-+-` spectrum-dependent?
- Do long negative runs cluster by residue class or factor grammar?
- Does reversal count predict the first constructive depth?
- Which depth-4 and deeper motifs are absent from large finite corpora?
- Which negative prefixes survive exactly through `k=19` and how do they split at `k=23`?
- Do separate histories collapse onto the same exact arithmetic state signature?
- Can any observed motif exclusion be promoted from finite evidence to a theorem?

The last step is essential. A finite absent motif is a theorem-hunting signal, not a universal exclusion.

## 10. Claim boundary

BREC telemetry does not change the mathematical status of Erdős–Straus.

A `+` is an exact finite Lane-I construction at a particular shift. A `-` is an exact finite miss at that shift. A long negative history is not a counterexample. An absent finite motif is not a theorem. A scheduler suggested by motif statistics is not a proof until separately established.

The safe pipeline is:

```text
exact arithmetic
  -> exact +/-/? Lane-I history
    -> BREC signatures and motifs
      -> finite structural evidence
        -> conjecture / theorem attempt
          -> independent verification
```
