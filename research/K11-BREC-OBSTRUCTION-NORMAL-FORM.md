# k=11 BREC obstruction normal form

**Status:** exact fixed-shift theorem  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`  
**Depends on:** the established exact `q=11` Type-II filter and its Type-I companion  
**Claim boundary:** this classifies the third BREC coordinate; it does not prove Erdős–Straus

## 1. Setup

Let `p` be a Mordell-hard prime and put

```text
C = C_11 = (p+11)/4.
```

Every Mordell-hard residue is `1 mod 24`, so

```text
C = 3 mod 6.
```

Hence `C` is odd and `3|C`.

The two exact Lane-I targets modulo `11` are

```text
Type II : -1 = 10
Type I  : -p^(-1).
```

Write

```text
Q_11 = {1,3,4,5,9}
```

for the quadratic-residue subgroup modulo `11`.

The existing exact Type-II theorem says that a miss can occur only in one of two geometries:

```text
A. pure QR splitting
B. one thin primitive defect packet
```

The second target can now be exhausted exactly inside those two geometries.

---

## 2. Pure-QR branch is automatically a combined miss

Suppose every prime divisor of `C` is a quadratic residue modulo `11`.

Then

```text
C is QR mod 11.
```

But at fixed shift `11`,

```text
p = 4C mod 11.
```

Since `4` is also a quadratic residue,

```text
p is QR mod 11.
```

Therefore `p^(-1)` is QR, while `-1` is a quadratic nonresidue because `11=3 mod4`. Thus

```text
-p^(-1) is NR mod 11.
```

The signed box in the pure-QR Type-II miss branch remains inside the QR subgroup. Consequently neither exact target can occur:

```text
pure QR Type-II miss
    => Type-I miss
    => combined BREC miss.
```

So no additional `p mod11` case split is needed once the fixed relation `p=4C mod11` is used.

---

## 3. Thin primitive Type-II branch

The established thin Type-II branch is:

```text
v_3(C)=1,
every other QR prime divisor is 1 mod 11,
no prime divisor is 7,8,10 mod 11,
all primitive NR prime divisors are 2 or 6 mod 11,
total primitive-NR valuation <= 2.
```

Let

```text
a_2 = total valuation of prime factors 2 mod 11,
a_6 = total valuation of prime factors 6 mod 11.
```

Then

```text
a_2+a_6 <= 2.
```

There are exactly six exponent states:

```text
(0,0)
(1,0)
(0,1)
(2,0)
(1,1)
(0,2).
```

The state `(0,0)` overlaps the thin edge of the pure-QR branch. Keeping it in the local exhaustion is useful because it makes the second-target behavior transparent.

---

## 4. Exact six-state exhaustion

The forced factor `3` contributes signed support

```text
{3^(-1),1,3} = {4,1,3}.
```

For each pair `(a_2,a_6)`, multiply this by the signed exponent intervals contributed by residue classes `2` and `6=2^(-1)`.

The exact result is:

```text
a2  a6   C mod11   p mod11   Type-I target   combined state
-------------------------------------------------------------
0   0       3          1            10          miss
1   0       6          2             5          miss
0   1       7          6             9          miss
2   0       1          4             8          Type-I-only
1   1       3          1            10          miss
0   2       9          3             7          Type-I-only
```

Type II misses in all six states by construction.

Type I rescues **only** the two same-orientation valuation-two packets:

```text
2^2
6^2
```

where the notation refers to residue-class valuation, not necessarily the square of one literal prime.

The mixed valuation-two packet

```text
2*6
```

still misses both targets.

---

## 5. Exact combined k=11 miss theorem

For a Mordell-hard prime `p`, the third BREC coordinate satisfies

```text
sigma_11(p) = -
```

if and only if the established q11 Type-II miss occurs and one of the following holds.

### Branch A: pure QR

Every prime divisor of

```text
C_11=(p+11)/4
```

is in

```text
{1,3,4,5,9} mod 11.
```

This branch always misses both targets.

### Branch B: thin primitive combined miss

All thin Type-II hypotheses hold and the primitive packet is one of

```text
(a2,a6) = (1,0), (0,1), (1,1),
```

with the empty `(0,0)` edge already contained in Branch A.

Equivalently, among genuinely non-QR thin defects:

```text
one valuation in class 2,
one valuation in class 6,
or one of each
```

are the complete combined-miss possibilities.

The only thin Type-II misses that are **not** BREC misses are

```text
(a2,a6) = (2,0) or (0,2),
```

which are exact Type-I-only rescues.

No other q11 Type-II miss geometry exists.

---

## 6. Translation onto the q23 Type-I-only branch

For the q23 rescue normal form, write

```text
C_23 = 6T,
p    = 24T - 23.
```

Then

```text
C_11 = C_23 - 3
     = 6T - 3
     = 3(2T-1).
```

Therefore a q23 Type-I-only rescue with BREC prefix

```text
---
```

must satisfy the exact k3 and k7 obstruction laws already proved, together with one of the following k11 conditions.

### q11 pure-QR predecessor

```text
every prime divisor of 2T-1 is QR mod 11.
```

The leading factor `3` is itself QR, so this is equivalent to pure-QR splitting of `C_11`.

### q11 thin primitive predecessor

```text
v_3(C_11)=1,
all QR prime factors of 2T-1 are 1 mod 11,
all NR prime factors of 2T-1 are 2 or 6 mod 11,
(a2,a6) is (1,0), (0,1), or (1,1).
```

Since

```text
C_11=3(2T-1),
```

`v_3(C_11)=1` is equivalent to

```text
3 does not divide 2T-1.
```

Thus the first three exact BREC obstruction coordinates are now simultaneous factor laws on

```text
6T-5,
3T-2,
2T-1.
```

---

## 7. Explicit ancestry checks

The exact verifier preserves several larger-prime guards.

```text
p = 8,243,281
history through k=19: ---++
```

has a genuine thin-primitive combined miss at `k=11`.

The two known full five-miss q23 Type-I-only witnesses

```text
p = 18,766,609
p = 27,211,969
```

both lie in the pure-QR q11 predecessor branch and therefore survive the exact third-coordinate obstruction.

A known constructive q11 case

```text
p = 5,151,841
history through k=19: -++-+
```

is also checked so that the normal-form verifier guards both sides of the classification.

---

## 8. Executable verifier

Run

```sh
python3 research/verify_k11_brec_obstruction_normal_form.py
```

The verifier independently checks:

```text
Mordell-hard forcing of 3|C_11 and odd C_11,
the pure-QR character implication p=4C mod11,
all six thin primitive signed-box states,
the exact Type-I-only packets 2^2 and 6^2,
the exact combined-miss packet set,
translation C_11=3(2T-1),
and explicit ancestry witnesses against the exact signed-box evaluator.
```

---

## 9. Frontier after k=11

For a q23 Type-I-only target with anchored BREC prefix `---`, the parameter `T` now obeys three exact predecessor restrictions:

```text
k=3:
  every prime divisor of 6T-5 is 1 mod 3

k=7:
  every prime divisor of 3T-2 is QR mod 7

k=11:
  pure QR splitting of 2T-1 mod 11
  OR one of three bounded thin primitive packets
```

The next coordinate is `k=15`, where the modulus is composite and the exact two-target filter has a different subgroup geometry. That is the next point to transport onto the same parameter `T`.

---

## 10. Claim boundary

This theorem classifies the exact combined hit/miss state at fixed `k=11` for Mordell-hard primes and translates its miss geometry onto the q23 rescue parameter.

It does not prove that the first three BREC misses force later construction, does not establish a universal finite Lane-I ceiling, and does not prove Erdős–Straus.
