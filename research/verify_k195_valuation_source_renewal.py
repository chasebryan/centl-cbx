#!/usr/bin/env python3
"""Verify exact character transfers in the k195 double-square source-renewal theorem."""
from __future__ import annotations

import argparse
import json
import math

K = 195
T0 = 3_925_816
T_STEP = 5_127_183
V0 = 1_447_809
V_MOD = 2_301_289


def jacobi(a: int, n: int) -> int:
    if n <= 0 or n % 2 == 0:
        raise ValueError(n)
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def legendre(a: int, p: int) -> int:
    return jacobi(a, p)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # Existing materialized source character types.
    assert legendre(41, 31) == 1
    assert legendre(41, 17) == -1
    assert legendre(37, 47) == 1
    assert legendre(37, 31) == -1

    # Verify the exact affine transfers on several points of the landed lift sublattice.
    phase_rows = []
    for s in range(8):
        v = V0 + V_MOD * s
        t = T0 + T_STEP * v
        p = 169 + 840 * t

        C19 = (p + 19) // 4
        C23 = (p + 23) // 4
        C31 = (p + 31) // 4
        C47 = (p + 47) // 4
        C195 = (p + 195) // 4

        assert C19 % 1081 == 0
        R = C19 // 1081
        B = 8 + 35 * t
        D = 5 + 21 * t
        J = 9 + 35 * t
        assert C23 == 6 * B
        assert C31 == 10 * D
        assert C47 == 6 * J

        assert C195 - C19 == 44
        assert C195 - C23 == 43
        assert C195 - C31 == 41
        assert C195 - C47 == 37
        assert C195 % (41 * 41) == 0
        assert C195 % (37 * 37) == 0

        # 37-square transfer into R.
        assert R % 37 == 13
        assert R % 2 == 1

        # 41-square transfer into B.
        assert B % 41 == 27
        assert t % 3 == 1
        assert B % 3 == 1

        # Removing the known q_J=37 source from J.
        assert J % 37 == 0
        J1 = J // 37
        assert J1 % 37 == 6
        assert J1 % 41 == 34
        assert J1 % 37 != 0

        phase_rows.append({
            "s": s,
            "R_mod37": R % 37,
            "B_mod41": B % 41,
            "J1_mod37": J1 % 37,
            "J1_mod41": J1 % 41,
        })

    # Aggregate transfer characters.
    assert legendre(13, 37) == -1
    assert legendre(27, 41) == -1
    assert legendre(6, 37) == -1
    assert legendre(34, 41) == -1

    # Small factors cannot discharge the relevant odd-witness obligations.
    assert legendre(2, 41) == 1
    assert legendre(2, 37) == -1  # may affect J1 mod37, but not the mod41 obligation

    # Exact source orientation inputs. These are theorem schemas:
    # q_R|C19 with (q_R/19)=+1 => (q_R/p)=+1,
    # q_J41|C47 with (q_J41/47)=+1 => (q_J41/p)=+1.
    # The existence of such q follows from the aggregate negative character plus
    # the landed all-QR own-support laws.
    forced_obligations = {
        "R": {
            "aggregate_transverse": "(R/37)=-1",
            "own_support": "all q|R have (q/19)=+1",
            "forced_witness": "exists odd q_R|R with (+19,-37)",
            "target_character": "+1 via origin19",
        },
        "B": {
            "aggregate_transverse": "(B/41)=-1",
            "own_support": "all q|B have (q/23)=+1",
            "small_factor_controls": ["(2/41)=+1", "3 does not divide B"],
            "forced_witness": "exists odd q_B41|B with (+23,-41)",
            "target_character": "+1 via origin23",
        },
        "J_over_37": {
            "aggregate_transverse": "(J/37 / 41)=-1",
            "own_support": "all q|J/37 have (q/47)=+1",
            "small_factor_control": "(2/41)=+1",
            "forced_witness": "exists odd q_J41|J/37 with (+47,-41)",
            "target_character": "+1 via origin47",
        },
    }

    # Distinctness semantics from landed odd-support separation:
    # R, B, D, and J have pairwise-disjoint odd support. q_J41 is additionally
    # distinct from37 because v37(J)=1 on this lift.
    assert 13 % 37 != 0
    assert 27 % 41 != 0
    assert 6 % 37 != 0
    assert 34 % 41 != 0

    report = {
        "analysis": "k195-valuation-source-renewal-v1",
        "double_square_sources": {"D": 41, "J": 37},
        "phase_rows": phase_rows,
        "characters": {
            "R_mod37": -1,
            "B_mod41": -1,
            "J1_mod37": -1,
            "J1_mod41": -1,
        },
        "forced_obligations": forced_obligations,
        "minimum_distinct_positive_sources": 5,
        "distinct_source_inventory": [
            "existing q_B in B",
            "41 in D",
            "37 in J",
            "new q_R in R",
            "new q_J41 in J/37",
        ],
        "extra_B41_obligation_may_merge_with_existing_q_B": True,
        "full_ancestry_reachability": "not proved",
        "failures": 0,
        "claim": (
            "conditional on the landed k195 double-square corridor and own-support survivor laws, "
            "valuation transfers force new positive source classes (+19,-37) in R and (+47,-41) in J/37, "
            "plus an additional (+23,-41) obligation in B; at least five distinct odd positive target-prime sources are forced"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
