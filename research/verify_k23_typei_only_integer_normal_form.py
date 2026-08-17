#!/usr/bin/env python3
"""Verify the exact conditional integer normal form for k=23 Type-I-only rescue.

This verifier is intentionally narrow.  It checks the algebraic lift from the
already-exhausted q=23 residue states 5^2 and 14^2 to the integer form

    C_23 = 6*m*R,
    p    = 24*m*R - 23,

where every prime divisor of m is 1 mod 23 and R has exactly two prime
valuations, counted with multiplicity, all in one residue class rho in {5,14}.

It also freezes:

  * the six Mordell-hard p mod 840 -> T=(p+23)/24 mod 35 classes;
  * the predecessor identities C_k=C_23-(23-k)/4 for k=3,7,11,15,19;
  * four explicit Type-I-only witnesses, including both full ----- survivors;
  * the exact k=3 and k=7 miss filters on the translated predecessor forms.

The q=23 normal form remains conditional on the previously proved Type-II miss
classification.  Nothing here establishes a bounded ES corridor or a pruning
rule.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "kernel"
sys.path.insert(0, str(KERNEL))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze_brec_cylinder as cylinder  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402
import verify_k23_typei_companion_patterns as companion  # noqa: E402

HARD_TO_T35 = {
    1: 1,
    121: 6,
    169: 8,
    289: 13,
    361: 16,
    529: 23,
}

SPECTRUM_T35 = {
    "A": {1, 6},
    "B": {8, 13},
    "C": {16, 23},
}

EARLY_K = (3, 7, 11, 15, 19)
QR7 = {1, 2, 4}

WITNESSES = {
    5_151_841: {"rho": 5, "history": "-++-+", "split": "distinct-semiprime"},
    8_243_281: {"rho": 14, "history": "---++", "split": "distinct-semiprime"},
    18_766_609: {"rho": 14, "history": "-----", "split": "distinct-semiprime"},
    27_211_969: {"rho": 5, "history": "-----", "split": "distinct-semiprime"},
}


def prime_power(q: int, e: int) -> int:
    return q**e


def spectrum_from_hard_residue(residue: int) -> str:
    if residue in {1, 121}:
        return "A"
    if residue in {169, 289}:
        return "B"
    if residue in {361, 529}:
        return "C"
    raise ValueError(f"not a Mordell-hard residue: {residue}")


def normal_form_record(p: int) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: explicit witness is not prime")

    hard_residue = p % 840
    if hard_residue not in HARD_TO_T35:
        raise SystemExit(f"p={p}: explicit witness is not Mordell-hard")

    stage23 = ancestry.classify_stage(p, 23)
    if stage23["hit_class"] != "type-I-only":
        raise SystemExit(
            f"p={p}: expected k23 Type-I-only, got {stage23['hit_class']}"
        )

    C = int(stage23["C"])
    factors = cylinder.factorint(C)
    if factors.get(2, 0) != 1 or factors.get(3, 0) != 1:
        raise SystemExit(f"p={p}: expected v2(C)=v3(C)=1")

    m = 1
    R = 1
    nr_factors: dict[int, int] = {}
    rho: int | None = None

    for q, exponent in sorted(factors.items()):
        if q in (2, 3):
            continue
        residue = q % 23
        if residue == 1:
            m *= prime_power(q, exponent)
            continue
        if residue not in {5, 14}:
            raise SystemExit(
                f"p={p}: factor {q}^{exponent} has forbidden residue {residue} mod 23"
            )
        if rho is None:
            rho = residue
        elif rho != residue:
            raise SystemExit(f"p={p}: mixed q23 nonresidue classes in rescue branch")
        nr_factors[q] = exponent
        R *= prime_power(q, exponent)

    if rho not in {5, 14}:
        raise SystemExit(f"p={p}: missing same-class q23 nonresidue defect")
    omega_R = sum(nr_factors.values())
    if omega_R != 2:
        raise SystemExit(f"p={p}: Omega(R)={omega_R}, expected 2")

    if C != 6 * m * R:
        raise SystemExit(f"p={p}: C != 6*m*R")
    if p != 24 * m * R - 23:
        raise SystemExit(f"p={p}: p != 24*m*R-23")

    if len(nr_factors) == 1 and next(iter(nr_factors.values())) == 2:
        split = "square"
    elif len(nr_factors) == 2 and set(nr_factors.values()) == {1}:
        split = "distinct-semiprime"
    else:
        raise SystemExit(f"p={p}: invalid Omega-two multiplicity split {nr_factors}")

    # T=mR=(p+23)/24 exists integrally for every hard p because p == 1 mod 24.
    T = m * R
    if T != (p + 23) // 24:
        raise SystemExit(f"p={p}: T identity failed")
    expected_t35 = HARD_TO_T35[hard_residue]
    if T % 35 != expected_t35:
        raise SystemExit(
            f"p={p}: T mod35={T % 35}, expected {expected_t35} from hard class"
        )

    spectrum = spectrum_from_hard_residue(hard_residue)
    if T % 35 not in SPECTRUM_T35[spectrum]:
        raise SystemExit(f"p={p}: spectrum/T35 mismatch")

    early = [ancestry.classify_stage(p, k) for k in EARLY_K]
    history = "".join(str(stage["sign"]) for stage in early)

    predecessors: list[dict[str, Any]] = []
    for stage in early:
        k = int(stage["k"])
        Ck = (p + k) // 4
        offset = (23 - k) // 4
        if Ck != C - offset:
            raise SystemExit(f"p={p}, k={k}: predecessor identity failed")
        predecessors.append({"k": k, "C": Ck, "offset_from_C23": offset})

    # Exact k=3 obstruction filter on C3=6T-5.
    C3 = C - 5
    f3 = cylinder.factorint(C3)
    k3_filter_miss = all(q % 3 == 1 for q in f3)
    if (early[0]["sign"] == "-") != k3_filter_miss:
        raise SystemExit(f"p={p}: k3 normal-form filter disagrees with signed box")

    # Exact k=7 obstruction filter on C7=2*(3T-2).
    C7 = C - 4
    if C7 != 2 * (3 * T - 2):
        raise SystemExit(f"p={p}: translated k7 affine identity failed")
    f7 = cylinder.factorint(C7)
    k7_filter_miss = all(q % 7 in QR7 for q in f7)
    if (early[1]["sign"] == "-") != k7_filter_miss:
        raise SystemExit(f"p={p}: k7 normal-form filter disagrees with signed box")

    return {
        "p": p,
        "p_mod_840": hard_residue,
        "spectrum": spectrum,
        "C23": C,
        "T": T,
        "T_mod_35": T % 35,
        "m": m,
        "R": R,
        "rho": rho,
        "Omega_R": omega_R,
        "R_factorization": cylinder.factor_text(nr_factors),
        "split": split,
        "early_history": history,
        "predecessors": predecessors,
        "k3_filter_miss": k3_filter_miss,
        "k7_filter_miss": k7_filter_miss,
        "k23": stage23,
    }


def verify_local_branches() -> list[dict[str, Any]]:
    expected = {
        5: {"state": (2, 0), "C_mod_23": 12, "p_mod_23": 2, "target": 11},
        14: {"state": (0, 2), "C_mod_23": 3, "p_mod_23": 12, "target": 21},
    }
    out: list[dict[str, Any]] = []
    for rho, exp in expected.items():
        a5, a14 = exp["state"]
        state = companion.classify(a5, a14)
        if state["hit_class"] != "type-I-only" or state["hit_type_II"]:
            raise SystemExit(f"rho={rho}: not the expected Type-I-only q23 state")
        if state["C_mod_23"] != exp["C_mod_23"]:
            raise SystemExit(f"rho={rho}: C residue mismatch")
        if state["p_mod_23"] != exp["p_mod_23"]:
            raise SystemExit(f"rho={rho}: p residue mismatch")
        if state["type_I_target"] != exp["target"]:
            raise SystemExit(f"rho={rho}: Type-I target mismatch")
        out.append(
            {
                "rho": rho,
                "C_mod_23": state["C_mod_23"],
                "p_mod_23": state["p_mod_23"],
                "type_I_target": state["type_I_target"],
                "type_II_target": state["type_II_target"],
                "support_size": state["support_size"],
            }
        )
    return out


def verify_hard_map() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for p_residue, expected_t35 in HARD_TO_T35.items():
        numerator = p_residue + 23
        if numerator % 24:
            raise SystemExit(f"hard residue {p_residue}: p+23 not divisible by 24")
        got = (numerator // 24) % 35
        if got != expected_t35:
            raise SystemExit(
                f"hard residue {p_residue}: T mod35={got}, expected {expected_t35}"
            )
        rows.append({"p_mod_840": p_residue, "T_mod_35": got})
    return rows


def verify() -> dict[str, Any]:
    local_branches = verify_local_branches()
    hard_map = verify_hard_map()

    witness_rows = [normal_form_record(p) for p in WITNESSES]
    by_p = {row["p"]: row for row in witness_rows}

    for p, expected in WITNESSES.items():
        row = by_p[p]
        if row["rho"] != expected["rho"]:
            raise SystemExit(f"p={p}: rho={row['rho']} != {expected['rho']}")
        if row["early_history"] != expected["history"]:
            raise SystemExit(
                f"p={p}: history {row['early_history']} != {expected['history']}"
            )
        if row["split"] != expected["split"]:
            raise SystemExit(f"p={p}: multiplicity split mismatch")

    deep = [p for p, row in by_p.items() if row["early_history"] == "-----"]
    if sorted(deep) != [18_766_609, 27_211_969]:
        raise SystemExit(f"unexpected full ----- witness set: {sorted(deep)}")
    if {by_p[p]["rho"] for p in deep} != {5, 14}:
        raise SystemExit("full ----- witnesses do not realize both q23 rescue branches")

    return {
        "verified": True,
        "mode": "k23-typei-only-integer-normal-form",
        "conditional_on": "exact q=23 Type-II miss normal form",
        "normal_form": "C23=6*m*R; p=24*m*R-23; q|m=>q=1 mod23; Omega(R)=2 in one rho in {5,14}",
        "local_branches": local_branches,
        "hard_class_map": hard_map,
        "predecessor_block": ["6T-5", "6T-4", "6T-3", "6T-2", "6T-1", "6T"],
        "witnesses": witness_rows,
        "full_five_miss_branches_realized": [5, 14],
        "claim_boundary": (
            "Exact conditional normal-form and explicit-witness verification only; "
            "no universal corridor ceiling, pruning theorem, or Erdős-Straus proof."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
