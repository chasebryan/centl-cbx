# k11-conditioned post-k23 forced-factor calendar

**Status:** exact cross-coordinate congruence theorem  
**Date:** 2026-08-17  
**Coordinate:** `T=(p+23)/24`  
**Ladder:** `C_(23+4j)=6T+j`

## 1. k11 obstruction leaves a finite phase set

The exact k11 combined-miss theorem already classifies the factor geometry of

```text
C11=3(2T-1).
```

Its product residue also gives a clean phase statement for the common corridor parameter `T`.

### Pure-QR k11 miss

If every prime divisor of `C11` is QR modulo11, then

```text
2T-1 in QR11={1,3,4,5,9}.
```

Solving for `T` gives

```text
T mod11 in {1,2,3,5,8}.
```

### Thin k11 combined misses

The three nonempty thin miss packets give

```text
(a2,a6)=(1,0)  -> 2T-1=2 mod11 -> T=7 mod11
(a2,a6)=(0,1)  -> 2T-1=6 mod11 -> T=9 mod11
(a2,a6)=(1,1)  -> 2T-1=1 mod11 -> T=1 mod11.
```

Therefore every k11 combined miss satisfies

```text
T mod11 in {1,2,3,5,7,8,9}.
```

For hard classes

```text
169,289,529 mod840,
```

the thin branch has already been excluded exactly, so only

```text
{1,2,3,5,8}
```

remain.

---

## 2. The same phase controls the future ladder

After k23 the cofactors are

```text
C_(23+4j)=6T+j.
```

For fixed `T mod11`, factor11 enters exactly when

```text
6T+j=0 mod11.
```

Choosing the first positive `j` gives the exact calendar

```text
T mod11    first j with 11 | (6T+j)    shift k
-------------------------------------------------
9                     1                  27
7                     2                  31
5                     3                  35
3                     4                  39
1                     5                  43
8                     7                  51
2                    10                  63.
```

Hence:

```text
k11 combined miss
=>
literal factor11 appears in the post-k23 ladder by k=63.
```

This is universal on the exact k11 miss domain. It is not a finite census statement.

---

## 3. Thin k11 packets point directly at k27 and k31

The two oriented one-defect packets are particularly striking.

```text
thin (0,1)
    -> T=9 mod11
    -> 11 | C27=6T+1.
```

```text
thin (1,0)
    -> T=7 mod11
    -> 11 | C31=6T+2.
```

Those are exactly the first two post-k23 absorber candidates already emphasized by the companion-ladder program.

The mixed thin packet gives

```text
thin (1,1)
    -> T=1 mod11
    -> 11 | C43=6T+5.
```

Thus the orientation of the q11 defect is not only a local k11 label. It predicts the exact future ladder position at which rational prime11 reappears.

---

## 4. Hard classes already provide a 5/7 calendar

The six hard classes fix `T mod35`, so factor5 and factor7 also enter the post-k23 ladder on deterministic schedules.

```text
p mod840   T mod35   first factor5   first factor7
---------------------------------------------------
1              1       j=4 k39         j=1 k27
121            6       j=4 k39         j=6 k47
169            8       j=2 k31         j=1 k27
289           13       j=2 k31         j=6 k47
361           16       j=4 k39         j=2 k31
529           23       j=2 k31         j=2 k31.
```

So hard529 universally has

```text
35 | C31.
```

This holds independently of the k11 phase.

---

## 5. Combine k11 phase and hard class by CRT

Since

```text
gcd(35,11)=1,
```

each pair

```text
(T mod35, T mod11)
```

defines one exact phase modulo

```text
385.
```

That phase determines every forced occurrence of the small primes

```text
5,7,11
```

in the first ten post-k23 companions.

The verifier exhausts every allowed hard-class/k11-phase pair and records the complete injection schedule through

```text
j=10,
k=63.
```

This is a finite state table generated from universal congruence identities, not from a bounded prime search.

---

## 6. Exact multi-prime coincidences

Some phase/hard-class combinations make two or more small-prime seeds arrive at the same companion.

### h529 at k31

For every k11 phase allowed in h529,

```text
5*7=35 | C31.
```

The q11 thin branch is impossible in h529, so factor11 does not coincide at j2 there. The universal seed is exactly the hard-class `35` seed before any additional factorization is examined.

### h1 + thin (0,1) at k27

Hard1 forces factor7 into `C27`.

The thin q11 packet `(0,1)` forces

```text
T=9 mod11,
```

and therefore factor11 into the same `C27`.

Hence

```text
h1 + k11 thin(0,1)
=>
7*11=77 | C27.
```

### h361 + thin (1,0) at k31

Hard361 forces factor7 into `C31`.

The thin packet `(1,0)` forces

```text
T=7 mod11,
```

and therefore factor11 into `C31`.

Thus

```text
h361 + k11 thin(1,0)
=>
77 | C31.
```

### Pure phase T=3 mod11 at k39

For hard classes whose factor5 calendar also lands at j4, the pure q11 phase

```text
T=3 mod11
```

forces

```text
5*11=55 | C39.
```

The verifier records all such coincidences rather than promoting only the visually attractive ones.

---

## 7. Relation to the existing companion-ladder theorem

The companion-ladder module proved

```text
C_j=C23+j=6T+j
```

and the support-renewal laws

```text
gcd(C_j,C23)=gcd(j,C23),
gcd(C_j,C19)=gcd(j+1,C19).
```

The new calendar adds a different kind of information.

Support renewal says which old primes can be inherited.

The phase calendar says which **new rational small primes are guaranteed to appear** because of arithmetic information propagated from an earlier BREC coordinate.

Together:

```text
ancestry state
    -> T phase
        -> deterministic small-prime injection
            + support-renewal bound
                -> exact later signed-box seed.
```

That is substantially closer to an executable decomposition grammar than treating each later shift as an independent factorization problem.

---

## 8. Why factor injection is not yet an absorber theorem

A forced factor is only a seed.

For example, factor11 can be QR, NR, inert, or subgroup-generating depending on the later modulus. Its mere presence does not imply that Type I or Type II hits.

Therefore the theorem is **not**

```text
k11 miss -> construction by k63.
```

The exact statement is only

```text
k11 miss -> factor11 enters some post-k23 cofactor by k63.
```

The value comes from feeding a deterministic seed into already-developed exact later-shift automata and normal forms.

The next step is to intersect this calendar with the k27/k31/k35/k39/k43/k51/k63 signed-box geometries and ask which seed/phase combinations become automatic absorbers.

---

## 9. Executable verifier

Run

```sh
python3 research/verify_k11_post_k23_forced_factor_calendar.py
```

It verifies:

```text
the pure-QR q11 T-phase set,
the three thin packet phases,
the complete seven-phase k11 miss union,
the first positive factor11 ladder position,
the hard-class factor5/factor7 calendar,
all CRT phases modulo385,
all 5/7/11 injections through j10,
and selected multi-prime coincidences.
```

---

## 10. Claim boundary

This theorem is an exact cross-coordinate congruence calendar.

It does not say that a forced small factor is itself a Lane-I certificate, does not prove construction by k63, does not establish a universal finite Lane-I ceiling, and does not prove Erdős–Straus.
