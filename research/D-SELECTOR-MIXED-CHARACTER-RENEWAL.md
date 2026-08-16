# D-selector mixed-character source renewal

**Status:** exact Route-B conditional module inside the candidate decomposition framework  
**Date:** 2026-08-16  
**Verifier:** `verify_d_selector_mixed_character_renewal.py`  
**Depends on:** `K27-D-SELECTOR-FACTOR-GRAMMAR.md`, k23 QR-support, `K31-SURVIVOR-NORMAL-FORM.md`, `ROUTE-B-K47-SURVIVOR-NORMAL-FORM.md`, and the ten-cofactor odd-support separation theorem.  
**Claim boundary:** exact necessary character-source consequences conditional on the realized Route-B D-selector state surviving the named shifts. It is not an existence theorem for that state, a termination theorem, a closed decomposition method, or an Erdős–Straus proof.

## 1. Starting state

Use the realized Route-B D-selector state

```text
k19 = FULL_QR
tau17 = 6
tau31 = 7
k27 = D
k31 = FULL_QR
tau9 = 7
```

with exact k27 cofactor grammar

```text
E = 17 * 31 * r * A,
```

where

```text
r is prime, r = 2 mod27, v_r(E)=1,
every prime factor of A is 1 mod27,
v17(E)=v31(E)=1.
```

For h169 write the companion cofactors

```text
C23 = 6B
C27 = 7E
C31 = 10D
C35 = 3F
C47 = 6J.
```

The consecutive companion identities are

```text
7E  - 6B  = 1
10D - 7E  = 1
3F  - 10D = 1
J = B + 1.
```

The goal is to collide the rigid E factors with the already-proved support laws on B, D, F, and J.

## 2. The factor 17 transfers exact neighbor characters

Because `17|E`, reduce the affine chain modulo17:

```text
B = -6^(-1) = 14 mod17
D =  10^(-1) = 12 mod17
F =  2*3^(-1) = 12 mod17
J = B+1       = 15 mod17.
```

Their quadratic characters are

```text
(14/17) = -1
(12/17) = -1
(12/17) = -1
(15/17) = +1.
```

Also

`(2/17)=+1`.

Therefore a negative aggregate character of B or D modulo17 cannot be supplied by a 2-adic factor.

### B reservoir

The k23 survivor theorem says every rational prime factor of B is a nonzero quadratic residue modulo23.

But

`(B/17)=-1`.

Hence the prime-factor occurrence parity satisfies

```text
sum_{q|B, (q/17)=-1} v_q(B) = 1 mod2.
```

So at least one **odd** rational prime `q_B|B` obeys

```text
(q_B/23)=+1
(q_B/17)=-1.
```

This is a forced mixed-character source class.

### D reservoir

The k31 miss theorem says every rational prime factor of D is a nonzero quadratic residue modulo31.

But

`(D/17)=-1`.

Thus

```text
sum_{q|D, (q/17)=-1} v_q(D) = 1 mod2,
```

and at least one odd prime `q_D|D` obeys

```text
(q_D/31)=+1
(q_D/17)=-1.
```

This is a second forced mixed-character source class.

## 3. The factor 31 forces a third source in J

Because `31|E`, reduce the affine chain modulo31:

```text
B = -6^(-1) = 5  mod31
D =  10^(-1) = 28 mod31
F =  2*3^(-1) = 11 mod31
J = B+1       = 6  mod31.
```

The relevant characters are

```text
(B/31) = +1
(D/31) = +1
(F/31) = -1
(J/31) = -1.
```

On realized Route B, a k47 miss has the exact support law

```text
every rational prime factor of J is QR mod47.
```

Since `(J/31)=-1`,

```text
sum_{q|J, (q/31)=-1} v_q(J) = 1 mod2.
```

Moreover `(2/31)=+1`, so a 2-adic factor cannot carry the negative character. The D-selector phase has `tau9=7`, hence `t=1 mod3` and `3 does not divide J`, so the witness is not the mandatory small prime3 either.

Therefore at least one odd prime `q_J|J` obeys

```text
(q_J/47)=+1
(q_J/31)=-1.
```

This is the third forced mixed-character source class.

## 4. The three source primes are distinct

The ten-cofactor support-separation theorem proves that the **odd parts** of

```text
R,B,E,D,F,G,H,J,K,L
```

are pairwise coprime.

The witnesses `q_B`, `q_D`, and `q_J` are all odd. Therefore

```text
q_B != q_D
q_B != q_J
q_D != q_J.
```

None can divide E either.

So the D-selector state does not merely require one awkward prime. It forces at least **three distinct fresh odd prime sources** in three independent reservoirs.

## 5. F is the sharp control

F also has negative aggregate character at both fixed moduli:

```text
(F/17)=-1
(F/31)=-1.
```

But `tau9=7` gives

```text
v3(F)=1.
```

And rational prime3 itself satisfies

```text
(3/17)=-1
(3/31)=-1.
```

Therefore the compulsory factor3 accounts for both negative signs:

```text
(F/3 / 17)=+1
(F/3 / 31)=+1.
```

So the present theorem **does not** manufacture a fourth fresh negative-character source from F. This is the exact control showing that the B/D/J conclusions are not a generic artifact of every neighboring reservoir.

If the k35 state is S7, the landed valuation theorem further says the same rational prime3 is the distinguished S7 factor and every prime factor of `F/3` is `1 mod7`. That is compatible with the character transfer above.

## 6. Machine consequence

The reduced proof state can now carry three existential source obligations:

```text
SRC_B17_23:
    exists q_B | B with (+23,-17)

SRC_D17_31:
    exists q_D | D with (+31,-17)

SRC_J31_47:
    exists q_J | J with (+47,-31)

DISTINCT:
    q_B, q_D, q_J pairwise distinct and absent from E.
```

These are theorem-bearing obligations. A routing or character-graph engine may consume them without first fully factoring every reservoir, provided it preserves their existential and distinctness semantics.

This is a form of **support renewal** stronger than pairwise coprimality alone: the state is forced to renew specific character types as it crosses the companion ladder.

## 7. Bryan Entanglement Cross boundary

Directionally, this is a natural `down (-/+) -> right (+)` history:

1. the D-selector excavates the state into a rigid E factor grammar;
2. the fixed E factors impose negative characters on neighboring reservoirs;
3. the positive-support survivor laws resolve those negatives into fresh mixed-character sources.

That history is scheduling/interpretation metadata only. The affine congruences, Legendre characters, support theorems, and odd-support separation are the proof-bearing objects.

## 8. Next target

Feed the three new source classes into the existing character-routing graph and ask which downstream companions they can enter by exact divisibility/congruence rules.

The most valuable next theorem is a **source-to-destination closure** showing that at least one of the three forced source classes necessarily activates a signed-box hit or a strictly smaller survivor grammar. That would turn character renewal into a genuine progress transition rather than only a richer state description.
