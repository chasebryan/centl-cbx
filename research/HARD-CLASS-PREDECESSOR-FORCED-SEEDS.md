# Hard-class predecessor forced seeds

**Status:** exact cross-coordinate congruence/state theorem  
**Date:** 2026-08-17  
**Scope:** q23 predecessor corridor, especially k11 and k19  
**Claim boundary:** local state-universe reduction only; not an Erdős–Straus proof

## 1. Hard classes already inject factors into later coordinates

On the q23 Type-I-only parameterization

```text
T=(p+23)/24,
```

the six Mordell-hard classes give

```text
p mod840   T mod35
------------------
1              1
121            6
169            8
289           13
361           16
529           23.
```

Because the predecessor forms are affine in `T`, these six residues force literal factors `5` and `7` before any expensive factorization search.

The exact pattern is

```text
T mod35=1   : 5 | (6T-1)
T mod35=6   : 5*7 | (6T-1)
T mod35=8   : 5 | (2T-1)
T mod35=13  : 5 | (2T-1), 7 | (6T-1)
T mod35=16  : 7 | (6T-5), 5 | (6T-1)
T mod35=23  : 7 | (6T-5), 5 | (2T-1).
```

This is exact congruence structure, not finite census behavior.

---

## 2. k11 acquires a hard-class seed

Recall

```text
C11 = 3(2T-1).
```

The factor `3` is forced for every Mordell-hard prime.

For hard classes

```text
p mod840 in {169,289,529},
```

we have

```text
T mod5=3,
```

and therefore

```text
5 | (2T-1).
```

So their exact q11 residue automaton is seeded by

```text
[3,5]
```

rather than merely `[3]`.

The exact state counts are

```text
seed [3]    : 11 Type-II-miss states = 9 combined + 2 Type-I-only
seed [3,5]  :  5 Type-II-miss states = 5 combined + 0 Type-I-only.
```

Therefore:

```text
p mod840 in {169,289,529}
and k11 Type-II misses
=> k11 Type I also misses.
```

The two thin q11 Type-I-only rescue packets cannot occur in those three hard classes.

This also has a direct normal-form interpretation. In the thin q11 branch every QR prime other than the forced `3` must be `1 mod11`. The forced literal factor `5` is QR modulo 11 but is not `1 mod11`, so it excludes the thin branch entirely. A remaining Type-II miss must be pure QR, and pure QR is already known to miss Type I as well.

---

## 3. k19 hard-class seeds

At k19,

```text
C19=6T-1.
```

The hard classes force the following exact seed residues modulo 19:

```text
p mod840    forced factors in C19    q19 seed
---------------------------------------------
1           5                         [5]
121         5,7                       [5,7]
169         none                      []
289         7                         [7]
361         5                         [5]
529         none                      [].
```

Feeding those forced occurrences into the exact Type-II-miss automaton gives:

```text
seed []     : 254 states = 136 combined + 118 Type-I-only
seed [5]    :  64 states =  44 combined +  20 Type-I-only
seed [7]    :  27 states =  18 combined +   9 Type-I-only
seed [5,7]  :   9 states =   9 combined +   0 Type-I-only.
```

Thus the abstract local k19 obstruction universe is already sharply hard-class dependent.

---

## 4. Exact h121 consequence

The strongest case is

```text
p = 121 mod840.
```

Then

```text
5*7 | C19.
```

The seed `[5,7]` leaves only nine Type-II-miss states, and **none** is Type-I-only.

Therefore the exact implication is

```text
p=121 mod840
and k19 Type II misses
=> k19 combined miss.
```

So for hard class121 the second target contributes no rescue after a Type-II miss at k19.

This is a universal fixed-shift statement for that hard class, not a finite observation.

---

## 5. Why the seeded closures are useful

The unseeded q19 universe contains

```text
254 Type-II-miss states.
```

But a proof search conditioned on hard class should not carry all 254 states blindly.

The correct class-sensitive local budgets are

```text
hard 1 or 361   : 64
hard 121        : 9
hard 169 or 529 : 254
hard 289        : 27.
```

This gives CBX a theorem-safe way to specialize k19 state analysis before considering q23 rescue class, earlier BREC ancestry, or finite realization.

The reduction is especially important after the 100M adversarial extension falsified the apparent 30M hard-class169 concentration. Instead of treating hard class as a finite pattern, we use the exact factors it forces into the arithmetic.

---

## 6. q23 rho=14 also injects an inert k11 factor

The q23 Type-I-only normal form gives

```text
rho=5  => T=2 mod23
rho=14 => T=12 mod23.
```

For `rho=14`,

```text
2T-1 = 23 = 0 mod23.
```

Hence

```text
23 | (2T-1).
```

But

```text
23 = 1 mod11,
```

so this forced factor is exactly inert in the k11 signed-box support.

This is still useful computationally: the factor may be stripped from the q11 support calculation with no state change, while remaining part of the exact integer factorization record.

---

## 7. Executable verifier

Run

```sh
python3 research/verify_hard_class_predecessor_forced_seeds.py
```

It verifies:

```text
the six hard T mod35 classes,
all forced 5/7 divisibilities,
q11 seed [3] versus [3,5] closures,
all four distinct q19 seeded closures,
the exact state counts and Type-I-only splits,
and the rho14 forced/inert factor23 identity.
```

The automata are exhaustive local finite-state calculations. No finite prime census is used to prove the seed reductions.

---

## 8. Claim boundary

The theorem reduces abstract local state universes using factors forced by exact congruence classes.

It does not assert that every seeded state is realized by an Erdős–Straus corridor prime, does not make finite non-realization universal, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
