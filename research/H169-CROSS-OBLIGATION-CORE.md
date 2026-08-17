# h169 cross-coordinate obligation core

**Status:** exact explanation layer over the landed h169 pair-route grammar, revision 2  
**Date:** 2026-08-17  
**Analyzer:** `analyze_h169_cross_obligation_core.py`  
**New coordinate:** `t mod11` inherited from the exact h169 k11 miss theorem

## 1. The obligation machine now crosses coordinates

The first obligation-core analyzer explained contradictions already visible inside the reduced h169 dependency grammar.

This layer adds one genuinely external ancestry coordinate:

```text
t11 = t mod11.
```

Under an inherited h169 k11 combined miss,

```text
t11 in {0,2,3,4,8}.
```

The analyzer tensors that exact five-phase domain with the landed Route-A / Route-B grammar and carries one explicit derived proposition:

```text
factor11_in_R.
```

This allows an earlier k11 obstruction to collide directly with the later k19 residual-support grammar.

Revision 2 also lets a phase carry an exact downstream **resource certificate** even when no branch-deletion theorem is available. The first such certificate is the forced factor11 seed at k43 on `t11=2`.

---

## 2. Two cross-coordinate theorem atoms

The contradiction layer compiles exactly two theorem atoms.

### Phase-to-reservoir theorem

On h169,

```text
T=8+35t.
```

Therefore

```text
t=8 mod11
iff
T=2 mod11
iff
11|C19.
```

On either realized pair route,

```text
C19=S*R
```

with

```text
S=391 or1081
```

and

```text
gcd(S,11)=1.
```

Hence inside the inherited k11-miss phase domain,

```text
factor11_in_R
iff
t mod11=8.
```

### BARE exclusion theorem

The landed k19 BARE mode requires

```text
every prime divisor of R is 1 mod19.
```

But

```text
11 mod19=11.
```

So

```text
factor11_in_R
->
k19_mode != BARE.
```

These are kept as two separate atoms so the contradiction engine can expose the actual arithmetic bridge instead of hiding it inside one black-box predicate.

---

## 3. Canonical four-atom cross-coordinate contradiction

Ask for

```text
t mod11=8
k19_mode=BARE.
```

The analyzer returns an inclusion-minimal core with four atoms:

```text
ASSUMPTION: t mod11=8
ASSUMPTION: k19_mode=BARE
THEOREM:    t11=8 iff factor11_in_R
THEOREM:    factor11_in_R excludes k19 BARE.
```

Delete any one atom and the cross grammar is satisfiable again.

This minimality is relative to the already-landed h169 dependency grammar, which is held fixed as background proof data.

The arithmetic explanation is exactly

```text
t11=8
-> 11|R

BARE
-> support(R) subset 1 mod19

11 mod19 !=1
-> contradiction.
```

That is the kind of explanation BREC should emit for a dead survivor state.

---

## 4. Formal-state contraction

Before adding `t mod11`, the landed grammar contains

```text
Route A: 105,600 formal tuples
Route B: 147,900 formal tuples.
```

Tensoring naively with the five allowed k11 phases would give

```text
Route A: 528,000
Route B: 739,500.
```

The cross-coordinate rule deletes BARE exactly on the `t11=8` slice, leaving

```text
Route A: 516,450
Route B: 736,950.
```

These are formal grammar counts only. They are not arithmetic survivor counts or densities.

The significance is not the percentage reduction. It is that the reduction comes from a different predecessor coordinate and therefore demonstrates real simultaneous-state coupling.

---

## 5. One phase now carries a mode deletion and valuation contraction

Query

```text
t mod11=8.
```

The analyzer forces

```text
factor11_in_R=true
k19_mode=FULL_QR.
```

It also attaches the exact seeded q19 valuation resource:

```text
Omega_NR(C19) <= 2
```

for every k19 Type-II miss on that phase.

Thus the live obligation ledger contains both

```text
horizontal state restriction:
    k19 FULL_QR only

vertical resource restriction:
    NR valuation budget <=2.
```

The generic unseeded h169 k19 budget is 8, so the same ancestry phase simultaneously deletes a mode and contracts the remaining NR resource from 8 to 2.

---

