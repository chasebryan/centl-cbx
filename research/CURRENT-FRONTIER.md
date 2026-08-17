# CENTL-CBX Current Research Frontier

## Status

Erdős–Straus remains open.

This repository contains an exact candidate-decomposition framework, a production-equivalent CBX X-ray kernel, and an increasingly explicit fixed-shift dependency grammar. Finite censuses, motif frequencies, and observed survivor contractions are not proofs unless a separate exact theorem and independent verifier are stated.

The detailed BREC ledger is maintained in

```text
research/BREC-CURRENT-FRONTIER.md.
```

This file records the global mathematical position.

---

## 1. Exact BREC recursive engine

The Bryan Recursive Entanglement Calculus is implemented as downstream exact Lane-I telemetry.

For admissible shifts

```text
k = 3 mod4,
```

BREC records

```text
+  iff the exact signed box hits {-1,-p^(-1)}
-  iff the exact signed box misses both targets
?  iff the application stage is undefined.
```

The production-equivalent verdict order remains

```text
W -> I -> N -> L.
```

BREC does not create proof or pruning authority by itself.

The exact cofactor orbit is affine:

```text
k_j = 4j+3,
C_j = (p+k_j)/4,
C_(j+1)=C_j+1,
4C_j-k_j=p.
```

Thus an anchored BREC history is a sequence of exact signed-box labels on consecutive cofactors while the modulus advances by four.

---

## 2. Anchored ancestry versus sliding motifs

BREC distinguishes

```text
sliding motif:
    a +/- word occurring anywhere in a history

anchored prefix:
    a +/- word beginning at absolute shift k=3.
```

For example

```text
-----
```

as an anchored prefix means exact combined misses at

```text
k=3,7,11,15,19.
```

This distinction is mandatory for fixed-shift theorem work.

---

## 3. The finite k23 coincidence pattern was falsified

The first `p<=2,000,000` BREC corpus contained no one-sided Type-I/Type-II state at fixed `k=23` after one or more all-negative ancestors.

That finite pattern was attacked directly and is false in general.

Exact Type-I-only witnesses include

```text
p =  5,151,841   early history -++-+
p =  8,243,281   early history ---++
p = 18,766,609   early history -----
p = 27,211,969   early history -----.
```

Therefore no all-negative ancestry depth from one through five forces Type-I/Type-II target coincidence at k23.

Permanent falsifier objects:

```text
research/verify_k23_brec_ancestry_falsifiers.py
research/K23-BREC-TWO-TARGET-COINCIDENCE.md.
```

This episode establishes the standing research rule:

```text
finite contraction
    -> candidate only
        -> adversarial extension
            -> preserve falsifier if false
            -> exact theorem + independent verifier if true
                -> only then pruning authority.
```

---

## 4. Exact q23 Type-I-only integer normal form

Conditional on the established q23 Type-II miss normal form, the Type-I companion has been exhausted exactly.

Write

```text
T=(p+23)/24.
```

Every q23 Type-I-only rescue has

```text
C23=6T,
p=24T-23,
T=mR,
```

where

```text
every prime divisor of m is 1 mod23,
Omega(R)=2,
all prime valuations of R lie in one class rho in {5,14} mod23.
```

The only local rescue states are the same-class valuation-two defects

```text
5^2
14^2.
```

The square and distinct-semiprime realizations of the two valuations are both locally compatible with all six Mordell-hard residue classes. Hard class alone cannot eliminate either q23 rescue split.

Files:

```text
research/K23-TYPEI-ONLY-INTEGER-NORMAL-FORM.md
research/verify_k23_typei_only_integer_normal_form.py
research/K23-RESCUE-SPLIT-HARD-CLASS-COMPATIBILITY.md
research/verify_k23_rescue_split_hard_classes.py.
```

---

## 5. The complete first-six q23 predecessor corridor

On the q23 Type-I-only parameter `T`, the first six Lane-I cofactors are

```text
C3  = 6T-5
C7  = 2(3T-2)
C11 = 3(2T-1)
C15 = 2(3T-1)
C19 = 6T-1
C23 = 6T.
```

Every predecessor through k19 now has an exact normal-form language.

### k=3

```text
sigma_3=-
iff
every prime divisor of 6T-5 is 1 mod3.
```

### k=7

```text
sigma_7=-
iff
every prime divisor of 3T-2 is in {1,2,4} mod7.
```

For Mordell-hard primes, Type I and Type II have identical hit/miss status at k7.

### k=11

The general exact combined miss is either:

```text
pure QR splitting modulo11,
```

or the thin primitive Type-II-miss branch over residue classes `(2,6)` with packet

```text
(1,0), (0,1), or (1,1).
```

The same-class valuation-two packets

```text
(2,0), (0,2)
```

are exact Type-I-only rescues.

### k=15

Let

```text
H=<2>={1,2,4,8} in U(15).
```

Then

