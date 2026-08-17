#!/usr/bin/env python3
"""Verify the exact pairwise-coprime theorem for the reduced q23 predecessor core.

For T>=1 define

    A = 6T-5,
    B = 3T-2,
    C = 2T-1,
    D = 3T-1,
    E = 6T-1.

These are the non-forced-factor cores of C3,C7,C11,C15,C19 on the q23
Type-I-only parameterization.  The theorem is that A,B,C,D,E are pairwise
coprime for every integer T.

The proof object stored here is symbolic: for each pair it records a linear
combination cancelling T.  Any common divisor must divide the resulting small
constant.  Constants +/-1 finish immediately; constants +/-2 are killed by
oddness; constants +/-3 are killed by a fixed 1 mod3 residue; +/-4 is killed
by oddness.

The finite numerical sweep is only a regression check for the formulas, not
the proof.
"""

from __future__ import annotations

import json
import math
from typing import Any

FORMS = {
    "A=6T-5": (6, -5),
    "B=3T-2": (3, -2),
    "C=2T-1": (2, -1),
    "D=3T-1": (3, -1),
    "E=6T-1": (6, -1),
}


def value(coeff: tuple[int, int], T: int) -> int:
    a, b = coeff
    return a * T + b


def cancellation(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int, int]:
    a, b = left
    c, d = right
    g = math.gcd(a, c)
    u = c // g
    v = -(a // g)
    if u * a + v * c != 0:
        raise RuntimeError("failed to cancel T")
    constant = u * b + v * d
    return u, v, constant


def exclusion_reason(name1: str, name2: str, constant: int) -> str:
    n = abs(constant)
    if n == 1:
        return "common divisor divides 1"
    if n in {2, 4}:
        # Every pair with cancellation constant 2/4 consists entirely of odd
        # forms: A,C,E are always odd.
        odd = {"A=6T-5", "C=2T-1", "E=6T-1"}
        if name1 not in odd or name2 not in odd:
            raise SystemExit(f"unexpected even-sensitive pair {name1}, {name2}")
        return f"common divisor divides {n}, but both forms are odd"
    if n == 3:
        if {name1, name2} == {"A=6T-5", "D=3T-1"}:
            return "common divisor divides 3, but A=1 mod 3"
        if {name1, name2} == {"B=3T-2", "E=6T-1"}:
            return "common divisor divides 3, but B=1 mod 3"
        raise SystemExit(f"unexpected mod-3 pair {name1}, {name2}")
    raise SystemExit(f"unhandled cancellation constant {constant}")


def verify() -> dict[str, Any]:
    names = list(FORMS)
    pairs: list[dict[str, Any]] = []

    for i, name1 in enumerate(names):
        for name2 in names[i + 1 :]:
            left = FORMS[name1]
            right = FORMS[name2]
            u, v, constant = cancellation(left, right)
            reason = exclusion_reason(name1, name2, constant)

            # Regression-sweep the symbolic identity and coprimality over a
            # substantial initial interval.  This does not substitute for the
            # cancellation proof above.
            for T in range(1, 20_001):
                x = value(left, T)
                y = value(right, T)
                if u * x + v * y != constant:
                    raise SystemExit(
                        f"{name1}, {name2}, T={T}: cancellation identity failed"
                    )
                if math.gcd(x, y) != 1:
                    raise SystemExit(
                        f"{name1}, {name2}, T={T}: gcd={math.gcd(x,y)}"
                    )

            pairs.append(
                {
                    "left": name1,
                    "right": name2,
                    "combination": f"{u}*left + ({v})*right = {constant}",
                    "constant": constant,
                    "exclusion": reason,
                    "gcd": 1,
                }
            )

    if len(pairs) != 10:
        raise SystemExit(f"expected 10 unordered pairs, got {len(pairs)}")

    return {
        "verified": True,
        "mode": "k23-predecessor-pairwise-coprime",
        "forms": list(FORMS),
        "pair_count": len(pairs),
        "pairs": pairs,
        "theorem": (
            "For every integer T, the five reduced predecessor forms "
            "6T-5, 3T-2, 2T-1, 3T-1, 6T-1 are pairwise coprime."
        ),
        "consequence": (
            "The five local obstruction grammars use disjoint prime supports. "
            "Any cross-coordinate proof must couple additive/residue/character "
            "information rather than rely on a shared prime divisor."
        ),
        "claim_boundary": (
            "Elementary gcd theorem for the predecessor core only; it does not "
            "make the five obstruction conditions incompatible or prove ES."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
