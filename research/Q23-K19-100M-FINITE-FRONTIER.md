# q23 -> k19 finite frontier through 100M

**Status:** preserved exact finite census  
**Date:** 2026-08-17  
**Grade:** `p <= 100,000,000`, q23 Type-I-only, anchored BREC prefix `----`  
**GitHub Actions run:** `32001085887`  
**Artifact:** `q23-k19-frontier-100000000` (`9278416424`)  
**Artifact SHA-256:** `1ff5ab15b8440b2d55aae633e92c923551fc11858fdc5a38161984294531eaf7`  
**Claim boundary:** finite census only; no universal ceiling or density statement

## 1. Why this run was made

The first 30M q23 -> k19 frontier had collapsed to three exact candidates, all in hard class

```text
p = 169 mod 840.
```

That was useful finite compression, but it created an obvious dangerous extrapolation:

```text
first four predecessor misses + q23 Type-I-only
might force hard class 169.
```

The branch was therefore extended adversarially to 100M before treating the pattern as anything more than finite evidence.

The extrapolation fails.

---

## 2. Exact 100M result

The forward search visited

```text
714,287  T=(p+23)/24 values in the six hard T mod35 classes
59,683   prime p=24T-23 values after the cheap hard-class/small-factor gate
113      exact q23 Type-I-only candidates before the prefix gate
9        exact q23 Type-I-only candidates with anchored prefix ----.
```

The nine candidates split at k19 as

```text
7  combined misses
1  Type-I-only construction
1  Type-II-only construction.
```

So

```text
---- parent count = 9
----- child count = 7
----+ child count = 2.
```

---

## 3. The nine exact candidates

### k19 combined misses

```text
p=18,766,609   p mod840=169   q23 rho=14   state 14:05551   depth2
p=27,211,969   p mod840=169   q23 rho=5    state  8:00501   depth1
p=35,870,641   p mod840=121   q23 rho=5    state  6:15555   depth3
p=48,224,401   p mod840=1     q23 rho=5    state  4:15555   depth2
p=49,554,961   p mod840=1     q23 rho=14   state  2:15555   depth2
p=54,831,841   p mod840=1     q23 rho=5    state  4:15555   depth2
p=85,241,521   p mod840=1     q23 rho=5    state  2:15055   depth2
```

### k19 Type-I-only

```text
p=31,935,121   p mod840=1   q23 rho=14   state 2:3fdff   depth3
```

Its k19 support has size 17. It misses the Type-II exponent `9` but hits the moving Type-I target.

### k19 Type-II-only

```text
p=25,180,849   p mod840=169   q23 rho=14   state 2:10a85   depth2
```

This is the original 30M `----+` candidate.

---

## 4. The hard-class-169 extrapolation is falsified

At 30M all three candidates were class `169 mod840`.

By 100M the exact candidate hard classes are

```text
1,
121,
169.
```

In particular, the first new `----` q23-rescue candidate above the 30M grade is

```text
p = 31,935,121 = 1 mod840,
```

and it constructs at k19 by Type I only.

The first new full `-----` survivor outside class169 is

```text
p = 35,870,641 = 121 mod840.
```

Therefore neither

```text
---- q23 rescue => p=169 mod840
```

nor

```text
----- q23 rescue => p=169 mod840
```

is a valid universal inference.

This falsifier is now part of the research record so the 30M compression is not accidentally promoted into a theorem later.

---

## 5. k19 state compression remains strong

Although the hard-class pattern broke, the exact cyclic-state theorem survived unchanged.

Across the nine finite candidates the k19 canonical depths are

```text
depth1 : 1
depth2 : 6
depth3 : 2.
```

No candidate requires the unique depth-4 full-support state.

The seven combined misses occupy only six distinct exact cyclic states:

```text
14:05551
8:00501
6:15555
4:15555
2:15555
2:15055.
```

The state

```text
4:15555
```

is realized twice.

This is finite arithmetic realization data inside the universal 136-state combined-miss universe, not a theorem excluding the other 130 states from the q23 corridor.

---

## 6. Branch balance changed

The nine candidates contain

```text
q23 rho=5  : 5
q23 rho=14 : 4.
```

Both q23 Type-I-only rescue classes therefore survive the first four exact predecessor misses through 100M, and both also occur among the seven k19 misses.

The 100M run gives no basis for eliminating either branch.

---

## 7. Next use of the census

The important object is no longer the hard class alone. The richer finite signature is

```text
(T mod35, q23 rho, k11 branch, k19 exact cyclic state).
```

The adversarial extension shows why this refinement is necessary: a one-coordinate pattern that looked absolute at 30M dissolved immediately when the search horizon moved.

The next theorem attempt should target compatibility of exact state components, with every finite pattern subjected to the same extension/falsifier discipline before promotion.

---

## 8. Claim boundary

The exact statement here is only:

```text
within p <= 100,000,000,
there are exactly nine q23 Type-I-only candidates with prefix ----
in this forward finite census,
and their k19 split is 7 miss / 2 construction.
```

Nothing in this file proves a universal upper bound, an infinite family statement, a density result, a pruning theorem, or Erdős–Straus.
