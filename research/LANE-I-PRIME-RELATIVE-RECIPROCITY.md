# Lane-I prime-relative reciprocity

**Status:** exact general Lane-I character theorem  
**Date:** 2026-08-17  
**Verifier:** `verify_lane_i_prime_relative_reciprocity.py`

## Theorem

Let `p` be an odd prime with

```text
p=1 mod4.
```

Let `k>0` satisfy

```text
k=3 mod4
```

and define the Lane-I cofactor

```text
C_k=(p+k)/4.
```

For every odd prime divisor `q|C_k` with

```text
gcd(q,k)=1,
```

we have the exact identity

```text
Legendre(q/p)=Jacobi(q/k).
```

When `k` itself is prime, the right side is simply the Legendre symbol

```text
(q/k).
```

---

## Proof

Because

```text
q|C_k=(p+k)/4,
```

we have

```text
p=-k mod q.
```

Since

```text
p=1 mod4,
```

quadratic reciprocity gives

```text
(q/p)=(p/q).
```

Therefore

```text
(q/p)
=(p/q)
=(-k/q)
=(-1/q)(k/q).
```

Now `k=3 mod4`, so Jacobi reciprocity gives

```text
(k/q)
=(-1)^((k-1)/2 * (q-1)/2) (q/k)
=(-1)^((q-1)/2) (q/k)
=(-1/q)(q/k).
```

Hence

```text
(-k/q)
=(-1/q)^2 (q/k)
=(q/k).
```

Thus

```text
(q/p)=(q/k).
```

The right-hand symbol is Jacobi when `k` is composite.

---

## Why this matters

Many Lane-I miss theorems are currently written locally:

```text
all prime divisors q of C_k lie in a Jacobi/Legendre +1 class modulo k.
```

The reciprocity bridge says that, whenever the theorem lies in the domain above, the same statement can be read globally as

```text
all those prime divisors are quadratic residues modulo the original prime p.
```

So a local shift character is not a separate phenomenon.

It is the restriction of a prime-relative character carried by the same factor `q`.

That gives the simultaneous obligation machine a common language across different coordinates:

```text
q is QR/NR modulo p.
```

Instead of comparing unrelated local residue alphabets at k=7,11,19,43,51,..., we can translate compatible character laws back to one global prime.

---

## Prime-shift specialization

If `k` is an odd prime with `k=3 mod4`, then

```text
(q/p)=(q/k).
```

Therefore a pure-QR local miss condition at shift k is exactly a pure-QR support condition modulo p.

Examples in the current h169 research tree include prime shifts where a landed branch requires all relevant prime factors to be quadratic residues modulo the shift modulus.

The bridge lets those branches be compared in one p-relative support grammar.

---

## Composite-shift specialization

The theorem is not restricted to prime k.

For composite

```text
k=3 mod4,
```

the correct right-hand object is

```text
Jacobi(q/k).
```

The newly landed k51 reciprocal shield is exactly the `k=51` instance.

On its selected h169 phase, the canonical combined-miss normal form says every prime divisor of `C51` has Jacobi +1 modulo51. The reciprocity theorem turns that immediately into

```text
(q/p)=+1
```

for every prime divisor `q|C51`.

Thus the k51 theorem is not an isolated composite curiosity. It is one member of a general Lane-I prime-relative character law.

---

## The new contradiction target

Suppose a local miss normal form at coordinate k requires

```text
Jacobi(q/k)=+1
```

for every relevant `q|C_k`.

Then the bridge gives

```text
(q/p)=+1.
```

To kill that local branch it is enough to force even one divisor

```text
q|C_k
```

with

```text
(q/p)=-1.
```

This is especially useful for the simultaneous consecutive-cofactor program because multiple local support laws can now be translated into one global character system against p.

The research question becomes

```text
Can all consecutive cofactors simultaneously maintain the p-relative
QR/NR obligations forced by their exact local miss normal forms?
```

That is a much smaller conceptual object than a collection of unrelated residue automata.

---

## Executable verification

Run

```sh
python3 research/verify_lane_i_prime_relative_reciprocity.py
```

The verifier checks:

```text
the exact reciprocity sign cancellation for q mod4=1 and3,
the Jacobi implementation,
the identity across more than 20,000 distinct prime-divisor instances
for p<10,000 and Lane-I shifts k<100,
both QR and NR signs,
composite k=51 cases,
and more than 4,000 h169 prime-factor instances across selected shifts.
```

The finite regressions guard the executable theorem. The proof is the exact reciprocity calculation above.

---

## Claim boundary

The theorem assumes

```text
p prime,
p=1 mod4,
k=3 mod4,
q odd prime,
q|C_k,
gcd(q,k)=1.
```

It deliberately excludes `q|k`, where the Jacobi symbol on the right is zero and the stated ±1 character identity is not the correct formulation.

It does not assert a Lane-I stage is a miss, does not force either character sign, and does not prove Erdős-Straus by itself.
