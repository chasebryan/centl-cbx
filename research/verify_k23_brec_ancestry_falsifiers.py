#!/usr/bin/env python3
"""Verify explicit falsifiers to finite k=23 BREC target-coincidence extrapolations.

The initial p<=2,000,000 BREC census observed that Type-I and Type-II occupancy
at fixed k=23 became identical after one all-negative ancestor and remained so
through the ----- parent.  Those observations are exact finite facts, but they
do not extend universally.

This script freezes exact larger prime witnesses showing:

  * a k=3 combined miss does not force k=23 target coincidence;
  * -- and --- ancestry do not force coincidence;
  * ---- and ----- ancestry do not force coincidence;
  * both same-class q=23 valuation-two rescue patterns, 5^2 and 14^2, can
    survive the full ----- ancestry.

Every stage is independently reconstructed from exact factorization and the
signed-box support.  No saved BREC history string is trusted as evidence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

KERNEL = Path(__file__).resolve().parents[1] / "kernel"
sys.path.insert(0, str(KERNEL))

import analyze_brec_cylinder as cylinder  # noqa: E402

HARD_RESIDUES = {1, 121, 169, 289, 361, 529}
EARLY_K = (3, 7, 11, 15, 19)


def classify_stage(p: int, k: int) -> dict[str, Any]:
    if k < 3 or k % 4 != 3:
        raise ValueError("Lane-I shift must be >=3 and congruent to 3 mod 4")
    if (p + k) % 4:
        raise ValueError(f"p={p}, k={k}: p+k is not divisible by 4")
    if cylinder.math.gcd(p, k) != 1:
        return {"p": p, "k": k, "sign": "?", "defined": False}

    C = (p + k) // 4
    factors = cylinder.factorint(C)
    support, formal_size = cylinder.signed_box_support(factors, k)
    type_ii = (k - 1) % k
    type_i = (-pow(p % k, -1, k)) % k
    hit_ii = type_ii in support
    hit_i = type_i in support

    if hit_i and hit_ii:
        hit_class = "both"
    elif hit_i:
        hit_class = "type-I-only"
    elif hit_ii:
        hit_class = "type-II-only"
    else:
        hit_class = "miss"

    return {
        "p": p,
        "k": k,
        "defined": True,
        "sign": "+" if (hit_i or hit_ii) else "-",
        "C": C,
        "factorization": cylinder.factor_text(factors),
        "factor_residues": {str(q): q % k for q in sorted(factors)},
        "box_formal_size": formal_size,
        "box_support_size": len(support),
        "missing_unit_residues": sorted(cylinder.unit_group(k) - support),
        "type_II_target": type_ii,
        "type_I_target": type_i,
        "hit_type_II": hit_ii,
        "hit_type_I": hit_i,
        "hit_class": hit_class,
    }


def q23_nonresidue_pattern(stage: dict[str, Any]) -> str:
    if stage["k"] != 23 or not stage["defined"]:
        raise ValueError("q23 pattern requires a defined k=23 stage")
    factors = cylinder.factorint(int(stage["C"]))
    nr: dict[int, int] = {}
    for q, exponent in factors.items():
        residue = q % 23
        symbol = pow(residue, 11, 23)
        if symbol == 22:
            nr[residue] = nr.get(residue, 0) + exponent
        elif symbol != 1:
            raise RuntimeError(f"unexpected Euler symbol {symbol} for q={q}")
    if not nr:
        return "QR"
    return "*".join(f"{r}^{nr[r]}" for r in sorted(nr))


def verify_witness(
    p: int,
    expected_history: str,
    minimum_negative_prefix: int,
    expected_pattern: str,
) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"witness {p} is not prime")
    if p % 840 not in HARD_RESIDUES:
        raise SystemExit(f"witness {p} is not Mordell-hard mod 840")

    early = [classify_stage(p, k) for k in EARLY_K]
    history = "".join(stage["sign"] for stage in early)
    if history != expected_history:
        raise SystemExit(
            f"p={p}: early history {history} != expected {expected_history}"
        )
    if not history.startswith("-" * minimum_negative_prefix):
        raise SystemExit(
            f"p={p}: history {history} lacks required depth-{minimum_negative_prefix} "
            "negative ancestry"
        )

    target = classify_stage(p, 23)
    if target["hit_class"] != "type-I-only":
        raise SystemExit(
            f"p={p}: k23 class {target['hit_class']} != type-I-only"
        )
    pattern = q23_nonresidue_pattern(target)
    if pattern != expected_pattern:
        raise SystemExit(
            f"p={p}: q23 pattern {pattern} != expected {expected_pattern}"
        )

    return {
        "p": p,
        "p_mod_840": p % 840,
        "early_history": history,
        "minimum_negative_prefix": minimum_negative_prefix,
        "early_stages": early,
        "k23": target,
        "q23_nonresidue_pattern": pattern,
    }


def verify() -> dict[str, Any]:
    witnesses = [
        verify_witness(5_151_841, "-++-+", 1, "5^2"),
        verify_witness(8_243_281, "---++", 3, "14^2"),
        verify_witness(18_766_609, "-----", 5, "14^2"),
        verify_witness(27_211_969, "-----", 5, "5^2"),
    ]

    # The depth-3 witness also falsifies depth 2; the depth-5 witnesses also
    # falsify depth 4.  Freeze that logical coverage explicitly.
    falsified_depths: dict[str, int] = {
        "1": 5_151_841,
        "2": 8_243_281,
        "3": 8_243_281,
        "4": 18_766_609,
        "5": 18_766_609,
    }

    return {
        "verified": True,
        "mode": "k23-brec-ancestry-falsifiers",
        "target_k": 23,
        "falsified_candidate": (
            "all-negative BREC ancestry of depths 1..5 forces Type-I/Type-II "
            "target coincidence at k=23"
        ),
        "falsified_depths": falsified_depths,
        "deep_rescue_patterns_realized": ["5^2", "14^2"],
        "witnesses": witnesses,
        "surviving_exact_result": (
            "Within the known q=23 Type-II miss normal form, Type-I-only rescue "
            "is confined to the same-class valuation-two patterns 5^2 and 14^2."
        ),
        "claim_boundary": (
            "These explicit witnesses disprove the stated ancestry-coincidence "
            "extrapolations. They do not settle Erdős-Straus or classify all deeper "
            "ancestry constraints."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
