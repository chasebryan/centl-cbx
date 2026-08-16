# Persistent-source q-adic valuation ladder

**Status:** exact general valuation theorem for materialized companion sources  
**Date:** 2026-08-16  
**Verifier:** `verify_persistent_source_qadic_valuation_ladder.py`  
**Depends on:** `COMPANION-SOURCE-CHARACTER-CONSERVATION.md` and exact companion arithmetic `C_k=(p+k)/4`.  
**Claim boundary:** this theorem classifies q-adic valuation along a persistent source ladder. It does not assert saturation, termination, or an Erdős–Straus proof.

## 1. Setup

Let

```text
p = 1 mod4,
j = 3 mod4,
C_j = (p+j)/4,
q = an odd prime divisor of C_j.
```

Write

```text
C_j = q A.
```

The materialized source q persists at every admissible destination

```text
k_n = j + 4 q n,
```

because

```text
C_(k_n)
 = (p+j+4qn)/4
 = C_j + qn
 = q(A+n).
```

This identity gives the complete valuation grammar.

## 2. Exact valuation theorem

For every `n>=0`,

```text
v_q(C_(k_n)) = 1 + v_q(A+n).
```

Therefore, for every `e>=2`,

```text
v_q(C_(k_n)) >= e
iff
A+n = 0 mod q^(e-1)
iff
n = -A mod q^(e-1).
```

Exact valuation is

```text
v_q(C_(k_n)) = e
```

iff

```text
n = -A mod q^(e-1)
```

but

```text
n != -A mod q^e.
```

For exponent1 the rule is simply

```text
v_q(C_(k_n)) = 1
iff
n != -A mod q.
```

So the persistent route decomposes into nested q-adic lift subladders.

## 3. Destination form

The same theorem has a particularly clean shift-coordinate form.

Since

```text
qA = C_j = (p+j)/4,
```

substitute

```text
n = -A + q^(e-1)m
```

into `k_n=j+4qn`:

```text
k
 = j + 4q(-A + q^(e-1)m)
 = j - 4qA + 4q^e m
 = -p + 4q^e m.
```

Hence

```text
v_q(C_k) >= e
iff
k = -p mod 4q^e.
```

Exact exponent e is

```text
k = -p mod 4q^e
```

but

```text
k != -p mod 4q^(e+1).
```

Thus every q-adic valuation layer is one exact arithmetic progression in the admissible shift coordinate.

## 4. Nested lift tree

Starting from the persistent source ladder

```text
q | C_k
<=>
k = -p mod4q,
```

the higher lifts form the nested chain

```text
q^2 | C_k  <=> k = -p mod4q^2
q^3 | C_k  <=> k = -p mod4q^3
q^4 | C_k  <=> k = -p mod4q^4
...
```

Each level is exactly one of q subphases of the previous level.

In the route-index coordinate n:

```text
v_q(C_k)>=2 : 1 class mod q
v_q(C_k)>=3 : 1 class mod q^2
v_q(C_k)>=4 : 1 class mod q^3
...
```

So the fraction of persistent route indices with valuation at least e is exactly

```text
1 / q^(e-1).
```

The exact exponent-e fraction is

```text
(q-1) / q^e.
```

These are exact periodic proportions on the n-lattice, not probabilistic assumptions.

## 5. Why this matters for the saturation barriers

The landed single-source barrier tested the multiplicity-one seed

```text
S1 = lcm(S0(k),q).
```

That theorem is valid exactly on the valuation-one sector

```text
v_q(C_k)=1.
```

If the state only knows `q|C_k` but has not resolved the q-adic valuation, it is unsafe to apply the multiplicity-one barrier globally.

The present theorem supplies the missing proof-state coordinate:

```text
source_q
source_origin_j
source_origin_quotient_A = C_j/q
route_index_n
qadic_valuation = 1 + v_q(A+n)
```

A scheduler can determine whether it is in the exponent1 sector or a higher q-adic lift before invoking a saturation barrier.

## 6. Pair-source valuation state

For two synchronized materialized sources `q1,q2`, each has its own exact lift coordinate:

```text
v_q1(C_k) >= e1 <=> k = -p mod 4q1^e1
v_q2(C_k) >= e2 <=> k = -p mod 4q2^e2.
```

Because `q1` and `q2` are distinct primes, the simultaneous lift system is compatible by CRT after removing the common factor4.

Thus synchronized source multiplicities are not independent guesses. They are exact nested CRT phases.

The landed two-source multiplicity-one barrier applies only to the sector

```text
v_q1(C_k)=1
v_q2(C_k)=1.
```

Higher valuations remain separate live states.

## 7. Machine normalization

The persistent-source proof object should therefore be normalized as

```text
SOURCE = (
  q,
  origin_j,
  A=C_j/q,
  target_character,
  transverse_characters,
  route_phase,
  valuation_phase
)
```

with

```text
route_phase:
    k = -p mod4q

valuation_phase(e):
    k = -p mod4q^e.
```

Unknown valuation must remain `UNKNOWN`. It must never be coerced to1 for the purpose of pruning.

## 8. Bryan Entanglement Cross boundary

This valuation ladder is naturally an `up (+/-)` expansion of a materialized source: one constructive route opens nested higher-power subroutes with different downstream consequences.

If a theorem later proves that a high-valuation subroute is dead, that may be annotated as `down (-/+)` or `left (-)` depending on the exact mechanism.

BEC/BREC annotations remain metadata. The q-adic identity is the proof-bearing object.

## 9. Next target

Now that the valuation state is exact, the next question is well-posed:

> For a renewed D-selector source q, can a higher-power seed `lcm(S0(k),q^e)` Jacobi-saturate on the exact lift subladder `k=-p mod4q^e`?

This should be attacked valuation-by-valuation rather than by conflating all persistent destinations with the exponent1 state.
