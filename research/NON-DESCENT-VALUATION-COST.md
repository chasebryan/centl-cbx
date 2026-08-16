# Non-descent valuation cost

**Status:** exact progress-dichotomy theorem for one-source h169 Jacobi-saturated character transitions.  
**Date:** 2026-08-16  
**Verifier:** `verify_non_descent_valuation_cost.py`  
**Depends on:** `VALUATION-OUTPUT-PRIME-CEILING.md` and `QADIC-PHASE-INDEX-COST.md`.  
**Claim boundary:** this theorem applies to one-source Jacobi-saturated miss transitions with a materialized source q and source valuation e. It does not cover arbitrary multi-source or non-Jacobi exact mechanisms and is not a global termination theorem or Erdős–Straus proof.

## 1. Two landed inequalities

For one routed source q used at valuation e, the output-prime ceiling gives every extractable prime character r the exact upper bound

```text
r <= 324e + 163.
```

The q-adic phase-index theorem gives the valuation-e route shell exact index

```text
I(q,e)=q^(e-1)
```

relative to the multiplicity-one source shell.

These two facts couple output size to arithmetic phase cost.

## 2. Non-descent forces a valuation floor

Suppose a saturated miss produces a prime character r that does not decrease the source modulus:

```text
r >= q.
```

Then

```text
q <= r <= 324e+163.
```

Therefore

```text
e >= (q-163)/324.
```

Since e is a positive integer, define

```text
E_nd(q)
  = max(1, ceil((q-163)/324)).
```

Every non-descending output must satisfy

```text
e >= E_nd(q).
```

Equivalently, if

```text
e < E_nd(q),
```

then every extractable prime character obeys

```text
r < q.
```

So below the non-descent valuation floor, any source-generating miss is a strict prime-modulus descent.

## 3. Exact phase-index lower bound for refusing descent

A valuation-e transition has phase index

```text
q^(e-1).
```

Thus every non-descending transition from q must pay at least

```text
I_nd(q)
  = q^(E_nd(q)-1).
```

That is an exact theorem-level lower bound on the q-adic phase refinement required before a non-descending character output is even arithmetically possible under this mechanism.

The actual transition may require larger e and therefore a larger index.

## 4. Threshold ladder

The first thresholds are immediate:

```text
e=1 -> r <= 487
e=2 -> r <= 811
e=3 -> r <= 1135
e=4 -> r <= 1459
...
```

Hence:

```text
q >= 488  -> valuation1 source generation must descend
q >= 812  -> every source-generating transition with e<=2 must descend
q >= 1136 -> every source-generating transition with e<=3 must descend
q >= 1460 -> every source-generating transition with e<=4 must descend.
```

More generally, under valuation cap E,

```text
q > 324E+163
```

forces strict modulus descent on every generated prime character.

## 5. Examples

### q1009

```text
E_nd(1009)=3.
```

So valuations1 and2 cannot produce a prime character at least1009.

Any non-descending output first becomes possible only at valuation3 or higher, whose phase shell already has index at least

```text
1009^2 = 1,018,081
```

relative to the multiplicity-one route.

### q5003

```text
E_nd(5003)=15.
```

Any non-descending one-source saturated output requires phase index at least

```text
5003^14.
```

The theorem does not claim such an output exists. It says no such output can exist before paying that valuation cost.

### q317

```text
E_nd(317)=1.
```

The theorem does not force q317 to descend at low valuation. The landed q317 machine is therefore correctly handled by exact finite closure instead: exponent1 is character-idempotent and exponent2 generates q13/q167, both smaller than317.

## 6. Bounded-valuation corollary

Fix a valuation cap E.

Every source prime satisfying

```text
q > 324E+163
```

has only two possible outcomes under a one-source Jacobi-saturated transition at valuation at most E:

```text
1. terminal hit, or
2. every generated prime character is strictly smaller than q.
```

So all non-descending character behavior under the cap is confined to the finite small-prime window

```text
q <= 324E+163.
```

The landed bounded-complexity finiteness theorem can then close that finite window into a quotient graph / SCC atlas.

## 7. Infinite-chain consequence

Consider a hypothetical infinite chain of genuinely new prime characters produced only by one-source Jacobi-saturated misses.

If the source valuations were bounded by E, then the character primes would remain in the finite bounded-complexity alphabet and could not remain genuinely new forever.

Therefore any infinite fresh-character chain in this one-source mechanism must use unbounded valuation.

If, in addition, the chain contains infinitely many non-descending steps with unbounded source q, those steps must satisfy

```text
E_nd(q) -> infinity
```

and their required q-adic phase indices

```text
I_nd(q)=q^(E_nd(q)-1)
```

also diverge.

This is a structural cost theorem, not termination: nested q-adic classes can remain nonempty at arbitrarily high index.

## 8. Candidate progress grammar

The theorem supports an exact three-way classification for one-source saturated transitions:

```text
TERMINAL:
    signed-box hit.

DESCENT:
    miss generates only prime characters r<q.

VALUATION_ESCAPE:
    non-descent is possible only after e>=E_nd(q),
    paying phase index at least I_nd(q).
```

Inside any bounded valuation box, only finitely many small q can avoid the descent theorem. Those states can be closed explicitly as finite SCCs.

This is substantially closer to a progress grammar, but still not a well-founded global measure because `VALUATION_ESCAPE` can in principle repeat indefinitely.

## 9. Bryan Entanglement Cross boundary

A qualifying `DESCENT` is a natural proved constructive/rightward event with decreasing source modulus. A `VALUATION_ESCAPE` is a natural upward expansion whose exact cost is q-adic phase refinement.

BEC/BREC names the observed transition type after proof. The inequalities and lattice index establish it.

## 10. Next target

The remaining obstruction to a genuine termination rank is now sharply isolated:

> Can valuation escape continue indefinitely on a surviving exact ancestry branch?

The best current route is to couple high valuation to early signed-box ancestry. If sufficiently high valuation forces one of the exact k3/k7/k11/k15 survivor grammars to fail, then the vertical escape axis would acquire a branch-local cap and the present dichotomy could become a true termination argument on that domain.
