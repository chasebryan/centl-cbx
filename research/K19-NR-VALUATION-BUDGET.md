# k=19 quadratic-nonresidue valuation budget

**Status:** exact finite-state valuation theorem  
**Date:** 2026-08-17  
**Shift:** `k=19`  
**Application:** BREC / Lane-I exact obstruction grammar

## 1. A real factor-count bound

The earlier k19 cyclic-state theorem proved that every exact signed-box state has a short canonical representative.

That was deliberately **not** a bound on the actual factorization of

```text
C19=(p+19)/4.
```

The result here is different.

Let

```text
Omega_NR(C19)
```

be the total valuation, counted with multiplicity, of prime factors of `C19` that are quadratic nonresidues modulo 19.

Then:

```text
k19 Type-II miss
=>
Omega_NR(C19) <= 8.
```

Because a BREC combined miss is in particular a Type-II miss, the same bound holds for every k19 BREC obstruction.

This is an actual bound on part of the integer factorization, not merely on a compressed state representation.

---

## 2. Why NR valuation is transition weight

Use primitive root `2` modulo19. Every unit residue is

```text
2^a mod19,
a in Z/18Z.
```

A prime-factor occurrence contributes one signed-box atom

```text
{-a,0,+a}.
```

For primitive root exponent `a`:

```text
a even  <=> residue is QR mod19
a odd   <=> residue is NR mod19.
```

If a prime occurs to valuation `e`, it contributes `e` identical atom transitions. Therefore the number of odd-exponent transitions along the exact factor path is precisely

```text
Omega_NR(C19).
```

This turns the exact Type-II-miss automaton into a weighted graph:

```text
QR transition weight = 0
NR transition weight = 1.
```

---

## 3. Why the weighted path cannot grow forever

Restrict the exact q19 signed-box transition graph to states whose support still omits exponent

```text
9,
```

the Type-II target `-1`.

The unseeded graph has exactly

```text
254 Type-II-miss states.
```

Compute its strongly connected components.

The decisive exact fact is:

```text
no strongly connected component contains an NR transition.
```

Every edge that stays inside an SCC has weight zero.

Therefore every NR transition moves strictly forward in the SCC condensation graph. The condensation is a finite DAG, so the total number of NR transitions on any Type-II-miss factor path is bounded by its longest weighted path.

That longest path has weight

```text
8.
```

Hence

```text
Omega_NR(C19) <= 8.
```

This is the proof object implemented by the verifier. It is stronger than the previous canonical-depth statement because it follows the actual multiplicity-expanded factor path.

---

## 4. The global bound is arithmetically sharp

The bound eight is not only an abstract automaton maximum.

Take

```text
p = 108,013.
```

Then

```text
C19 = (108013+19)/4
    = 27,008
    = 2^7 * 211.
```

Modulo19,

```text
2 = 2 mod19,
211 = 2 mod19.
```

Both are quadratic nonresidues, so

```text
Omega_NR(C19)=7+1=8.
```

The exact signed support misses Type II but hits Type I:

```text
k19 hit class = Type-I-only.
```

Therefore

```text
8
```

is the best possible universal Type-II-miss NR valuation bound at k19.

---

## 5. Hard-class seeds improve the budget

The exact hard-class seed theorem gives the following forced QR factors in `C19`:

```text
hard 1       : [5]
hard 121     : [5,7]
hard 169     : []
hard 289     : [7]
hard 361     : [5]
hard 529     : [].
```

Run the same weighted SCC computation from each seeded exact state.

The result is the hard-class budget atlas:

```text
p mod840    forced seed    Type-II-miss max Omega_NR
----------------------------------------------------
1           [5]                         6
121         [5,7]                       0
169         []                          8
289         [7]                         2
361         [5]                         6
529         []                          8.
```

So a hard-class-conditioned exact search may carry dramatically smaller nonresidue defect budgets than the generic q19 theorem.

---

## 6. h121: zero NR valuation

For

```text
p=121 mod840,
```

the forced factors `5` and `7` already fill the complete QR subgroup modulo19.

Any NR prime factor would immediately add the opposite coset and hit Type II.

Thus

```text
k19 Type-II miss
=>
Omega_NR(C19)=0.
```

This is the valuation form of the existing h121 theorem

```text
k19 miss iff every prime divisor of C19 is QR mod19.
```

Example:

