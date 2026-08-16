# q13 / q167 source semantic split

**Status:** exact multiplicity-one source-classification theorem following the q317 square-lift breakout  
**Date:** 2026-08-16  
**Verifier:** `verify_q13_q167_source_semantic_split.py`  
**Depends on:** `Q317-SQUARE-LIFT-CHARACTER-BREAKOUT.md`, h169 class-seed arithmetic, the Jacobi-saturation lemma, and the landed h169 positive-source/phase state.  
**Claim boundary:** exact multiplicity-one routing consequences for the two positive characters extracted by the q317 square lift. Higher valuations, additional routed factors, and full ancestry remain separate live states. This is not a termination theorem or Erdős–Straus proof.

## 1. Two outputs of the same parent mechanism

The q317 square-lift theorem has two source-generating miss branches:

```text
k39 miss  -> (13/p)=+1
k167 miss -> (167/p)=+1.
```

Both are new positive-character consequences of the q317 exponent-two state.

They do **not** behave the same way when routed again.

## 2. Complete multiplicity-one q13 closure

For one routed copy of q13, the seed is

```text
S13(k) = lcm(gcd(210,(169+k)/4),13).
```

As in the other multiplicity-one closures, the seed has at most five distinct primes, so saturation requires

```text
phi(k)<=486,
k<=486^2=236196
```

for odd admissible k.

The complete exact q13 route closure contains

```text
69 compatible low-totient route shifts
```

and exactly three multiplicity-one saturations:

```text
k=3
k=23
k=55.
```

Their miss outputs are all already controlled:

```text
k3  -> (3/p)=+1         hard-class character
k23 -> (23/p)=+1        landed h169 source
k55 -> (55/p)=+1        product of already-controlled (5/p) and (11/p)
```

Therefore q13 is **character-idempotent under multiplicity-one Jacobi saturation**.

But q13 is not useless. The positive q13 character itself contracts the landed k39 h169 phase state. Since

```text
p = 8t mod13
```

with 8 a quadratic nonresidue, `(13/p)=+1` restricts the landed k39 survivor set

```text
{1,2,5,6,7,8,9,10,11}
```

to

```text
{2,5,6,7,8,11}.
```

Thus q13 is best classified as

```text
PHASE_CONTRACTING + MULTIPLICITY_ONE_IDEMPOTENT.
```

## 3. Complete multiplicity-one q167 closure

For one routed copy of q167,

```text
S167(k) = lcm(gcd(210,(169+k)/4),167).
```

The same rigorous multiplicity-one bound applies:

```text
phi(k)<=486,
k<=236196.
```

The complete exact q167 route closure contains

```text
79 compatible low-totient route shifts
```

and exactly four multiplicity-one saturations:

```text
k=15
k=23
k=71
k=111.
```

The first two are miss-side idempotent:

```text
k15 -> (15/p)=+1 from already-controlled 3 and5 characters
k23 -> (23/p)=+1 already landed.
```

The other two generate new positive characters.

### k71

Since 71 is prime, a saturated miss forces directly

```text
(71/p)=+1.
```

### k111

Since

```text
111=3*37
```

and h169 fixes `(3/p)=+1`, a saturated miss forces

```text
(37/p)=+1.
```

Therefore q167 is **source-generating already at multiplicity one**:

```text
q167
  -> k71  : HIT_OR_EXTRACT_71_POSITIVE
  -> k111 : HIT_OR_EXTRACT_37_POSITIVE.
```

## 4. Compatibility with the q317-square parent branches

The q317 square-lift parent classes are exact arithmetic progressions.

The q13 route conditions for k3,k23,k55 and the q167 route conditions for k15,k23,k71,k111 each impose one additional congruence

```text
p = -k mod 4q.
```

Every such system is CRT-compatible with its corresponding q317-square parent progression. The common factor4 is consistent because all named destinations are3 modulo4, while the odd source prime is coprime to the parent modulus.

Thus the semantic split is not produced by incompatible route fantasies. Each classified child route has a nonempty exact arithmetic progression beneath its q317-square parent state.

This is compatibility only, not full survivor realizability.

## 5. Machine taxonomy

The three-source chain now exhibits three distinct semantic classes:

```text
q13:
    PHASE_CONTRACTING
    MULTIPLICITY_ONE_IDEMPOTENT

q167:
    MULTIPLICITY_ONE_SOURCE_GENERATING

q317:
    VALUATION_SENSITIVE
    e=1 -> CHARACTER_IDEMPOTENT
    e=2 -> SOURCE_GENERATING
```

So the scheduler must not rank sources only by presence or count. It should record what exact proof-state change a source can produce at the current valuation.

A useful theorem-bearing event vocabulary is

```text
TERMINAL_HIT
PHASE_CONTRACTION
SOURCE_GENERATION
CHARACTER_IDEMPOTENCE
VALUATION_EXPANSION
SATURATION_BARRIER.
```

These are semantic consequences of proved arithmetic transitions. They are not yet a well-founded progress measure.

## 6. Bryan Entanglement Cross boundary

This theorem gives the draft Cross a concrete observational distinction:

```text
q13  : right (+) through phase contraction, then local loop/left at multiplicity one
q167 : right (+) through immediate source generation
q317 : left at e1, up (+/-) into valuation, then right (+) at e2
```

BEC/BREC does not determine any classification above. The exact finite closures and character identities do.

## 7. Next target

The next mathematical target is to test whether q71 and q37 continue source growth or become idempotent. If the source-generation chain repeatedly enters a finite semantic alphabet, that may expose a cycle theorem. If it keeps forcing genuinely new prime-character sources, then the next task is to prove a bounded resource or a compulsory signed-box exit.
