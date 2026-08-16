#!/usr/bin/env python3
"""Verify the conditional k195 double-square valuation selector."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter

K = 195
QD = 41
QJ = 37
T0 = 3_925_816
T_STEP = 5_127_183
V0 = 1_447_809
V_MOD = 2_301_289
S39 = frozenset({1, 2, 5, 6, 7, 8, 9, 10, 11})
S43 = frozenset(set(range(43)) - {2, 28, 30})
S47 = frozenset(set(range(47)) - {1, 5, 6, 10, 13, 21, 23, 36, 37, 38, 40, 42, 44})
S51 = frozenset(set(range(17)) - {4, 5, 7, 14})
S55 = frozenset(set(range(11)) - {5, 6, 7, 10})


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


def phi(n: int) -> int:
    out = n
    for q in factorization(n):
        out -= out // q
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


def legendre(a: int, p: int) -> int:
    return jacobi(a, p)


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


def crt_pair(r1: int, m1: int, r2: int, m2: int) -> tuple[int, int]:
    g = math.gcd(m1, m2)
    if (r2 - r1) % g:
        raise AssertionError("incompatible CRT pair")
    m2g = m2 // g
    if m2g == 1:
        lcm = m1 // g * m2
        return r1 % lcm, lcm
    y = ((r2 - r1) // g) * pow(m1 // g, -1, m2g) % m2g
    lcm = m1 // g * m2
    return (r1 + m1 * y) % lcm, lcm


def class_seed(k: int) -> int:
    return math.gcd(210, (169 + k) // 4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # Exact Route-B D-selector progression.
    assert T0 == 705 + 1081 * 3631
    assert T_STEP == 1081 * 4743

    # Character types of the materialized D/J witnesses.
    assert legendre(QD, 31) == 1
    assert legendre(QD, 17) == -1
    assert legendre(QJ, 47) == 1
    assert legendre(QJ, 31) == -1

    # k195 is the first positive route index for both source ladders.
    assert (K - 31) // 4 == QD
    assert (K - 47) // 4 == QJ
    assert K == 31 + 4 * QD
    assert K == 47 + 4 * QJ

    # C195 = 91 + 210t. Square-lift t phases are unique.
    c0 = (169 + K) // 4
    assert c0 == 91
    t41 = (-c0 * pow(210, -1, QD * QD)) % (QD * QD)
    t37 = (-c0 * pow(210, -1, QJ * QJ)) % (QJ * QJ)
    assert t41 == 728
    assert t37 == 319

    v41 = (t41 - T0) * pow(T_STEP, -1, QD * QD) % (QD * QD)
    v37 = (t37 - T0) * pow(T_STEP, -1, QJ * QJ) % (QJ * QJ)
    assert v41 == 468
    assert v37 == 776
    v0, vmod = crt_pair(v41, QD * QD, v37, QJ * QJ)
    assert (v0, vmod) == (V0, V_MOD)
    assert V_MOD == QD * QD * QJ * QJ

    # Verify the lift and source materialization on several points of the exact sublattice.
    for s in range(8):
        v = V0 + V_MOD * s
        t = T0 + T_STEP * v
        p = 169 + 840 * t
        C195 = (p + K) // 4
        D = 5 + 21 * t
        J = 9 + 35 * t
        assert D % QD == 0
        assert J % QJ == 0
        assert C195 % (QD * QD) == 0
        assert C195 % (QJ * QJ) == 0

    # Exact saturation threshold at k195.
    base = class_seed(K)
    assert base == 7
    kernel = jacobi_kernel(K)
    assert phi(K) == 96
    assert len(kernel) == 48
    assert all(jacobi(q, K) == 1 for q in (7, QD, QJ))

    residue_counts: dict[str, int] = {}
    saturated: dict[str, bool] = {}
    for eD, eJ in ((1, 1), (2, 1), (1, 2), (2, 2)):
        seed = 7 * (QD ** eD) * (QJ ** eJ)
        residues = divisor_square_residues(seed, K)
        key = f"{eD},{eJ}"
        residue_counts[key] = len(residues)
        saturated[key] = residues == kernel

    assert residue_counts == {"1,1": 24, "2,1": 35, "1,2": 36, "2,2": 48}
    assert saturated == {"1,1": False, "2,1": False, "1,2": False, "2,2": True}

    # Once both quadratic lifts saturate, all higher exponents remain saturated.
    for eD in range(2, 6):
        for eJ in range(2, 6):
            seed = 7 * (QD ** eD) * (QJ ** eJ)
            assert divisor_square_residues(seed, K) == kernel

    # h169 fixed characters at 3 and5 are positive.
    assert 169 % 3 == 1
    assert 169 % 5 == 4
    assert legendre(169, 3) == 1
    assert legendre(169, 5) == 1

    # p = 8t mod13, and 8 is NR13. Classify the landed k39 survivor phases.
    assert 169 % 13 == 0
    assert 840 % 13 == 8
    assert legendre(8, 13) == -1
    forced_hit = set()
    compatible = set()
    rows = []
    for t13 in sorted(S39):
        p13 = 8 * t13 % 13
        char13 = legendre(p13, 13)
        rows.append((t13, p13, char13))
        if char13 == -1:
            forced_hit.add(t13)
        else:
            compatible.add(t13)
    assert forced_hit == {1, 9, 10}
    assert compatible == {2, 5, 6, 7, 8, 11}
    assert len(S39) == 9 and len(compatible) == 6

    # The lift corridor is not empty under the currently landed phase-only filters through k55.
    s = 5
    v = V0 + V_MOD * s
    t = T0 + T_STEP * v
    phase_witness = {
        13: t % 13,
        43: t % 43,
        47: t % 47,
        17: t % 17,
        11: t % 11,
    }
    assert phase_witness == {13: 7, 43: 12, 47: 0, 17: 6, 11: 1}
    assert phase_witness[13] in S39
    assert phase_witness[43] in S43
    assert phase_witness[47] in S47
    assert phase_witness[17] in S51
    assert phase_witness[11] in S55

    report = {
        "analysis": "k195-double-square-phase-selector-v1",
        "route_b_d_selector": {"t0": T0, "t_step": T_STEP},
        "sources": {
            "D": {"q": QD, "origin": 31, "characters": {"31": 1, "17": -1}},
            "J": {"q": QJ, "origin": 47, "characters": {"47": 1, "31": -1}},
        },
        "destination": K,
        "double_square_phase": {
            "t_mod_41sq": t41,
            "t_mod_37sq": t37,
            "v_class": V0,
            "v_modulus": V_MOD,
        },
        "saturation": {
            "class_seed": base,
            "phi": phi(K),
            "kernel_size": len(kernel),
            "residue_counts": residue_counts,
            "saturated": saturated,
            "higher_exponents_checked": "2..5 in each source",
        },
        "tau13_selector": {
            "k39_survivors": sorted(S39),
            "forced_k195_hit": sorted(forced_hit),
            "k195_miss_character_compatible": sorted(compatible),
            "contraction": "9->6",
        },
        "phase_only_nonempty_witness": phase_witness,
        "full_ancestry_reachability": "not proved",
        "failures": 0,
        "claim": (
            "conditional on materialized q_D=41 and q_J=37 with both square lifts at k195, "
            "the seed 7*41^2*37^2 Jacobi-saturates; tau13 phases 1,9,10 force a k195 hit, "
            "while only 2,5,6,7,8,11 remain character-compatible with a miss"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
