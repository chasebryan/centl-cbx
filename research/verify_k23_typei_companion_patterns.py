#!/usr/bin/env python3
"""Exact q=23 Type-I companion classification inside the known Type-II defect normal form.

The existing q=23 Type-II filter reduces every Type-II miss to either:

  * pure quadratic splitting; or
  * v2(C)=v3(C)=1, all other quadratic-residue factors congruent to 1 mod 23,
    with primitive nonresidue classes 5 and 14 of total valuation at most 2.

Factors congruent to 1 do not change the signed-box support or C modulo 23, so
all thin-defect Type-I behavior is determined by the six exponent pairs

    (a,b),  a,b >= 0,  a+b <= 2,

where a is total valuation in class 5 and b is total valuation in class 14.

This script exhausts those six states exactly in (Z/23Z)^x and classifies the
Type-II target -1 and the Type-I target -p^-1, using p == 4C (mod 23).

It proves only this finite residue-pattern lemma conditional on the q=23
Type-II normal form.  It does not prove that earlier BREC obstruction ancestry
excludes any of the patterns.
"""

from __future__ import annotations

import json
from typing import Any

MODULUS = 23
TYPE_II_TARGET = 22


def signed_box_support(residue_exponents: dict[int, int]) -> set[int]:
    support = {1}
    for residue, exponent in sorted(residue_exponents.items()):
        if exponent <= 0:
            continue
        inverse = pow(residue, -1, MODULUS)
        local = {
            pow(residue, z, MODULUS)
            if z >= 0
            else pow(inverse, -z, MODULUS)
            for z in range(-exponent, exponent + 1)
        }
        support = {(a * b) % MODULUS for a in support for b in local}
    return support


def classify(a5: int, a14: int) -> dict[str, Any]:
    if a5 < 0 or a14 < 0 or a5 + a14 > 2:
        raise ValueError("thin-defect exponents require a5,a14>=0 and a5+a14<=2")

    exponents = {2: 1, 3: 1}
    if a5:
        exponents[5] = a5
    if a14:
        exponents[14] = a14

    c_mod = 1
    for residue, exponent in exponents.items():
        c_mod = (c_mod * pow(residue, exponent, MODULUS)) % MODULUS
    p_mod = (4 * c_mod) % MODULUS
    type_i_target = (-pow(p_mod, -1, MODULUS)) % MODULUS

    support = signed_box_support(exponents)
    hit_ii = TYPE_II_TARGET in support
    hit_i = type_i_target in support
    if hit_i and hit_ii:
        hit_class = "both"
    elif hit_i:
        hit_class = "type-I-only"
    elif hit_ii:
        hit_class = "type-II-only"
    else:
        hit_class = "miss"

    units = set(range(1, MODULUS))
    return {
        "a5": a5,
        "a14": a14,
        "total_nonresidue_valuation": a5 + a14,
        "C_mod_23": c_mod,
        "p_mod_23": p_mod,
        "type_II_target": TYPE_II_TARGET,
        "type_I_target": type_i_target,
        "support_size": len(support),
        "support": sorted(support),
        "missing": sorted(units - support),
        "hit_type_II": hit_ii,
        "hit_type_I": hit_i,
        "hit_class": hit_class,
    }


def verify() -> dict[str, Any]:
    states = [
        classify(a5, a14)
        for total in range(3)
        for a5 in range(total + 1)
        for a14 in [total - a5]
    ]

    expected = {
        (0, 0): ("miss", 9, 22),
        (1, 0): ("miss", 19, 9),
        (0, 1): ("miss", 19, 18),
        (2, 0): ("type-I-only", 21, 11),
        (1, 1): ("miss", 21, 22),
        (0, 2): ("type-I-only", 21, 21),
    }

    for state in states:
        key = (state["a5"], state["a14"])
        hit_class, support_size, type_i_target = expected[key]
        if state["hit_class"] != hit_class:
            raise SystemExit(
                f"q23 pattern {key}: {state['hit_class']} != {hit_class}"
            )
        if state["support_size"] != support_size:
            raise SystemExit(
                f"q23 pattern {key}: support {state['support_size']} != {support_size}"
            )
        if state["type_I_target"] != type_i_target:
            raise SystemExit(
                f"q23 pattern {key}: Type-I target {state['type_I_target']} "
                f"!= {type_i_target}"
            )
        if state["hit_type_II"]:
            raise SystemExit(f"q23 pattern {key}: expected Type-II miss normal form")

    one_sided = [
        (state["a5"], state["a14"])
        for state in states
        if state["hit_class"] == "type-I-only"
    ]
    if one_sided != [(2, 0), (0, 2)]:
        raise SystemExit(f"unexpected one-sided pattern set: {one_sided}")

    return {
        "verified": True,
        "modulus": MODULUS,
        "conditional_on": "known q=23 Type-II miss normal form",
        "states": states,
        "type_I_only_patterns": [
            {"a5": 2, "a14": 0, "name": "5^2"},
            {"a5": 0, "a14": 2, "name": "14^2"},
        ],
        "conclusion": (
            "Within the q=23 Type-II miss normal form, Type I rescues exactly "
            "the same-class valuation-two thin defects 5^2 and 14^2."
        ),
        "claim_boundary": (
            "This is a finite residue-group classification conditional on the exact "
            "q=23 Type-II normal form; it is not an ancestry-exclusion theorem."
        ),
    }


def main() -> int:
    result = verify()
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
