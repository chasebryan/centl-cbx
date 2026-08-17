# h169 k11 t=0 -> k51 reciprocal shield

**Status:** exact quadratic-reciprocity normal form  
**Date:** 2026-08-17  
**Verifier:** `verify_h169_k11_t0_k51_reciprocal_shield.py`  
**Depends on:** `H169-K11-T0-K51-JACOBI-NORMAL-FORM.md`

## The local shield has a global prime interpretation

On the selected h169 k11 phase

```text
t mod11=0,
```

write

```text
t=11u,
R=1+42u,
C51=55R.
```

Since

```text
p=169+9240u,
```

we also have the exact identity

```text
p=220R-51.
```

The canonical k51 theorem says

```text
k51 combined miss
iff
every residual prime factor q|R lies in H51,
```

where

```text
H51=ker Jacobi(./51).
```

Quadratic reciprocity turns this local support subgroup into a statement relative to the global prime p.

---

## Reciprocity identity

For every odd prime

```text
q notin {3,17},
```

we have

```text
(-51/q)
=
(-1/q)(3/q)(17/q).
```

Now

```text
(3/q)=(q/3)(-1)^((q-1)/2)
```

while

```text
(17/q)=(q/17)
```

because `17=1 mod4`.

The sign in `(3/q)` cancels `(−1/q)`, giving the exact identity

```text
(-51/q)
=
(q/3)(q/17)
=
Jacobi(q/51).
```

Therefore

```text
q in H51
iff
(-51/q)=+1.
```

So `H51` is exactly the set of residue classes for which `-51` is a quadratic residue.

---

## Residual factors see p as a square

If

```text
q|R,
```

then from

```text
p=220R-51
```

we get

```text
p=-51 mod q.
```

Hence

```text
(p/q)
=
(-51/q)
=
Jacobi(q/51).
```

Thus for every residual prime divisor `q|R`,

```text
q in H51
iff
(p/q)=+1.
```

Every h169 prime satisfies

```text
p=1 mod4.
```

So quadratic reciprocity has no sign when p and q are exchanged:

```text
(q/p)=(p/q).
```

Therefore the exact bridge is

```text
q in H51
iff
(p/q)=+1
iff
(q/p)=+1.
```

The composite-modulus shield is a prime-relative quadratic-residue shield.

---

## The forced factors are also quadratic residues modulo p

On this phase,

```text
p=4 mod5
p=4 mod11
p=1 mod4.
```

Therefore

```text
(5/p)=+1
(11/p)=+1.
```

Since

```text
C51=5*11*R,
```

the residual equivalence extends to the entire factorization of C51.

---

# Reciprocal Shield Theorem

For an h169 prime `p` on the inherited k11 phase `t=0 mod11`,

```text
k51 combined miss
iff
every prime divisor q of C51 satisfies
(q/p)=+1.
```

Equivalently:

```text
k51 combined miss
iff
C51 has no prime divisor that is a quadratic nonresidue modulo p.
```

This is an exact reformulation of the canonical k51 Jacobi normal form.

---

## Why this matters

The k51 obstruction is no longer trapped inside an unfamiliar composite signed-box language.

It can now be stated against the original Erdős–Straus prime:

```text
every prime divisor of C51 must be a square class modulo p.
```

That opens a different attack surface.

The selected branch can be killed by proving that the simultaneous companion obligations force even one prime divisor

```text
q|C51
```

with

```text
(q/p)=-1.
```

Because the residual-support isolation theorem says every large prime divisor of `R` is private to k51 within the early companion block, such a contradiction will probably not come from direct support sharing. It must come from reciprocity, a product-character law, an affine companion identity, or ancestry information.

The target is now extremely compact:

```text
FORCE ONE NR MOD p INTO C51.
```

The canonical k51 theorem then does the rest.

---

## Relation to the fourteen-companion block

On the same phase,

```text
(C3,C7,...,C55)
=
(55R-12,55R-11,...,55R,55R+1).
```

The central term `55R` therefore has two simultaneous descriptions:

```text
local composite description:
    all residual factors lie in H51

global prime description:
    all prime factors are QR modulo p.
```

The surrounding thirteen consecutive integers carry their own exact miss obligations.

The research problem is now to make those obligations force a prime-relative nonresidue into the center.

---

## Executable verification

Run

```sh
python3 research/verify_h169_k11_t0_k51_reciprocal_shield.py
```

The verifier checks the canonical k51 normal form, the reciprocity character identity over a large regression set of rational primes, the fixed factors5 and11, and exact h169 regression examples satisfying the H51 support condition.

---

## Claim boundary

The theorem does not prove that `C51` must contain a quadratic nonresidue modulo p.

It gives an exact equivalent target for killing the selected k51 combined-miss branch.

No finite Lane-I ceiling or Erdős–Straus proof is claimed here.
