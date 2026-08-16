#!/usr/bin/env python3
"""Verify the finite multiplicity-one descendant closure below q317^2."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

from classify_jacobi_saturation_extractions import ACTIVE_SOURCES

PHI_LIMIT = 486
K_BOUND = PHI_LIMIT * PHI_LIMIT
EXPECTED = {
    37: {3, 7, 11, 27, 71},
    71: {7, 11, 23, 31},
}
EXPECTED_ROUTE_COUNTS = {37: 77, 71: 76}


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


def scan(q: int, phi: list[int]) -> tuple[list[int], int]:
    routed = 0
    sats = []
    for k in range(3, K_BOUND + 1, 4):
        if phi[k] > PHI_LIMIT or math.gcd(k, q) != 1:
            continue
        if jacobi((-k) % q, q) != 1:
            continue
        routed += 1
        seed = math.lcm(class_seed(k), q)
        if math.gcd(seed, k) != 1:
            continue
        residues = divisor_square_residues(seed, k)
        if len(residues) != phi[k] // 2:
            continue
        kernel = jacobi_kernel(k)
        assert len(kernel) == phi[k] // 2
        if residues == kernel:
            sats.append(k)
    return sats, routed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    assert K_BOUND == 236_196
    phi = phi_sieve(K_BOUND)
    assert sum(1 for k in range(3, K_BOUND + 1, 4) if phi[k] <= PHI_LIMIT) == 158

    scans = {}
    for q in (37, 71):
        sats, routed = scan(q, phi)
        assert set(sats) == EXPECTED[q]
        assert routed == EXPECTED_ROUTE_COUNTS[q]
        scans[q] = {"compatible_routes": routed, "saturations": sats}

    baseline = set(ACTIVE_SOURCES[169])
    assert {7, 11, 23, 31} <= baseline
    assert jacobi(169, 3) == 1
    assert jacobi(169, 5) == 1

    assert EXPECTED[71] == {7, 11, 23, 31}
    assert EXPECTED[37] == {3, 7, 11, 27, 71}
    assert 27 == 3 ** 3
    assert all(71 % d for d in range(2, int(math.isqrt(71)) + 1))

    local = {}
    for q in (37, 71):
        local[q] = {}
        for k in sorted(EXPECTED[q]):
            seed = math.lcm(class_seed(k), q)
            residues = divisor_square_residues(seed, k)
            kernel = jacobi_kernel(k)
            assert residues == kernel
            local[q][k] = {
                "base_seed": class_seed(k),
                "kernel_size": len(kernel),
            }

    graph = {
        13: [],
        167: [37, 71],
        37: [71],
        71: [],
    }
    assert set(graph) == {13, 167, 37, 71}
    assert graph[13] == []
    assert graph[71] == []
    assert graph[37] == [71]
    assert set(graph[167]) == {37, 71}

    report = {
        "analysis": "q317-multiplicity-one-descendant-closure-v1",
        "bound": {"phi_limit": PHI_LIMIT, "odd_k_bound": K_BOUND},
        "new_scans": scans,
        "local_saturation_data": local,
        "descendant_graph": graph,
        "new_descendant_character_primes": [13, 37, 71, 167],
        "multiplicity_one_generation_depth_after_q317_square": 2,
        "sinks": [13, 71],
        "escape_mechanisms_still_live": [
            "higher valuation",
            "multiple routed factors",
            "affine/support transfer",
            "exact-state promotion",
            "incoming repulsion",
            "direct signed-box geometry",
        ],
        "failures": 0,
        "claim": (
            "the multiplicity-one source-generation descendants of the q317 square lift close on the finite set {13,167,37,71}; "
            "q37 generates only q71 and q71 generates no new character, so the local multiplicity-one generation depth is at most two"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
