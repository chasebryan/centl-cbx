# k195 double-square corridor: deterministic prefix full-ancestry audit

**Status:** exact finite first-hit census, deliberately not a universal theorem  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_prefix_full_ancestry_audit.py`  
**Depends on:** `K195-PRE55-ANCESTRY-PHASE-ENVELOPE.md` and exact Type-I/full-Type-II signed-box semantics.  
**Claim boundary:** this document reports exact ancestry for the canonical prefix `0 <= s < 1000` only. It does not prove a universal early absorber, does not show that later phase classes cannot reach k195, and is not an Erdős–Straus proof.

## 1. Why a finite audit is useful here

The exact phase envelope leaves 17,280 classes per period, but phase survival is not signed-box survival.

Before trying to prove a universal absorber, we need exact first-hit specimens showing which earlier shifts actually solve corridor primes.

The canonical first prefix is chosen as

```text
0 <= s < 1000.
```

Every resulting target p is below `2^64`, which lets the verifier use the known deterministic 64-bit Miller-Rabin basis and exact Pollard-Rho factorization. No probable-prime assumption is needed.

## 2. Exact scope

The k195 double-square corridor is

```text
t = 7,423,185,617,863
  + 11,799,129,838,887 s,
p = 169 + 840t.
```

Apply the landed pre-55 phase envelope first.

Inside `0<=s<1000`:

```text
phase-compatible s classes: 150
prime target p values:        31
```

The verifier pins the exact 31 s-values.

## 3. Full signed-box semantics

For each prime p and each admissible shift

```text
k=3,7,11,...,195,
```

write

```text
C_k=(p+k)/4.
```

Factor C_k exactly, construct every divisor residue of `C_k^2` modulo k from the prime-power factorization, and test both exact targets:

```text
Type I : d = -4^(-1) mod k
Type II: d = -C_k mod k.
```

The first k containing either target is the exact first signed-box hit.

This is Lane-I geometry, not a phase proxy.

## 4. Exact prefix result

All 31 phase-compatible prime targets hit by k11:

```text
first k3  : 21
first k7  :  6
first k11 :  4
first k>=15: 0
```

Thus

```text
maximum observed first hit = 11
reaches k195 in this prefix = 0.
```

For these 31 targets the first hit contains both Type-I and Type-II witnesses in the exact divisor residue set:

```text
I+II: 31.
```

The verifier records the exact factorization and residue-set size at every first hit.

## 5. Interpretation

This result is much stronger than the old phase-only witness, but it is still finite evidence.

It says:

> in the first deterministic prime laboratory inside the corrected double-square phase shell, early full signed boxes dominate completely.

It does **not** say:

> every double-square state is universally absorbed by k11.

That second sentence would require a theorem about the factor-support grammar of C3, C7, and C11 across the whole corridor.

The census tells us exactly where to look for such a theorem.

## 6. Next theorem target

The first three shifts should now be attacked symbolically.

For h169:

- at k3 the exact Type-I and Type-II target coincide at residue2;
- at k7 they coincide at residue5 because `C7=2 mod7`;
- k11 is the first small shift whose target geometry begins depending on the moving target residue more substantially.

The next useful result is an exact survivor grammar for the double-square corridor through k3/k7/k11, preferably expressed as prime-factor residue restrictions on the three companions rather than another range census.

If that grammar proves empty after coupling to the q41/q37 D-selector support state, k195 is ancestry-dead. If it leaves a residual class, that class becomes the correct search space for a genuine k195 reachability anchor.

## 7. Bryan Entanglement Cross boundary

The finite prefix is strong scheduling telemetry: early shifts carry overwhelming constructive pressure in the observed laboratory.

It is **not** proof-side pruning outside the audited prefix. BEC/BREC may record that pressure but cannot universalize it.
