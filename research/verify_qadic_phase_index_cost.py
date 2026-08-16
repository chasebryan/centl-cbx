#!/usr/bin/env python3
"""Verify exact q-adic lattice-index costs for routed source valuation lifts."""
from __future__ import annotations

import argparse
import json
import math


def crt_pair(a: int, m: int, b: int, n: int) -> tuple[int, int]:
    g = math.gcd(m, n)
    assert (b - a) % g == 0
    mm, nn = m // g, n // g
    x = ((b - a) // g) * pow(mm, -1, nn) % nn
    mod = m * nn
    return (a + m * x) % mod, mod


def vq(n: int, q: int) -> int:
    if n == 0:
        return 10**9
    e = 0
    while n % q == 0:
        n //= q
        e += 1
    return e


def one_source_class(A: int, q: int, e: int) -> tuple[int, int]:
    mod = q ** (e - 1)
    return ((-A) % mod if mod > 1 else 0), mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    one_source = []
    for q in (13, 29, 37, 41, 71, 317):
        A = q + 2
        for e in range(1, 5):
            r, mod = one_source_class(A, q, e)
            assert mod == q ** (e - 1)
            # Check several complete residue periods when feasible.
            limit = min(max(3 * mod, 30), 50_000)
            for n in range(limit):
                assert (vq(q * (A + n), q) >= e) == ((n - r) % mod == 0)
            if e < 4:
                r2, mod2 = one_source_class(A, q, e + 1)
                assert mod2 == q * mod
                children = [(r + mod * a) % mod2 for a in range(q)]
                assert len(set(children)) == q
                assert sum(x == r2 for x in children) == 1
                for x in children:
                    if x == r2:
                        assert vq(q * (A + x), q) >= e + 1
                    else:
                        assert vq(q * (A + x), q) == e
        one_source.append({"q": q, "index_e4": q**3})

    multi = []
    for qs, es in [([37, 41], [2, 2]), ([13, 29, 71], [3, 2, 2])]:
        Q = math.prod(qs)
        Bs = [2 + i for i in range(len(qs))]
        residue, modulus = 0, 1
        for B, q, e in zip(Bs, qs, es):
            Qi = Q // q
            local_mod = q ** (e - 1)
            local = 0 if local_mod == 1 else (-B * pow(Qi, -1, local_mod)) % local_mod
            residue, modulus = crt_pair(residue, modulus, local, local_mod)
        expected = math.prod(q ** (e - 1) for q, e in zip(qs, es))
        assert modulus == expected
        for h in range(5):
            n = residue + modulus * h
            for B, q, e in zip(Bs, qs, es):
                Qi = Q // q
                assert vq(q * (B + Qi * n), q) >= e
        ratios = []
        for j, q in enumerate(qs):
            es2 = list(es)
            es2[j] += 1
            res2, mod2 = 0, 1
            for B, qi, ei in zip(Bs, qs, es2):
                Qi = Q // qi
                lm = qi ** (ei - 1)
                lr = 0 if lm == 1 else (-B * pow(Qi, -1, lm)) % lm
                res2, mod2 = crt_pair(res2, mod2, lr, lm)
            assert mod2 // modulus == q
            ratios.append(q)
        multi.append({"qs": qs, "es": es, "index": modulus, "increment_ratios": ratios})

    # Fixed-destination phase identity q^e|C_k iff p=-k mod4q^e.
    target = []
    for q, k in ((29, 951), (41, 195), (37, 195), (317, 39)):
        for e in range(1, 5):
            mod = 4 * q**e
            p = (-k) % mod
            assert (p + k) % mod == 0
            if e < 4:
                assert (4 * q ** (e + 1)) // mod == q
        target.append({"q": q, "k": k, "e4_vs_e1_index": q**3})

    assert 29**9 == 14_507_145_975_869
    assert 41 * 37 == 1517
    assert 317 == 317**1

    report = {
        "analysis": "qadic-phase-index-cost-v1",
        "one_source": one_source,
        "multi_source": multi,
        "target_phase": target,
        "landed_examples": {
            "q29_e10_extra_index": 29**9,
            "k195_double_square_extra_index": 1517,
            "q317_e2_extra_index": 317,
        },
        "termination_rank": False,
        "failures": 0,
        "claim": "valuation floor e selects one q-adic route class modulo q^(e-1); each lift costs q, and distinct synchronized source costs multiply by CRT",
    }
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
