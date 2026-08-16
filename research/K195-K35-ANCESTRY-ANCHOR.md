# k195 / q19-square corridor: exact k35 ancestry anchor

**Status:** exact certified prime anchor inside the Route-B D-selector / q19-square / q41-q37 double-square laboratory  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_k35_ancestry_anchor.py`  
**Depends on:** the landed k15 Route-B source theorem, k15-origin q19 square-lift gate, D-selector support grammar, k195 double-square selector, and full Type-II geometry classifier.  
**Claim boundary:** one exact prime anchor. It proves that the combined corridor can survive every admissible signed box through k31 and first exit at k35. It does not prove a universal k35 ceiling or any state reaches k167/k195 alive.

## 1. Anchor

Use the normalized k195 double-square corridor

```text
t = 7,423,185,617,863
  + 11,799,129,838,887 s.
```

Take

```text
s = 2,778,207
  = 312 mod361.
```

Then

```text
t = 32,780,432,535,490,353,472
p = 169 + 840t
  = 27,535,563,329,811,896,916,649.
```

The verifier proves p prime by a Lucas certificate from the complete factorization of `p-1`.

Relevant phases are

```text
tau9  = 7
tau11 = 0
tau13 = 5
tau17 = 6
tau19 = 11
tau23 = 15
tau31 = 7
tau43 = 18
tau47 = 0.
```

Thus the anchor is on the landed k15-origin q19 square-lift subphase and on the q41/q37 double-square corridor.

## 2. Exact ancestry through k31

The companion factorizations are:

```text
C3
 = 6,883,890,832,452,974,229,163
   [prime]

C7
 = 2^2 * 11 * 53 * 277 * 27,486,439 * 387,710,159

C11
 = 3 * 5 * 223 * 2,057,964,374,425,403,357

C15
 = 2 * 19 * 181,155,021,906,657,216,557

C19
 = 23 * 43 * 47 * 6,139,547 * 24,121,454,767

C23
 = 2^4 * 3 * 112,486,999 * 1,274,941,936,559

C27
 = 7 * 17 * 31 * 1,866,058,778,111,405,321

C31
 = 2 * 5 * 41 * 122,117 * 137,490,911,503,961.
```

The exact divisor-square masks are:

```text
k3  : {1}
k7  : {1,2,4}
k11 : {1,3,4,5,9}
k15 : {1,2,4,8}
k19 : QR19
k23 : exact 11-residue miss mask
k27 : exact D-mode miss mask
k31 : QR31.
```

None contains either fixed-shift target at its k. Therefore

```text
k3,k7,k11,k15,k19,k23,k27,k31
```

all miss exactly.

## 3. The early q19 source and its square lift are real

At k15,

```text
C15 = 2 * 19 * 181,155,021,906,657,216,557.
```

Every factor lies in the unique h169 k15 Jacobi-positive survivor state. The factor19 satisfies

```text
(19/15)=+1
```

and, because `19|C15`, companion-source orientation gives

```text
(19/p)=+1.
```

At k167,

```text
C167
 = 2^2 * 3 * 7 * 19^2 * 61 * 3,721,496,813,892,461.
```

Hence

```text
19^2 | C167.
```

So this is not merely a phase-compatible q19-square state. The source and the square lift are both arithmetically materialized.

The anchor nevertheless never reaches k167 alive, because k35 terminates it first.

## 4. The Route-B D-selector state is realized through k31

### k19

Since `C19=23*47*R`,

```text
R = 43 * 6,139,547 * 24,121,454,767.
```

Their residues modulo19 are

```text
5,1,17,
```

all QR19. Since residues outside1 occur, this is FULL_QR rather than BARE.

### k23

Since `C23=6B`,

```text
B = 2^3 * 112,486,999 * 1,274,941,936,559.
```

The prime residues modulo23 are

```text
2,2,6,
```

all QR23.

### k27

Since `C27=7E`,

```text
E = 17 * 31 * r,
r = 1,866,058,778,111,405,321.
```

The final factor is prime and

```text
r = 2 mod27.
```

Thus the exact D-selector factor grammar is present:

```text
E=17*31*r,
r prime,
r=2 mod27.
```

### k31

Since `C31=10D`,

```text
D = 41 * 122,117 * 137,490,911,503,961.
```

Their residues modulo31 are

```text
10,8,5,
```

all QR31. The factor41 lies outside the BARE stabilizer `{1,5,25}`, so k31 is FULL_QR and the renewed source

```text
q_D=41
```

is materialized.

## 5. The later q37/q41 double-square geometry is present

At k47,

```text
C47
 = 2 * 3 * 37 * 31,008,517,263,301,685,717.
```

Thus

```text
J=C47/6
 = 37 * 31,008,517,263,301,685,717,
```

and both factors are QR47. The renewed source

```text
q_J=37
```

is materialized in the later companion geometry.

At k195,

```text
C195
 = 7 * 37^2 * 41^2 * 12,113 * 13,763 * 2,563,303.
```

Hence

```text
37^2 | C195
41^2 | C195.
```

So the intended k195 double-square valuation structure exists exactly on this same prime target, even though ancestry terminates much earlier.

## 6. First live exit: k35

At k35,

```text
C35
 = 3^2 * 139 * 1181 * 4,659,365,366,269,541.
```

The exact targets in the divisor-square representation are

```text
Type I  = 26 mod35
Type II = 19 mod35.
```

Explicit witnesses are

```text
d_I  = 1181
      = 26 mod35,

d_II = 15,703,614,099
      = 3^4 * 139 * 1181^2
      = 19 mod35.
```

Both divide `C35^2`. Therefore

```text
k35 = HIT (Type I + Type II).
```

Since every earlier admissible shift misses, k35 is the exact first live exit.

## 7. Full Type-II geometry at the exit

There are exactly six Type-II divisor witnesses at k35.

Their root-geometry classification is

```text
interior incomparable : 4
López-A boundary      : 1
López-B boundary      : 1.
```

So the k35 Type-II geometry is **mixed**, not boundary-only.

The smallest Type-II witness above has root data

```text
(s,b,c)
 = (139, 10,629, 4,659,365,366,269,541).
```

It satisfies

```text
C35 = s*b*c,
d_II = s*b^2,
```

and

```text
b does not divide c,
c does not divide b.
```

Thus an explicit incomparable interior Type-II root occurs at the actual first exit.

This is precisely the geometry that a López-only interpretation would fail to represent as the governing state.

## 8. Machine consequence

This anchor proves all of the following simultaneously:

```text
q19-square sublattice is nonempty through k15;
Route-B D-selector state can survive through k31;
q41/q37 later double-square geometry can coexist with that ancestry;
first live exit can occur at k35;
that exit can expose genuine incomparable Type-II geometry.
```

Therefore the next ancestry theorem cannot stop at k15, and the q19/k167 bridge cannot be treated as automatically live merely because its phase is compatible.

The sharp symbolic target is now the exact k35 survivor/absorber grammar on the q19-square corridor.

## 9. Bryan Entanglement Cross boundary

A faithful observational path is

```text
down (-/+): early ancestry excavates through eight misses
up (+/-):   q19/q41/q37 valuation geometry remains latent
right (+):  k35 terminates constructively
up/right:   the live Type-II exit exposes mixed boundary/interior geometry.
```

The BEC path is descriptive. Prime certificates, exact factorizations, divisor masks, and signed-box roots carry the proof.
