#!/usr/bin/env python3
"""Verify the h169 k11-miss future factor-11 partition.

For h169 write

    p = 169 + 840 t,
    T = (p+23)/24 = 8 + 35 t.

The landed class-conditioned k11 theorem says a combined miss is pure-QR.
Therefore 2T-1 is a quadratic residue modulo 11, which restricts

    T mod11 to {1,2,3,5,8}

and equivalently

    t mod11 to {0,2,3,4,8}.

The post-k23 companion ladder is

    C_(23+4j) = 6T + j.

For each of the five allowed phases there is a unique first positive j with
11 | C_(23+4j).  The resulting h169 partition is

    t11  T11  p11  j   k
      0    8    4   7  51
      2    1    1   5  43
      3    3    5   4  39
      4    5    9   3  35
      8    2    3  10  63.

Thus every h169 k11 combined miss carries a deterministic future factor-11
appointment, no later than k63.  This is a congruence/ancestry theorem only;
it does not say the later signed box misses or hits.
"""

from __future__ import annotations

import json

QR11 = {1, 3, 4, 5, 9}
EXPECTED_T11 = {1, 2, 3, 5, 8}
EXPECTED_T_SMALL = {0, 2, 3, 4, 8}
EXPECTED = {
    0: {"T11": 8, "p11": 4, "j": 7, "k": 51},
    2: {"T11": 1, "p11": 1, "j": 5, "k": 43},
    3: {"T11": 3, "p11": 5, "j": 4, "k": 39},
    4: {"T11": 5, "p11": 9, "j": 3, "k": 35},
    8: {"T11": 2, "p11": 3, "j": 10, "k": 63},
}


def first_positive_j(T11: int) -> int:
    for j in range(1, 12):
        if (6 * T11 + j) % 11 == 0:
            return j
    raise RuntimeError("no factor-11 companion phase found")


def pure_qr_T_phases() -> set[int]:
    inv2 = pow(2, -1, 11)
    return {((r + 1) * inv2) % 11 for r in QR11}


def verify() -> dict[str, object]:
    T_phases = pure_qr_T_phases()
    if T_phases != EXPECTED_T11:
        raise SystemExit(f"pure-QR T11 phases changed: {sorted(T_phases)}")

    allowed_t = {
        t11
        for t11 in range(11)
        if (8 + 35 * t11) % 11 in T_phases
    }
    if allowed_t != EXPECTED_T_SMALL:
        raise SystemExit(f"h169 t11 phase set changed: {sorted(allowed_t)}")

    rows = []
    shifts = set()
    for t11 in sorted(allowed_t):
        T11 = (8 + 35 * t11) % 11
        p11 = (169 + 840 * t11) % 11
        if p11 != (2 * T11 - 1) % 11:
            raise SystemExit(f"t11={t11}: p/T coordinate disagreement")

        j = first_positive_j(T11)
        k = 23 + 4 * j
        expected = EXPECTED[t11]
        actual = {"T11": T11, "p11": p11, "j": j, "k": k}
        if actual != expected:
            raise SystemExit(f"t11={t11}: {actual} != {expected}")

        # Universal congruence check in the h169 progression.  Modulo 44 is
        # enough because 11 | (p+k)/4 iff 44 | p+k.
        p44 = (169 + 840 * t11) % 44
        if (p44 + k) % 44 != 0:
            raise SystemExit(f"t11={t11}: factor11 does not divide C{k}")

        # j is the first positive occurrence in the post-k23 ladder.
        for earlier in range(1, j):
            if (6 * T11 + earlier) % 11 == 0:
                raise SystemExit(f"t11={t11}: factor11 occurred before j={j}")

        shifts.add(k)
        rows.append(
            {
                "t_mod_11": t11,
                "T_mod_11": T11,
                "p_mod_11": p11,
                "first_post_k23_j_with_factor_11": j,
                "shift_k": k,
                "companion": f"C{k}",
            }
        )

    if shifts != {35, 39, 43, 51, 63}:
        raise SystemExit(f"future shift partition changed: {sorted(shifts)}")

    # Calendar-to-grammar interface at k35.  On t=4 mod11, factor11 lies in
    # F=C35/3.  The exact S7 branch requires every non-distinguished factor to
    # be 1 mod7 and exactly one distinguished factor 3 mod7.  Since 11=4 mod7,
    # S7 is impossible.  The J35 character branch remains compatible because
    # 11 lies in H35.
    H35 = {1, 3, 4, 9, 11, 12, 13, 16, 17, 27, 29, 33}
    if 11 % 7 != 4 or 11 % 35 not in H35:
        raise SystemExit("k35 factor11 branch interface changed")

    return {
        "verified": True,
        "mode": "h169-k11-future-factor11-partition",
        "h169_coordinate": "p=169+840t; T=8+35t",
        "k11_combined_miss_implies_t_mod_11": sorted(allowed_t),
        "partition": rows,
        "future_factor_11_shifts": sorted(shifts),
        "latest_forced_shift": max(shifts),
        "calendar_to_grammar_interfaces": {
            "t_mod_11_3": (
                "p mod11=5 and 11|C39; the landed routed k39 Jacobi-plus "
                "support theorem applies if k39 also misses"
            ),
            "t_mod_11_4": (
                "11|C35 and literal 11=4 mod7 excludes the k35 S7 branch; "
                "therefore a k35 miss is J35-only"
            ),
        },
        "theorem": (
            "Every h169 k11 combined miss lies in exactly one of five t mod11 "
            "phases, each of which forces literal factor11 into a deterministic "
            "post-k23 companion C35,C39,C43,C51,or C63."
        ),
        "claim_boundary": (
            "Exact necessary ancestry/congruence partition.  It does not assert "
            "that every phase is arithmetically realized by a prime survivor, "
            "nor that the forced later factor by itself causes a hit."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
