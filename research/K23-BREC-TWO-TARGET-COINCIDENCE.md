# k=23 BREC two-target coincidence frontier

**Status:** exact finite census result and theorem target  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`  
**Claim boundary:** every count below is finite; no universal theorem is claimed

## 1. Why this matters

The exact prime Erdős–Straus Lane-I condition at an admissible shift `k` asks whether the signed box

```text
R_k(C),   C=(p+k)/4
```

contains at least one of two targets:

```text
Type II: -1
Type I : -p^(-1)
```

The current exact-ES frontier identifies the Type-I companion at `k=23` as the next target after the combined `k=19` corridor filter.

BREC changes the way that question can be asked. Instead of looking at `k=23` in isolation, it conditions the target on the exact earlier obstruction ancestry.

The first five BREC coordinates are

```text
k = 3, 7, 11, 15, 19.
```

Thus the parent

```text
-----
```

means that **both** exact targets missed at each of those five earlier shifts.

The finite data now indicates something sharper than an independent Type-I rescue mechanism:

> after even the first exact `k=3` combined miss, Type-I and Type-II occupancy at `k=23` coincide throughout the current two-million-prime census.

That suggests the Type-I companion may be approachable as a **conditional target-coincidence theorem**.

---

## 2. Reproducible census identity

Initial preserved corpus:

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

The corpus contains exactly

```text
4519 Mordell-hard primes.
```

The optimized BREC engine and the independent standalone Lane-I reference agree exactly on the entire finite grade:

```text
90,380 target stages
90,380 exact factorizations
37,146 constructive stages
53,234 obstructive stages
0 undefined stages
```

The BREC evaluator used the collapsed exact target pair

```text
{-1,-p^(-1)}
```

and one signed-box traversal per stage. Every one of the 90,380 coprimality tests was eliminated by the prime `p>K` shortcut on this grade.

---

## 3. Unconditioned k=23 target states

Reconstructing the exact signed box at `k=23` for all 4519 hard primes gives four possible local states.

The finite census is:

```text
both targets hit      2956
neither target hits   1561
Type-I only              2
Type-II only             0
----------------------------
total                  4519
```

The only two Type-I-only rescues are

```text
p = 1,544,209
p = 1,911,841
```

Both have a `k=23` nonresidue-factor pattern

```text
14^2 mod 23.
```

Their BREC histories begin with `+`, so neither survives the first exact combined obstruction at `k=3`.

This observation is the first key contraction.

---

## 4. One negative ancestor removes every observed one-sided k=23 state

Condition only on

```text
sigma_3(p) = -.
```

There are

```text
2770
```

such primes through two million.

At fixed target `k=23` they split as

```text
both targets hit      1792
neither target hits    978
Type-I only              0
Type-II only             0
----------------------------
total                  2770
```

So throughout this exact finite corpus,

```text
k=3 combined miss
    =>
[-1 in R_23(C_23)] iff [-p^(-1) in R_23(C_23)].
```

This is **not yet a theorem**. It is a precise theorem target.

### Candidate K23-C1: conditional two-target coincidence

For every Mordell-hard prime `p`, let

```text
C_3  = (p+3)/4,
C_23 = (p+23)/4.
```

Candidate statement:

```text
if neither {-1,-p^(-1)} lies in R_3(C_3),
then
-1 lies in R_23(C_23)
iff
-p^(-1) lies in R_23(C_23).
```

A proof of this implication would absorb the Type-I companion into the existing `k=23` Type-II classification on the `k=3` obstruction branch.

---

## 5. Recursive contraction through the corridor

Keep the target fixed at `k=23` while adding earlier all-negative BREC ancestry.

The exact two-million-prime populations are:

```text
ancestry    primes at target    both    neither    I-only    II-only
--------------------------------------------------------------------
empty             4519          2956      1561        2         0
-                 2770          1792       978        0         0
--                1781          1164       617        0         0
---                711           462       249        0         0
----               480           315       165        0         0
-----              237           149        88        0         0
```

The target-coincidence phenomenon therefore appears immediately at depth one and survives every deeper obstruction condition tested.

This is a particularly clean BREC effect: the target itself does not move. Only its exact ancestry is tightened.

---

## 6. The anchored ----- parent at k=23

The deepest parent needed for the current corridor is

```text
-----
```

through `k=19`.

It contains exactly

```text
237
```

primes through two million.

At `k=23`:

```text
-----+     149
------      88
```

Every one of the 149 constructive children hits **both** exact targets.

Every one of the 88 obstructive children misses **both** exact targets.

There are no one-sided target states.

---

## 7. Exact signed-box geometry of the constructive child

For all 149 primes in `-----+`, the factorization of

```text
C_23=(p+23)/4
```

has the forced common factors

```text
2 and 3,
```

so

```text
gcd(C_23 over the child) = 6.
```

The exact signed-box support sizes modulo 23 are:

```text
support size 22    125 primes
support size 20     22 primes
support size 18      2 primes
```

Since the unit group modulo 23 has size 22,

```text
125 / 149
```

constructive children already fill the entire unit group.

The remaining 24 still contain both targets despite small support defects.

Observed missing-residue patterns are:

```text
support 20: missing {9,18}
support 18: missing {5,9,14,18}
```

Neither pattern removes `-1`, and neither removes the corresponding Type-I target for those primes.

---

## 8. Exact signed-box geometry of the obstructive child

The 88 primes in `------` again satisfy

```text
gcd(C_23 over the child) = 6.
```

Their signed-box support is dramatically more rigid:

```text
support size 11     86 primes
support size 19      2 primes
support size 22      0 primes
```

### Main branch: 86 / 88

For 86 primes the signed-box support is exactly the quadratic-residue subgroup modulo 23:

```text
{1,2,3,4,6,8,9,12,13,16,18}.
```

Because `23 = 3 mod 4`,

```text
-1 = 22
```

is a quadratic nonresidue and is automatically absent.

Every prime factor of `C_23` lies in a quadratic-residue class modulo 23 on this branch.

### Thin branch: 2 / 88

Exactly two obstructive primes escape pure quadratic splitting:

```text
p =   415,969
C =   103,998 = 2 * 3 * 17,333
17,333 = 14 mod 23

