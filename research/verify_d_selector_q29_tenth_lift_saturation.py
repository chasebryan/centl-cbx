#!/usr/bin/env python3
"""Verify q29 tenth-lift Jacobi saturation at k951 and q317 extraction."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

Q = 29
ORIGIN = 23
N_ROUTE = 8
K = 951
BASE = 70
TARGET_EXP = 10
P0 = 3_297_685_609
PSTEP = 4_306_833_720
EXPECTED_S0 = 250_148_936_915_814
EXPECTED_SMOD = 420_707_233_300_201
EXPECTED_P_CLASS = 1_077_349_876_531_183_834_133_689
EXPECTED_P_MOD = 1_811_916_098_625_212_549_577_720
EXPECTED_SIZES = [77, 127, 159, 189, 217, 243, 269, 286, 302, 316]


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


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


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


def vp(n: int, q: int) -> int:
    e = 0
    while n % q == 0:
        e += 1
        n //= q
    return e


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # Source characters and persistent route.
    assert jacobi(Q, 23) == 1
    assert jacobi(Q, 17) == -1
    assert K == ORIGIN + 4 * Q * N_ROUTE
    assert factorization(K) == Counter({3: 1, 317: 1})
    assert is_prime(317)
    assert jacobi(Q, K) == 1
    assert math.gcd(210, (169 + K) // 4) == BASE

    kernel = jacobi_kernel(K)
    assert len(kernel) == 316

    sizes = []
    saturated = []
    for e in range(1, TARGET_EXP + 1):
        seed = BASE * Q**e
        residues = divisor_square_residues(seed, K)
        sizes.append(len(residues))
        saturated.append(residues == kernel)
        assert residues <= kernel

    assert sizes == EXPECTED_SIZES
    assert saturated == [False] * 9 + [True]
    assert divisor_square_residues(BASE * Q**10, K) == kernel

    # Compatibility with Route-B D-selector ancestry.
    lift_mod = 4 * Q**TARGET_EXP
    target = (-K) % lift_mod
    g = math.gcd(PSTEP, lift_mod)
    assert g == 4
    assert (target - P0) % g == 0

    reduced_step = PSTEP // g
    reduced_mod = lift_mod // g
    rhs = (target - P0) // g
    s0 = (rhs * pow(reduced_step, -1, reduced_mod)) % reduced_mod
    assert s0 == EXPECTED_S0
    assert reduced_mod == EXPECTED_SMOD

    p_class = P0 + PSTEP * s0
    combined_mod = PSTEP * reduced_mod
    assert p_class == EXPECTED_P_CLASS
    assert combined_mod == EXPECTED_P_MOD
    assert math.gcd(p_class, combined_mod) == 1
    assert p_class % 840 == 169
    assert p_class % lift_mod == target
    assert p_class % 12 == 1

    # Reconstruct the Route-B D-selector parameterization exactly.
    u = 3631 + 4743 * s0
    t = 705 + 1081 * u
    p_reconstructed = 169 + 840 * t
    assert p_reconstructed == p_class

    C23 = (p_class + 23) // 4
    C951 = (p_class + 951) // 4
    assert vp(C23, Q) == 1
    assert vp(C951, Q) == 10
    assert C951 - C23 == 8 * Q

    # Saturated miss extraction: 951=3*317 and h169 fixes (3/p)=+1
    # for prime p because p=1 mod12. Thus Jacobi(951/p)=+1 implies
    # (317/p)=+1. Pin the hard-class sign and factorization used.
    assert p_class % 3 == 1
    assert factorization(951) == Counter({3: 1, 317: 1})

    report = {
        "analysis": "d-selector-q29-tenth-lift-saturation-v1",
        "source": {
            "q": Q,
            "origin": ORIGIN,
            "characters": {"mod23": 1, "mod17": -1},
            "route_index": N_ROUTE,
            "destination": K,
            "destination_factorization": {"3": 1, "317": 1},
        },
        "saturation": {
            "base_seed": BASE,
            "kernel_size": len(kernel),
            "residue_sizes_e1_through_e10": sizes,
            "first_saturating_exponent": 10,
            "saturating_seed": BASE * Q**10,
        },
        "route_b_compatibility": {
            "s_phase": f"{s0} mod {reduced_mod}",
            "p_phase": f"{p_class} mod {combined_mod}",
            "primitive": math.gcd(p_class, combined_mod) == 1,
            "origin_v29": vp(C23, Q),
            "destination_v29": vp(C951, Q),
        },
        "progress_dichotomy": {
            "hit": "Jacobi-negative factor of C951 yields exact signed-box hit under saturation",
            "miss": "Jacobi(951/p)=+1; h169 fixes (3/p)=+1; therefore (317/p)=+1",
        },
        "failures": 0,
        "claim": (
            "conditional on a Route-B D-selector q29 B witness and the exact tenth-power lift at k951, "
            "70*29^10 Jacobi-saturates modulo951 for the first time at exponent10, so k951 either hits "
            "or a miss extracts the new positive target-prime character (317/p)=+1"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
