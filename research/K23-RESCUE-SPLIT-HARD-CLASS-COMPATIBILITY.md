# k=23 rescue split / hard-class compatibility

**Status:** exact local congruence theorem  
**Date:** 2026-08-17  
**Depends on:** `K23-TYPEI-ONLY-INTEGER-NORMAL-FORM.md`  
**Claim boundary:** local CRT/Dirichlet compatibility only; not an Erdős–Straus proof

## 1. Question

Inside the exact conditional `k=23` Type-I-only normal form,

```text
C_23 = 6*m*R,
p    = 24*m*R - 23,
```

where every prime divisor of `m` is `1 mod 23` and `R` has exactly two prime valuations in one residue class

```text
rho in {5,14} mod 23.
```

There are two multiplicity splits:

```text
square:              R = r^2
distinct-semiprime:  R = r*s, r != s,
```

with every rescue prime congruent to the same `rho mod 23`.

A natural first question is whether the six Mordell-hard residue classes themselves eliminate either split.

They do not.

---

## 2. Theorem

Let

```text
H = {1,121,169,289,361,529} mod 840
```

be the Mordell-hard prime residue classes. For every

```text
rho in {5,14},
h in H,
split in {square, distinct-semiprime},
```

there are infinitely many local integer normal-form choices `(m,R)` satisfying

```text
C = 6*m*R,
p_candidate = 24*m*R - 23,
p_candidate = h mod 840,
```

with the selected q23 rescue class `rho` and selected multiplicity split.

The word **candidate** matters. The theorem does not assert that `p_candidate` is prime.

---

## 3. Modulus 805 separates the two local obligations

The hard-class normal form uses

```text
T = m*R = (p+23)/24
```

and the six exact correspondences

```text
p mod 840    T mod 35
---------------------
1               1
121             6
169             8
289            13
361            16
529             23.
```

The q23 factor conditions and the mod35 hard-class condition are coprime, so work modulo

```text
23*35 = 805.
```

For each rescue class choose rescue primes with

```text
r = rho mod 23,
r = 1   mod 35.
```

CRT gives the fixed classes

```text
rho=5   : r = 281 mod 805
rho=14  : r = 106 mod 805.
```

Both classes are coprime to 805, so Dirichlet supplies infinitely many primes in each progression.

Therefore both

```text
r^2
```

and

```text
r*s  with r != s
```

may be formed using rescue primes from one of these progressions, and in either case

```text
R = 1 mod 35.
```

---

## 4. The multiplier carries the hard class

For each required `T mod 35 = t`, choose a multiplier prime `m` satisfying

```text
m = 1 mod 23,
m = t mod 35.
```

CRT gives

```text
T mod35    m mod805
-------------------
1              1
6            461
8            323
13           783
16           576
23            93.
```

Every displayed class is coprime to 805. Dirichlet therefore supplies infinitely many primes in each progression.

Since `R=1 mod35`,

```text
T=mR=t mod35.
```

Consequently

```text
p_candidate=24T-23
```

falls in the corresponding Mordell-hard class modulo 840.

This construction works independently for both rescue classes and both multiplicity splits.

---

## 5. Exact consequence

There are

```text
2 rescue classes * 2 multiplicity splits * 6 hard classes = 24
```

local combinations.

Every one of the 24 combinations is arithmetically realizable at the CRT/factor-normal-form level.

Therefore neither of the following can be true on congruence grounds alone:

```text
"the square rescue split is excluded by Mordell-hard classes"
```

or

```text
"the distinct-semiprime rescue split is excluded by Mordell-hard classes".
```

Any genuine elimination must use more structure than `p mod 840` plus the local q23 residue normal form.

That pushes the proof search back where it belongs: into the five predecessor constraints

```text
6T-5,
6T-4,
6T-3,
6T-2,
6T-1
```

and their exact signed-box/factor grammars.

---

## 6. Why this is useful

This is a small negative theorem, but it closes a tempting dead end.

The normal form naturally invites a square-versus-semiprime split. It would be easy to spend substantial effort hoping one branch disappears after imposing the six hard residue classes. The CRT computation proves that this cannot happen.

Both branches survive every hard class before earlier-shift ancestry is imposed.

So the next useful discriminator must come from at least one of:

```text
k=3 obstruction on 6T-5
k=7 obstruction on 6T-4
k=11 obstruction on 6T-3
k=15 obstruction on 6T-2
k=19 obstruction on 6T-1
```

or a cross-shift relation coupling several of them.

---

## 7. Executable verification

Run

```sh
python3 research/verify_k23_rescue_split_hard_classes.py
```

The verifier:

1. reconstructs all CRT classes modulo 805;
2. checks that every progression is a unit class, the hypothesis needed for Dirichlet;
3. finds finite prime representatives with deterministic exact primality checks;
4. constructs both multiplicity splits for both q23 rescue classes;
5. checks all six hard classes;
6. verifies all 24 combinations and their local Type-I target residues.

The finite representatives are regression witnesses. The infinitude statement itself is the direct application of Dirichlet to the displayed coprime residue classes.

---

## 8. Claim boundary

This theorem does not say that the affine expression

```text
24*m*R - 23
```

is prime infinitely often. It does not say that any constructed candidate survives `k=3,7,11,15,19`. It does not grant CBX pruning authority.

It proves only that **Mordell-hard congruence classes do not eliminate either exact k23 Type-I-only multiplicity split.** Erdős–Straus remains open.
