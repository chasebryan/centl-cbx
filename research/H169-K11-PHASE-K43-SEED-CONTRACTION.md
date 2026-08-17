# h169 k11 phase -> k43 seed contraction

**Status:** exact seeded local-automaton theorem  
**Date:** 2026-08-17  
**Scope:** h169 under an inherited k11 combined miss  
**Verifier:** `verify_h169_k11_phase_k43_seed.py`

## 1. The selected k11 child

Write

```text
p = 169 + 840t
T = (p+23)/24 = 8 + 35t.
```

The landed h169 k11 theorem gives the exact necessary phase set

```text
k11 miss
->
t mod11 in {0,2,3,4,8}.
```

Select

```text
t = 2 mod11.
```

Then

```text
T = 1 mod11.
```

At k43,

```text
C43 = (p+43)/4
    = 6T+5
    = 53+210t.
```

Therefore

```text
T=1 mod11
->
11 | C43.
```

This is exactly the k43 child already predicted by the deterministic factor-11 calendar.

---

## 2. The forced factor is structured modulo 43

Use primitive root

```text
g=3 mod43.
```

The literal factor 11 satisfies

```text
11 = 3^30 mod43
ord_43(11)=7.
```

It is also a quadratic residue modulo43.

Thus the inherited k11 phase does not inject a generic factor into the k43 signed box. It injects a fixed order-seven QR seed.

The local question becomes exact:

```text
What Type-II-miss signed-box states remain reachable modulo43
once one occurrence of residue11 is already present?
```

---

## 3. Complete exact local state contraction

The verifier exhausts the entire prime-modulus q43 Type-II-miss automaton.

Without a forced seed:

```text
Type-II-miss states        18,048
combined-miss states        7,740
Type-I-only states         10,308
```

With one forced occurrence of literal factor11:

```text
Type-II-miss states         2,317
combined-miss states        1,217
Type-I-only states          1,100
```

So the exact local miss universe contracts from

```text
18,048 -> 2,317
```

with

```text
15,731 states removed.
```

Equivalently, every k43 Type-II miss on this h169 ancestry child lies inside the exact seed11 closure

```text
2317 / 18048
```

of the unseeded local state space.

This is a finite-state theorem, not a census of primes.

---

## 4. The vertical resource contracts too

Give each signed-box transition weight

```text
0  if the added factor residue is QR mod43
1  if the added factor residue is NR mod43.
```

For the complete Type-II-miss graph, the verifier computes strongly connected components and confirms that no SCC contains a positive-NR edge.

Therefore the maximum accumulated NR valuation is finite and is obtained on the condensation DAG.

The exact bounds are

```text
unseeded q43 Type-II miss:
Omega_NR(C43) <= 20

seed11 q43 Type-II miss:
Omega_NR(C43) <= 14.
```

Thus the k11 ancestry phase cuts the remaining vertical resource by six:

```text
20 -> 14.
```

This is the same architectural phenomenon already exposed at k19: ancestry information can contract both the horizontal finite state and the vertical valuation budget.

---

## 5. Obligation form

The theorem can be carried by BREC as

```text
h169
+ inherited k11 miss
+ t mod11=2

-> T mod11=1
-> 11|C43
-> seed11 q43 signed-box state

and, conditional on k43 Type-II miss,

state(C43) in Q43_seed11
|Q43_seed11| = 2317
Omega_NR(C43) <= 14.
```

The corresponding generic local resources are

```text
|Q43_generic| = 18048
Omega_NR(C43) <= 20.
```

So the obligation ledger can now attach a concrete finite resource certificate to this phase before any arithmetic factor search is scheduled.

---

## 6. Why this is not yet a branch deletion

At k19 the forced factor11 collided with an already-landed survivor support law:

```text
BARE -> every q|R is 1 mod19.
```

That turned the seed into a contradiction and deleted BARE.

At k43 there is not yet a landed survivor-mode theorem of comparable strength. The seed therefore yields an exact **resource contraction**, not yet a route deletion.

That distinction matters.

The next theorem-mining question is not whether 2,317 is a small number. It is:

```text
Which of those 2,317 abstract local states are compatible with the
simultaneous earlier cofactor obligations and realized h169 route ancestry?
```

That is where another contradiction core may appear.

---

## 7. Consecutive-cofactor interpretation

The k43 result should not be isolated as a new independent shift theorem.

It is another obligation placed on the same affine survivor object. Earlier coordinates have already restricted phase, support, route mode, and valuations. The k43 seed adds a new local state ceiling and a new valuation ceiling to that same object.

The research target remains simultaneous satisfiability:

```text
Can the obligations inherited from k3,k7,k11,k15,k19,k23,...
coexist with the seed11 k43 miss closure?
```

The correct next computation is therefore intersection, not range extension.

---

## 8. Next unresolved k11 child

The deterministic factor11 partition now has the following status:

```text
t11=8 -> k19  : mode deletion + NR budget contraction
t11=4 -> k35  : existing branch collapse
t11=3 -> k39  : existing routed support theorem
t11=2 -> k43  : exact seed-state + NR budget contraction
t11=0 -> k51  : unresolved
```

The remaining child k51 is composite-modulus geometry. It should not be forced through the prime-modulus q automaton.

The natural next object is an exact signed-box automaton on

```text
(Z/51Z)^* ~= (Z/3Z)^* x (Z/17Z)^*,
```

or an equivalent CRT representation, with the literal factor11 preloaded.

---

## 9. Executable verification

Run

```sh
python3 research/verify_h169_k11_phase_k43_seed.py
```

The verifier checks:

```text
the inherited h169 k11 phase set,
t=2 mod11 -> T=1 mod11,
t=2 mod11 -> 11|C43,
the deterministic calendar destination k43,
primitive root 3 modulo43,
log_3(11)=30,
ord_43(11)=7,
11 QR modulo43,
complete unseeded q43 Type-II-miss closure,
complete seed11 q43 Type-II-miss closure,
combined-miss and Type-I-only splits,
absence of positive-NR edges inside miss SCCs,
and the exact NR budgets 20 and14.
```

---

## 10. Claim boundary

The theorem does not say a k11 miss forces `t=2 mod11`; four other admissible phase children remain.

It does not say the arithmetic survivor reaches k43, does not say k43 must miss, and does not assert that every abstract seed11 state is realized by a prime corridor candidate.

It gives an exact conditional local consequence:

```text
h169 + inherited k11 miss + t=2 mod11 + k43 Type-II miss
->
seed11 q43 closure of size 2317
and
Omega_NR(C43)<=14.
```

No finite Lane-I ceiling or Erdős-Straus proof is claimed by this theorem alone.
