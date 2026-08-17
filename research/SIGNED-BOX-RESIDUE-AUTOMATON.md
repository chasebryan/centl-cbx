# Signed-box residue automaton

**Status:** exact finite-state reduction for prime Lane-I moduli  
**Date:** 2026-08-17  
**Use:** BREC local-state classification and adversarial theorem search

## 1. Why a finite automaton exists

Fix an odd prime Lane-I modulus `q` and a primitive root `g modulo q`.

Write each prime-factor occurrence of

```text
C = product r_i
```

with multiplicity as

```text
r_i = g^(a_i),
```

where exponents live in

```text
Z/(q-1)Z.
```

The signed box of `C` consists of products in which each prime-power exponent may range from negative valuation to positive valuation.

A prime power

```text
r^e
```

can be treated exactly as `e` repeated factor occurrences of residue `r`, because

```text
{-e,-e+1,...,e}
```

is the e-fold sum of

```text
{-1,0,+1}.
```

Therefore it is enough to process one factor occurrence at a time.

---

## 2. Exact state

Represent the local signed-box state by

```text
X = (A,S),
```

where

```text
A = log_g(C) mod(q-1)
```

and `S` is the set of signed-box exponents already reachable.

The initial empty factorization is

```text
A=0,
S={0}.
```

If one new prime-factor occurrence has exponent

```text
a = log_g(r),
```

the exact transition is

```text
A' = A+a,
S' = S union (S+a) union (S-a).
```

That is a deterministic finite-state update.

The support is always inversion-symmetric:

```text
e in S  =>  -e in S.
```

It also always contains `0`.

---

## 3. Exact Lane-I targets in exponent coordinates

Because

```text
p = 4C mod q,
```

we have

```text
log_g(p) = log_g(4)+A.
```

The Type-II target is

```text
-1,
```

whose exponent is

```text
(q-1)/2.
```

The Type-I target is

```text
-p^(-1),
```

whose exponent is

```text
(q-1)/2 - log_g(4) - A
```

modulo `q-1`.

So the complete local Type-I / Type-II verdict is a function of the finite state `(A,S)`.

No factor magnitude is needed for this residue-level classification.

---

## 4. Why Type-II-miss closure can be pruned exactly

Every transition contains the old support:

```text
S subseteq S'.
```

Therefore once the Type-II exponent

```text
(q-1)/2
```

enters `S`, it can never leave under further factor occurrences.

Thus an exhaustive search for all possible Type-II misses may discard a state immediately after Type II hits.

This pruning is exact.

Type-I hits do **not** have the same monotonicity because the Type-I target moves when `A` changes. A Type-I-only intermediate residue state may later return to a combined miss while Type II remains absent.

The automaton therefore prunes only Type-II hits.

---

## 5. Finite state bound

For

```text
n=q-1,
```

a Type-II-miss support:

- contains exponent `0`;
- excludes exponent `n/2`;
- is invariant under `e -> -e`.

The remaining `n-2` exponents form

```text
(n-2)/2
```

inversion pairs.

Hence there are at most

```text
2^((n-2)/2)
```

possible inversion-symmetric Type-II-miss support masks.

Multiplying by the `n` possible values of `A` gives the elementary state bound

```text
n * 2^((n-2)/2).
```

For `q=19`,

```text
n=18,
```

so the entire abstract Type-II-miss residue universe has at most

```text
18 * 2^8 = 4608
```

states.

For `q=23`,

```text
22 * 2^10 = 22528.
```

This makes exact closure practical without a finite prime census.

---

## 6. Forced-factor seeds

A hard-prime class can supply guaranteed factor occurrences before the automaton begins.

Examples already present in the CBX program:

```text
k=7:
    forced factor 2

k=23 for Mordell-hard primes:
    forced factors 2 and 3

k=19, h121:
    forced factors 5 and 7.
```

Applying those occurrences to the initial state produces a seeded automaton.

The closure then classifies every abstract residue/multiplicity state obtainable after arbitrary additional prime factors while Type II remains absent.

This turns class-conditioned forced-factor information into an exact finite state-space reduction.

---

## 7. Regression roles

The executable automaton is

```text
research/classify_signed_box_residue_automaton.py
```

and is intended to be checked against already-understood moduli before it is trusted for a new one.

### q=7 seed 2

The forced factor `2` gives the full quadratic-residue subgroup. Any nonresidue occurrence hits Type II, and no Type-I-only state remains in the Type-II-miss closure.

### q=23 seed 2,3

The closure must recover Type-I-only residue states. The independent exact q23 companion verifier identifies the surviving normal forms as

```text
5^2
14^2.
```

### q=19 h121 seed 5,7

The seed already fills the complete quadratic-residue subgroup. Any nonresidue occurrence hits Type II, so the Type-II-miss closure has no Type-I-only state.

These three cases give positive and negative regression tests for the same state machine.

---

## 8. h169 k=19 use

The immediate difficult q23 rescue lane is

```text
p = 169 mod840,
M = 8 mod35,
C_19 = 6M-1.
```

Unlike h121, h169 has no forced factor `5` or `7` at `k=19`.

Therefore its local residue possibilities are naturally studied by the **unseeded q=19 automaton**.

The automaton does not prove that every abstract state occurs on the h169 q23 rescue family. Instead it gives a complete finite catalogue of the local residue states that are even capable of missing Type II.

The forward q23 branch generator can then be mapped into this catalogue after the exact `k=3,7,11,15` conditions are imposed.

This separates two questions cleanly:

```text
local possibility:
    exact finite residue automaton

arithmetic realization:
    q23 rescue branch + earlier BREC factor conditions.
```

That separation is the next useful reduction.

---

## 9. Research direction

For q19 the next analysis should compare:

1. every abstract combined-miss state in the unseeded automaton;
2. every abstract Type-I-only state;
3. the subset actually realized by h169 q23 rescue candidates with prefix `----`;
4. the still smaller subset realized by full `-----` witnesses.

A residue state absent from a finite candidate census is not a theorem.

A residue state absent from the **exact automaton closure** is impossible at the local signed-box level and may be used as an exact exclusion.

This distinction is precisely why the automaton is useful.

---

## 10. Claim boundary

The automaton exhausts prime-factor residue/multiplicity states modulo a fixed prime `q` from a specified forced seed.

It does not by itself enforce:

- primality of `p`;
- Mordell-hard congruences away from `q`;
- the q23 rescue normal form;
- earlier BREC obstruction conditions;
- actual existence of integer factorizations realizing every abstract state.

Those conditions belong to the arithmetic-realization layer and must remain separately verified.
