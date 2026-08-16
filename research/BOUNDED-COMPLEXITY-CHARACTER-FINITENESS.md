# Bounded-complexity character finiteness

**Status:** exact structural theorem for the h169 Jacobi-saturation source machine  
**Date:** 2026-08-16  
**Verifier:** `verify_bounded_complexity_character_finiteness.py`  
**Depends on:** `VALUATION-OUTPUT-PRIME-CEILING.md`.  
**Claim boundary:** this theorem applies to Jacobi-saturated transitions whose mandatory seed consists of the h169 class seed plus at most a fixed number of routed prime powers with bounded valuations. It does not bound arbitrary affine reservoir renewal, exact-state promotion, direct signed-box mechanisms, or unbounded valuation/source arity. It is not a termination theorem or Erdős–Straus proof.

## 1. Fixed complexity class

Fix integers

```text
m >= 0
E >= 1.
```

Consider h169 Jacobi-saturation transitions whose mandatory seed has the form

```text
S = lcm(S0(k), q1^e1, ..., qs^es)
```

with

```text
s <= m,
1 <= ei <= E,
S0(k)=gcd(210,(169+k)/4).
```

The h169 class seed is squarefree and has at most four distinct prime factors.

Therefore

```text
#Div(S^2)
 <= 3^4 * product_i(2ei+1)
 <= 81(2E+1)^m.
```

## 2. Finite destination theorem

If S Jacobi-saturates an admissible odd destination k, then

```text
phi(k)/2 <= #Div(S^2),
```

so

```text
phi(k) <= B(m,E),
```

where

```text
B(m,E) = 162(2E+1)^m.
```

Because every admissible k is odd and

```text
phi(k)^2 >= k,
```

we obtain the absolute destination ceiling

```text
k <= B(m,E)^2.
```

Thus the set of possible Jacobi-saturating destinations in any fixed `(m,E)` complexity class is finite.

## 3. Finite output-character theorem

Every prime character r that can be extracted from a saturated miss divides k. Hence

```text
r-1 <= phi(k) <= B(m,E),
```

and therefore

```text
r <= B(m,E)+1.
```

So every newly extracted prime character belongs to the finite set

```text
P(m,E) = {prime r : r <= 162(2E+1)^m + 1}.
```

This bound is independent of the sizes of the incoming routed source primes.

## 4. Recursive fixed-point corollary

Start from any finite positive-character source alphabet A0.

Repeatedly apply only h169 Jacobi-saturated transitions with

```text
source arity <= m
source valuations <= E.
```

Every newly generated prime character lies in `P(m,E)`. Therefore the full recursive alphabet is contained in

```text
A0 union P(m,E),
```

which is finite.

Consequently a bounded-complexity character-generation process cannot create infinitely many distinct prime characters.

If it runs indefinitely without a terminal hit, it must eventually revisit already-known character state and enter a finite fixed point or strongly connected component.

This is a theorem about the **character alphabet**, not about the full arithmetic state.

## 5. Escape dichotomy

Any hypothetical branch that creates infinitely many genuinely new prime characters through the broader candidate framework must eventually do at least one of the following:

```text
1. use unbounded source valuation;
2. use unbounded simultaneous routed-source arity;
3. leave the bounded Jacobi-saturation mechanism through another exact transition family.
```

The third category includes, for example,

```text
affine/support renewal,
exact-state promotion,
incoming repulsion,
direct Type-I/Type-II signed-box geometry.
```

So fresh-character infinity cannot hide inside a bounded `(m,E)` Jacobi routing box.

## 6. Concrete examples

### Multiplicity one

For

```text
m=1, E=1,
```

```text
B=486,
output prime <=487,
k<=236196.
```

This is the exact bound used by the landed multiplicity-one closures.

### One source through valuation two

For

```text
m=1, E=2,
```

```text
B=810,
output prime <=811,
k<=656100.
```

The landed q317 descendant valuation-two fixed point

```text
{13,19,37,47,71,167}
```

lies entirely inside this finite output alphabet.

### Two multiplicity-one sources

For

```text
m=2, E=1,
```

```text
B=1458,
k<=2125764,
output prime<=1459.
```

This recovers the exact two-source cardinality ceiling used by the landed synchronization barrier.

## 7. Machine consequence

The proof state may attach a bounded-complexity box

```text
CHAR_ARITY_CAP = m
CHAR_VALUATION_CAP = E
CHAR_PHI_CEILING = B(m,E)
CHAR_DESTINATION_CEILING = B(m,E)^2
CHAR_OUTPUT_PRIME_CEILING = B(m,E)+1.
```

Within a fixed box, the scheduler can quotient repeated character states into SCCs. It should not count repeated visits as progress.

If a branch escapes the finite character box by raising valuation or arity, that increase must be represented explicitly in proof state.

## 8. Bryan Entanglement Cross boundary

The theorem gives the draft Cross a rigorous interpretation rule:

```text
bounded rightward character propagation -> finite semantic closure;
continued fresh expansion -> must pay an upward complexity move or switch mechanisms.
```

BEC/BREC remains observational metadata. The finiteness theorem comes from divisor cardinality, totient bounds, and explicit complexity caps.

## 9. Toward a progress measure

This theorem still does not supply a well-founded global ordinal.

What it does supply is a sharp reduction of possibilities:

```text
bounded complexity -> finite quotient graph;
unbounded escape   -> explicit valuation/arity growth or another exact mechanism.
```

The next target is to quantify the arithmetic cost of an upward complexity move. For q-adic valuation, that cost is already encoded by nested congruence sublattices modulo powers of q. Coupling finite SCC closure to that exact phase cost is the most promising current route toward a genuine progress measure.
