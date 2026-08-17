# h169 obligation-core hunter

**Status:** exact explanation layer over the landed h169 dependency grammar  
**Date:** 2026-08-17  
**Analyzer:** `analyze_h169_obligation_core.py`  
**Underlying proof engine:** `propagate_h169_dependency_state.py`  
**Claim boundary:** no new pruning theorem is introduced here

## 1. Change of question

The useful question is no longer only

```text
which Lane-I shifts miss?
```

or even

```text
which symbolic survivor modes remain?
```

For a deep survivor state, the sharper question is

```text
what must all be true at once for this state to exist?
```

The h169 research tree already contains enough exact implications to answer part of that question mechanically.

The obligation-core hunter turns the existing dependency grammar into an explanation engine.

For a nonempty formal state it emits the accumulated arithmetic obligations.

For an empty formal state it deletes irrelevant assumptions and theorem rules until it reaches an irreducible contradiction core.

So the output is no longer merely

```text
-
```

or

```text
contradiction=true.
```

It can say why the state died.

---

## 2. Existing theorem grammar, not a new heuristic

The analyzer imports the exact rules already compiled in

```text
propagate_h169_dependency_state.py.
```

The current theorem atoms are

```text
k19-bare-phase
k27-phase8-q-selector
k31-bare-phase-seam
route-b-k47-thin-even
route-b-odd-full-full
k35-v3-ge2-j-only.
```

They encode landed implications such as

```text
Route-B k19 BARE
  -> tau19=8
  -> 19|E
  -> on k27 miss, k27 mode Q.
```

The new analyzer grants none of these statements extra authority. It only composes and explains them.

---

## 3. Obligation ledger

For a satisfiable formal proof state, the analyzer records five classes of obligation.

### Phase obligations

The surviving domains of

```text
tau19=t mod19
tau31=t mod31
tau4=t mod4
tau9=t mod9.
```

Singleton domains become forced coordinates.

### Survivor-mode obligations

The remaining exact mode domains at

```text
k19
k27
k31
k35
k47.
```

For example, Route-B `k19=BARE` forces

```text
tau19=8
k27=Q.
```

### Support and character obligations

The underlying propagator already exports theorem-safe consequences such as

```text
k23 miss -> every prime factor of B is QR mod23
k31 miss -> every prime factor of D is QR mod31
k27 Q    -> every prime factor of E is QR mod27
k31 BARE -> every prime factor of D lies in {1,5,25} mod31.
```

These are now grouped as obligations of one hypothetical arithmetic survivor.

### Valuation and seam obligations

The phase state determines exact derived data including

```text
parity,
2-adic support seam,
k35 v3 bucket,
gcd(D,J) domain.
```

The point is to retain vertical valuation information beside horizontal character/support information rather than treating them as separate research universes.

### Affine and support-separation obligations

On the two realized h169 routes,

```text
Route A: S=391=17*23
Route B: S=1081=23*47.
```

The ten-companion block is

```text
C19 = S*R
C23 = S*R+1 =  6B
C27 = S*R+2 =  7E
C31 = S*R+3 = 10D
C35 = S*R+4 =  3F
C39 = S*R+5 =  2G
C43 = S*R+6 =    H
C47 = S*R+7 =  6J
C51 = S*R+8 =  5K
C55 = S*R+9 = 14L.
```

The odd parts of

```text
R,B,E,D,F,G,H,J,K,L
```

are pairwise coprime.

Only the already-proved 2-adic seams may recycle support.

Thus every live state carries a set of separate prime reservoirs tied together by one consecutive affine block.

That is precisely the sort of object on which cross-coordinate contradiction should be searched.

---

## 4. Contradiction cores

Suppose a partial state is incompatible with the theorem grammar.

The analyzer treats two things as removable atoms:

```text
user/state assumptions
theorem rules.
```

It then repeatedly removes any atom whose deletion leaves the system contradictory.

The final set is **inclusion-minimal**:

```text
the complete core is contradictory,
but deleting any one retained atom makes it satisfiable.
```

This is an irreducible unsatisfiable core.

It is intentionally **not** advertised as minimum-cardinality. Different irreducible cores can exist in a constraint system, and finding the absolutely smallest one is not needed for the research purpose.

