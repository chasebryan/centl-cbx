# Lane-I divisor-square duality

**Status:** exact arithmetic identity  
**Date:** 2026-08-17  
**Scope:** admissible Lane-I signed-box evaluation

## 1. Signed box

Let

```text
C = product q_i^(e_i)
```

with

```text
gcd(C,k)=1.
```

The Lane-I signed box is

```text
B_k(C)
=
{ product q_i^(z_i) mod k : -e_i <= z_i <= e_i }.
```

Negative exponents are well-defined because every factor of `C` is a unit modulo `k`.

---

## 2. Replace signed exponents by divisors of C^2

For one signed exponent vector `z_i`, put

```text
d_i = e_i-z_i.
```

Then

```text
0 <= d_i <= 2e_i.
```

Define

```text
D = product q_i^(d_i).
```

Exactly those exponent bounds say

```text
D divides C^2.
```

Also

```text
product q_i^(z_i)
=
product q_i^(e_i-d_i)
=
C / D.
```

Therefore the signed box has the exact divisor-square representation

```text
B_k(C)
=
{ C D^(-1) mod k : D divides C^2 }.
```

This is a bijective change of exponent coordinates.

---

## 3. Type-II target

The Type-II target is

```text
-1.
```

We have

```text
C D^(-1) = -1 mod k
```

if and only if

```text
D = -C mod k.
```

Thus

```text
Type II hit
iff
some divisor D of C^2 satisfies
D = -C mod k.
```

---

## 4. Type-I target becomes constant

For an admissible Lane-I state,

```text
4C = p+k,
```

so

```text
p = 4C mod k.
```

The Type-I target is

```text
-p^(-1).
```

The signed box is inversion-symmetric because every exponent interval is symmetric:

```text
x in B_k(C)
iff
x^(-1) in B_k(C).
```

Therefore Type I hits iff the inverse target

```text
-p
```

belongs to the box.

Using the divisor-square representation:

```text
C D^(-1) = -p = -4C mod k.
```

Cancel `C`:

```text
D^(-1) = -4 mod k.
```

Invert:

```text
D = -4^(-1) mod k.
```

Hence the exact Type-I criterion is

```text
Type I hit
iff
some divisor D of C^2 satisfies
D = -4^(-1) mod k.
```

The target residue is **independent of p and C** once the shift `k` is fixed.

---

## 5. Combined Lane-I criterion

Let

```text
D_k(C^2)
=
{ D mod k : D divides C^2 }.
```

Then the complete exact Lane-I construction condition is

```text
delta_k(C)=0
```

if and only if

```text
-C mod k
```

or

```text
-4^(-1) mod k
```

lies in `D_k(C^2)`.

Equivalently:

```text
combined hit
iff
{-C, -4^(-1)} intersects D_k(C^2).
```

This is exactly equivalent to the existing signed-box target pair

```text
{-1,-p^(-1)}.
```

---

## 6. Concrete fixed-shift Type-I divisor targets

Because the Type-I divisor target depends only on `k`, early Lane-I shifts have fixed values:

```text
k=3:   -4^(-1) = 2 mod3
k=7:   -4^(-1) = 5 mod7
k=11:  -4^(-1) = 8 mod11
k=15:  -4^(-1) = 11 mod15
k=19:  -4^(-1) = 14 mod19
k=23:  -4^(-1) = 17 mod23.
```

This supplies a second exact coordinate system for the BREC corridor:

```text
signed-box view:
    hit {-1,-p^(-1)}

divisor-square view:
    divisors of C^2 hit {-C,-4^(-1)}.
```

The two views are mathematically identical.

---

## 7. Exact residue dynamic program

The divisor-square view suggests an evaluator that never walks negative exponents.

Start with the reachable divisor residue set

```text
R = {1}.
```

For each prime power

```text
q^e || C,
```

update by multiplying every current residue by

```text
1,q,q^2,...,q^(2e)
```

modulo `k`, deduplicating residues after each factor.

At every stage the number of distinct residues is at most

```text
k.
```

So the residue-state work is bounded by the modulus rather than by the formal signed-box size

```text
product (2e_i+1).
```

The evaluator may also return immediately once either target residue is reached, because exponent zero for every future prime factor preserves every already-reachable divisor residue.

---

## 8. Why this may outperform recursive signed-box DFS

The existing exact DFS walks formal exponent combinations until it finds a target.

When many exponent combinations collide modulo `k`, the formal box can be much larger than its distinct residue support.

The divisor-residue DP merges those collisions immediately:

```text
formal signed box size      product (2e_i+1)
residue DP state size       <= k.
```

The expected win is therefore largest when:

- `C` has several prime factors or repeated valuations;
- `k` is modest;
- many formal products collapse to the same residue;
- both exact targets are absent or found late by DFS.

For tiny boxes, DFS may still be cheaper. The likely production endpoint is therefore a measured hybrid, not an unconditional replacement.

---

## 9. Interaction with the BREC residue automaton

The signed-box residue automaton and divisor-square DP are two views of the same finite modular object.

The automaton evolves the signed support as factor occurrences are added.

The divisor-square DP evolves the nonnegative divisor support of `C^2`.

The exact target transform

```text
{-1,-p^(-1)}
<->
{-C,-4^(-1)}
```

connects them.

This gives CBX a useful three-level picture:

```text
factorization of C
    -> finite modular support state
        -> exact BREC +/- label.
```

---

## 10. Implementation target

A standalone C prototype should compare:

```text
reference:
    factor C
    delta_zero(...)

prototype:
    factor C
    divisor residues of C^2
    test {-C,-4^(-1)}
```

across every admissible shift in finite exact corpora.

Only after exact equality and benchmark evidence should the DP be considered for promotion into the shared kernel.

The consecutive-cofactor prestrip prototype is complementary:

```text
cofactor block prestrip
    -> cheaper exact factorization
        -> divisor-square residue DP
            -> BREC sign.
```

Together they define a plausible next-generation exact Lane-I evaluator without changing the mathematics.

---

## 11. Claim boundary

The divisor-square duality is an exact algebraic reformulation of the current Lane-I signed-box test.

It does not strengthen the mathematical coverage of Lane I by itself and does not prove Erdős–Straus. Its value is that it exposes a bounded residue-state evaluator and a constant Type-I divisor target that may be easier to optimize and reason about.
