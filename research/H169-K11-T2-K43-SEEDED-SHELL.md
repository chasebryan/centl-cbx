# h169 k11 t=2 mod11 -> seeded k43 shell

**Status:** exact cross-coordinate seeded-state theorem  
**Date:** 2026-08-17  
**Scope:** h169 under inherited k11 combined miss  
**Verifier:** `verify_h169_k11_t2_k43_seeded_shell.py`

## 1. The unresolved k11 child lands directly on k43

Write

```text
p = 169 + 840t
T = (p+23)/24 = 8 + 35t.
```

The exact h169 k11 theorem gives

```text
k11 miss
->
t mod11 in {0,2,3,4,8}.
```

The child

```text
t=2 mod11
```

has

```text
T=1 mod11.
```

Since the post-k23 ladder is

```text
C_(23+4j)=6T+j,
```

at k43 we have `j=5`, hence

```text
C43=6T+5=11=0 mod11.
```

Therefore

```text
h169 + inherited k11 miss + t=2 mod11
->
11 | C43.
```

This turns the previously unresolved k43 child into a seeded exact signed-box problem.

---

## 2. Literal factor11 supplies a concrete q43 signed shell

Modulo43, primitive root3 gives

```text
11 = 3^30 mod43
ord_43(11)=7.
```

One forced factor occurrence contributes

```text
{11^-1,1,11}
=
{4,1,11}.
```

So before any other prime factor of `C43` is inspected, the exact signed support already contains

```text
{1,4,11}.
```

This is proof-bearing support, not a probabilistic character annotation.

---

## 3. Exact local state contraction

The unseeded q43 Type-II-miss automaton has

```text
18,048 Type-II-miss states
 = 7,740 combined misses
 + 10,308 Type-I-only states.
```

Its largest minimal abstract factor-occurrence depth is

```text
5.
```

Starting instead from one forced factor11 gives

```text
2,317 Type-II-miss states
 = 1,217 combined misses
 + 1,100 Type-I-only states,
```

with maximal minimal depth

```text
4.
```

Therefore the ancestry seed removes exactly

```text
15,731 Type-II-miss states
6,523 combined-miss states.
```

This is an exact finite local closure comparison. It is not a density claim about h169 primes.

---

## 4. Three factor residues become immediate Type-II absorbers

From the forced seed support `{1,4,11}`, add one additional prime-factor occurrence with residue `r mod43`.

Exhausting all 41 non-inert unit residues gives exactly three residues for which Type II is hit immediately:

```text
r in {32,39,42} mod43.
```

For each of those residues, the one-occurrence state actually hits both targets.

Thus any seeded q43 Type-II miss must satisfy the exact support exclusion

```text
q | C43/11
and Type II misses
->
q mod43 not in {32,39,42}
```

for every prime-factor occurrence `q` outside the distinguished forced copy of11.

Because signed support only expands as factor occurrences are added, a later factor cannot repair such a hit.

---

## 5. The seed creates a new combined-miss phase exclusion

Without any seed, a q43 combined miss already cannot have

```text
C43 mod43 in {32,42}.
```

The reasons are structural:

```text
C43=32 -> p=4C43=-1 mod43 -> Type-I target=1,
and 1 is always in every signed box.

C43=42=-1 -> C43 itself is in the signed box -> Type II hit.
```

The forced factor11 adds one new exclusion:

```text
C43 != 8 mod43.
```

Indeed,

```text
C43=8
-> p=4C43=32 mod43
-> Type-I target -p^-1 = 4.
```

But `4` is already present in the factor11 seed support `{1,4,11}`.

Therefore a seeded combined miss must have

```text
C43 mod43 not in {8,32,42}.
```

---

## 6. The new C43 exclusion becomes an h169 t-phase exclusion

On h169,

```text
p=169+840t
 = 40+23t mod43.
```

The new seeded exclusion `C43=8` is equivalent to

```text
p=32 mod43.
```

Solving on the h169 progression gives exactly

```text
t=9 mod43.
```

