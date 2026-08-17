# h169 cross-coordinate obligation core

**Status:** exact explanation layer over the landed h169 pair-route grammar  
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

---

## 2. Two cross-coordinate theorem atoms

The layer compiles exactly two new theorem atoms.

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

The new cross-coordinate rule deletes BARE exactly on the `t11=8` slice, leaving

```text
Route A: 516,450
Route B: 736,950.
```

These are formal grammar counts only. They are not arithmetic survivor counts or densities.

The significance is not the percentage reduction. It is that the reduction comes from a **different predecessor coordinate** and therefore demonstrates real simultaneous-state coupling.

---

## 5. A live phase carries both mode and valuation obligations

Query only

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

This is the first explicit machine object in this line of work where an ancestry phase simultaneously contracts a symbolic mode and a valuation budget.

---

## 6. Why this is the desired architecture

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
+ support-subgroup laws
+ separated reservoirs
+ valuation budgets
+ affine companion identities.
```

Then a contradiction is an unsatisfiable subset of those obligations.

The machine can preserve the smallest current exact reason for death, cluster recurring reasons, and promote recurring core families into theorem-mining targets.

That gives a concrete research loop:

```text
survivor state
-> obligation accumulation
-> contradiction
-> irreducible core
-> recurring core family
-> human-readable theorem.
```

---

## 7. Interface

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

Live phase ledger:

```sh
python3 research/analyze_h169_cross_obligation_core.py \
  --route A \
  --state-json '{"t_mod_11":8}'
```

The state JSON also accepts the landed base grammar fields, so phase constraints can be combined with k27/k31/k35/k47 mode assumptions.

---

## 8. Next collision targets

The exact five-way k11 phase partition now points to three especially clean next destinations:

```text
t11=4 -> factor11 at k35, S7 already deleted
t11=3 -> factor11 at k39, routed J39+ support theorem active
t11=8 -> factor11 at k19 now deletes BARE and cuts NR budget to2.
```

The unresolved children are

```text
t11=0 -> factor11 at k51
t11=2 -> factor11 at k43.
```

Those should be attacked as **seeded local automata**, not as generic new shift scans.

For each destination, ask whether the forced literal factor11 causes

```text
automatic hit,
branch deletion,
smaller miss closure,
new support character,
or valuation-budget contraction.
```

If either child collapses, feed the result back into this cross-coordinate grammar as another theorem atom.

---

## 9. Claim boundary

The base h169 grammar remains fixed background proof data. The cross-core minimality claim is relative to that background.

The five `t mod11` values are necessary phases under an inherited h169 k11 miss; the analyzer does not assert every phase has an arithmetic realization.

Formal tuple counts are not prime counts. No finite Lane-I ceiling or Erdős–Straus proof follows from this module alone.
