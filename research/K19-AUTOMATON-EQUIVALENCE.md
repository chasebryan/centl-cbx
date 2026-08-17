# k=19 automaton equivalence

**Status:** exact implementation-equivalence theorem  
**Date:** 2026-08-17  
**Scope:** local signed-box state space modulo 19  
**Claim boundary:** implementation/state theorem only; not an Erdős–Straus proof

## 1. Two independent implementations

The current CBX research branch contains two independently written descriptions of the exact `k=19` signed-box state space.

### Full BREC cyclic closure

`verify_k19_brec_state_compression.py` starts from

```text
(c,S)=(0,{0})
```

and allows every valuation atom in `Z/18Z`, retaining states whether or not Type II has already hit.

It finds

```text
439 exact reachable states.
```

### Type-II-miss residue automaton

`classify_signed_box_residue_automaton.py` uses the same cyclic exponent language but prunes a transition as soon as exponent `9`, the `-1` target, enters the support.

Because signed support is monotone under adding factors, a Type-II hit can never disappear. This pruning is exact.

The unseeded q19 automaton therefore enumerates exactly the states that can still miss Type II.

---

## 2. Exact equivalence result

The independent closures agree state-for-state.

Filtering the 439-state full closure by

```text
9 not in S
```

gives exactly

```text
254 states.
```

The independently generated Type-II-miss automaton also gives exactly

```text
254 states.
```

Not only the count, but every `(c,S)` identity is the same.

The minimal canonical depth of every one of the 254 states also agrees between the two BFS implementations.

---

## 3. Second-target split

Inside the Type-II-miss closure the moving Type-I target exponent is

```text
7-c mod 18.
```

The exact 254-state split is

```text
136 combined misses
118 Type-I-only states.
```

The full BREC implementation's `is_combined_miss(c,S)` predicate selects exactly the same 136 state identities as the generic automaton's independently computed second-target test.

Thus there are three separate identities being cross-checked:

```text
Type-II-miss state set identity,
minimal canonical-depth identity,
combined-miss state identity.
```

All three agree exactly.

---

## 4. Why this matters

The two implementations were built for different research purposes.

The full 439-state closure is useful for describing every exact k19 state and proving the small canonical-state bound.

The 254-state automaton is useful for theorem search because Type-II construction can be pruned monotonically and the remaining states can be conditioned on forced seeds or arithmetic branches.

Agreement between them reduces the chance that a subtle state encoding or target formula error is being propagated through the current q23/k19 research.

It also makes the counts interpretable without ambiguity:

```text
439  all exact cyclic states
254  exact states still missing Type II
136  exact states missing both Type II and Type I
118  exact Type-I-only states inside the Type-II-miss closure.
```

---

## 5. Arithmetic realization remains separate

The 254-state automaton is a local residue/multiplicity universe.

It does not imply that every state occurs for

```text
C19=(p+19)/4
```

with `p` prime, much less for a prime that also satisfies the first four BREC obstruction coordinates and the q23 Type-I-only rescue normal form.

That distinction is now central:

```text
abstract exact state reachability
        !=
arithmetic realization in the q23 corridor.
```

The current frontier analyzers are designed precisely to measure the second set inside the first without conflating them.

---

## 6. Executable cross-check

Run

```sh
python3 research/verify_k19_automaton_equivalence.py
```

The verifier:

1. rebuilds the full 439-state closure;
2. filters it by absence of exponent 9;
3. independently rebuilds the generic Type-II-miss closure using the other module's transition implementation;
4. compares all 254 state identities;
5. compares all minimal BFS depths;
6. compares the 136 combined-miss identities;
7. checks the public generic automaton summary against the reconstructed closure.

This is intentionally redundant exact computation.

---

## 7. Claim boundary

This result proves equivalence of two exact finite-state implementations at modulus 19.

It does not prove that all 254 local states are arithmetically realizable, does not make finite non-realization universal, does not create a Lane-I ceiling, and does not prove Erdős–Straus.
