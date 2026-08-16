#!/usr/bin/env python3
"""Verify the complete q317 exponent-two saturation breakout."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

Q = 317
E = 2
PHI_LIMIT = 810
K_BOUND = PHI_LIMIT * PHI_LIMIT
EXPECTED_E2 = {7, 11, 15, 23, 31, 39, 167}
EXPECTED_NEW = {39, 167}
PARENT_P = 1_077_349_876_531_183_834_133_689
PARENT_MOD = 1_811_916_098_625_212_549_577_720
EXPECTED_CRT = {
    39: 120_944_665_017_010_843_655_597_365_969,
    167: 47_177_936_809_781_190_337_189_229_329,
}
EXPECTED_CRT_MOD = 182_077_636_834_748_983_894_515_505_080


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


def valuation(n: int, q: int) -> int:
    e = 0
    while n % q == 0:
        e += 1
        n //= q
    return e


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # Exact cardinality bound for exponent2.
    max_divisor_residues = (3 ** 4) * (2 * E + 1)
    assert max_divisor_residues == 405
    assert PHI_LIMIT == 2 * max_divisor_residues
    assert K_BOUND == 656_100

    phi = phi_sieve(K_BOUND)
    eligible = [
        k for k in range(3, K_BOUND + 1, 4)
        if phi[k] <= PHI_LIMIT and math.gcd(k, Q) == 1
    ]

    qr317 = {x * x % Q for x in range(1, Q)}
    routed = [
        k for k in eligible
        if (-k) % Q != 0 and (-k) % Q in qr317
    ]

    saturations = []
    for k in routed:
        base = class_seed(k)
        seed = base * (Q ** E)
        if math.gcd(seed, k) != 1:
            continue
        residues = divisor_square_residues(seed, k)
        if len(residues) != phi[k] // 2:
            continue
        kernel = jacobi_kernel(k)
        assert len(kernel) == phi[k] // 2
        if residues == kernel:
            saturations.append(k)

    assert set(saturations) == EXPECTED_E2

    # Pin the two genuinely new exponent-two destinations and minimality.
    local = {}
    for k in sorted(EXPECTED_NEW):
        base = class_seed(k)
        kernel = jacobi_kernel(k)
        counts = {}
        sats = {}
        for e in (1, 2, 3, 4):
            seed = base * (Q ** e)
            residues = divisor_square_residues(seed, k)
            counts[e] = len(residues)
            sats[e] = residues == kernel
        assert not sats[1]
        assert sats[2]
        assert sats[3] and sats[4]
        local[k] = {
            "base_seed": base,
            "kernel_size": len(kernel),
            "residue_counts": counts,
            "saturated": sats,
        }

    assert local[39]["base_seed"] == 2
    assert local[39]["kernel_size"] == 12
    assert local[39]["residue_counts"][1] == 9
    assert local[39]["residue_counts"][2] == 12
    assert local[167]["base_seed"] == 42
    assert local[167]["kernel_size"] == 83
    assert local[167]["residue_counts"][1] == 61
    assert local[167]["residue_counts"][2] == 83

    # Character outputs.
    assert 39 == 3 * 13
    assert 169 % 3 == 1
    assert jacobi(169, 3) == 1
    assert 167 > 2 and all(167 % d for d in range(2, int(math.isqrt(167)) + 1))

    # Compatibility with the exact q29 tenth-lift parent progression.
    lift_mod = 4 * Q * Q
    combined = {}
    for k in sorted(EXPECTED_NEW):
        p0, modulus = crt_pair(PARENT_P, PARENT_MOD, (-k) % lift_mod, lift_mod)
        assert p0 == EXPECTED_CRT[k]
        assert modulus == EXPECTED_CRT_MOD
        assert p0 % PARENT_MOD == PARENT_P % PARENT_MOD
        assert (p0 + k) % lift_mod == 0
        Ck = (p0 + k) // 4
        assert valuation(Ck, Q) == 2
        assert jacobi(p0 % Q, Q) == 1
        combined[k] = {
            "p_class": p0,
            "modulus": modulus,
            "v317_Ck": 2,
        }

    report = {
        "analysis": "q317-square-lift-character-breakout-v1",
        "bound": {
            "max_divisor_residues": max_divisor_residues,
            "phi_limit": PHI_LIMIT,
            "odd_k_bound": K_BOUND,
            "eligible_low_totient_shifts": len(eligible),
            "compatible_q317_routes": len(routed),
        },
        "exponent_two_saturations": sorted(saturations),
        "new_vs_exponent_one": sorted(EXPECTED_NEW),
        "local_thresholds": local,
        "outputs": {
            "39": "HIT_OR_EXTRACT_13_POSITIVE",
            "167": "HIT_OR_EXTRACT_167_POSITIVE",
        },
        "parent_phase_compatibility": combined,
        "failures": 0,
        "claim": (
            "q317 multiplicity-one saturated misses are character-idempotent, but exponent2 adds exactly k39 and k167; "
            "both are minimally square-lift saturated and, on miss, force new positive q13 or q167 character data"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
