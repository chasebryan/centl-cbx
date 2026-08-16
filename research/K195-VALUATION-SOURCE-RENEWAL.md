# k195 valuation-driven source renewal

**Status:** exact conditional source-renewal theorem inside the Route-B D-selector laboratory  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_valuation_source_renewal.py`  
**Depends on:** `K195-DOUBLE-SQUARE-PHASE-SELECTOR.md`, the landed k19/k23/k47 support laws, D-selector mixed-character renewal, ten-cofactor odd-support separation, and companion-source character conservation.  
**Claim boundary:** exact character and source consequences conditional on the k195 double-square corridor. This is not a full-ancestry theorem, termination theorem, closed decomposition method, or Erdős–Straus proof.

## 1. Setup

Assume the realized Route-B D-selector state and the k195 double-square gate

```text
q_D = 41 in D,
q_J = 37 in J,
41^2 | C195,
37^2 | C195.
```

Use the companion cofactors

```text
C19 = 1081 R,
C23 = 6 B,
C31 = 10 D,
C47 = 6 J.
```

The landed survivor normal forms give

```text
every prime factor of R is QR mod19,
every prime factor of B is QR mod23,
every prime factor of D is QR mod31,
every prime factor of J is QR mod47.
```

The landed ten-cofactor theorem makes the odd prime supports of R,B,D,J pairwise disjoint.

## 2. The 37-square lift forces a new R-reservoir source

Because

```text
C195 - C19 = (195-19)/4 = 44,
```

we have

```text
C195 = 1081R + 44.
```

Reduce modulo37. Since

```text
1081 = 8 mod37,
44   = 7 mod37,
```

the condition `37^2 | C195`, and hence in particular `37 | C195`, gives

```text
8R + 7 = 0 mod37,
R = 13 mod37.
```

But

```text
(13/37) = -1.
```

Therefore

```text
(R/37) = -1.
```

The integer R is odd, and every prime factor of R is QR mod19. Hence an odd number of prime-factor occurrences of R must be nonresidues modulo37. In particular there exists an odd prime

```text
q_R | R
(q_R/19) = +1
(q_R/37) = -1.
```

Since `q_R|R|C19`, companion-source character conservation converts this immediately to

```text
(q_R/p)=+1.
```

Thus the double-square corridor creates a genuinely new positive target-prime source rooted at origin19.

## 3. The 41-square lift strengthens the B reservoir

Likewise

```text
C195 - C23 = (195-23)/4 = 43,
```

so

```text
C195 = 6B + 43.
```

Modulo41,

```text
6B + 2 = 0,
B = 27 mod41,
```

and

```text
(27/41) = -1.
```

The D-selector state has `tau9=7`, hence `t=1 mod3`, and therefore

```text
B = 8+35t = 1 mod3.
```

So 3 does not divide B. Also

```text
(2/41)=+1.
```

Therefore the negative aggregate character `(B/41)=-1` must be carried by at least one odd prime factor

```text
q_B41 | B
(q_B41/23)=+1
(q_B41/41)=-1.
```

This may or may not be the same rational prime as the previously forced B-reservoir witness with transverse character `-17`; the theorem does not identify them. It does, however, enrich the B proof state with a second exact negative-character obligation.

Because `q_B41|B|C23`, it is also a positive target-prime source after materialization.

## 4. Removing the known 37 source from J forces another source

The relation

```text
C195 = C47 + 37 = 6J + 37
```

combined with `37^2|C195` gives

```text
J = 37 J1,
J1 = 6 mod37.
```

In particular

```text
v37(J)=1.
```

Now use the other square lift, `41^2|C195`. Modulo41,

```text
6J + 37 = 0,
J = 28 mod41.
```

Since `37^(-1)=10 mod41`, dividing out the known factor37 gives

```text
J1 = J/37 = 34 mod41.
```

But

```text
(34/41) = -1.
```

Every prime factor of J1 is QR mod47 because every prime factor of J is QR mod47. Also

```text
(2/41)=+1.
```

Therefore at least one **odd** prime factor of J1 satisfies

```text
q_J41 | J/37
(q_J41/47)=+1
(q_J41/41)=-1.
```

This prime is not37 because it divides `J/37` and `J/37=6 mod37`.

Since `q_J41|J|C47`, companion-source character conservation gives

```text
(q_J41/p)=+1.
```

Thus the valuation corridor creates a second positive source in the J reservoir in addition to the original source37.

## 5. Forced distinctness: at least five positive sources

Before the double-square refinement, the D-selector renewal theorem already guarantees three distinct odd reservoir witnesses:

```text
q_B in B,
41 in D,
37 in J.
```

The present theorem adds

```text
q_R in R,
q_J41 in J/37.
```

Odd-support separation across R,B,D,J implies

```text
q_R != q_B,41,37,q_J41,
q_J41 != q_B,41,
q_B != 41,37.
```

And `q_J41 != 37` by the exact quotient calculation above.

Therefore the k195 double-square corridor forces **at least five distinct odd rational primes** carrying positive target-prime source character:

```text
q_B,
41,
37,
q_R,
q_J41.
```

The extra B obligation `q_B41` may coincide with q_B or may increase the distinct count further; no stronger distinctness claim is made here.

## 6. Recursive machine consequence

The source state is no longer static. Conditional on the double-square gate, exact arithmetic creates new source obligations:

```text
37^2 lift
    -> R has aggregate -37 character
    -> NEW_SOURCE q_R : (+19,-37)

41^2 lift
    -> B has aggregate -41 character
    -> B_SOURCE_OBLIGATION : (+23,-41)

37^2 + 41^2
    -> J=37*J1 with (J1/41)=-1
    -> NEW_SOURCE q_J41 : (+47,-41)
```

This is a genuine recursive source-generation step:

```text
source valuation
    -> affine character transfer
    -> reservoir character debt
    -> new materialized source class
    -> new persistent companion ladder.
```

The new q_R ladder begins at origin19. The q_J41 ladder begins at origin47. Their actual destination moduli remain q-dependent until the source primes are materialized.

## 7. Bryan Entanglement Cross boundary

A natural observational history is

```text
up (+/-):   37 and41 enter quadratic valuation subladders
right (+):  k195 becomes a Jacobi-saturated selector
up (+/-):   square lifts transfer characters into R,B,J/37
right (+):  new positive source classes are forced
```

BEC/BREC remains post-proof scheduling metadata. The affine congruences, Legendre products, support laws, and support separation are the proof.

## 8. Next target

The strongest next target is now **recursive source closure**:

1. materialize the new R-source class `(+19,-37)` and J-source class `(+47,-41)`;
2. classify their first synchronized destinations with the existing 41/37 sources;
3. ask whether the source count or admissible phase volume must strictly increase/decrease under repetition.

A repeatable theorem of that form could become a genuine progress measure for the candidate decomposition framework.
