#!/usr/bin/env python3
"""Verify the exact k=15 BREC combined-obstruction normal form.

For every Mordell-hard prime p:

  * p mod 15 is 1 or 4;
  * C15=(p+15)/4 mod 15 is therefore 4 or 1;
  * p == 1 mod 8, so C15 is even;
  * the forced factor 2 lies in the order-four subgroup
        H=<2>={1,2,4,8} of (Z/15Z)^x;
  * both exact targets lie in the other coset -H={7,11,13,14}.

The theorem is

    sigma_15(p) = -
    iff every prime divisor of C15 lies in H.

The only possible thin-support loophole is v2(C15)=1 with every other H-factor
congruent to 1.  Exact coset coordinates plus the hard condition C15 mod15 in
{1,4} show that any outside-H factor then forces the Type-II target to occur.
"""

from __future__ import annotations

import json
from typing import Any

MOD = 15
H = {1, 2, 4, 8}
K = {7, 11, 13, 14}
HARD = (1, 121, 169, 289, 361, 529)


def signed_support(residue_valuations: dict[int, int]) -> set[int]:
    support = {1}
    for residue, exponent in sorted(residue_valuations.items()):
        if exponent <= 0:
            continue
        if residue % 3 == 0 or residue % 5 == 0:
            raise ValueError(f"nonunit residue {residue} mod15")
        inv = pow(residue, -1, MOD)
        local = {
            pow(residue, z, MOD) if z >= 0 else pow(inv, -z, MOD)
            for z in range(-exponent, exponent + 1)
        }
        support = {(a * b) % MOD for a in support for b in local}
    return support


def classify(residue_valuations: dict[int, int]) -> dict[str, Any]:
    if residue_valuations.get(2, 0) < 1:
        raise ValueError("k15 state requires the forced factor 2")
    C = 1
    for residue, exponent in residue_valuations.items():
        C = (C * pow(residue, exponent, MOD)) % MOD
    p = (4 * C) % MOD
    support = signed_support(residue_valuations)
    target_ii = 14
    target_i = (-pow(p, -1, MOD)) % MOD
    hit_ii = target_ii in support
    hit_i = target_i in support
    if hit_i and hit_ii:
        hit_class = "both"
    elif hit_i:
        hit_class = "type-I-only"
    elif hit_ii:
        hit_class = "type-II-only"
    else:
        hit_class = "miss"
    return {
        "valuations": {str(k): v for k, v in sorted(residue_valuations.items()) if v},
        "C_mod_15": C,
        "p_mod_15": p,
        "support": sorted(support),
        "target_type_II": target_ii,
        "target_type_I": target_i,
        "hit_class": hit_class,
    }


def verify() -> dict[str, Any]:
    # Hard residue and target-coset input.
    classes = []
    for h in HARD:
        p15 = h % MOD
        if p15 not in {1, 4}:
            raise SystemExit(f"hard residue {h}: p mod15={p15}")
        if h % 8 != 1:
            raise SystemExit(f"hard residue {h}: p is not 1 mod8")
        C15 = (p15 * pow(4, -1, MOD)) % MOD
        if C15 not in {1, 4}:
            raise SystemExit(f"hard residue {h}: C15 mod15={C15}")
        target_i = (-pow(p15, -1, MOD)) % MOD
        if target_i not in K or 14 not in K:
            raise SystemExit(f"hard residue {h}: target escaped -H")
        classes.append(
            {
                "p_mod_840": h,
                "p_mod_15": p15,
                "C15_mod_15": C15,
                "type_II_target": 14,
                "type_I_target": target_i,
            }
        )

    # Forced factor 2, valuation one, is H with the element 4 missing.
    forced_one = signed_support({2: 1})
    forced_two = signed_support({2: 2})
    if forced_one != {1, 2, 8}:
        raise SystemExit(f"v2=1 support mismatch: {forced_one}")
    if forced_two != H:
        raise SystemExit(f"v2=2 does not fill H: {forced_two}")

    # Any second nontrivial H factor fills H with forced v2=1.
    h_fill = {}
    for residue in sorted(H - {1, 2}):
        support = signed_support({2: 1, residue: 1})
        if support != H:
            raise SystemExit(f"H residue {residue} failed to fill H: {support}")
        h_fill[str(residue)] = sorted(support)

    # Once H is full, any K factor fills the entire unit group.
    units = H | K
    full_coset = {}
    for residue in sorted(K):
        support = signed_support({2: 2, residue: 1})
        if support != units:
            raise SystemExit(f"full H + K residue {residue} did not fill units")
        full_coset[str(residue)] = sorted(support)

    # Thin support coordinates.  Write H=<a=2> and K=-a^j.
    # Mapping j -> residue is {0:14,1:13,2:11,3:7}.
    k_by_j = {0: 14, 1: 13, 2: 11, 3: 7}
    thin_single = {}
    for j, residue in k_by_j.items():
        state = classify({2: 1, residue: 1})
        thin_single[str(j)] = state
        # j=0 reaches Type II directly; j=+/-1 reaches both K targets;
        # j=2 reaches the Type-I target 11 but not Type II in isolation.
        if j == 0 and 14 not in state["support"]:
            raise SystemExit("thin K j=0 failed to reach Type II")
        if j in {1, 3} and not {11, 14}.issubset(set(state["support"])):
            raise SystemExit(f"thin K j={j} failed to reach both target positions")
        if j == 2 and 14 in state["support"]:
            raise SystemExit("thin K j=2 unexpectedly reached Type II")

    # If every K factor were j=2 (residue 11), avoiding Type II in the thin
    # skeleton, their total valuation m must be even because hard C15 is in H.
    # Then the K product is (-4)^m = 1 mod15 and C15 would be forced to 2,
    # contradicting hard C15 in {1,4}.
    impossible_all_11 = []
    for m in (2, 4, 6):
        C15 = (2 * pow(11, m, MOD)) % MOD
        impossible_all_11.append({"m": m, "C15_mod_15": C15})
        if C15 != 2 or C15 in {1, 4}:
            raise SystemExit(f"all-11 thin contradiction failed at m={m}")

    # Canonical all-H states miss both targets.
    all_h_cases = [
        classify({2: 1, 1: 3}),
        classify({2: 2}),
        classify({2: 1, 4: 1}),
    ]
    for state in all_h_cases:
        if state["C_mod_15"] in {1, 4} and state["hit_class"] != "miss":
            raise SystemExit(f"hard-compatible all-H state did not miss: {state}")

    return {
        "verified": True,
        "mode": "k15-brec-obstruction-normal-form",
        "H": sorted(H),
        "minus_H": sorted(K),
        "hard_residue_classes": classes,
        "forced_factor": 2,
        "forced_v1_support": sorted(forced_one),
        "forced_v2_support": sorted(forced_two),
        "H_fill_checks": h_fill,
        "full_coset_checks": full_coset,
        "thin_single_K_checks": thin_single,
        "thin_all_11_contradiction": impossible_all_11,
        "combined_miss_iff": (
            "every prime divisor q of C15=(p+15)/4 lies in {1,2,4,8} mod 15"
        ),
        "q23_rescue_translation": {
            "C15": "2*(3*H*D-1)",
            "miss_iff": (
                "every prime divisor of 3*H*D-1 lies in {1,2,4,8} mod 15"
            ),
        },
        "claim_boundary": (
            "This is an exact k=15 combined-miss lemma for Mordell-hard primes; "
            "it does not eliminate the q23 Type-I rescue family."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
