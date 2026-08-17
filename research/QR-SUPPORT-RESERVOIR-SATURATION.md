# Quadratic-residue support reservoir saturation

**Status:** exact reusable signed-box lemma  
**Date:** 2026-08-17  
**Scope:** prime Lane-I moduli `q = 3 mod4`  
**Claim boundary:** local signed-box theorem; not a global shift selector or Erdős–Straus proof

## 1. Reservoir lemma

Let `q` be an odd prime with

```text
q = 3 mod4.
```

Let `C` be a q-unit Lane-I cofactor and factor it as

```text
C = A*B.
```

Assume:

1. every prime-factor occurrence used in `A` is a quadratic residue modulo `q`;
2. the exact signed-box support of `A` is the entire quadratic-residue subgroup

```text
R_q(A) = Q_q.
```

Then the full exact signed box of `C` has only two possibilities relevant to the two Lane-I targets.

### If every prime divisor of B is QR

All factors of `C` are QR, so

```text
R_q(C) subset Q_q.
```

But `A` already supplies all of `Q_q`, therefore

```text
R_q(C) = Q_q.
```

At fixed prime shift `q`,

```text
p = 4C mod q.
```

Since both `4` and `C` are QR,

```text
p is QR mod q.
```

Because `q=3 mod4`, `-1` is a quadratic nonresidue. Hence both exact targets

```text
Type II : -1
Type I  : -p^(-1)
```

lie in the nonresidue coset and both miss.

### If B has any NR prime divisor r

Choose that factor occurrence with signed exponent `+1` and all other B factors with exponent zero. Since the A-reservoir independently supplies every element of `Q_q`, the full box contains

```text
r*Q_q,
```

which is the entire nonresidue coset.

It also contains `Q_q` by choosing exponent zero on every B factor. Therefore

```text
R_q(C) = Q_q union rQ_q = U(q).
```

Both exact targets hit.

Thus:

```text
R_q(A)=Q_q from a QR-only subfactor A

=>

combined miss at k=q
iff
every prime divisor of B is QR mod q.
```

In this reservoir regime, Type-I and Type-II hit/miss status coincide exactly.

---

## 2. Why the factor partition matters

The lemma is stronger than merely observing

```text
Q_q subset R_q(C).
```

The QR subgroup must be supplied by a factor subcollection `A` independently of any nonresidue factor used to generate the opposite coset.

That independence is what licenses the product

```text
r * Q_q.
```

This is why forced small-factor reservoirs are so useful: their support can be proved complete before the residual cofactor is examined.

---

## 3. h121 k19 is the cleanest instance

For

```text
p = 121 mod840,
q = 19,
```

we have

```text
35 = 5*7 | C19.
```

Both factors are QR modulo 19, and their valuation-one signed supports satisfy

```text
R_19(5*7) = Q_19.
```

So choose

```text
A=5*7.
```

The reservoir lemma immediately gives

```text
sigma_19(p)=-
iff
every prime divisor of C19 is QR mod19.
```

This recovers the exact h121 k19 obstruction normal form from one reusable group principle.

---

## 4. k11 saturation from v3 >= 2

Modulo 11, the QR subgroup has order five and `3` is a generator of it.

If

```text
v3(C11) >= 2,
```

then the subfactor

```text
A=3^2
```

has exact signed exponents

```text
-2,-1,0,1,2,
```

which cover the entire order-five subgroup. Hence

```text
R_11(3^2)=Q_11.
```

The reservoir lemma therefore gives:

```text
v3(C11)>=2
=>
sigma_11=- iff every prime divisor of C11 is QR mod11.
```

This explains structurally why the genuinely thin q11 branch is confined to

```text
v3(C11)=1.
```

The general k11 normal form already proves that fact by exhaustive local classification; the reservoir lemma reveals the subgroup mechanism behind it.

---

## 5. h1 / h361 k19 valuation threshold

For hard classes

```text
p mod840 in {1,361},
```

the literal prime `5` is forced into `C19`.

Modulo 19,

```text
ord_19(5)=9,
```

and `5` generates the full QR subgroup.

A single valuation supplies only three signed powers, so it does not yet saturate `Q_19`. But if

```text
v5(C19) >= 4,
```

then the subfactor

```text
A=5^4
```

contributes signed exponents

```text
-4,-3,-2,-1,0,1,2,3,4,
```

which are all nine elements of the order-nine QR subgroup.

Therefore, in either hard class 1 or 361,

```text
v5(C19)>=4
=>
sigma_19=- iff every prime divisor of C19 is QR mod19.
```

Equivalently, once the forced 5-adic reservoir reaches valuation four, any single nonresidue factor is automatically constructive for both exact targets.

This does not classify the lower-valuation cases `v5=1,2,3`.

---

## 6. General saturation threshold for a QR generator

Suppose a QR residue `g` has exact order

```text
m = (q-1)/2
```

inside `Q_q`, and `m` is odd because `q=3 mod4`.

A prime power occurrence `g^e` contributes the signed exponent interval

```text
-e,-e+1,...,e
```

inside the cyclic order-m QR subgroup.

Therefore

```text
e >= (m-1)/2
```

is sufficient to cover all `m` QR exponents.

For the two applications above:

```text
q=11: m=5  -> threshold e=2
q=19: m=9  -> threshold e=4.
```

This gives a generic valuation-to-reservoir mechanism wherever an actual rational prime factor lands in a QR generator class.

---

## 7. Algorithmic consequence

A theorem-safe Lane-I evaluator can recognize a saturated QR reservoir before exploring the full signed box.

Once a QR-only factor subcollection has exact support `Q_q`:

```text
residual cofactor all QR  -> exact combined miss
residual cofactor has NR  -> exact combined construction.
```

So after reservoir saturation, the expensive target-support question collapses to a quadratic-character classification of the residual prime factors.

This is useful both for exact search acceleration and for symbolic dependency grammars, but only after the reservoir condition itself has been proved for the branch.

---

## 8. Executable verification

Run

```sh
python3 research/verify_qr_support_reservoir_saturation.py
```

The verifier checks the concrete exact reservoirs used here:

```text
R_19(5*7)=Q_19,
R_11(3^2)=Q_11,
R_19(5^4)=Q_19,
```

then exhausts all nonresidue representatives in each application and verifies that multiplying the reservoir by one NR occurrence fills the complete unit group. It also checks the target-character implication for every QR cofactor residue.

The general lemma is the elementary coset proof above; the executable verifier protects the concrete repository applications against arithmetic transcription errors.

---

## 9. Claim boundary

The reservoir lemma is an exact local signed-box theorem.

It does not prove that a required reservoir occurs in every hard class or every shift, does not classify unsaturated residual cases, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
