# D-selector mixed-character factor-witness renewal

**Status:** exact Route-B conditional module inside the candidate decomposition framework  
**Date:** 2026-08-16  
**Verifier:** `verify_d_selector_mixed_character_renewal.py`  
**Depends on:** `K27-D-SELECTOR-FACTOR-GRAMMAR.md`, k23 QR-support, `K31-SURVIVOR-NORMAL-FORM.md`, `ROUTE-B-K47-SURVIVOR-NORMAL-FORM.md`, and the ten-cofactor odd-support separation theorem.  
**Claim boundary:** exact necessary mixed-character **factor-witness** consequences conditional on the realized Route-B D-selector state surviving the named shifts. These witnesses are not, by themselves, legacy character-routing sources of the form `(q/p)=+1`. This is not an existence theorem for the overall state, a termination theorem, a closed decomposition method, or an Erdős–Straus proof.

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

Write

```text
C23 = 6B
C27 = 7E
C31 = 10D
C35 = 3F
C47 = 6J.
```

Then

```text
7E  - 6B  = 1
10D - 7E  = 1
3F  - 10D = 1
J = B + 1.
```

## 2. Factor 17 transfers exact neighbor characters

Because `17|E`, modulo17:

```text
B = 14
D = 12
F = 12
J = 15.
```

Hence

```text
(B/17) = -1
(D/17) = -1
(F/17) = -1
(J/17) = +1.
```

Also `(2/17)=+1`, so a 2-adic factor cannot account for a negative aggregate character at17.

### B reservoir

The k23 survivor theorem says every rational prime factor of B is a nonzero quadratic residue modulo23, while `(B/17)=-1`.

Therefore

```text
sum_{q|B, (q/17)=-1} v_q(B) = 1 mod2,
```

and at least one **odd factor witness** `q_B|B` satisfies

```text
(q_B/23)=+1
(q_B/17)=-1.
```

### D reservoir

The k31 survivor theorem says every rational prime factor of D is a nonzero quadratic residue modulo31, while `(D/17)=-1`.

Therefore

```text
sum_{q|D, (q/17)=-1} v_q(D) = 1 mod2,
```

and at least one odd factor witness `q_D|D` satisfies

```text
(q_D/31)=+1
(q_D/17)=-1.
```

## 3. Factor 31 forces a third witness in J

Because `31|E`, modulo31:

```text
B = 5
D = 28
F = 11
J = 6.
```

Thus

```text
(B/31) = +1
(D/31) = +1
(F/31) = -1
(J/31) = -1.
```

Route-B k47 survival says every rational prime factor of J is a nonzero quadratic residue modulo47. Since `(J/31)=-1`,

```text
sum_{q|J, (q/31)=-1} v_q(J) = 1 mod2.
```

Also `(2/31)=+1`. The D-selector phase has `tau9=7`, hence `t=1 mod3` and `3 does not divide J`.

Therefore at least one odd factor witness `q_J|J` satisfies

```text
(q_J/47)=+1
(q_J/31)=-1.
```

## 4. The three witnesses are distinct

The ten-cofactor theorem makes the odd parts of

```text
R,B,E,D,F,G,H,J,K,L
```

pairwise coprime.

The witnesses `q_B`, `q_D`, `q_J` are odd, so

```text
q_B != q_D
q_B != q_J
q_D != q_J,
```

and none divides E.

Thus the D-selector state forces at least **three distinct fresh odd factor witnesses** in three separate reservoirs.

## 5. F is the sharp control

F has negative aggregate character at both fixed moduli:

```text
(F/17)=-1
(F/31)=-1.
```

But `tau9=7` gives `v3(F)=1`, and

```text
(3/17)=-1
(3/31)=-1.
```

Therefore the compulsory factor3 accounts for both negative signs:

```text
(F/3 / 17)=+1
(F/3 / 31)=+1.
```

So this theorem does **not** force a fourth fresh negative-character witness from F. If the k35 state is S7, the landed valuation theorem identifies the same rational prime3 as the distinguished S7 factor and gives 1-mod7 support for `F/3`.

## 6. Critical orientation boundary

These factor-witness characters are **not the same object** as the legacy character-routing sources.

The old routing graph uses fixed prime moduli q with a proved character relative to the Erdős–Straus target prime p, for example

```text
(q/p)=+1.
```

The present theorem gives variable reservoir factors with characters relative to small fixed moduli, for example

```text
(q_B/23)=+1
(q_B/17)=-1.
```

No direct promotion

```text
factor witness -> legacy routing source
```

is permitted.

A separate exact reciprocity/identity theorem would be required to convert one orientation into the other. Until such a theorem exists, the machine must store these as **reservoir witness obligations**, not `ACTIVE_SOURCES` entries.

This distinction is proof-critical.

## 7. Machine consequence

The reduced proof state may carry

```text
WIT_B17_23:
    exists q_B | B with (q_B/23)=+1 and (q_B/17)=-1

WIT_D17_31:
    exists q_D | D with (q_D/31)=+1 and (q_D/17)=-1

WIT_J31_47:
    exists q_J | J with (q_J/47)=+1 and (q_J/31)=-1

DISTINCT:
    q_B, q_D, q_J pairwise distinct and absent from E.
```

These obligations strengthen support renewal, but they grant **no character-routing edge by themselves**.

## 8. Bryan Entanglement Cross boundary

Directionally this can still be annotated as excavation resolving into richer structure:

1. D-selector rigidity fixes factors17 and31 in E;
2. affine transfer forces negative aggregate characters in B,D,J;
3. positive own-support laws force distinct mixed-character factor witnesses.

The BEC/BREC history is observational/scheduling metadata only. The affine congruences, Legendre products, support theorems, and odd-support separation carry the proof.

## 9. Next target

The correct next theorem is **orientation conversion**, not immediate routing:

> Determine whether the Route-B D-selector equations plus the fact that `q_B|C23`, `q_D|C31`, or `q_J|C47` can convert any witness character `(q/m)` into a useful character involving the target prime p, or else prove that no such direct conversion exists inside the local companion ladder.

Only after that conversion is proved may these witnesses enter the legacy character-routing graph.
