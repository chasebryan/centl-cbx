#!/usr/bin/env python3
"""Verify the first four Lane-I misses as one p-relative consecutive block.

For Mordell-hard classes h in {169,289,529}, the landed exact normal forms are:

  k=3  miss iff every q|C3 has Jacobi(q/3)=+1;
  k=7  miss iff every q|C7 has Legendre(q/7)=+1;
  k=11 miss iff every q|C11 has Legendre(q/11)=+1;
  k=15 miss iff every q|C15 has Jacobi(q/15)=+1.

The generic Lane-I prime-relative reciprocity theorem turns each local +1
condition into Legendre(q/p)=+1. Since C7=C3+1, C11=C3+2, C15=C3+3, the four
misses are equivalent to four consecutive integers all having exclusively
p-quadratic-residue prime support.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from typing import Any

import verify_lane_i_prime_relative_reciprocity as bridge

HARD_CLASSES = {169, 289, 529}
SHIFTS = (3, 7, 11, 15)
H3 = {1}
H7 = {1, 2, 4}
H11 = {1, 3, 4, 5, 9}
H15 = {1, 2, 4, 8}
LOCAL_PLUS = {3: H3, 7: H7, 11: H11, 15: H15}


def is_prime(n: int) -> bool:
    return bridge.is_prime(n)


def factorint(n: int) -> dict[int, int]:
    return bridge.factorint(n)


def local_character_plus(q: int, k: int) -> bool:
    if math.gcd(q, k) != 1:
        return False
    return q % k in LOCAL_PLUS[k]


def local_miss(p: int, k: int) -> bool:
    C = (p + k) // 4
    if 4 * C != p + k:
        raise ValueError("Lane-I cofactor is not integral")
    return all(local_character_plus(q, k) for q in factorint(C))


def all_prime_support_qr_mod_p(p: int, C: int) -> bool:
    return all(bridge.legendre(q, p) == 1 for q in factorint(C))


def verify_local_plus_sets() -> dict[str, Any]:
    # Freeze that the four landed support monoids are exactly Jacobi +1.
    expected = {}
    for k in SHIFTS:
        units = {r for r in range(1, k) if math.gcd(r, k) == 1}
        plus = {r for r in units if bridge.jacobi(r, k) == 1}
        if plus != LOCAL_PLUS[k]:
            raise SystemExit(
                f"k={k}: landed local + support {sorted(LOCAL_PLUS[k])} "
                f"!= Jacobi + set {sorted(plus)}"
            )
        expected[str(k)] = {
            "unit_group": sorted(units),
            "Jacobi_plus_support": sorted(plus),
        }
    return expected


def verify_symbolic_block() -> dict[str, Any]:
    # C_{k+4}=C_k+1 is an integer identity. Freeze it algebraically by the
    # numerator difference, not by finite prime samples.
    rows = []
    for j, k in enumerate(SHIFTS):
        if k != 3 + 4 * j:
            raise SystemExit("first-four shift indexing changed")
        rows.append(
            {
                "j": j,
                "k": k,
                "C_k": f"X+{j}" if j else "X",
            }
        )
    return {
        "X": "C3=(p+3)/4",
        "identity": "C_{3+4j}=X+j for j=0,1,2,3",
        "vector": ["X", "X+1", "X+2", "X+3"],
        "rows": rows,
    }


def verify_one_prime(p: int) -> dict[str, Any]:
    if not is_prime(p) or p % 840 not in HARD_CLASSES:
        raise ValueError("p must be prime in hard class 169,289,529")
    if p % 4 != 1:
        raise SystemExit("hard prime is not 1 mod4")

    X = (p + 3) // 4
    cofactors = [X + j for j in range(4)]
    direct = [(p + k) // 4 for k in SHIFTS]
    if direct != cofactors:
        raise SystemExit(f"consecutive cofactor identity failed at p={p}")

    misses = [local_miss(p, k) for k in SHIFTS]
    qr_support = [all_prime_support_qr_mod_p(p, C) for C in cofactors]

    # Coordinate-by-coordinate equivalence via the generic reciprocity bridge.
    for k, C, miss, qr in zip(SHIFTS, cofactors, misses, qr_support):
        for q in factorint(C):
            if math.gcd(q, k) != 1:
                raise SystemExit(
                    f"unexpected q|k on theorem domain: p={p}, k={k}, q={q}"
                )
            values = bridge.bridge_value(p, k, q)
            local_plus = local_character_plus(q, k)
            global_plus = values["q_over_p"] == 1
            if local_plus != global_plus:
                raise SystemExit(
                    f"local/global character disagreement p={p}, k={k}, q={q}"
                )
        if miss != qr:
            raise SystemExit(
                f"coordinate equivalence failed p={p}, k={k}: miss={miss}, qr={qr}"
            )

    simultaneous_miss = all(misses)
    product_all_qr = all(qr_support)
    if simultaneous_miss != product_all_qr:
        raise SystemExit(f"four-coordinate equivalence failed at p={p}")

    return {
        "p": p,
        "p_mod_840": p % 840,
        "X": X,
        "cofactors": cofactors,
        "misses": misses,
        "all_prime_support_QR_mod_p": qr_support,
        "simultaneous_first_four_miss": simultaneous_miss,
    }


def finite_regression() -> dict[str, Any]:
    counts: Counter[str] = Counter()
    examples_miss: list[dict[str, Any]] = []
    examples_constructive: list[dict[str, Any]] = []

    # Scan all primes in the three exact hard classes through 5M.
    for h in sorted(HARD_CLASSES):
        p = h
        while p <= 5_000_000:
            if is_prime(p):
                row = verify_one_prime(p)
                counts[f"hard_{h}_primes"] += 1
                counts["primes_checked"] += 1
                if row["simultaneous_first_four_miss"]:
                    counts["simultaneous_miss"] += 1
                    if len(examples_miss) < 12:
                        examples_miss.append(row)
                else:
                    counts["not_simultaneous_miss"] += 1
                    if len(examples_constructive) < 12:
                        examples_constructive.append(row)
            p += 840

    if counts["primes_checked"] < 1_000:
        raise SystemExit(f"finite regression unexpectedly small: {counts}")
    if counts["simultaneous_miss"] == 0 or counts["not_simultaneous_miss"] == 0:
        raise SystemExit("finite regression failed to exercise both theorem sides")
    return {
        "p_hi": 5_000_000,
        "counts": dict(sorted(counts.items())),
        "simultaneous_miss_examples": examples_miss,
        "other_examples": examples_constructive,
    }


def verify() -> dict[str, Any]:
    bridge_obj = bridge.verify()
    if bridge_obj["identity"] != "Legendre(q/p)=Jacobi(q/k)":
        raise SystemExit("generic reciprocity bridge changed")
    supports = verify_local_plus_sets()
    block = verify_symbolic_block()
    regression = finite_regression()

    return {
        "verified": True,
        "mode": "four-consecutive-prime-qr-block",
        "hard_classes_mod_840": sorted(HARD_CLASSES),
        "shifts": list(SHIFTS),
        "local_Jacobi_plus_support": supports,
        "consecutive_block": block,
        "equivalence": (
            "sigma3=sigma7=sigma11=sigma15=- iff every prime divisor of "
            "X(X+1)(X+2)(X+3) is a quadratic residue modulo p"
        ),
        "theorem": (
            "Let p be prime with p mod840 in {169,289,529}, and X=(p+3)/4. "
            "Then the first four Lane-I coordinates k=3,7,11,15 are all combined "
            "misses if and only if every prime divisor of the four consecutive "
            "integers X,X+1,X+2,X+3 is a quadratic residue modulo p."
        ),
        "finite_regression": regression,
        "claim_boundary": (
            "Exact synthesis of landed first-four local normal forms with the "
            "Lane-I reciprocity bridge. It does not say such four-term blocks are "
            "impossible and therefore does not prove termination or Erdős-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
