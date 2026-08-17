# h289 k=19 quotient normal form

**Status:** exact class-conditioned finite-group theorem  
**Date:** 2026-08-17  
**Hard class:** `p = 289 mod840`  
**Application:** `CBX-Lane-I-shift-history-v1`

## 1. Statement

For every Mordell-hard prime

```text
p = 289 mod840,
```

the k19 cofactor

```text
C19=(p+19)/4
```

contains a forced factor `7`.

That factor does more than provide a small residue seed. Modulo 19 it supplies an entire order-three subgroup of the signed-box exponent group, so the exact k19 Type-II-miss problem factors through the six-element quotient

```text
Z/18Z / <6>  ~=  Z/6Z.
```

The complete quotient has only

```text
9 Type-II-miss states,
6 combined-miss states,
3 Type-I-only states.
```

The full seeded q19 state space consists of exactly three lifts of each quotient state:

```text
27 Type-II-miss states
 = 18 combined misses
 +  9 Type-I-only states.
```

This is a complete exact local normal form for the h289 k19 Type-II-miss state space.

---

## 2. Why factor 7 is forced

The h289 hard class corresponds to

```text
T=(p+23)/24 = 13 mod35.
```

Thus

```text
C19=6T-1 = 77 mod210,
```

so

```text
7 | C19.
```

Equivalently, directly from the hard class,

```text
p+19 = 0 mod28.
```

The forced prime is therefore universal over the entire h289 lane.

---

## 3. Factor 7 supplies a subgroup, not merely three random points

Use primitive root `2` modulo 19. Then

```text
7 = 2^6 mod19.
```

Since

```text
ord_19(7)=3,
```

one valuation of 7 contributes signed exponent support

```text
{0,+6,-6}
 = {0,6,12}
```

inside `Z/18Z`.

But this is already the complete subgroup

```text
K=<6>={0,6,12}.
```

Higher powers of 7 do not enlarge the support beyond K.

Once K is present, every subsequent signed-box support is K-periodic. If exponent `x` occurs, then

```text
x,
x+6,
x+12
```

all occur.

That is the structural reason a quotient exists.

---

## 4. Exact six-state exponent quotient

Define

```text
cbar = c mod6,
Sbar = S mod6,
```

where `(c,S)` is the ordinary q19 cyclic signed-box state.

Because support is K-periodic, target membership depends only on `(cbar,Sbar)`.

The two targets reduce to

```text
Type II : 9 mod18 -> 3 mod6
Type I  : 7-c mod18 -> 1-cbar mod6.
```

Therefore

```text
Type-II miss iff 3 not in Sbar,
combined miss iff 3 not in Sbar and 1-cbar not in Sbar.
```

A prime-factor occurrence whose base-2 exponent is `a mod18` acts only through

```text
a mod6
```

on this quotient.

The six quotient atom classes correspond to the following actual unit residues modulo 19:

```text
a mod6   residues mod19
-----------------------
0        {1,7,11}
1        {2,3,14}
2        {4,6,9}
3        {8,12,18}
4        {5,16,17}
5        {10,13,15}.
```

The class `3` is immediately Type-II constructive because adding it places the quotient target `3` into support.

---

## 5. Complete nine-state table

Starting from the forced-factor quotient seed

```text
(cbar,Sbar)=(0,{0}),
```

the exact Type-II-miss closure is:

```text
cbar   Sbar                 Type-I target   class
--------------------------------------------------------
0      {0}                       1           combined miss
1      {0,1,5}                   0           Type-I-only
2      {0,2,4}                   5           combined miss
4      {0,2,4}                   3           combined miss
5      {0,1,5}                   2           combined miss
0      {0,1,2,4,5}               1           Type-I-only
0      {0,2,4}                   1           combined miss
2      {0,1,2,4,5}               5           Type-I-only
4      {0,1,2,4,5}               3           combined miss.
```

No other quotient state can remain Type-II-missing.

So the complete combined-miss quotient is only six states.

---

## 6. Why there are exactly three full lifts per quotient state

The quotient forgets the K-component of the product exponent.

For each quotient product exponent `cbar`, the full exponent may lie in exactly three classes:

```text
cbar,
cbar+6,
cbar+12 mod18.
```

The verifier reconstructs the full q19 seeded closure independently and finds:

```text
27 full Type-II-miss states,
9 quotient states,
exactly 3 full lifts for every quotient state.
```

The target classification is constant on each three-state fiber because both exact target-membership questions are K-periodic.

Hence

```text
6 quotient combined misses * 3 = 18 full combined misses
3 quotient Type-I-only states * 3 = 9 full Type-I-only states.
```

---

## 7. Comparison with the other hard classes

The k19 hard-class seed picture is now qualitatively different across lanes.

```text
h121:
  forced 5 and7 fill the full QR subgroup
  -> Type-II miss iff all factors QR
  -> no Type-I-only state

h289:
  forced 7 fills an order-three subgroup
  -> exact quotient from 18 exponents to 6
  -> 9 Type-II-miss quotient states

h1/h361:
  forced 5 gives a strong seed but not a subgroup-complete local support

h169/h529:
  no forced 5/7 seed at k19.
```

So h289 is neither as rigid as h121 nor as unconstrained as h169/h529. It has its own exact quotient geometry.

---

## 8. Exact regression witnesses

The verifier preserves several h289 prime states.

```text
p=1,129
C19=287=7*41
k19 = Type-I-only.
```

```text
p=8,689
C19=2,177=7*311
k19 = combined miss.
```

```text
p=22,129
C19=5,537=7^2*113
k19 = Type-II-only.
```

The first two lie inside the Type-II-miss quotient closure on opposite sides of the moving Type-I target. The third confirms that factors outside the quotient miss closure still construct exactly as expected.

These are regression guards, not the proof of the finite-group theorem.

---

## 9. Cross-coordinate value

The generic unseeded q19 Type-II-miss universe has

```text
254 states.
```

The h289 forced factor had already reduced that to

```text
27 full states.
```

The quotient theorem now shows that the exact target-relevant information is only

```text
9 quotient states,
```

of which only six are combined misses.

That is a substantial theorem-safe compression for any future q23 predecessor search in hard class289.

A cross-coordinate machine does not need to carry the full 439-state q19 automaton, nor even the 27 seeded states, when it only needs to decide the two exact k19 targets in h289. The nine-state quotient is sufficient.

---

## 10. Executable verifier

Run

```sh
python3 research/verify_h289_k19_quotient_normal_form.py
```

The verifier independently checks:

```text
h289 forces literal factor7 in C19,
log_2(7)=6 mod18,
ord_19(7)=3,
forced support K={0,6,12},
K-periodicity of every full seeded state,
the complete nine-state quotient closure,
the six/three combined-vs-Type-I split,
the complete 27-state full seeded closure,
exactly three full lifts per quotient state,
agreement with the generic signed-box automaton,
and exact prime regression witnesses.
```

---

## 11. Claim boundary

This theorem completely classifies the **local h289 k19 Type-II-miss residue state space** up to the exact quotient relevant to target membership.

It does not assert that all nine quotient states occur after k3/k7/k11/k15 ancestry, does not turn missing finite realizations into pruning rules, does not establish a universal Lane-I ceiling, and does not prove Erdős–Straus.
