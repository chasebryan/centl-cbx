# k195 double-square corridor: exact pre-55 ancestry phase envelope

**Status:** exact phase-only ancestry reduction for the landed k195 double-square corridor  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_pre55_ancestry_phase_envelope.py`  
**Depends on:** landed Route-B D-selector grammar, `K195-DOUBLE-SQUARE-PHASE-SELECTOR.md`, k19/k27 coupling, k39/k43/k51/k55 phase theorems, and Route-B k47 phase feedback.  
**Claim boundary:** exact necessary phase conditions only. Surviving phase classes are not asserted to reach k195 through full signed-box ancestry. This is not a termination theorem or Erdős–Straus proof.

## 1. Normalize the double-square corridor

The landed k195 theorem has

```text
t = 3,925,816 + 5,127,183 v
v = 1,447,809 + 2,301,289 s.
```

Therefore

```text
t = 7,423,185,617,863
  + 11,799,129,838,887 s.
```

Call these coefficients `T_*` and `Delta_*`.

## 2. Frozen coordinates

The exact corridor fixes

```text
tau9  = t mod9  = 7
tau17 = t mod17 = 6
tau23 = t mod23 = 15
tau31 = t mod31 = 7
tau47 = t mod47 = 0.
```

These are exactly the Route-B D-selector / q41-q37 double-square coordinates.

Consequences already landed:

- `tau17=6` and `tau31=7` force k27 mode D;
- `tau31=7` excludes k31 BARE, so a k31 miss is FULL_QR;
- `tau9=7` is the D-selector valuation phase;
- `tau47=0` is the realized Route-B k47 phase;
- `tau23=15` is fixed Route-B ancestry.

## 3. Moving coordinates

Modulo the remaining independent pre-55 phase moduli,

```text
tau19 = 10 + 12s mod19
tau13 =  2 +  s mod13
tau43 = 10 +  9s mod43
tau11 =  4 +  6s mod11.
```

Each coefficient is invertible modulo its modulus, so every residue occurs exactly once as s traverses that modulus.

## 4. Exact survival requirements before k55

### k19 plus k27 D compatibility

A realized pair-route k19 miss requires

```text
S19={0,2,7,8,11,14,15,16,17}.
```

But `tau19=8` forces k27 mode Q, which is incompatible with the already-forced k27 mode D. Therefore the double-square corridor must satisfy

```text
tau19 in {0,2,7,11,14,15,16,17}.
```

Exactly 8 of19 phases remain.

### k39

The landed k39 survivor phase set is

```text
tau13 in {1,2,5,6,7,8,9,10,11}.
```

Exactly 9 of13 phases remain.

### k43

The exact k43 elementary phase shell removes

```text
{2,28,30} mod43,
```

leaving 40 of43 phases.

### Route-B k47 plus k55

The landed k55 phase theorem allows

```text
{0,1,2,3,4,8,9} mod11.
```

But Route-B k47 feedback proves

```text
tau11=1 -> k47 hit.
```

So reaching beyond k47 requires

```text
tau11 in {0,2,3,4,8,9}.
```

Exactly 6 of11 phases remain.

This corrects the old phase-only witness in the original k195 PR: its `tau11=1` point is not ancestry-live under the newer k47 theorem.

## 5. Exact CRT volume

The moduli

```text
19,13,43,11
```

are pairwise coprime, and the four moving coordinates are affine bijections of s modulo each modulus.

Hence the exact combined s-period is

```text
M = 19*13*43*11 = 116,831.
```

The number of phase classes not excluded before k55 is

```text
8*9*40*6 = 17,280.
```

Therefore the exact necessary phase fraction is

```text
17,280 / 116,831
= 0.1479059496195359...
```

and the proved pre-55 phase elimination is

```text
99,551 / 116,831
= 0.8520940503804641...
```

or about **85.21%** of the double-square s-lattice.

This is a periodic exact class count, not a probabilistic density claim.

## 6. k195 output split inside the surviving envelope

If a state actually reaches k195, the landed saturation selector uses tau13.

Among the 9 k39-surviving tau13 phases:

```text
{1,9,10}       -> k195 MUST HIT
{2,5,6,7,8,11} -> k195 miss character-compatible.
```

Because tau13 is independent of the other three moving coordinates, the 17,280 pre-55 phase classes split exactly into

```text
5,760  guaranteed-k195-hit classes upon reach
11,520 k195-miss-compatible classes upon reach.
```

This statement remains conditional on reaching k195 alive.

## 7. Corrected nonempty phase witness

For example

```text
s=8
```

gives

```text
tau19=11
tau13=10
tau43=39
tau11=8,
```

with the frozen coordinates above. It satisfies every phase-only pre-55 survival condition in this theorem.

Since tau13=10, if an exact state on this phase reaches k195 it lies in the guaranteed-hit side of the k195 selector.

This is only a phase witness, not a full arithmetic survivor.

## 8. What this does and does not settle

It settles the exact phase shell around the k195 ancestry problem and removes the stale tau11=1 witness.

It does **not** prove that any of the remaining 17,280 classes contains a prime target that survives every earlier full signed box. Factor-support state still matters at k3,k7,k11,... and finite first-hit evidence shows that those earlier shifts are highly active.

The next layer must therefore use full Type-I / Type-II signed-box ancestry, not another phase-only proxy.

## 9. Bryan Entanglement Cross boundary

This is a clean `down (-/+)` excavation event: exact prior theorems remove 85.21% of the corridor before expensive ancestry work.

The BEC label is scheduler metadata only. The modular implications and CRT count are the proof-bearing objects.
