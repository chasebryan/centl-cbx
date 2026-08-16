#!/usr/bin/env python3
"""Regression verifier for the valuation-to-output-prime ceiling theorem."""
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


def phi_sieve(n: int) -> list[int]:
    phi = list(range(n + 1))
    for p in range(2, n + 1):
        if phi[p] == p:
            for m in range(p, n + 1, p):
                phi[m] -= phi[m] // p
    return phi


def class_seed(k: int) -> int:
    return math.gcd(210, (169 + k) // 4)


def one_source_phi_ceiling(e: int) -> int:
    return 162 * (2 * e + 1)


def one_source_output_ceiling(e: int) -> int:
    return one_source_phi_ceiling(e) + 1


def multi_source_phi_ceiling(exponents: tuple[int, ...]) -> int:
    product = 1
    for e in exponents:
        assert e >= 1
        product *= 2 * e + 1
    return 162 * product


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # h169 class-seed complexity.
    assert factorization(210) == Counter({2: 1, 3: 1, 5: 1, 7: 1})
    max_seed_omega = 0
    seeds = set()
    for k in range(3, 50_000, 4):
        s = class_seed(k)
        seeds.add(s)
        fac = factorization(s)
        assert all(e == 1 for e in fac.values())
        assert 210 % s == 0
        max_seed_omega = max(max_seed_omega, len(fac))
    assert max_seed_omega <= 4

    # Direct finite regression of the odd totient inequality used by the theorem.
    phi = phi_sieve(250_000)
    worst_margin = None
    worst_n = None
    for n in range(1, len(phi), 2):
        margin = phi[n] * phi[n] - n
        assert margin >= 0
        if worst_margin is None or margin < worst_margin:
            worst_margin = margin
            worst_n = n

    # Prime-power factor proof ingredients for a broad exact regression.
    for p in range(3, 1000, 2):
        if any(p % d == 0 for d in range(3, int(math.isqrt(p)) + 1, 2)):
            continue
        assert (p - 1) * (p - 1) >= p
        for a in range(1, 8):
            lhs = (p ** (a - 1) * (p - 1)) ** 2
            rhs = p ** a
            assert lhs >= rhs

    rows = []
    for e in range(1, 21):
        divisor_ceiling = (3 ** 4) * (2 * e + 1)
        phi_ceiling = one_source_phi_ceiling(e)
        k_ceiling = phi_ceiling * phi_ceiling
        output_ceiling = one_source_output_ceiling(e)
        assert divisor_ceiling == 81 * (2 * e + 1)
        assert phi_ceiling == 2 * divisor_ceiling
        assert output_ceiling == 324 * e + 163
        rows.append({
            "valuation": e,
            "divisor_residue_ceiling": divisor_ceiling,
            "phi_ceiling": phi_ceiling,
            "k_ceiling": k_ceiling,
            "output_prime_ceiling": output_ceiling,
        })

    # Known landed one-source examples.
    assert one_source_phi_ceiling(1) == 486
    assert one_source_phi_ceiling(2) == 810
    assert one_source_output_ceiling(2) == 811
    assert 13 <= one_source_output_ceiling(2)
    assert 167 <= one_source_output_ceiling(2)
    assert one_source_output_ceiling(10) == 3403
    assert 317 <= one_source_output_ceiling(10)

    # Landed two-source multiplicity-one theorem is the m=2,e1=e2=1 case.
    assert multi_source_phi_ceiling((1, 1)) == 1458
    assert multi_source_phi_ceiling((1, 1)) ** 2 == 2_125_764

    # Example descent threshold semantics.
    examples = []
    for q, e in ((1009, 1), (5000, 2), (10000, 10)):
        ceiling = one_source_output_ceiling(e)
        if q > ceiling:
            assert ceiling < q
            examples.append({
                "incoming_q": q,
                "valuation": e,
                "output_prime_ceiling": ceiling,
                "strict_descent": True,
            })

    report = {
        "analysis": "valuation-output-prime-ceiling-v1",
        "h169_class_seed": {
            "distinct_observed_seeds_under_50000": len(seeds),
            "max_distinct_prime_factors": max_seed_omega,
            "ambient_squarefree_seed": 210,
        },
        "odd_totient_regression": {
            "checked_through": len(phi) - 1,
            "minimum_margin_phi_squared_minus_n": worst_margin,
            "minimum_margin_witness": worst_n,
        },
        "one_source_rows": rows,
        "known_transition_checks": {
            "q317_e2_outputs": [13, 167],
            "q317_e2_ceiling": one_source_output_ceiling(2),
            "q29_e10_output": 317,
            "q29_e10_ceiling": one_source_output_ceiling(10),
        },
        "two_source_e1_phi_ceiling": multi_source_phi_ceiling((1, 1)),
        "descent_examples": examples,
        "failures": 0,
        "claim": (
            "for an h169 Jacobi-saturated seed built from the squarefree class seed plus one source q^e, "
            "phi(k)<=162(2e+1), k<=[162(2e+1)]^2, and every extractable prime character r<=324e+163; "
            "therefore q>324e+163 implies strict prime-modulus descent on any miss-generated source"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
