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

The optimized BREC evaluator is independently checked against `cbx-standalone-i`. Active experiments include small-prime stripping, admissible target collapse, one signed-box traversal for both exact targets, and a cofactor prestrip prototype.

## 2. q23 Type-I-only target normal form

For a Mordell-hard prime rescued by Type I but not Type II at `k=23`, write

```text
T = (p+23)/24.
```

Then

```text
C23 = 6T,
p   = 24T-23,
T   = mR,
```

where

```text
every prime divisor of m is 1 mod 23,
Omega(R)=2,
all prime valuations of R lie in one class rho in {5,14} mod 23.
```

The two local rescue branches are exactly the same-class valuation-two states `5^2` and `14^2`.

The square and distinct-semiprime realizations of `R` are both locally compatible with all six Mordell-hard classes. Hard classes alone therefore cannot eliminate either split.

## 3. Exact predecessor corridor

The five earlier Lane-I coordinates are

```text
C3  = 6T-5,
C7  = 2(3T-2),
C11 = 3(2T-1),
C15 = 2(3T-1),
C19 = 6T-1.
```

Every predecessor now has an exact normal-form language.

### k=3

```text
MISS iff every prime divisor of 6T-5 is 1 mod 3.
```

### k=7

```text
MISS iff every prime divisor of 3T-2 is in {1,2,4} mod 7.
```

Type I and Type II have identical hit/miss status for Mordell-hard primes at this shift.

### k=11

Combined miss is either pure QR splitting modulo 11 or the exact thin primitive packet over residue classes `(2,6)` with packet

```text
(1,0), (0,1), or (1,1).
```

The same-class valuation-two packets `(2,0)` and `(0,2)` are Type-I-only rescues.

### k=15

With

```text
H=<2>={1,2,4,8} in U(15),
```

```text
MISS iff every prime divisor of 3T-1 lies in H mod 15.
```

### k=19

Write each prime valuation of `6T-1` as a discrete-log atom `a_i` to base `2` modulo 19. Define

```text
c = sum a_i mod 18,
S = sum {-a_i,0,+a_i} in Z/18Z.
```

The targets are

```text
Type II exponent = 9,
Type I exponent  = 7-c mod18.
```

Exact combined miss is

```text
9 not in S and 7-c not in S.
```

Exhaustive state closure gives

```text
439 reachable cyclic states,
136 combined-miss states,
max canonical atoms for any state = 4,
max canonical atoms for a miss     = 3.
```

The atom bound is state complexity, not a bound on `Omega(C19)`.

## 4. Pairwise-coprime predecessor core

After removing the forced factors from k7/k11/k15, define

```text
A=6T-5,
B=3T-2,
C=2T-1,
D=3T-1,
E=6T-1.
```

These five forms are pairwise coprime for every integer `T`.

Exact cancellations are

```text
A-2B=-1
A-3C=-2
A-2D=-3
A-E=-4
2B-3C=-1
B-D=-1
2B-E=-3
3C-2D=-1
3C-E=-2
2D-E=-1.
```

Parity and the fixed `1 mod3` residues remove the possible factors 2 and 3 in the non-unit rows. Therefore no cross-coordinate contradiction can rely on one prime being shared by two reduced predecessor forms.

## 5. Mandatory full-corridor regression witnesses

Two exact primes realize all five predecessor misses and then a Type-I-only construction at k23:

```text
p = 18,766,609    rho=14
p = 27,211,969    rho=5
```

Both have

```text
early BREC history = -----
k23 hit class       = Type-I-only.
```

Any proposed incompatibility theorem for the five predecessor laws is false unless it includes additional hypotheses that preserve these verified states correctly.

## 6. Current finite q23 -> k19 frontier

At the preserved finite grade

```text
p <= 30,000,000,
q23 Type-I-only,
anchored predecessor prefix ----,
```

there are exactly three candidates in the current forward census:

```text
p=18,766,609    -----    k19 miss          q23 rho=14
p=25,180,849    ----+    k19 Type-II-only  q23 rho=14
p=27,211,969    -----    k19 miss          q23 rho=5.
```

Thus the first four exact predecessor obstructions plus the q23 rescue grammar collapse the 30M branch to three primes, and k19 removes one of them.

This is finite compression only. It is not a universal three-candidate theorem.

The frontier analyzer now projects every candidate into the exact 439-state k19 automaton, including canonical state depth and atom representatives, so the finite q23 frontier can be compared directly with the 136 universal fixed-shift miss states.

## 7. Exact synthesis files

The current proof objects are:

```text
research/K3-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K7-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K11-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K15-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K19-BREC-CYCLIC-STATE-COMPRESSION.md
research/K23-TYPEI-ONLY-INTEGER-NORMAL-FORM.md
research/K23-PREDECESSOR-CORRIDOR-NORMAL-FORMS.md
research/K23-PREDECESSOR-CORE-PAIRWISE-COPRIME.md
```

with independent executable verifiers beside them.

## 8. Active proof target

The next target is **cross-coordinate compatibility**, not another isolated fixed-shift filter.

The exact object is

```text
T
 |
 +-- 6T-5   k3 semigroup
 +-- 3T-2   k7 QR semigroup
 +-- 2T-1   k11 QR/thin packet
 +-- 3T-1   k15 subgroup semigroup
 +-- 6T-1   k19 cyclic state
 +-- 6T      q23 same-class Omega-two rescue.
```

Priority questions:

1. Which of the 136 k19 miss states remain compatible with the first four exact predecessor laws and each q23 rescue class?
2. Does the k11 pure/thin branch force a restricted k19 product exponent or canonical atom family?
3. Do hard `T mod35`, q23 `rho`, and k19 cyclic state form a smaller exact quotient than any coordinate reveals?
4. What character-vector relations are forced across the pairwise-coprime affine tuple?
5. Can a genuine cross-coordinate lemma remove an infinite family without contradicting the two mandatory full-corridor witnesses?

## 9. Research discipline

The k23 coincidence falsification remains the standing rule:

```text
finite contraction
    -> candidate only
        -> adversarial extension
            -> preserve falsifier if false
            -> exact theorem + independent verifier if true
                -> only then pruning authority
```

This applies to motifs, prefix cylinders, residue patterns, state absences, and scheduler heuristics alike.

## 10. Claim boundary

The fixed-shift normal forms, pairwise-coprime theorem, q23 integer rescue normal form, and k19 finite-group state closure are exact statements with executable verification.

The 30M branch collapse is finite evidence only.

No result here proves Erdős–Straus, a universal finite Lane-I ceiling, or a complete closed decomposition method.
