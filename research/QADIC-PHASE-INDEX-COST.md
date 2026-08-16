# Exact q-adic phase-index cost

**Status:** exact lattice-index theorem for valuation expansion in the h169 source machine  
**Date:** 2026-08-16  
**Verifier:** `verify_qadic_phase_index_cost.py`  
**Depends on:** `PERSISTENT-SOURCE-QADIC-VALUATION-LADDER.md` and `BOUNDED-COMPLEXITY-CHARACTER-FINITENESS.md`.  
**Claim boundary:** this theorem measures the exact congruence index paid when routed source valuations are raised. It is not by itself a well-founded progress measure, does not prove that a lifted branch is nonempty after all other survivor constraints, and is not a termination theorem or Erdős–Straus proof.

## 1. One source: valuation is a nested route lattice

Let p be fixed, let j be an admissible origin shift, and let q be an odd prime source with

```text
q | C_j,
C_j = (p+j)/4.
```

Write

```text
C_j = qA.
```

Every persistent destination is

```text
k_n = j + 4qn,
n in Z_{>=0},
```

and

```text
C_{k_n} = C_j + qn
          = q(A+n).
```

Therefore, for every `e>=1`,

```text
v_q(C_{k_n}) >= e
iff
A+n = 0 mod q^(e-1)
iff
n = -A mod q^(e-1).
```

So the valuation-at-least-e destinations form exactly one residue class in the route-index lattice modulo

```text
q^(e-1).
```

Relative to the full multiplicity-one route shell, their exact lattice index is

```text
I_q(e) = q^(e-1).
```

## 2. Every upward valuation step costs exactly q

Inside the valuation-at-least-e lattice, the next condition

```text
v_q(C_k) >= e+1
```

selects exactly one of the q residue subclasses modulo `q^e`.

Hence

```text
I_q(e+1) / I_q(e) = q.
```

Equivalently:

> raising a routed source valuation floor by one multiplies the route-lattice index by exactly q.

The parent `v_q>=e` class splits into q children:

```text
q-1 children have exact valuation e,
1 child has valuation at least e+1.
```

This is an exact partition, not an asymptotic density statement.

## 3. Dual target-phase formulation

The same cost can be viewed with k fixed and p varying.

Since

```text
q^e | C_k
iff
p = -k mod 4q^e,
```

raising the valuation floor from e to e+1 refines

```text
p = -k mod 4q^e
```

to

```text
p = -k mod 4q^(e+1).
```

Thus, inside any compatible target-prime progression whose q-adic modulus has reached exactly `q^e`, the next lift occupies one of q congruence subclasses. Its relative index is again exactly q.

This is the target-phase version of the same lattice theorem.

## 4. Several distinct synchronized sources

Let

```text
q1,...,qm
```

be distinct odd routed source primes, all coprime to the relevant origin shifts and to one another.

Assume their multiplicity-one persistent routes have been synchronized. Let

```text
Q = product_i qi
```

and choose one synchronized destination k0. Every common persistent destination is

```text
k_n = k0 + 4Qn.
```

For each source qi, because `qi|C_k0`, write

```text
C_k0 = qi Bi,
Q = qi Qi,
```

with `gcd(Qi,qi)=1`. Then

```text
C_{k_n} = C_k0 + Qn
        = qi(Bi + Qi n).
```

Therefore

```text
v_qi(C_{k_n}) >= ei
iff
n = ai mod qi^(ei-1)
```

for one uniquely determined residue `ai`, because `Qi` is invertible modulo every power of qi.

The moduli

```text
qi^(ei-1)
```

are pairwise coprime. CRT therefore gives one simultaneous residue class modulo

```text
L(e1,...,em)
 = product_i qi^(ei-1).
```

Hence the exact common route-lattice index relative to the synchronized multiplicity-one shell is

```text
I(e1,...,em)
 = product_i qi^(ei-1).
```

## 5. Incremental multi-source cost

