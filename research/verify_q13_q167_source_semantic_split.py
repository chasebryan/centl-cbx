#!/usr/bin/env python3
"""Verify the multiplicity-one semantic split between q13 and q167."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

from classify_jacobi_saturation_extractions import ACTIVE_SOURCES

PHI_LIMIT = 486
K_BOUND = PHI_LIMIT * PHI_LIMIT
S39 = frozenset({1, 2, 5, 6, 7, 8, 9, 10, 11})
EXPECTED = {
    13: {3, 23, 55},
    167: {15, 23, 71, 111},
}
EXPECTED_ROUTE_COUNTS = {13: 69, 167: 79}
PARENTS = {
    13: (
        120_944_665_017_010_843_655_597_365_969,
        182_077_636_834_748_983_894_515_505_080,
    ),
    167: (
        47_177_936_809_781_190_337_189_229_329,
        182_077_636_834_748_983_894_515_505_080,
    ),
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


def crt_pair(a: int, m: int, b: int, n: int) -> tuple[int, int]:
    g = math.gcd(m, n)
    assert (b - a) % g == 0
    mm = m // g
    nn = n // g
    x = ((b - a) // g) * pow(mm, -1, nn) % nn
    modulus = m * nn
    return (a + m * x) % modulus, modulus


def scan_source(q: int, phi: list[int]) -> tuple[list[int], int]:
    routed = 0
    sats = []
    for k in range(3, K_BOUND + 1, 4):
        if phi[k] > PHI_LIMIT or math.gcd(k, q) != 1:
            continue
        if jacobi((-k) % q, q) != 1:
            continue
        routed += 1
        base = class_seed(k)
        seed = math.lcm(base, q)
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

    phi = phi_sieve(K_BOUND)
    assert sum(1 for k in range(3, K_BOUND + 1, 4) if phi[k] <= PHI_LIMIT) == 158

    scans = {}
    for q in (13, 167):
        sats, routed = scan_source(q, phi)
        assert set(sats) == EXPECTED[q]
        assert routed == EXPECTED_ROUTE_COUNTS[q]
        scans[q] = {"routed": routed, "saturations": sats}

    # q13 is multiplicity-one character-idempotent relative to h169.
    h169_sources = set(ACTIVE_SOURCES[169])
    assert {7, 11, 23, 31} <= h169_sources
    assert EXPECTED[13] == {3, 23, 55}
    assert 55 == 5 * 11
    assert jacobi(169, 3) == 1
    assert jacobi(169, 5) == 1

    # The q13 positive character itself contracts the landed k39 phase set 9->6.
    assert 169 % 13 == 0
    assert 840 % 13 == 8
    assert jacobi(8, 13) == -1
    q13_positive_phases = {
        t for t in S39
        if jacobi((8 * t) % 13, 13) == 1
    }
    assert q13_positive_phases == {2, 5, 6, 7, 8, 11}

    # q167 has two source-generating multiplicity-one saturated destinations.
    assert EXPECTED[167] == {15, 23, 71, 111}
    assert all(71 % d for d in range(2, int(math.isqrt(71)) + 1))
    assert 111 == 3 * 37
    assert jacobi(169, 3) == 1

    # Exact parent-route compatibility for every classified child saturation.
    compatible_children = {}
    for q in (13, 167):
        parent_p, parent_mod = PARENTS[q]
        rows = []
        for k in sorted(EXPECTED[q]):
            child_mod = 4 * q
            p0, modulus = crt_pair(parent_p, parent_mod, (-k) % child_mod, child_mod)
            assert p0 % parent_mod == parent_p % parent_mod
            assert (p0 + k) % child_mod == 0
            assert jacobi(p0 % q, q) == 1
            rows.append({"k": k, "p_class": p0, "modulus": modulus})
        compatible_children[q] = rows

    # Pin exact kernel equality at each saturated destination.
    local = {}
    for q in (13, 167):
        local[q] = {}
        for k in sorted(EXPECTED[q]):
            base = class_seed(k)
            residues = divisor_square_residues(math.lcm(base, q), k)
            kernel = jacobi_kernel(k)
            assert residues == kernel
            local[q][k] = {
                "base_seed": base,
                "kernel_size": len(kernel),
            }

    report = {
        "analysis": "q13-q167-source-semantic-split-v1",
        "bound": {"phi_limit": PHI_LIMIT, "odd_k_bound": K_BOUND},
        "scans": scans,
        "q13": {
            "semantic_class": ["PHASE_CONTRACTING", "MULTIPLICITY_ONE_IDEMPOTENT"],
            "k39_phase_contraction": {
                "before": sorted(S39),
                "after": sorted(q13_positive_phases),
                "count": "9->6",
            },
            "multiplicity_one_miss_outputs": {
                3: "known q3 character",
                23: "known q23 character",
                55: "known q5*q11 character product",
            },
        },
        "q167": {
            "semantic_class": ["MULTIPLICITY_ONE_SOURCE_GENERATING"],
            "idempotent_destinations": [15, 23],
            "source_generating_destinations": {
                71: "HIT_OR_EXTRACT_71_POSITIVE",
                111: "HIT_OR_EXTRACT_37_POSITIVE",
            },
        },
        "local_saturation_data": local,
        "parent_phase_compatibility": compatible_children,
        "failures": 0,
        "claim": (
            "the q317 square-lift outputs split semantically: q13 contracts the h169 tau13 phase state but is multiplicity-one character-idempotent, "
            "whereas q167 is multiplicity-one source-generating through saturated destinations k71 and k111"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
