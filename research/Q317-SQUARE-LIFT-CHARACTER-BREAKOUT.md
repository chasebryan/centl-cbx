# q317 square-lift character breakout

**Status:** exact conditional valuation theorem following the q29 tenth-lift extraction  
**Date:** 2026-08-16  
**Verifier:** `verify_q317_square_lift_character_breakout.py`  
**Depends on:** `D-SELECTOR-Q29-TENTH-LIFT-SATURATION.md`, `Q317-MULTIPLICITY-ONE-SATURATION-IDEMPOTENCE.md`, the Jacobi-saturation lemma, and h169 class-seed arithmetic.  
**Claim boundary:** this theorem classifies two exact q317 square-lift branches conditional on the q29 tenth-lift parent state and its miss-extracted positive q317 character. It is not a universal ancestry theorem, termination theorem, closed decomposition method, or Erdős–Straus proof.

## 1. Why the square lift matters

A miss on the landed q29 tenth-lift branch at k951 forces

```text
(317/p)=+1.
```

The landed multiplicity-one closure then shows that `317^1` can Jacobi-saturate only at

```text
k in {7,11,15,23,31},
```

and every miss at those destinations merely repeats already-controlled h169 character data.

Thus exponent1 is character-idempotent.

The first unresolved question is whether the next valuation layer

```text
317^2 | C_k
```

breaks that loop.

It does.

## 2. Complete exponent-two finite closure

With seed

```text
S_2(k) = lcm(gcd(210,(169+k)/4), 317^2),
```

the h169 class contributes at most four squarefree primes and q317 has exponent2. Hence

```text
#Div(S_2^2) <= 3^4 * 5 = 405.
```

A Jacobi-saturating odd destination requires

```text
phi(k)/2 <= 405,
```

so

```text
phi(k) <= 810.
```

For odd k,

```text
phi(k)^2 >= k,
```

therefore every possible exponent-two saturation lies within the rigorous finite bound

```text
k <= 810^2 = 656100.
```

Exhausting every admissible h169 destination in this bound whose q317 route character is positive gives exactly seven exponent-two saturations:

```text
k = 7, 11, 15, 23, 31, 39, 167.
```

The first five are inherited from exponent1. The genuinely new square-lift destinations are

```text
k39
k167.
```

## 3. k39 is first new-character breakout

At k39,

```text
S0 = gcd(210,(169+39)/4) = 2.
```

The exact residue counts are

```text
seed 2*317      -> 9 residues
seed 2*317^2    -> 12 residues.
```

The Jacobi-positive kernel modulo39 has

```text
phi(39)/2 = 12
```

members, and

```text
DivSq(2*317^2) = H39.
```

Thus exponent2 is the first q317 saturation at k39.

A saturated miss forces

```text
(39/p)=+1.
```

Since

```text
39 = 3*13
```

and h169 fixes

```text
(3/p)=+1,
```

a miss forces

```text
(13/p)=+1.
```

Therefore the square lift has the exact dichotomy

```text
317^2 | C39
    |
    +-- k39 hit  -> exact decomposition certificate
    |
    `-- k39 miss -> positive q13 character.
```

The q13 character is not part of the baseline h169 positive-source alphabet `{7,11,23,31}` used by the multiplicity-one q317 theorem.

## 4. k167 gives a second new source

At prime destination167,

```text
S0 = gcd(210,(169+167)/4) = 42.
```

The exact residue counts are

```text
seed 42*317      -> 61 residues
seed 42*317^2    -> 83 residues.
```

Since

```text
phi(167)/2 = 83,
```

we have

```text
DivSq(42*317^2) = H167.
```

Again exponent2 is minimal.

A saturated miss at prime k167 forces directly

```text
(167/p)=+1.
```

Thus

```text
317^2 | C167
    |
    +-- k167 hit  -> exact decomposition certificate
    |
    `-- k167 miss -> new positive q167 character.
```

## 5. Exact compatibility with the q29 tenth-lift parent

The landed q29 tenth-lift parent phase is

```text
p = 1,077,349,876,531,183,834,133,689
    mod
    1,811,916,098,625,212,549,577,720.
```

For each new square-lift destination impose

```text
p = -k mod 4*317^2.
```

The CRT systems are compatible because the only common factor is4 and every admissible k is3 modulo4.

The primitive combined classes are:

### k39

```text
p = 120,944,665,017,010,843,655,597,365,969
    mod
    182,077,636,834,748,983,894,515,505,080.
```

### k167

```text
p = 47,177,936,809,781,190,337,189,229,329
    mod
    182,077,636,834,748,983,894,515,505,080.
```

At each canonical representative,

```text
v317(C_k)=2
```

exactly.

So the square-lift breakout is arithmetically compatible with the q29 tenth-lift parent state and does not rely on an impossible phase intersection.

Compatibility is not a full survivor-realizability claim.

## 6. Machine consequence

The q317 branch now has a proved valuation grammar:

```text
q317 exponent1:
    hit-capable,
    but every saturated miss is CHARACTER_IDEMPOTENT.

q317 exponent2:
    k39  -> HIT_OR_EXTRACT_13_POSITIVE
    k167 -> HIT_OR_EXTRACT_167_POSITIVE.
```

This is the first exact proof that increasing the valuation of an extracted source can change the **semantic class** of its miss branch from idempotent to source-generating.

A scheduler should therefore never collapse

```text
source q
```

into a valuation-free character node. The valuation coordinate changes what proof-state information a miss can create.

## 7. Bryan Entanglement Cross boundary

An observational BEC history is

```text
right (+): q29 tenth lift extracts q317
left (-):  q317 multiplicity-one miss loops in known character state
up (+/-):  q317 enters its square-lift subphase
right (+): square lift either hits or creates q13/q167.
```

BEC/BREC does not establish saturation, compatibility, or character extraction.

## 8. Next target

Two directions now matter:

1. classify whether q13 or q167 can themselves generate non-idempotent progress at low valuation;
2. test whether the q317 square-lift branches feed back into already-landed h169 phase restrictions strongly enough to reduce the product-state grammar.

The first is a source-recursion question. The second is a state-contraction question. Both are stronger targets than another valuation-free scan.
