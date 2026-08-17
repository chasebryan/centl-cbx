#!/usr/bin/env python3
"""Verify the elementary hard-class forced-factor/support atlas at k=19.

For each Mordell-hard residue h mod 840, this records which of the small QR
factors 5 and 7 are forced into C19=(p+19)/4 by h mod5 and h mod7, and the
signed-box support they guarantee modulo 19 before any other factor is used.

Only h121 has both forced factors; their supports fill the complete QR subgroup
mod19.  The atlas is an exact input to class-conditioned BREC k19 analysis, not
a universal k19 miss classification for the other five classes.
"""

from __future__ import annotations

import json

HARD = (1, 121, 169, 289, 361, 529)
HARD_M_MOD35 = {1: 1, 121: 6, 169: 8, 289: 13, 361: 16, 529: 23}
QR19 = {pow(x, 2, 19) for x in range(1, 19)}


def local_support(q: int) -> set[int]:
    return {1, q % 19, pow(q, -1, 19)}


def product_support(parts: list[set[int]]) -> set[int]:
    support = {1}
    for part in parts:
        support = {(a * b) % 19 for a in support for b in part}
    return support


def verify() -> dict[str, object]:
    rows = []
    expected = {
        1: [5],
        121: [5, 7],
        169: [],
        289: [7],
        361: [5],
        529: [],
    }

    for h in HARD:
        forced = []
        if (h + 19) % 5 == 0:
            forced.append(5)
        if (h + 19) % 7 == 0:
            forced.append(7)
        if forced != expected[h]:
            raise SystemExit(f"h={h}: forced {forced} != {expected[h]}")

        parts = [local_support(q) for q in forced]
        support = product_support(parts)
        if not support.issubset(QR19):
            raise SystemExit(f"h={h}: forced support escaped QR19")

        M35 = HARD_M_MOD35[h]
        C19_mod35 = (6 * M35 - 1) % 35
        if 5 in forced and C19_mod35 % 5:
            raise SystemExit(f"h={h}: q23 M class lost forced factor5")
        if 7 in forced and C19_mod35 % 7:
            raise SystemExit(f"h={h}: q23 M class lost forced factor7")

        rows.append(
            {
                "hard_class_mod_840": h,
                "q23_M_mod_35": M35,
                "forced_factors_of_C19": forced,
                "forced_support_mod_19": sorted(support),
                "forced_support_size": len(support),
                "fills_QR19": support == QR19,
                "C19_mod_35": C19_mod35,
            }
        )

    full = [row["hard_class_mod_840"] for row in rows if row["fills_QR19"]]
    if full != [121]:
        raise SystemExit(f"unexpected full-QR forced classes: {full}")

    return {
        "verified": True,
        "mode": "k19-brec-hard-class-support-atlas",
        "QR19": sorted(QR19),
        "factor5_support": sorted(local_support(5)),
        "factor7_support": sorted(local_support(7)),
        "rows": rows,
        "full_QR_forced_classes": full,
        "claim_boundary": (
            "The forced-factor/support atlas is exact.  Only h121 is classified "
            "completely from this atlas alone; other hard classes require further "
            "signed-box analysis."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