```text
p=6,841
C19=1,715=5*7^3
Omega_NR=0
k19 combined miss.
```

---

## 7. h289: at most two NR valuations

For

```text
p=289 mod840,
```

factor7 is forced and supplies the order-three exponent subgroup

```text
K={0,6,12}.
```

The weighted automaton gives

```text
Omega_NR(C19) <= 2
```

for every Type-II miss.

This agrees exactly with the independently derived concrete h289 residue normal form, whose thin branch satisfies

```text
alpha+beta <= 2.
```

The abstract weighted graph and the human-readable residue grammar therefore reach the same valuation ceiling by different routes.

An arithmetic sharpness witness is

```text
p=93,529
C19=23,387=7*13*257
Omega_NR=2
k19 combined miss.
```

---

## 8. h1 / h361: at most six NR valuations

Hard classes

```text
1 and 361 mod840
```

force factor5 into `C19`.

Starting the exact Type-II-miss automaton from that seed reduces the global NR budget from eight to

```text
Omega_NR(C19) <= 6.
```

The seed-[5] bound is arithmetically sharp already in h1:

```text
p = 11,896,466,401
C19 = 2,974,116,605
    = 5 * 29^6.
```

Modulo19,

```text
5 is QR,
29 = 10 mod19 is NR.
```

Therefore

```text
Omega_NR(C19)=6,
```

and the exact k19 state is Type-I-only.

No claim is made here that h361 itself attains six. The theorem-safe bound for both lanes is six because they begin from the same exact forced q19 seed.

---

## 9. k11 ancestry can dynamically lower the later budget

The k11-to-k19 phase theorem proved that in hard classes

```text
169,289,529,
```

a k11 miss forces

```text
T mod11 in {1,2,3,5,8}.
```

On the phase

```text
T=2 mod11,
```

literal factor11 enters `C19`.

Factor11 has order three modulo19 and supplies the same subgroup K as factor7. Therefore:

```text
h169 + T=2 mod11:
    generic hard-lane budget 8 -> phase budget 2

h529 + T=2 mod11:
    generic hard-lane budget 8 -> phase budget 2

h289 + T=2 mod11:
    existing budget remains 2.
```

The reduction to two is arithmetically attained on the previously unseeded lanes.

For example:

```text
p=1,023,289   hard169
T=2 mod11
C19=255,827=11*13*1789
Omega_NR=2
k19 Type-I-only.
```

And:

```text
p=670,849   hard529
T=2 mod11
C19=167,717=11*79*193
Omega_NR=2
k19 Type-I-only.
```

This is a concrete example of ancestry changing a later **factorization budget**, not merely relabeling a finite state.

---

## 10. Why this matters for the decomposition framework

The k19 obstruction can now be represented by two layers:

```text
finite support state
+
actual NR valuation budget.
```

The budget is monotone and integer-valued. Every new NR prime-factor occurrence consumes one unit, and the exact state graph proves that no Type-II-miss path can replenish that resource through a cycle.

This is close to the kind of quantity needed in a well-founded decomposition machine:

```text
state transition
    -> consume bounded defect resource
        -> either hit a target
        -> or enter a smaller conditioned state space.
```

It is not yet a global termination measure because QR factors can still accumulate through zero-weight cycles. But it is a genuine finite arithmetic resource that was not present in the earlier canonical-state formulation.

---

## 11. Executable verifier

Run

```sh
python3 research/verify_k19_nr_valuation_budget.py
```

For each seed it:

1. exhausts the exact Type-II-miss signed-box state graph;
2. weights every NR atom transition by one;
3. computes all SCCs;
4. verifies there is no positive-weight edge inside any SCC;
5. contracts to a DAG;
6. computes the exact longest weighted path;
7. cross-checks the state count against the independent residue automaton;
8. verifies arithmetic sharpness/regression primes with exact factorization and signed-box evaluation.

The expected exact budgets are

```text
seed []      : 8
seed [5]     : 6
seed [7]     : 2
seed [5,7]   : 0
seed [11]    : 2
seed [7,11]  : 2.
```

---

## 12. Claim boundary

This theorem bounds only the total valuation of quadratic-nonresidue prime factors of `C19` under an exact Type-II miss.

It does not bound the total number of QR factors, does not bound `Omega(C19)` itself, does not prove that every hard-lane upper bound is attained, does not establish a finite Lane-I ceiling, and does not prove Erdős–Straus.
