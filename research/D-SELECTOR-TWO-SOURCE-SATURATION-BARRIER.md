# D-selector two-source synchronization and saturation barrier

**Status:** exact synchronization theorem plus complete finite two-source saturation closure  
**Date:** 2026-08-16  
**Verifier:** `verify_d_selector_two_source_saturation_barrier.py`  
**Depends on:** `COMPANION-SOURCE-CHARACTER-CONSERVATION.md`, `D-SELECTOR-SINGLE-SOURCE-SATURATION-BARRIER.md`, h169 class-seed arithmetic, and the D-selector witness distinctness theorem.  
**Claim boundary:** this theorem concerns Jacobi-kernel saturation by the bare h169 class seed plus exactly two distinct D-selector renewed sources. It does not rule out richer ancestry factors, three-source saturation, incoming-repulsion mechanisms, or other signed-box transitions. It is not a termination theorem and not an Erdős–Straus proof.

## 1. Two persistent sources always synchronize

Let two materialized renewed sources have distinct prime values `q1 != q2` and origins

```text
j1,j2 in {23,31,47}.
```

Their persistent companion routes are

```text
k = j1 mod 4q1
k = j2 mod 4q2.
```

All three origins are `3 mod4`. Write

```text
k = 3 + 4x,
a_i = (j_i-3)/4.
```

Then the two route conditions become

```text
x = a1 mod q1
x = a2 mod q2.
```

The D-selector odd-support theorem makes the renewed witness primes distinct. Therefore `gcd(q1,q2)=1`, and CRT gives a unique solution

```text
x mod q1*q2.
```

Hence every pair of distinct materialized renewed sources has an infinite exact common destination ladder

```text
k = k0 + 4*q1*q2*n.
```

So two-source synchronization is never the obstruction.

## 2. Bare two-source seed size

At an h169 destination k, let

```text
S0(k) = gcd(210,(169+k)/4)
```

be the mandatory hard-class seed.

With two routed source primes define

```text
S2(k,q1,q2) = lcm(S0(k),q1,q2).
```

Because 210 is squarefree, `S2` is squarefree and has at most six distinct prime factors.

Therefore

```text
#Div(S2^2) <= 3^6 = 729.
```

Its divisor-square residue set modulo k can therefore contain at most729 residues.

## 3. Totient bound

For `k=3 mod4`, the Jacobi-positive unit kernel has exactly

```text
phi(k)/2
```

members because `Jacobi(-1/k)=-1` makes the character nontrivial.

Jacobi saturation by `S2` requires

```text
phi(k)/2 <= 729,
```

hence

```text
phi(k) <= 1458.
```

Using the elementary inequality

```text
phi(k)^2 >= k/2,
```

we obtain the rigorous absolute bound

```text
k <= 2*1458^2 = 4,251,528.
```

Thus the apparently infinite synchronized-ladder question again has a complete finite closure.

## 4. Exact source-pair classes

The three proved witness types are

```text
B: origin23, (q/23)=+1, (q/17)=-1
D: origin31, (q/31)=+1, (q/17)=-1
J: origin47, (q/47)=+1, (q/31)=-1.
```

The forced witnesses occupy distinct reservoirs, so the required pair types are

```text
B-D
B-J
D-J.
```

For each admissible k inside the rigorous bound, a source of origin j can persist to k exactly when

```text
q | (k-j)/4.
```

The verifier factors those route indices, retains every prime q satisfying the corresponding character type, forms every distinct cross-reservoir pair, and tests

```text
S2 = lcm(S0(k),q1,q2)
```

against the exact Jacobi-positive kernel modulo k.

The enumeration is deliberately broader than actual D-selector realizations: it accepts every abstract source prime satisfying the proved character types and route congruences. Therefore a zero-saturation result on this superset applies a fortiori to the actual reservoir witnesses.

## 5. Complete exact result

The verifier obtains

```text
admissible k with phi(k)<=1458: 474
largest such low-totient k:      3255
synchronized candidate pairs:     249
  B-D:                             102
  B-J:                              46
  D-J:                             101
largest synchronized candidate k: 2499
Jacobi saturations:                  0
```

No bare two-source D-selector seed saturates any common persistent destination.

The distinction between `3255` and `2499` is intentional:

- 3255 is the largest admissible low-totient shift surviving the cardinality gate;
- 2499 is the largest shift at which an eligible synchronized D-selector source pair actually occurs.

## 6. Theorem

Let `q1,q2` be two distinct materialized renewed D-selector sources drawn from two of the B,D,J reservoirs. Let k be any later admissible destination lying on both persistent source ladders.

Then

```text
lcm(S0(k),q1,q2)
```

is not Jacobi-saturating modulo k.

Thus the bare h169 class seed plus one or two renewed D-selector sources is insufficient for Jacobi saturation everywhere on their exact persistent routes.

## 7. Stronger machine consequence

Combining the one-source and two-source barriers gives the exact scheduler rule

```text
bare h169 class seed
+ <=2 renewed D-selector routed primes
-> Jacobi saturation impossible.
```

So a saturation-oriented scheduler must not spend work on these states unless it has at least one additional proof-bearing seed factor beyond that bare state.

This is stronger than a performance heuristic. It is a mathematical elimination of two infinite families of saturation probes.

It does **not** imply the underlying destination itself is dead. The same destination may still be useful through:

- all three renewed sources;
- a further exact ancestry factor;
- incoming repulsion;
- exact-state promotion;
- direct Type-I or full Type-II signed-box geometry.

## 8. Bryan Entanglement Cross boundary

The transition history is naturally

```text
up (+/-): two independent persistent routes open
right (+): CRT guarantees synchronization
down (-/+): cardinality and totient bounds collapse the infinite synchronized family
left (-): exact closure eliminates every bare two-source saturation state.
```

These labels describe the theorem after the fact. They do not participate in CRT, Jacobi saturation, or proof validity.

## 9. Next target

The next saturation threshold is now forced:

> either synchronize all three renewed D-selector sources, or introduce a genuinely new proof-bearing ancestry factor.

The three-source bare seed has at most seven distinct prime factors and therefore at most `3^7=2187` square-divisor residues. A complete three-source analysis would begin with

```text
phi(k) <= 4374
k <= 2*4374^2.
```

Before paying that larger finite-closure cost, the better strategic question is whether exact-state promotion or the imported character-saturation graph supplies an additional structural factor that reduces the problem more sharply than a raw three-source census.
