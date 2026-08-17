# h169 k11 future factor-11 partition

**Status:** exact ancestry/congruence theorem  
**Date:** 2026-08-17  
**Verifier:** `verify_h169_k11_future_factor_partition.py`

## 1. One early miss schedules one later factor

Write the h169 hard lane as

```text
p = 169 + 840t
T = (p+23)/24 = 8 + 35t.
```

The exact h169 k11 theorem has already removed the thin branch:

```text
k11 combined miss
iff
C11 has pure quadratic-residue prime support modulo11.
```

Since

```text
C11 = 3(2T-1)
```

and 3 is itself QR modulo11, a k11 miss forces

```text
2T-1 in QR11={1,3,4,5,9}.
```

Therefore

```text
T mod11 in {1,2,3,5,8}.
```

Using `T=8+35t`, this is equivalent to

```text
t mod11 in {0,2,3,4,8}.
```

So the h169 k11 obstruction has exactly five possible phase children modulo11.

---

## 2. The post-k23 ladder converts phase into a literal factor

For

```text
k = 23+4j,
```

the companion ladder is

```text
C_k = 6T+j.
```

Factor11 appears when

```text
6T+j = 0 mod11.
```

The five h169 k11-miss phases give the exact partition

```text
t mod11   T mod11   p mod11   first j   shift
------------------------------------------------
0            8          4         7       k51
2            1          1         5       k43
3            3          5         4       k39
4            5          9         3       k35
8            2          3        10       k63.
```

Hence

```text
h169 + k11 miss
=>
11 divides one deterministic post-k23 companion
among C35,C39,C43,C51,C63,
with the location determined by t mod11.
```

The latest appointment is k63.

---

## 3. This is ancestry, not a census

The implication follows only from

```text
the exact k11 support theorem
+
the affine coordinate T=8+35t
+
C_(23+4j)=6T+j.
```

No prime bound, search cutoff, first-hit histogram, or probabilistic assumption occurs.

The theorem does **not** say that phase alone implies k11 miss. It says that any actual h169 k11 miss must lie on one of the five rows.

---

## 4. The phase rows have different later meanings

The factor11 appointment becomes useful only when intersected with the exact grammar at its destination.

### t=3 mod11 -> k39

Here

```text
p=5 mod11
11|C39.
```

This is exactly the routed branch of the landed k39 theorem. If k39 also misses, every prime factor of C39 lies in the Jacobi-plus subgroup modulo39.

Thus this phase already carries

```text
k11 ancestry
-> forced factor11 at k39
-> exact J39+ support obligation on a k39 survivor.
```

### t=4 mod11 -> k35

Here

```text
p=9 mod11
11|C35.
```

Since

```text
C35=3F,
```

literal prime11 divides F.

But

```text
11=4 mod7,
```

while the exact S7 branch permits only one `3 mod7` factor occurrence and otherwise only `1 mod7` factors.

Therefore S7 is impossible.

The complete k35 theorem contracts to

```text
k35 miss iff J35(F).
```

So this calendar row deletes an entire later survivor branch.

---

## 5. The remaining three appointments are now sharply defined targets

The other h169 k11 phases force

```text
t=0 mod11 -> 11|C51
t=2 mod11 -> 11|C43
t=8 mod11 -> 11|C63.
```

These should not be treated as generic later shifts anymore.

For each one, the next question is:

```text
what does the exact destination signed-box grammar do
when literal factor11 is preloaded into the companion?
```

The desired outcome is one of

```text
automatic hit,
branch deletion,
smaller exact miss automaton,
new character/support obligation,
or valuation-budget contraction.
```

This converts the broad later-shift search into three exact seeded-state problems.

---

## 6. Relation to the obligation machine

The h169 survivor state should now remember the disjunctive ancestry obligation

```text
t mod11 in {0,2,3,4,8}
```

with a deterministic destination map

```text
0 -> k51
2 -> k43
3 -> k39
4 -> k35
8 -> k63.
```

That is stronger than retaining only the fact

```text
(11/p)=+1.
```

The phase tells the machine **where the character source must physically re-enter the consecutive-cofactor ladder as the rational prime11**.

This is exactly the kind of cross-coordinate obligation that BREC should preserve.

---

## 7. Executable verifier

Run

```sh
python3 research/verify_h169_k11_future_factor_partition.py
```

It independently verifies

```text
the QR11-derived T phase set,
the equivalent h169 t phase set,
the p mod11 values,
the first positive post-k23 ladder position,
the factor11 divisibility using p+k mod44,
the five destination shifts,
and the k35 factor11/S7 incompatibility interface.
```

---

## 8. Claim boundary

This theorem does not prove any later shift hits merely because factor11 is present. It does not prove that all five phase rows are realized by prime survivors. It does not establish a finite Lane-I ceiling or prove Erdős–Straus.

Its role is exact and narrower: an h169 k11 obstruction now carries a five-way future factor-placement schedule, and two of those placements already connect to stronger landed survivor grammars.
