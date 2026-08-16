# h169 k15 Route-B source renewal

**Status:** exact ancestry-to-source coupling theorem  
**Date:** 2026-08-16  
**Verifier:** `verify_k15_route_b_source_renewal.py`  
**Depends on:** `K195-K15-SURVIVOR-NORMAL-FORM.md`, Route-B k19 ancestry `C19=1081R`, odd-support separation, and `COMPANION-SOURCE-CHARACTER-CONSERVATION.md`.  
**Claim boundary:** exact necessary consequences of simultaneous h169 k15 survival and realized Route-B ancestry. It does not assert that such a joint state is globally realizable, does not prove termination, and does not prove Erdős–Straus.

## 1. Mandatory factor 2 collapses k15 to one survivor state

For h169

```text
C15 = (p+15)/4 = 46+210t = 2(23+105t).
```

So every C15 has a mandatory prime factor2.

The general k15 closure has two safe sectors:

```text
H_J = {1,2,4,8}
H_3 = {1,4,7,13}.
```

But

```text
2 notin H_3.
```

Therefore the `ONE3` sector is impossible for h169.

Rebuilding the exact residue closure from the mandatory factor2 seed gives

```text
19 states total
1 miss state at final center1.
```

That unique miss mask is

```text
H_J = {1,2,4,8}.
```

Hence the h169-specific theorem sharpens to

```text
k15 misses
iff
every rational prime factor q|C15 satisfies Jacobi(q/15)=+1.
```

There is no second h169 k15 mode.

## 2. Route B puts two negative aggregate characters into C15

On realized Route B,

```text
C19 = 1081 R = 23*47*R.
```

Since

```text
C19 = C15+1,
```

we have

```text
C15 = -1 mod23
C15 = -1 mod47.
```

Both primes are `3 mod4`, so

```text
(-1/23) = -1
(-1/47) = -1.
```

Thus

```text
(C15/23) = -1
(C15/47) = -1.
```

These are exact aggregate character debts carried by the k15 reservoir.

## 3. The mandatory factor2 cannot pay either debt

Quadratic reciprocity for 2 gives

```text
(2/23)=+1
(2/47)=+1,
```

because both 23 and47 are7 modulo8.

Therefore the negative product character at23 and47 must be supplied by **odd** prime-factor occurrences of C15.

There exists at least one odd prime witness `a|C15` with

```text
(a/23)=-1,
```

and at least one odd prime witness `b|C15` with

```text
(b/47)=-1.
```

The same rational prime is allowed to serve both obligations; the theorem does not claim `a != b`.

More precisely, the total multiplicity of 23-negative odd factor occurrences is odd, and independently the total multiplicity of 47-negative odd factor occurrences is odd.

## 4. Every odd k15 factor is already a positive target-prime source

A k15 miss forces every prime factor of C15 into the Jacobi-positive kernel H_J. Therefore every odd prime factor q of C15 satisfies

```text
(q/15)=+1.
```

Since q divides the origin companion C15 and origin shift15 is `3 mod4`, the landed companion-source orientation theorem gives

```text
(q/p) = (q/15) = +1.
```

Hence the negative-character witnesses above are simultaneously genuine positive target-prime character sources:

```text
WIT_15_23:
    exists odd prime a|C15
    (a/p)=+1
    (a/23)=-1

WIT_15_47:
    exists odd prime b|C15
    (b/p)=+1
    (b/47)=-1.
```

These sources are not speculative scheduler labels. Their target-prime orientation follows exactly from the companion-source theorem.

## 5. Freshness relative to the Route-B D-selector reservoirs

The early and later companions differ by small integers:

```text
C19-C15 = 1
C23-C15 = 2
C27-C15 = 3
C31-C15 = 4
C47-C15 = 8.
```

Any odd prime shared by C15 and one of these later companions would have to divide the corresponding difference.

But `gcd(C15,15)=1`, so no odd factor of C15 is3 or5. Therefore no odd prime factor of C15 can divide any of

```text
C19,C23,C27,C31,C47.
```

Thus the k15 witness sources are fresh relative to the dynamic Route-B reservoirs

```text
R,B,E,D,J.
```

In particular they cannot be the materialized q_D or q_J witnesses already living in D and J.

## 6. Exact transition semantics

A Route-B state that survives k15 does not enter the k19+ machine empty-handed. It carries at least the existential source obligations

```text
SRC15_NEG23
SRC15_NEG47
```

with

```text
source origin = 15
positive target character = +1
transverse negative character = -1 at23 or47
odd support disjoint from R,B,E,D,J.
```

The two obligations may collapse to one prime if a single factor is negative at both23 and47. Otherwise they represent two distinct new positive sources.

So the exact ancestry transition is

```text
k15 miss
  -> unique J15 support state
  -> negative character debt at23 and47
  -> one or two fresh positive source witnesses
  -> enter Route-B k19+ grammar with renewed source state.
```

## 7. Why this is stronger than a survivor label

The previous k15 normal form said only which factorizations can avoid the signed-box targets.

The Route-B coupling adds a constructive consequence:

> **survival itself forces new proof resources.**

This is one of the clearest examples in the current machine of an obstruction resolving into construction.

It does not yet prove a well-founded progress measure because the new source values are unbounded and may enter character SCCs. But it means k15 survival is not semantically inert.

## 8. Bryan Entanglement Cross boundary

This transition is naturally annotated

```text
down (-/+): k15 survivor set collapses to one Jacobi-positive state
left (-):   Route-B adjacency imposes two negative aggregate characters
right (+): those debts force fresh positive target-prime sources.
```

The arrows are observational/scheduling metadata. The mandatory factor2, residue identities, character products, and reciprocity theorem are the proof-bearing objects.

## 9. Next target

The correct next question is whether the fresh origin15 sources interact obligatorily with the already-landed Route-B D-selector sources at k19/k23/k27/k31/k47.

Two useful directions are:

1. derive exact character intersections for a source `q|C15` with `(q/15)=+1` and `(q/23)=-1` or `(q/47)=-1`;
2. determine whether one of the forced origin15 source ladders must hit or saturate before the distant k195 double-square destination.

Either result would turn k15 survival into a stronger ancestry-progress rule.
