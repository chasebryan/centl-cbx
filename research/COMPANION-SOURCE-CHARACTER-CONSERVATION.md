# Companion-source character conservation

**Status:** exact general routing lemma with Route-B D-selector corollaries  
**Date:** 2026-08-16  
**Verifier:** `verify_companion_source_character_conservation.py`  
**Depends on:** exact companion arithmetic `C_k=(p+k)/4`, quadratic/Jacobi reciprocity, and `D-SELECTOR-MIXED-CHARACTER-RENEWAL.md`.  
**Claim boundary:** this theorem converts a materialized companion factor into a correctly oriented positive target-prime character source and proves character conservation along its persistent admissible route. It does not prove that any destination saturates, hits, or terminates the search, and it is not an Erdős–Straus proof.

## 1. Setup

Let

```text
p = an odd prime with p = 1 mod4,
j = an odd admissible shift with j = 3 mod4,
C_j = (p+j)/4,
q = an odd prime divisor of C_j,
gcd(q,j)=1.
```

Because `q|C_j`,

```text
p+j = 0 mod 4q.
```

In particular

```text
p = -j mod q.
```

The character orientation problem is:

> if the reservoir theorem gives `(q/j)`, what does that say about the legacy routing character `(q/p)`?

## 2. Orientation-conversion theorem

### Theorem

Under the setup above,

```text
(q/p) = (q/j),
```

where `(q/p)` is a Legendre symbol and `(q/j)` is the Jacobi symbol (Legendre when j is prime).

### Proof

Since `p=1 mod4`, quadratic reciprocity gives

```text
(q/p) = (p/q).
```

Because `p=-j modq`,

```text
(p/q) = (-j/q)
      = (-1/q)(j/q).
```

Since `j=3 mod4`, reciprocity between j and q gives

```text
(j/q) = (-1/q)(q/j).
```

Therefore

```text
(q/p)
 = (-1/q)^2 (q/j)
 = (q/j).
```

No assumption on `q mod4` is needed.

## 3. Persistent companion route

The stronger congruence

```text
p+j = 0 mod4q
```

implies that for every integer `n>=0`, the shift

```text
k_n = j + 4qn
```

satisfies

```text
k_n = 3 mod4
```

and

```text
q | C_(k_n).
```

Indeed,

```text
p+k_n = (p+j) + 4qn = 0 mod4q.
```

So every companion factor q generates an exact infinite **persistent route ladder**

```text
j,
j+4q,
j+8q,
j+12q,
...
```

inside the admissible shift geometry.

## 4. Character-conservation theorem

### Theorem

For every persistent destination

```text
k = j + 4qn,
```

we have

```text
(q/k) = (q/j) = (q/p).
```

### Proof

Because `k=3 mod4`, Jacobi reciprocity gives

```text
(q/k) = (-1/q)(k/q).
```

But `k=j modq`, so

```text
(k/q) = (j/q).
```

And because `j=3 mod4`,

```text
(j/q) = (-1/q)(q/j).
```

Thus

```text
(q/k)
 = (-1/q)^2 (q/j)
 = (q/j).
```

Combining with the orientation theorem yields

```text
(q/k) = (q/p) = (q/j).
```

The source character is therefore **conserved along the entire persistent companion route**.

## 5. Transverse negative-character cancellation

Suppose additionally that a small odd modulus `m` satisfies

```text
(q/m) = -1.
```

If a persistent destination k is divisible by m, write

```text
k = m*s.
```

When the source is positive at its origin,

```text
(q/j)=+1,
```

character conservation gives

```text
(q/k)=+1.
```

By multiplicativity in the denominator,

```text
(q/k) = (q/m)(q/s).
```

Hence

```text
+1 = (-1)(q/s),
```

so necessarily

```text
(q/s) = -1.
```

This is the **transverse-character cancellation law**:

> a negative secondary character cannot make the full routed Jacobi character negative; any persistent destination containing that negative modulus must place a compensating negative character in the complementary quotient.

The barrier is exact and independent of how s factors.

## 6. D-selector witness conversion

The landed D-selector witness theorem gives three distinct odd factors:

```text
q_B | B with (q_B/23)=+1 and (q_B/17)=-1
q_D | D with (q_D/31)=+1 and (q_D/17)=-1
q_J | J with (q_J/47)=+1 and (q_J/31)=-1.
```

Their origin shifts are respectively

```text
j_B = 23
j_D = 31
j_J = 47.
```

All three origins are `3 mod4`, and all three q values divide the corresponding companions.

Therefore the orientation theorem upgrades the materialized witnesses to

```text
(q_B/p)=+1
(q_D/p)=+1
(q_J/p)=+1.
```

They are genuine positive target-prime character sources once the witness primes themselves have been identified.

Their persistent route ladders are

```text
q_B : k = 23 + 4 q_B n
q_D : k = 31 + 4 q_D n
q_J : k = 47 + 4 q_J n.
```

At every destination on the corresponding ladder,

```text
(q_B/k)=+1
(q_D/k)=+1
(q_J/k)=+1.
```

## 7. Secondary-character barriers on the three ladders

The negative witness characters now become transverse constraints rather than direct negative routes.

### B witness

If a persistent q_B destination is divisible by17,

```text
k = 17*s,
```

then

```text
(q_B/s)=-1.
```

### D witness

If a persistent q_D destination is divisible by17,

```text
k = 17*s,
```

then

```text
(q_D/s)=-1.
```

### J witness

If a persistent q_J destination is divisible by31,

```text
k = 31*s,
```

then

```text
(q_J/s)=-1.
```

So the obvious attempt to turn the secondary negative character into a negative full Jacobi destination **self-cancels**.

This does not make the witness useless. Positive routed factors are exactly what can enlarge a positive seed kernel and participate in composite Jacobi saturation. It does mean that the next search must look for **saturation/extraction**, not a naive direct negative-coset hit.

## 8. Machine semantics

The proof state may now distinguish two stages:

```text
WITNESS(q,j,m):
    q | C_j
    (q/j)=+1
    (q/m)=-1

MATERIALIZED_SOURCE(q):
    (q/p)=+1
    route_ladder = {j+4qn : n>=0}
    (q/k)=+1 on every route destination
```

The orientation theorem permits

```text
WITNESS -> MATERIALIZED_SOURCE
```

only when q is an actual identified prime factor of C_j.

An existential witness obligation with unknown q may carry the theorem symbolically, but a scheduler cannot enumerate concrete destination shifts until q is materialized.

## 9. Bryan Entanglement Cross boundary

This theorem gives a useful directional interpretation:

- `down (-/+)`: rigid state forces a mixed-character reservoir witness;
- `right (+)`: orientation conversion proves a positive target-prime source;
- `up (+/-)`: the source opens an infinite persistent destination ladder;
- `left/down`: the transverse negative character encounters a cancellation barrier instead of becoming a direct negative Jacobi route.

Those labels are scheduling/telemetry metadata. Reciprocity and companion congruences carry the proof.

## 10. Next target

The correct next search is dynamic composite saturation:

1. materialize q_B, q_D, or q_J on exact candidate states;
2. walk its persistent ladder `j+4qn`;
3. combine the positive routed q with mandatory destination seed factors;
4. test whether the enlarged seed saturates the destination QR/Jacobi-positive kernel;
5. if saturation occurs, extract a new fixed prime character or terminate by an incompatible center.

A theorem showing that one of the three forced sources must saturate within a bounded symbolic destination family would be a genuine candidate progress rule toward a decomposition method.
