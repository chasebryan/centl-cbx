#!/usr/bin/env python3
"""Exact certificate for a q19/q41/q37 corridor prime whose first hit is k35."""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import math

S = 2_778_207
T0 = 7_423_185_617_863
DT = 11_799_129_838_887
T = 32_780_432_535_490_353_472
P = 27_535_563_329_811_896_916_649
U64 = 1 << 64

C3 = 6_883_890_832_452_974_229_163
C15Q = 181_155_021_906_657_216_557
C47Q = 31_008_517_263_301_685_717

LUCAS = {
    P: (17, {2: 3, 3: 4, 7: 1, 13: 1, 1873: 1, 3671: 1, 175727: 1, 386471: 1}),
    C3: (2, {2: 1, 3: 4, 7: 1, 13: 1, 1873: 1, 3671: 1, 175727: 1, 386471: 1}),
    C15Q: (2, {2: 2, 73: 1, 3329: 1, 186360441766067: 1}),
    C47Q: (2, {2: 2, 7: 1, 31: 1, 43: 1, 53: 1, 15675339284603: 1}),
}

F = {
    3: {C3: 1},
    7: {2: 2, 11: 1, 53: 1, 277: 1, 27486439: 1, 387710159: 1},
    11: {3: 1, 5: 1, 223: 1, 2057964374425403357: 1},
    15: {2: 1, 19: 1, C15Q: 1},
    19: {23: 1, 43: 1, 47: 1, 6139547: 1, 24121454767: 1},
    23: {2: 4, 3: 1, 112486999: 1, 1274941936559: 1},
    27: {7: 1, 17: 1, 31: 1, 1866058778111405321: 1},
    31: {2: 1, 5: 1, 41: 1, 122117: 1, 137490911503961: 1},
    35: {3: 2, 139: 1, 1181: 1, 4659365366269541: 1},
    47: {2: 1, 3: 1, 37: 1, C47Q: 1},
    167: {2: 2, 3: 1, 7: 1, 19: 2, 61: 1, 3721496813892461: 1},
    195: {7: 1, 37: 2, 41: 2, 12113: 1, 13763: 1, 2563303: 1},
}


def prod(f: dict[int, int]) -> int:
    out = 1
    for q, e in f.items():
        out *= q**e
    return out


