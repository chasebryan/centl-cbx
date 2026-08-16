# D-selector single-source saturation barrier

**Status:** exact finite-closure theorem for the h169 persistent-source ladders  
**Date:** 2026-08-16  
**Verifier:** `verify_d_selector_single_source_saturation_barrier.py`  
**Depends on:** `COMPANION-SOURCE-CHARACTER-CONSERVATION.md`, h169 class-seed arithmetic, and `JACOBI-SATURATION-CHARACTER-EXTRACTION.md`.  
**Claim boundary:** this theorem rules out Jacobi-kernel saturation by the h169 mandatory class seed plus exactly one D-selector renewed source on that source's persistent companion ladder. It does not rule out saturation after adding a second routed factor or richer exact ancestry state, does not prove a shift ceiling, and does not prove Erdős–Straus.

## 1. Question

The D-selector state forces three mixed-character factor witnesses. Once materialized, the companion-source conservation theorem turns them into positive target-prime sources:

```text
B witness: origin j=23, (q/23)=+1, (q/17)=-1
D witness: origin j=31, (q/31)=+1, (q/17)=-1
J witness: origin j=47, (q/47)=+1, (q/31)=-1.
```

A materialized source q persists through

```text
k = j + 4 q n,   n>=0,
```

with

```text
q | C_k
(q/k)=+1.
```

The natural first question is whether the mandatory h169 destination seed, enlarged by **that one routed factor q**, can ever Jacobi-saturate a persistent destination.

This theorem answers: **no**.

## 2. h169 mandatory seed

For an admissible h169 shift `k=3 mod4`, the hard-class seed is

```text
S0(k) = gcd(210, (169+k)/4).
```

Since

```text
210 = 2*3*5*7
```

is squarefree, `S0(k)` is squarefree and has at most four distinct prime factors.

With one routed prime q, define

```text
S(k,q) = lcm(S0(k), q).
```

This seed is still squarefree and has at most five distinct prime factors.

Therefore the number of divisors of its square is bounded by

```text
#Div(S^2) <= 3^5 = 243.
```

Consequently its divisor-square residue set modulo k has size at most243.

## 3. Jacobi-positive kernel size

For `k=3 mod4`, the Jacobi character on the unit group is nontrivial because

```text
Jacobi(-1/k) = -1.
```

Hence its positive kernel

```text
H_k = {u in U(k) : Jacobi(u/k)=+1}
```

has exactly

```text
|H_k| = phi(k)/2
```

members.

If `S(k,q)` Jacobi-saturates k, its divisor-square residues must equal `H_k`. Thus necessarily

```text
phi(k)/2 <= 243,
```

or

```text
phi(k) <= 486.
```

This converts an apparently infinite q-dependent route problem into a finite one.

## 4. Elementary absolute bound on k

For every positive integer n,

```text
phi(n)^2 >= n/2.
```

A direct prime-power proof is enough. If `p^a || n`, then

```text
phi(p^a)^2 / p^a = p^(a-2) (p-1)^2.
```

For every odd p this factor is at least1. For p=2 it is at least1 except in the single case `2^1`, where it is exactly1/2. Multiplying the prime-power factors therefore gives

```text
phi(n)^2 / n >= 1/2.
```

So

```text
phi(k) <= 486
```

implies

```text
k <= 2*486^2 = 472392.
```

No asymptotic estimate is being used. This is an elementary exact bound.

## 5. Complete persistent-route exhaustion

For each origin type

```text
B: j=23, negative transverse modulus17
D: j=31, negative transverse modulus17
J: j=47, negative transverse modulus31
```

the verifier exhausts every admissible `k=3 mod4` through472392 satisfying `phi(k)<=486`.

For each such k and origin j, write

```text
d = (k-j)/4.
```

A persistent route `k=j+4qn` exists exactly when an eligible source prime q divides d, with `n=d/q`.

The verifier considers every prime divisor q of d satisfying the corresponding D-selector witness character type:

```text
B: (q/23)=+1 and (q/17)=-1
D: (q/31)=+1 and (q/17)=-1
J: (q/47)=+1 and (q/31)=-1.
```

For every such pair `(k,q)`, it constructs

```text
S = lcm(S0(k), q)
```

and compares the exact divisor-square residue set against the complete Jacobi-positive kernel modulo k.

The complete exact census is:

```text
admissible k with phi(k)<=486: 158
largest such k:                 1155
eligible persistent pairs:      180
  B-type:                         61
  D-type:                         58
  J-type:                         61
Jacobi saturations:                0
```

The observed maximum1155 is a result of the exhaustive finite check, not an assumption used to obtain the rigorous472392 search bound.

## 6. Theorem

For the h169 D-selector state, let q be any materialized renewed source of one of the three proved character types, and let

```text
k = j + 4qn, n>=1,
```

be any later destination on its persistent companion ladder.

Then

```text
lcm(S0(k), q)
```

is **not** Jacobi-saturating modulo k.

Equivalently:

> the h169 mandatory class seed plus one renewed D-selector source is never enough to fill the destination Jacobi-positive kernel anywhere on that source's persistent route.

The origin `n=0` is not a new routing destination and is excluded from the saturation claim.

## 7. Interpretation

This is a useful negative theorem, not a dead end.

The D-selector state does create new positive sources. The conservation theorem opens exact persistent ladders. But the first naive scheduler policy

```text
materialize one source
-> walk its ladder
-> test base+q saturation
```

can now be deleted completely.

Every such attempt fails for theorem-level reasons plus finite exact closure.

The next constructive mechanism must use at least one of:

1. **two routed source factors** at the same destination;
2. an additional mandatory factor supplied by exact ancestry rather than the bare h169 class seed;
3. a non-saturation signed-box mechanism such as exact incoming repulsion;
4. a destination where the source participates in a richer exact-state promotion.

This is a real reduction of the candidate search grammar.

## 8. Machine consequence

A scheduler may add the exact rule

```text
if state == h169 D-selector
and destination is on a single materialized renewed-source persistent ladder
and candidate seed == lcm(class_seed(k), q):
    mark SINGLE_SOURCE_SATURATION_IMPOSSIBLE
```

This rule can suppress an infinite family of futile saturation probes.

It must **not** prune a destination from all research, because another routed factor or exact-state component may enlarge the seed and change saturation.

## 9. Bryan Entanglement Cross boundary

The natural directional history is:

```text
down (-/+): D-selector forces witness renewal
right (+):  witness orientation becomes a positive source
up (+/-):   persistent ladder opens infinitely many destinations
down (-/+): exact cardinality bound collapses the infinite ladder to a finite saturation question
left (-):   all single-source saturation candidates are eliminated
```

The arrows describe the proved transition history. They do not establish the cardinality bound, totient inequality, or saturation failure.

## 10. Next target

The immediate next theorem target is **two-source synchronization**:

> Can two of the three distinct renewed sources land in the same admissible destination, and if so, when does `lcm(S0(k), q1, q2)` Jacobi-saturate or force an exact signed-box hit?

Because each source has a persistent arithmetic progression, synchronization is a CRT problem over q-dependent step sizes. The support-separation theorem guarantees the sources are distinct, which keeps that next state structurally nondegenerate.
