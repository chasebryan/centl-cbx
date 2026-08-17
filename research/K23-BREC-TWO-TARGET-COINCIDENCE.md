# k=23 BREC two-target coincidence: finite phase and falsification

**Status:** finite coincidence preserved; universal extrapolation **FALSIFIED**  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`  
**Claim boundary:** finite counts are exact; the former K23-C1/K23-C2 extrapolations are not theorems

## 1. Result in one sentence

The first `p <= 2,000,000` BREC corpus displayed a striking Type-I / Type-II target coincidence at fixed `k=23` after all-negative ancestry, but exact larger witnesses now show that **no all-negative prefix of depths 1 through 5 forces that coincidence universally**.

This is a productive falsification. It removes a seductive but false shortcut while leaving a stronger exact residue classification behind:

> inside the known `q=23` Type-II miss normal form, **Type I rescues exactly the same-class valuation-two thin defects `5^2` and `14^2`.**

That classification, rather than ancestry coincidence, is now the correct immediate object.

---

## 2. The initial two-million-prime phase

Preserved corpus:

```text
branch      research/brec-recursive-engine
commit      79ca809c3cf1991e0c440848c77f0812041cef2a
workflow    BREC recursive engine
run id      31997927195
artifact    brec-finite-census-2000000-K80-N8
p bound     2,000,000
k bound     80
BREC order  8
```

The corpus contains exactly 4519 Mordell-hard primes. The optimized BREC engine and the independent standalone Lane-I reference agree exactly on:

```text
90,380 target stages
90,380 exact factorizations
37,146 constructive stages
53,234 obstructive stages
0 undefined stages
```

At fixed `k=23`, before conditioning on ancestry:

```text
both targets hit      2956
neither target hits   1561
Type-I only              2
Type-II only             0
----------------------------
total                  4519
```

The two Type-I-only primes in this small corpus are:

```text
1,544,209
1,911,841
```

Both realize the `14^2` nonresidue defect pattern modulo 23.

Conditioning on even one initial combined miss appeared to delete every one-sided state:

```text
ancestry    primes at k23    both    neither    I-only    II-only
-----------------------------------------------------------------
empty             4519       2956      1561        2         0
-                 2770       1792       978        0         0
--                1781       1164       617        0         0
---                711        462       249        0         0
----               480        315       165        0         0
-----              237        149        88        0         0
```

Those rows remain exact finite facts. What failed was the inference that the observed coincidence should continue universally.

---

## 3. K23-C1 is false

The former candidate K23-C1 proposed:

```text
k=3 combined miss
    =>
[-1 in R_23(C_23)] iff [-p^(-1) in R_23(C_23)].
```

Exact falsifier:

```text
p = 5,151,841
p mod 840 = 121
```

This is a Mordell-hard prime.

At `k=3`:

```text
C_3 = (p+3)/4 = 1,287,961
C_3 is prime
C_3 = 1 mod 3
signed-box support mod 3 = {1}
target = 2
```

so the exact combined `k=3` state is a miss:

```text
sigma_3(p) = -.
```

But at `k=23`:

```text
C_23 = 1,287,966
     = 2 * 3 * 97 * 2213
97   = 5 mod 23
2213 = 5 mod 23
```

The nonresidue pattern is therefore

```text
5^2.
```

The signed box has size 21 and misses `-1=22`, while containing the Type-I target:

```text
Type-II target = 22    miss
Type-I target  = 11    hit
```

Thus

```text
k=3 miss
and
k=23 Type-I-only rescue.
```

K23-C1 is disproved.

---

## 4. Deeper all-negative ancestry also fails to force coincidence

The falsification is not confined to depth one.

Exact explicit witnesses:

```text
p =  8,243,281
history through k=19 = ---++
k23 state            = Type-I-only
q23 defect            = 14^2
```

This falsifies coincidence after `--` and after `---` ancestry.

More importantly:

```text
p = 18,766,609
history through k=19 = -----
k23 state            = Type-I-only
q23 defect            = 14^2
```

and

```text
p = 27,211,969
history through k=19 = -----
k23 state            = Type-I-only
q23 defect            = 5^2
```

These two witnesses falsify coincidence after both `----` and the full `-----` parent used by the current corridor.

Therefore the statement

```text
all-negative BREC ancestry of any depth 1..5
forces Type-I/Type-II coincidence at k=23
```

is false.

The executable witness verifier is:

```text
research/verify_k23_brec_ancestry_falsifiers.py
```

It reconstructs every relevant shift directly from exact factorization and signed-box support. It does not trust a pre-recorded history string.

---

## 5. What survives the falsification

The useful exact reduction is the `q=23` Type-I companion classification.

The known Type-II miss normal form contains either:

```text
(A) pure quadratic splitting modulo 23,
```

or a thin defect with

```text
v2(C)=v3(C)=1,
all remaining QR factors = 1 mod 23,
primitive NR classes only 5 and 14,
total NR valuation <= 2.
```

Since residue-1 factors do not change the signed box, there are only six thin residue states to inspect:

```text
(a5,a14) =
(0,0),
(1,0),
(0,1),
(2,0),
(1,1),
(0,2).
```

Exact unit-group exhaustion gives:

```text
pattern       support size     Type-II     Type-I      local class
-------------------------------------------------------------------
QR / 0,0            9            miss        miss         miss
5^1                19            miss        miss         miss
14^1               19            miss        miss         miss
5^2                21            miss        hit          I-only
5^1*14^1           21            miss        miss         miss
14^2               21            miss        hit          I-only
```

So, **conditional on the exact q=23 Type-II normal form**:

```text
Type-I-only rescue
iff
same-class valuation-two defect: 5^2 or 14^2.
```

This finite residue-group statement is executable in:

```text
research/verify_k23_typei_companion_patterns.py
```

Unlike K23-C1, this classification is not a corpus frequency extrapolation. It exhausts the six residue states permitted by the stated normal form.

---

## 6. The two-million `-----` cylinder remains useful, but only as a finite laboratory

At `p <= 2,000,000`, the `-----` parent contained 237 primes and split at `k=23` as:

```text
-----+   149
------    88
```

All 149 constructive children hit both targets. All 88 obstructive children missed both.

Their signed-box support geometry was especially clean:

```text
constructive support size 22    125
constructive support size 20     22
constructive support size 18      2

