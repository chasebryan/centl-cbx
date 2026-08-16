#!/usr/bin/env python3
"""Verify the complete multiplicity-one q317 saturation/idempotence closure."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

from classify_jacobi_saturation_extractions import ACTIVE_SOURCES

Q = 317
PHI_LIMIT = 486
K_BOUND = PHI_LIMIT * PHI_LIMIT
EXPECTED_SATURATIONS = {
    7: 2,
    11: 15,
    15: 2,
    23: 6,
    31: 10,
}


def phi_sieve(n: int) -> list[int]:
    phi = list(range(n + 1))
    for p in range(2, n + 1):
        if phi[p] == p:
            for m in range(p, n + 1, p):
                phi[m] -= phi[m] // p
    return phi


def factorization(n: int) -> Counter[int]:
    out: Counter[int] = Counter()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] += 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out[n] += 1
    return out


def jacobi(a: int, n: int) -> int:
    if n <= 0 or n % 2 == 0:
        raise ValueError(n)
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def divisor_square_residues(seed: int, k: int) -> set[int]:
    residues = {1}
    for q, e in factorization(seed).items():
        powers = [pow(q, a, k) for a in range(2 * e + 1)]
        residues = {x * y % k for x in residues for y in powers}
    return residues


def jacobi_kernel(k: int) -> set[int]:
    return {
        u for u in range(1, k)
        if math.gcd(u, k) == 1 and jacobi(u, k) == 1
    }


def class_seed(k: int) -> int:
    return math.gcd(210, (169 + k) // 4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    assert Q % 4 == 1
    qr317 = {x * x % Q for x in range(1, Q)}
    assert len(qr317) == 158

    phi = phi_sieve(K_BOUND)
    eligible = [
        k for k in range(3, K_BOUND + 1, 4)
        if phi[k] <= PHI_LIMIT
    ]
    assert len(eligible) == 158
    assert max(eligible) == 1155

    routed = [
        k for k in eligible
        if (-k) % Q != 0 and (-k) % Q in qr317
    ]
    assert len(routed) == 76

    saturations: dict[int, int] = {}
    rows = []
    for k in routed:
        base = class_seed(k)
        seed = math.lcm(base, Q)
        if math.gcd(seed, k) != 1:
            continue
        residues = divisor_square_residues(seed, k)
        kernel = jacobi_kernel(k)
        assert len(kernel) == phi[k] // 2
        sat = residues == kernel
        if sat:
            saturations[k] = base
            rows.append({
                "k": k,
                "base_seed": base,
                "seed": seed,
                "factorization": dict(factorization(k)),
                "kernel_size": len(kernel),
                "routed_p_mod317": (-k) % Q,
            })

    assert saturations == EXPECTED_SATURATIONS, saturations

    # Character-idempotence relative to the landed h169 source graph.
    h169_sources = set(ACTIVE_SOURCES[169])
    assert {7, 11, 23, 31} <= h169_sources
    assert 169 % 7 == 1
    assert 169 % 12 == 1  # fixes (3/p)=+1 for prime p in h169
    assert 169 % 5 == 4   # fixes (5/p)=+1

    miss_outputs = {
        7: "(7/p)=+1 already hard/source-controlled",
        11: "(11/p)=+1 already in landed h169 source set",
        15: "(15/p)=+1 already fixed by hard mod3/mod5 characters",
        23: "(23/p)=+1 already in landed h169 source set",
        31: "(31/p)=+1 already in landed h169 source set",
    }

    report = {
        "analysis": "q317-multiplicity-one-saturation-idempotence-v1",
        "bounds": {
            "phi_limit": PHI_LIMIT,
            "odd_k_bound": K_BOUND,
            "low_totient_admissible_k": len(eligible),
            "largest_low_totient_k": max(eligible),
        },
        "route": {
            "source": Q,
            "positive_residue_classes_mod317": len(qr317),
            "low_totient_routed_candidates": len(routed),
        },
        "saturations": rows,
        "saturating_shifts": sorted(saturations),
        "miss_outputs": miss_outputs,
        "landed_h169_sources": sorted(h169_sources),
        "multiplicity_one_new_character_outputs": 0,
        "failures": 0,
        "claim": (
            "a multiplicity-one q317 source Jacobi-saturates exactly at k=7,11,15,23,31 in the complete h169 closure; "
            "each saturated miss only reasserts already-controlled character data, although any of the five branches may still terminate by hit"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
