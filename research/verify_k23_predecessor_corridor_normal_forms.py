#!/usr/bin/env python3
"""Verify the exact five-coordinate predecessor normal form before k=23.

On the q23 Type-I-only rescue branch write

    T = (p+23)/24,
    C23 = 6T,
    p = 24T-23.

Then the five preceding Lane-I integers are

    C3  = 6T-5,
    C7  = 2(3T-2),
    C11 = 3(2T-1),
    C15 = 2(3T-1),
    C19 = 6T-1.

This verifier composes the independently verified exact fixed-shift normal
forms at k=3,7,11,15,19 and checks them against the exact signed-box evaluator
on preserved q23 Type-I-only witnesses.

The synthesis is deliberately not a contradiction theorem.  Two explicit
primes, 18,766,609 and 27,211,969, realize the full five-negative predecessor
word and then construct Type-I-only at k=23.  Any future cross-coordinate
argument must retain those regression witnesses.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "kernel"
RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(KERNEL))
sys.path.insert(0, str(RESEARCH))

import analyze_brec_cylinder as cylinder  # noqa: E402
import verify_k11_brec_obstruction_normal_form as k11  # noqa: E402
import verify_k19_brec_state_compression as k19  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402
import verify_k23_typei_only_integer_normal_form as q23  # noqa: E402

EARLY_K = (3, 7, 11, 15, 19)
H15 = {1, 2, 4, 8}
QR7 = {1, 2, 4}


def k3_miss(T: int) -> bool:
    factors = cylinder.factorint(6 * T - 5)
    return all(q % 3 == 1 for q in factors)


def k7_miss(T: int) -> bool:
    # C7=2(3T-2), and the forced factor 2 is QR modulo 7.
    factors = cylinder.factorint(3 * T - 2)
    return all(q % 7 in QR7 for q in factors)


def k11_miss(T: int) -> tuple[bool, dict[str, Any]]:
    C11 = 3 * (2 * T - 1)
    state = k11.classify_factorization(C11)
    return bool(state["combined_miss"]), state


def k15_miss(T: int) -> bool:
    # C15=2(3T-1), with 2 already in H=<2> modulo 15.
    factors = cylinder.factorint(3 * T - 1)
    return all(q % 15 in H15 for q in factors)


def k19_miss(T: int) -> tuple[bool, dict[str, Any]]:
    C19 = 6 * T - 1
    state = k19.state_from_factorization(C19)
    public = {key: value for key, value in state.items() if key != "state"}
    return bool(state["combined_miss"]), public


def corridor_record(p: int) -> dict[str, Any]:
    normal = q23.normal_form_record(p)
    T = int(normal["T"])

    stages = [ancestry.classify_stage(p, k) for k in EARLY_K]
    history = "".join(str(stage["sign"]) for stage in stages)
    if history != normal["early_history"]:
        raise SystemExit(f"p={p}: q23 normal-form history disagrees with exact stages")

    pred3 = k3_miss(T)
    pred7 = k7_miss(T)
    pred11, state11 = k11_miss(T)
    pred15 = k15_miss(T)
    pred19, state19 = k19_miss(T)
    predictions = [pred3, pred7, pred11, pred15, pred19]

    for stage, predicted in zip(stages, predictions, strict=True):
        exact_miss = stage["sign"] == "-"
        if exact_miss != predicted:
            raise SystemExit(
                f"p={p}, k={stage['k']}: predecessor normal form "
                f"predicted miss={predicted}, exact miss={exact_miss}"
            )

    predecessor_values = {
        "k3": 6 * T - 5,
        "k7_reduced": 3 * T - 2,
        "k11_reduced": 2 * T - 1,
        "k15_reduced": 3 * T - 1,
        "k19": 6 * T - 1,
        "k23": 6 * T,
    }
    if stages[0]["C"] != predecessor_values["k3"]:
        raise SystemExit(f"p={p}: C3 affine identity failed")
    if stages[1]["C"] != 2 * predecessor_values["k7_reduced"]:
        raise SystemExit(f"p={p}: C7 affine identity failed")
    if stages[2]["C"] != 3 * predecessor_values["k11_reduced"]:
        raise SystemExit(f"p={p}: C11 affine identity failed")
    if stages[3]["C"] != 2 * predecessor_values["k15_reduced"]:
        raise SystemExit(f"p={p}: C15 affine identity failed")
    if stages[4]["C"] != predecessor_values["k19"]:
        raise SystemExit(f"p={p}: C19 affine identity failed")
    if normal["C23"] != predecessor_values["k23"]:
        raise SystemExit(f"p={p}: C23 affine identity failed")

    return {
        "p": p,
        "p_mod_840": normal["p_mod_840"],
        "spectrum": normal["spectrum"],
        "T": T,
        "T_mod_35": normal["T_mod_35"],
        "q23_rho": normal["rho"],
        "q23_split": normal["split"],
        "early_history": history,
        "predecessor_values": predecessor_values,
        "normal_form_misses": {
            "k3": pred3,
            "k7": pred7,
            "k11": pred11,
            "k15": pred15,
            "k19": pred19,
        },
        "k11_state": state11,
        "k19_state": state19,
        "k23_hit_class": normal["k23"]["hit_class"],
    }


def verify() -> dict[str, Any]:
    # These four q23 Type-I-only witnesses exercise both rescue classes and
    # both constructive/obstructive predecessor patterns already frozen in CI.
    expected = {
        5_151_841: "-++-+",
        8_243_281: "---++",
        18_766_609: "-----",
        27_211_969: "-----",
    }
    rows = [corridor_record(p) for p in expected]
    by_p = {row["p"]: row for row in rows}

    for p, history in expected.items():
        if by_p[p]["early_history"] != history:
            raise SystemExit(f"p={p}: {by_p[p]['early_history']} != {history}")
        if by_p[p]["k23_hit_class"] != "type-I-only":
            raise SystemExit(f"p={p}: target stage is not Type-I-only")

    deep = [row for row in rows if row["early_history"] == "-----"]
    if {row["p"] for row in deep} != {18_766_609, 27_211_969}:
        raise SystemExit("full five-negative regression set changed")
    if {row["q23_rho"] for row in deep} != {5, 14}:
        raise SystemExit("full five-negative regressions no longer realize both q23 classes")
    for row in deep:
        if not all(row["normal_form_misses"].values()):
            raise SystemExit(f"p={row['p']}: a predecessor theorem rejected a known survivor")

    return {
        "verified": True,
        "mode": "k23-predecessor-corridor-normal-forms",
        "parameter": "T=(p+23)/24",
        "q23_target": (
            "C23=6T with Type-I-only rescue normal form: 23-split multiplier and "
            "same-class Omega-two defect rho in {5,14}"
        ),
        "coordinates": {
            "k3": {
                "integer": "6T-5",
                "miss": "every prime divisor is 1 mod 3",
            },
            "k7": {
                "integer": "C7=2(3T-2)",
                "miss": "every prime divisor of 3T-2 is in {1,2,4} mod 7",
            },
            "k11": {
                "integer": "C11=3(2T-1)",
                "miss": (
                    "pure QR splitting mod 11, or thin primitive packet over "
                    "classes 2,6 in {(1,0),(0,1),(1,1)}"
                ),
            },
            "k15": {
                "integer": "C15=2(3T-1)",
                "miss": "every prime divisor of 3T-1 is in {1,2,4,8} mod 15",
            },
            "k19": {
                "integer": "6T-1",
                "miss": (
                    "cyclic state (c,S) in one of 136 exact obstruction states; "
                    "targets are exponents 9 and 7-c mod 18"
                ),
            },
        },
        "full_five_negative_regressions": [18_766_609, 27_211_969],
        "witnesses": rows,
        "claim_boundary": (
            "Exact composition of independently verified fixed-shift normal forms. "
            "The five conditions are simultaneously realizable, so this is not a "
            "contradiction, finite ceiling, pruning theorem, or Erdős-Straus proof."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
