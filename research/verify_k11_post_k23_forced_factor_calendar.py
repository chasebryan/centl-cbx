#!/usr/bin/env python3
"""Verify the exact k11-conditioned post-k23 forced-factor calendar.

For a Mordell-hard prime write T=(p+23)/24.  The post-k23 companion ladder is

    C_{23+4j} = 6*T + j,  j>=0.

The exact k11 combined-miss grammar constrains T modulo 11:

  pure-QR branch                 -> T in {1,2,3,5,8} mod11
  thin packet (a2,a6)=(1,0)    -> T = 7 mod11
  thin packet (a2,a6)=(0,1)    -> T = 9 mod11
  thin packet (a2,a6)=(1,1)    -> T = 1 mod11.

Therefore every k11 combined miss has

    T mod11 in {1,2,3,5,7,8,9}.

For each phase there is a unique j mod11 with 11 | (6T+j).  Choosing the
first positive representative gives

  T11  9  7  5  3  1  8  2
  j    1  2  3  4  5  7 10
  k   27 31 35 39 43 51 63.

Thus a k11 miss forces literal factor 11 into the post-k23 ladder no later
than k=63.

Hard classes also fix T mod35, hence deterministic factor-5/factor-7 calendar
entries.  This verifier combines the mod35 and mod11 information by CRT modulo
385 and freezes all exact small-prime injections through j=10.
"""

from __future__ import annotations

import json
from typing import Any

HARD_TO_T35 = {
    1: 1,
    121: 6,
    169: 8,
    289: 13,
    361: 16,
    529: 23,
}

PURE_T11 = {1, 2, 3, 5, 8}
THIN_PACKET_TO_T11 = {
    (1, 0): 7,
    (0, 1): 9,
    (1, 1): 1,
}
GENERAL_MISS_T11 = PURE_T11 | set(THIN_PACKET_TO_T11.values())
COLLAPSED_HARD = {169, 289, 529}

EXPECTED_J11 = {
    9: 1,
    7: 2,
    5: 3,
    3: 4,
    1: 5,
    8: 7,
    2: 10,
}

EXPECTED_HARD_5_7 = {
    1: {5: 4, 7: 1},
    121: {5: 4, 7: 6},
    169: {5: 2, 7: 1},
    289: {5: 2, 7: 6},
    361: {5: 4, 7: 2},
    529: {5: 2, 7: 2},
}


def inv(a: int, m: int) -> int:
    return pow(a, -1, m)


def t11_from_residual(residual_mod11: int) -> int:
    return ((residual_mod11 + 1) * inv(2, 11)) % 11


def derive_k11_phases() -> dict[str, Any]:
    qr11 = {1, 3, 4, 5, 9}
    pure = {t11_from_residual(r) for r in qr11}
    if pure != PURE_T11:
        raise SystemExit(f"pure q11 T phases changed: {sorted(pure)}")

    thin = {}
    for packet in ((1, 0), (0, 1), (1, 1)):
        a2, a6 = packet
        residual = pow(2, a2, 11) * pow(6, a6, 11) % 11
        phase = t11_from_residual(residual)
        thin[packet] = phase
    if thin != THIN_PACKET_TO_T11:
        raise SystemExit(f"thin q11 T phases changed: {thin}")

    if pure | set(thin.values()) != GENERAL_MISS_T11:
        raise SystemExit("general k11 miss phase union changed")

    return {
        "pure_QR_T_mod_11": sorted(pure),
        "thin_packets": [
            {"a2": a2, "a6": a6, "T_mod_11": phase}
            for (a2, a6), phase in sorted(thin.items())
        ],
        "combined_miss_T_mod_11": sorted(GENERAL_MISS_T11),
    }


def first_positive_factor_step(t_mod: int, prime: int) -> int:
    for j in range(1, prime + 1):
        if (6 * t_mod + j) % prime == 0:
            return j
    raise RuntimeError("factor step not found")


def verify_factor11_calendar() -> list[dict[str, int]]:
    rows = []
    for t11 in sorted(GENERAL_MISS_T11):
        j = first_positive_factor_step(t11, 11)
        expected = EXPECTED_J11[t11]
        if j != expected:
            raise SystemExit(f"T11={t11}: factor11 j={j} != {expected}")
        rows.append(
            {
                "T_mod_11": t11,
                "first_positive_j_with_11_dividing_companion": j,
                "shift_k": 23 + 4 * j,
            }
        )
    if max(row["shift_k"] for row in rows) != 63:
        raise SystemExit("k11 miss factor11 calendar no longer closes by k63")
    return rows


def crt35_11(t35: int, t11: int) -> int:
    for t in range(t35, 35 * 11, 35):
        if t % 11 == t11:
            return t
    # t35 itself may be zero in a generic call, although not in hard classes.
    for t in range(t35 % 35, 35 * 11, 35):
        if t % 11 == t11:
            return t
    raise RuntimeError("CRT(35,11) failed")


