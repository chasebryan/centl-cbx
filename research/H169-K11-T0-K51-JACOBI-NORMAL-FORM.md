# h169 k11 t=0 mod11 -> k51 Jacobi normal form

**Status:** exact phase-conditioned survivor theorem  
**Date:** 2026-08-17  
**Scope:** h169 under inherited k11 combined miss  
**Verifier:** `verify_h169_k11_t0_k51_jacobi_normal_form.py`

## 1. Statement

Write

```text
p = 169 + 840t.
```

On the exact h169 k11-miss child

```text
t = 0 mod11,
```

write `t=11u`. Then

```text
C51 = (p+51)/4
    = 55 + 210t
    = 55(1+42u).
```

Thus the phase forces **both** rational primes

```text
5 and 11
```

into `C51`.

Strip one occurrence of each and write

```text
C51 = 55 R.
```

Define the Jacobi kernel

```text
H51 = { r in U(51) : (r/3)(r/17)=+1 }.
```

Then the exact normal form is

```text
k51 combined miss
iff
every prime-factor occurrence of R lies in H51.
```

Explicitly,

```text
H51 = {
  1,4,5,11,13,14,16,19,
  20,23,25,29,41,43,44,49
} mod51.
```

This is not a bounded census statement. It is an exact finite signed-box theorem.

---

## 2. Why the seed is much stronger than factor11 alone

The h169 hard class already forces factor5 into `C51`.

The selected k11 ancestry phase forces factor11 into the same cofactor.

So the correct local seed is not

```text
[11]
```

but

```text
[5,11].
```

Their individual signed supports are

```text
factor5  -> {1,5,41}
factor11 -> {1,11,14}.
```

Together they preload

```text
{1,4,5,11,13,14,19,41,43}.
```

Every one of those residues lies in `H51`.

The seeded center is

```text
5*11 = 55 = 4 mod51,
```

which also lies in `H51`.

---

## 3. The Jacobi kernel protects both targets

`H51` is an index-two subgroup of `U(51)`.

The Type-II target is

```text
-1 = 50 mod51.
```

Its Jacobi character is

```text
(50/3)(50/17) = -1,
```

so Type II lies outside `H51`.

Now suppose every residual prime factor of `R` lies in `H51`.

Then:

```text
signed support stays inside H51,
C51 stays inside H51,
p=4C51 stays inside H51.
```

Therefore

```text
-p^-1
```

also lies in the opposite Jacobi coset because `-1` is outside `H51`.

So neither target can enter the signed support.

This proves the easy direction:

```text
all residual factors in H51
->
k51 combined miss.
```

---

## 4. The converse is exact and word-level

The difficult direction is stronger than a final-state classification.

The complete Type-II-miss automaton from seed `[5,11]` contains exactly

```text
86 states
 = 26 combined misses
 + 60 Type-I-only states.
```

Now augment each state with one bit:

```text
outside_used = has any residual factor outside H51 appeared?
```

Exhaust the complete Type-II-miss word graph.

The result is perfectly separated:

```text
outside_used = false:
    26 states
    all 26 are combined misses

outside_used = true:
    60 states
    all 60 are Type-I-only.
```

And there are

```text
0 combined misses
```

with `outside_used=true`.

Any word that hits Type II can be discarded permanently because signed support is monotone under additional factors.

Therefore no factorization that ever uses an outside-`H51` residual prime occurrence can return to a combined miss.

That proves the converse:

```text
k51 combined miss
->
every residual prime-factor occurrence lies in H51.
```

Together:

```text
k51 miss
iff
support_prime(R) subset H51.
```

---

## 5. The 86-state universe is already tiny

The local k51 seed `[5,11]` leaves only

```text
86 Type-II-miss states.
```

The combined-miss portion is just

```text
26 states.
```

Moreover, the `H51`-only closure itself has exactly those same

```text
26 states,
```

and every one of them is a combined miss.

So the normal form is not merely a useful description of some survivor family. It exactly identifies the entire combined-miss component of the seeded local automaton.

---

## 6. Immediate one-factor shell

From the `[5,11]` seed, one additional non-inert factor occurrence gives

```text
15 misses
7 Type-I-only
7 Type-II-only
2 both.
```

The 16 outside-`H51` residues are exactly

```text
{2,7,8,10,22,26,28,31,32,35,37,38,40,46,47,50}.
```

Every one of them is already non-missing after one occurrence.

The full flagged automaton is what proves that the seven Type-I-only cases cannot later “escape back” into a combined miss without hitting Type II.

This distinction matters because Type-I occupancy itself is not monotone, while Type-II occupancy is.

---

