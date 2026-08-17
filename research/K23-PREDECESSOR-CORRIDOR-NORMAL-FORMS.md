# k=23 predecessor corridor normal forms

**Status:** exact synthesis of independently verified fixed-shift theorems  
**Date:** 2026-08-17  
**Application:** `CBX-Lane-I-shift-history-v1`  
**Claim boundary:** structural reduction only; the full five-negative corridor is explicitly realizable

## 1. One parameter now carries the whole early corridor

On the exact `k=23` Type-I-only rescue branch, write

```text
T = (p+23)/24.
```

Then

```text
p    = 24T-23,
C_23 = 6T.
```

The q23 factor normal form is already rigid:

```text
T = mR,
```

where

```text
every prime divisor of m is 1 mod 23,
Omega(R)=2,
all prime valuations of R lie in one class rho in {5,14} mod 23.
```

The entire five-coordinate predecessor corridor is therefore the translated block

```text
C_3  = 6T-5,
C_7  = 6T-4 = 2(3T-2),
C_11 = 6T-3 = 3(2T-1),
C_15 = 6T-2 = 2(3T-1),
C_19 = 6T-1,
C_23 = 6T.
```

This is the point at which the BREC representation stops being merely descriptive. The first five signs are exact arithmetic constraints on five neighboring affine forms of one integer `T`.

---

## 2. Coordinate 1: k=3

The exact combined-target theorem is

```text
sigma_3(p) = -
```

if and only if every prime divisor of

```text
6T-5
```

is

```text
1 mod 3.
```

So the first obstruction coordinate is a multiplicative-semigroup condition on one endpoint of the six-term block.

---

## 3. Coordinate 2: k=7

Since

```text
C_7 = 2(3T-2)
```

and the forced factor `2` already lies in the quadratic-residue subgroup modulo `7`, the exact theorem reduces to

```text
sigma_7(p) = -
```

if and only if every prime divisor of

```text
3T-2
```

lies in

```text
{1,2,4} mod 7.
```

Type I and Type II have identical hit/miss status at this shift for Mordell-hard primes.

---

## 4. Coordinate 3: k=11

Here

```text
C_11 = 3(2T-1).
```

The exact combined miss has two branches.

### Pure-QR branch

Every prime divisor of `2T-1` is a quadratic residue modulo `11`.

### Thin primitive branch

The exact q11 Type-II thin hypotheses hold, and the primitive nonresidue valuation packet over residue classes `(2,6)` is one of

```text
(1,0),
(0,1),
(1,1).
```

The same-class valuation-two packets

```text
(2,0),
(0,2)
```

are not misses. They are exact Type-I-only rescues.

Thus the third BREC coordinate is no longer an open-ended factorization problem. It is one pure subgroup branch plus three bounded thin packets.

---

## 5. Coordinate 4: k=15

The exact combined theorem is especially clean.

Let

```text
H = <2> = {1,2,4,8}
```

inside `U(15)`. Since

```text
C_15 = 2(3T-1),
```

we have

```text
sigma_15(p) = -
```

if and only if every prime divisor of

```text
3T-1
```

lies in `H` modulo `15`.

The previously tempting thin-11 loophole does not survive the full fixed-shift congruence conditions. It was removed by exact analysis and explicit falsifier testing.

---

## 6. Coordinate 5: k=19

The fifth coordinate is naturally a finite cyclic-state problem rather than a short residue-class sentence.

Because `2` is a primitive root modulo `19`, write each prime valuation of

```text
C_19 = 6T-1
```

as a discrete-log atom

```text
a_i in Z/18Z.
```

Define

```text
c = sum_i a_i mod 18,
S = sum_i {-a_i,0,+a_i} subset Z/18Z.
```

Then the exact target exponents are

```text
Type II : 9
Type I  : 7-c mod 18,
```

and

```text
sigma_19(p) = -
```

if and only if

```text
9 not in S
and
7-c not in S.
```

The complete finite-state closure contains

