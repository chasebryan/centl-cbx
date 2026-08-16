#!/usr/bin/env python3
"""Verify the k15-origin q19 square-lift progress gate at k167."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

T_BASE = 7_423_185_617_863
T_STEP = 11_799_129_838_887
Q = 19
K = 167
SEED = 42 * Q * Q


def jacobi(a: int, n: int) -> int:
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


def residues(seed: int, k: int) -> set[int]:
    R = {1}
    for q, e in factorization(seed).items():
        R = {x * pow(q, a, k) % k for x in R for a in range(2 * e + 1)}
    return R


def legendre(a: int, p: int) -> int:
    r = pow(a % p, (p - 1) // 2, p)
    return 1 if r == 1 else -1 if r == p - 1 else 0


def t_of_s(s: int) -> int:
    return T_BASE + T_STEP * s


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # q19 materialization at C15.
    for t in range(19):
        c15 = 46 + 210 * t
        assert (c15 % 19 == 0) == (t == 11)
    assert jacobi(19, 15) == 1
    assert legendre(19, 23) == -1
    assert legendre(19, 47) == -1

    # Exact square-lift phase at C167.
    solutions = [t for t in range(361) if (84 + 210 * t) % 361 == 0]
    assert solutions == [144]
    assert 144 % 19 == 11
    assert pow(210, -1, 361) == 153

    # Persistent-route identity from origin15 to k167.
    assert K == 15 + 4 * Q * 2
    for t in range(0, 361 * 3, 37):
        c15 = 46 + 210 * t
        c167 = 84 + 210 * t
        assert c167 == c15 + 38
        if c15 % 19 == 0:
            A = c15 // 19
            assert c167 == 19 * (A + 2)

    # Double-square corridor conversion t=144 mod361 <=> s=312 mod361.
    assert T_BASE % 361 == 257
    assert T_STEP % 361 == 297
    assert math.gcd(T_STEP, 361) == 1
    s_phase = ((144 - T_BASE) * pow(T_STEP, -1, 361)) % 361
    assert s_phase == 312
    for h in range(10):
        s = 312 + 361 * h
        assert t_of_s(s) % 361 == 144

    # A phase-compatible member of the square-lift sublattice.
    s_wit = 1395
    assert s_wit % 361 == 312
    t = t_of_s(s_wit)
    phase = {m: t % m for m in (9, 11, 13, 17, 19, 23, 31, 43, 47)}
    assert phase == {9: 7, 11: 3, 13: 6, 17: 6, 19: 11, 23: 15, 31: 7, 43: 9, 47: 0}
    assert phase[19] in {0, 2, 7, 11, 14, 15, 16, 17}
    assert phase[13] in {1, 2, 5, 6, 7, 8, 9, 10, 11}
    assert phase[43] not in {2, 28, 30}
    assert phase[11] in {0, 2, 3, 4, 8}

    # Exact h169 class seed and QR saturation at prime k167.
    assert math.gcd(210, 84) == 42
    assert factorization(K) == Counter({167: 1})
    kernel = {u for u in range(1, K) if legendre(u, K) == 1}
    assert len(kernel) == 83
    R = residues(SEED, K)
    assert len(R) == 83
    assert R == kernel

    # Multiplicity-one control is not saturated.
    R1 = residues(42 * 19, K)
    assert R1 != kernel

    # Baseline h169 active sources do not contain q167.
    baseline = {7, 11, 23, 31}
    assert 167 not in baseline

    report = {
        "analysis": "k15-q19-square-lift-k167-v1",
        "materialization": {
            "tau19": 11,
            "source": 19,
            "origin": 15,
            "target_character": 1,
            "transverse": {"23": -1, "47": -1},
        },
        "square_lift": {
            "destination": 167,
            "route_index": 2,
            "t_phase": "144 mod361",
            "s_phase_on_k195_corridor": "312 mod361",
        },
        "phase_compatibility_witness": {"s": s_wit, **{f"tau{m}": r for m, r in phase.items()}},
        "saturation": {
            "class_seed": 42,
            "valuation": 2,
            "seed": SEED,
            "kernel_size": len(kernel),
            "saturated": True,
            "multiplicity_one_saturated": False,
        },
        "outcome": "if reached: k167 hit OR miss promotes (167/p)=+1",
        "failures": 0,
    }
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