Hence the cross-coordinate theorem contains the exact phase deletion

```text
h169
+ k11 miss
+ t=2 mod11
+ k43 combined miss

=>

t != 9 mod43.
```

This is a clean example of an early obstruction phase deleting a later CRT phase through a forced signed-box seed.

---

## 7. The same seed contracts the nonresidue valuation resource

Give each q43 factor occurrence weight

```text
0 if QR mod43
1 if NR mod43.
```

As at k19, the exact Type-II-miss transition graph has no positive-weight edge inside any strongly connected component.

Therefore total nonresidue valuation is bounded by the longest weighted path in the SCC condensation DAG.

The unseeded local theorem is

```text
Type-II miss at q43
->
Omega_NR(C43) <= 20.
```

With the forced factor11 seed,

```text
Type-II miss at q43
+ 11|C43
->
Omega_NR(C43) <= 14.
```

So the h169 k11 phase gives a vertical resource contraction

```text
20 -> 14.
```

The bound is an exact automaton upper bound. No claim is made here that 14 is arithmetically sharp inside the h169 ancestry corridor.

---

## 8. Arithmetic regressions show the seed does not predetermine the outcome

The selected ancestry phase realizes every q43 outcome class.

Examples:

```text
p=48,049
C43=12,023=11*1093
k11 miss
k43 combined miss.
```

```text
p=177,409
C43=44,363=11*37*109
k43 Type-II-only.
```

```text
p=583,969
C43=146,003=11*13*1021
k43 both targets hit.
```

```text
p=1,498,729
C43=374,693=11*23*1481
k43 Type-I-only.
```

So factor11 does not solve k43 by itself. It carves the local state universe down sharply and creates exact new obligations.

---

## 9. Obligation-machine form

The useful machine rule is now

```text
IF
    hard_class = 169
    AND inherited k11 miss
    AND t mod11 = 2
THEN
    11 | C43
    q43_seed_support contains {1,4,11}
    any k43 Type-II miss excludes factor residues {32,39,42} mod43
    any k43 combined miss excludes t mod43 = 9
    any k43 Type-II miss has Omega_NR(C43) <= 14.
```

This is precisely the desired architecture:

```text
early phase
-> forced rational factor
-> exact later signed support
-> support exclusions
+ CRT phase deletion
+ valuation-budget contraction.
```

---

## 10. What remains of the five-way k11 partition

The current h169 k11 children now have the following exact downstream structure:

```text
t11=8 -> factor11 at C19
           BARE deleted
           q19 NR budget 8 -> 2

t11=4 -> factor11 at C35
           S7 deleted
           k35 miss becomes J35-only

t11=3 -> factor11 at C39
           routed J39+ support theorem applies on miss

t11=2 -> factor11 at C43
           q43 closure 18,048 -> 2,317
           combined closure 7,740 -> 1,217
           t43=9 deleted
           q43 NR budget 20 -> 14

t11=0 -> factor11 at C51
           still the clean unresolved seeded destination.
```

That leaves k51 as the obvious next phase-conditioned local target.

---

## 11. Executable verifier

Run

```sh
python3 research/verify_h169_k11_t2_k43_seeded_shell.py
```

It verifies independently:

```text
the exact h169 k11 phase bridge,
q43 primitive-root and factor11 order data,
seed support {1,4,11},
unseeded and seeded full Type-II-miss closures,
combined-miss and Type-I-only counts,
the one-occurrence absorber set {32,39,42},
generic and seeded C43 phase exclusions,
the h169 t43=9 exclusion,
absence of positive-NR SCC edges,
NR valuation budgets 20 and14,
and arithmetic witnesses for all four k43 outcome classes.
```

---

## 12. Claim boundary

The theorem is exact but local.

It does not say the k11 miss forces `t=2 mod11`; four other h169 k11 phases remain. It does not say factor11 forces k43 to hit. It does not assert every abstract seeded state is realized arithmetically. It does not establish a finite Lane-I ceiling or prove Erdős–Straus.
