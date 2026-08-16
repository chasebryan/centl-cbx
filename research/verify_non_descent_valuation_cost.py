#!/usr/bin/env python3
"""Verify the non-descent valuation and q-adic phase-cost bounds."""
from __future__ import annotations

import argparse
import json


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def output_ceiling(e: int) -> int:
    assert e >= 1
    return 324 * e + 163


def non_descent_floor(q: int) -> int:
    assert q >= 2
    return max(1, ceil_div(q - 163, 324))


def non_descent_index(q: int) -> int:
    e = non_descent_floor(q)
    return q ** (e - 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    # Exact threshold ladder.
    assert output_ceiling(1) == 487
    assert output_ceiling(2) == 811
    assert output_ceiling(3) == 1135
    assert output_ceiling(4) == 1459
    assert non_descent_floor(487) == 1
    assert non_descent_floor(488) == 2
    assert non_descent_floor(811) == 2
    assert non_descent_floor(812) == 3
    assert non_descent_floor(1135) == 3
    assert non_descent_floor(1136) == 4

    # For every q in a broad exact range, e below E_nd forces ceiling < q,
    # while e=E_nd is the first valuation whose ceiling can reach q.
    checked = 0
    for q in range(2, 20_001):
        e0 = non_descent_floor(q)
        assert output_ceiling(e0) >= q or e0 == 1
        for e in range(1, e0):
            assert output_ceiling(e) < q
        if e0 > 1:
            assert output_ceiling(e0 - 1) < q
            assert output_ceiling(e0) >= q
        checked += 1

    # Fixed-cap form: q > 324E+163 forces descent for all e<=E.
    cap_rows = []
    for E in range(1, 11):
        threshold = output_ceiling(E)
        for q in (threshold + 1, threshold + 17, threshold + 1000):
            for e in range(1, E + 1):
                assert output_ceiling(e) < q
        cap_rows.append({"valuation_cap": E, "max_non_descent_source": threshold})

    # Pinned examples.
    assert non_descent_floor(1009) == 3
    assert non_descent_index(1009) == 1009**2 == 1_018_081
    assert non_descent_floor(5003) == 15
    assert non_descent_index(5003) == 5003**14
    assert non_descent_floor(317) == 1

    examples = []
    for q in (317, 487, 488, 811, 812, 1009, 5003, 10_007):
        e0 = non_descent_floor(q)
        examples.append({
            "q": q,
            "minimum_non_descent_valuation": e0,
            "minimum_phase_index": str(q ** (e0 - 1)),
            "previous_valuation_ceiling": output_ceiling(e0 - 1) if e0 > 1 else None,
            "first_possible_ceiling": output_ceiling(e0),
        })

    # Known landed transitions are consistent.
    # q317 e2 -> 13,167 are both descents, though descent was not forced by threshold.
    assert 13 < 317 and 167 < 317
    assert output_ceiling(2) == 811
    # q29 e10 -> 317 is an ascent allowed because q29 is in the small-source window.
    assert 317 <= output_ceiling(10)
    assert non_descent_floor(29) == 1

    report = {
        "analysis": "non-descent-valuation-cost-v1",
        "checked_source_integers": checked,
        "cap_rows": cap_rows,
        "examples": examples,
        "pinned": {
            "q1009": {"E_nd": 3, "I_nd": 1_018_081},
            "q5003": {"E_nd": 15, "I_nd": str(5003**14)},
            "q317": {"E_nd": 1, "landed_e2_outputs": [13, 167]},
        },
        "termination_rank": False,
        "failures": 0,
        "claim": (
            "if a one-source h169 Jacobi-saturated miss produces an extracted prime r>=q, then "
            "e>=max(1,ceil((q-163)/324)); consequently its q-adic phase index is at least q^(E_nd(q)-1)"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