def hard_phase_rows() -> list[dict[str, Any]]:
    rows = []
    for hard, t35 in HARD_TO_T35.items():
        phases = PURE_T11 if hard in COLLAPSED_HARD else GENERAL_MISS_T11

        j5 = first_positive_factor_step(t35 % 5, 5)
        j7 = first_positive_factor_step(t35 % 7, 7)
        if {5: j5, 7: j7} != EXPECTED_HARD_5_7[hard]:
            raise SystemExit(
                f"hard={hard}: factor5/7 calendar changed: j5={j5}, j7={j7}"
            )

        for t11 in sorted(phases):
            t385 = crt35_11(t35, t11)
            if t385 % 35 != t35 or t385 % 11 != t11:
                raise SystemExit("CRT phase mismatch")

            injections = []
            for j in range(1, 11):
                forced = [
                    prime
                    for prime in (5, 7, 11)
                    if (6 * t385 + j) % prime == 0
                ]
                if forced:
                    injections.append(
                        {
                            "j": j,
                            "k": 23 + 4 * j,
                            "forced_primes": forced,
                            "forced_product": __import__("math").prod(forced),
                        }
                    )

            j11 = EXPECTED_J11[t11]
            if not any(
                entry["j"] == j11 and 11 in entry["forced_primes"]
                for entry in injections
            ):
                raise SystemExit(
                    f"hard={hard}, T11={t11}: missing forced factor11 entry"
                )
            if not any(
                entry["j"] == j5 and 5 in entry["forced_primes"]
                for entry in injections
            ):
                raise SystemExit(f"hard={hard}: missing factor5 entry")
            if not any(
                entry["j"] == j7 and 7 in entry["forced_primes"]
                for entry in injections
            ):
                raise SystemExit(f"hard={hard}: missing factor7 entry")

            rows.append(
                {
                    "p_mod_840": hard,
                    "T_mod_35": t35,
                    "T_mod_11": t11,
                    "T_mod_385": t385,
                    "k11_branch_domain": (
                        "pure-QR-only" if hard in COLLAPSED_HARD else "general-miss"
                    ),
                    "first_j_factor5": j5,
                    "first_j_factor7": j7,
                    "first_j_factor11": j11,
                    "injections_through_j10": injections,
                }
            )
    return rows


def coincidence_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = []
    for row in rows:
        for entry in row["injections_through_j10"]:
            if len(entry["forced_primes"]) >= 2:
                summary.append(
                    {
                        "p_mod_840": row["p_mod_840"],
                        "T_mod_11": row["T_mod_11"],
                        **entry,
                    }
                )
    return summary


def verify() -> dict[str, Any]:
    phases = derive_k11_phases()
    factor11 = verify_factor11_calendar()
    rows = hard_phase_rows()
    coincidences = coincidence_summary(rows)

    # Exact headline coincidences useful for the post-k23 absorber program.
    wanted = {
        (529, t11, 2, (5, 7))
        for t11 in PURE_T11
    }
    observed_529 = {
        (
            row["p_mod_840"],
            row["T_mod_11"],
            row["j"],
            tuple(row["forced_primes"]),
        )
        for row in coincidences
        if row["p_mod_840"] == 529 and row["j"] == 2
    }
    if not wanted.issubset(observed_529):
        raise SystemExit("h529 no longer forces 5*7 at k31 on every allowed phase")

    # Thin packet (0,1) => T11=9 => 11 enters at k27; in h1 the hard class
    # independently forces 7 at that same step.
    if not any(
        row["p_mod_840"] == 1
        and row["T_mod_11"] == 9
        and row["j"] == 1
        and row["forced_primes"] == [7, 11]
        for row in coincidences
    ):
        raise SystemExit("h1 / thin(0,1) no longer forces 7*11 at k27")

    # Thin packet (1,0) => T11=7 => 11 enters at k31; h361 forces 7 there.
    if not any(
        row["p_mod_840"] == 361
        and row["T_mod_11"] == 7
        and row["j"] == 2
        and row["forced_primes"] == [7, 11]
        for row in coincidences
    ):
        raise SystemExit("h361 / thin(1,0) no longer forces 7*11 at k31")

    return {
        "verified": True,
        "mode": "k11-post-k23-forced-factor-calendar",
        "k11_phase_grammar": phases,
        "factor11_calendar": factor11,
        "universal_k11_miss_consequence": (
            "Every k11 combined miss forces literal factor11 into some post-k23 "
            "companion C_{23+4j} with j in {1,2,3,4,5,7,10}, hence no later "
            "than k=63."
        ),
        "hard_class_factor5_7_calendar": [
            {
                "p_mod_840": hard,
                "T_mod_35": t35,
                "j5": EXPECTED_HARD_5_7[hard][5],
                "k5": 23 + 4 * EXPECTED_HARD_5_7[hard][5],
                "j7": EXPECTED_HARD_5_7[hard][7],
                "k7": 23 + 4 * EXPECTED_HARD_5_7[hard][7],
            }
            for hard, t35 in HARD_TO_T35.items()
        ],
        "hard_phase_rows": rows,
        "multi_prime_injections": coincidences,
        "claim_boundary": (
            "Exact congruence/phase calendar.  Forced small factors are state seeds, "
            "not automatic Lane-I constructions; no terminating shift selector or "
            "Erdos-Straus proof is claimed."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
