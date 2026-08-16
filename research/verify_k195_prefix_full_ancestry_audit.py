#!/usr/bin/env python3
"""Deterministic 64-bit full signed-box ancestry audit for the first k195 corridor prefix."""
from __future__ import annotations

import argparse
import collections
import json
import math

T_BASE = 7_423_185_617_863
T_STEP = 11_799_129_838_887
S_LIMIT = 1000
U64 = 1 << 64

S19_D = frozenset({0, 2, 7, 11, 14, 15, 16, 17})
S13 = frozenset({1, 2, 5, 6, 7, 8, 9, 10, 11})
S43 = frozenset(set(range(43)) - {2, 28, 30})
S11 = frozenset({0, 2, 3, 4, 8, 9})

EXPECTED_PRIME_S = (
    21, 33, 51, 65, 91, 108, 143, 198, 208, 316, 337, 363, 395,
    449, 451, 458, 559, 602, 645, 696, 734, 759, 762, 810, 850, 901,
    943, 944, 945, 968, 979,
)
EXPECTED_HIST = {3: 21, 7: 6, 11: 4}


def t_of_s(s: int) -> int:
    return T_BASE + T_STEP * s


def p_of_s(s: int) -> int:
    return 169 + 840 * t_of_s(s)


def phase_ok(s: int) -> bool:
    t = t_of_s(s)
    return (
        t % 19 in S19_D
        and t % 13 in S13
        and t % 43 in S43
        and t % 11 in S11
    )


def is_prime_u64(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    assert n < U64, n
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    for c in range(1, 128):
        x = 2 + c
        y = x
        d = 1
        for _ in range(200_000):
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            if d == 1:
                continue
            if d != n:
                return d
            break
    raise RuntimeError(f"Pollard-rho failed on {n}")


def factor_u64(n: int) -> collections.Counter[int]:
    assert 0 < n < U64
    out: collections.Counter[int] = collections.Counter()

    # Peel a modest deterministic trial-division prefix first.
    p = 2
    while p <= 97:
        while n % p == 0:
            out[p] += 1
            n //= p
        p += 1 if p == 2 else 2
        if p == 4:
            p = 3
    # The loop above intentionally visits odd integers too; primality below
    # keeps correctness independent of whether a trial divisor was prime.

    def rec(m: int) -> None:
        if m == 1:
            return
        if is_prime_u64(m):
            out[m] += 1
            return
        d = pollard_rho(m)
        rec(d)
        rec(m // d)

    rec(n)
    product = 1
    for q, e in out.items():
        assert is_prime_u64(q)
        product *= q ** e
    return out


def factor_exact(n: int) -> collections.Counter[int]:
    original = n
    fac = factor_u64(n)
    product = 1
    for q, e in fac.items():
        product *= q ** e
    assert product == original, (original, fac, product)
    return fac


def divisor_square_residues_from_factorization(fac: collections.Counter[int], k: int) -> set[int]:
    residues = {1 % k}
    for q, e in fac.items():
        powers = [pow(q, a, k) for a in range(2 * e + 1)]
        residues = {x * y % k for x in residues for y in powers}
    return residues


def signed_box_hit(p: int, k: int) -> tuple[bool, bool, int, collections.Counter[int], int]:
    assert p % 4 == 1 and k % 4 == 3
    C = (p + k) // 4
    assert C < U64
    fac = factor_exact(C)
    residues = divisor_square_residues_from_factorization(fac, k)
    type_i_target = (-pow(4, -1, k)) % k
    type_ii_target = (-C) % k
    return (
        type_i_target in residues,
        type_ii_target in residues,
        C,
        fac,
        len(residues),
    )


def first_hit(p: int, k_max: int = 195) -> dict[str, object] | None:
    for k in range(3, k_max + 1, 4):
        type_i, type_ii, C, fac, residue_count = signed_box_hit(p, k)
        if type_i or type_ii:
            return {
                "k": k,
                "type_i": type_i,
                "type_ii": type_ii,
                "C": C,
                "factorization": dict(sorted(fac.items())),
                "residue_count": residue_count,
            }
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    phase_classes = [s for s in range(S_LIMIT) if phase_ok(s)]
    assert len(phase_classes) == 150

    # Every target in this canonical prefix is genuinely below 2^64, so the
    # Miller-Rabin basis above is deterministic rather than probable-prime.
    assert max(p_of_s(s) for s in range(S_LIMIT)) < U64

    prime_s = tuple(s for s in phase_classes if is_prime_u64(p_of_s(s)))
    assert prime_s == EXPECTED_PRIME_S

    hist: collections.Counter[int] = collections.Counter()
    rows = []
    for s in prime_s:
        p = p_of_s(s)
        hit = first_hit(p)
        assert hit is not None
        k = int(hit["k"])
        hist[k] += 1
        rows.append({
            "s": s,
            "p": p,
            "tau19": t_of_s(s) % 19,
            "tau13": t_of_s(s) % 13,
            "tau43": t_of_s(s) % 43,
            "tau11": t_of_s(s) % 11,
            "first_hit": hit,
        })

    assert dict(sorted(hist.items())) == EXPECTED_HIST
    assert max(hist) == 11
    assert sum(hist.values()) == len(prime_s) == 31

    mechanism_hist = collections.Counter()
    for row in rows:
        h = row["first_hit"]
        if h["type_i"] and h["type_ii"]:
            mechanism_hist["I+II"] += 1
        elif h["type_i"]:
            mechanism_hist["I-only"] += 1
        elif h["type_ii"]:
            mechanism_hist["II-only"] += 1
    assert mechanism_hist == collections.Counter({"I+II": 31})

    report = {
        "analysis": "k195-prefix-full-ancestry-audit-v1",
        "scope": {
            "s_min": 0,
            "s_max_exclusive": S_LIMIT,
            "phase_filtered_classes": len(phase_classes),
            "prime_targets": len(prime_s),
            "deterministic_u64": True,
        },
        "first_hit_histogram": {str(k): v for k, v in sorted(hist.items())},
        "mechanism_histogram": dict(mechanism_hist),
        "maximum_first_hit": max(hist),
        "reaches_k195": 0,
        "prime_s": list(prime_s),
        "rows": rows,
        "claim_boundary": (
            "exact finite ancestry census on the canonical 0<=s<1000 prefix of the current phase envelope; "
            "not a universal absorber theorem and not evidence that later s-classes cannot reach k195"
        ),
        "failures": 0,
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