## 7. The normal form becomes a clean mod17 phase theorem

For every h169 prime,

```text
p = 1 mod3.
```

On a k51 combined miss, `C51` lies in `H51`, hence

```text
p=4C51 in H51.
```

Because `(p/3)=+1`, Jacobi positivity is equivalent here to

```text
(p/17)=+1.
```

Now

```text
p = 169 + 840t
  = 16 + 7t mod17.
```

Solving `(p/17)=+1` gives exactly

```text
t mod17 in {0,2,8,10,11,12,15,16}.
```

The phase

```text
t=5 mod17
```

would make `17|p`, so it is impossible for the h169 primes under discussion.

Thus among the 16 prime-admissible `t mod17` phases, a k51 combined miss retains exactly eight:

```text
1/2.
```

This is a clean cross-coordinate phase contraction produced by a support theorem, not by a prime census.

---

## 8. Arithmetic witnesses

The normal form is realized arithmetically.

### Combined miss

```text
p=55,609
t=66=0 mod11
C51=13,915=5*11^2*23
R=253=11*23.
```

Both residual prime residues lie in `H51`, and k51 is a combined miss.

### Both targets hit

```text
p=64,849
C51=16,225=5^2*11*59.
```

After stripping one 5 and one11,

```text
R=295=5*59,
```

and `59=8 mod51` lies outside `H51`. Both targets hit.

### Type-I-only

```text
p=231,169
C51=57,805=5*11*1051
R=1051=31 mod51,
```

with `31` outside `H51`.

### Type-II-only

```text
p=379,009
C51=94,765=5*11*1723
R=1723=40 mod51,
```

with `40` outside `H51`.

The four outcome classes are therefore all arithmetically present on the selected ancestry phase, while the exact combined-miss normal form still holds.

---

## 9. The five-way k11 phase tree is now substantially sharper

The h169 k11 obstruction had five exact children:

```text
t11 in {0,2,3,4,8}.
```

They now carry:

```text
t11=8
  -> factor11 at C19
  -> k19 BARE deleted
  -> q19 NR budget 8 -> 2

t11=4
  -> factor11 at C35
  -> S7 deleted
  -> k35 miss becomes J35-only

t11=3
  -> factor11 at C39
  -> routed J39+ support theorem

t11=2
  -> factor11 at C43
  -> exact seeded q43 shell
  -> 2,317 Type-II-miss states
  -> 1,217 combined misses
  -> t43=9 excluded
  -> NR budget 20 -> 14

t11=0
  -> factors 5 and11 at C51
  -> exact H51 Jacobi normal form
  -> only 26 combined local states
  -> (p/17)=+1
  -> eight allowed t17 phases.
```

The formerly vague “future factor schedule” has become five different structural obligations.

That is exactly the direction the contradiction machine needs.

---

## 10. Obligation-machine rule

The phase can now be encoded as

```text
IF
    hard_class = 169
    AND inherited k11 miss
    AND t mod11 = 0
    AND k51 combined miss
THEN
    C51 = 55 R
    every prime factor of R has Jacobi +1 mod51
    (p/17)=+1
    t mod17 in {0,2,8,10,11,12,15,16}.
```

The support obligation is stronger than merely requiring

```text
(R/51)=+1.
```

Every individual prime-factor occurrence must lie in the Jacobi kernel.

---

## 11. Why this is a useful “noun-sized theorem”

This result can be stated without introducing the full CBX vocabulary:

```text
For p=169 mod840 on the k11-obstruction phase t=0 mod11,
write (p+51)/4=55R.
Then the k51 signed-box obstruction survives exactly when every
prime factor of R has Jacobi symbol +1 modulo51.
```

That is a compact theorem with an independent executable verifier.

The machinery can remain underneath it rather than inside its statement.

---

## 12. Executable verifier

Run

```sh
python3 research/verify_h169_k11_t0_k51_jacobi_normal_form.py
```

It verifies:

```text
the h169/k11 phase bridge,
C51=55(1+42u),
the exact H51 subgroup,
the [5,11] seed support,
the complete 86-state Type-II-miss closure,
the exact 26/60 class split,
the 26-state H51-only sufficiency closure,
the augmented outside-H51 word automaton,
zero combined misses after any outside-H51 factor,
the one-step outside-H51 shell,
the exact t mod17 consequence,
and arithmetic witnesses for all four k51 outcome classes.
```

---

## 13. Claim boundary

The theorem resolves only the `t=0 mod11` child of an inherited h169 k11 obstruction at the k51 coordinate.

It does not eliminate the surviving `H51` prime-support family, does not say k11 miss forces this phase, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
