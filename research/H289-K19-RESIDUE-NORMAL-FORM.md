# h289 k=19 residue normal form

**Status:** exact fixed-shift residue/valuation theorem  
**Date:** 2026-08-17  
**Hard class:** `p = 289 mod840`  
**Depends on:** the h289 order-three quotient theorem

## 1. From nine abstract quotient states to a concrete factor grammar

Hard class289 forces

```text
7 | C19=(p+19)/4.
```

The quotient theorem shows that the exact Type-II-miss state factors through

```text
Z/18Z / <6> ~= Z/6Z.
```

That finite statement can be unfolded into a concrete classification of the prime-factor residue classes of `C19`.

The result closely resembles the thin-defect normal forms already found at q11 and q23.

---

## 2. Six quotient residue classes modulo19

Use primitive root `2` modulo19 and reduce the discrete-log exponent modulo6.

The unit residues split as

```text
quotient class 0 : {1,7,11}
quotient class 1 : {2,3,14}
quotient class 2 : {4,6,9}
quotient class 3 : {8,12,18}
quotient class 4 : {5,16,17}
quotient class 5 : {10,13,15}.
```

Quadratic residues are the even quotient classes:

```text
QR19 = classes 0,2,4.
```

Quadratic nonresidues are the odd classes:

```text
NR19 = classes 1,3,5.
```

Define

```text
K      = {1,7,11}
P_plus = {2,3,14}
P_minus= {10,13,15}.
```

The direct class3 residues are

```text
D = {8,12,18}.
```

The QR residues outside K are

```text
Q_out = {4,5,6,9,16,17}.
```

---

## 3. Why class3 is impossible in a Type-II miss

The forced factor7 already supplies quotient support

```text
{0}.
```

A factor in quotient class3 contributes

```text
{0,+3,-3}={0,3}.
```

But quotient exponent `3` is exactly the Type-II target `-1`.

Therefore any prime divisor of `C19` in

```text
{8,12,18} mod19
```

forces Type-II construction immediately.

So no Type-II-miss h289 state can contain a factor from D.

---

## 4. Why QR support outside K cannot coexist with an NR factor

The forced K reservoir occupies quotient class0.

Any QR factor outside K lies in quotient class2 or4. Its signed support adds

```text
{0,+2,-2}={0,2,4},
```

which is the complete even subgroup of `Z/6Z`.

Now add any allowed NR factor from class1 or5. Multiplying the even subgroup by one odd coset fills the entire quotient group:

```text
{0,2,4} + {0,+1,-1} = Z/6Z.
```

In particular the Type-II target3 appears.

Therefore:

```text
Type-II miss + at least one NR factor
=> every QR prime factor lies in K={1,7,11} mod19.
```

Conversely, if all prime factors are QR, the state is always a combined miss because both Lane-I targets are NR.

This gives the first branch of the normal form.

---

## 5. Pure-QR branch

### Branch A

```text
every prime divisor of C19 is QR mod19.
```

Then

```text
C19 is QR,
p=4C19 is QR,
-1 and -p^(-1) are NR,
```

so both exact targets miss.

Thus every pure-QR h289 k19 state is a combined miss.

No further multiplicity restriction is needed in this branch.

---

## 6. Thin-NR branch

Assume at least one NR factor occurs while Type II still misses.

The preceding arguments force:

```text
all QR factors lie in K={1,7,11},
all NR factors lie in P_plus or P_minus,
no factor lies in {8,12,18}.
```

Let

```text
alpha = total prime-factor valuation in P_plus={2,3,14},
beta  = total prime-factor valuation in P_minus={10,13,15}.
```

Every P_plus or P_minus occurrence may be signed to contribute `+1` in the quotient: use `+a` for class1 and `-a` for class5.

Therefore any three such occurrences can be signed to sum to

```text
1+1+1=3 mod6,
```

which hits Type II.

Hence a Type-II miss requires

```text
alpha+beta <= 2.
```

Conversely, with only one or two such occurrences, quotient support never reaches3.

So the complete non-QR Type-II-miss geometry is exactly