p = 1,915,201
C =   478,806 = 2 * 3 * 79,801
79,801 = 14 mod 23
```

For both primes the signed-box support has size 19 and misses exactly

```text
{9,18,22}.
```

Their Type-I target is

```text
18,
```

while the Type-II target is

```text
22.
```

Both targets are therefore absent for the same exact three-residue defect.

This is the surviving `14^1` thin-defect branch of the known `q=23` Type-II filter.

---

## 9. How the q=23 Type-II defect grammar contracts under BREC ancestry

The existing exact `q=23` Type-II filter permits a pure quadratic branch and thin nonresidue defects involving primitive classes `5` and `14`.

The fixed-target BREC census shows the following contraction among **combined k=23 misses**:

```text
ancestry    QR branch    14^1    5^1    5^1*14^1
-------------------------------------------------
empty          1490        37      32        2
-               929        25      23        1
--              591        14      11        1
---             241         6       2        0
----            159         4       2        0
-----            86         2       0        0
```

By the time the prime has survived the combined exact filters through `k=19`, every observed class-5 thin defect has disappeared.

Only two class-14 single defects remain.

### Candidate K23-C2: deep thin-defect contraction

A natural theorem target is therefore:

```text
combined misses at k=3,7,11,15,19
and combined miss at k=23
```

force either

```text
(A) pure quadratic splitting modulo 23,
```

or a sharply constrained class-14 defect.

The finite data suggests the class-14 branch may collapse all the way to

```text
C_23 = 6r,
r prime,
r = 14 mod 23,
```

but that stronger statement is currently only a finite observation.

---

## 10. The important inversion of the search question

Before BREC, the immediate frontier question was naturally phrased:

> Can Type I rescue the remaining Type-II failures at `k=23`?

The current finite evidence suggests a different route:

> Why does earlier combined obstruction destroy the one-sided Type-I rescue states, making Type-I and Type-II occupancy coincide at `k=23`?

That is a more structural question.

The two exceptional unconditioned Type-I-only primes show that target coincidence is **not** an unconditional identity at `k=23`.

The fact that both exceptions disappear after one `k=3` combined miss gives a concrete place to attack the implication.

The desired proof object is therefore not a statistical scheduler rule. It is an exact compatibility theorem between the `k=3` obstruction geometry and the `k=23` signed-box defect grammar.

---

## 11. Executable research path

Generate and independently verify the finite corpus:

```sh
kernel/cbx-standalone-i \
  --hi 2000000 \
  --i-max 80 \
  > standalone-summary.json

kernel/cbx-brec-i \
  --hi 2000000 \
  --i-max 80 \
  --order 8 \
  --histories brec-histories.tsv \
  > brec-summary.json

python3 kernel/verify_brec_i.py \
  standalone-summary.json \
  brec-summary.json
```

Trace the fixed `k=23` target through increasing ancestry:

```sh
python3 kernel/analyze_brec_target.py \
  brec-histories.tsv \
  --target-k 23 \
  --max-prefix-depth 5
```

Inspect the exact deepest parent geometry:

```sh
python3 kernel/analyze_brec_cylinder.py \
  brec-histories.tsv \
  --prefix='-----'
```

The CI workflow preserves all of these finite outputs and freezes the canonical two-million-prime counts as regression facts.

---

## 12. Next mathematical attack

The next proof work should proceed in this order:

1. **Classify the two unconditioned Type-I-only states.**  Both are `14^2` Type-II thin defects at `k=23`.
2. **Prove or falsify K23-C1.**  Determine whether the `k=3` combined miss algebraically excludes every one-sided `k=23` target state.
3. **Push the implication through the known q=23 defect normal form.**  This should reduce the proof to finitely many residue/valuation patterns rather than arbitrary factorizations.
4. **Classify the deep `-----` obstruction child.**  Explain why the class-5 defect disappears and why the surviving class-14 defect has the observed three-residue hole `{9,18,22}`.
5. **Only after an exact theorem exists**, feed it back into the CBX pruning/scheduling layer.

BREC has therefore done something useful beyond visualization: it has identified a conditional equivalence statement that the old first-hit view could not naturally expose.

---

## 13. Claim boundary

The equations defining each signed box, each target, each factorization, and each finite count above are exact for the stated corpus.

The following are **not** yet proved universally:

```text
K23-C1 conditional two-target coincidence,
K23-C2 deep thin-defect contraction,
any finite k ceiling,
Erdős-Straus.
```

The purpose of this note is to freeze the new theorem targets with enough executable provenance that they can be attacked and independently falsified.
