# Valuation-to-output-prime ceiling

**Status:** exact cardinality/descent theorem for h169 Jacobi-saturated source transitions  
**Date:** 2026-08-16  
**Verifier:** `verify_valuation_output_prime_ceiling.py`  
**Depends on:** h169 class-seed arithmetic, the Jacobi-saturation lemma, and explicit q-adic source valuation state.  
**Claim boundary:** this theorem bounds destinations and extractable character primes for Jacobi-saturated transitions built from the h169 class seed plus a fixed number of routed source powers. It does not prove that saturation occurs, does not cover arbitrary extra ancestry factors, and is not a termination theorem or Erdős–Straus proof.

## 1. The h169 class seed has bounded squarefree complexity

For every admissible shift `k=3 mod4`, the h169 mandatory class seed is

```text
S0(k) = gcd(210,(169+k)/4).
```

Because

```text
210 = 2*3*5*7
```

is squarefree, `S0(k)` is squarefree and has at most four distinct prime factors.

This fixed four-prime ceiling is the combinatorial input.

## 2. One routed source at valuation e

Let q be one additional routed prime source, with exact known valuation

```text
q^e | C_k,
e>=1.
```

Use the mandatory seed

```text
S = lcm(S0(k),q^e).
```

The square `S^2` has at most

```text
3^4 * (2e+1)
```

divisors.

If q overlaps the class seed the actual number is smaller, so this remains a valid upper bound.

Therefore the divisor-square residue set satisfies

```text
|DivSq(S)| <= 81(2e+1).
```

If S is Jacobi-saturating modulo k, then this residue set must equal the positive Jacobi kernel. Since `k=3 mod4`, the Jacobi character is nontrivial and

```text
|H_k| = phi(k)/2.
```

Hence every one-source valuation-e saturation obeys

```text
phi(k) <= 162(2e+1).
```

Define

```text
Phi_e = 162(2e+1).
```

Then saturation forces

```text
phi(k) <= Phi_e.
```

## 3. Exact destination ceiling

For every odd integer k,

```text
phi(k)^2 >= k.
```

A prime-power proof is immediate. For an odd prime power `p^a`,

```text
phi(p^a)^2 / p^a
 = p^(a-2)(p-1)^2
 >= 1,
```

including `a=1` because `(p-1)^2>=p` for every odd prime p. Multiplying over coprime prime powers proves the inequality for every odd k.

Therefore a one-source valuation-e Jacobi saturation must lie below the absolute finite ceiling

```text
k <= Phi_e^2
  = [162(2e+1)]^2.
```

This turns every fixed-valuation one-source saturation question into a finite exact closure problem.

## 4. Output-prime ceiling

Suppose a saturated miss at k allows one or more prime characters to be extracted from the factorization of k.

Every such extracted prime r divides k. Therefore

```text
r-1 <= phi(k).
```

Combining with the saturation bound gives

```text
r <= Phi_e + 1
  = 162(2e+1)+1
  = 324e+163.
```

Thus:

> **Any prime character extracted by a one-source h169 Jacobi-saturated transition at source valuation e is at most `324e+163`.**

The bound is independent of the incoming source prime q.

It also applies to each prime in a multi-character product output, because every such prime divides k.

## 5. Conditional prime-modulus descent

The output ceiling immediately gives a genuine local descent criterion.

If the incoming source prime satisfies

```text
q > 324e+163,
```

then every newly extractable prime character r satisfies

```text
r < q.
```

So on any one-source valuation-e saturated miss satisfying that threshold, source-character generation is strictly descending in prime modulus.

This is a real theorem-backed descent statement.

It is **not** a global termination measure because:

- many productive transitions have q below the threshold;
- valuation e may grow;
- multi-source transitions have a larger combinatorial budget;
- exact-state mechanisms need not be Jacobi-saturation transitions;
- a branch can hit constructively instead of extracting a new character.

But the machine may safely mark the qualifying transition as

```text
PRIME_MODULUS_DESCENT = true.
```

## 6. Multiple routed sources

The same argument extends cleanly.

Suppose m distinct routed primes enter the mandatory seed with exact valuations

```text
q_1^e1, ..., q_m^em.
```

Then

```text
S = lcm(S0(k),q_1^e1,...,q_m^em)
```

has

```text
#Div(S^2)
 <= 3^4 * product_i (2e_i+1).
```

Therefore Jacobi saturation forces

```text
phi(k)
 <= 162 * product_i (2e_i+1),
```

and consequently

```text
k
 <= [162 * product_i (2e_i+1)]^2.
```

Every extracted prime character r obeys

```text
r
 <= 162 * product_i (2e_i+1) + 1.
```

This multi-source form explains why the multiplicity-one two-source closure was finite and gives the exact valuation-aware replacement for its exponent-one bound.

## 7. Known transitions fit the theorem

### q317 square lift

At e=2,

```text
r <= 324*2+163 = 811.
```

The landed new outputs

```text
13
167
```

obey the ceiling.

### q29 tenth lift

At e=10,

```text
r <= 324*10+163 = 3403.
```

The landed miss-extracted source

```text
317
```

obeys the ceiling.

These examples do not saturate the bound; they are consistency checks, not sharpness claims.

## 8. Machine consequence

A valuation-aware source transition can now carry exact cardinality metadata:

```text
SOURCE_VALUATION = e
SATURATION_PHI_CEILING = 162(2e+1)
SATURATION_K_CEILING = [162(2e+1)]^2
OUTPUT_PRIME_CEILING = 324e+163
```

For multiple sources replace `(2e+1)` by the product of the valuation factors.

The scheduler gains two proof-safe uses:

1. **finite closure:** enumerate every possible saturating destination at fixed valuation;
2. **conditional descent:** if incoming q exceeds the output ceiling, any miss-generated source prime is strictly smaller.

This is stronger than a heuristic preference for small destinations. It is an exact consequence of seed complexity.

## 9. Bryan Entanglement Cross boundary

BEC/BREC can annotate a qualifying source transition as constructive rightward progress with a proved descending modulus, or annotate increasing valuation as upward expansion that raises the output ceiling.

The arrow is not the descent theorem. The divisor cardinality, totient bound, and source valuation are.

## 10. Next target

The natural next question is whether repeated source-generation chains can be partitioned into:

```text
A. descent transitions: q > output ceiling,
B. bounded small-prime states: q <= output ceiling,
C. valuation-expansion transitions that pay an exact q-adic phase contraction.
```

If the bounded small-prime states can be finitely closed and every valuation expansion carries a well-founded phase cost, those two ingredients could begin to support an actual progress measure for the candidate decomposition framework.
