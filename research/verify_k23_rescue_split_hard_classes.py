#!/usr/bin/env python3
"""Verify the CRT skeleton showing both k23 rescue multiplicity splits survive every hard class.

Within the exact q=23 Type-I-only normal form, the nonresidue part R has two
prime valuations in one class rho in {5,14}.  Those two valuations can occur as
one square r^2 or as two distinct primes r*s.

This verifier checks a clean CRT/Dirichlet construction modulo

    lcm(23,35) = 805.

Choose rescue primes r (and s) with

    r == rho (mod 23),
    r == 1   (mod 35),

and choose a 23-split multiplier prime m with

    m == 1 (mod 23),
    m == h (mod 35),

for each hard T=(p+23)/24 class h in {1,6,8,13,16,23}.  Every resulting CRT
class is coprime to 805, so Dirichlet's theorem applies to each progression.
Consequently both the square and distinct-semiprime local rescue splits are
compatible with every Mordell-hard residue class.

This is a local congruence result.  It does not assert that p=24*m*R-23 is
prime for infinitely many choices, nor that any such p survives earlier Lane-I
shifts.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

KERNEL = Path(__file__).resolve().parents[1] / "kernel"
sys.path.insert(0, str(KERNEL))

import analyze_brec_cylinder as cylinder  # noqa: E402

MOD23 = 23
MOD35 = 35
MOD805 = MOD23 * MOD35
HARD_TO_T35 = {1: 1, 121: 6, 169: 8, 289: 13, 361: 16, 529: 23}
T35_TO_HARD = {v: k for k, v in HARD_TO_T35.items()}


def crt_pair(a: int, m: int, b: int, n: int) -> int:
    if math.gcd(m, n) != 1:
        raise ValueError("crt_pair requires coprime moduli")
    for x in range(a % m, m * n, m):
        if x % n == b % n:
            return x
    raise RuntimeError("CRT solution not found")


def first_prime_in_class(residue: int, modulus: int) -> int:
    n = residue % modulus
    if n < 2:
        n += modulus
    for _ in range(1_000_000):
        if cylinder.is_prime64(n):
            return n
        n += modulus
    raise SystemExit(f"no finite prime representative found for {residue} mod {modulus}")


def verify() -> dict[str, Any]:
    rescue_classes: dict[int, int] = {}
    rescue_primes: dict[int, int] = {}
    for rho in (5, 14):
        cls = crt_pair(rho, 23, 1, 35)
        if cls % 23 != rho or cls % 35 != 1:
            raise SystemExit(f"rho={rho}: rescue CRT mismatch")
        if math.gcd(cls, MOD805) != 1:
            raise SystemExit(f"rho={rho}: rescue CRT class is not a unit mod 805")
        prime = first_prime_in_class(cls, MOD805)
        if prime % 23 != rho or prime % 35 != 1:
            raise SystemExit(f"rho={rho}: finite prime representative mismatch")
        rescue_classes[rho] = cls
        rescue_primes[rho] = prime

    multiplier_rows: list[dict[str, int]] = []
    multiplier_prime_by_h: dict[int, int] = {}
    for hard_residue, h in HARD_TO_T35.items():
        cls = crt_pair(1, 23, h, 35)
        if cls % 23 != 1 or cls % 35 != h:
            raise SystemExit(f"h={h}: multiplier CRT mismatch")
        if math.gcd(cls, MOD805) != 1:
            raise SystemExit(f"h={h}: multiplier CRT class is not a unit mod 805")
        prime = first_prime_in_class(cls, MOD805)
        if prime % 23 != 1 or prime % 35 != h:
            raise SystemExit(f"h={h}: multiplier prime representative mismatch")
        multiplier_prime_by_h[h] = prime
        multiplier_rows.append(
            {
                "hard_p_mod_840": hard_residue,
                "T_mod_35": h,
                "m_crt_mod_805": cls,
                "finite_prime_m": prime,
            }
        )

    constructions: list[dict[str, Any]] = []
    for rho in (5, 14):
        r = rescue_primes[rho]
        # Find a second distinct prime in the same rescue progression.
        s = r + MOD805
        while not cylinder.is_prime64(s):
            s += MOD805
        if s == r or s % 23 != rho or s % 35 != 1:
            raise SystemExit(f"rho={rho}: distinct rescue-prime representative failed")

        for hard_residue, h in HARD_TO_T35.items():
            m = multiplier_prime_by_h[h]
            for split, R in (("square", r * r), ("distinct-semiprime", r * s)):
                T = m * R
                C = 6 * T
                p_candidate = 24 * T - 23

                if T % 35 != h:
                    raise SystemExit(f"rho={rho}, h={h}, split={split}: T mod35 mismatch")
                if p_candidate % 840 != hard_residue:
                    raise SystemExit(
                        f"rho={rho}, h={h}, split={split}: hard p residue mismatch"
                    )
                if m % 23 != 1:
                    raise SystemExit("multiplier lost 23-split condition")
                expected_r23 = (rho * rho) % 23
                if R % 23 != expected_r23:
                    raise SystemExit("rescue product lost same-class valuation-two residue")

                p23 = p_candidate % 23
                type_i_target = (-pow(p23, -1, 23)) % 23
                expected_target = 11 if rho == 5 else 21
                if type_i_target != expected_target:
                    raise SystemExit(
                        f"rho={rho}: Type-I target {type_i_target} != {expected_target}"
                    )

                constructions.append(
                    {
                        "rho": rho,
                        "split": split,
                        "hard_p_mod_840": hard_residue,
                        "T_mod_35": h,
                        "r": r,
                        "s": r if split == "square" else s,
                        "m": m,
                        "C_mod_23": C % 23,
                        "p_candidate_mod_23": p23,
                        "type_I_target": type_i_target,
                        "p_candidate_mod_840": p_candidate % 840,
                    }
                )

    expected_count = 2 * 2 * len(HARD_TO_T35)
    if len(constructions) != expected_count:
        raise SystemExit(f"construction count {len(constructions)} != {expected_count}")

    seen = {
        (row["rho"], row["split"], row["hard_p_mod_840"])
        for row in constructions
    }
    expected = {
        (rho, split, hard)
        for rho in (5, 14)
        for split in ("square", "distinct-semiprime")
        for hard in HARD_TO_T35
    }
    if seen != expected:
        raise SystemExit("not every rescue/split/hard-class combination was realized")

    return {
        "verified": True,
        "mode": "k23-rescue-split-hard-class-compatibility",
        "modulus": MOD805,
        "rescue_crt_classes": [
            {
                "rho": rho,
                "class_mod_805": rescue_classes[rho],
                "finite_prime_representative": rescue_primes[rho],
            }
            for rho in (5, 14)
        ],
        "multiplier_classes": multiplier_rows,
        "combinations_verified": len(constructions),
        "constructions": constructions,
        "dirichlet_hypotheses": "all displayed progression classes are coprime to 805",
        "conclusion": (
            "Both square and distinct-semiprime q23 Type-I-only rescue splits are "
            "locally compatible with every Mordell-hard residue class."
        ),
        "claim_boundary": (
            "CRT plus Dirichlet compatibility only.  No assertion that p=24*m*R-23 "
            "is prime infinitely often or survives the earlier BREC corridor."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
