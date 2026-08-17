#!/usr/bin/env python3
"""Verify concrete applications of the QR support reservoir saturation lemma.

For q == 3 (mod 4), suppose a QR-only subfactor A has exact signed-box support
Q_q, the full quadratic-residue subgroup.  Then an independent NR factor r
adds the complete coset r*Q_q, so the full support becomes U(q).  If the
residual factors are all QR, support remains Q_q and both Lane-I targets are NR.

The general implication is an elementary coset proof.  This executable object
freezes the concrete repository reservoirs:

  * q=19, A=5*7      (h121 k19);
  * q=11, A=3^2      (k11 whenever v3>=2);
  * q=19, A=5^4      (h1/h361 k19 whenever v5>=4).
"""

from __future__ import annotations

import json
from typing import Any


def factor_signed_support(mod: int, factors: list[tuple[int, int]]) -> set[int]:
    support = {1}
    for residue, exponent in factors:
        r = residue % mod
        if r == 0:
            raise ValueError("reservoir factors must be units")
        local = {pow(r, z, mod) for z in range(-exponent, exponent + 1)}
        support = {(a * b) % mod for a in support for b in local}
    return support


def qr_group(q: int) -> set[int]:
    return {pow(x, 2, q) for x in range(1, q)}


def verify_application(
    name: str,
    q: int,
    factors: list[tuple[int, int]],
) -> dict[str, Any]:
    if q % 4 != 3:
        raise SystemExit(f"{name}: q={q} is not 3 mod4")
    Q = qr_group(q)
    U = set(range(1, q))
    NR = U - Q
    support = factor_signed_support(q, factors)

    if support != Q:
        raise SystemExit(
            f"{name}: reservoir support {sorted(support)} != Q={sorted(Q)}"
        )
    for residue, _ in factors:
        if residue % q not in Q:
            raise SystemExit(f"{name}: reservoir contains NR residue {residue}")

    nr_cosets: dict[str, list[int]] = {}
    for r in sorted(NR):
        coset = {(r * x) % q for x in Q}
        if coset != NR:
            raise SystemExit(f"{name}: r={r} does not map Q onto NR coset")
        combined = Q | coset
        if combined != U:
            raise SystemExit(f"{name}: Q union rQ is not U(q)")
        nr_cosets[str(r)] = sorted(coset)

    # If C is QR, p=4C is QR.  For q=3 mod4, both -1 and -p^-1 are NR.
    target_rows = []
    if (q - 1) in Q:
        raise SystemExit(f"{name}: -1 is unexpectedly QR")
    for C in sorted(Q):
        p = (4 * C) % q
        if p not in Q:
            raise SystemExit(f"{name}: p=4C is not QR for C={C}")
        type_ii = q - 1
        type_i = (-pow(p, -1, q)) % q
        if type_ii not in NR or type_i not in NR:
            raise SystemExit(f"{name}: target character failure at C={C}")
        if type_ii in support or type_i in support:
            raise SystemExit(f"{name}: QR reservoir unexpectedly hits NR target")
        target_rows.append(
            {
                "C_mod_q": C,
                "p_mod_q": p,
                "type_II_target": type_ii,
                "type_I_target": type_i,
            }
        )

    return {
        "name": name,
        "q": q,
        "factors": [
            {"residue": residue, "valuation": exponent}
            for residue, exponent in factors
        ],
        "Q": sorted(Q),
        "NR": sorted(NR),
        "support": sorted(support),
        "support_size": len(support),
        "all_NR_representatives_fill_U": True,
        "nr_cosets": nr_cosets,
        "target_character_rows": target_rows,
    }


def multiplicative_order(a: int, q: int) -> int:
    x = 1
    for n in range(1, q):
        x = x * a % q
        if x == 1:
            return n
    raise RuntimeError("order not found")


def verify_thresholds() -> list[dict[str, int]]:
    rows = []
    for q, residue, expected_order, expected_threshold in (
        (11, 3, 5, 2),
        (19, 5, 9, 4),
    ):
        order = multiplicative_order(residue, q)
        if order != expected_order:
            raise SystemExit(
                f"q={q}, residue={residue}: order {order} != {expected_order}"
            )
        threshold = (order - 1) // 2
        if threshold != expected_threshold:
            raise SystemExit(
                f"q={q}, residue={residue}: threshold {threshold} != {expected_threshold}"
            )
        below = factor_signed_support(q, [(residue, threshold - 1)])
        at = factor_signed_support(q, [(residue, threshold)])
        Q = qr_group(q)
        if below == Q:
            raise SystemExit(f"q={q}: reservoir saturates before claimed threshold")
        if at != Q:
            raise SystemExit(f"q={q}: reservoir fails at claimed threshold")
        rows.append(
            {
                "q": q,
                "generator_residue": residue,
                "QR_order": order,
                "valuation_threshold": threshold,
                "support_size_below": len(below),
                "support_size_at_threshold": len(at),
            }
        )
    return rows


def verify_hard_class_valuation_conditions() -> dict[str, Any]:
    # h1/h361 force one factor 5 at C19=(p+19)/4.  The valuation-four
    # saturation condition is equivalent to p+19 divisible by 4*5^4 because
    # four is a 5-adic unit.
    for hard in (1, 361):
        if (hard + 19) % 5:
            raise SystemExit(f"hard={hard}: factor5 is not forced in C19")

    modulus = 625
    target_p_mod625 = (-19) % modulus
    if target_p_mod625 != 606:
        raise SystemExit("p mod625 threshold residue changed")

    return {
        "hard_classes_with_forced_5": [1, 361],
        "base_forcing": "5 | C19",
        "saturation_condition": "v5(C19)>=4",
        "equivalent_p_congruence_mod_625": target_p_mod625,
    }


def verify() -> dict[str, Any]:
    applications = [
        verify_application("h121-k19-forced-5x7", 19, [(5, 1), (7, 1)]),
        verify_application("k11-v3-at-least-2", 11, [(3, 2)]),
        verify_application("h1-h361-k19-v5-at-least-4", 19, [(5, 4)]),
    ]
    thresholds = verify_thresholds()
    hard = verify_hard_class_valuation_conditions()

    return {
        "verified": True,
        "mode": "qr-support-reservoir-saturation",
        "applications": applications,
        "generator_thresholds": thresholds,
        "h1_h361_k19": hard,
        "lemma": (
            "For q=3 mod4, if a QR-only factor subcollection A has exact signed "
            "support Q_q, then an independent NR factor fills the opposite coset "
            "and hence U(q); if all residual factors are QR, support remains Q_q "
            "and both Lane-I targets miss."
        ),
        "claim_boundary": (
            "Executable verification of concrete reservoir applications and threshold "
            "arithmetic.  The general lemma is the elementary coset argument; no "
            "global Lane-I ceiling or Erdos-Straus proof is claimed."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
