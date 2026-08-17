# h169 k11 phase-2 -> k19 mode and valuation collapse

**Status:** exact cross-coordinate theorem composition  
**Date:** 2026-08-17  
**Scope:** realized h169 Route-A / Route-B simultaneous-survivor laboratory  
**Verifier:** `verify_h169_k11_phase2_k19_collapse.py`

## 1. The phase

Write

```text
p = 169 + 840t
T = (p+23)/24 = 8 + 35t.
```

The landed h169 k11 theorem says a combined miss is pure quadratic-residue support modulo11. Therefore

```text
k11 miss
->
t mod11 in {0,2,3,4,8}.
```

Select the exact child

```text
t = 8 mod11.
```

Then

```text
T = 8 + 35t = 2 mod11.
```

At k19,

```text
C19 = 6T-1,
```

so

```text
T=2 mod11
->
11 | C19.
```

This phase was already known to preload the order-three q19 seed supplied by residue11. The new point is what that literal factor does to the **realized h169 survivor mode**.

---

## 2. The realized pair routes force factor11 into R

The two realized h169 q23/k19 pair routes have

```text
Route A:
C19 = 391 R = 17*23*R

Route B:
C19 = 1081 R = 23*47*R.
```

Neither fixed route seed contains 11:

```text
gcd(391,11)=1
gcd(1081,11)=1.
```

Therefore on the selected k11 phase,

```text
11 | C19
and
C19 = S*R
with gcd(S,11)=1
```

imply

```text
11 | R.
```

So the earlier k11 phase injects a literal prime directly into the residual k19 support reservoir.

---

## 3. BARE cannot carry it

The landed realized k19 normal form has two survivor modes:

```text
BARE
FULL_QR.
```

BARE has the exact residual-support law

```text
k19 BARE
->
every prime divisor of R is 1 mod19.
```

But the forced prime is

```text
11 = 11 mod19,
```

not `1 mod19`.

Hence

```text
11|R
->
k19 BARE impossible.
```

Therefore the simultaneous-survivor statement is

```text
h169 realized pair route
+ k11 miss
+ t=8 mod11
+ k19 miss

=>

k19 mode = FULL_QR.
```

This is a genuine product-state deletion. A phase obligation created at k11 kills one of the exact k19 survivor modes.

---

## 4. The same phase also cuts the valuation resource

There is a second, independent consequence.

The factor11 seed has order three modulo19 and supplies the exact q19 subgroup

```text
K={0,6,12}
```

in exponent coordinates.

The weighted Type-II-miss automaton already proves

```text
generic h169 k19 Type-II miss:
Omega_NR(C19) <= 8.
```

Starting from the forced seed11 state gives

```text
phase t=8 mod11:
Omega_NR(C19) <= 2.
```

So one ancestry fact produces two contractions at once:

```text
horizontal:
BARE deleted

vertical:
NR valuation budget 8 -> 2.
```

This is exactly the coupling we need if valuation escape is to become part of a contradiction machine rather than a separate side problem.

---

## 5. Obligation form

The selected child can be written as a short exact obligation chain:

```text
k11 miss
-> t11 in {0,2,3,4,8}

choose t11=8
-> T11=2
-> 11|C19

C19=S*R, gcd(S,11)=1
-> 11|R

k19 BARE
-> support(R) subset {1 mod19}

11 mod19 != 1
-> contradiction

therefore
k19 miss -> FULL_QR.
```

At the same time:

```text
11 seed at q19
-> exact Type-II-miss NR budget <=2.
```

The same proof-state edge therefore carries both a mode obligation and a bounded valuation resource.

---

## 6. Why this is more useful than another census

No prime range is used.

No empirical absence is promoted to a theorem.

No assumption is made that `t=8 mod11` is the only k11 child.

The result is a reusable exact rule:

```text
IF
    h169 pair-route context
    AND inherited k11 miss
    AND t mod11=8
    AND k19 survives
THEN
    k19_mode=FULL_QR
    Omega_NR(C19)<=2.
```

That is the sort of object the obligation propagator can consume immediately.

---

## 7. Relation to the future factor-11 calendar

The same h169 phase has

```text
t=8 mod11
T=2 mod11.
```

Factor11 is already present at k19, and its next post-k23 re-entry occurs at

```text
k63.
```

Thus the state carries a recurrence-like ancestry signature:

```text
11 enters C19
...
11 re-enters the post-k23 ladder at C63.
```

The k19 occurrence is already strong enough to delete BARE and cut the NR budget. The later k63 occurrence is a separate seeded-state target for future exact grammar work.

---

## 8. Contradiction-core interpretation

Inside an obligation engine, the impossible partial state

```text
t mod11 = 8
k19_mode = BARE
```

has a short theorem-backed explanation:

```text
t11=8
-> 11|R

BARE
-> every q|R is 1 mod19

11 mod19=11
-> contradiction.
```

This is more valuable than returning only an empty formal state. It identifies the precise arithmetic collision that killed it.

Repeated collisions of this form are candidates for parametric survivor-elimination lemmas.

---

## 9. Executable verifier

Run

```sh
python3 research/verify_h169_k11_phase2_k19_collapse.py
```

It verifies:

```text
the exact h169 k11 t mod11 phase domain,
t=8 -> T=2 mod11,
T=2 -> 11|C19,
the Route-A and Route-B fixed seed factorizations,
gcd(S,11)=1 on both routes,
the landed BARE residual-support law,
11 mod19 != 1,
BARE exclusion,
the generic q19 NR valuation budget 8,
the seed11 NR valuation budget 2,
and absence of positive-NR cycles in the seeded miss SCCs.
```

---

## 10. Claim boundary

The theorem does not say a k11 miss forces `t=8 mod11`; four other allowed h169 k11 phases remain.

It is scoped to the realized h169 pair-route simultaneous-survivor laboratory whose exact k19 modes and affine route seeds are already landed.

It does not prove that k19 must miss, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
