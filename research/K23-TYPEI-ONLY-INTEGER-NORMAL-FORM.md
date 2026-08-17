# k=23 Type-I-only integer normal form

**Status:** exact conditional normal form  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`  
**Claim boundary:** conditional on the proved `q=23` Type-II miss normal form; not an Erdős–Straus proof

## 1. Starting point

Let `p` be a Mordell-hard prime and put

```text
C = C_23 = (p + 23) / 4.
```

The exact `q=23` Type-II miss normal form has two branches:

1. pure quadratic splitting modulo `23`; or
2. the thin branch

```text
v_2(C) = v_3(C) = 1,
all other quadratic-residue prime factors are 1 mod 23,
primitive nonresidue classes are only 5 and 14,
total nonresidue valuation <= 2.
```

The exact Type-I companion classification already proves that a Type-II miss is rescued by Type I **if and only if** the thin defect is one of

```text
5^2
14^2.
```

This note lifts those two residue states from a finite unit-group description to a full integer factorization normal form.

---

## 2. Two multiplicative sets

Define

```text
M_23 = { m >= 1 : every prime divisor q of m satisfies q = 1 mod 23 }.
```

For `rho in {5,14}`, define

```text
S_rho^(2)
  = { R >= 1 : Omega(R)=2 and every prime divisor q of R satisfies q=rho mod 23 }.
```

Here `Omega` counts prime factors with multiplicity.

Thus every `R in S_rho^(2)` has exactly one of two shapes:

```text
square split:      R = r^2
semiprime split:   R = r*s,  r != s
```

where all displayed primes are congruent to the same `rho mod 23`.

The square and semiprime cases are the complete multiplicity split of the same-class valuation-two defect.

---

## 3. Exact normal-form theorem

Conditional on the exact `q=23` Type-II miss normal form,

```text
k=23 is Type-I-only
```

if and only if there exist

```text
rho in {5,14},
m in M_23,
R in S_rho^(2)
```

such that

```text
C = 6*m*R.
```

Equivalently,

```text
p = 24*m*R - 23.
```

Because `Omega(R)=2`, the same statement may be written more concretely as

```text
p = 24*m*r*s - 23,
```

where

```text
r,s are prime,
r = s is allowed,
r = s = rho mod 23,
rho in {5,14},
every prime divisor of m is 1 mod 23.
```

The notation `r = s = rho mod 23` means both `r` and `s` are congruent to `rho` modulo `23`; it does not require `r=s` as integers.

### Why this is exact

In the thin Type-II miss normal form, the prime factors `2` and `3` occur exactly once. Every other quadratic-residue factor must be `1 mod 23`, so their complete product is an element of `M_23`. The only Type-I-rescuing nonresidue exponent states are `(a_5,a_14)=(2,0)` and `(0,2)`. Hence the nonresidue part has exactly two prime valuations, counted with multiplicity, all in one residue class `rho=5` or `rho=14`. This is precisely `S_rho^(2)`.

Conversely, any factorization of this form realizes one of those two residue exponent states and therefore realizes the already-exhausted Type-I-only unit-group state, provided the stated `q=23` Type-II miss normal form hypotheses hold.

---

## 4. The two branches have fixed local targets

### `rho = 5`

Since

```text
5^2 = 2 mod 23,
6*5^2 = 12 mod 23,
```

we have

```text
C = 12 mod 23,
p = 4C = 2 mod 23,
Type-I target -p^(-1) = 11 mod 23.
```

The Type-II target remains

```text
-1 = 22 mod 23.
```

So the `5^2` branch has the fixed local signature

```text
Type I  : hit 11
Type II : miss 22.
```

### `rho = 14`

Similarly,

```text
14^2 = 12 mod 23,
6*14^2 = 3 mod 23,
```

so

```text
C = 3 mod 23,
p = 12 mod 23,
Type-I target -p^(-1) = 21 mod 23,
```

with Type II again missing `22`.

Thus the two integer branches are arithmetically distinct already modulo `23`:

```text
5^2 branch   : C=12, p=2,  Type-I target=11 mod 23
14^2 branch  : C=3,  p=12, Type-I target=21 mod 23.
```

---

## 5. Mordell-hard class constraint becomes a modulus-35 constraint

Write

```text
T = m*R = (p + 23) / 24.
```

For a Mordell-hard prime,

```text
p mod 840 in {1,121,169,289,361,529}.
```

Since `840 = 24*35`, the six hard classes give the exact correspondence

```text
p mod 840    T mod 35
---------------------
1               1
121             6
169             8
289            13
361            16
529            23
```

Therefore every k23 Type-I-only hard-prime candidate must satisfy

```text
m*R mod 35 in {1,6,8,13,16,23}.
```

This is not sufficient for primality or for any earlier BREC ancestry, but it is an exact congruence gate on the integer normal form.

The existing CBX spectrum partition becomes

```text
Spectrum A : T mod 35 in {1,6}
Spectrum B : T mod 35 in {8,13}
Spectrum C : T mod 35 in {16,23}.
```

---

## 6. The earlier corridor is five consecutive predecessor integers

The most useful structural simplification is independent of the residue classification.

For every earlier Lane-I shift

```text
k in {3,7,11,15,19},
```

we have

```text
C_k = (p+k)/4
    = (p+23)/4 - (23-k)/4
    = C - (23-k)/4.
