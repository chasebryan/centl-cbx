#!/usr/bin/env python3
"""Verify exact k3/k7/k11 survivor grammar for the k195 double-square corridor."""
from __future__ import annotations

import argparse
import collections
import json
import math
from collections import deque
from fractions import Fraction

T_BASE = 7_423_185_617_863
T_STEP = 11_799_129_838_887
PERIOD = 19 * 13 * 43 * 11

S19_D = frozenset({0, 2, 7, 11, 14, 15, 16, 17})
S13 = frozenset({1, 2, 5, 6, 7, 8, 9, 10, 11})
S43 = frozenset(set(range(43)) - {2, 28, 30})
S11_PRE = frozenset({0, 2, 3, 4, 8, 9})
S11_POST_K11 = frozenset({0, 2, 3, 4, 8})

QR7 = frozenset({1, 2, 4})
QR11 = frozenset({1, 3, 4, 5, 9})

EXPECTED_K11 = {
    0: {
        frozenset({1}),
        frozenset({1, 2, 3, 4, 6}),
        QR11,
    },
    2: {
        frozenset({1, 3, 9}),
        QR11,
        frozenset({1, 3, 6, 7, 9}),
        frozenset({1, 2, 3, 4, 5, 6, 7, 9, 10}),
    },
    3: {
        frozenset({1, 4, 5}),
        QR11,
    },
    4: {
        frozenset({1, 3, 5}),
        frozenset({1, 2, 3, 5, 7}),
        QR11,
    },
    8: {
        frozenset({1, 4, 9}),
        QR11,
    },
    9: set(),
}


def t_of_s(s: int) -> int:
    return T_BASE + T_STEP * s


def transition(mask: frozenset[int], center: int, r: int, k: int) -> tuple[frozenset[int], int]:
    local = {1, r % k, (r * r) % k}
    return (
        frozenset((x * y) % k for x in mask for y in local),
        center * r % k,
    )


def full_closure(k: int) -> set[tuple[frozenset[int], int]]:
    units = tuple(r for r in range(1, k) if math.gcd(r, k) == 1)
    start = (frozenset({1}), 1)
    q = deque([start])
    seen = {start}
    while q:
        mask, center = q.popleft()
        for r in units:
            nxt = transition(mask, center, r, k)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen


def miss_masks(k: int, final_center: int, type_i: int, type_ii: int) -> set[frozenset[int]]:
    return {
        mask for mask, center in full_closure(k)
        if center == final_center and type_i not in mask and type_ii not in mask
    }


def verify_k3() -> dict[str, object]:
    closure = full_closure(3)
    misses = miss_masks(3, final_center=1, type_i=2, type_ii=2)
    assert misses == {frozenset({1})}

    # Direct iff over arbitrary prime-factor residue occurrences collapses to:
    # all residues 1 => mask {1}; any residue2 contributes target2 itself.
    for n2 in range(8):
        seq = [2] * n2
        mask, center = frozenset({1}), 1
        for r in seq:
            mask, center = transition(mask, center, r, 3)
        if center == 1:
            assert (2 not in mask) == (n2 == 0)
    return {"closure_states": len(closure), "miss_masks": [sorted(x) for x in misses]}


def verify_k7() -> dict[str, object]:
    closure = full_closure(7)
    misses = miss_masks(7, final_center=2, type_i=5, type_ii=5)
    expected = {
        QR7,
        frozenset({1, 2, 3, 4, 6}),
    }
    assert len(closure) == 17
    assert misses == expected

    # Product automaton proves the factor-occurrence grammar, not just endpoint masks.
    # qr_only tracks the all-QR sector. thin_count tracks whether the sequence after
    # deleting residue1 is exactly two residue3 occurrences; -1 means impossible.
    units = tuple(range(1, 7))
    start = (frozenset({1}), 1, True, 0)
    q = deque([start])
    seen = {start}
    bad_miss_paths = []
    valid_miss_classes = collections.Counter()
    while q:
        mask, center, qr_only, thin_count = q.popleft()
        if center == 2 and 5 not in mask:
            valid = qr_only or thin_count == 2
            if not valid:
                bad_miss_paths.append((mask, center, qr_only, thin_count))
            valid_miss_classes["QR7" if qr_only else "THIN_33"] += 1
        for r in units:
            nmask, ncenter = transition(mask, center, r, 7)
            n_qr_only = qr_only and r in QR7
            if thin_count == -1:
                n_thin = -1
            elif r == 1:
                n_thin = thin_count
            elif r == 3 and thin_count < 2:
                n_thin = thin_count + 1
            else:
                n_thin = -1
            nxt = (nmask, ncenter, n_qr_only, n_thin)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    assert not bad_miss_paths, bad_miss_paths
    assert set(valid_miss_classes) == {"QR7", "THIN_33"}

    return {
        "closure_states": len(closure),
        "miss_masks": [sorted(x) for x in sorted(misses, key=lambda m: (len(m), sorted(m)))],
        "factor_grammars": ["QR7", "THIN_33"],
        "product_automaton_states": len(seen),
    }


