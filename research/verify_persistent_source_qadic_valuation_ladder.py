#!/usr/bin/env python3
"""Verify the exact q-adic valuation grammar on persistent companion-source ladders."""
from __future__ import annotations

import argparse
import json
import math


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


def prime_factors(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out.append(n)
    return out


def vp(n: int, q: int) -> int:
    if n <= 0:
        raise ValueError(n)
    e = 0
    while n % q == 0:
        n //= q
        e += 1
    return e


def companion(p: int, k: int) -> int:
    assert p % 4 == 1 and k % 4 == 3
    return (p + k) // 4


def check_source(p: int, j: int, q: int, steps: int = 160) -> int:
    Cj = companion(p, j)
    assert Cj % q == 0
    A = Cj // q
    checks = 0

    for n in range(steps + 1):
        k = j + 4 * q * n
        Ck = companion(p, k)
        assert Ck == Cj + q * n == q * (A + n)
        valuation = vp(Ck, q)
        assert valuation == 1 + vp(A + n, q)

        for e in range(2, 6):
            at_least = valuation >= e
            assert at_least == ((A + n) % (q ** (e - 1)) == 0)
            assert at_least == ((p + k) % (4 * q**e) == 0)
            assert at_least == ((k + p) % (4 * q**e) == 0)

            exact = valuation == e
            phase_exact = (
                (A + n) % (q ** (e - 1)) == 0
                and (A + n) % (q**e) != 0
            )
            assert exact == phase_exact
        checks += 1

    # Exact phase counts on one q^3 block for small q.
    if q <= 13:
        period = q**3
        vals = [1 + vp(A + n, q) for n in range(period)]
        assert sum(v >= 2 for v in vals) == q**2
        assert sum(v >= 3 for v in vals) == q
        assert sum(v >= 4 for v in vals) == 1
        assert sum(v == 1 for v in vals) == (q - 1) * q**2
        assert sum(v == 2 for v in vals) == (q - 1) * q
        assert sum(v == 3 for v in vals) == q - 1

    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    general_sources = 0
    general_checks = 0
    origin_histogram: dict[int, int] = {}

    # Broad regression over small prime targets and admissible shifts.
    for p in range(5, 2501):
        if p % 4 != 1 or not is_prime(p):
            continue
        for j in range(3, 100, 4):
            Cj = companion(p, j)
            for q in prime_factors(Cj):
                if q == 2 or math.gcd(q, j) != 1:
                    continue
                general_sources += 1
                origin_histogram[j] = origin_histogram.get(j, 0) + 1
                general_checks += check_source(p, j, q, steps=24)

    assert general_sources > 1000
    assert general_checks > 20_000

    # Adversarial high-valuation origins.
    pinned = [
        # p, j, q, expected v_q(C_j)
        (13, 23, 3, 2),   # C23=9
        (269, 31, 5, 2),  # C31=75
        (61, 47, 3, 3),   # C47=27
    ]
    pinned_rows = []
    for p, j, q, expected in pinned:
        assert is_prime(p)
        Cj = companion(p, j)
        assert vp(Cj, q) == expected
        A = Cj // q
        check_source(p, j, q, steps=200)
        pinned_rows.append({
            "p": p,
            "origin_j": j,
            "q": q,
            "C_j": Cj,
            "A": A,
            "origin_valuation": expected,
            "square_lift_n_phase": (-A) % q,
            "cube_lift_n_phase": (-A) % (q*q),
        })

    # Two-source lift compatibility is CRT after the common factor 4 is removed.
    # A concrete coprime check is sufficient here because the theorem itself is algebraic.
    q1, q2 = 5, 7
    e1, e2 = 3, 2
    assert math.gcd(q1**e1, q2**e2) == 1
    a1, a2 = 17, 9
    x = a1 + q1**e1 * (((a2 - a1) * pow(q1**e1, -1, q2**e2)) % (q2**e2))
    assert x % (q1**e1) == a1 % (q1**e1)
    assert x % (q2**e2) == a2 % (q2**e2)

    report = {
        "analysis": "persistent-source-qadic-valuation-ladder-v1",
        "general_regression": {
            "materialized_sources": general_sources,
            "route_points_checked": general_checks,
            "origins_seen": len(origin_histogram),
        },
        "pinned_high_valuation_origins": pinned_rows,
        "theorem": {
            "companion_identity": "C_(j+4qn)=q(A+n), A=C_j/q",
            "valuation": "v_q(C_k)=1+v_q(A+n)",
            "at_least_e_n_phase": "n=-A mod q^(e-1)",
            "at_least_e_k_phase": "k=-p mod 4q^e",
            "exact_e": "lift at e but not e+1",
        },
        "scheduler_boundary": "multiplicity-one saturation barriers require proven v_q(C_k)=1; UNKNOWN is not exponent1",
        "failures": 0,
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
