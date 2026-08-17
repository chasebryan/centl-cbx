#!/usr/bin/env python3
"""Verify the exact k=19 BREC obstruction normal form in hard class h=121.

For a Mordell-hard prime p == 121 mod 840:

  p == 1 mod 5  ->  5 divides C19=(p+19)/4,
  p == 2 mod 7  ->  7 divides C19.

Modulo 19, 5 is a quadratic-residue generator of order 9 and 7=5^6 has
order 3.  Their valuation-one signed supports already sum to the complete QR
subgroup of (Z/19Z)^x.  Therefore:

    sigma_19(p) = -
    iff every prime divisor of C19 is a quadratic residue mod 19.

Any NR factor fills the other coset and hence the full unit group.  Both exact
targets then hit.  If all factors are QR, p is QR mod19 and both targets are
NR, so both miss.
"""

from __future__ import annotations

import json

MOD = 19
HARD_CLASS = 121
QR19 = {pow(x, 2, MOD) for x in range(1, MOD)}
NR19 = set(range(1, MOD)) - QR19


def signed_local(residue: int, exponent: int = 1) -> set[int]:
    inv = pow(residue, -1, MOD)
    return {
        pow(residue, z, MOD) if z >= 0 else pow(inv, -z, MOD)
        for z in range(-exponent, exponent + 1)
    }


def verify() -> dict[str, object]:
    if HARD_CLASS % 5 != 1 or HARD_CLASS % 7 != 2:
        raise SystemExit("h121 forced-factor congruences failed")

    if 5 not in QR19 or 7 not in QR19:
        raise SystemExit("forced 5/7 factors are not QR mod19")

    # Order checks.
    order5 = next(e for e in range(1, 19) if pow(5, e, 19) == 1)
    order7 = next(e for e in range(1, 19) if pow(7, e, 19) == 1)
    if order5 != 9 or order7 != 3:
        raise SystemExit(f"unexpected orders: ord19(5)={order5}, ord19(7)={order7}")
    if pow(5, 6, 19) != 7:
        raise SystemExit("7 != 5^6 mod19")

    support5 = signed_local(5)
    support7 = signed_local(7)
    combined = {(a * b) % 19 for a in support5 for b in support7}
    if combined != QR19:
        raise SystemExit(f"forced 5/7 support does not fill QR19: {combined}")

    # Every NR representative multiplies QR19 onto the complete NR coset.
    nr_coset_checks = {}
    for q in sorted(NR19):
        coset = {(q * r) % 19 for r in QR19}
        if coset != NR19:
            raise SystemExit(f"q={q}: NR coset mismatch")
        nr_coset_checks[str(q)] = len(coset)

    # Type-II target -1 is NR.  If p is QR, Type-I -p^-1 is NR too.
    if 18 not in NR19:
        raise SystemExit("-1 is not NR mod19")
    for p19 in sorted(QR19):
        target_i = (-pow(p19, -1, 19)) % 19
        if target_i not in NR19:
            raise SystemExit(f"QR p={p19}: Type-I target is not NR")

    return {
        "verified": True,
        "mode": "h121-k19-brec-obstruction-normal-form",
        "hard_class_mod_840": HARD_CLASS,
        "forced_prime_factors_of_C19": [5, 7],
        "QR19": sorted(QR19),
        "NR19": sorted(NR19),
        "ord19_5": order5,
        "ord19_7": order7,
        "support_from_5": sorted(support5),
        "support_from_7": sorted(support7),
        "forced_combined_support": sorted(combined),
        "forced_combined_support_is_QR19": True,
        "nonresidue_coset_checks": nr_coset_checks,
        "two_target_coincidence": True,
        "miss_iff": (
            "every prime divisor q of C19=(p+19)/4 is a quadratic residue mod 19"
        ),
        "q23_rescue_translation": {
            "hard_M_mod_35": 6,
            "C19": "6*H*D-1",
            "forced_divisor": 35,
            "miss_iff": "every prime divisor of 6*H*D-1 is QR mod 19",
        },
        "claim_boundary": (
            "This exact k19 theorem is restricted to Mordell-hard class 121 mod840. "
            "Other hard classes require separate k19 analysis."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
