# k195 / q19-square corridor: exact k35 ancestry anchor

**Status:** exact certified prime anchor inside the Route-B D-selector / q19-square / q41-q37 double-square laboratory  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_k35_ancestry_anchor.py`  
**Claim boundary:** one exact prime anchor. It proves that this combined corridor can survive every admissible signed box through k31 and first exit at k35. It does not prove a universal k35 ceiling, termination, or Erdős–Straus.

## Anchor

```text
s = 2,778,207
t = 32,780,432,535,490,353,472
p = 27,535,563,329,811,896,916,649
```

The verifier proves p prime with a Lucas certificate from the complete factorization of `p-1` and certifies all companion factors used below.

Relevant phases:

```text
tau9=7, tau11=0, tau13=5, tau17=6,
tau19=11, tau23=15, tau31=7, tau43=18, tau47=0.
```

## Exact ancestry

```text
k3  miss
k7  miss
k11 miss
k15 miss
k19 miss
k23 miss
k27 miss
k31 miss
k35 HIT, Type I + Type II
```

The exact companion factorizations are pinned in the verifier. The corresponding miss masks at k3 through k31 contain neither fixed-shift target.

## Realized source / valuation state

At k15, q19 is materialized exactly once and has positive Jacobi character at origin15. At k167, `19^2|C167`.

The same prime realizes the Route-B D-selector geometry:

```text
k19 FULL_QR
k23 QR support
k27 D-mode with C27=7*17*31*r, r prime, r=2 mod27
k31 FULL_QR with materialized q41
```

Later companions also contain materialized q37 and satisfy

```text
37^2 | C195
41^2 | C195.
```

So the q19-square and q41/q37 double-square geometry coexist on a target that is genuinely alive through k31.

## k35 first exit

```text
C35 = 3^2 * 139 * 1181 * 4,659,365,366,269,541.
```

Targets:

```text
Type I  = 26 mod35
Type II = 19 mod35.
```

Explicit witnesses:

```text
d_I  = 1181
     = 26 mod35,

d_II = 15,703,614,099
     = 3^4 * 139 * 1181^2
     = 19 mod35.
```

Both divide `C35^2`, so k35 is the exact first live hit.

## Full Type-II geometry

There are exactly six Type-II divisor witnesses at k35:

```text
interior incomparable : 4
Lopez-A boundary      : 1
Lopez-B boundary      : 1.
```

The smallest Type-II root is

```text
(s,b,c)=(139,10,629,4,659,365,366,269,541)
```

with neither `b|c` nor `c|b`.

Thus the actual first exit exposes mixed full Type-II geometry and genuine non-Lopez interior structure.

## Machine consequence

This anchor proves that the q19-square sublattice is nonempty through k31, the Route-B D-selector state can remain live through k31, and latent q41/q37 double-square geometry can coexist with that ancestry. The sharp next symbolic target is the k35 survivor/absorber grammar on the q19-square corridor.

BEC/BREC may annotate the path after proof. Prime certificates, exact factorizations, divisor masks, and signed-box roots carry the mathematics.