```

Hence

```text
k=3   : C_3  = C-5
k=7   : C_7  = C-4
k=11  : C_11 = C-3
k=15  : C_15 = C-2
k=19  : C_19 = C-1
k=23  : C_23 = C.
```

So a full `-----` BREC ancestry ending in a k23 Type-I-only rescue is exactly a simultaneous obstruction problem on the five consecutive integers immediately preceding

```text
C = 6*m*R.
```

The corridor is therefore not six unrelated factorizations. It is the translated block

```text
6mR-5,
6mR-4,
6mR-3,
6mR-2,
6mR-1,
6mR.
```

This is the correct integer object for the next coupling step.

---

## 7. First two exact ancestry constraints

Two earlier shifts already have particularly clean exact filters.

### k=3

For Mordell-hard primes, Type I and Type II coincide at `k=3`, and the stage misses exactly when every prime factor of `C_3` is `1 mod 3`.

On the k23 rescue normal form this becomes

```text
k3 MISS
iff
every prime divisor of 6*m*R - 5 is 1 mod 3.
```

### k=7

For Mordell-hard primes there is no Type-I surplus at `k=7`; combined miss equals the exact Type-II miss. The exact q7 filter says every prime factor of `C_7` must be a quadratic residue modulo `7`.

Since

```text
C_7 = 6*m*R - 4 = 2*(3*m*R - 2)
```

and `2` is itself a quadratic residue modulo `7`, this becomes

```text
k7 MISS
iff
every prime divisor of 3*m*R - 2 lies in {1,2,4} mod 7.
```

Thus the first two negative BREC ancestors impose exact multiplicative-semigroup conditions on two consecutive affine forms in the same parameter `mR`.

That is already a more rigid object than a frequency table.

---

## 8. Explicit witnesses in the normal form

The preserved ancestry falsifiers lie exactly in this parameterization.

```text
p = 5,151,841
C = 1,287,966
C = 6 * 97 * 2213
97   = 5 mod 23
2213 = 5 mod 23
```

so this is the distinct-semiprime `5^2` branch.

```text
p = 8,243,281
C = 2,060,826
C = 6 * 37 * 9283
37   = 14 mod 23
9283 = 14 mod 23
```

so this is the distinct-semiprime `14^2` branch.

```text
p = 18,766,609
C = 4,691,658
C = 6 * 83 * 9421
83   = 14 mod 23
9421 = 14 mod 23
```

and

```text
p = 27,211,969
C = 6,802,998
C = 6 * 97 * 11689
97    = 5 mod 23
11689 = 5 mod 23.
```

The last two survive the complete earlier `-----` ancestry, proving that both same-class branches can reach the k23 Type-I-only state after five exact earlier misses.

---

## 9. What this changes in the proof search

The k23 one-sided problem has now lost almost all of its local freedom.

Instead of asking about arbitrary factorizations of `(p+23)/4`, the residual branch is

```text
p = 24*m*r*s - 23
```

with

```text
m : 23-split support, all prime factors 1 mod 23
r,s : two prime valuations in one fixed primitive-NR class, both 5 or both 14 mod 23
```

plus the six hard-class residues modulo `35` and whichever earlier consecutive-integer obstruction conditions are imposed.

The next theorem-hunting program should therefore work directly on

```text
T = m*r*s
```

and the translated corridor

```text
6T-5, 6T-4, 6T-3, 6T-2, 6T-1, 6T.
```

The immediate tasks are:

1. classify square (`r=s`) versus distinct-semiprime (`r!=s`) realizability under hard classes;
2. push the exact `k=11`, `k=15`, and `k=19` miss normal forms onto `6T-3`, `6T-2`, and `6T-1`;
3. determine whether either `rho=5` or `rho=14` branch acquires a genuine impossible character combination under the full five-predecessor ancestry;
4. preserve every explicit survivor or falsifier found while doing so.

---

## 10. Claim boundary

This note does **not** prove that every integer of the displayed form produces a prime, a Mordell-hard prime, or a five-stage BREC survivor.

It proves a conditional factorization normal form for the already-classified k23 Type-I-only state and an exact translation of the earlier Lane-I coordinates into five consecutive predecessor integers.

No finite ceiling, ancestry pruning theorem, closed decomposition method, or Erdős–Straus proof is claimed.