def mr(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    assert n < U64
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
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


def certify(n: int, cache: dict[int, bool]) -> bool:
    if n in cache:
        return cache[n]
    if n < U64:
        cache[n] = mr(n)
        return cache[n]
    a, fac = LUCAS[n]
    assert prod(fac) == n - 1
    assert all(certify(q, cache) for q in fac)
    assert pow(a, n - 1, n) == 1
    assert all(math.gcd(pow(a, (n - 1) // q, n) - 1, n) == 1 for q in fac)
    cache[n] = True
    return True


def C(k: int) -> int:
    return (P + k) // 4


def residues(fac: dict[int, int], k: int) -> set[int]:
    out = {1 % k}
    for q, e in fac.items():
        out = {x * pow(q, a, k) % k for x in out for a in range(2 * e + 1)}
    return out


def targets(k: int) -> tuple[int, int]:
    return (-pow(4, -1, k)) % k, (-C(k)) % k


def leg(a: int, p: int) -> int:
    r = pow(a % p, (p - 1) // 2, p)
    return 1 if r == 1 else -1 if r == p - 1 else 0


def classify_type2_roots() -> tuple[list[dict[str, object]], collections.Counter[str]]:
    k = 35
    fac = F[k]
    items = list(fac.items())
    _, target = targets(k)
    roots = []
    counts: collections.Counter[str] = collections.Counter()
    for exps in itertools.product(*[range(2 * e + 1) for _, e in items]):
        d = 1
        for (q, _), a in zip(items, exps):
            d *= q**a
        if d % k != target:
            continue
        s = b = c = 1
        for (q, eC), a in zip(items, exps):
            parity = a % 2
            if parity:
                s *= q
            b *= q ** (a // 2)
            c *= q ** ((2 * eC - a - parity) // 2)
        assert d == s * b * b
        assert C(k) == s * b * c
        if c % b == 0:
            geom = "A"
        elif b % c == 0:
            geom = "B"
        else:
            geom = "interior"
        counts[geom] += 1
        roots.append({"d": d, "s": s, "b": b, "c": c, "geometry": geom})
    return roots, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    assert S % 361 == 312
    assert T == T0 + DT * S
    assert P == 169 + 840 * T
    assert P % 840 == 169

    cache: dict[int, bool] = {}
    assert certify(P, cache)
    for k, fac in F.items():
        assert prod(fac) == C(k), (k, prod(fac), C(k))
        assert all(certify(q, cache) for q in fac), (k, fac)

    phases = {m: T % m for m in (9, 11, 13, 17, 19, 23, 31, 43, 47)}
    assert phases == {9: 7, 11: 0, 13: 5, 17: 6, 19: 11, 23: 15, 31: 7, 43: 18, 47: 0}

    expected_masks = {
        3: {1},
        7: {1, 2, 4},
        11: {1, 3, 4, 5, 9},
        15: {1, 2, 4, 8},
        19: {1, 4, 5, 6, 7, 9, 11, 16, 17},
        23: {1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18},
        27: {1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 22, 23, 25, 26},
        31: {1, 2, 4, 5, 7, 8, 9, 10, 14, 16, 18, 19, 20, 25, 28},
    }
    ancestry = []
    for k in (3, 7, 11, 15, 19, 23, 27, 31):
        mask = residues(F[k], k)
        assert mask == expected_masks[k]
        tI, tII = targets(k)
        assert tI not in mask and tII not in mask
        ancestry.append({"k": k, "status": "MISS", "mask_size": len(mask)})

    # k15 q19 source and k167 square lift.
    assert F[15].get(19) == 1
    assert leg(19, 15) == 1
    assert leg(P, 19) == 1  # reciprocity because P=1 mod4
    assert F[167].get(19) == 2

    # Route-B support through k31.
    R = {43: 1, 6139547: 1, 24121454767: 1}
    assert prod(R) * 23 * 47 == C(19)
    assert all(leg(q, 19) == 1 for q in R)
    assert any(q % 19 != 1 for q in R)

    B = {2: 3, 112486999: 1, 1274941936559: 1}
    assert prod(B) * 6 == C(23)
    assert all(leg(q, 23) == 1 for q in B)

    r27 = 1866058778111405321
    assert C(27) == 7 * 17 * 31 * r27
    assert r27 % 27 == 2

    D = {41: 1, 122117: 1, 137490911503961: 1}
    assert prod(D) * 10 == C(31)
    assert all(leg(q, 31) == 1 for q in D)
    assert 41 % 31 == 10
    assert 10 not in {1, 5, 25}

    J = {37: 1, C47Q: 1}
    assert prod(J) * 6 == C(47)
    assert all(leg(q, 47) == 1 for q in J)
    assert F[195].get(37) == 2 and F[195].get(41) == 2

    # First hit at k35, with explicit divisor witnesses.
    k = 35
    mask35 = residues(F[k], k)
    tI, tII = targets(k)
    assert (C(k) % k, tI, tII) == (16, 26, 19)
    dI = 1181
    dII = 15_703_614_099
    assert C(k) * C(k) % dI == 0 and dI % k == tI
    assert C(k) * C(k) % dII == 0 and dII % k == tII
    assert tI in mask35 and tII in mask35
    ancestry.append({"k": 35, "status": "HIT", "type_I": True, "type_II": True})

    roots, geometry = classify_type2_roots()
    assert len(roots) == 6
    assert geometry == collections.Counter({"interior": 4, "A": 1, "B": 1})
    smallest = min(roots, key=lambda row: int(row["d"]))
    assert smallest == {
        "d": dII,
        "s": 139,
        "b": 10629,
        "c": 4659365366269541,
        "geometry": "interior",
    }
    assert smallest["c"] % smallest["b"] != 0
    assert smallest["b"] % smallest["c"] != 0

    report = {
        "analysis": "k195-k35-ancestry-anchor-v1",
        "s": S,
        "t": T,
        "p": P,
        "prime_certificate": "Lucas complete factorization of p-1",
        "phases": phases,
        "ancestry": ancestry,
        "q19": {"v19_C15": 1, "v19_C167": 2, "positive_target_character": True},
        "d_selector": {
            "k19": "FULL_QR",
            "k23": "QR support",
            "k27": {"mode": "D", "r": r27, "r_mod27": 2},
            "k31": "FULL_QR with q41",
            "later_q37_in_C47": True,
            "k195_double_square": {"v37": 2, "v41": 2},
        },
        "k35": {
            "type_I_witness": dI,
            "type_II_witness": dII,
            "type_II_geometry_counts": dict(geometry),
            "smallest_type_II_root": smallest,
        },
        "failures": 0,
        "claim": (
            "the certified prime survives exact signed boxes k3 through k31 on the q19-square and q41/q37 double-square corridor, "
            "then first hits at k35 with both Type-I and mixed Type-II geometry including four incomparable interior roots"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
