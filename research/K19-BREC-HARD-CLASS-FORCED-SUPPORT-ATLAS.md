# k=19 BREC hard-class forced-support atlas

**Status:** exact class-conditioned input atlas  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`

## 1. Purpose

The first four BREC obstruction coordinates admit compact normal forms that hold across all six Mordell-hard classes.

At `k=19`, the forced-factor geometry splits by hard class. The correct next step is therefore not to assume one uniform seed structure, but to record exactly what each hard class contributes before any additional factor of

```text
C_19=(p+19)/4
```

is examined.

This atlas isolates that class-conditioned seed.

---

## 2. Forced factors 5 and 7

For a hard residue `h mod840`, factor `5` is forced into `C_19` when

```text
h+19 = 0 mod5,
```

and factor `7` is forced when

```text
h+19 = 0 mod7.
```

The six classes give:

```text
hard class    forced factors in C_19
------------------------------------
1             5
121           5,7
169           none
289           7
361           5
529           none
```

Both `5` and `7` are quadratic residues modulo 19.

---

## 3. Guaranteed signed support modulo 19

At valuation one, factor `5` contributes

```text
{5^(-1),1,5} mod19.
```

Factor `7` contributes

```text
{7^(-1),1,7} mod19.
```

Their class-conditioned product support gives:

```text
hard class    guaranteed QR support source
-------------------------------------------
1             factor 5 only
121           factors 5 and 7
169           identity only
289           factor 7 only
361           factor 5 only
529           identity only
```

Only the h121 pair fills the complete quadratic-residue subgroup modulo 19 at the forced-seed level.

That is why h121 admits the immediate exact theorem

```text
sigma_19=-
iff
all prime divisors of C_19 are QR mod19.
```

The other five classes do not receive that theorem merely from their forced seed.

---

## 4. q23 rescue coordinates

On the q23 Type-I-only rescue branch,

```text
M=HD,
p=24M-23,
C_19=6M-1.
```

The hard classes correspond to

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

The factor atlas is visible directly from `6M-1`:

```text
M=1 mod35   -> 5 divides 6M-1
M=6 mod35   -> 35 divides 6M-1
M=8 mod35   -> neither 5 nor 7 is forced
M=13 mod35  -> 7 divides 6M-1
M=16 mod35  -> 5 divides 6M-1
M=23 mod35  -> neither 5 nor 7 is forced.
```

Thus the q23 rescue frontier naturally splits into six arithmetic lanes before the k19 signed-box search begins.

---

## 5. Why h169 is the immediate hard lane

The explicit q23 Type-I-only witnesses with full anchored obstruction history

```text
-----
```

at

```text
p = 18,766,609
p = 27,211,969
```

both lie in

```text
p = 169 mod840.
```

The h169 row has no forced `5` or `7` seed at k19. It therefore lacks the immediate QR-subgroup saturation available in h121.

This makes h169 the natural first class for the next exact k19 normal-form search.

---

## 6. Executable verification

The atlas is frozen in

```text
research/verify_k19_brec_hard_class_support_atlas.py
```

and the complete h121 consequence is separately verified by

```text
research/verify_h121_k19_brec_obstruction_normal_form.py
```

Run:

```sh
python3 research/verify_k19_brec_hard_class_support_atlas.py
python3 research/verify_h121_k19_brec_obstruction_normal_form.py
```

The first verifier checks the six forced-factor rows and the exact guaranteed support. The second proves the full h121 k19 obstruction theorem.

---

## 7. Next target

For h169 q23 Type-I-only rescues,

```text
M = 8 mod35,
C_19 = 6M-1,
```

with no forced factor `5` or `7`.

The correct next task is to use the exact forward branch search to classify the factor-character states of `6M-1` after the already-proved k3, k7, k11, and k15 obstruction conditions have been imposed.

Any finite pattern discovered there must be attacked immediately with larger branch generation before being promoted to a theorem candidate.

---

## 8. Claim boundary

This atlas proves only the hard-class forced-factor/support input at k19.

It does not classify k19 for h1, h169, h289, h361, or h529. Only h121 receives the complete QR/no-QR obstruction criterion from the forced support alone.
