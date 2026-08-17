# h169 k11 t=0 -> fourteen-companion block

**Status:** exact consecutive-cofactor theorem  
**Date:** 2026-08-17  
**Verifier:** `verify_h169_k11_t0_fourteen_companion_block.py`  
**Depends on:** `H169-K11-T0-K51-JACOBI-NORMAL-FORM.md`

## Theorem

On the h169 k11 child

```text
t mod11=0,
```

write

```text
t=11u,
R=1+42u.
```

The canonical k51 normal form gives

```text
C51=55R.
```

For

```text
k_j=3+4j,
0<=j<=13,
```

the complete Lane-I companion window from k=3 through k=55 satisfies

```text
C_(3+4j)=55R+(j-12).
```

Therefore

```text
(C3,C7,C11,C15,C19,C23,C27,C31,C35,C39,C43,C47,C51,C55)
=
(55R-12,55R-11,55R-10,55R-9,55R-8,55R-7,55R-6,
 55R-5,55R-4,55R-3,55R-2,55R-1,55R,55R+1).
```

The surviving object is literally a block of fourteen consecutive integers.

---

## Proof

On this phase,

```text
p=169+840(11u)=169+9240u.
```

Hence

```text
C_(3+4j)
=(p+3+4j)/4
=43+j+2310u.
```

But

```text
55R+(j-12)
=55(1+42u)+(j-12)
=43+j+2310u.
```

So the identity is exact.

---

## Immediate gcd law

For every `j !=12`,

```text
gcd(R,C_(3+4j))
=
gcd(R,55R+j-12)
=
gcd(R,j-12).
```

This is a cleaner form of the residual support-isolation theorem.

Since

```text
R=1+42u
```

is always

```text
1 mod2,
1 mod3,
1 mod7,
```

the offsets `-12,...,-1,+1` leave only three possible support-sharing channels:

```text
C7  =55R-11 : possible shared prime11
C11 =55R-10 : possible shared prime5
C31 =55R-5  : possible shared prime5.
```

Every other companion in the block is exactly coprime to `R`.

More precisely,

```text
gcd(R,C7)=11   iff u=6 mod11,
gcd(R,C11)=5   iff u=2 mod5,
gcd(R,C31)=5   iff u=2 mod5,
```

and those gcds equal1 otherwise.

---

## Why this is the right simultaneous object

The k51 Jacobi theorem says a combined miss requires every residual prime factor of `R` to remain inside

```text
H51=ker Jacobi(./51).
```

The persistent-shield theorem says repeated factor11 can cycle forever inside that local shield.

The fourteen-companion theorem now puts that shield carrier inside one rigid arithmetic block:

```text
55R-12,
55R-11,
...
55R,
55R+1.
```

So the remaining question is no longer whether fourteen unrelated coordinates can each miss.

It is whether **one run of fourteen consecutive integers** can simultaneously satisfy all of the exact support, character, valuation, and ancestry obligations already attached to those coordinates.

That is the compression target.

---

## Research corollary

Any prime

```text
q notin {5,11}
```

dividing the k51 residual `R` divides no other member of the companion block.

Thus every large H51-supported factor of the shield reservoir is private to the central term `55R`.

A future theorem forcing

```text
Jacobi(q/51)=-1
```

for even one such private divisor `q|R` would puncture the canonical k51 combined-miss normal form.

The most promising mechanisms are therefore not direct factor sharing but cross-coordinate character laws, reciprocity, CRT ancestry, and product constraints on this consecutive block.

---

## Executable verification

Run

```sh
python3 research/verify_h169_k11_t0_fourteen_companion_block.py
```

The verifier checks the symbolic affine identity coefficient-by-coefficient, reconstructs all fourteen offsets, derives the exact gcd law, and freezes the three exceptional overlap phases.

---

## Claim boundary

This theorem does not force a divisor of `R` outside `H51` and does not prove termination.

It supplies a compact, exact simultaneous arithmetic object for the selected hardest k51 child. No finite Lane-I ceiling or Erdős-Straus proof is claimed here.
