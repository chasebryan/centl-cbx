# h169 k11 t=0 -> persistent k51 shield cycle

**Status:** exact persistence theorem inside the landed k51 Jacobi normal form  
**Date:** 2026-08-17  
**Verifier:** `verify_h169_k11_t0_k51_persistent_shield_cycle.py`  
**Depends on:** `H169-K11-T0-K51-JACOBI-NORMAL-FORM.md`

## 1. The normal form leaves one precise escape mechanism

The landed k51 theorem says that on the h169 k11 child

```text
t mod11=0,
```

we have

```text
C51=55R
```

and

```text
k51 combined miss
iff
every prime-factor occurrence of R lies in H51,
```

where

```text
H51=<11>=ker Jacobi(./51)
```

is the 16-element index-two subgroup of `U(51)`.

That theorem gives a complete support normal form. It also exposes the natural vertical question:

```text
Can repeated valuation at the already-forced prime11 remain inside H51 forever?
```

The answer is yes in the exact local residue machine.

---

## 2. Start from the correct hard-class seed

The selected h169 phase forces

```text
5|C51
11|C51.
```

So the exact starting seed is

```text
[5,11],
```

not `[11]` alone.

Its signed support already contains nine residues of `H51`.

Now repeatedly add another occurrence of the same rational prime11.

The exact U(51) transition is

```text
C' = 11C mod51
S' = S union 11S union 11^(-1)S.
```

---

## 3. H51 saturates after four further copies of11

Starting from `[5,11]`, the support sizes under further factor11 occurrences are

```text
additional 11s     support size
0                  9
1                 11
2                 13
3                 15
4                 16.
```

At four additional copies,

```text
S=H51.
```

Because the seed already contained one forced copy of11, the same statement in valuation language is

```text
v11(C51)=5
->
signed support has saturated H51.
```

This distinction is frozen explicitly by the verifier:

```text
additional factor11 occurrences to saturation = 4
total v11 at saturation                         = 5.
```

---

## 4. After saturation the exact state has period16

Once

```text
S=H51,
```

multiplication by11 merely permutes H51, so the support never changes again.

The center continues to move by

```text
C -> 11C mod51.
```

Since

```text
ord_51(11)=16,
```

the center returns after exactly16 further occurrences.

The verifier checks the full signed-box state, not only the center:

```text
state(additional 11s = 4)
=
state(additional 11s = 20).
```

No shorter positive period closes that saturated state.

Thus the exact local cycle length is

```text
16.
```

---

## 5. Every state on the cycle is a combined miss

The canonical normal form proves that support contained in `H51` is exactly the combined-miss condition on this seeded branch.

Every state on the saturated cycle has

```text
support=H51.
```

Therefore every cycle state is a combined miss.

So local k51 geometry admits

```text
v11=5,6,7,...
```

with an endlessly repeating residue-state pattern.

The precise theorem-safe conclusion is

```text
local k51 signed-box geometry imposes no finite ceiling on v11(C51).
```

This is a local possibility theorem, not an assertion that actual h169 prime corridor candidates realize every valuation.

---

## 6. This identifies the vertical escape carrier

The broad termination picture was

```text
horizontal character dynamics
-> finite state / SCC closure

vertical valuation dynamics
-> possible escape.
```

At k51, the escape is no longer abstract.

It is the exact object

```text
H51=<11>=ker Jacobi(./51)
```

together with the exact valuation cycle

```text
support saturation at total v11=5
then period16 under further factor11 copies.
```

The local automaton has already closed. What remains is a repeatable valuation carrier living inside a protected combined-miss subgroup.

That means a global proof should not waste effort trying to derive a purely local k51 valuation ceiling. The local theorem says such a ceiling is false at the residue-state level.

---

## 7. The simultaneous survivor system now has a sharp target

To terminate this child, another coordinate must puncture the shield.

The target is now concrete:

```text
force some q|R with q notin H51,
```

or equivalently

```text
force Jacobi(q/51)=-1
for some prime q|R.
```

The canonical k51 normal form then immediately converts that puncture into a non-miss.

So the desired contradiction architecture is

```text
earlier/later cofactor obligation
-> outside-H51 prime occurrence in R
-> canonical k51 normal form
-> k51 cannot remain a combined miss.
```

That is a substantially cleaner target than “bound valuation growth somehow.”

---

## 8. Why consecutive-cofactor coupling matters here

The post-k23 ladder is a consecutive affine family. The ten-cofactor separation theorem already says large odd prime support is not freely shared among neighboring letters.

Therefore an outside-H51 puncture cannot simply be borrowed from another cofactor. It must be forced into the k51 residual by phase, reciprocity, character, or affine arithmetic.

This turns the next theorem-mining problem into a simultaneous satisfiability question:

```text
Can R remain entirely H51-supported while the neighboring cofactors
simultaneously satisfy their own exact miss obligations?
```

That is exactly the research direction the obligation machine was built to attack.

---

## 9. Executable verification

Run

```sh
python3 research/verify_h169_k11_t0_k51_persistent_shield_cycle.py
```

It verifies:

```text
the canonical k51 Jacobi normal form,
the correct hard-class seed [5,11],
H51 order16,
first H51 support saturation after four additional 11s,
total v11=5 at saturation,
full support persistence after saturation,
exact state return after16 further copies,
absence of any shorter positive period,
and combined-miss status for every saturated cycle state.
```

---

## 10. Claim boundary

This theorem does not assert arbitrarily large `v11(C51)` is arithmetically realized by h169 prime corridor candidates.

It proves that the local k51 residue machine cannot forbid it.

A global theorem may still eliminate the cycle through ancestry or simultaneous neighboring-cofactor constraints. Indeed, that is now the intended next attack.

No finite Lane-I ceiling or Erdős-Straus proof follows from this persistence theorem alone.
