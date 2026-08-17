# BREC Current Frontier

**Status:** active exact theorem / falsifier frontier  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`  
**Claim boundary:** Erdős–Straus remains open

This file records the BREC-specific frontier without replacing the broader exact research ledger in `CURRENT-FRONTIER.md`.

## 1. Exact recursive engine

The Bryan Recursive Entanglement Calculus is implemented in CBX as downstream exact Lane-I telemetry.

For each admissible shift `k = 3 mod 4`:

```text
+  iff the exact signed box hits {-1,-p^(-1)}
-  iff the exact signed box misses both targets
?  iff the application stage is undefined
```

The production-equivalent verdict order remains:

```text
W -> I -> N -> L
```

BREC does not create pruning authority by itself.

The active engine/analyzer chain is:

```text
kernel/src/cbx_brec_i.c
kernel/verify_brec_i.py
kernel/analyze_brec.py
kernel/analyze_brec_cylinder.py
kernel/analyze_brec_target.py
```

The optimized BREC evaluator is independently checked against `cbx-standalone-i` and currently uses:

```text
small-prime stripping before Pollard-rho
admissible target collapse to {-1,-p^(-1)}
one signed-box traversal for both targets
prime p>K coprimality shortcut
```

## 2. Canonical finite development census

The preserved two-million-prime development corpus used:

```text
p <= 2,000,000
k <= 80
BREC order = 8
```

with exactly:

```text
4519 Mordell-hard primes
90,380 target stages
90,380 exact factorizations
37,146 constructive stages
53,234 obstructive stages
0 undefined stages
```

The optimized BREC engine and standalone exact Lane-I reference agreed on the full finite grade.

These are regression facts, not universal statements.

## 3. Anchored ancestry versus sliding motifs

BREC now keeps two notions separate:

```text
sliding motif   = a +/- word occurring anywhere in a history
anchored prefix = a +/- word beginning at absolute shift k=3
```

For example, anchored

```text
-----
```

means exact combined misses at

```text
k = 3, 7, 11, 15, 19.
```

This distinction is required for fixed-shift theorem work.

## 4. Important falsification at k=23

The first `p <= 2,000,000` corpus showed no one-sided Type-I / Type-II state at fixed `k=23` after one or more all-negative ancestors.

That exact finite pattern does **not** generalize.

Explicit exact Type-I-only witnesses include:

```text
p =  5,151,841   early history -++-+
p =  8,243,281   early history ---++
p = 18,766,609   early history -----
p = 27,211,969   early history -----
```

Therefore no all-negative prefix of depths `1..5` forces Type-I / Type-II target coincidence at `k=23`.

Permanent falsifier guard:

```text
research/verify_k23_brec_ancestry_falsifiers.py
```

The discarded finite coincidence is documented, rather than hidden, in:

```text
research/K23-BREC-TWO-TARGET-COINCIDENCE.md
```

## 5. Exact k=3 obstruction theorem

For every Mordell-hard prime:

```text
p = 1 mod 3.
```

At `k=3`, Type I and Type II coincide at target `2 mod 3`. Hence:

```text
sigma_3(p) = -
iff
every prime divisor of C_3=(p+3)/4 is 1 mod 3.
```

Files:

```text
research/K3-BREC-OBSTRUCTION-NORMAL-FORM.md
research/verify_k3_brec_obstruction_normal_form.py
```

This is an exact first-coordinate theorem.

## 6. Exact q=23 Type-I companion normal form

Conditional on the established q23 Type-II miss normal form, the Type-I companion reduces to six residue states in primitive nonresidue classes `5` and `14` with total valuation at most two.

Exact exhaustion gives Type-I-only rescue **only** for:

```text
5^2
14^2
```

The mixed `5*14`, the valuation-one defects, and the pure quadratic branch remain Type-I misses.

Equivalently every q23 Type-I-only rescue in this normal form has:

```text
C_23 = 6HD
p    = 24HD - 23
```

where:

```text
all prime divisors of H are 1 mod 23
Omega(D)=2
all prime divisors of D are 5 mod 23
or all are 14 mod 23
```

For a Mordell-hard prime:

```text
HD mod 35 in {1,6,8,13,16,23}.
```

Files:

```text
research/K23-TYPEI-COMPANION-NORMAL-FORM.md
research/verify_k23_typei_companion_patterns.py
```

## 7. Exact bridge to the first BREC coordinate

Since:

```text
C_3 = C_23 - 5,
```

a q23 Type-I-only rescue with a leading `k=3` miss satisfies:

```text
C_23 = 6HD
p    = 24HD - 23
C_3  = 6HD - 5
```

and:

```text
every prime divisor of 6HD-5 is 1 mod 3.
```

Explicit witnesses prove that this system is realizable for both q23 rescue classes. Therefore no simple `k=3` versus `k=23` incompatibility remains.

## 8. Immediate mathematical frontier

The next exact target is to transport the remaining early shift conditions:

```text
k = 7, 11, 15, 19
```

onto the two explicit q23 rescue branches:

```text
p = 24HD - 23,
D in the 5^2 or 14^2 class.
```

The required research order is:

```text
1. derive the exact k=7 branch condition
2. generate adversarial 5^2 / 14^2 rescue candidates
3. preserve explicit counterexamples to any false contraction
4. identify only those residue/valuation restrictions that survive
5. repeat for k=11,15,19
6. promote nothing to pruning without a separate proof and verifier
```

## 9. Research discipline

The k23 coincidence episode establishes the BREC rule:

```text
finite contraction
    -> candidate only
        -> adversarial extension
            -> preserve falsifier if false
            -> exact theorem + independent verifier if true
                -> only then pruning authority
```

This applies to motifs, spectrum-conditioned absences, prefix cylinders, valuation patterns, and scheduler heuristics alike.

## 10. Claim boundary

The exact new results are:

```text
k3 BREC obstruction normal form
q23 Type-I companion six-state classification
explicit falsification of ancestry-coincidence depths 1..5
```

No result here proves Erdős–Straus, a universal finite Lane-I ceiling, or a complete closed decomposition method.
