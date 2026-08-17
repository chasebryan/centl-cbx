# BREC Lane-I recursive corridor

**Status:** exact finite research language  
**Application:** `CBX-Lane-I-shift-history-v1`  
**Date:** 2026-08-17  
**Claim boundary:** theorem-hunting framework, not an Erdős–Straus proof

## 1. Purpose

The fixed-shift Erdős–Straus corridor is naturally recursive.

For a Mordell-hard prime `p`, order the Lane-I shifts

```text
k_j = 4j + 3,  j = 0,1,2,...
```

and put

```text
C_j(p) = (p + k_j) / 4.
```

Whenever `gcd(p,k_j)=1`, define the exact sign

```text
sigma_j(p) = +   if the signed box for C_j(p) hits {-1,-p^(-1)} mod k_j,
sigma_j(p) = -   otherwise.
```

If the shift is not admissible, write `?` and do not identify it with a negative sign.

The finite corridor word through `K = 4m+3` is

```text
W_K(p) = sigma_0(p) sigma_1(p) ... sigma_m(p).
```

This is the exact CBX application of the Bryan Recursive Entanglement Calculus to the Lane-I shift axis.

## 2. Why this representation is useful

The usual first-hit statistic keeps only one coordinate:

```text
k*(p) = min { k_j : sigma_j(p) = + }.
```

The recursive word retains strictly more information.

For example,

```text
----+-+
```

records that the prime missed the first four exact shifts, constructed at the fifth, missed again, and constructed again. The first-hit statistic sees only the fifth coordinate and discards the later re-entry.

This matters because the current proof program is already about interacting fixed-shift constraints. BREC gives those simultaneous constraints an explicit history address.

## 3. Two statistics that must not be confused

CBX now records two different recursive views.

### Sliding motifs

A motif such as

```text
--+
```

is counted whenever that contiguous three-sign pattern occurs **anywhere** inside a prime's Lane-I history.

These are useful for studying local transition/re-entry behavior, but they are not tied to a particular absolute shift.

### Anchored prefix cylinders

A prefix such as

```text
--+
```

in the prefix-cylinder table means specifically

```text
k=3   miss
k=7   miss
k=11  construct
```

because prefixes are anchored at the start of the corridor.

The immediate `k=23` proof program requires **anchored prefix cylinders**, not sliding motif counts. `analyze_brec.py` reports both structures separately so a local pattern at later shifts cannot be mistaken for an early-corridor population.

## 4. Prefix cylinders

For a binary word

```text
w in {+,-}^d,
```

define the finite anchored prefix cylinder

```text
C_X(w) = { p <= X : p is Mordell-hard and W_K(p) begins with w }.
```

If a `?` occurs inside the requested prefix, that prime is excluded from the binary cylinder at that depth and counted separately as an undefined-prefix exclusion.

When `p > K`, all shifts `k <= K` are automatically coprime to prime `p`, so the corridor contains no `?` positions and the prefix is literally binary.

The binary cylinders at fixed depth partition the eligible finite hard-prime corpus:

```text
C_X(w),  |w| = d.
```

They are empirical finite sets. Their occupancy or emptiness is not automatically universal.

## 5. The all-negative cylinder

The central obstruction cylinder is

```text
C_X(-^d).
```

Its elements miss every exact Lane-I shift in the first `d` corridor coordinates.

The first six coordinates are

```text
1 -> k=3
2 -> k=7
3 -> k=11
4 -> k=15
5 -> k=19
6 -> k=23
```

Thus

```text
-----+
```

means exact failure at `3,7,11,15,19` followed by exact construction at `23`.

This makes the current `k=23` continuation problem directly visible as the split

```text
-----  ->  -----+
       ->  ------
```

inside the recursive corridor.

The mathematical target is not merely to observe that one child is small. The target is to explain the split by exact arithmetic constraints inherited from the parent cylinder.

## 6. Conditional child counts

For an anchored prefix `w`, define finite child counts

```text
N_X(w+) = |C_X(w+)|,
N_X(w-) = |C_X(w-)|.
```

When their sum is nonzero, the finite constructive continuation rate is

```text
rho_X(w) = N_X(w+) / (N_X(w+) + N_X(w-)).
```

