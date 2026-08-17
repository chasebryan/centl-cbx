# BREC Lane-I affine cofactor recurrence

**Status:** exact structural identity  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`

## 1. The hidden recurrence

For a fixed Mordell-hard prime `p`, write the admissible Lane-I shift sequence as

```text
k_j = 4j + 3,
```

and define

```text
C_j = (p+k_j)/4.
```

Then

```text
C_j = (p+3)/4 + j.
```

Therefore the Lane-I cofactor does not jump around as BREC advances. It moves through consecutive integers:

```text
C_(j+1) = C_j + 1.
```

At the same time,

```text
k_(j+1) = k_j + 4.
```

The quantity

```text
4C_j - k_j
```

is invariant:

```text
4C_j - k_j = p.
```

Thus the exact Lane-I search axis is the affine lattice orbit

```text
(C,k) -> (C+1,k+4)
```

on the invariant line

```text
4C-k=p.
```

This is the arithmetic backbone beneath the BREC sign history.

---

## 2. BREC interpretation

The BREC word for `p` can now be written as a labeling of that affine orbit.

At state

```text
X_j = (p,k_j,C_j),
```

define

```text
sigma_j = +
```

when the exact signed box of `C_j` modulo `k_j` hits at least one target in

```text
{-1,-p^(-1)},
```

and

```text
sigma_j = -
```

when it misses both.

The recursive search state therefore has two layers:

```text
geometric recurrence:
    (C,k) -> (C+1,k+4)

exact state label:
    sigma(C,k,p) in {+,-}
```

BREC preserves the complete sequence of those labels.

This makes the recursive interpretation more precise than treating the signs as free-floating directions. The directions are attached to a deterministic arithmetic orbit.

---

## 3. Exact first-six corridor

The first six Lane-I coordinates are

```text
k = 3, 7, 11, 15, 19, 23.
```

Their cofactors are exactly

```text
C_3,
C_3+1,
C_3+2,
C_3+3,
C_3+4,
C_3+5.
```

So the anchored BREC prefix through `k=23` is a six-label X-ray over six consecutive integers, while the signed-box modulus changes by four at each step.

This is a useful distinction:

```text
cofactor axis:  consecutive integers
modulus axis:   arithmetic progression 3 mod 4
prime invariant: 4C-k=p
```

---

## 4. q=23 Type-I rescue corridor

On the exact q23 Type-I-only rescue normal form,

```text
C_23 = 6M,
M = HD,
p = 24M - 23.
```

The entire first-six BREC cofactor corridor becomes

```text
k=3:   C_3  = 6M - 5
k=7:   C_7  = 6M - 4
k=11:  C_11 = 6M - 3
k=15:  C_15 = 6M - 2
k=19:  C_19 = 6M - 1
k=23:  C_23 = 6M.
```

So the q23 rescue problem is literally a signed-box grammar on the consecutive block

```text
6M-5,
6M-4,
6M-3,
6M-2,
6M-1,
6M.
```

The forced small factors are immediately visible:

```text
6M-5 = 1 mod 6
6M-4 = 2(3M-2)
6M-3 = 3(2M-1)
6M-2 = 2(3M-1)
6M-1 = 5 mod 6
6M   = 6M.
```

That six-integer block is the exact arithmetic object behind an anchored history such as

```text
-----+
```

on the q23 rescue branch.

---

## 5. First four obstruction normal forms on the same parameter

The exact BREC normal forms already derived become conditions on successive members of this one block.

### k=3

```text
C_3 = 6M-5
```

misses iff every prime divisor is

```text
1 mod 3.
```

### k=7

```text
C_7 = 2(3M-2)
```

misses iff every prime divisor of `3M-2` is a quadratic residue modulo 7.

### k=11

```text
C_11 = 3(2M-1)
```

misses iff it lies in the exact QR/thin k11 normal form.

### k=15

```text
C_15 = 2(3M-1)
```

misses iff every prime divisor of `3M-1` lies in

```text
{1,2,4,8} mod 15.
```

The q23 target itself is

```text
C_23 = 6M,
```

with Type-I-only rescue restricted to the exact `5^2` or `14^2` q23 defect branch.

The only early coordinate in this six-block not yet reduced to a new BREC normal form is `k=19`, where

```text
C_19=6M-1.
```

---

## 6. Factor-dependency consequence

For two Lane-I coordinates `i` and `j`,

```text
C_j-C_i = j-i.
```

Therefore

```text
gcd(C_i,C_j) divides |j-i|.
```

Large prime factors cannot persist arbitrarily between nearby BREC coordinates. Any shared factor between two cofactor states must divide their small index separation.

For adjacent states specifically,

```text
gcd(C_j,C_(j+1)) = 1.
```

So direct factor inheritance between consecutive BREC coordinates is impossible.

The dependencies observed by CBX must therefore arise through residue, character, valuation, or affine compatibility constraints rather than through literal persistence of the same nontrivial factor from one adjacent cofactor to the next.

This sharpens the interpretation of recursive entanglement in the ES application.

---

## 7. Kernel optimization consequence

The current exact engine may compute each

```text
C=(p+k)/4
```

independently inside the shift loop.

The recurrence permits the exact equivalent walk

```text
C = (p+3)/4
k = 3

repeat:
    evaluate(C,k)
    C = C+1
    k = k+4
```

with no repeated division by four.

More importantly, a block of consecutive cofactors can be small-prime stripped by a segmented wheel:

```text
C_0, C_0+1, ..., C_0+n
```

For each small prime `q`, compute the first divisible offset once, then visit offsets separated by `q`.

This replaces repeated small-prime divisibility probes at every shift with one residue calculation per small prime per cofactor block.

That optimization is exact and naturally aligned with BREC's recursive state order.

---

## 8. New implementation target

The next kernel optimization should therefore be a **cofactor-block prestripper** for `cbx-brec-i`:

```text
input:
    p, K

construct:
    C_0=(p+3)/4
    N=(K-3)/4+1
    consecutive block C_0 ... C_0+N-1

for each small prime q <= strip bound:
    locate first block offset divisible by q
    strip q-adic valuation from only those offsets

send residuals to deterministic MR / Pollard-rho
```

The existing exact factorization path remains the reference oracle until full finite equivalence is established.

---

## 9. Mathematical next step

The affine recurrence also changes the theorem-hunting question.

Instead of treating the early shifts as unrelated moduli, the q23 rescue frontier can be posed as:

> classify the factor/character grammar of the consecutive six-block `6M-5,...,6M` under the exact q23 condition on `6M`.

The first four members already have exact obstruction normal forms. The next unresolved member is

```text
6M-1
```

at `k=19`.

That is the correct next local target.

---

## 10. Claim boundary

The affine recurrence and gcd consequences are exact identities.

They do not by themselves prove any finite Lane-I ceiling or the Erdős–Straus conjecture. Their significance is structural: BREC is now attached to an explicit arithmetic orbit, and both the next proof search and the next kernel optimization can exploit that orbit without changing exact semantics.
