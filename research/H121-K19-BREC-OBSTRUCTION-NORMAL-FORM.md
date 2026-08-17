# h121 k=19 BREC obstruction normal form

**Status:** exact class-conditioned lemma  
**Date:** 2026-08-17  
**Hard class:** `p = 121 mod 840`  
**Application:** `CBX-Lane-I-shift-history-v1`

## 1. Statement

Let `p` be a Mordell-hard prime in the class

```text
p = 121 mod 840
```

and define

```text
C_19 = (p+19)/4.
```

Then

```text
sigma_19(p) = -
```

if and only if every prime divisor of `C_19` is a quadratic residue modulo 19.

Equivalently, the presence of **any** quadratic-nonresidue prime divisor of `C_19` forces a combined `k=19` construction.

In this hard class the Type-I and Type-II targets therefore have exact coincident hit/miss status at `k=19`.

---

## 2. Why h121 is special

The class `121 mod840` satisfies

```text
p = 1 mod5
p = 2 mod7.
```

Since

```text
19 = 4 mod5,
19 = 5 mod7,
```

we have

```text
p+19 = 0 mod5
p+19 = 0 mod7.
```

Because `4` is invertible modulo both 5 and 7,

```text
5 divides C_19
7 divides C_19.
```

Thus every h121 `k=19` cofactor carries the forced factor pair

```text
5 * 7.
```

---

## 3. Their support modulo 19

The quadratic-residue subgroup modulo 19 has order 9.

The forced factor `5` is a quadratic residue of exact order 9, so it generates the whole QR subgroup abstractly. With valuation one, however, its signed local support contains only

```text
{5^(-1),1,5}.
```

The forced factor `7` is also a quadratic residue and satisfies

```text
7 = 5^6 mod19,
```

with order 3.

Its valuation-one signed support is

```text
{7^(-1),1,7}.
```

Write the QR subgroup additively in exponents of `5`, modulo 9.

The factor `5` contributes

```text
{0,+1,-1}.
```

The factor `7=5^6` contributes

```text
{0,+3,-3}.
```

Their sumset is

```text
{0,+/-1,+/-2,+/-3,+/-4},
```

which is every residue modulo 9.

Therefore the two forced factors alone give the entire quadratic-residue subgroup:

```text
Q_19 subseteq R_19(C_19).
```

Since all contributions from the forced pair are quadratic residues, their exact support is `Q_19`.

---

## 4. One nonresidue fills the unit group

If some prime divisor `q` of `C_19` is a quadratic nonresidue modulo 19, then signed exponent `+1` makes `q` available.

Multiplying by the already-complete QR subgroup gives

```text
q Q_19,
```

which is the full nonresidue coset.

Hence the signed box contains

```text
Q_19 union qQ_19 = (Z/19Z)^x.
```

Both exact targets are therefore hit.

---

## 5. If all factors are QR, both targets miss

If every prime divisor of `C_19` is a quadratic residue modulo 19, the entire signed box remains inside `Q_19`.

Because

```text
p = 4C_19 mod19
```

and `4` is a square, `p` is then also a quadratic residue modulo 19.

The Type-II target is

```text
-1 = 18 mod19,
```

which is a quadratic nonresidue because `19 = 3 mod4`.

The Type-I target is

```text
-p^(-1).
```

Since `p^(-1)` is QR and `-1` is NR, the Type-I target is NR as well.

Thus neither target can lie in the QR-only signed box.

This proves

```text
sigma_19(p) = -
iff
all prime divisors of C_19 are QR mod19.
```

---

## 6. Translation to the q=23 rescue branch

For a q23 Type-I-only rescue write

```text
M = HD,
C_23 = 6M,
p = 24M - 23.
```

The h121 hard class corresponds exactly to

```text
M = 6 mod35.
```

The affine cofactor recurrence gives

```text
C_19 = 6M - 1.
```

When `M=6 mod35`,

```text
6M-1 = 0 mod35,
```

so the forced `5*7` pair is visible directly in the consecutive-cofactor block.

The exact h121 `k=19` obstruction therefore becomes

```text
M = 6 mod35
and
sigma_19 = -
iff
every prime divisor of 6M-1 is QR mod19.
```

---

## 7. Relation to the known q23 falsifiers

The shallow Type-I-only witness

```text
p = 5,151,841
```

lies in hard class `121 mod840`, but its early history is

```text
-++-+
```

so it constructs at `k=19` rather than entering the h121 obstruction branch.

The deeper exact `-----` q23 Type-I-only witnesses currently preserved are in the harder h169 class, where the forced `5*7` saturation mechanism is absent.

That separation is useful: the k19 problem is not equally difficult across the six Mordell-hard classes.

---

## 8. Executable verification

The exact finite-group obligations are frozen in

```text
research/verify_h121_k19_brec_obstruction_normal_form.py
```

Run:

```sh
python3 research/verify_h121_k19_brec_obstruction_normal_form.py
```

The verifier checks:

```text
h121 mod5 and mod7 forced factors,
5 and 7 are QR mod19,
ord_19(5)=9,
ord_19(7)=3,
7=5^6 mod19,
the forced signed supports fill Q_19,
every NR representative sends Q_19 to the complete NR coset,
and both targets are NR whenever C_19 is QR-only.
```

---

## 9. Current k19 frontier

The exact class-conditioned result suggests splitting `k=19` by hard class rather than searching for one opaque universal rule.

The six q23 rescue hard classes correspond to

```text
p mod840    M mod35
-------------------
1              1
121            6
169            8
289           13
361           16
529           23
```

The h121 row is now solved at `k=19` by forced QR-subgroup saturation.

The full `-----` one-sided q23 rescue witnesses occur in h169, making that class the immediate unresolved BREC target.

---

## 10. Claim boundary

This theorem is exact only for the hard class

```text
p = 121 mod840.
```

It does not classify `k=19` for h1, h169, h289, h361, or h529, and it does not establish a global Lane-I ceiling or an Erdős–Straus proof.
