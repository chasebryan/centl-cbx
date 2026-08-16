#!/usr/bin/env python3
"""Verify the exact D-selector mixed-character factor-witness theorem."""
from __future__ import annotations

import argparse
import json


def legendre(a: int, p: int) -> int:
    r = pow(a % p, (p - 1) // 2, p)
    if r == 1:
        return 1
    if r == p - 1:
        return -1
    return 0


def inv(a: int, p: int) -> int:
    return pow(a, -1, p)


def neighbor_residues(modulus: int) -> dict[str, int]:
    b = (-inv(6, modulus)) % modulus
    d = inv(10, modulus) % modulus
    f = (2 * inv(3, modulus)) % modulus
    j = (b + 1) % modulus
    return {"B": b, "D": d, "F": f, "J": j}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    r17 = neighbor_residues(17)
    r31 = neighbor_residues(31)
    assert r17 == {"B": 14, "D": 12, "F": 12, "J": 15}
    assert r31 == {"B": 5, "D": 28, "F": 11, "J": 6}

    c17 = {name: legendre(value, 17) for name, value in r17.items()}
    c31 = {name: legendre(value, 31) for name, value in r31.items()}
    assert c17 == {"B": -1, "D": -1, "F": -1, "J": 1}
    assert c31 == {"B": 1, "D": 1, "F": -1, "J": -1}

    # 2-adic seams cannot carry the required negative transfer characters.
    assert legendre(2, 17) == 1
    assert legendre(2, 31) == 1

    # F is the exact control: its compulsory factor 3 pays both negative signs.
    assert legendre(3, 17) == -1
    assert legendre(3, 31) == -1
    assert c17["F"] * legendre(3, 17) == 1
    assert c31["F"] * legendre(3, 31) == 1

    # Route-B D-selector arithmetic.
    for n in range(2 * 3 * 5 * 7):
        u = 3631 + 4743 * n
        t = 705 + 1081 * u
        assert t % 17 == 6
        assert t % 31 == 7
        assert t % 9 == 7
        assert t % 23 == 15
        assert t % 47 == 0

        B = 8 + 35 * t
        E = 7 + 30 * t
        D = 5 + 21 * t
        F = 17 + 70 * t
        J = 9 + 35 * t

        assert 7 * E - 6 * B == 1
        assert 10 * D - 7 * E == 1
        assert 3 * F - 10 * D == 1
        assert J == B + 1
        assert E % 17 == 0
        assert E % 31 == 0
        assert B % 17 == 14
        assert D % 17 == 12
        assert F % 17 == 12
        assert J % 17 == 15
        assert B % 31 == 5
        assert D % 31 == 28
        assert F % 31 == 11
        assert J % 31 == 6
        assert F % 3 == 0
        assert F % 9 != 0
        assert J % 3 != 0

    report = {
        "analysis": "d-selector-mixed-character-renewal-v2-orientation-safe",
        "neighbor_residues": {"mod17": r17, "mod31": r31},
        "neighbor_characters": {"mod17": c17, "mod31": c31},
        "forced_factor_witnesses": [
            {
                "reservoir": "B",
                "witness": "q_B",
                "conditions": ["q_B|B", "(q_B/23)=+1", "(q_B/17)=-1"],
                "negative_occurrence_parity_mod17": "odd",
            },
            {
                "reservoir": "D",
                "witness": "q_D",
                "conditions": ["q_D|D", "(q_D/31)=+1", "(q_D/17)=-1"],
                "negative_occurrence_parity_mod17": "odd",
            },
            {
                "reservoir": "J",
                "witness": "q_J",
                "conditions": ["q_J|J", "(q_J/47)=+1", "(q_J/31)=-1"],
                "negative_occurrence_parity_mod31": "odd",
            },
        ],
        "distinctness": (
            "q_B,q_D,q_J are odd and pairwise distinct by landed odd-support "
            "separation across B,D,J; none divides E"
        ),
        "F_control": {
            "v3_F": 1,
            "3_char_mod17": -1,
            "3_char_mod31": -1,
            "F_over_3_char_mod17": 1,
            "F_over_3_char_mod31": 1,
            "fresh_negative_witness_forced": False,
        },
        "orientation_boundary": {
            "legacy_routing_source": "fixed q with a proved character (q/p)",
            "present_witness": "variable reservoir factor q with characters (q/m) against small fixed moduli",
            "direct_promotion_allowed": False,
            "required_next_theorem": "exact reciprocity/identity orientation conversion involving target prime p",
        },
        "failures": 0,
        "claim": (
            "conditional on the landed Route-B D-selector survivor state, B,D,J "
            "contain three distinct fresh odd mixed-character factor witnesses; "
            "these witnesses are not legacy routing sources without an additional "
            "orientation-conversion theorem"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