If only source qj is raised from `ej` to `ej+1`, while all other valuation floors are unchanged, then

```text
I(...,ej+1,...)
---------------- = qj.
I(...,ej,...)
```

If several distinct sources are simultaneously raised by increments `delta_i>=0`, the exact additional index is

```text
product_i qi^delta_i.
```

Thus valuation expansion has a multiplicative arithmetic cost determined by the actual source primes, not by an arbitrary scheduler weight.

## 6. Target-phase CRT with the h169 hard class

For source primes coprime to 840, the h169 hard-class condition

```text
p = 169 mod840
```

can be combined with fixed-destination source-lift conditions

```text
p = -k mod 4 * product_i qi^ei.
```

Whenever the multiplicity-one route shell is compatible, increasing source qi from exponent ei to `ei+1` adds exactly one new qi-adic digit and refines the combined target progression by index qi.

For distinct sources, the total refinement relative to their multiplicity-one target shell is

```text
product_i qi^(ei-1).
```

This is the phase-lattice cost used implicitly in the landed q29^10 and k195 q41^2/q37^2 constructions.

## 7. Landed examples

### q29 tenth lift

Relative to the materialized multiplicity-one q29 route, the condition

```text
v29(C951) >= 10
```

has exact route/phase index

```text
29^9.
```

Each step from exponent e to e+1 costs another factor29.

### k195 double-square gate

The two synchronized sources are

```text
q_D=41,
q_J=37.
```

Demanding both square lifts gives exact index

```text
41^(2-1) * 37^(2-1)
= 41*37
= 1517
```

relative to their synchronized multiplicity-one route shell.

In the target-phase representation, the corresponding extra q-adic modulus is likewise multiplied by 1517.

### q317 square breakout

Raising q317 from exponent1 to exponent2 costs exact index

```text
317.
```

That single upward move is precisely the layer where the landed character semantics change from multiplicity-one idempotence to source generation at k39/k167.

## 8. Coupling to bounded-complexity character finiteness

The landed bounded-complexity theorem says that, for fixed source arity m and valuation cap E, Jacobi character propagation is confined to a finite destination/character box and therefore eventually enters a finite quotient state or SCC if it does not hit.

The present theorem says that escaping such a box by raising a source valuation has an exact lattice cost:

```text
finite character SCC at bounded E
        |
        `-- raise q valuation by 1
                -> phase index multiplied by q.
```

This gives a rigorous two-axis grammar:

```text
horizontal axis: finite character-state motion / SCC closure
vertical axis:   q-adic valuation expansion with exact lattice index cost.
```

## 9. Why this is not yet termination

The phase index is **not** a well-founded descent variable.

An infinite nested chain

```text
mod q,
mod q^2,
mod q^3,
...
```

can remain arithmetically nonempty. Increasing lattice index therefore measures restriction/cost, but does not prove that only finitely many upward moves can occur.

Likewise, a branch may escape through higher source arity or a non-Jacobi exact mechanism.

So the machine may record

```text
PHASE_INDEX_COST
```

but may not promote it to `TERMINATION_RANK`.

## 10. Bryan Entanglement Cross boundary

This theorem gives the draft upward arrow a mathematically clean observational meaning:

```text
up (+/-) = valuation expansion that opens a new semantic layer
           while multiplying exact phase index by the source prime.
```

The upward label does not prove the cost. The q-adic congruence lattice does.

Likewise, finite rightward character motion can now be quotient-collapsed when it enters an SCC.

## 11. Next target

A genuine progress measure would need one more ingredient that prevents unbounded vertical motion.

The strongest next targets are:

1. derive a branch-local upper bound on useful valuation from exact signed-box ancestry; or
2. prove that sufficiently high valuation necessarily creates a terminal hit or a strict prime-modulus descent before another valuation increase is needed.

The k195 ancestry laboratory and the valuation/output-prime ceiling are the two current theorem families most likely to supply that missing cap.
