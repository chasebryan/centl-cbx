#!/usr/bin/env python3
"""Verify the exact k=7 BREC obstruction normal form for Mordell-hard primes.

For every Mordell-hard prime p:

  * p mod 7 is in {1,2,4}, the quadratic-residue subgroup;
  * p == 1 mod 8, so C7=(p+7)/4 is even;
  * the forced factor 2 is a nontrivial quadratic residue mod 7 and its signed
    exponent {-1,0,+1} already generates the full QR subgroup {1,2,4};
  * both Lane-I targets -1 and -p^-1 are quadratic nonresidues mod 7.

Consequently the signed box at k=7 is exactly the QR subgroup when every prime
divisor of C7 is a QR mod 7, and becomes the full unit group as soon as one NR
prime divisor occurs.  Hence the two targets always have the same hit/miss
status and

    sigma_7(p) = -
    iff every prime divisor q of C7=(p+7)/4 is in {1,2,4} mod 7.

On the q23 Type-I-only rescue branch C23=6HD, p=24HD-23, this translates to

    C7 = 2*(3HD-2)

and the k7 miss condition is exactly that every prime divisor of 3HD-2 is a
quadratic residue modulo 7.
"""

from __future__ import annotations

import json

HARD = (1, 121, 169, 289, 361, 529)
QR7 = {1, 2, 4}
NR7 = {3, 5, 6}
UNITS7 = set(range(1, 7))


def legendre7(a: int) -> int:
    a %= 7
    if a == 0:
        return 0
    v = pow(a, 3, 7)
    if v == 1:
        return 1
    if v == 6:
        return -1
    raise RuntimeError(f"unexpected Euler value {v} mod 7")


def verify() -> dict[str, object]:
    classes = []
    for h in HARD:
        p7 = h % 7
        if p7 not in QR7:
            raise SystemExit(f"hard residue {h}: p mod7={p7} is not QR")
        if h % 8 != 1:
            raise SystemExit(f"hard residue {h}: p is not 1 mod8")

        type_ii = 6
        type_i = (-pow(p7, -1, 7)) % 7
        if type_i not in NR7 or type_ii not in NR7:
            raise SystemExit(f"hard residue {h}: k7 target is not NR")

        c7 = ((h + 7) // 4) % 7
        if c7 not in QR7:
            raise SystemExit(f"hard residue {h}: C7 mod7={c7} is not QR")

        classes.append(
            {
                "p_mod_840": h,
                "p_mod_7": p7,
                "C7_mod_7": c7,
                "type_II_target": type_ii,
                "type_I_target": type_i,
            }
        )

    # The forced factor 2 has exponent at least one.  Its local signed support
    # is {2^-1,1,2} = {4,1,2}, exactly QR7.
    forced_two = {pow(2, -1, 7), 1, 2}
    if forced_two != QR7:
        raise SystemExit(f"forced factor 2 does not generate QR7: {forced_two}")

    # Multiplication by any NR is the other coset.  Once one NR factor is
    # available at signed exponent +1, QR7 union q*QR7 is the full unit group.
    cosets = {}
    for q in sorted(NR7):
        nr_coset = {(q * r) % 7 for r in QR7}
        if nr_coset != NR7:
            raise SystemExit(f"q={q}: NR coset mismatch {nr_coset}")
        if QR7 | nr_coset != UNITS7:
            raise SystemExit(f"q={q}: QR+NR does not fill units")
        cosets[str(q)] = sorted(nr_coset)

    # Inversion and -1 character check for the Type-I target.
    for p7 in QR7:
        if legendre7((-pow(p7, -1, 7)) % 7) != -1:
            raise SystemExit(f"p7={p7}: Type-I target character failed")
    if legendre7(6) != -1:
        raise SystemExit("Type-II target -1 is not NR mod7")

    return {
        "verified": True,
        "mode": "k7-brec-obstruction-normal-form",
        "hard_residue_classes": classes,
        "QR7": sorted(QR7),
        "NR7": sorted(NR7),
        "forced_factor": 2,
        "forced_factor_signed_support": sorted(forced_two),
        "nonresidue_cosets": cosets,
        "two_target_coincidence": True,
        "miss_iff": (
            "every prime divisor q of C7=(p+7)/4 is a quadratic residue mod 7"
        ),
        "hit_iff": (
            "some prime divisor q of C7=(p+7)/4 is a quadratic nonresidue mod 7"
        ),
        "q23_rescue_translation": {
            "C7": "2*(3*H*D-2)",
            "miss_iff": (
                "every prime divisor of 3*H*D-2 is in {1,2,4} mod 7"
            ),
        },
        "claim_boundary": (
            "This is an exact k=7 residue-group lemma for Mordell-hard primes. "
            "It does not classify compatibility with all later shifts."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
