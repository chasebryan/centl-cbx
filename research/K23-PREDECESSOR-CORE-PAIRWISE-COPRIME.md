# k=23 predecessor core is pairwise coprime

**Status:** elementary exact theorem  
**Date:** 2026-08-17  
**Scope:** q23 Type-I-only predecessor parameterization  
**Claim boundary:** structural theorem only; it does not make the corridor impossible

## 1. Reduced predecessor core

On the q23 Type-I-only parameterization

```text
T=(p+23)/24,
```

the five predecessor integers are

```text
C3  = 6T-5,
C7  = 2(3T-2),
C11 = 3(2T-1),
C15 = 2(3T-1),
C19 = 6T-1.
```

Remove the fixed factors `2,3,2` already built into the exact k7, k11, and k15 normal forms. Define

```text
A = 6T-5,
B = 3T-2,
C = 2T-1,
D = 3T-1,
E = 6T-1.
```

Then:

```text
A,B,C,D,E are pairwise coprime for every integer T.
```

This is stronger than an empirical observation and requires no primality assumption on `p`.

---

## 2. Ten exact cancellations

Every pair admits a tiny linear combination in which `T` cancels:

```text
A - 2B = -1
A - 3C = -2
A - 2D = -3
A - E  = -4

2B - 3C = -1
B - D    = -1
2B - E   = -3

3C - 2D = -1
3C - E  = -2

2D - E = -1.
```

Any common divisor of a pair must divide the corresponding constant.

The `±1` rows finish immediately.

For the `±2` and `±4` rows, the involved forms are among

```text
A,C,E,
```

all of which are odd, so no factor `2` survives.

For

```text
A - 2D = -3,
```

we have

```text
A = 6T-5 = 1 mod 3,
```

so `3` cannot divide `A`.

For

```text
2B - E = -3,
```

we have

```text
B = 3T-2 = 1 mod 3,
```

so again `3` cannot be common.

Therefore every pair has gcd one.

---

## 3. Consequence for the BREC corridor

The five exact predecessor obstruction grammars now live on **disjoint prime supports**:

```text
6T-5     k3 semigroup condition
3T-2     k7 QR condition
2T-1     k11 QR/thin condition
3T-1     k15 subgroup condition
6T-1     k19 cyclic-state condition.
```

No prime can occur in two of these reduced forms.

This closes one natural but unproductive line of attack: a contradiction cannot come from arguing that one shared prime factor is forced to satisfy incompatible local residue requirements at two predecessor coordinates. There is no shared prime factor to exploit.

The coupling must instead come from the **additive relations between the forms**, from global residue classes of `T`, from character reciprocity, or from the q23 factor grammar on `T` itself.

---

## 4. The right cross-coordinate object

Pairwise coprimality makes the corridor look less like overlapping factor sets and more like a short admissible tuple of neighboring linear forms:

```text
6T-5,
3T-2,
2T-1,
3T-1,
6T-1.
```

Each coordinate carries its own multiplicative restriction, but the coordinates are locked together additively by one `T`.

This suggests the next proof language should resemble a **character vector of an affine tuple**:

```text
T
 -> local factor semigroup at 6T-5
 -> local QR semigroup at 3T-2
 -> local q11 branch at 2T-1
 -> local H15 semigroup at 3T-1
 -> local cyclic state at 6T-1
 -> q23 rescue factor state at T.
```

Any universal obstruction must couple these separate prime supports through the common affine parameter.

---

## 5. Relation to the two known full survivors

Pairwise coprimality is fully compatible with the verified `-----+` primes

```text
18,766,609
27,211,969.
```

The theorem therefore does not reduce the full corridor to the empty set. It describes why the five local constraints can coexist without direct factor collision.

This is useful negative structure: it tells us which kind of contradiction **cannot** finish the branch.

---

## 6. Executable proof object

Run

```sh
python3 research/verify_k23_predecessor_pairwise_coprime.py
```

The verifier records the ten symbolic cancellation identities, checks the parity/mod-3 exclusions, and regression-tests the formulas and gcds through `T=20,000`.

The symbolic cancellation argument is the proof. The finite sweep is only a guard against transcription mistakes.

---

## 7. Claim boundary

This theorem proves pairwise coprimality of the five reduced predecessor forms.

It does not prove their individual obstruction conditions are independent, does not show their simultaneous satisfaction has positive or zero density, does not create a finite Lane-I ceiling, and does not prove Erdős–Straus.
