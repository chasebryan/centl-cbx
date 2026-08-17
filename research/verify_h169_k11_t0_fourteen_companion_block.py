#!/usr/bin/env python3
"""Verify the exact fourteen-consecutive-companion normal form on h169, t11=0.

The canonical selected k11 child has

    t = 11u,
    R = 1+42u,
    C51 = 55R.

For j=0,...,13 and k=3+4j,

    C_k = (p+k)/4 = 55R + (j-12).

Hence

    (C3,C7,...,C55)
      = (55R-12,55R-11,...,55R,55R+1),

fourteen consecutive integers centered at the k51 shield carrier 55R.

The gcd corollary is immediate:

    gcd(R,C_k)=gcd(R,j-12).

Combined with R=1 mod 2,3,7, this recovers the exact support-isolation law:
only 11 at C7 and 5 at C11/C31 can overlap the residual R.
"""

from __future__ import annotations

import json
import math
from typing import Any

import verify_h169_k11_t0_k51_jacobi_normal_form as k51

J_VALUES = tuple(range(14))
SHIFTS = tuple(3 + 4 * j for j in J_VALUES)
EXPECTED_VECTOR = tuple(range(-12, 2))


def verify_symbolic_identity() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offsets = []

    # Check equality of affine coefficients, not a finite numeric sample.
    # p=169+840(11u)=169+9240u, so
    # C_k=(169+k)/4 +2310u.
    # 55R+(j-12)=55(1+42u)+(j-12)=43+j+2310u.
    for j in J_VALUES:
        k = 3 + 4 * j
        constant_direct = (169 + k) // 4
        constant_block = 55 + (j - 12)
        if constant_direct != constant_block:
            raise SystemExit(
                f"block constant failed at j={j}, k={k}: "
                f"{constant_direct}!={constant_block}"
            )
        offset = j - 12
        offsets.append(offset)
        rows.append(
            {
                "j": j,
                "k": k,
                "offset_from_C51": offset,
                "Ck_affine_u": f"{constant_direct}+2310u",
                "Ck_block_form": (
                    "55R" if offset == 0 else f"55R{offset:+d}"
                ),
            }
        )

    if tuple(offsets) != EXPECTED_VECTOR:
        raise SystemExit(f"companion offset vector changed: {offsets}")
    if [row["k"] for row in rows] != list(SHIFTS):
        raise SystemExit("companion shift ordering changed")
    return rows


def exact_overlap_from_block() -> dict[str, Any]:
    # R=1+42u is identically coprime to2,3,7.
    # For k!=51, gcd(R,Ck)=gcd(R,|offset|), and |offset|<=12.
    possible: dict[int, list[int]] = {}
    always_coprime: list[int] = []

    for j in J_VALUES:
        k = 3 + 4 * j
        offset = j - 12
        if offset == 0:
            continue
        d = abs(offset)
        candidates = []
        for q in (5, 11):
            if d % q == 0:
                candidates.append(q)
        if candidates:
            possible[k] = candidates
        else:
            always_coprime.append(k)

    expected_possible = {7: [11], 11: [5], 31: [5]}
    if possible != expected_possible:
        raise SystemExit(f"block overlap channels changed: {possible}")
    expected_coprime = [3, 15, 19, 23, 27, 35, 39, 43, 47, 55]
    if always_coprime != expected_coprime:
        raise SystemExit(f"block coprime list changed: {always_coprime}")

    # Freeze exact exceptional phases. These loops are complete modulo the only
    # candidate prime; the gcd bound itself comes from the symbolic block law.
    for u in range(11):
        R = 1 + 42 * u
        C7 = 55 * R - 11
        want = 11 if u == 6 else 1
        if math.gcd(R, C7) != want:
            raise SystemExit(f"C7 overlap phase changed at u={u}")
    for u in range(5):
        R = 1 + 42 * u
        for k, offset in ((11, -10), (31, -5)):
            C = 55 * R + offset
            want = 5 if u == 2 else 1
            if math.gcd(R, C) != want:
                raise SystemExit(f"C{k} overlap phase changed at u={u}")

    return {
        "gcd_law": "gcd(R,C_{3+4j})=gcd(R,j-12) for j!=12",
        "R_fixed_residues": {"mod2": 1, "mod3": 1, "mod7": 1},
        "always_coprime_shifts": always_coprime,
        "only_possible_shared_prime_support": {
            "C7": [11],
            "C11": [5],
            "C31": [5],
        },
        "exact_exception_phases": {
            "C7": "gcd(R,C7)=11 iff u mod11=6; otherwise1",
            "C11": "gcd(R,C11)=5 iff u mod5=2; otherwise1",
            "C31": "gcd(R,C31)=5 iff u mod5=2; otherwise1",
        },
    }


def verify() -> dict[str, Any]:
    canonical = k51.verify()
    phase = canonical["phase"]
    if phase["t_mod_11"] != 0 or phase["T_mod_11"] != 8:
        raise SystemExit("canonical selected h169 phase changed")
    if phase["forced_factor_occurrences"] != [5, 11]:
        raise SystemExit("canonical k51 hard-class seed changed")
    if phase["residual_name"] != "R=C51/55=1+42u":
        raise SystemExit(f"canonical residual coordinate changed: {phase['residual_name']}")

    rows = verify_symbolic_identity()
    overlap = exact_overlap_from_block()

    return {
        "verified": True,
        "mode": "h169-k11-t0-fourteen-companion-block",
        "canonical_parent": canonical["mode"],
        "parameterization": {
            "p": "169+9240u",
            "t": "11u",
            "R": "1+42u",
            "C51": "55R",
        },
        "indexing": "k_j=3+4j, 0<=j<=13",
        "block_identity": "C_{3+4j}=55R+(j-12)",
        "companion_vector": [
            "55R-12",
            "55R-11",
            "55R-10",
            "55R-9",
            "55R-8",
            "55R-7",
            "55R-6",
            "55R-5",
            "55R-4",
            "55R-3",
            "55R-2",
            "55R-1",
            "55R",
            "55R+1",
        ],
        "rows": rows,
        "support_overlap_corollary": overlap,
        "theorem": (
            "On the h169 inherited-k11 child t=0 mod11, writing t=11u and "
            "R=1+42u, the Lane-I companions k=3,7,...,55 are exactly the fourteen "
            "consecutive integers 55R-12 through55R+1.  Consequently "
            "gcd(R,C_{3+4j})=gcd(R,j-12), and the only possible residual support "
            "shared with another companion is 11 at C7 and 5 at C11/C31."
        ),
        "claim_boundary": (
            "Exact affine/consecutive-block theorem on one inherited h169 k11 phase. "
            "It does not force a factor outside H51 and does not prove termination; "
            "it supplies the simultaneous arithmetic object on which the next "
            "character contradiction should be sought."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
