#!/usr/bin/env python3
"""Verify the valuation<=2 one-source character fixed point below q317^2."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

A2 = (13, 19, 37, 47, 71, 167)
EXPECTED = {
    13: {
        1: (69, {3, 23, 55}),
        2: (120, {3, 23, 27, 35, 55}),
    },
    19: {
        1: (76, {3, 15, 27, 31}),
        2: (122, {3, 15, 27, 31, 71, 167}),
    },
    37: {
        1: (77, {3, 7, 11, 27, 71}),
        2: (130, {3, 7, 11, 27, 47, 71}),
    },
    47: {
        1: (79, {11, 15, 31}),
        2: (124, {11, 15, 31, 39}),
    },
    71: {
        1: (76, {7, 11, 23, 31}),
        2: (125, {7, 11, 23, 31, 39, 55}),
    },
    167: {
        1: (79, {15, 23, 71, 111}),
        2: (137, {15, 23, 35, 39, 71, 95, 111}),
    },
}
GRAPH = {
    13: set(),
    19: {71, 167},
    37: {47, 71},
    47: {13},
    71: {13},
    167: {13, 19, 37, 71},
}


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


def phi_sieve(n: int) -> list[int]:
    phi = list(range(n + 1))
    for p in range(2, n + 1):
        if phi[p] == p:
            for m in range(p, n + 1, p):
                phi[m] -= phi[m] // p
    return phi


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


def closure(q: int, e: int, phi: list[int]) -> tuple[int, set[int]]:
    phi_limit = 162 * (2 * e + 1)
    k_bound = phi_limit * phi_limit
    routed = 0
    sats: set[int] = set()
    for k in range(3, k_bound + 1, 4):
        if phi[k] > phi_limit or math.gcd(k, q) != 1:
            continue
        if jacobi((-k) % q, q) != 1:
            continue
        routed += 1
        fac = factorization(class_seed(k))
        fac[q] = max(fac.get(q, 0), e)
        seed = 1
        for p, a in fac.items():
            seed *= p ** a
        if math.gcd(seed, k) != 1:
            continue
        residues = divisor_square_residues(seed, k)
        if len(residues) != phi[k] // 2:
            continue
        kernel = jacobi_kernel(k)
        if residues == kernel:
            sats.add(k)
    return routed, sats


def extracted_new_primes(q: int, sats: set[int]) -> set[int]:
    # Baseline h169 characters known independently of A2.
    baseline = {3, 5, 7, 11, 23, 31}
    outputs = set()
    for k in sats:
        for r, exponent in factorization(k).items():
            if exponent % 2 == 0:
                continue
            if r not in baseline:
                outputs.add(r)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # One sieve covers the e=2 ceiling.
    max_phi = 162 * 5
    max_k = max_phi * max_phi
    assert max_k == 656_100
    phi = phi_sieve(max_k)

    rows = {}
    derived_graph = {}
    for q in A2:
        rows[q] = {}
        union_outputs = set()
        for e in (1, 2):
            routed, sats = closure(q, e, phi)
            exp_routed, exp_sats = EXPECTED[q][e]
            assert routed == exp_routed
            assert sats == exp_sats
            outputs = extracted_new_primes(q, sats)
            union_outputs |= outputs
            rows[q][e] = {
                "compatible_routes": routed,
                "saturations": sorted(sats),
                "nonbaseline_outputs": sorted(outputs),
            }
        # Source-self output does not add a new character; retain graph edges only to A2.
        derived_graph[q] = {r for r in union_outputs if r in A2 and r != q}
        assert derived_graph[q] == GRAPH[q], (q, derived_graph[q], GRAPH[q])

    alphabet = set(A2)
    for q, outputs in derived_graph.items():
        assert outputs <= alphabet

    # Pin the only nontrivial SCC: 19 <-> 167.
    assert 167 in derived_graph[19]
    assert 19 in derived_graph[167]
    assert 19 not in derived_graph[19]
    assert 167 not in derived_graph[167]

    # Every route outside the SCC flows toward q13 or through q37/q71 to q13.
    assert derived_graph[13] == set()
    assert derived_graph[47] == {13}
    assert derived_graph[71] == {13}
    assert derived_graph[37] == {47, 71}

    report = {
        "analysis": "q317-valuation2-source-automaton-v1",
        "alphabet": list(A2),
        "closures": rows,
        "source_graph": {str(q): sorted(v) for q, v in derived_graph.items()},
        "strongly_connected_components": [[19, 167], [13], [37], [47], [71]],
        "nontrivial_scc": [19, 167],
        "valuation2_character_fixed_point": True,
        "next_known_escape": {
            "source": 71,
            "valuation": 3,
            "destination": 51,
            "output": 17,
            "status": "preliminary target for next theorem",
        },
        "failures": 0,
        "claim": (
            "for sources {13,19,37,47,71,167}, complete one-source Jacobi-saturation closures at valuations 1 and 2 "
            "produce no prime character outside that finite alphabet; the only nontrivial character SCC is {19,167}"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