obstructive support size 11       86
obstructive support size 19        2
```

The 86 size-11 obstruction boxes equal the quadratic-residue subgroup modulo 23. The two size-19 obstruction boxes were single `14^1` defects.

This remains valuable structural evidence, but the larger `-----` Type-I-only witnesses show that the cylinder eventually admits valuation-two same-class defects as well.

So the correct question is no longer:

> Why does the `-----` parent eliminate one-sided states?

It is:

> **What arithmetic controls when a same-class valuation-two `5^2` or `14^2` q23 defect is compatible with a given earlier BREC ancestry?**

That question survived contact with larger data.

---

## 7. The new theorem-hunting target

BREC has still narrowed the work significantly.

The Type-I companion at `k=23` is no longer an arbitrary second target. Within the known Type-II miss normal form, it is localized to exactly two residue patterns:

```text
5^2
14^2.
```

Therefore the next exact program should be:

1. derive the full integer normal form of the `5^2` and `14^2` branches, including multiplicity split across one or two prime factors;
2. express each earlier shift condition `k=3,7,11,15,19` on those branches;
3. identify which earlier signed-box constraints are independent and which merely postpone the first realizable one-sided prime;
4. search for a genuine incompatibility theorem only after the parametric branch has been exposed;
5. retain explicit falsifiers as permanent regression tests so no future finite-census illusion is promoted again.

This is a better target than K23-C1 because it is based on an exact exhaustive residue classification rather than an observed absence.

---

## 8. Research lesson from BREC

BREC did not fail here. It did exactly what an X-ray calculus should do.

At two million, the recursive ancestry exposed a striking apparent collapse. Extending the arithmetic then found the hidden re-entry:

```text
obstruction ancestry
    -> apparent target coincidence
        -> larger-scale Type-I-only re-entry.
```

That is precisely the sort of structure a first-hit-only view would hide.

The recursive framework therefore gives us two useful objects at once:

```text
positive evidence: finite contractions worth explaining
negative evidence: exact histories that kill false extrapolations early
```

Both belong in CBX.

---

## 9. Executable verification

Run the exact q23 residue classification:

```sh
python3 research/verify_k23_typei_companion_patterns.py
```

Run the explicit ancestry falsifiers:

```sh
python3 research/verify_k23_brec_ancestry_falsifiers.py
```

The normal BREC finite-census workflow remains:

```sh
kernel/cbx-standalone-i --hi 2000000 --i-max 80 > standalone-summary.json

kernel/cbx-brec-i \
  --hi 2000000 \
  --i-max 80 \
  --order 8 \
  --histories brec-histories.tsv \
  > brec-summary.json

python3 kernel/verify_brec_i.py standalone-summary.json brec-summary.json
```

The first two verifiers are now the important guards: they preserve both the exact surviving q23 companion classification and the explicit counterexamples to the discarded ancestry-coincidence hypothesis.

---

## 10. Frozen status

The following former candidates are **falsified**:

```text
K23-C1  k3 combined miss forces k23 target coincidence
K23-C2  deep ----- ancestry eliminates same-class valuation-two rescue
```

The following exact conditional classification survives:

```text
within the known q23 Type-II miss normal form,
Type-I-only rescue occurs exactly for 5^2 or 14^2 thin defects.
```

Erdős–Straus remains open. No finite `k` ceiling or universal ancestry pruning rule is established by this work.
