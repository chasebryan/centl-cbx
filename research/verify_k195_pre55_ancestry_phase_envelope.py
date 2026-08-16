#!/usr/bin/env python3
"""Verify exact pre-55 phase ancestry envelope for the k195 double-square corridor."""
from __future__ import annotations

import argparse
import json
from fractions import Fraction

T_BASE = 7_423_185_617_863
T_STEP = 11_799_129_838_887
PERIOD = 19 * 13 * 43 * 11

S19_D = frozenset({0, 2, 7, 11, 14, 15, 16, 17})
S13 = frozenset({1, 2, 5, 6, 7, 8, 9, 10, 11})
S43 = frozenset(set(range(43)) - {2, 28, 30})
S11 = frozenset({0, 2, 3, 4, 8, 9})
K195_FORCED_HIT_13 = frozenset({1, 9, 10})
K195_MISS_COMPAT_13 = frozenset({2, 5, 6, 7, 8, 11})


def t_of_s(s: int) -> int:
    return T_BASE + T_STEP * s


def phase_ok(t: int) -> bool:
    return (
        t % 19 in S19_D
        and t % 13 in S13
        and t % 43 in S43
        and t % 11 in S11
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # Reconstruct from landed k195 progression constants.
    assert T_BASE == 3_925_816 + 5_127_183 * 1_447_809
    assert T_STEP == 5_127_183 * 2_301_289

    # Frozen D-selector / Route-B coordinates.
    frozen = {m: T_BASE % m for m in (9, 17, 23, 31, 47)}
    assert frozen == {9: 7, 17: 6, 23: 15, 31: 7, 47: 0}
    for s in range(100):
        t = t_of_s(s)
        assert {m: t % m for m in frozen} == frozen

    # Moving affine coordinates.
    affine = {
        19: (T_BASE % 19, T_STEP % 19),
        13: (T_BASE % 13, T_STEP % 13),
        43: (T_BASE % 43, T_STEP % 43),
        11: (T_BASE % 11, T_STEP % 11),
    }
    assert affine == {19: (10, 12), 13: (2, 1), 43: (10, 9), 11: (4, 6)}

    # Each moving coefficient is invertible, hence a permutation of its residue field.
    for m, (_a, b) in affine.items():
        assert sorted((b * s) % m for s in range(m)) == list(range(m))

    assert PERIOD == 116_831
    alive = []
    forced_hit = 0
    miss_compatible = 0
    for s in range(PERIOD):
        t = t_of_s(s)
        if not phase_ok(t):
            continue
        alive.append(s)
        tau13 = t % 13
        if tau13 in K195_FORCED_HIT_13:
            forced_hit += 1
        elif tau13 in K195_MISS_COMPAT_13:
            miss_compatible += 1
        else:
            raise AssertionError(tau13)

    assert len(alive) == 17_280
    assert forced_hit == 5_760
    assert miss_compatible == 11_520
    assert len(alive) == len(S19_D) * len(S13) * len(S43) * len(S11)

    # Corrected phase-only witness. The original k195 PR's s=5 witness had tau11=1,
    # which newer Route-B k47 feedback proves cannot reach past k47.
    stale_t = t_of_s(5)
    assert stale_t % 11 == 1
    assert not phase_ok(stale_t)

    witness_s = 8
    witness_t = t_of_s(witness_s)
    witness = {
        19: witness_t % 19,
        13: witness_t % 13,
        43: witness_t % 43,
        11: witness_t % 11,
    }
    assert witness == {19: 11, 13: 10, 43: 39, 11: 8}
    assert phase_ok(witness_t)
    assert witness[13] in K195_FORCED_HIT_13

    surviving = Fraction(len(alive), PERIOD)
    eliminated = 1 - surviving
    assert surviving == Fraction(17_280, 116_831)
    assert eliminated == Fraction(99_551, 116_831)

    report = {
        "analysis": "k195-pre55-ancestry-phase-envelope-v1",
        "corridor": {"t_base": T_BASE, "t_step": T_STEP},
        "frozen": {f"tau{m}": r for m, r in frozen.items()},
        "moving_affine": {
            f"tau{m}": f"{aa}+{bb}*s mod{m}" for m, (aa, bb) in affine.items()
        },
        "phase_sets": {
            "tau19": sorted(S19_D),
            "tau13": sorted(S13),
            "tau43_count": len(S43),
            "tau11": sorted(S11),
        },
        "exact_period": PERIOD,
        "surviving_classes": len(alive),
        "surviving_fraction": f"{surviving.numerator}/{surviving.denominator}",
        "surviving_decimal": float(surviving),
        "eliminated_classes": PERIOD - len(alive),
        "eliminated_fraction": f"{eliminated.numerator}/{eliminated.denominator}",
        "eliminated_decimal": float(eliminated),
        "k195_if_reached": {
            "forced_hit_classes": forced_hit,
            "miss_compatible_classes": miss_compatible,
        },
        "stale_phase_witness_s5_tau11": stale_t % 11,
        "corrected_phase_witness": {"s": witness_s, **{f"tau{m}": r for m, r in witness.items()}},
        "full_signed_box_reachability": "not proved by this phase module",
        "failures": 0,
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