The goal is a short exact explanation.

---

## 5. Canonical four-atom core

Consider the partial Route-B state

```text
k19_mode = BARE
k27_mode = A.
```

The analyzer returns a contradiction core containing exactly four atoms:

```text
ASSUMPTION: k19_mode=BARE
ASSUMPTION: k27_mode=A
THEOREM:    Route-B BARE -> tau19=8
THEOREM:    tau19=8 -> on k27 miss, mode Q.
```

The proof is transparent:

```text
k19 BARE
  -> tau19=8
  -> k27 Q
  contradicts k27 A.
```

Every atom is necessary to this core.

This is the desired direction for BREC contradiction mining: replace a dead symbolic state with the smallest theorem-backed reason currently available for its death.

---

## 6. A live state also becomes more informative

Run

```sh
python3 research/analyze_h169_obligation_core.py \
  --route B \
  --state-json '{"k19_mode":"BARE"}'
```

The result is not merely “live.”

It records that the state must simultaneously carry

```text
tau19=8
k27 mode Q
QR23 support on B
QR27 support on E
QR31 support on D
the route-B consecutive affine block
pairwise-separated odd support reservoirs
and the remaining phase/mode domains.
```

That ledger is a better input to theorem mining than a bare BREC word.

---

## 7. Why this matters for valuation escape

A valuation increase should no longer be viewed only as “more complexity.”

It can be stored as another obligation attached to one reservoir in the consecutive block.

A future state can therefore look schematically like

```text
character obligations
+ support-subgroup obligations
+ exact mode obligations
+ q-adic valuation obligations
+ forced rational factors
+ forbidden support sharing
+ CRT phase obligations
+ affine companion identities.
```

The termination target then changes from

```text
prove valuations cannot grow forever
```

into the more local and plausible statement

```text
continued survival keeps adding obligations,
and sufficiently rich obligation sets become jointly unrealizable.
```

The present analyzer does not prove that termination statement. It creates the proof-state format needed to hunt it exactly.

---

## 8. Minimal obstruction cores are theorem-mining targets

The next generation of exact searches should not rank survivor states only by depth or rarity.

For every contradiction found after adding a candidate theorem, record its irreducible core.

Then cluster cores by structure:

```text
phase + mode collision
support + affine collision
valuation + mode collision
forced-factor + branch collision
character + reciprocity collision
source + support-separation collision.
```

Repeated core shapes are candidates for human-readable lemmas.

In other words:

```text
machine contradiction
  -> minimal core
    -> recurring core family
      -> exact parametric theorem.
```

That is a much cleaner bridge from computation to mathematics than simply extending a census.

---

## 9. Executable interface

Self-test:

```sh
python3 research/analyze_h169_obligation_core.py --self-test
```

Contradictory state:

```sh
python3 research/analyze_h169_obligation_core.py \
  --route B \
  --state-json '{"k19_mode":"BARE","k27_mode":"A"}'
```

Live state:

```sh
python3 research/analyze_h169_obligation_core.py \
  --route B \
  --state-json '{"k19_mode":"BARE"}'
```

Allowed domains can be supplied as JSON lists, for example

```sh
--state-json '{"tau4":[0,2],"k31_mode":["BARE","FULL_QR"]}'
```

---

## 10. Immediate next theorem target

The analyzer exposes where the current exact grammar stops contracting.

The highest-value next mathematical work is therefore not another isolated shift.

It is to add exact rules that couple the currently independent obligation classes, especially

```text
k27 mode
x k31 mode
x k35 branch
x CRT phase
x separated support reservoirs
x affine identities.
```

A new theorem is especially valuable if it either

```text
empties an entire formal product-state family
```

or

```text
forces a later rational-prime selector / signed-box hit.
```

That is the direct route from the existing dependency grammar toward a genuine contradiction machine.

---

## 11. Claim boundary

The obligation ledger contains only already-proved consequences within the realized h169 pair-route laboratory.

An irreducible formal contradiction is exact inside that grammar, but is not automatically a theorem about every Mordell-hard prime or every possible h169 route.

No result in this module establishes a universal Lane-I ceiling, a complete decomposition theorem, or Erdős–Straus.
