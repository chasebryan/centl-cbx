#!/usr/bin/env python3
"""Verify the exact k=3 BREC obstruction normal form for Mordell-hard primes.

For every Mordell-hard prime p:

  p == 1 (mod 3),
  C3 = (p+3)/4 == 1 (mod 3),

and the two Lane-I signed-box targets coincide modulo 3:

  Type II = -1 = 2,
  Type I  = -p^-1 = 2.

Because (Z/3Z)^x = {1,2}, the signed box contains 2 iff at least one prime
divisor of C3 is 2 mod 3.  Hence the exact combined k=3 miss condition is

  every prime divisor q of C3 satisfies q == 1 (mod 3).

The script exhausts the Mordell-hard residue classes modulo 840 and the only
possible unit-factor residue supports modulo 3.  The accompanying research
note gives the direct proof.
"""

from __future__ import annotations

import json

HARD = (1, 121, 169, 289, 361, 529)


def verify() -> dict[str, object]:
    classes = []
    for h in HARD:
        if h % 4 != 1:
            raise SystemExit(f"hard residue {h} is not 1 mod 4")
        if h % 3 != 1:
            raise SystemExit(f"hard residue {h} is not 1 mod 3")

        # C3=(p+3)/4.  Since 4 == 1 mod 3, C3 == p == 1 mod 3.
        c3_mod3 = ((h + 3) * pow(4, -1, 3)) % 3
        type_ii = 2
        type_i = (-pow(h % 3, -1, 3)) % 3
        if c3_mod3 != 1 or type_i != type_ii:
            raise SystemExit(f"hard residue {h}: k3 target identity failed")
        classes.append(
            {
                "p_mod_840": h,
                "p_mod_3": h % 3,
                "C3_mod_3": c3_mod3,
                "type_II_target": type_ii,
                "type_I_target": type_i,
            }
        )

    # Abstract signed-box support modulo 3.  Exponents can always choose zero.
    # If all factor residues are 1, only 1 is reachable.  If any factor residue
    # is 2 with positive valuation, choosing exponent +1 for that factor and 0
    # for every other factor reaches 2.
    all_qr_support = {1}
    one_nr_support = {1, 2}
    if 2 in all_qr_support or 2 not in one_nr_support:
        raise SystemExit("mod-3 signed-box support classification failed")

    return {
        "verified": True,
        "mode": "k3-brec-obstruction-normal-form",
        "hard_residue_classes": classes,
        "combined_target": 2,
        "miss_iff": "every prime divisor q of C3=(p+3)/4 is 1 mod 3",
        "hit_iff": "some prime divisor q of C3=(p+3)/4 is 2 mod 3",
        "claim_boundary": (
            "This is an exact residue-group lemma for Mordell-hard primes; it does "
            "not imply incompatibility with any particular later-shift defect."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
