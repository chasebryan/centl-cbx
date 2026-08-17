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

Two exact primes first exposed the realizability of all five predecessor misses followed by a Type-I-only construction at k23:

```text
p = 18,766,609    rho=14
p = 27,211,969    rho=5
```

Both have

```text
early BREC history = -----
k23 hit class       = Type-I-only.
```

The 100M extension described below adds further full-corridor survivors, so these two are no longer the only finite examples. They remain mandatory regression witnesses because many exact normal forms were derived against them.

## 6. Current finite q23 -> k19 frontier

The initial preserved grade

```text
p <= 30,000,000,
q23 Type-I-only,
anchored predecessor prefix ----,
```

contained exactly three candidates:

```text
p=18,766,609    -----    k19 miss          q23 rho=14
p=25,180,849    ----+    k19 Type-II-only  q23 rho=14
p=27,211,969    -----    k19 miss          q23 rho=5.
```

All three happened to lie in hard class `169 mod840`. That pattern was deliberately treated as a candidate only and the same branch was extended to 100M.

### Adversarial extension through 100M

At

```text
p <= 100,000,000,
q23 Type-I-only,
anchored predecessor prefix ----,
```

the exact forward census contains nine candidates:

```text
7  k19 combined misses
1  k19 Type-I-only construction
1  k19 Type-II-only construction.
```

The nine candidates are

```text
18,766,609   mod840=169   -----   rho=14   k19 miss
25,180,849   mod840=169   ----+   rho=14   k19 Type-II-only
27,211,969   mod840=169   -----   rho=5    k19 miss
31,935,121   mod840=1     ----+   rho=14   k19 Type-I-only
35,870,641   mod840=121   -----   rho=5    k19 miss
48,224,401   mod840=1     -----   rho=5    k19 miss
49,554,961   mod840=1     -----   rho=14   k19 miss
54,831,841   mod840=1     -----   rho=5    k19 miss
85,241,521   mod840=1     -----   rho=5    k19 miss.
```

Therefore the apparent 30M implication

```text
---- q23 rescue => hard class 169
```

is false, and even the stronger observed child pattern

```text
----- q23 rescue => hard class 169
```

is false. The first full five-miss survivor outside class169 is

```text
p=35,870,641 = 121 mod840.
```

This falsification is preserved in `Q23-K19-100M-FINITE-FRONTIER.md` together with the exact workflow run and artifact digest.

The seven 100M k19 misses occupy six distinct cyclic states:

```text
14:05551
8:00501
6:15555
4:15555
2:15555
2:15055.
```

Their canonical state depths remain at most three, exactly as required by the universal fixed-shift k19 state theorem.

The 100M result is finite compression and finite falsification only. It is not a universal nine-candidate theorem.

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
research/Q23-K19-100M-FINITE-FRONTIER.md
```

with independent executable verifiers beside the exact theorem modules.

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

The 100M falsifier makes the next quotient clearer: hard class alone is too weak. Priority questions are now:

1. Which of the 136 k19 combined-miss states remain arithmetically realizable after the first four exact predecessor laws and each q23 rescue class?
2. Does the k11 pure/thin branch force a restricted k19 product exponent or canonical atom family?
3. Does the joint signature `(T mod35, q23 rho, k11 branch, k19 state)` admit an exact compression not visible in any coordinate separately?
4. What character-vector relations are forced across the pairwise-coprime affine tuple?
5. Can a genuine cross-coordinate lemma remove an infinite family while preserving every explicit 100M full-corridor survivor?

## 9. Research discipline

The k23 coincidence and 30M hard-class falsifications reinforce the standing rule:

```text
finite contraction
    -> candidate only
        -> adversarial extension
            -> preserve falsifier if false
            -> exact theorem + independent verifier if true
                -> only then pruning authority
```

This applies to motifs, prefix cylinders, residue patterns, state absences, hard-class patterns, and scheduler heuristics alike.

## 10. Claim boundary

The fixed-shift normal forms, pairwise-coprime theorem, q23 integer rescue normal form, and k19 finite-group state closure are exact statements with executable verification.

The 30M and 100M branch collapses are finite evidence only. The 100M run also supplies a finite falsifier to the 30M hard-class pattern.

No result here proves Erdős–Straus, a universal finite Lane-I ceiling, or a complete closed decomposition method.
