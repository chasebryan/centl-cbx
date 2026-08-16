#!/usr/bin/env python3
"""Complete finite verifier for the h169 D-selector single-source multiplicity-one saturation barrier."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

PHI_LIMIT = 486
# Admissible k is odd, hence phi(k)^2 >= k.
ABSOLUTE_K_BOUND = PHI_LIMIT * PHI_LIMIT
ORIGINS = {
    "B": (23, 17),
    "D": (31, 17),
    "J": (47, 31),
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
    assert k % 4 == 3
    return math.gcd(210, (169 + k) // 4)


def source_type(q: int, origin: int, negative_modulus: int) -> bool:
    return (
        q % 2 == 1
        and math.gcd(q, origin * negative_modulus) == 1
        and jacobi(q, origin) == 1
        and jacobi(q, negative_modulus) == -1
    )


def saturates(seed: int, k: int, kernel_cache: dict[int, set[int]]) -> bool:
    if math.gcd(seed, k) != 1:
        return False
    kernel = kernel_cache.setdefault(k, jacobi_kernel(k))
    return divisor_square_residues(seed, k) == kernel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    phi = phi_sieve(ABSOLUTE_K_BOUND)
    assert all(phi[k] * phi[k] >= k for k in range(3, ABSOLUTE_K_BOUND + 1, 2))

    eligible_k = [
        k for k in range(3, ABSOLUTE_K_BOUND + 1, 4)
        if phi[k] <= PHI_LIMIT
    ]
    assert len(eligible_k) == 158
    assert max(eligible_k) == 1155

    kernel_cache: dict[int, set[int]] = {}
    for k in eligible_k:
        kernel = jacobi_kernel(k)
        kernel_cache[k] = kernel
        assert len(kernel) == phi[k] // 2
        assert jacobi(-1, k) == -1

    counts = Counter()
    saturations: list[dict[str, int | str]] = []
    candidate_examples: list[dict[str, int | str]] = []

    for label, (origin, negative_modulus) in ORIGINS.items():
        for k in eligible_k:
            if k <= origin:
                continue
            d = (k - origin) // 4
            for q in factorization(d):
                if not source_type(q, origin, negative_modulus):
                    continue
                n = d // q
                assert n >= 1
                assert k == origin + 4 * q * n

                base = class_seed(k)
                # Multiplicity-one scope: one known copy of q only.
                seed = math.lcm(base, q)
                omega = len(factorization(seed))
                assert omega <= 5
                assert len(divisor_square_residues(seed, k)) <= 3 ** omega <= 243

                counts[label] += 1
                if len(candidate_examples) < 12:
                    candidate_examples.append({
                        "type": label,
                        "origin": origin,
                        "negative_modulus": negative_modulus,
                        "q": q,
                        "n": n,
                        "k": k,
                        "phi_k": phi[k],
                        "base_seed": base,
                        "multiplicity_one_seed": seed,
                    })

                if saturates(seed, k, kernel_cache):
                    saturations.append({"type": label, "origin": origin, "q": q, "n": n, "k": k, "seed": seed})

    assert counts == Counter({"B": 61, "D": 58, "J": 61}), counts
    assert sum(counts.values()) == 180
    assert not saturations, saturations

    report = {
        "analysis": "d-selector-single-source-saturation-barrier-v2-valuation-safe",
        "scope": "multiplicity-one routed source factor; requires v_q(C_k)=1 before pruning",
        "absolute_bound": {
            "max_seed_prime_factors": 5,
            "max_square_divisor_count": 243,
            "required_phi_max": PHI_LIMIT,
            "odd_k_phi_bound": "phi(k)^2 >= k",
            "k_bound": ABSOLUTE_K_BOUND,
        },
        "finite_closure": {
            "eligible_k_count": len(eligible_k),
            "largest_eligible_k": max(eligible_k),
            "persistent_candidate_pairs": sum(counts.values()),
            "by_type": dict(counts),
            "multiplicity_one_jacobi_saturations": len(saturations),
        },
        "candidate_examples": candidate_examples,
        "valuation_boundary": "q-adic lifts q^e, e>=2, are separate live states",
        "failures": 0,
        "claim": (
            "in the valuation-one sector, the h169 class seed plus one known copy of a renewed source prime never Jacobi-saturates; "
            "higher q-adic lifts are explicitly outside this barrier"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
