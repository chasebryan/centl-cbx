# Exact q-adic phase-index cost

**Status:** exact lattice-index theorem for routed-source valuation expansion.  
**Date:** 2026-08-16  
**Verifier:** `verify_qadic_phase_index_cost.py`  
**Depends on:** `PERSISTENT-SOURCE-QADIC-VALUATION-LADDER.md` and `BOUNDED-COMPLEXITY-CHARACTER-FINITENESS.md`.  
**Claim boundary:** exact congruence-index accounting only. This is not by itself a termination rank, a closed decomposition method, or an Erdős–Straus proof.

## One source

Let q be an odd materialized source at origin j, with

```text
C_j=(p+j)/4=qA.
```

Its persistent destinations are

```text
k_n=j+4qn,
C_{k_n}=q(A+n).
```

Therefore, for every `e>=1`,

```text
v_q(C_{k_n})>=e
iff n=-A mod q^(e-1).
```

So the valuation-at-least-e route shell has exact index

```text
I_q(e)=q^(e-1)
```

inside the multiplicity-one route shell.

Increasing the valuation floor once gives

```text
I_q(e+1)/I_q(e)=q.
```

Equivalently, a `v_q>=e` class has exactly q children modulo `q^e`: q-1 have exact valuation e and one has valuation at least e+1.

## Dual target-phase form

For fixed destination k,

```text
q^e|C_k
iff p=-k mod 4q^e.
```

Thus increasing e by one also refines a compatible target-p progression by exact index q.

## Several synchronized sources

Let distinct odd sources `q_1,...,q_m` have synchronized multiplicity-one routes. Put

```text
Q=product_i q_i
```

and write their common destinations as

```text
k_n=k_0+4Qn.
```

For each i,

```text
C_{k_0}=q_i B_i,
Q=q_i Q_i,
gcd(Q_i,q_i)=1,
```

so

```text
C_{k_n}=q_i(B_i+Q_i n).
```

The condition `v_{q_i}(C_{k_n})>=e_i` therefore selects one residue class of n modulo `q_i^(e_i-1)`. Since these prime-power moduli are pairwise coprime, CRT gives one simultaneous class modulo

```text
I(e_1,...,e_m)=product_i q_i^(e_i-1).
```

Hence the exact lattice index relative to the synchronized multiplicity-one shell is that product. Raising only source q_j by one multiplies the index by exactly q_j. Raising several sources by increments `delta_i` multiplies it by

```text
product_i q_i^delta_i.
```

## h169 target-phase form

For routed source primes coprime to840, the hard class

```text
p=169 mod840
```

combines by CRT with fixed-destination lift conditions. Once the multiplicity-one shell is compatible, requiring exponents `e_i` adds exact relative index

```text
product_i q_i^(e_i-1).
```

## Landed examples

```text
q29 exponent10:
    extra index = 29^9

k195 q41^2/q37^2:
    extra index = 41*37 = 1517

q317 exponent2:
    extra index = 317.
```

These are exact lattice indices, not heuristic rarity scores.

## Coupling to finite character SCCs

The bounded-complexity theorem proves that bounded Jacobi character propagation lives in a finite quotient graph. The present theorem measures what an escape by valuation costs:

```text
bounded character SCC
    -> raise q valuation by one
    -> exact phase index multiplied by q.
```

This gives a rigorous two-axis grammar:

```text
horizontal: finite character-state motion / SCC closure
vertical:   q-adic valuation expansion with exact lattice cost.
```

## Critical boundary

`PHASE_INDEX_COST` is not a well-founded termination variable. An infinite nested q-adic progression can remain nonempty, so increasing index measures restriction without proving that upward motion must stop.

The machine may record the exact cost, but may not call it `TERMINATION_RANK`.

## Bryan Entanglement Cross boundary

A proved valuation increase is a natural observational `up (+/-)` event: it enters a richer semantic layer while multiplying the exact phase index by q. BEC/BREC remains metadata; the q-adic lattice is the proof.

## Next target

Combine this theorem with the landed output-prime ceiling. If a saturated miss creates a new prime `r>=q`, the valuation must be large enough to permit non-descent. That should give an exact lower bound on the phase-index cost of every non-descending source transition.
