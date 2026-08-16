# q317 descendant character automaton through valuation two

**Status:** exact finite one-source Jacobi-saturation closure for valuations 1 and 2 in the h169 state.

**Claim boundary:** this closes only one-source character outputs at exact source valuation `e<=2`. Higher valuations, simultaneous sources, affine/support renewal, exact-state promotion, incoming repulsion, and direct signed-box geometry remain live. It is not a termination theorem or an Erdős–Straus proof.

## Closed alphabet

Starting from the landed q317 square-lift outputs and recursively applying complete one-source closures at valuations 1 and 2 gives exactly

```text
A2 = {13,19,37,47,71,167}.
```

No such transition from a source in A2 produces a prime character outside A2.

The exact source-generation graph is

```text
13  -> {}
19  -> {71,167}
37  -> {47,71}
47  -> {13}
71  -> {13}
167 -> {13,19,37,71}.
```

The only nontrivial strongly connected component is

```text
{19,167}
```

through the exact miss-side cycle

```text
167^2 at k95  -> 19
19^2  at k167 -> 167.
```

Once both positive characters are known, replaying that component adds no new character information.

## Complete closures

The verifier exhausts the rigorous finite bounds supplied by the valuation/output ceiling theorem.

```text
q13:
 e1 routes 69,  saturations {3,23,55}
 e2 routes 120, saturations {3,23,27,35,55}

q19:
 e1 routes 76,  saturations {3,15,27,31}
 e2 routes 122, saturations {3,15,27,31,71,167}

q37:
 e1 routes 77,  saturations {3,7,11,27,71}
 e2 routes 130, saturations {3,7,11,27,47,71}

q47:
 e1 routes 79,  saturations {11,15,31}
 e2 routes 124, saturations {11,15,31,39}

q71:
 e1 routes 76,  saturations {7,11,23,31}
 e2 routes 125, saturations {7,11,23,31,39,55}

q167:
 e1 routes 79,  saturations {15,23,71,111}
 e2 routes 137, saturations {15,23,35,39,71,95,111}.
```

Composite outputs reduce using already-fixed h169 characters:

```text
39  = 3*13  -> q13
95  = 5*19  -> q19
111 = 3*37  -> q37.
```

All other named new outputs are prime destinations q47, q71, or q167, or are already-controlled hard/source characters.

## Machine consequence

After every character in A2 is known, set

```text
VAL2_CHARACTER_FIXED_POINT = true.
```

Repeated valuation-1/2 one-source character routing inside A2 must not be counted as progress. The `{19,167}` SCC should be quotient-collapsed.

This proves that source count alone cannot be a progress measure.

The next possible escape is valuation 3. A preliminary exact closure identifies the first new prime outside A2 through

```text
q71^3 at k51 -> q17,
```

because `51=3*17` and h169 fixes the q3 character.

## Bryan Entanglement Cross boundary

BEC/BREC may annotate SCC looping and fixed-point closure after the arithmetic theorem is established. It has no proof or pruning authority.
