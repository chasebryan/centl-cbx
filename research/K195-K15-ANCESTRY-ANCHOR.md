# k195 double-square corridor: exact k15 ancestry anchor

**Status:** exact certified prime anchor inside the corrected double-square corridor  
**Date:** 2026-08-16  
**Verifier:** `verify_k195_k15_ancestry_anchor.py`  
**Depends on:** `K195-EARLY-ANCESTRY-SURVIVOR-GRAMMAR.md`, Route-B D-selector support laws, and `K195-DOUBLE-SQUARE-PHASE-SELECTOR.md`.  
**Claim boundary:** one exact prime anchor proving that the combined early-survivor / D-selector / q41-q37 double-square state is arithmetically nonempty through k11. This anchor first hits at k15. It does not prove that any state reaches k195.

## 1. The anchor

Take

```text
s = 59,176.
```

On the corrected double-square corridor

```text
t = 7,423,185,617,863
  + 11,799,129,838,887 s,
```

this gives

```text
t = 698,232,730,531,594,975
p = 169 + 840t
  = 586,515,493,646,539,779,169.
```

The verifier certifies p prime by a Lucas primality certificate from the complete factorization of `p-1`, rather than by a probable-prime test.

The relevant phase coordinates are

```text
tau9  = 7
tau11 = 2
tau13 = 2
tau17 = 6
tau19 = 16
tau23 = 15
tau31 = 7
tau43 = 39
tau47 = 0.
```

So the anchor lies in the corrected phase envelope and in the k195 miss-compatible tau13 side.

## 2. Early ancestry: k3 miss

```text
C3 = 146,628,873,411,634,944,793
```

is prime and

```text
C3 = 1 mod3.
```

Therefore every prime factor of C3 is1 mod3 and the exact k3 support theorem gives a miss.

## 3. Early ancestry: k7 miss

```text
C7 = 146,628,873,411,634,944,794
   = 2 * 73,314,436,705,817,472,397.
```

The large factor is prime, and modulo7 the factor residues are

```text
2,1.
```

Both lie in

```text
QR7={1,2,4}.
```

Thus the anchor is in the exact k7 `QR7` survivor mode.

## 4. Early ancestry: k11 miss

```text
C11 = 146,628,873,411,634,944,795
    = 3 * 5 * 9,775,258,227,442,329,653.
```

The last factor is prime. Modulo11 the prime-factor residues are

```text
3,5,9,
```

all in

```text
QR11={1,3,4,5,9}.
```

The exact divisor mask is therefore QR11 itself. At `tau11=2`, center3, QR11 is one of the landed exact k11 miss states.

So the anchor survives k11 with normalized early state

```text
C3_support = ONE_MOD3
C7_mode    = QR7
k11_state  = (tau11=2, mask=QR11).
```

This proves that the early survivor grammar is arithmetically realizable; it is not merely a formal product state.

## 5. The intended Route-B D-selector support is present

### k19 / R reservoir

```text
C19 = 23 * 47 * 49,891 * 2,718,764,527,607.
```

Since `23*47=1081`,

```text
R = 49,891 * 2,718,764,527,607.
```

Modulo19 the residues are

```text
16,1.
```

Both are QR19 and the first is outside the BARE 1-residue state, so this is a FULL_QR k19 support state.

### k23 / B reservoir

```text
C23 = 2*3*13*29*127*510,414,703,076,627.
```

Thus

```text
B = C23/6
```

has prime residues modulo23

```text
13,6,12,6,
```

all QR23.

### k27 / E reservoir

```text
C27 = 7*17*31*39,747,593,768,401,991.
```

Hence

```text
E = 17*31*39,747,593,768,401,991.
```

The final prime is

```text
2 mod27.
```

So this is exactly the D-selector factor grammar

```text
E = 17*31*r,
r prime,
r=2 mod27.
```

### k31 / D reservoir

```text
C31 = 2^5 * 5^2 * 41 * 4,470,392,482,062,041.
```

Thus

```text
D=C31/10
```

has only QR31 prime residues, including the materialized renewed source

```text
q_D=41,
41=10 mod31.
```

Residue10 lies outside the BARE stabilizer `{1,5,25}`, so this is FULL_QR.

### k47 / J reservoir

```text
C47 = 2^2 * 3 * 37 * 661 * 499,614,539,162,731.
```

Thus

```text
J=C47/6
```

has only QR47 prime residues and contains the materialized renewed source

```text
q_J=37.
```

So the exact Route-B D-selector support architecture is present at this anchor.

## 6. The double-square destination geometry is also present

At k195,

```text
C195
 = 7 * 37^2 * 41^2 * 67 * 277 * 490,451,113.
```

Therefore

```text
37^2 | C195
41^2 | C195.
```

The anchor is not merely on the phase progression. It realizes the intended q37/q41 double-square divisibility geometry exactly.

## 7. But full ancestry stops at k15

At

```text
k=15,
```

we have

```text
C15
 = 2^2 * 97 * 377,909,467,555,760,167.
```

The exact targets are

```text
Type I  = 11 mod15
Type II = 14 mod15.
```

Two explicit divisors of `C15^2` are

```text
d_I  = 776 = 2^3*97
d_II = 194 = 2*97.
```

They satisfy

```text
d_I  = 11 mod15
d_II = 14 mod15.
```

Hence k15 contains both Type-I and Type-II witnesses.

The exact ancestry path of this anchor is therefore

```text
k3  miss
k7  miss
k11 miss
k15 HIT (I+II).
```

It never reaches k195 alive.

## 8. Why this anchor matters

This settles an important ambiguity created by the finite prefix audit.

The early k3/k7/k11 survivor grammar is **not empty** when coupled to the intended later D-selector / q41-q37 double-square support state. There are genuine prime targets in that combined state.

Therefore a proof that k195 is ancestry-dead cannot stop at k11.

The next symbolic ancestry layer must include k15 and later shifts.

At the same time, this anchor shows exactly what the desired mechanism looks like: a highly structured double-square state can still be solved far earlier by a small signed box.

## 9. Bryan Entanglement Cross boundary

This anchor gives a concrete directional history:

```text
up (+/-): later q41/q37 double-square geometry exists
left/down: early ancestry restrictions survive through k11
a sharp right (+): k15 supplies an exact I+II decomposition exit.
```

The BEC path is descriptive only. The prime certificates, exact factorization, and signed-box divisors carry the proof.
