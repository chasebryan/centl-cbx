#!/usr/bin/env python3
"""Verify the exact h169 k15 Route-B source-renewal coupling."""
from __future__ import annotations

import argparse
import json
import math
from collections import deque

HJ = frozenset({1, 2, 4, 8})
TARGETS = {11, 14}


def legendre(a: int, p: int) -> int:
    r = pow(a % p, (p - 1) // 2, p)
    return 1 if r == 1 else -1 if r == p - 1 else 0


def jacobi15(a: int) -> int:
    return legendre(a, 3) * legendre(a, 5)


def transition(mask: frozenset[int], center: int, r: int) -> tuple[frozenset[int], int]:
    local = {1, r % 15, (r * r) % 15}
    return frozenset((x * y) % 15 for x in mask for y in local), center * r % 15


def mandatory_two_closure() -> set[tuple[frozenset[int], int]]:
    start = transition(frozenset({1}), 1, 2)
    units = [r for r in range(1, 15) if math.gcd(r, 15) == 1]
    seen = {start}
    q = deque([start])
    while q:
        state = q.popleft()
        for r in units:
            nxt = transition(*state, r)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # h169 C15 has a mandatory factor2 and fixed center1 modulo15.
    for t in range(0, 15 * 23 * 47, 137):
        c15 = 46 + 210 * t
        assert c15 % 2 == 0
        assert c15 % 15 == 1
        assert math.gcd(c15, 15) == 1

    seen = mandatory_two_closure()
    misses = {
        mask for mask, center in seen
        if center == 1 and TARGETS.isdisjoint(mask)
    }
    assert len(seen) == 19
    assert misses == {HJ}
    assert all(jacobi15(r) == 1 for r in HJ)
    assert {r for r in range(1, 15) if math.gcd(r, 15) == 1 and jacobi15(r) == 1} == set(HJ)

    # Route-B t=705+1081u makes C19=23*47*R. Check the exact adjacent residue transfer.
    for u in range(23 * 47):
        t = 705 + 1081 * u
        c15 = 46 + 210 * t
        c19 = 47 + 210 * t
        assert c19 == c15 + 1
        assert c19 % (23 * 47) == 0
        assert c15 % 23 == 22
        assert c15 % 47 == 46

    assert legendre(-1, 23) == -1
    assert legendre(-1, 47) == -1
    assert legendre(2, 23) == 1
    assert legendre(2, 47) == 1

    # Freshness: an odd q|C15 shared with a later named companion must divide
    # the offset. None of the only possible odd offset primes can divide C15.
    offsets = {19: 1, 23: 2, 27: 3, 31: 4, 47: 8}
    for t in range(0, 3 * 5 * 8):
        c15 = 46 + 210 * t
        assert c15 % 3 != 0 and c15 % 5 != 0
        for k, delta in offsets.items():
            ck = c15 + delta
            g = math.gcd(c15, ck)
            # Any common odd factor would divide delta. Here every gcd is a power of2.
            odd = g
            while odd % 2 == 0:
                odd //= 2
            assert odd == 1, (t, k, g)

    # Orientation conversion is exact for any odd prime q|C15 because origin15=3 mod4.
    # Exhaust representative odd primes and h169 primes where q actually divides C15.
    orientation_examples = 0
    for p in range(169, 200_000, 840):
        if p < 2:
            continue
        # primality not required for the divisibility scan; only use p values that
        # are prime under a simple exact trial test.
        if any(p % d == 0 for d in range(2, int(math.isqrt(p)) + 1)):
            continue
        c15 = (p + 15) // 4
        for q in range(3, int(math.isqrt(c15)) + 1, 2):
            if c15 % q:
                continue
            if any(q % d == 0 for d in range(2, int(math.isqrt(q)) + 1)):
                continue
            if math.gcd(q, 15) != 1:
                continue
            assert legendre(q, p) == jacobi15(q)
            orientation_examples += 1
    assert orientation_examples > 0

    report = {
        "analysis": "k15-route-b-source-renewal-v1",
        "mandatory_two_closure_states": len(seen),
        "unique_k15_miss_mask": sorted(HJ),
        "h169_k15_mode": "J15_ONLY",
        "route_b_transfer": {
            "C15_mod23": -1,
            "C15_mod47": -1,
            "2_char_mod23": 1,
            "2_char_mod47": 1,
        },
        "forced_obligations": [
            "exists odd a|C15 with (a/p)=+1 and (a/23)=-1",
            "exists odd b|C15 with (b/p)=+1 and (b/47)=-1",
        ],
        "witness_distinctness": "not forced; one prime may satisfy both negative characters",
        "fresh_from_R_B_E_D_J": True,
        "orientation_examples_checked": orientation_examples,
        "failures": 0,
    }
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
