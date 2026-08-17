# CENTL-CBX research index

This directory contains exact theorem modules, executable verifiers, finite research grammars, and preserved falsifiers for the focused Erdős–Straus program.

## BREC / Lane-I recursive corridor

The current Bryan Recursive Entanglement Calculus work is organized as a proof-and-falsifier chain rather than a single narrative file.

### Application geometry

- [`BREC-LANE-I-RECURSIVE-CORRIDOR.md`](BREC-LANE-I-RECURSIVE-CORRIDOR.md) — anchored Lane-I BREC corridor, sliding motifs versus absolute prefix cylinders, and the falsification discipline for finite contractions.

### Exact first-coordinate theorem

- [`K3-BREC-OBSTRUCTION-NORMAL-FORM.md`](K3-BREC-OBSTRUCTION-NORMAL-FORM.md) — proves that for a Mordell-hard prime, the combined `k=3` miss is equivalent to every prime divisor of `(p+3)/4` being `1 mod 3`.
- [`verify_k3_brec_obstruction_normal_form.py`](verify_k3_brec_obstruction_normal_form.py) — executable residue-group verification.

### Exact q=23 Type-I companion reduction

- [`K23-TYPEI-COMPANION-NORMAL-FORM.md`](K23-TYPEI-COMPANION-NORMAL-FORM.md) — conditional on the existing exact q23 Type-II miss normal form, classifies Type-I-only rescue as exactly the same-class valuation-two defects `5^2` and `14^2`, with integer branch `p=24HD-23`.
- [`verify_k23_typei_companion_patterns.py`](verify_k23_typei_companion_patterns.py) — exhaustive six-state unit-group calculation and hard `HD mod 35` reduction.

### Preserved finite phase and its falsification

- [`K23-BREC-TWO-TARGET-COINCIDENCE.md`](K23-BREC-TWO-TARGET-COINCIDENCE.md) — records the exact two-million-prime target-coincidence phase, its later falsification, and the surviving exact companion result.
- [`verify_k23_brec_ancestry_falsifiers.py`](verify_k23_brec_ancestry_falsifiers.py) — exact larger witnesses showing that all-negative ancestry depths 1 through 5 do not force Type-I/Type-II coincidence at `k=23`.

The methodological order is intentional:

```text
finite observation
  -> exact candidate
    -> adversarial falsifier search
      -> preserved counterexample if false
      -> exact lemma + independent verifier if true
```

No finite BREC motif, cylinder collapse, or target coincidence has pruning authority on its own.

## Broader exact frontier

The remaining files in this directory continue the fixed-shift character, valuation, survivor-grammar, source-renewal, and Type-II geometry program. [`CURRENT-FRONTIER.md`](CURRENT-FRONTIER.md) is the high-level research ledger.

This index tracks the active branch-level organization. It does not replace the detailed claim boundaries inside individual theorem and falsifier documents.
