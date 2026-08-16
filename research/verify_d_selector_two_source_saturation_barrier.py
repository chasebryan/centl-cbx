#!/usr/bin/env python3
"""Complete verifier for D-selector two-source synchronization and saturation barrier."""
from __future__ import annotations

import argparse
import json
import math
from array import array
from collections import Counter

PHI_LIMIT = 1458
ABSOLUTE_K_BOUND = 2 * PHI_LIMIT * PHI_LIMIT
TYPES = {
    "B": (23, 17),
    "D": (31, 17),
    "J": (47, 31),
}
PAIR_TYPES = (("B", "D"), ("B", "J"), ("D", "J"))


def phi_sieve(n: int) -> array:
    phi = array("I", range(n + 1))
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


def source_type(q: int, origin: int, negative_modulus: int) -> bool:
    return (
        q % 2 == 1
        and math.gcd(q, origin * negative_modulus) == 1
        and jacobi(q, origin) == 1
        and jacobi(q, negative_modulus) == -1
    )


def class_seed(k: int) -> int:
    return math.gcd(210, (169 + k) // 4)


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


def crt_x(a1: int, q1: int, a2: int, q2: int) -> tuple[int, int]:
    assert math.gcd(q1, q2) == 1
    t = ((a2 - a1) * pow(q1, -1, q2)) % q2
    mod = q1 * q2
    return (a1 + q1 * t) % mod, mod


def synchronized_class(j1: int, q1: int, j2: int, q2: int) -> tuple[int, int]:
    a1 = (j1 - 3) // 4
    a2 = (j2 - 3) // 4
    x0, xmod = crt_x(a1, q1, a2, q2)
    return 3 + 4 * x0, 4 * xmod


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    phi = phi_sieve(ABSOLUTE_K_BOUND)
    eligible = [
        k for k in range(3, ABSOLUTE_K_BOUND + 1, 4)
        if phi[k] <= PHI_LIMIT
    ]
    assert len(eligible) == 474
    assert max(eligible) == 3255

    counts = Counter()
    saturations: list[dict[str, int | str]] = []
    candidate_ks: list[int] = []
    examples: list[dict[str, int | str]] = []
    kernel_cache: dict[int, set[int]] = {}

    for k in eligible:
        available: dict[str, list[int]] = {}
        for label, (origin, negative_modulus) in TYPES.items():
            if k <= origin:
                available[label] = []
                continue
            d = (k - origin) // 4
            available[label] = [
                q for q in factorization(d)
                if source_type(q, origin, negative_modulus)
            ]

        for left, right in PAIR_TYPES:
            j1, _ = TYPES[left]
            j2, _ = TYPES[right]
            for q1 in available[left]:
                for q2 in available[right]:
                    if q1 == q2:
                        # Actual D-selector witnesses occupy distinct odd
                        # reservoirs. The abstract enumeration may encounter a
                        # prime satisfying two character types, but such a same-q
                        # pair is not an allowed renewed-source pair.
                        continue
                    assert math.gcd(q1, q2) == 1
                    n1 = (k - j1) // (4 * q1)
                    n2 = (k - j2) // (4 * q2)
                    assert n1 >= 1 and n2 >= 1
                    assert k == j1 + 4 * q1 * n1
                    assert k == j2 + 4 * q2 * n2

                    k0, period = synchronized_class(j1, q1, j2, q2)
                    assert (k - k0) % period == 0

                    base = class_seed(k)
                    seed = math.lcm(base, q1, q2)
                    omega = len(factorization(seed))
                    assert omega <= 6
                    residues = divisor_square_residues(seed, k)
                    assert len(residues) <= 3 ** omega <= 729

                    key = f"{left}{right}"
                    counts[key] += 1
                    candidate_ks.append(k)
                    if len(examples) < 15:
                        examples.append({
                            "pair_type": key,
                            "k": k,
                            "q1": q1,
                            "q2": q2,
                            "n1": n1,
                            "n2": n2,
                            "sync_class": k0,
                            "sync_period": period,
                            "phi_k": int(phi[k]),
                            "base_seed": base,
                            "two_source_seed": seed,
                        })

                    kernel = kernel_cache.setdefault(k, jacobi_kernel(k))
                    assert len(kernel) == phi[k] // 2
                    if residues == kernel:
                        saturations.append({
                            "pair_type": key,
                            "k": k,
                            "q1": q1,
                            "q2": q2,
                            "seed": seed,
                        })

    assert counts == Counter({"BD": 102, "BJ": 46, "DJ": 101}), counts
    assert sum(counts.values()) == 249
    assert candidate_ks and max(candidate_ks) == 2499
    assert not saturations, saturations

    report = {
        "analysis": "d-selector-two-source-saturation-barrier-v1",
        "absolute_bound": {
            "max_seed_prime_factors": 6,
            "max_square_divisor_count": 729,
            "required_phi_max": PHI_LIMIT,
            "k_bound": ABSOLUTE_K_BOUND,
        },
        "synchronization": {
            "theorem": "distinct source primes always synchronize by CRT in x=(k-3)/4",
            "pair_types": ["BD", "BJ", "DJ"],
        },
        "finite_closure": {
            "eligible_low_totient_k": len(eligible),
            "largest_low_totient_k": max(eligible),
            "synchronized_candidate_pairs": sum(counts.values()),
            "by_pair_type": dict(counts),
            "largest_synchronized_candidate_k": max(candidate_ks),
            "jacobi_saturations": len(saturations),
        },
        "examples": examples,
        "failures": 0,
        "claim": (
            "every distinct pair of materialized D-selector renewed sources has a common persistent CRT ladder, "
            "but the bare h169 class seed plus those two sources never Jacobi-saturates any common destination; "
            "bare saturation therefore requires at least three renewed sources or additional proof-bearing ancestry"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
