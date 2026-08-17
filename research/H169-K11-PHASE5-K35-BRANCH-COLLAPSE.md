# h169 k11 phase-5 -> k35 branch collapse

**Status:** exact cross-coordinate branch theorem  
**Date:** 2026-08-17  
**Hard class:** `p=169 mod840`  
**Phase:** `T=(p+23)/24 = 5 mod11`

## 1. Statement

On h169, the exact k35 survivor theorem is

```text
k35 miss
iff
J35(F) OR S7(F),
```

where

```text
C35=3F,
F=2T+1.
```

On the exact phase

```text
T=5 mod11,
```

literal prime11 divides `F`.

But

```text
11=4 mod7.
```

The S7 branch permits exactly one prime-factor occurrence congruent to `3 mod7` and requires every other occurrence to be `1 mod7`. A forced factor `11=4 mod7` is incompatible with S7.

Therefore

```text
h169 + T=5 mod11
=>
S7(F)=false
```

and the complete k35 theorem collapses to

```text
k35 miss iff J35(F).
```

This is range-free and uses no prime census.

---

## 2. Why phase 5 is naturally produced by k11 ancestry

The h169 hard class belongs to the class-conditioned k11 collapse:

```text
p mod840 in {169,289,529}
=>
k11 miss iff C11 is pure QR mod11.
```

Writing

```text
C11=3(2T-1),
```

a k11 miss restricts

```text
T mod11 in {1,2,3,5,8}.
```

So phase5 is one of only five exact children of an h169 k11 obstruction.

The theorem here resolves that child at the later k35 branch:

```text
k11 miss
  -> T11 in {1,2,3,5,8}

T11=5
  -> 11 | F=C35/3
  -> S7 impossible
  -> k35 miss iff J35.
```

BREC ancestry has therefore removed one of the two exact k35 survivor mechanisms on this phase.

---

## 3. Arithmetic of the forced factor

For h169 write

```text
p=169+840t.
```

Then

```text
T=8+35t.
```

Modulo11,

```text
T=5
iff
t=4.
```

Also

```text
F=2T+1.
```

Thus

```text
T=5 mod11
=>
F=11 mod11
=>
11|F.
```

The factor is universal on the phase.

---

## 4. Why J35 survives the forced factor

The k35 character subgroup is

```text
H35={r in U(35):(r/5)(r/7)=+1}.
```

The literal prime11 satisfies

```text
11 in H35.
```

Equivalently,

```text
(11/5)(11/7)=+1.
```

So the phase does not eliminate the J35 branch. It only eliminates S7.

This asymmetry is important:

```text
forced factor11
  negative for S7
  neutral/compatible for J35.
```

The result is a genuine branch collapse rather than an automatic k35 construction.

---

## 5. Exact examples

The verifier preserves both sides of the phase-conditioned theorem.

### J35 survivor

```text
p=3,529
T=148=5 mod11
F=297=3^3*11
J35=true
S7=false
k35 miss.
```

Another survivor is

```text
p=31,249
F=2,607=3*11*79
J35=true
S7=false
k35 miss.
```

### Construction because J35 fails

```text
p=179,089
T=7,463=5 mod11
F=14,927=11*23*59
J35=false
S7=false
k35 constructs.
```

So the exact phase theorem is genuinely

```text
miss iff J35,
```

not merely a one-way exclusion of S7.

---

## 6. Relation to the forced-factor calendar

The k11-conditioned post-k23 calendar already says

```text
T=5 mod11
->
11 | C35.
```

The present theorem turns that calendar entry from a passive factor injection into an exact branch decision:

```text
factor calendar:
    T11=5 -> 11 enters k35

k35 survivor grammar:
    11=4 mod7 -> S7 impossible

combined:
    T11=5 -> only J35 can survive.
```

This is the first direct use of the new calendar to delete a later survivor branch.

---

## 7. Machine consequence

For h169 dependency propagation, the phase-conditioned k35 rule is now

```text
if k11_miss and T_mod11==5:
    k35_S7 = false
    if k35_miss:
        k35_branch = J35
```

No factorization search for S7 is needed on this child state.

A future proof-state machine should preserve the reason:

```text
forced literal factor11 in F
with 11=4 mod7.
```

That is proof data, unlike a finite empirical absence of S7.

---

## 8. Next phases

The other h169 pure-k11 phases inject factor11 at

```text
T11=3 -> k39
T11=1 -> k43
T11=8 -> k51
T11=2 -> k63.
```

The same method should now be applied to the exact survivor grammars at those later shifts:

```text
forced factor
  + exact local branch grammar
    -> branch deletion, quotient reduction, or automatic target hit.
```

The phase5/k35 result proves that this calendar-to-grammar composition can yield exact structural reductions.

---

## 9. Executable verifier

Run

```sh
python3 research/verify_h169_k11_phase5_k35_branch_collapse.py
```

It checks:

```text
h169 phase arithmetic,
T11=5 <=> t11=4,
11|F,
11=4 mod7,
11 in H35,
S7 impossibility,
exact k11 miss state,
exact k35 signed-box state,
and regression primes on both sides of J35.
```

---

## 10. Claim boundary

The theorem does not say k11 miss forces `T=5 mod11`; it resolves only that exact phase child.

It does not eliminate the J35 branch, does not prove construction by k35, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
