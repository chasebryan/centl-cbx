# k195 double-square corridor: exact k3/k7/k11 ancestry survivor grammar

**Status:** exact range-free early signed-box grammar  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_early_ancestry_survivor_grammar.py`  
**Depends on:** `K195-PRE55-ANCESTRY-PHASE-ENVELOPE.md`, exact signed-box semantics, and h169 companion arithmetic.  
**Claim boundary:** exact necessary-and-sufficient local miss grammars at k3 and k7, plus the complete exact endpoint miss atlas at k11 for the double-square phase envelope. This does not yet prove that the joint three-companion grammar is empty, and does not prove full reachability or non-reachability of k195.

## 1. The first three companions form a fresh local ladder

For h169

```text
p = 169 + 840t.
```

The first three admissible companions are

```text
C3  = (p+3)/4  = 43 + 210t
C7  = (p+7)/4  = 44 + 210t = C3+1
C11 = (p+11)/4 = 45 + 210t = C3+2.
```

Since C3 is odd,

```text
gcd(C3,C7)=1
gcd(C7,C11)=1
gcd(C3,C11)=gcd(C3,2)=1.
```

So k3, k7, and k11 draw on **three pairwise-coprime factor reservoirs**. An early survivor cannot recycle a prime factor from one of these companions into another.

This is the small-k analogue of the later support-renewal ladder.

## 2. Exact k3 theorem

Modulo3,

```text
C3 = 1.
```

The Type-I and Type-II targets coincide:

```text
-4^(-1) = -C3 = 2 mod3.
```

Every prime factor of C3 is a unit modulo3.

### Theorem

```text
k3 misses
iff
every rational prime factor q|C3 satisfies q=1 mod3.
```

Proof:

- if any q=2 mod3 divides C3, q itself is a divisor of `C3^2` and realizes the target2;
- if every q=1 mod3, every divisor of `C3^2` is1 mod3, so target2 is absent.

Thus k3 survival is an exact positive-support law, not a census observation.

## 3. Exact k7 theorem

Modulo7,

```text
C7 = 2.
```

Again the Type-I and Type-II targets coincide:

```text
-4^(-1) = -C7 = 5 mod7.
```

The quadratic residues are

```text
QR7={1,2,4},
```

and the nonresidues are `{3,5,6}`.

Because `C7=2 mod7` is QR, the total number of nonresidue prime-factor occurrences in C7, counted with multiplicity, is even.

### Theorem

k7 misses if and only if **one** of the following two exact factor grammars holds.

### QR7 sector

```text
every prime factor q|C7 lies in QR7.
```

Then every divisor residue of `C7^2` is QR and target5 is absent.

### Thin 3-sector

After deleting all prime-factor occurrences congruent to1 modulo7, the remaining occurrence multiset is exactly

```text
{3,3}.
```

Equivalently:

- exactly two prime-factor occurrences are3 mod7;
- every other occurrence is1 mod7.

The exact divisor mask is then

```text
{1,2,3,4,6},
```

which omits only the target5.

### Why there are no other misses

- residue5 is an immediate target;
- any occurrence6 combined with the necessary remaining center2 support creates5;
- three or more occurrences3 fill the target;
- after the exact `{3,3}` skeleton, any nontrivial QR residue2 or4 also fills5.

The complete finite residue-state closure has exactly two miss masks at final center2:

```text
{1,2,4}
{1,2,3,4,6}.
```

These correspond exactly to the two factor grammars above.

## 4. k11 depends on the moving tau11 coordinate

For h169,

```text
C11 = t+1 mod11.
```

The fixed Type-I target is

```text
-4^(-1)=8 mod11,
```

while the Type-II target is

```text
-C11 mod11.
```

The landed corrected k195 pre-55 envelope allowed

```text
tau11 in {0,2,3,4,8,9}.
```

The complete exact k11 factor-residue closure contains 59 states. Restricting to the corresponding final centers gives the following exact miss atlas.

### tau11=0, center1, Type-II target10

```text
{1}
{1,2,3,4,6}
{1,3,4,5,9}
```

### tau11=2, center3, Type-II target8

```text
{1,3,9}
{1,3,4,5,9}
{1,3,6,7,9}
{1,2,3,4,5,6,7,9,10}
```

### tau11=3, center4, Type-II target7

```text
{1,4,5}
{1,3,4,5,9}
```

### tau11=4, center5, Type-II target6

```text
{1,3,5}
{1,2,3,5,7}
{1,3,4,5,9}
```

### tau11=8, center9, Type-II target2

```text
{1,4,9}
{1,3,4,5,9}
```

### tau11=9, center10, Type-II target1

```text
NO MISS STATES.
```

Therefore the new exact ancestry theorem is

```text
tau11=9 -> k11 always hits.
```

This is range-free.

## 5. The common QR11 state

The mask

```text
QR11={1,3,4,5,9}
```

appears as a miss at every surviving k11 center

```text
1,3,4,5,9.
```

So QR11-only factor support is a common k11 obstruction family whenever C11 itself is QR11.

The remaining miss masks are thinner exact states. Across the five live tau11 phases there are

```text
14 center-labelled miss states
10 distinct masks.
```

This finite k11 atlas is the correct proof-state coordinate for the next ancestry coupling. It should not be compressed into a false single QR iff theorem.

## 6. Improved exact phase contraction

The previous pre-55 envelope had six allowed tau11 phases.

The k11 theorem removes tau11=9, leaving

```text
tau11 in {0,2,3,4,8}.
```

The exact s-period remains

```text
116,831 = 19*13*43*11.
```

The phase-live count therefore improves from

```text
8*9*40*6 = 17,280
```

to

```text
8*9*40*5 = 14,400.
```

So the exact phase fraction not yet excluded becomes

```text
14,400 / 116,831
= 0.1232549580162799...
```

and the proved elimination becomes about

```text
87.6745%.
```

If a state reaches k195, the tau13 selector still splits these 14,400 classes exactly into

```text
4,800 guaranteed-k195-hit classes
9,600 k195-miss-compatible classes.
```

## 7. Normalized early ancestry state

A double-square state surviving k3,k7,k11 must now carry

```text
EARLY = (
  C3_support = ONE_MOD3,
  C7_mode in {QR7, THIN_33},
  tau11 in {0,2,3,4,8},
  k11_mask in exact_endpoint_atlas(tau11),
  pairwise_disjoint_support(C3,C7,C11)
).
```

This is a genuine finite survivor grammar, not a first-hit histogram.

Before k15 is examined, the original huge double-square corridor has already been replaced by:

- one exact k3 support law;
- two exact k7 modes;
- fourteen center-labelled k11 endpoint states;
- five live tau11 phases;
- three pairwise-disjoint early factor reservoirs.

## 8. Relation to the deterministic prefix audit

The finite `0<=s<1000` audit found 31 corridor primes and all hit by k11 or earlier.

This theorem explains the structural pressure behind that observation without universalizing the finite sample.

The next question is now sharply defined:

> Are any of the 28 formal `k7 mode × k11 endpoint` combinations arithmetically realizable simultaneously with the k3 support law and the later D-selector q41/q37 double-square constraints?

If not, k195 is ancestry-dead by k11. If yes, those exact combinations are the only states that deserve k15+ analysis.

## 9. Bryan Entanglement Cross boundary

This is a stronger downward excavation than the phase shell alone: exact signed-box semantics convert a large search corridor into a small support/mask grammar.

BEC/BREC can annotate the contraction, but the factor-support and residue-state theorems remain the sole proof authority.
