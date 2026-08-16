# D-selector two-source synchronization and multiplicity-one saturation barrier

**Status:** exact synchronization theorem plus complete finite two-source saturation closure  
**Date:** 2026-08-16  
**Verifier:** `verify_d_selector_two_source_saturation_barrier.py`  
**Depends on:** `COMPANION-SOURCE-CHARACTER-CONSERVATION.md`, `D-SELECTOR-SINGLE-SOURCE-SATURATION-BARRIER.md`, h169 class-seed arithmetic, and D-selector witness distinctness.  
**Claim boundary:** this theorem concerns the bare h169 class seed plus **one known copy of each of two distinct renewed source primes**, i.e. `lcm(S0,q1,q2)`. It does not rule out q-adic valuation lifts such as `q1^2|C_k`, richer ancestry factors, three-source states, incoming repulsion, or other signed-box transitions. It is not a termination theorem and not an Erdős–Straus proof.

## 1. Two persistent sources always synchronize

For distinct materialized source primes `q1 != q2` with origins `j1,j2 in {23,31,47}`, their persistent routes are

```text
k = j1 mod 4q1
k = j2 mod 4q2.
```

Write `k=3+4x` and `a_i=(j_i-3)/4`. Then

```text
x = a1 mod q1
x = a2 mod q2.
```

Odd-support separation makes the renewed witnesses distinct, so CRT gives a unique solution modulo `q1*q2`. Every source pair therefore has an infinite common destination ladder

```text
k = k0 + 4*q1*q2*n.
```

Synchronization is not the obstruction.

## 2. Multiplicity-one seed size

At h169 destination k,

```text
S0(k)=gcd(210,(169+k)/4).
```

The multiplicity-one two-source seed is

```text
S2=lcm(S0(k),q1,q2).
```

Since 210 is squarefree, `S2` has at most six distinct prime factors, so

```text
#Div(S2^2) <= 3^6 = 729.
```

For `k=3 mod4`, the nontrivial Jacobi-positive kernel has size `phi(k)/2`. Saturation therefore requires

```text
phi(k) <= 1458.
```

Because k is odd, the factorwise identity

```text
phi(k)^2/k = product_{p^a||k} p^(a-2)(p-1)^2
```

has every factor at least1. Hence

```text
phi(k)^2 >= k,
```

and the rigorous absolute bound sharpens to

```text
k <= 1458^2 = 2,125,764.
```

## 3. Exact source-pair classes

The proved witness types are

```text
B: origin23, (q/23)=+1, (q/17)=-1
D: origin31, (q/31)=+1, (q/17)=-1
J: origin47, (q/47)=+1, (q/31)=-1.
```

The cross-reservoir pair types are B-D, B-J, and D-J.

For each admissible k in the rigorous bound, a source of origin j persists exactly when

```text
q | (k-j)/4.
```

The verifier accepts every abstract prime q satisfying the corresponding character type and route congruence, a superset of actual D-selector realizations, then tests the exact multiplicity-one seed `lcm(S0,q1,q2)` against the full Jacobi-positive kernel.

## 4. Complete exact result

```text
admissible k with phi(k)<=1458: 474
largest such low-totient k:      3255
synchronized candidate pairs:     249
  B-D:                             102
  B-J:                              46
  D-J:                             101
largest synchronized candidate k: 2499
multiplicity-one saturations:        0
```

The values 3255 and2499 are deliberately distinct telemetry fields: the first is the largest low-totient shift surviving the cardinality gate, the second the largest actual synchronized source-pair candidate.

## 5. Theorem

Let `q1,q2` be two distinct materialized renewed D-selector sources from different B,D,J reservoirs and let k lie on both persistent ladders. Then

```text
lcm(S0(k),q1,q2)
```

is not Jacobi-saturating modulo k.

Combined with the landed one-source multiplicity-one closure, the exact safe scheduler statement is

```text
bare h169 class seed
+ at most two distinct renewed source primes,
  each supplied only to exponent1
-> Jacobi saturation impossible.
```

This does **not** authorize pruning a q-adic lift. If exact state proves `q^e|C_k` with `e>=2`, the seed contains additional q powers and this theorem no longer applies.

It also does not kill the destination itself. Three distinct sources, additional ancestry, incoming repulsion, exact-state promotion, or direct Type-I/full-Type-II geometry remain live.

## 6. Machine consequence

The scheduler may suppress multiplicity-one saturation probes only when the proof state records no stronger q-adic valuation:

```text
if source_count <= 2
and every routed source valuation_known == 1
and no additional proof-bearing seed factor:
    SINGLE_OR_PAIR_MULTIPLICITY_ONE_SATURATION = IMPOSSIBLE
```

Unknown valuation must not be silently treated as exponent1.

## 7. Bryan Entanglement Cross boundary

BEC/BREC may annotate route expansion, CRT synchronization, finite excavation, and obstruction. It cannot infer source valuation and grants no pruning permission.

## 8. Next target

The correct next attack is **valuation-aware source geometry** before a raw three-source census:

1. classify q-adic lift phases on the persistent ladder;
2. determine whether `S0*q^e` or `S0*q1^e1*q2^e2` can saturate for `e_i>=2`;
3. only after those lifts are controlled should the machine conclude that three distinct sources or a new ancestry factor is necessary.