```text
439 reachable states,
136 combined-miss states.
```

Every combined-miss state has a canonical representative using at most three valuation atoms, although the actual factorization of `6T-1` may contain many more valuations.

---

## 7. The exact five-negative corridor

For a q23 Type-I-only rescue, the anchored BREC word

```text
-----+
```

is therefore equivalent to the simultaneous satisfaction of:

```text
6T-5:
  every prime divisor is 1 mod 3

3T-2:
  every prime divisor is QR mod 7

2T-1:
  pure QR mod 11
  OR one of the three exact thin combined-miss packets

3T-1:
  every prime divisor lies in {1,2,4,8} mod 15

6T-1:
  cyclic state (c,S) lies in one of the 136 exact k19 miss states

6T:
  q23 Type-I-only normal form with rho=5 or rho=14 and Omega(R)=2.
```

This is the first point in the current corridor program where **every predecessor coordinate before k=23 has an exact finite normal-form language**.

The remaining problem is not another isolated fixed-shift classification. It is compatibility across these five neighboring forms.

---

## 8. Two explicit full-corridor survivors prevent a false contradiction

The conjunction above is not empty.

Two preserved exact primes satisfy all five predecessor obstruction laws and then construct Type I at k23:

```text
p = 18,766,609    q23 rescue class rho=14
p = 27,211,969    q23 rescue class rho=5.
```

Both have

```text
early history = -----
k23            = Type-I-only.
```

This is crucial. Any proposed cross-coordinate theorem that claims the five predecessor laws are mutually incompatible is false unless it contains additional hypotheses that exclude neither of these verified primes accidentally.

They are now mandatory regression guards for the next phase.

---

## 9. What has actually been compressed

Before this synthesis, a candidate `-----+` prime could be viewed as six independent signed-box evaluations with arbitrary factorizations.

Now it is one parameter `T` subjected to five exact local grammars and one q23 rescue grammar:

```text
T
 |
 +-- 6T-5   mod 3 semigroup
 +-- 3T-2   mod 7 QR semigroup
 +-- 2T-1   mod 11 QR/thin packet
 +-- 3T-1   mod 15 subgroup semigroup
 +-- 6T-1   one of 136 cyclic k19 states
 +-- 6T      q23 same-class Omega-two rescue state.
```

The search space has changed shape. The correct next object is a **cross-coordinate compatibility grammar** on `T`, not another disconnected collection of percentages.

---

## 10. Immediate theorem targets

The next reductions should ask which information is shared by several coordinates at once. High-value candidates are:

1. the six exact hard classes `T mod 35` together with the q23 class `rho in {5,14}`;
2. character vectors of the five predecessor forms across moduli `3,7,11,15,19,23`;
3. whether the q11 pure/thin branch constrains the k19 product exponent `c` or canonical atom family;
4. whether the square versus distinct-semiprime q23 rescue split changes the allowable k19 state distribution after all four earlier misses;
5. whether the two known full-corridor survivors occupy the same deeper cross-coordinate invariant or two genuinely separate components.

The hard classes alone cannot eliminate either q23 multiplicity split. That dead end is already closed by the modulus-805 compatibility theorem.

---

## 11. Executable synthesis verifier

Run

```sh
python3 research/verify_k23_predecessor_corridor_normal_forms.py
```

The verifier does not trust stored history strings. For each preserved q23 Type-I-only witness it reconstructs exact signed-box stages and checks them against:

```text
k3 factor criterion,
k7 QR criterion,
k11 exact pure/thin classifier,
k15 subgroup criterion,
k19 cyclic-state classifier,
and the q23 integer rescue normal form.
```

It preserves both `-----+` survivors as compulsory regression tests.

---

## 12. Claim boundary

This synthesis proves no incompatibility because the exact conjunction is known to be realizable.

It does not create pruning authority, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.

Its value is sharper: the first five obstruction coordinates have been converted into one exact, auditable compatibility problem on a single integer parameter. The next theorem must live **between the coordinates**, not merely inside one of them.
