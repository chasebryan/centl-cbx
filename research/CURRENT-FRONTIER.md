# CENTL-CBX Current Research Frontier

## Status

Erdős–Straus remains open.

This repository contains an exact candidate-decomposition framework and an increasingly explicit fixed-shift dependency grammar. None of the finite censuses, BREC motif frequencies, or survivor contractions below constitutes a proof unless an exact theorem and independent verifier are stated.

## BREC recursive corridor update — 2026-08-17

The Bryan Recursive Entanglement Calculus is now implemented as exact downstream Lane-I telemetry and theorem-hunting infrastructure.

The application records, for admissible shifts `k = 3 mod 4`,

```text
+  iff the exact signed box hits {-1,-p^(-1)}
-  iff the exact signed box misses both targets
?  iff the application stage is undefined
```

The production-equivalent verdict order remains

```text
W -> I -> N -> L.
```

BREC creates no proof authority by itself.

### Exact engine work

The active branch includes:

```text
kernel/src/cbx_brec_i.c
kernel/verify_brec_i.py
kernel/analyze_brec.py
kernel/analyze_brec_cylinder.py
kernel/analyze_brec_target.py
```

The optimized BREC evaluator is independently compared against the standalone exact Lane-I reference. It uses:

```text
small-prime stripping before Pollard-rho,
admissible target collapse to {-1,-p^(-1)},
one signed-box traversal for both targets,
prime p>K coprimality shortcut.
```

The canonical two-million-prime development census verified exact agreement on 4519 Mordell-hard primes and 90,380 Lane-I stages through `k<=80`.

### Anchored ancestry versus sliding motifs

BREC now distinguishes:

```text
sliding motif:      a +/- word occurring anywhere in a history,
anchored prefix:    a +/- word beginning at absolute shift k=3.
```

This distinction is required for fixed-shift theorem work. For example,

```text
-----
```

as an anchored prefix means exact combined misses at

```text
k=3,7,11,15,19.
```

### Finite k23 coincidence was falsified

The first `p<=2,000,000` corpus showed no one-sided Type-I/Type-II state at fixed `k=23` after one or more all-negative ancestors. That exact finite pattern has now been adversarially tested and does **not** generalize.

Explicit exact Type-I-only witnesses include:

```text
p =  5,151,841   early history -++-+
p =  8,243,281   early history ---++
p = 18,766,609   early history -----
p = 27,211,969   early history -----
```

Therefore all proposed statements of the form

```text
all-negative BREC ancestry of depth 1..5
forces Type-I/Type-II target coincidence at k=23
```

are false.

The falsifiers are permanent executable regression objects:

```text
research/verify_k23_brec_ancestry_falsifiers.py
research/K23-BREC-TWO-TARGET-COINCIDENCE.md
```

### Exact k3 obstruction theorem

For every Mordell-hard prime,

```text
p = 1 mod 3.
```

At `k=3`, Type I and Type II coincide at target `2 mod 3`. Hence

```text
sigma_3(p) = -
iff
every prime divisor of C_3=(p+3)/4 is 1 mod 3.
```

This is an exact theorem, not a finite observation.

Files:

```text
research/K3-BREC-OBSTRUCTION-NORMAL-FORM.md
research/verify_k3_brec_obstruction_normal_form.py
```

### Exact q23 Type-I companion normal form

Conditional on the already-established q23 Type-II miss normal form, the Type-I companion is now exhausted exactly.

The six possible nonresidue valuation states are

```text
(a5,a14) =
(0,0), (1,0), (0,1), (2,0), (1,1), (0,2).
```

Exact unit-group classification gives Type-I-only rescue **only** for

```text
5^2
14^2.
```

The mixed valuation-two defect `5*14`, both valuation-one defects, and pure quadratic branch all remain Type-I misses.

Equivalently every q23 Type-I-only rescue in this normal form has

```text
C_23 = 6HD,
p = 24HD - 23,
```

where

```text
all prime divisors of H are 1 mod 23,
Omega(D)=2,
all prime divisors of D are 5 mod 23
or all are 14 mod 23.
```

For a Mordell-hard prime,

```text
HD mod 35 in {1,6,8,13,16,23}.
```

Files:

```text
research/K23-TYPEI-COMPANION-NORMAL-FORM.md
research/verify_k23_typei_companion_patterns.py
```

### Current exact bridge problem

Because

```text
C_3 = C_23 - 5,
```

a q23 Type-I-only rescue that survives the first BREC obstruction satisfies

```text
C_23 = 6HD,
p = 24HD - 23,
C_3 = 6HD - 5,
all prime divisors of 6HD-5 are 1 mod 3.
```

Explicit witnesses prove this system is realizable for both q23 rescue classes, so no simple k3-vs-k23 incompatibility remains.

The immediate mathematical task is now:

> transport the exact `k=7,11,15,19` obstruction conditions onto the two explicit q23 rescue branches `p=24HD-23`, determine which conditions create genuine structural reductions, and attack every proposed reduction with targeted branch generation before promoting it to a theorem.

This is the active Type-I companion frontier.

---

## Existing fixed-shift / character frontier

The prior exact program remains in force. In particular, the q23 Type-II filter, later q-adic character/valuation ladders, source-renewal results, k27/k31/k35 survivor grammars, Route-B k47 structure, and later-phase feedback modules remain part of the active exact corpus.

The new BREC layer changes how those constraints can be conditioned and compared; it does not invalidate their exact statements.

## Research discipline

The k23 coincidence episode establishes the repository rule:

```text
finite contraction
    -> candidate only
        -> adversarial extension
            -> preserve falsifier if false
            -> exact theorem + independent verifier if true
                -> only then pruning authority
```

This rule applies equally to BREC motifs, spectrum-conditioned absences, prefix cylinders, valuation patterns, and scheduler heuristics.

## Immediate next work

1. Parameterize the `5^2` and `14^2` q23 Type-I-only branches at the integer level.
2. Translate `k=7` exact misses onto `p=24HD-23` first, before stacking deeper ancestry.
3. Search for the first realizable and first impossible residue/valuation subclasses under that translation.
4. Repeat for `k=11,15,19`, preserving a dependency chain rather than a single opaque finite filter.
5. Maintain independent exact verification against the existing Lane-I engine.
6. Never convert a finite BREC absence into pruning without a separate theorem.

## Claim boundary

No result in this frontier establishes the Erdős–Straus conjecture, a universal finite Lane-I ceiling, or a complete closed decomposition method.

The exact new results are:

```text
k3 BREC obstruction normal form,
q23 Type-I companion six-state classification,
explicit falsification of ancestry-coincidence depths 1..5.
```

The remaining bridge from these local results to a universal proof is open.
