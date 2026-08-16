# k195 ancestry: exact k15 survivor normal form

**Status:** exact h169 fixed-k15 theorem  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_k15_survivor_normal_form.py`  
**Depends on:** exact Type-I/full-Type-II signed-box semantics.  
**Claim boundary:** exact k15 miss theorem for h169. It is one ancestry layer inside the k195 program, not a universal k195 reachability theorem and not an Erdős–Straus proof.

## 1. Fixed k15 geometry

For h169

```text
p=169+840t
C15=(p+15)/4=46+210t=1 mod15.
```

So every prime factor of C15 is a unit modulo15.

The exact targets are

```text
Type I  = -4^(-1) = 11 mod15
Type II = -C15     = 14 mod15.
```

## 2. Complete exact closure

The complete unit-factor residue closure modulo15 contains 41 states.

At final center1 there are exactly four miss masks:

```text
{1}
{1,4}
{1,2,4,8}
{1,4,7,13}.
```

Define

```text
H_J = {1,2,4,8}
H_3 = {1,4,7,13}.
```

`H_J` is the Jacobi-positive kernel modulo15, while `H_3` is the subgroup of units congruent to1 modulo3.

Their intersection is

```text
H_J intersection H_3 = {1,4}.
```

Both exact targets 11 and14 lie outside both H_J and H_3.

Every one of the four miss masks is contained in at least one of these two subgroups.

## 3. Exact theorem

```text
k15 misses
iff
[
  every prime factor q|C15 lies in H_J
]
OR
[
  every prime factor q|C15 lies in H_3
].
```

Equivalently:

### J15 sector

```text
Jacobi(q/15)=+1
```

for every rational prime q dividing C15.

### ONE3 sector

```text
q=1 mod3
```

for every rational prime q dividing C15.

## 4. Proof of the converse directions

If all prime factors lie in H_J, every divisor of C15^2 lies in the subgroup H_J, which contains neither target. Hence k15 misses.

The same argument holds for H_3.

Conversely, if k15 misses, its exact divisor mask is one of the four masks above. Every prime factor q of C15 is itself a divisor of C15^2, so q modulo15 belongs to the final divisor mask. Since every miss mask is contained in H_J or H_3, all prime factors lie in the corresponding safe subgroup.

Thus the two-sector theorem is iff and range-free.

## 5. Relation to the certified k15 anchor

The landed `s=59176` anchor has

```text
C15 = 2^2 * 97 * 377909467555760167.
```

Modulo15 the nontrivial prime residues include

```text
2 and 7.
```

Residue2 lies in H_J but not H_3; residue7 lies in H_3 but not H_J.

Therefore the factor support is contained in neither safe sector. The exact theorem predicts a hit, matching the explicit Type-I and Type-II divisors already certified.

## 6. Ancestry consequence

A k195 double-square state that survives k15 must now carry one extra finite mode:

```text
k15_mode in {J15, ONE3},
```

with overlap allowed when all factors lie in `{1,4}`.

So the ancestry grammar through k15 is now symbolic:

```text
k3  : ONE_MOD3
k7  : QR7 | THIN_33
k11 : one of 14 exact endpoint states
k15 : J15 | ONE3.
```

The next unresolved layer is k19+, where the Route-B D-selector state begins to interact directly with the later reservoir grammar.

## 7. Bryan Entanglement Cross boundary

This is another `down (-/+)` compression of ancestry state: the k15 signed box reduces arbitrary factorization to two exact support sectors. BEC/BREC may schedule by that distinction but does not create the theorem.
