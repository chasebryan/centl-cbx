# D-selector q29 tenth-lift saturation at k951

**Status:** exact conditional progress theorem inside the Route-B D-selector laboratory  
**Date:** 2026-08-16  
**Verifier:** `verify_d_selector_q29_tenth_lift_saturation.py`  
**Depends on:** `PERSISTENT-SOURCE-QADIC-VALUATION-LADDER.md`, `COMPANION-SOURCE-CHARACTER-CONSERVATION.md`, and `JACOBI-SATURATION-CHARACTER-EXTRACTION.md`.  
**Claim boundary:** this is a conditional theorem on the q=29 B-reservoir witness and its tenth-power lift at k951. It does not prove that every D-selector state contains q29, does not establish a universal shift ceiling, and is not an Erdős–Straus proof.

## 1. The source

The B-reservoir witness class requires

```text
(q/23)=+1
(q/17)=-1.
```

The prime

```text
q=29
```

has exactly those characters:

```text
(29/23)=+1
(29/17)=-1.
```

If `29|B`, then because `C23=6B` and `29` is coprime to6,

```text
29 | C23.
```

The companion-source orientation theorem then gives

```text
(29/p)=(29/23)=+1.
```

Thus a materialized q29 B witness is a genuine positive target-prime source.

## 2. Its persistent destination k951

The q29 persistent route from origin23 is

```text
k = 23 + 4*29*n.
```

At

```text
n=8
```

we obtain

```text
k = 951 = 3*317.
```

Character conservation gives

```text
Jacobi(29/951)=+1.
```

The h169 mandatory class seed at k951 is

```text
S0 = gcd(210,(169+951)/4)
   = gcd(210,280)
   = 70.
```

## 3. q-adic lift condition

The valuation theorem says

```text
29^e | C951
iff
951 = -p mod 4*29^e.
```

The constructive branch of this theorem is the tenth lift

```text
29^10 | C951.
```

Equivalently,

```text
p = -951 mod 4*29^10.
```

On this branch the exact mandatory seed includes

```text
S10 = 70*29^10.
```

Because the source route starts at j23 and

```text
951 = 23 + 4*29*8,
```

a tenth lift at k951 actually has source valuation exactly one at the origin:

```text
v29(C23)=1.
```

Indeed, writing `C951=29^10 M`,

```text
C23 = C951 - 8*29
    = 29(29^9 M - 8),
```

and the parenthesis is nonzero modulo29.

So this is a genuine example of a multiplicity-one materialized source climbing to a high q-adic lift later on its persistent ladder.

## 4. Exact saturation threshold

Let

```text
S_e = 70*29^e.
```

The Jacobi-positive kernel modulo951 has exactly

```text
phi(951)/2
= (2*316)/2
= 316
```

units.

The exact divisor-square residue counts are

```text
e=1   77
e=2  127
e=3  159
e=4  189
e=5  217
e=6  243
e=7  269
e=8  286
e=9  302
e=10 316
```

For exponents1 through9, the residue set is a strict subset of the positive kernel.

At exponent10,

```text
{d mod951 : d|S10^2}
=
{u in U(951) : Jacobi(u/951)=+1}.
```

Therefore

```text
70*29^10
```

is Jacobi-saturating modulo951, and exponent10 is the first saturating q29 power on this destination.

## 5. Exact hit-or-extract dichotomy

The Jacobi-saturation theorem now applies.

### If C951 contains a Jacobi-negative prime factor

Then the saturated seed plus that factor fills the negative coset and realizes the exact Type-I target.

So k951 **hits** and produces a valid signed-box decomposition certificate.

### If k951 misses

Then every prime factor of C951 has positive Jacobi character and the saturation theorem forces

```text
Jacobi(951/p)=+1.
```

Since

```text
951=3*317
```

and h169 has

```text
p=169 mod840
=> p=1 mod3,
```

quadratic reciprocity gives

```text
(3/p)=(p/3)=+1.
```

Therefore a saturated miss forces

```text
(317/p)=+1.
```

So the tenth-lift state has an exact constructive dichotomy:

```text
q29 tenth lift at k951
        |
        +-- k951 hit -> decomposition certificate
        |
        `-- k951 miss -> new fixed positive character (317/p)=+1.
```

Either outcome advances exact state.

## 6. Compatibility with realized Route-B D-selector ancestry

The realized Route-B D-selector phase can be written

```text
u = 3631 mod4743,
t = 705 + 1081u,
p = 169 + 840t.
```

Hence

```text
p = 3,297,685,609 mod 4,306,833,720.
```

The tenth-lift condition is

```text
p = -951 mod 4*29^10.
```

These congruences are compatible. Solving them gives the primitive class

```text
p = 1,077,349,876,531,183,834,133,689
    mod
    1,811,916,098,625,212,549,577,720.
```

Equivalently, if

```text
u = 3631 + 4743*s,
```

then the tenth-lift subphase is

```text
s = 250,148,936,915,814
    mod 420,707,233,300,201.
```

The progression is arithmetically compatible with the full Route-B D-selector phase state. This statement is compatibility only; it does not assert that every integer or prime in the progression realizes all remaining survivor support conditions.

## 7. Why the previous barrier remains correct

The multiplicity-one single-source theorem applies to the sector

```text
v29(C_k)=1.
```

This branch instead has

```text
v29(C951)>=10.
```

So there is no contradiction.

The barrier correctly removed futile exponent-one saturation work, while the valuation theorem preserved the high-lift subroute that actually becomes constructive.

This is exactly the machine behavior we wanted from explicit q-adic state.

## 8. Machine consequence

Add a conditional progress rule:

```text
if route == B_D_SELECTOR
and materialized_B_witness == 29
and destination == 951
and v29(C951) >= 10:
    seed = 70*29^10
    JACOBI_SATURATED = true
    outcome = HIT_OR_EXTRACT_317_POSITIVE
```

A miss may promote

```text
317
```

to the positive fixed-character source set for the target prime.

The promotion is proof-bearing only after the tenth-lift condition and saturation theorem are established.

## 9. Bryan Entanglement Cross boundary

This is a particularly clean BEC history:

```text
down (-/+): D-selector state forces a B-reservoir witness obligation
right (+):  q29 materializes and becomes a positive source
up (+/-):   persistent route opens nested q-adic lifts
left/down:  exponents1..9 fail to saturate
right (+):  exponent10 saturates and forces hit-or-extract progress.
```

BEC describes the path. The q-adic congruence, exact residue closure, and Jacobi extraction carry the proof.

## 10. Next target

The new extracted source q317 should be fed into the exact character-routing and promotion graph.

Two questions are now natural:

1. Which admissible destinations route q317 into a companion with a mandatory seed that it saturates or expands?
2. Does the q317 branch create a strictly smaller survivor grammar than the original D-selector state?

That is the first genuinely constructive continuation generated by the renewed-source valuation program.
