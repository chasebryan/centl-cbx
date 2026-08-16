# k15-origin q19 square-lift progress gate at k167

**Status:** exact conditional ancestry-progress theorem  
**Date:** 2026-08-16  
**Verifier:** `verify_k15_q19_square_lift_k167.py`  
**Depends on:** `K15-ROUTE-B-SOURCE-RENEWAL.md`, `PERSISTENT-SOURCE-QADIC-VALUATION-LADDER.md`, `JACOBI-SATURATION-CHARACTER-EXTRACTION.md`, and the corrected k195 ancestry phase envelope.  
**Claim boundary:** this theorem is conditional on reaching k167 through earlier ancestry with the stated q19 square-lift phase. It does not prove that every such phase survives to k167, does not prove k195 reachability, and is not an Erdős–Straus proof.

## 1. q19 materializes at k15 exactly on tau19=11

For h169

```text
C15 = 46+210t.
```

Modulo19,

```text
C15 = 8+t.
```

Therefore

```text
19|C15
iff
t=11 mod19.
```

Prime19 belongs to the unique h169 k15 safe kernel:

```text
Jacobi(19/15)=+1.
```

It also carries both Route-B transverse negative characters:

```text
(19/23)=-1
(19/47)=-1.
```

So on `tau19=11`, a k15 miss automatically has a materialized origin15 positive source q19 that can pay both k15 Route-B character debts.

By companion-source orientation,

```text
(19/p)=(19/15)=+1.
```

## 2. k167 is the second persistent q19 destination

The origin15 q19 persistent ladder is

```text
k = 15 + 4*19*n.
```

At

```text
n=2
```

we obtain

```text
k=167.
```

The corresponding companion identity is

```text
C167 = C15 + 38.
```

If `C15=19A`, then

```text
C167 = 19(A+2).
```

Thus the general valuation theorem specializes to

```text
v19(C167)>=2
iff
A=-2 mod19.
```

## 3. Exact square-lift phase

Directly,

```text
C167 = (p+167)/4 = 84+210t.
```

Therefore

```text
19^2 | C167
iff
84+210t = 0 mod361.
```

Since `210^(-1)=153 mod361`, this is

```text
t = 144 mod361.
```

The phase reduces to

```text
t=11 mod19,
```

so every q19 square-lift state at k167 automatically materializes q19 at C15 first.

## 4. Double-square corridor form

On the corrected q41/q37 k195 corridor

```text
t = 7,423,185,617,863
  + 11,799,129,838,887 s.
```

Modulo361,

```text
t = 257 + 297s.
```

Since297 is invertible modulo361,

```text
t=144 mod361
iff
s=312 mod361.
```

So the q19 square lift is one exact sublattice of the k195 double-square corridor.

It is compatible with the current pre55/early phase shell. For example

```text
s=1395 = 312 + 3*361
```

has

```text
tau11=3
tau13=6
tau19=11
tau43=9
```

and all frozen D-selector coordinates remain

```text
tau9=7,tau17=6,tau23=15,tau31=7,tau47=0.
```

This is phase compatibility only, not a full signed-box reachability witness.

## 5. Exact Jacobi saturation at k167

For h169,

```text
C167 = 84+210t,
```

so the mandatory class seed is

```text
S0 = gcd(210,C167)=42.
```

On the square-lift branch the seed contains

```text
S = 42*19^2.
```

Since167 is prime,

```text
|QR167| = 83.
```

The exact divisor-square residue set satisfies

```text
{d mod167 : d|S^2} = QR167.
```

Thus `42*19^2` is QR/Jacobi-saturating modulo167.

The multiplicity-one q19 seed does not have this property; the constructive transition genuinely uses valuation2.

## 6. Hit-or-extract gate

The saturation theorem gives the exact dichotomy.

### If C167 contains a quadratic nonresidue factor modulo167

The saturated seed plus that factor fills the negative coset and the signed box hits, producing a decomposition certificate.

### If k167 misses

Every prime factor of C167 is QR167, and the saturation theorem forces

```text
(167/p)=+1.
```

Prime167 is not in the baseline h169 active source set

```text
{7,11,23,31}.
```

So, unless already learned through some independent branch, the miss side promotes a new positive target-prime character source q167.

The exact progress transition is therefore

```text
s=312 mod361
+ survive to k167
     |
     +-- k167 HIT -> decomposition certificate
     |
     `-- k167 MISS -> (167/p)=+1.
```

## 7. Relation to the landed valuation-two automaton

The landed valuation-two source automaton independently contains the exact transition

```text
19^2 at k167 -> 167.
```

This theorem supplies a new **ancestry origin** for that transition: q19 can be forced already at k15 by the Route-B source-renewal state, and the k195 double-square corridor has an explicit q19-square subphase.

So the bounded character automaton is now connected directly to the k15 ancestry grammar rather than only to the q317 descendant program.

## 8. Machine consequence

Add the conditional proof-state rule

```text
if route == K195_DOUBLE_SQUARE
and s mod361 == 312
and state survives through k15 with q19 materialized
and reaches k167:
    v19(C167) >= 2
    SATURATED_167 = true
    outcome = HIT_OR_PROMOTE_167
```

No pruning permission is granted before reachability is established.

## 9. Bryan Entanglement Cross boundary

A natural annotation is

```text
down (-/+): k15 survival forces q19 on tau19=11
up (+/-):   q19 opens its persistent q-adic ladder
right (+):  the square-lift subphase at k167 saturates
right (+):  outcome is hit or positive q167 promotion.
```

BEC/BREC describes the transition. The companion identity, q-adic phase, and exact residue saturation carry the proof.
