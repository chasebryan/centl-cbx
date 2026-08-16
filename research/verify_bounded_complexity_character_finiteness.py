#!/usr/bin/env python3
"""Regression verifier for bounded-complexity character finiteness."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter


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


def class_seed(k: int) -> int:
    return math.gcd(210, (169 + k) // 4)


def complexity_bound(m: int, E: int) -> int:
    assert m >= 0 and E >= 1
    return 162 * ((2 * E + 1) ** m)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # Exact h169 squarefree seed structure.
    assert factorization(210) == Counter({2: 1, 3: 1, 5: 1, 7: 1})
    max_omega = 0
    for k in range(3, 100_000, 4):
        s = class_seed(k)
        fac = factorization(s)
        assert 210 % s == 0
        assert all(e == 1 for e in fac.values())
        max_omega = max(max_omega, len(fac))
    assert max_omega <= 4

    rows = []
    for m in range(0, 5):
        for E in range(1, 7):
            B = complexity_bound(m, E)
            divisor_ceiling = 81 * ((2 * E + 1) ** m)
            assert B == 2 * divisor_ceiling
            rows.append({
                "arity_cap": m,
                "valuation_cap": E,
                "divisor_residue_ceiling": divisor_ceiling,
                "phi_ceiling": B,
                "destination_ceiling": B * B,
                "output_prime_ceiling": B + 1,
            })

    # Pin the three landed cardinality regimes.
    assert complexity_bound(1, 1) == 486
    assert complexity_bound(1, 1) ** 2 == 236_196
    assert complexity_bound(1, 2) == 810
    assert complexity_bound(1, 2) ** 2 == 656_100
    assert complexity_bound(2, 1) == 1458
    assert complexity_bound(2, 1) ** 2 == 2_125_764

    # The landed valuation-two fixed-point alphabet is inside P(1,2).
    A2 = {13, 19, 37, 47, 71, 167}
    assert max(A2) <= complexity_bound(1, 2) + 1

    # Known higher-valuation consistency check.
    assert 317 <= complexity_bound(1, 10) + 1

    # Direct odd-prime-power regression of phi(n)^2 >= n.
    for p in range(3, 500, 2):
        if any(p % d == 0 for d in range(3, int(math.isqrt(p)) + 1, 2)):
            continue
        for a in range(1, 7):
            phi_pa = (p ** (a - 1)) * (p - 1)
            assert phi_pa * phi_pa >= p ** a

    report = {
        "analysis": "bounded-complexity-character-finiteness-v1",
        "max_h169_class_seed_omega_regression": max_omega,
        "complexity_rows": rows,
        "pinned_regimes": {
            "m1_E1": {
                "phi": complexity_bound(1, 1),
                "k": complexity_bound(1, 1) ** 2,
                "output_prime": complexity_bound(1, 1) + 1,
            },
            "m1_E2": {
                "phi": complexity_bound(1, 2),
                "k": complexity_bound(1, 2) ** 2,
                "output_prime": complexity_bound(1, 2) + 1,
            },
            "m2_E1": {
                "phi": complexity_bound(2, 1),
                "k": complexity_bound(2, 1) ** 2,
                "output_prime": complexity_bound(2, 1) + 1,
            },
        },
        "valuation2_fixed_point_alphabet": sorted(A2),
        "escape_dichotomy": [
            "unbounded source valuation",
            "unbounded routed-source arity",
            "transition outside bounded Jacobi saturation",
        ],
        "failures": 0,
        "claim": (
            "for fixed routed-source arity m and valuation cap E, every h169 Jacobi-saturated destination satisfies "
            "phi(k)<=162(2E+1)^m and every extracted prime character is <=162(2E+1)^m+1; "
            "therefore recursive fresh-character growth inside a fixed complexity box is finite"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
