# D-selector single-source multiplicity-one saturation barrier

**Status:** exact finite-closure theorem for the valuation-one sector of h169 persistent-source ladders  
**Date:** 2026-08-16  
**Verifier:** `verify_d_selector_single_source_saturation_barrier.py`  
**Refined by:** `PERSISTENT-SOURCE-QADIC-VALUATION-LADDER.md`  
**Claim boundary:** this theorem rules out Jacobi saturation by the h169 class seed plus **one known copy** of a renewed source prime, `lcm(S0(k),q)`. It applies only when the proof state establishes `v_q(C_k)=1`. Higher q-adic lifts remain live. It is not a shift ceiling, termination theorem, or Erdős–Straus proof.

## 1. Multiplicity-one seed

For admissible h169 shift k,

```text
S0(k)=gcd(210,(169+k)/4).
```

In the valuation-one sector for one routed source q,

```text
S1=lcm(S0(k),q).
```

Since 210 is squarefree, S1 has at most five distinct prime factors and

```text
#Div(S1^2)<=3^5=243.
```

The Jacobi-positive kernel at odd `k=3 mod4` has exactly `phi(k)/2` elements. Saturation therefore requires

```text
phi(k)<=486.
```

Because k is odd, the stronger factorwise bound

```text
phi(k)^2 >= k
```

holds, so the exact finite search need only cover

```text
k<=486^2=236196.
```

## 2. Complete exact closure

For B-, D-, and J-type renewed source characters, the verifier exhausts every persistent pair `(k,q)` inside that rigorous bound and tests the exact seed `lcm(S0(k),q)`.

```text
admissible k with phi(k)<=486: 158
largest such k:                 1155
eligible persistent pairs:      180
  B-type:                         61
  D-type:                         58
  J-type:                         61
multiplicity-one saturations:      0
```

The abstract source enumeration is a superset of actual D-selector realizations.

## 3. Valuation-safe theorem

If q is a materialized renewed source, k is a later destination on its persistent ladder, and exact state proves

```text
v_q(C_k)=1,
```

then

```text
lcm(S0(k),q)
```

is not Jacobi-saturating modulo k.

This theorem does **not** apply merely from knowing `q|C_k`.

The exact valuation theorem now gives

```text
C_j=qA
k=j+4qn
v_q(C_k)=1+v_q(A+n).
```

So multiplicity-one is the explicit phase

```text
n != -A mod q.
```

Higher lifts satisfy

```text
v_q(C_k)>=e <=> k=-p mod4q^e
```

and must be analyzed separately.

## 4. Machine consequence

The safe scheduler rule is

```text
if source_count == 1
and qadic_valuation == 1
and candidate_seed == lcm(S0(k),q):
    multiplicity_one_saturation = IMPOSSIBLE
```

If valuation is `UNKNOWN` or at least2, no pruning permission is granted by this theorem.

The destination itself also remains live for two-source synchronization, richer ancestry, incoming repulsion, exact-state promotion, or direct signed-box geometry.

## 5. Bryan Entanglement Cross boundary

BEC/BREC can label the valuation-one branch as an exact excavated obstruction and higher q-adic subladders as upward expansion. It cannot infer valuation and never supplies proof authority.
