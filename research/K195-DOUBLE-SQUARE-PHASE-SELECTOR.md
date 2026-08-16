# k195 double-square valuation selector

**Status:** exact conditional fixed-shift selector inside the h169 / Route-B D-selector laboratory  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_double_square_phase_selector.py`  
**Depends on:** the Route-B k27 D-selector factor grammar, mixed-character reservoir witnesses, companion-source character conservation, persistent-source q-adic valuation ladder, Jacobi-kernel saturation lemma, and the landed k39 phase survivor set.  
**Claim boundary:** this is a conditional fixed-shift and phase-contraction theorem. It does not prove that a prime reaches k195 under full ancestry, does not prove termination, and does not prove Erdős–Straus.

## 1. The first quadratic two-source gate

On the realized Route-B D-selector state write

```text
p = 169 + 840t,
t = 705 + 1081u,
u = 3631 + 4743v.
```

Hence

```text
t = 3,925,816 + 5,127,183 v.
```

The D and J reservoirs are

```text
D = 5 + 21t,
J = 9 + 35t.
```

The mixed-character renewal theorem permits materialized witnesses

```text
q_D = 41,
q_J = 37,
```

because

```text
(41/31)=+1, (41/17)=-1,
(37/47)=+1, (37/31)=-1.
```

At

```text
k = 195
```

the two persistent ladders synchronize at their first positive route index:

```text
(195-31)/4 = 41,
(195-47)/4 = 37.
```

Thus, whenever 41 is materialized in D and 37 is materialized in J, both sources enter `C195`.

## 2. Exact double-square lift phase

For h169,

```text
C195 = (p+195)/4 = 91 + 210t.
```

Since 210 is invertible modulo both `41^2` and `37^2`, the square-lift conditions are unique phases:

```text
41^2 | C195  <=>  t = 728 mod 1681,
37^2 | C195  <=>  t = 319 mod 1369.
```

Inside the Route-B D-selector progression

```text
t = 3,925,816 + 5,127,183 v,
```

these combine to the single exact phase

```text
v = 1,447,809 mod (41^2 * 37^2)
  = 1,447,809 mod 2,301,289.
```

So the double-square lift is a genuine q-adic sublattice, not an assumed multiplicity.

## 3. Minimal saturation threshold

The mandatory h169 class seed at k195 is

```text
S0 = gcd(210,(169+195)/4) = 7.
```

The relevant seeds are therefore

```text
S11 = 7 * 41   * 37,
S21 = 7 * 41^2 * 37,
S12 = 7 * 41   * 37^2,
S22 = 7 * 41^2 * 37^2.
```

Modulo195,

```text
phi(195)=96,
|H195|=48,
```

where `H195` is the Jacobi-positive kernel.

Exact divisor-square residue counts are

```text
|DivSq(S11)| = 24,
|DivSq(S21)| = 35,
|DivSq(S12)| = 36,
|DivSq(S22)| = 48.
```

The first three do not equal `H195`. The last does:

```text
DivSq(S22) = H195.
```

Thus **both** source valuations must reach at least two before this particular seed saturates. The gate is genuinely quadratic in both sources.

Moreover

```text
Jacobi(7/195)=Jacobi(41/195)=Jacobi(37/195)=+1.
```

Once `S22` fills `H195`, increasing either source exponent cannot leave the positive kernel and cannot remove already-realized residues. Therefore every seed

```text
7 * 41^a * 37^b,  a>=2, b>=2,
```

is also Jacobi-saturating modulo195.

## 4. Saturated miss forces the q13 character

The Jacobi-saturation theorem says that a k195 miss can occur only if every prime factor of `C195` has positive Jacobi character modulo195. Equivalently the target prime must satisfy

```text
(195/p)=+1.
```

Since

```text
195 = 3 * 5 * 13
```

and the h169 class fixes

```text
(3/p)=+1,
(5/p)=+1,
```

a saturated k195 miss forces exactly

```text
(13/p)=+1.
```

If `(13/p)=-1`, k195 must contain an exact signed-box hit.

## 5. One-third contraction of the landed k39 survivor phases

For h169,

```text
p = 169 + 840t = 8t mod13.
```

The residue8 is a quadratic nonresidue modulo13. Therefore

```text
(13/p) = -(t/13)
```

for nonzero `t mod13`.

The landed k39 theorem permits exactly

```text
S39 = {1,2,5,6,7,8,9,10,11} mod13.
```

On these nine phases:

```text
t mod13 in {1,9,10}
    -> (13/p)=-1
    -> double-square k195 MUST HIT.

 t mod13 in {2,5,6,7,8,11}
    -> (13/p)=+1
    -> character-compatible with a k195 miss.
```

Hence, conditional on the k195 double-square valuation gate, the already-reduced k39 phase coordinate contracts from nine possibilities to at most six:

```text
9 -> 6.
```

This removes exactly one third of the k39 survivor phase set on that valuation corridor.

The six remaining phases are only **necessary** for a k195 miss. They do not guarantee one; any negative-Jacobi residual factor still produces a hit.

## 6. The corridor is not phase-vacuous through k55

The double-square phase still has free CRT motion after fixing `v mod 41^2*37^2`.

For example, choosing the next free parameter equal to5 gives a t-class whose named phase coordinates are

```text
t mod13 = 7,
t mod43 = 12,
t mod47 = 0,
t mod17 = 6,
t mod11 = 1.
```

These lie in the landed survivor sets for k39, k43, k47, k51, and k55.

Therefore the k195 valuation corridor is not already empty under the currently proved **phase-only** filters through55.

This is not a full-ancestry statement. Exact signed-box hits at other earlier shifts may still terminate an individual target before195.

## 7. Machine consequence

Add the conditional propagation rule

```text
state = Route-B D-selector
q_D = 41 materialized in D
q_J = 37 materialized in J
v41(C195) >= 2
v37(C195) >= 2

=> K195_JACOBI_SATURATED
=> if tau13 in {1,9,10}: TERMINAL_HIT_AT_K195
=> else tau13 in {2,5,6,7,8,11} is necessary for k195 miss.
```

This is the first explicit example in the renewed-source program where **higher q-adic valuation reverses a multiplicity-one saturation barrier and turns it into constructive phase contraction**.

## 8. Bryan Entanglement Cross boundary

A natural observational history is

```text
up (+/-):    source routes split into q-adic lift subladders
left (-):    multiplicity-one two-source saturation is blocked
up (+/-):    both sources enter the square-lift phase
right (+):   k195 becomes Jacobi-saturated
right/down:  three tau13 classes terminate; six remain restricted
```

The directional history is metadata. The q-adic congruences, exact divisor-square residue equality, and Jacobi character calculation are the proof-bearing objects.

## 9. Next target

Two questions are now sharply separated:

1. **ancestry:** which, if any, double-square k195 states survive every earlier signed box and genuinely reach this selector as a first live exit?
2. **recursion:** on the six character-compatible tau13 phases, does the saturated k195 miss create a new support reservoir or character source that contracts the state again?

The next machine step should attack ancestry first, while preserving the k195 selector as a valid conditional fixed-shift theorem regardless of that outcome.
