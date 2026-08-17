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

The BREC profiler introduces two exact optimization experiments while retaining the original core as the reference implementation.

### Small-prime stripping

Before a residual reaches the shared Miller–Rabin / Pollard-rho factorizer, `cbx-brec-i` removes a fixed prefix of small prime factors through 97.

Lane I visits consecutive values of `C` as `k` advances by 4, so small factors occur frequently. Stripping them before Pollard-rho reduces expensive residual work without changing the factorization.

### Dual-target signed-box traversal

The existing `delta_k(C)` test asks whether the same signed box contains either of two exact residues. The reference implementation may traverse the box once for the first residue and again for the second.

The BREC profiler computes both residues first and performs one recursive signed-box traversal whose leaf condition accepts either target.

The profiler self-test compares both optimized operations against the shared exact reference implementation on fixed factorizations and Lane-I samples before finite research runs are admitted by CI.

These optimizations remain local to `cbx-brec-i` until finite equivalence and benchmark evidence justify promotion into the common kernel.

## 7. Commands

Build:

```sh
make -C kernel cbx-brec-i
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

Supported recursive motif order is currently `1..16`.

## 8. Research questions opened by this engine

The useful questions are now richer than “which k hits most often?” Examples include:

- Which exact obstructive prefixes most often precede a construction?
- Are re-entrant histories such as `+-+` or `-+-` spectrum-dependent?
- Do long negative runs cluster by residue class or factor grammar?
- Does reversal count predict the first constructive depth?
- Which depth-4 and deeper motifs are absent from large finite corpora?
- Do separate histories collapse onto the same exact arithmetic state signature?
- Can any observed motif exclusion be promoted from finite evidence to a theorem?

The last step is essential. A finite absent motif is a theorem-hunting signal, not a universal exclusion.

## 9. Claim boundary

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