def verify_k11() -> dict[str, object]:
    closure = full_closure(11)
    assert len(closure) == 59
    rows = {}
    total = 0
    unique_masks = set()
    for tau in sorted(S11_PRE):
        center = (tau + 1) % 11
        type_i = 8
        type_ii = (-center) % 11
        got = miss_masks(11, center, type_i, type_ii)
        assert got == EXPECTED_K11[tau], (tau, got, EXPECTED_K11[tau])
        total += len(got)
        unique_masks |= got
        rows[tau] = {
            "center": center,
            "type_ii": type_ii,
            "miss_count": len(got),
            "masks": [sorted(x) for x in sorted(got, key=lambda m: (len(m), sorted(m)))],
        }

    assert total == 14
    assert len(unique_masks) == 10
    assert EXPECTED_K11[9] == set()
    for tau in S11_POST_K11:
        assert QR11 in EXPECTED_K11[tau]

    return {
        "closure_states": len(closure),
        "center_labelled_miss_states": total,
        "distinct_miss_masks": len(unique_masks),
        "tau11_9_universal_hit": True,
        "atlas": rows,
    }


def verify_companion_ladder() -> dict[str, object]:
    for t in range(2 * 3 * 5 * 7 * 11):
        c3 = 43 + 210 * t
        c7 = 44 + 210 * t
        c11 = 45 + 210 * t
        assert c7 == c3 + 1
        assert c11 == c3 + 2
        assert c3 % 2 == 1
        assert math.gcd(c3, c7) == 1
        assert math.gcd(c7, c11) == 1
        assert math.gcd(c3, c11) == 1
    return {"pairwise_coprime": True, "shape": "X,X+1,X+2 with X odd"}


def verify_phase_contraction() -> dict[str, object]:
    pre = 0
    post = 0
    forced_hit = 0
    miss_compat = 0
    for s in range(PERIOD):
        t = t_of_s(s)
        base_ok = (
            t % 19 in S19_D
            and t % 13 in S13
            and t % 43 in S43
        )
        if base_ok and t % 11 in S11_PRE:
            pre += 1
        if base_ok and t % 11 in S11_POST_K11:
            post += 1
            if t % 13 in {1, 9, 10}:
                forced_hit += 1
            else:
                miss_compat += 1
    assert pre == 17_280
    assert post == 14_400
    assert forced_hit == 4_800
    assert miss_compat == 9_600
    frac = Fraction(post, PERIOD)
    return {
        "pre_k11_phase_classes": pre,
        "post_k11_phase_classes": post,
        "surviving_fraction": f"{frac.numerator}/{frac.denominator}",
        "surviving_decimal": float(frac),
        "eliminated_decimal": float(1 - frac),
        "if_reaches_k195_forced_hit": forced_hit,
        "if_reaches_k195_miss_compatible": miss_compat,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = {
        "analysis": "k195-early-ancestry-survivor-grammar-v1",
        "companion_ladder": verify_companion_ladder(),
        "k3": verify_k3(),
        "k7": verify_k7(),
        "k11": verify_k11(),
        "phase_contraction": verify_phase_contraction(),
        "normalized_state": {
            "C3_support": "all prime factors 1 mod3",
            "C7_mode": ["QR7", "THIN_33"],
            "tau11": sorted(S11_POST_K11),
            "k11_endpoint_states": 14,
            "early_support_reservoirs": "pairwise coprime",
        },
        "claim_boundary": (
            "exact local miss grammars and endpoint atlas only; joint arithmetic realizability of the formal early-state product remains open"
        ),
        "failures": 0,
    }
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
