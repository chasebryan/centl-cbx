#!/usr/bin/env python3
"""Verify exact hard-class forced seeds in the q23 predecessor corridor.

On the q23 Type-I-only parameterization T=(p+23)/24, Mordell-hard classes give
six exact T residues modulo 35.  Those residues force literal small factors in
some predecessor forms before any factorization search:

    T mod35 = 1   -> 5 | (6T-1)
    T mod35 = 6   -> 5*7 | (6T-1)
    T mod35 = 8   -> 5 | (2T-1)
    T mod35 = 13  -> 5 | (2T-1), 7 | (6T-1)
    T mod35 = 16  -> 7 | (6T-5), 5 | (6T-1)
    T mod35 = 23  -> 7 | (6T-5), 5 | (2T-1).

The q11 predecessor C11=3(2T-1) always has a forced factor 3.  Therefore hard
classes with T=3 mod5 additionally seed residue 5 modulo 11.  The exact q11
Type-II-miss automaton contracts from 11 states (seed [3]) to 5 states (seed
[3,5]); all five are combined misses, so Type-I-only rescue is impossible in
hard classes 169,289,529 once Type II misses.

At k19, hard-class forced factors seed the q19 automaton as follows:

    hard 1,361   : [5]    -> 64 Type-II-miss states = 44 combined + 20 I-only
    hard 121     : [5,7]  ->  9 Type-II-miss states =  9 combined +  0 I-only
    hard 289     : [7]    -> 27 Type-II-miss states = 18 combined +  9 I-only
    hard 169,529 : []     ->254 Type-II-miss states =136 combined +118 I-only.

These are exact local state-universe reductions, not arithmetic realization or
coverage theorems.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(RESEARCH))

import classify_signed_box_residue_automaton as auto  # noqa: E402

HARD_TO_T35 = {
    1: 1,
    121: 6,
    169: 8,
    289: 13,
    361: 16,
    529: 23,
}

EXPECTED_K19 = {
    1: ([5], 64, 44, 20),
    121: ([5, 7], 9, 9, 0),
    169: ([], 254, 136, 118),
    289: ([7], 27, 18, 9),
    361: ([5], 64, 44, 20),
    529: ([], 254, 136, 118),
}


def forced_small_factors(t35: int) -> dict[str, list[int]]:
    forms = {
        "A3=6T-5": 6 * t35 - 5,
        "B7=3T-2": 3 * t35 - 2,
        "C11core=2T-1": 2 * t35 - 1,
        "D15core=3T-1": 3 * t35 - 1,
        "E19=6T-1": 6 * t35 - 1,
    }
    return {
        name: [q for q in (5, 7) if value % q == 0]
        for name, value in forms.items()
    }


def q11_seed_for_hard(hard: int) -> list[int]:
    t35 = HARD_TO_T35[hard]
    seed = [3]
    if (2 * t35 - 1) % 5 == 0:
        seed.append(5)
    return seed


def q19_seed_for_hard(hard: int) -> list[int]:
    t35 = HARD_TO_T35[hard]
    e = 6 * t35 - 1
    return [q for q in (5, 7) if e % q == 0]


def compact(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "seed_residues": summary["seed_residues"],
        "type_II_miss_states": summary["type_II_miss_states"],
        "combined_miss_states": summary["combined_miss_states"],
        "type_I_only_states": summary["type_I_only_states"],
        "minimal_depth_distribution": summary["minimal_depth_distribution"],
        "combined_support_size_distribution": summary[
            "combined_support_size_distribution"
        ],
    }


def verify() -> dict[str, Any]:
    # Evaluate each distinct seed once, then reuse the exact finite closure.
    q11_cache: dict[tuple[int, ...], dict[str, Any]] = {}
    q19_cache: dict[tuple[int, ...], dict[str, Any]] = {}

    class_rows: list[dict[str, Any]] = []
    for hard, t35 in HARD_TO_T35.items():
        factors = forced_small_factors(t35)
        seed11 = q11_seed_for_hard(hard)
        seed19 = q19_seed_for_hard(hard)

        key11 = tuple(seed11)
        if key11 not in q11_cache:
            q11_cache[key11] = auto.classify(11, seed11, 100_000, 8)
        key19 = tuple(seed19)
        if key19 not in q19_cache:
            q19_cache[key19] = auto.classify(19, seed19, 500_000, 8)

        s11 = q11_cache[key11]
        s19 = q19_cache[key19]

        expected_seed, total, combined, ionly = EXPECTED_K19[hard]
        if seed19 != expected_seed:
            raise SystemExit(f"hard={hard}: q19 seed {seed19} != {expected_seed}")
        if (
            s19["type_II_miss_states"],
            s19["combined_miss_states"],
            s19["type_I_only_states"],
        ) != (total, combined, ionly):
            raise SystemExit(
                f"hard={hard}: q19 state counts changed: "
                f"{s19['type_II_miss_states']}, {s19['combined_miss_states']}, "
                f"{s19['type_I_only_states']}"
            )

        if seed11 == [3, 5]:
            if (
                s11["type_II_miss_states"],
                s11["combined_miss_states"],
                s11["type_I_only_states"],
            ) != (5, 5, 0):
                raise SystemExit(f"hard={hard}: seeded q11 closure changed")
        else:
            if seed11 != [3]:
                raise SystemExit(f"hard={hard}: unexpected q11 seed {seed11}")
            if (
                s11["type_II_miss_states"],
                s11["combined_miss_states"],
                s11["type_I_only_states"],
            ) != (11, 9, 2):
                raise SystemExit(f"hard={hard}: base q11 closure changed")

        class_rows.append(
            {
                "p_mod_840": hard,
                "T_mod_35": t35,
                "forced_small_factors": factors,
                "k11": compact(s11),
                "k19": compact(s19),
            }
        )

    # q23 rho=14 gives T=12 mod23, so 23|(2T-1).  At q11 this factor is
    # residue 1 and therefore exactly inert in the signed-box automaton.
    if (2 * 12 - 1) % 23 != 0 or 23 % 11 != 1:
        raise SystemExit("rho14 forced/inert factor-23 identity failed")
    if (2 * 2 - 1) % 23 == 0:
        raise SystemExit("rho5 unexpectedly forces factor 23 in C11 core")

    return {
        "verified": True,
        "mode": "hard-class-predecessor-forced-seeds",
        "hard_to_T_mod35": HARD_TO_T35,
        "classes": class_rows,
        "k11_exact_consequence": (
            "For p mod840 in {169,289,529}, Type-II miss at k11 automatically "
            "implies combined miss; the Type-I-only q11 packets are impossible."
        ),
        "k19_exact_consequence": (
            "For p=121 mod840, Type-II miss at k19 automatically implies combined "
            "miss; the exact seeded local closure has 9 states and no Type-I-only state."
        ),
        "q23_rho14_k11_inert_factor": (
            "rho=14 forces 23|(2T-1), and 23=1 mod11, so this factor is inert in "
            "the k11 signed-box support."
        ),
        "claim_boundary": (
            "Exact local state reductions forced by hard congruence classes.  Abstract "
            "seeded states need not all be arithmetically realized by prime corridor "
            "candidates, and no finite Lane-I ceiling or ES proof is claimed."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
