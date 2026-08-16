#!/usr/bin/env python3
"""Complete finite verifier for the h169 D-selector single-source saturation barrier."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

PHI_LIMIT = 486
ABSOLUTE_K_BOUND = 2 * PHI_LIMIT * PHI_LIMIT
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

    # Finite regression of the elementary phi(n)^2 >= n/2 inequality over
    # the entire exact search interval. The document also contains the direct
    # prime-power proof, so correctness does not depend on this finite check.
    assert all(2 * phi[n] * phi[n] >= n for n in range(1, ABSOLUTE_K_BOUND + 1))

    eligible_k = [
        k for k in range(3, ABSOLUTE_K_BOUND + 1, 4)
        if phi[k] <= PHI_LIMIT
    ]
    assert len(eligible_k) == 158
    assert max(eligible_k) == 1155

    # Jacobi(-1/k)=-1 makes the character nontrivial, so every positive
    # kernel has exactly phi(k)/2 units.
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
            delta = k - origin
            assert delta % 4 == 0
            d = delta // 4
            for q in factorization(d):
                if not source_type(q, origin, negative_modulus):
                    continue
                n = d // q
                assert n >= 1
                assert k == origin + 4 * q * n
                assert math.gcd(q, k) == 1

                base = class_seed(k)
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
                        "seed": seed,
                    })

                if saturates(seed, k, kernel_cache):
                    saturations.append({
                        "type": label,
                        "origin": origin,
                        "q": q,
                        "n": n,
                        "k": k,
                        "seed": seed,
                    })

    assert counts == Counter({"B": 61, "D": 58, "J": 61}), counts
    assert sum(counts.values()) == 180
    assert not saturations, saturations

    report = {
        "analysis": "d-selector-single-source-saturation-barrier-v1",
        "absolute_bound": {
            "max_seed_prime_factors": 5,
            "max_square_divisor_count": 243,
            "required_phi_max": PHI_LIMIT,
            "phi_lower_bound": "phi(k)^2 >= k/2",
            "k_bound": ABSOLUTE_K_BOUND,
        },
        "finite_closure": {
            "eligible_k_count": len(eligible_k),
            "largest_eligible_k": max(eligible_k),
            "persistent_candidate_pairs": sum(counts.values()),
            "by_type": dict(counts),
            "jacobi_saturations": len(saturations),
        },
        "candidate_examples": candidate_examples,
        "failures": 0,
        "claim": (
            "for h169 and any later persistent destination of a materialized D-selector B/D/J witness type, "
            "the mandatory class seed plus that single routed prime never Jacobi-saturates; "
            "a second routed factor or richer exact ancestry is required for saturation"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