```text
sigma_15=-
iff
every prime divisor of 3T-1 lies in H mod15.
```

### k=19

Using primitive root `2` modulo19, expand prime valuations of `6T-1` into discrete-log atoms `a_i` and define

```text
c = sum a_i mod18,
S = sum {-a_i,0,+a_i} subset Z/18Z.
```

The exact target exponents are

```text
Type II : 9
Type I  : 7-c mod18.
```

Hence

```text
sigma_19=-
iff
9 not in S and 7-c not in S.
```

The exhaustive local state closure is

```text
439 exact reachable states,
254 Type-II-miss states,
136 combined-miss states,
118 Type-I-only states.
```

Every combined-miss state has a canonical representative of at most three valuation atoms; every state has one of at most four. This is a state-complexity bound, not a bound on `Omega(C19)`.

The full 439-state closure and the independently written Type-II-miss automaton have been cross-verified state-for-state, including minimal depths and the identities of all 136 combined misses.

Core files:

```text
research/K3-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K7-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K11-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K15-BREC-OBSTRUCTION-NORMAL-FORM.md
research/K19-BREC-CYCLIC-STATE-COMPRESSION.md
research/K19-AUTOMATON-EQUIVALENCE.md
research/K23-PREDECESSOR-CORRIDOR-NORMAL-FORMS.md.
```

---

## 6. Reduced predecessor forms are pairwise coprime

Remove the forced factors from k7, k11, and k15 and define

```text
A=6T-5,
B=3T-2,
C=2T-1,
D=3T-1,
E=6T-1.
```

Then

```text
A,B,C,D,E
```

are pairwise coprime for every integer `T`.

This follows from the exact cancellations

```text
A-2B=-1
A-3C=-2
A-2D=-3
A-E=-4
2B-3C=-1
B-D=-1
2B-E=-3
3C-2D=-1
3C-E=-2
2D-E=-1,
```

with parity and fixed mod3 residues removing the only possible factors in the non-unit rows.

Therefore a cross-coordinate contradiction cannot be based on one nontrivial prime factor being shared by two reduced predecessor coordinates. The coupling must use the common affine parameter, residue/character information, valuation structure, or the q23 factor grammar.

Files:

```text
research/K23-PREDECESSOR-CORE-PAIRWISE-COPRIME.md
research/verify_k23_predecessor_pairwise_coprime.py.
```

---

## 7. Hard-class conditioning now gives exact local reductions

The six hard classes correspond to

```text
p mod840   T mod35
------------------
1              1
121            6
169            8
289           13
361           16
529           23.
```

These residues inject literal factors into the predecessor forms.

### k11 hard-class collapse

For

```text
p mod840 in {169,289,529},
```

we have

```text
5 | (2T-1).
```

The literal prime `5` is QR modulo11 but is not `1 mod11`. It therefore makes the general q11 thin branch impossible.

Exact consequence:

```text
p mod840 in {169,289,529}
=>
sigma_11=- iff every prime divisor of C11 is QR mod11.
```

Equivalently a Type-II miss automatically implies a Type-I miss in those three hard classes.

Files:

```text
research/H169-H289-H529-K11-BREC-OBSTRUCTION-NORMAL-FORM.md
research/verify_h169_h289_h529_k11_brec_obstruction_normal_form.py.
```

### k19 hard-class seeds

The forced q19 seeds are

```text
hard 1       : [5]
hard 121     : [5,7]
hard 169     : []
hard 289     : [7]
hard 361     : [5]
hard 529     : [].
```

Their exact Type-II-miss state budgets are

```text
seed []     : 254 = 136 combined + 118 Type-I-only
seed [5]    :  64 =  44 combined +  20 Type-I-only
seed [7]    :  27 =  18 combined +   9 Type-I-only
seed [5,7]  :   9 =   9 combined +   0 Type-I-only.
```

For h121 the forced factors `5*7` fill the entire QR subgroup modulo19, yielding the exact theorem

```text
sigma_19=-
iff
every prime divisor of C19 is QR mod19.
```

For h289 the forced factor `7` supplies the order-three subgroup `{0,6,12}` in the q19 exponent group. Exact target behavior factors through

```text
Z/18Z / <6> ~= Z/6Z.
```

The complete h289 Type-II-miss quotient has only

```text
9 states = 6 combined misses + 3 Type-I-only,
```

with exactly three full q19 lifts per quotient state.

Files:

```text
research/HARD-CLASS-PREDECESSOR-FORCED-SEEDS.md
research/H121-K19-BREC-OBSTRUCTION-NORMAL-FORM.md
research/H289-K19-QUOTIENT-NORMAL-FORM.md
research/verify_hard_class_predecessor_forced_seeds.py
research/verify_h289_k19_quotient_normal_form.py.
```

---

## 8. QR support reservoir principle

A reusable subgroup mechanism has now been isolated.

For prime `q=3 mod4`, suppose a QR-only factor subcollection `A` has exact signed support

