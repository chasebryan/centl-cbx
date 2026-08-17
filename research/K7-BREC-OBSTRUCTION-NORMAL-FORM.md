# k=7 BREC obstruction normal form

**Status:** exact elementary lemma  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`

## 1. Statement

Let `p` be a Mordell-hard prime and define

```text
C_7 = (p+7)/4.
```

Then the two Lane-I targets at `k=7` always have the same exact hit/miss status.

Moreover,

```text
sigma_7(p) = -
```

if and only if every prime divisor of `C_7` is a quadratic residue modulo 7:

```text
q mod 7 in {1,2,4}.
```

Equivalently,

```text
sigma_7(p) = +
```

if and only if `C_7` has at least one prime divisor in the quadratic-nonresidue classes

```text
{3,5,6} mod 7.
```

This gives an exact normal form for the second BREC coordinate.

---

## 2. Mordell-hard residue input

The Mordell-hard classes modulo 840 are

```text
1, 121, 169, 289, 361, 529.
```

Reducing modulo 7 gives only

```text
1,2,4,
```

which is exactly the quadratic-residue subgroup

```text
Q_7 = {1,2,4}.
```

Thus every Mordell-hard prime satisfies

```text
(p/7)=+1.
```

The same hard classes are all

```text
1 mod 8.
```

Therefore

```text
p+7 = 0 mod 8,
```

so

```text
2 divides C_7.
```

---

## 3. The forced factor 2 fills the quadratic-residue subgroup

Modulo 7,

```text
2^(-1)=4.
```

Because the exponent of the factor `2` in `C_7` is at least one, its signed local exponent range includes

```text
-1,0,+1.
```

Therefore the signed box already contains

```text
{2^(-1),1,2} = {4,1,2} = Q_7.
```

Any additional quadratic-residue factor keeps the support inside the same subgroup.

Hence, if **all** prime divisors of `C_7` are quadratic residues modulo 7, the complete signed-box support is exactly

```text
R_7(C_7)=Q_7={1,2,4}.
```

---

## 4. One nonresidue fills the other coset

Let `q` be any quadratic-nonresidue prime divisor of `C_7`. Then

```text
q mod 7 in {3,5,6}.
```

Since its valuation is positive, the signed box permits exponent `+1` on `q` while independently ranging over the already-present `Q_7` support from the factor `2`.

Thus the support contains

```text
q Q_7.
```

For every nonresidue `q`,

```text
q Q_7 = {3,5,6},
```

the full nonresidue coset.

Together with the forced quadratic-residue subgroup:

```text
Q_7 union qQ_7 = (Z/7Z)^x.
```

So a single nonresidue prime divisor makes the signed-box support equal the entire unit group modulo 7.

---

## 5. Both targets are nonresidues

The Type-II target is

```text
-1 = 6 mod 7.
```

Since `7 = 3 mod 4`, `-1` is a quadratic nonresidue.

The Type-I target is

```text
-p^(-1).
```

For a Mordell-hard prime, `p` is a quadratic residue modulo 7, so `p^(-1)` is also a quadratic residue. Multiplying by the nonresidue `-1` gives a nonresidue.

Hence both exact targets lie in

```text
{3,5,6}.
```

Therefore:

- if every factor of `C_7` is a quadratic residue, the box is exactly `Q_7` and **both targets miss**;
- if any factor is a nonresidue, the box is the full unit group and **both targets hit**.

This proves the theorem.

---

## 6. Stronger target-coincidence conclusion

Unlike the finite `k=23` target coincidence that was later falsified, the `k=7` coincidence is exact:

```text
-1 in R_7(C_7)
iff
-p^(-1) in R_7(C_7)
```

for every Mordell-hard prime.

The reason is structural and visible in the proof:

```text
forced factor 2
    -> full QR subgroup already present
        -> any NR factor fills the whole NR coset
            -> both NR targets appear together.
```

This is precisely the kind of BREC contraction that can be promoted from finite observation to theorem because its mechanism is exact.

---

## 7. Translation onto the q=23 Type-I rescue branch

The exact q23 companion normal form writes a Type-I-only rescue as

```text
C_23 = 6HD,
p    = 24HD - 23.
```

At `k=7`:

```text
C_7 = (p+7)/4
    = (24HD-16)/4
    = 6HD-4
    = 2(3HD-2).
```

The forced factor `2` is already a quadratic residue modulo 7. Therefore the exact `k=7` obstructive condition becomes:

```text
sigma_7(p) = -
iff
every prime divisor of 3HD-2 is in {1,2,4} mod 7.
```

So a q23 Type-I-only rescue with BREC prefix

```text
--
```

must satisfy the simultaneous exact conditions

```text
p = 24HD - 23 is Mordell-hard prime,
D is a same-class valuation-two 5^2 or 14^2 defect mod 23,
all prime divisors of H are 1 mod 23,
all prime divisors of 6HD-5 are 1 mod 3,
all prime divisors of 3HD-2 are quadratic residues mod 7.
```

The first two BREC obstruction coordinates are therefore now expressed as explicit factor conditions on the same integer parameter `HD`.

---

## 8. Executable verification

The finite residue-group proof obligations are frozen in:

```text
research/verify_k7_brec_obstruction_normal_form.py
```

Run:

```sh
python3 research/verify_k7_brec_obstruction_normal_form.py
```

The verifier checks:

```text
all six Mordell-hard residue classes,
p mod7 in Q_7,
p mod8 = 1,
the forced factor-2 signed support equals Q_7,
all three NR cosets equal {3,5,6},
both exact targets are nonresidues,
and the q23 branch translation C_7=2(3HD-2).
```

---

## 9. Next coordinate

With `k=3` and `k=7` now in exact normal form, the next BREC obstruction coordinate is `k=11`.

The current bridge system for a q23 Type-I-only rescue with prefix `--` is:

```text
C_23 = 6HD,
p    = 24HD - 23,
C_3  = 6HD - 5,
C_7  = 2(3HD - 2),

all prime divisors of C_3 are 1 mod 3,
all prime divisors of C_7 are QR mod 7.
```

The next task is to determine whether `k=11` admits a similarly exact character normal form or requires a richer signed-box state classification.

---

## 10. Claim boundary

This document proves the exact `k=7` characterization for Mordell-hard primes and its algebraic translation onto the q23 rescue branch.

It does not claim that the combined `k=3` and `k=7` conditions eliminate either q23 rescue class. Existing explicit primes already show that deeper ancestry can survive.