```text
QR support only in K,
NR support only in P_plus/P_minus,
alpha+beta<=2.
```

---

## 7. Exact Type-I companion packets

Inside the thin-NR branch, quotient product exponent and support are determined by `(alpha,beta)`:

```text
cbar = alpha-beta mod6.
```

The Type-I target is

```text
1-cbar mod6.
```

The five nonempty packets are:

```text
alpha beta   cbar   support             result
----------------------------------------------------------
1     0       1     {0,1,5}             Type-I-only
0     1       5     {0,1,5}             combined miss
2     0       2     {0,1,2,4,5}         Type-I-only
1     1       0     {0,1,2,4,5}         Type-I-only
0     2       4     {0,1,2,4,5}         combined miss.
```

Thus the exact thin companion classification is

```text
Type-I-only:
    (alpha,beta) in {(1,0),(2,0),(1,1)}

combined miss:
    (alpha,beta) in {(0,1),(0,2)}.
```

The empty packet `(0,0)` is already part of the pure-QR branch.

This orientation asymmetry is real. P_plus and P_minus are inverse quotient directions, but the moving Type-I target depends on the product exponent, so the two orientations are not interchangeable.

---

## 8. Complete theorem

For a Mordell-hard prime

```text
p=289 mod840,
```

k19 Type II misses if and only if one of the following holds.

### A. Pure QR

```text
every prime divisor of C19 is QR mod19.
```

This is always a combined miss.

### B. Thin NR

```text
all QR prime divisors lie in {1,7,11} mod19,
all NR prime divisors lie in {2,3,14,10,13,15} mod19,
alpha+beta<=2,
```

where alpha counts total valuations in `{2,3,14}` and beta counts total valuations in `{10,13,15}`.

Inside Branch B:

```text
(alpha,beta)=(1,0),(2,0),(1,1)
    -> Type-I-only

(alpha,beta)=(0,1),(0,2)
    -> combined miss.
```

There are no other h289 k19 Type-II-miss geometries.

---

## 9. Regression witnesses

The verifier preserves representative exact primes.

### Thin Type-I-only

```text
p=1,129
C19=287=7*41
41=3 mod19 in P_plus
(alpha,beta)=(1,0)
=> Type-I-only.
```

### Thin combined miss

```text
p=10,369
C19=2,597=7^2*53
53=15 mod19 in P_minus
(alpha,beta)=(0,1)
=> combined miss.
```

### Pure QR combined miss

```text
p=8,689
C19=2,177=7*311
311=7 mod19 in K
=> pure QR combined miss.
```

### Outside the Type-II-miss normal form

```text
p=22,129
C19=5,537=7^2*113
113=18 mod19 in direct quotient class3
=> Type-II construction.
```

These are regression guards only. The theorem follows from the exact quotient geometry.

---

## 10. Why this is stronger than the nine-state table

The quotient theorem says the target-relevant abstract universe contains only nine Type-II-miss states.

This theorem explains **which integer factorizations can inhabit them**.

Instead of carrying an opaque state key, a proof search may use the human-readable grammar

```text
PURE_QR
or
THIN_NR(alpha,beta)
```

with only five nonempty thin packets.

This is directly comparable to the q11 and q23 defect grammars and is more suitable for cross-coordinate coupling with the factor restrictions on

```text
6T-5,
3T-2,
2T-1,
3T-1,
6T.
```

---

## 11. Executable verifier

Run

```sh
python3 research/verify_h289_k19_residue_normal_form.py
```

It checks:

```text
the six residue classes in the Z/6 quotient,
the QR/NR partition,
direct class3 Type-II forcing,
QR-outside-K plus NR saturation,
the alpha+beta<=2 necessity,
all six thin packets including the empty overlap,
the exact Type-I-only packet set,
and exact prime regressions.
```

---

## 12. Claim boundary

This is a complete exact fixed-shift normal form for h289 at k19.

It does not assert that every thin packet is realized after the earlier anchored BREC misses, does not prove that the q23 Type-I-only branch reaches or avoids h289 infinitely often, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
