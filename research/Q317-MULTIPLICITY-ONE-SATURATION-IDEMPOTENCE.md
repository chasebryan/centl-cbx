# q317 multiplicity-one saturation idempotence

**Status:** exact finite closure for the q317 source extracted by the q29 tenth-lift branch  
**Date:** 2026-08-16  
**Verifier:** `verify_q317_multiplicity_one_saturation_idempotence.py`  
**Depends on:** `D-SELECTOR-Q29-TENTH-LIFT-SATURATION.md`, h169 class-seed arithmetic, and the landed h169 positive-source atlas.  
**Claim boundary:** this theorem classifies multiplicity-one Jacobi saturation by the extracted source q317. Higher 317-adic lifts, additional routed factors, exact-state promotion, and direct signed-box mechanisms remain live. This is not a termination theorem or Erdős–Straus proof.

## 1. Input state

A miss on the landed q29 tenth-lift branch at k951 forces

```text
(317/p)=+1.
```

Thus q317 becomes a positive target-prime character source.

To route q317 into `C_k`, we require

```text
p = -k mod317.
```

Because `317=1 mod4`, `(-1/317)=+1`. Hence `(317/p)=+1` is equivalent, by reciprocity, to p being a nonzero quadratic residue modulo317, and the routed residue `-k mod317` is also quadratic-residue.

So the q317 route branches are exactly the admissible shifts with

```text
-k in QR(317).
```

## 2. Multiplicity-one cardinality bound

At h169 destination k, the bare seed with one copy of q317 is

```text
S(k)=lcm(gcd(210,(169+k)/4),317).
```

It has at most five distinct prime factors, so `S^2` has at most

```text
3^5=243
```

divisors.

A Jacobi-saturating seed at odd `k=3 mod4` must fill a kernel of size `phi(k)/2`, so

```text
phi(k)<=486.
```

Since k is odd, `phi(k)^2>=k`, giving the exact finite bound

```text
k<=486^2=236196.
```

## 3. Complete q317 route closure

The verifier exhausts every admissible k in this rigorous bound satisfying both

```text
phi(k)<=486
-k in QR(317).
```

There are

```text
158 low-totient admissible shifts total
76 compatible q317 route shifts
```

and exactly five multiplicity-one q317 saturations:

```text
k=7   base=2
k=11  base=15
k=15  base=2
k=23  base=6
k=31  base=10.
```

No other multiplicity-one q317 route destination Jacobi-saturates.

## 4. Saturated-miss output is character-idempotent

At each of the five saturating destinations, a hit remains constructive. But if the fixed shift misses, the Jacobi-saturation theorem only returns character information already present in the landed h169 state.

### k=7

A saturated miss gives

```text
(7/p)=+1.
```

This is already fixed by the h169 hard class because `p=169 mod840` gives `p=1 mod7`.

### k=11

A saturated miss gives

```text
(11/p)=+1.
```

q11 is already a landed positive h169 character source.

### k=15=3*5

A saturated miss gives

```text
(15/p)=+1,
```

which is already determined by the hard-class mod3 and mod5 data.

### k=23

A saturated miss gives

```text
(23/p)=+1,
```

already present in the h169 source set.

### k=31

A saturated miss gives

```text
(31/p)=+1,
```

also already present in the h169 source set.

Therefore the multiplicity-one q317 Jacobi-saturation layer is **character-idempotent**:

> it can terminate by hit, but a miss does not enlarge the current fixed positive-character alphabet.

## 5. Machine consequence

After q317 extraction, the scheduler may classify multiplicity-one saturation branches as

```text
q317 route
  |
  +-- k in {7,11,15,23,31}
  |      +-- hit  -> constructive certificate
  |      `-- miss -> CHARACTER_IDEMPOTENT
  |
  `-- every other multiplicity-one route
         -> NOT_JACOBI_SATURATING.
```

This prevents an artificial recursive character cascade in which q317 is treated as though every saturated miss must generate another new source.

Higher `317^e` valuation states are not covered and must remain live.

## 6. Bryan Entanglement Cross boundary

The q29 tenth lift is a rightward constructive event because it either hits or creates q317. The q317 multiplicity-one follow-up is mixed:

- the five saturated branches remain rightward-capable through direct hit;
- their miss branches loop back into already-known character state;
- the other branches are multiplicity-one saturation obstructions.

BEC/BREC can annotate this shape but cannot infer idempotence or pruning.

## 7. Next target

The next useful q317 question is not another multiplicity-one saturation scan. It is either:

1. a q317-adic lift analysis, using the general valuation ladder; or
2. exact-state promotion / incoming repulsion using q317 as an additional positive factor.

The scheduler should prioritize whichever mechanism creates a genuinely new proof-state coordinate rather than recycling the existing character alphabet.
