# Four-Consecutive Prime-QR Block

**Status:** exact simultaneous Lane-I theorem  
**Date:** 2026-08-17  
**Verifier:** `verify_four_consecutive_prime_qr_block.py`  
**Depends on:** the exact k3, k7, class-conditioned k11, and k15 obstruction normal forms plus `LANE-I-PRIME-RELATIVE-RECIPROCITY.md`

## Theorem

Let `p` be prime with

```text
p mod840 in {169,289,529}.
```

Put

```text
X=(p+3)/4.
```

Then

```text
C3  = X
C7  = X+1
C11 = X+2
C15 = X+3.
```

The first four Lane-I coordinates are simultaneously obstructive,

```text
sigma3=sigma7=sigma11=sigma15=-,
```

if and only if every prime divisor of

```text
X(X+1)(X+2)(X+3)
```

is a quadratic residue modulo `p`.

Equivalently:

```text
first four BREC misses
iff
four consecutive integers have exclusively p-QR prime support.
```

---

## Why the four local normal forms unify

The landed exact obstruction laws are:

```text
k=3:
miss iff every q|C3 is 1 mod3

k=7:
miss iff every q|C7 is QR mod7

k=11, hard classes 169/289/529:
miss iff every q|C11 is QR mod11

k=15:
miss iff every q|C15 lies in H15={1,2,4,8}.
```

Each support set is exactly the Jacobi +1 kernel for its shift:

```text
H3  = {1}
H7  = {1,2,4}
H11 = {1,3,4,5,9}
H15 = {1,2,4,8}.
```

The Lane-I Prime-Relative Reciprocity theorem says that for every prime factor `q|C_k`,

```text
Jacobi(q/k)=Legendre(q/p).
```

Therefore every one of the four local obstruction conditions translates to the same global statement:

```text
all prime divisors of C_k are QR modulo p.
```

The four local languages collapse into one.

---

## The consecutive structure is exact

Because the Lane-I shifts advance by four,

```text
C_(k+4)
=(p+k+4)/4
=C_k+1.
```

Hence the first four cofactors are not merely related.

They are consecutive:

```text
X,
X+1,
X+2,
X+3.
```

So the object carried by a `----` BREC prefix in these hard classes is an exact four-integer support block.

---

## Simultaneous support interpretation

A survivor through k15 is therefore not four independent misses.

It is one arithmetic object satisfying

```text
for every prime q dividing X(X+1)(X+2)(X+3):
(q/p)=+1.
```

Because consecutive integers are pairwise constrained by

```text
gcd(X+i,X+j) | |i-j|,
```

their large prime supports are nearly disjoint while all of them are required to lie in the same index-two quadratic-residue half of `U(p)`.

This is the first clean p-relative simultaneous support theorem for a consecutive Lane-I block.

---

## What it changes in the search

The natural research question is no longer

```text
Can k3 miss?
Can k7 miss?
Can k11 miss?
Can k15 miss?
```

Those questions are already classified.

The better question is

```text
How long can a consecutive cofactor block maintain exclusively p-QR prime support
while the later exact Lane-I obligations are added?
```

At k19 and beyond, the obstruction grammar develops finite NR budgets, seeded shells, subgroup modes, and valuation escape. The p-relative reciprocity bridge gives a common character coordinate in which those later resources can be compared to the four-term QR block.

This is the desired transition from coordinate-by-coordinate search to simultaneous satisfiability.

---

## A compact blackboard form

```text
p mod840 in {169,289,529}
X=(p+3)/4

sigma3=sigma7=sigma11=sigma15=-

iff

q|X(X+1)(X+2)(X+3)
=>
(q/p)=+1.
```

That statement contains no CBX implementation vocabulary. It is an ordinary exact number-theory theorem about four consecutive integers and one prime.

---

## Executable verification

Run

```sh
python3 research/verify_four_consecutive_prime_qr_block.py
```

The verifier checks:

```text
the four landed local +1 support sets,
that each is exactly the Jacobi +1 set,
the generic Lane-I reciprocity bridge,
the symbolic consecutive-cofactor identity,
coordinate-by-coordinate local/global character equivalence,
and a finite prime regression across all three hard classes through p<=5,000,000.
```

The finite regression guards the executable synthesis. The theorem follows from the exact landed normal forms plus quadratic reciprocity.

---

## Claim boundary

The theorem does not say four consecutive p-QR-supported integers are impossible. They are arithmetically realizable and occur among finite survivors.

It identifies the exact object that must be extended, punctured, or contradicted by later Lane-I obligations.

No finite Lane-I ceiling or Erdős-Straus proof is claimed here.
