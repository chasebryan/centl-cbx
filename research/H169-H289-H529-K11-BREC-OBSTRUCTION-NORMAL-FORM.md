# h169 / h289 / h529 k=11 BREC obstruction normal form

**Status:** exact class-conditioned fixed-shift theorem  
**Date:** 2026-08-17  
**Hard classes:** `p mod840 in {169,289,529}`  
**Application:** `CBX-Lane-I-shift-history-v1`

## 1. Statement

Let `p` be a Mordell-hard prime with

```text
p mod840 in {169,289,529}
```

and define

```text
C11 = (p+11)/4.
```

Then

```text
sigma_11(p) = -
```

if and only if every prime divisor of `C11` is a quadratic residue modulo `11`.

Equivalently, in these three hard classes:

```text
k11 Type-II miss
=> k11 Type-I miss.
```

The two thin q11 Type-I-only rescue packets that exist in the unrestricted Mordell-hard k11 theorem cannot occur here.

---

## 2. The forced factor that kills the thin branch

On the q23-compatible parameterization

```text
T=(p+23)/24,
```

the six Mordell-hard classes correspond to fixed residues modulo 35. For the three classes in this theorem:

```text
p mod840   T mod35
------------------
169            8
289           13
529           23.
```

All three satisfy

```text
T = 3 mod5.
```

Therefore

```text
2T-1 = 0 mod5.
```

Since

```text
C11 = 3(2T-1),
```

the literal rational prime `5` is forced into `C11` in every one of these hard classes.

This is not a finite pattern. It is a congruence identity on the entire hard class.

---

## 3. Recall the complete general q11 Type-II miss geometry

The exact general k11 theorem leaves only two Type-II-miss branches.

### Branch A: pure QR

Every prime divisor of `C11` is a quadratic residue modulo 11.

### Branch B: thin primitive

```text
v3(C11)=1,
every other QR prime divisor is 1 mod11,
primitive NR factors occur only in classes 2 and 6 mod11,
total primitive-NR valuation <=2.
```

There are no other Type-II miss geometries.

The Type-I companion theorem further says that, inside Branch B, only the same-class valuation-two packets

```text
(2,0)
(0,2)
```

are Type-I-only rescues.

---

## 4. Literal prime 5 excludes Branch B

Modulo 11,

```text
5 is a quadratic residue,
5 != 1 mod11.
```

Indeed,

```text
QR11 = {1,3,4,5,9}.
```

But Branch B requires every QR prime divisor other than the forced prime `3` to be exactly

```text
1 mod11.
```

The hard-class-forced literal prime `5` violates that requirement immediately.

Therefore:

```text
Branch B is impossible
```

for every prime in hard classes 169, 289, and 529.

A k11 Type-II miss in these classes can only be Branch A, the pure-QR branch.

---

## 5. Pure QR automatically misses Type I

At fixed shift 11,

```text
p = 4C11 mod11.
```

If every prime divisor of `C11` is QR modulo 11, then `C11` is QR. Since `4` is also QR,

```text
p is QR mod11.
```

Because

```text
11 = 3 mod4,
```

`-1` is a quadratic nonresidue modulo 11. Thus both exact targets

```text
Type II : -1
Type I  : -p^(-1)
```

are nonresidues, while the entire signed box remains in the QR subgroup.

Hence both targets miss.

Combining this with the exclusion of the thin branch proves

```text
sigma_11(p) = -
iff
every prime divisor of C11 is QR mod11
```

for

```text
p mod840 in {169,289,529}.
```

---

## 6. Independent finite-state cross-check

The literal factors forced at k11 are

```text
3 and 5.
```

Seeding the exact q11 Type-II-miss residue automaton with

```text
[3,5]
```

gives the complete local closure

```text
5 Type-II-miss states
5 combined-miss states
0 Type-I-only states
5 QR-only combined-miss states.
```

So the independently written finite-state machine reaches the same conclusion: once the hard-class seed `[3,5]` is installed, the second target never rescues a Type-II miss.

The automaton is a cross-check. The theorem itself follows symbolically from the complete general q11 branch classification plus the forced literal factor 5.

---

## 7. Exact regression witnesses

The verifier preserves both sides of the theorem in each hard class.

### h169

```text
p=2,689
C11=675=3^3*5^2
all factors QR mod11
=> k11 miss.
```

```text
p=1,009
C11=255=3*5*17
17=6 mod11 is NR
=> k11 construction.
```

### h289

```text
p=12,049
C11=3,015=3^2*5*67
67=1 mod11
=> k11 miss.
```

```text
p=1,129
C11=285=3*5*19
19=8 mod11 is NR
=> k11 construction.
```

### h529

```text
p=5,569
C11=1,395=3^2*5*31
31=9 mod11
=> k11 miss.
```

```text
p=3,049
C11=765=3^2*5*17
17=6 mod11 is NR
=> k11 construction.
```

These examples are regression guards only. They are not used to establish the universal class-conditioned theorem.

---

## 8. Cross-coordinate significance

This is the first new simplification produced by combining the q23 corridor parameter `T`, a Mordell-hard residue class, and the exact q11 branch grammar.

The general q11 obstruction has two geometries:

```text
pure QR
or thin primitive.
```

But half of the six hard classes split cleanly:

```text
h169, h289, h529
    -> forced factor 5 in C11
        -> thin branch impossible
            -> pure QR is the only k11 obstruction.
```

That means the q23 predecessor grammar should no longer carry the generic q11 thin packets in these three lanes.

The remaining hard classes

```text
1,121,361
```

retain the generic q11 possibility and must be treated separately.

---

## 9. Executable verifier

Run

```sh
python3 research/verify_h169_h289_h529_k11_brec_obstruction_normal_form.py
```

The verifier checks:

```text
the hard-class T mod35 map,
T=3 mod5 in all three classes,
forced literal factors 3 and 5 in C11,
quadratic character of 5 modulo11,
seeded [3,5] q11 automaton closure,
and exact signed-box regression primes on both sides in all three classes.
```

---

## 10. Claim boundary

This theorem is exact only for

```text
p mod840 in {169,289,529}.
```

It does not classify the complete k11 obstruction in hard classes `1`, `121`, or `361`, does not prove incompatibility with the other predecessor coordinates, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