```text
R_q(A)=Q_q,
```

the full quadratic-residue subgroup.

Then:

```text
residual factors all QR
    -> support remains Q_q
    -> both Lane-I targets miss

any residual NR factor
    -> its coset rQ_q is complete
    -> support becomes U(q)
    -> both targets hit.
```

This recovers the h121 k19 theorem and gives exact valuation thresholds such as

```text
q=11, v3(C11)>=2
    -> QR reservoir saturated

q=19, v5(C19)>=4
    -> QR reservoir saturated.
```

In hard classes 1 and361, where literal factor5 is already forced at k19, the latter gives the conditional exact theorem

```text
v5(C19)>=4
=>
sigma_19=- iff every prime divisor of C19 is QR mod19.
```

Files:

```text
research/QR-SUPPORT-RESERVOIR-SATURATION.md
research/verify_qr_support_reservoir_saturation.py.
```

---

## 9. Finite q23 -> k19 frontier and preserved falsification

The first finite grade

```text
p<=30,000,000,
q23 Type-I-only,
anchored prefix ----
```

contained exactly three candidates, all accidentally in hard class169.

That pattern was attacked at 100M and failed.

At

```text
p<=100,000,000
```

the exact forward census contains nine q23 Type-I-only candidates with prefix `----`:

```text
18,766,609   mod840=169   -----   rho=14   k19 miss
25,180,849   mod840=169   ----+   rho=14   k19 Type-II-only
27,211,969   mod840=169   -----   rho=5    k19 miss
31,935,121   mod840=1     ----+   rho=14   k19 Type-I-only
35,870,641   mod840=121   -----   rho=5    k19 miss
48,224,401   mod840=1     -----   rho=5    k19 miss
49,554,961   mod840=1     -----   rho=14   k19 miss
54,831,841   mod840=1     -----   rho=5    k19 miss
85,241,521   mod840=1     -----   rho=5    k19 miss.
```

The k19 split is

```text
7 combined misses
1 Type-I-only
1 Type-II-only.
```

Therefore neither

```text
---- q23 rescue => hard class169
```

nor

```text
----- q23 rescue => hard class169
```

is a universal implication.

The finite falsification is preserved in

```text
research/Q23-K19-100M-FINITE-FRONTIER.md.
```

No universal nine-candidate statement is claimed.

---

## 10. Existing later-shift exact corpus remains active

The prior exact program is still in force, including:

```text
q23 Type-II filters,
h169 realized k19 routes,
post-k23 companion ladder and support-renewal laws,
k27 survivor grammar and QR selectors,
k31 survivor normal forms,
k35 branch/valuation structure,
Route-B k47 structure,
later phase feedback modules,
reduced h169 dependency grammar,
prime backbone and composite core.
```

The BREC predecessor work does not replace those modules. It gives them a sharper ancestry-conditioned entry state.

In particular, the h169 post-k23 ladder

```text
C23=6B,
C_{23+4j}=6B+j
```

and its exact support-renewal identities remain major candidates for a genuine terminating decomposition transition.

---

## 11. Active proof targets

The immediate frontier is now cross-coordinate rather than fixed-shift.

The exact early object is

```text
T
 |
 +-- 6T-5   k3 semigroup
 +-- 3T-2   k7 QR semigroup
 +-- 2T-1   k11 class-conditioned QR/thin grammar
 +-- 3T-1   k15 subgroup semigroup
 +-- 6T-1   k19 class-conditioned finite state
 +-- 6T      q23 same-class Omega-two rescue.
```

High-value targets are:

1. determine which class-conditioned k19 states remain arithmetically compatible with the first four predecessor laws and each q23 rescue class;
2. exploit the h289 nine-state quotient rather than the generic 439-state k19 universe;
3. reduce the h1/h361 seed-[5] k19 universe, especially the unsaturated valuation cases below the QR-reservoir threshold;
4. determine whether the q11 hard-class collapse forces later k19 product exponents or support modes;
5. couple the exact predecessor grammar to the existing post-k23 h169 ladder and its k27/k31 absorber candidates;
6. attack every apparent finite cross-coordinate absence by targeted extension before promoting it to a theorem.

The desired end product is not another percentage table. It is a well-founded exact transition grammar in which every surviving state is either decomposed or mapped to a strictly reduced proof-bearing state.

---

## 12. Claim boundary

Exact results currently include the fixed-shift predecessor normal forms, q23 Type-I-only integer normal form, pairwise-coprime predecessor core, k19 finite-state closure and independent automaton equivalence, class-conditioned k11 collapse, h121 k19 QR theorem, h289 k19 quotient theorem, and QR-reservoir saturation lemma.

The 30M and 100M q23/k19 contractions are finite evidence only; the 100M run also preserves a falsifier to the 30M hard-class pattern.

No result in this repository currently proves the Erdős–Straus conjecture, a universal finite Lane-I ceiling, or a complete closed decomposition method.