`analyze_brec.py` computes these anchored child counts from the per-prime history ledger. It separately computes sliding motif continuation rates from the motif summary.

The rate is a search heuristic only. A value near `1` suggests that the obstructive child `w-` may have a rigid exceptional grammar worth classifying. A value of exactly `1` in a finite census is still not a theorem.

## 7. Negative-run escape

For the pure anchored obstructive prefix

```text
w_r = -^r,
```

define the finite escape rate

```text
eta_X(r) = N_X(-^r +) / (N_X(-^r +) + N_X(-^(r+1))).
```

This is a direct numerical probe of how often `r` initial exact failures resolve at the next shift.

The corresponding theorem-hunting question is sharper:

> What exact factor, residue, character, valuation, or signed-box constraint distinguishes `-^r+` from `-^(r+1)`?

That is the direction in which BREC becomes useful to the proof program rather than merely descriptive.

## 8. Re-entry

BREC automatically exposes the depth-three re-entrant sliding words

```text
+-+
-+-
```

which are not among the eight selected Cross/Compass rays.

For Lane I these mean:

```text
+-+ : construct, miss, construct
-+- : miss, construct, miss
```

Their presence proves only that local exact success/failure is not monotone in the shift axis for the observed corpus. Their arithmetic classification may reveal which factor changes destroy or restore signed-box occupancy.

## 9. Spectrum conditioning

Every sliding motif and every anchored prefix cylinder is conditioned by the existing A/B/C hard-prime spectrum.

For a word `w`, CBX can therefore compare

```text
N_A(w), N_B(w), N_C(w).
```

This allows two separate questions:

1. Is a history globally rare because one spectrum suppresses it?
2. Does the same recursive prefix split differently across spectra?

A spectrum-local disappearance is more useful than a global percentage when it can be translated into an exact residue or character obstruction.

## 10. From corpus signal to theorem target

The preferred workflow is:

```text
1. census exact histories
2. find a low-entropy anchored parent prefix
3. compare its + and - children
4. recover the arithmetic state of both child populations
5. identify a candidate invariant
6. state an exact lemma
7. verify independently
8. only then use it for pruning or proof
```

This is intentionally stricter than training a scheduler directly from the finite frequencies.

## 11. Immediate corridor target

The current exact-ES frontier already singles out the continuation around `k=23`.

BREC gives a canonical data slice for that work:

```text
prefix through k=19  = first five signs
child at k=23        = sixth sign
```

The immediate experiment is therefore:

```text
isolate every prime in the ----- parent cylinder,
split it into -----+ and ------,
then compare exact factor/residue/valuation data for C_23=(p+23)/4.
```

If the negative child collapses to a small exact grammar, that grammar becomes a candidate Type-I/Type-II companion theorem at `k=23`.

If it does not collapse, the result is still useful: it falsifies the idea that the first five failures alone force a low-complexity `k=23` obstruction.

## 12. Implementation

Generate a corpus:

```sh
kernel/cbx-brec-i \
  --hi 2000000 \
  --i-max 80 \
  --order 8 \
  --histories brec-histories.tsv \
  > brec-summary.json
```

Analyze it with anchored cylinders through `k=23`:

```sh
python3 kernel/analyze_brec.py \
  brec-summary.json \
  --histories brec-histories.tsv \
  --prefix-depth 6 \
  --json > brec-analysis.json
```

Verify the optimized engine independently against the existing standalone implementation before drawing research conclusions:

```sh
python3 kernel/verify_brec_i.py \
  standalone-summary.json \
  brec-summary.json
```

The GitHub Actions `BREC recursive engine` workflow performs this exact reference check and preserves the resulting finite corpus as an artifact.

## 13. Claim boundary

A BREC word is an exact record of a finite sequence of arithmetic outcomes.

It is not, by itself:

- a counterexample certificate,
- a universal state transition law,
- a probability model for all primes,
- a pruning theorem,
- or a proof of Erdős–Straus.

Its value is that it stops CBX from throwing away the ancestry of exact successes and failures. The proof search can now ask not merely **where did a prime first construct?**, but **what exact recursive obstruction history brought it there, and what arithmetic changed at the next branch?**