## 6. A second phase now carries a k43 resource certificate

Revision 2 resolves the previously open `t11=2` child as an exact local-state contraction.

On

```text
t mod11=2,
```

we have

```text
T mod11=1
```

and

```text
C43=(p+43)/4=6T+5,
```

so

```text
11|C43.
```

The exact q43 signed-box automaton gives

```text
unseeded Type-II-miss states: 18,048
seed11 Type-II-miss states:    2,317
```

with exact class split

```text
seed11 combined-miss: 1,217
seed11 Type-I-only:   1,100.
```

The weighted miss graph has no positive-NR edge inside an SCC and gives

```text
unseeded Omega_NR(C43) <=20
seed11   Omega_NR(C43) <=14.
```

Therefore a query with

```text
t mod11=2
```

now receives a theorem-backed obligation object recording

```text
11|C43
state(C43) in exact seed11 q43 closure of size 2317
Omega_NR(C43)<=14.
```

This does not delete a route or survivor mode yet because no landed k43 support law has been found that conflicts with the seed11 closure. It is a resource contraction awaiting a simultaneous-state collision.

---

## 7. Why this is the desired architecture

A survivor should not be stored merely as

```text
------
```

or as a bag of independent shift labels.

The proof state is becoming

```text
phase obligations
+ survivor modes
+ forced rational factors
+ local finite-state certificates
+ support-subgroup laws
+ separated reservoirs
+ valuation budgets
+ affine companion identities.
```

Then either a contradiction appears immediately, or the surviving state carries a strictly richer and more expensive obligation ledger.

The machine can preserve the smallest current exact reason for death, cluster recurring reasons, and promote recurring core families into theorem-mining targets.

That gives a concrete research loop:

```text
survivor state
-> obligation accumulation
-> state/resource contraction
-> contradiction when available
-> irreducible core
-> recurring core family
-> human-readable theorem.
```

---

## 8. Interface

Self-test:

```sh
python3 research/analyze_h169_cross_obligation_core.py --self-test
```

Canonical contradiction:

```sh
python3 research/analyze_h169_cross_obligation_core.py \
  --route B \
  --state-json '{"t_mod_11":8,"k19_mode":"BARE"}'
```

Live k19 phase ledger:

```sh
python3 research/analyze_h169_cross_obligation_core.py \
  --route A \
  --state-json '{"t_mod_11":8}'
```

Live k43 resource ledger:

```sh
python3 research/analyze_h169_cross_obligation_core.py \
  --route A \
  --state-json '{"t_mod_11":2}'
```

The state JSON also accepts the landed base grammar fields, so ancestry phase constraints can be intersected with k19/k27/k31/k35/k47 mode assumptions.

---

## 9. Status of the five k11 phase children

The exact phase partition now reads

```text
t11=8 -> factor11 at k19
           BARE deleted
           Omega_NR: 8 -> 2

t11=4 -> factor11 at k35
           existing 3-adic branch structure active

t11=3 -> factor11 at k39
           existing routed J39+ support theorem active

t11=2 -> factor11 at k43
           Type-II-miss states: 18048 -> 2317
           Omega_NR: 20 -> 14

t11=0 -> factor11 at k51
           unresolved composite-modulus child.
```

The only untouched child of this particular factor11 partition is now k51.

The k51 target should be attacked as composite unit-group geometry, not by pretending 51 is a prime modulus. A natural exact state space is

```text
(Z/51Z)^* ~= (Z/3Z)^* x (Z/17Z)^*.
```

The first question is whether preloading literal residue11 shrinks the complete Type-II-miss closure, creates a character restriction, or produces a finite valuation resource that can collide with the earlier route grammar.

---

## 10. Claim boundary

The base h169 grammar remains fixed background proof data. The cross-core minimality claim is relative to that background.

The five `t mod11` values are necessary phases under an inherited h169 k11 miss; the analyzer does not assert every phase has an arithmetic realization.

The k43 certificate is a complete abstract local automaton result conditional on the phase and a k43 Type-II miss. It does not assert every seed11 state is arithmetically realized.

Formal tuple counts are not prime counts. No finite Lane-I ceiling or Erdős-Straus proof follows from this module alone.
