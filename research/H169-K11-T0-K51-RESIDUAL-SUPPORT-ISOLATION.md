# h169 k11 t=0 -> k51 residual support isolation

**Status:** exact simultaneous-support theorem  
**Date:** 2026-08-17  
**Verifier:** `verify_h169_k11_t0_k51_residual_support_isolation.py`  
**Depends on:** `H169-K11-T0-K51-JACOBI-NORMAL-FORM.md`

## 1. The k51 shield reservoir can be separated from the companion block

On the h169 k11 child

```text
t=0 mod11,
```

write

```text
t=11u.
```

The canonical k51 normal form gives

```text
C51=55R
R=1+42u.
```

The k51 combined-miss condition is already exact:

```text
k51 combined miss
iff
every residual prime-factor occurrence of R lies in H51.
```

The next simultaneous question is whether those residual factors can be recycled from the neighboring Lane-I cofactors.

They almost cannot.

---

## 2. Every companion through k55 is affine in the same u

For every Lane-I shift

```text
k in {3,7,11,15,19,23,27,31,35,39,43,47,51,55},
```

we have

```text
Ck=(p+k)/4
  =ak+2310u,

ak=(169+k)/4.
```

For `k !=51`, any common divisor of `R` and `Ck` must divide the fixed determinant

```text
2310R - 42Ck
=
2310 - 42ak.
```

Meanwhile

```text
R=1+42u
```

satisfies identically

```text
R=1 mod2
R=1 mod3
R=1 mod7.
```

So every factor 2,3,7 in the determinant is automatically unavailable to the residual.

---

## 3. Exact determinant table

The fixed determinant values are

```text
k=3   :  504 = 2^3 * 3^2 * 7
k=7   :  462 = 2 * 3 * 7 * 11
k=11  :  420 = 2^2 * 3 * 5 * 7
k=15  :  378 = 2 * 3^3 * 7
k=19  :  336 = 2^4 * 3 * 7
k=23  :  294 = 2 * 3 * 7^2
k=27  :  252 = 2^2 * 3^2 * 7
k=31  :  210 = 2 * 3 * 5 * 7
k=35  :  168 = 2^3 * 3 * 7
k=39  :  126 = 2 * 3^2 * 7
k=43  :   84 = 2^2 * 3 * 7
k=47  :   42 = 2 * 3 * 7
k=55  :  -42 = -2 * 3 * 7.
```

After the permanent `R mod2,3,7` exclusions, only three possible overlap channels survive:

```text
k7  : prime11
k11 : prime5
k31 : prime5.
```

Everything else is exactly coprime to `R`.

---

## 4. The three exceptions are exact, not merely possible

At k7,

```text
C7=44+2310u
```

is always divisible by11.

Also

```text
R=1+42u
 =1+9u mod11.
```

Therefore

```text
11|R
iff
u=6 mod11.
```

Because the determinant contains only one factor11,

```text
gcd(R,C7)=11  iff u=6 mod11,
gcd(R,C7)=1   otherwise.
```

At k11 and k31,

```text
C11=45+2310u
C31=50+2310u
```

are both always divisible by5.

Since

```text
R=1+42u
 =1+2u mod5,
```

we have

```text
5|R
iff
u=2 mod5.
```

Again the determinants contain only one factor5, so

```text
gcd(R,C11)=gcd(R,C31)=5  iff u=2 mod5,
```

and both gcds are1 otherwise.

---

## 5. Exact support-isolation theorem

Hence on this selected h169 child,

```text
gcd(R,C3)=1
gcd(R,C15)=1
gcd(R,C19)=1
gcd(R,C23)=1
gcd(R,C27)=1
gcd(R,C35)=1
gcd(R,C39)=1
gcd(R,C43)=1
gcd(R,C47)=1
gcd(R,C55)=1.
```

The only possible shared residual support in the entire Lane-I window through k55 is

```text
11 shared with C7,
5  shared with C11,
5  shared with C31,
```

and even those occur only on their exact `u` phases above.

A particularly useful corollary is

```text
q>11 and q|R
->
q divides no other Ck through k55, k!=51.
```

More sharply, every prime `q` dividing `R` other than 5 or11 is private to k51 throughout this window.

---

## 6. The exceptional overlaps are locally admissible

The three small overlap channels do not themselves create a contradiction with the landed local miss laws:

```text
11 mod7 =4,
```

which is a quadratic residue modulo7;

```text
5 mod11 =5,
```

which is a quadratic residue modulo11;

and

```text
5 mod31=5 in H31={1,5,25},
```

which is the landed thin k31 support subgroup.

So the theorem does not manufacture a false contradiction from the only small shared factors.

Instead it says something structurally stronger:

```text
the large-prime part of the k51 H51 escape reservoir is genuinely private.
```

---

## 7. Why this sharpens the termination target

The persistent-shield theorem showed that local k51 geometry cannot cap repeated factor11 valuation.

The Jacobi normal form showed that a combined miss requires all residual factors to remain in `H51`.

This theorem now adds:

```text
except for 5 and11,
that residual support cannot be inherited from any other early companion.
```

Therefore a deep k51 combined miss must continually build its own H51-supported factorization rather than recycle the large odd support of neighboring cofactors.

The surviving object is becoming increasingly expensive:

```text
H51-only residual support
+ almost complete support isolation
+ exact t17 phase restriction
+ neighboring independent miss obligations.
```

That is precisely the simultaneous arithmetic pressure we want to make collide.

---

## 8. The next theorem target

The most valuable next question is now narrower than “puncture H51 somehow.”

Ask:

```text
Can the other early miss normal forms force a character condition on the
private prime divisors of R that is incompatible with H51?
```

Because the private factors cannot appear in the neighboring cofactors themselves, any such condition must arrive through reciprocity, CRT ancestry, product character, or a companion relation rather than direct factor sharing.

A successful theorem of the form

```text
simultaneous earlier misses
-> some q|R has Jacobi(q/51)=-1
```

would immediately puncture the canonical k51 shield and kill this branch.

---

## 9. Executable verification

Run

```sh
python3 research/verify_h169_k11_t0_k51_residual_support_isolation.py
```

The verifier checks:

```text
the canonical t11=0 k51 residual identity,
the complete determinant table,
R mod2=R mod3=R mod7=1,
all ten unconditional coprimalities,
the exact k7/11 overlap phase,
the exact k11/5 overlap phase,
the exact k31/5 overlap phase,
and compatibility of the three exceptional factors with the landed k7/k11/k31 support shields.
```

---

## 10. Claim boundary

This theorem does not force any prime divisor of `R` outside `H51`.

It therefore does not kill the k51 Jacobi shield and does not prove termination.

It proves that the shield's large-prime residual support is isolated from every other Lane-I companion through k55. That converts “consecutive cofactors are coupled” into an exact negative-sharing law on the hardest surviving k51 child.

No finite Lane-I ceiling or Erdős-Straus proof is claimed here.
