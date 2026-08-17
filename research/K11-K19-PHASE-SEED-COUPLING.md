# k11 -> k19 phase-seed coupling

**Status:** exact cross-coordinate theorem  
**Date:** 2026-08-17  
**Hard classes:** `p mod840 in {169,289,529}`  
**Application:** q23 Type-I-only predecessor corridor

## 1. The first real bridge between two predecessor coordinates

The class-conditioned k11 theorem gives, for

```text
p mod840 in {169,289,529},
```

```text
sigma_11=-
iff
every prime divisor of C11 is QR mod11.
```

On the q23 parameter

```text
T=(p+23)/24,
```

we have

```text
C11=3(2T-1).
```

Because `3` is a quadratic residue modulo 11, a k11 miss forces

```text
2T-1 is QR mod11.
```

This does not determine `T mod11` uniquely, but it collapses it to five exact phases:

```text
T mod11 in {1,2,3,5,8}.
```

One of those phases injects a new exact factor into the later k19 coordinate.

---

## 2. The selected phase T=2 mod11

At k19,

```text
C19=6T-1.
```

If

```text
T=2 mod11,
```

then

```text
6T-1=11=0 mod11.
```

Therefore

```text
11 | C19.
```

So the exact implication chain is

```text
hard class in {169,289,529}
    + k11 miss
        -> T mod11 in {1,2,3,5,8}

and on the phase T=2:

T=2 mod11
    -> 11 | C19.
```

This is a genuine cross-coordinate coupling. Information extracted from the factor geometry of `C11` changes the exact starting state of the k19 signed-box problem.

---

## 3. Factor 11 is an order-three q19 seed

Use primitive root `2` modulo19.

```text
11 = 2^12 mod19.
```

Moreover

```text
ord_19(11)=3.
```

Hence one literal occurrence of factor11 contributes exact signed exponent support

```text
{0,+12,-12}
 = {0,6,12}
```

inside `Z/18Z`.

Call this subgroup

```text
K={0,6,12}.
```

This is exactly the same subgroup supplied by the h289 forced factor7, because

```text
7=2^6 mod19
```

also has order three.

Thus factor11 and factor7 are different rational primes but identical **target-relevant subgroup seeds** at k19.

---

## 4. The same nine-state quotient appears

Once K is present, every exact signed-box support is K-periodic. Therefore target membership factors through

```text
Z/18Z / K ~= Z/6Z.
```

Write

```text
cbar=c mod6,
Sbar=S mod6.
```

Then

```text
Type II target = 3
Type I target  = 1-cbar mod6.
```

The exact Type-II-miss quotient closure is the same one already derived for h289:

```text
9 quotient states
 = 6 combined misses
 + 3 Type-I-only states.
```

The full seeded q19 closure is

```text
27 states
 = 18 combined misses
 + 9 Type-I-only states,
```

with exactly three full exponent lifts per quotient state.

The verifier reconstructs the seed7 and seed11 closures independently and confirms that their quotient state identities are exactly equal.

---

## 5. Why this matters most for h169 and h529

The hard-class seed atlas at k19 is

```text
h1   -> [5]
h121 -> [5,7]
h169 -> []
h289 -> [7]
h361 -> [5]
h529 -> [].
```

So h169 and h529 have no forced factor5 or7 at k19 from the hard class alone.

But both belong to the k11 class-conditioned QR theorem. Therefore, if a surviving state lands on

```text
T=2 mod11,
```

then the earlier k11 phase creates the missing order-three k19 seed:

```text
h169 or h529
 + k11 miss
 + T=2 mod11
    -> 11 | C19
    -> K={0,6,12}
    -> exact 9-state k19 quotient.
```

This is precisely the kind of dependency BREC was meant to expose: an obstruction coordinate is not merely a historical minus sign. Its arithmetic residue state can constrain the exact state space of a later coordinate.

---

## 6. h289 receives the same seed twice

Hard class289 already forces

```text
7 | C19.
```

So its k19 state always has the K seed and always admits the nine-state quotient.

On the additional phase

```text
T=2 mod11,
```

factor11 is forced as well.

This does not create a smaller quotient automatically because both 7 and11 lie in the same subgroup K. The second factor changes the full product exponent and multiplicity state but does not enlarge the target-relevant quotient subgroup.

That is an exact example of **redundant positive entanglement**: two independent arithmetic causes land on the same finite-state compression.

---

## 7. Exact phase derivation

The five allowed phases can be derived without factoring any integer.

For k11 miss in these hard classes,

```text
2T-1 in QR11={1,3,4,5,9}.
```

Solving

```text
2T-1=r mod11
```

for each QR residue gives

```text
T=(r+1)/2 mod11
```

and therefore exactly

```text
T mod11={1,2,3,5,8}.
```

So a theorem-safe dependency propagator may attach this five-phase set immediately after proving a k11 miss in h169, h289, or h529.

If the CRT phase is already known more precisely, it may collapse directly to one member of this set.

---

## 8. Regression witnesses

The verifier preserves exact primes on the selected phase.

### h169

```text
p=53,089
T=2 mod11
k11 miss
11 | C19
k19 both targets hit.
```

```text
p=71,569
T=2 mod11
k11 miss
11 | C19
k19 Type-II-only.
```

```text
p=80,809
T=2 mod11
k11 miss
11 | C19
k19 combined miss.
```

So the order-three seed does not predetermine the k19 outcome. It compresses the exact outcome space to the nine-state quotient.

### h529

```text
p=5,569
T=2 mod11
k11 miss
C19=1,397=11*127
k19 combined miss.
```

These are regression guards only. The phase/seed implication is universal on the stated class-conditioned branch.

---

## 9. Machine consequence

A class-conditioned predecessor state should now carry at least

```text
hard_class,
T mod11 phase set,
k11 branch,
k19 seed subgroup.
```

For hard classes 169/289/529:

```text
k11 miss
  -> T11 in {1,2,3,5,8}

T11=2
  -> add k19 seed K
  -> replace generic q19 state search by 9-state quotient.
```

For h289 the quotient is already active from the hard-class factor7 seed. For h169/h529 the phase condition activates it dynamically.

This is proof-bearing constraint propagation, not a statistical scheduler heuristic.

---

## 10. Executable verifier

Run

```sh
python3 research/verify_k11_k19_phase_seed_coupling.py
```

The verifier checks:

```text
the five exact T mod11 phases,
T=2 mod11 -> 11|C19,
log_2(11)=12 mod18,
ord_19(11)=3,
seed11 support K={0,6,12},
seed7 and seed11 quotient-state identity,
9-state / 6+3 quotient split,
27-state / 18+9 full split,
and exact prime regressions.
```

---

## 11. Claim boundary

The theorem does **not** say k11 miss forces `T=2 mod11`; it forces a five-element phase set and identifies what happens on one member.

It does not assert every quotient state is realized after the full predecessor ancestry, does not eliminate the known h169 `-----+` witnesses, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
