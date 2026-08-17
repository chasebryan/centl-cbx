#!/usr/bin/env python3
"""Verify a concrete residue/valuation normal form for h289 at k=19.

Hard class p=289 mod840 forces literal factor 7 into C19.  In base-2
exponents modulo 19, 7 has exponent 6 and supplies K={0,6,12}.  Quotient by K
reduces factor residues to Z/6 classes:

  0: {1,7,11}       QR kernel K
  1: {2,3,14}       NR positive orientation P+
  2: {4,6,9}        QR outside K
  3: {8,12,18}      NR direct Type-II forcing
  4: {5,16,17}      QR outside K
  5: {10,13,15}     NR negative orientation P-

The exact Type-II miss normal form is:

  A. pure QR: every prime divisor of C19 is QR mod19; or
  B. thin NR: every QR factor lies in K, every NR factor lies in P+ or P-,
     and alpha+beta <= 2, where alpha/beta are total valuations in P+/P-.

Inside thin NR:

  Type-I-only packets: (1,0), (2,0), (1,1)
  combined-miss packets: (0,1), (0,2)

The empty packet is already contained in pure QR.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "kernel"
RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(KERNEL))
sys.path.insert(0, str(RESEARCH))

import analyze_brec_cylinder as cylinder  # noqa: E402
import classify_signed_box_residue_automaton as auto  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402

HARD = 289
K = {1, 7, 11}
P_PLUS = {2, 3, 14}
QR_OUTSIDE = {4, 5, 6, 9, 16, 17}
P_MINUS = {10, 13, 15}
DIRECT_II = {8, 12, 18}
QR19 = K | QR_OUTSIDE
NR19 = P_PLUS | P_MINUS | DIRECT_II

THIN_TYPE_I_ONLY = {(1, 0), (2, 0), (1, 1)}
THIN_COMBINED_MISS = {(0, 1), (0, 2)}

REGRESSIONS = {
    1_129: "type-I-only",   # thin (1,0)
    10_369: "miss",        # thin (0,1)
    8_689: "miss",         # pure QR
    22_129: "type-II-only",# direct-II residue 18
}


def residue_partition() -> dict[str, Any]:
    g = auto.primitive_root(19)
    logs = auto.log_table(19, g)
    if g != 2:
        raise SystemExit(f"q19 primitive root changed: {g}")

    classes = {i: set() for i in range(6)}
    for residue in range(1, 19):
        classes[logs[residue] % 6].add(residue)

    expected = {
        0: K,
        1: P_PLUS,
        2: {4, 6, 9},
        3: DIRECT_II,
        4: {5, 16, 17},
        5: P_MINUS,
    }
    if classes != expected:
        raise SystemExit(f"q19 quotient residue partition changed: {classes}")
    if QR19 != {pow(x, 2, 19) for x in range(1, 19)}:
        raise SystemExit("declared QR19 partition is incorrect")
    if NR19 != set(range(1, 19)) - QR19:
        raise SystemExit("declared NR19 partition is incorrect")

    return {
        "primitive_root": g,
        "classes": {str(k): sorted(v) for k, v in classes.items()},
        "K": sorted(K),
        "P_plus": sorted(P_PLUS),
        "P_minus": sorted(P_MINUS),
        "QR_outside_K": sorted(QR_OUTSIDE),
        "direct_Type_II": sorted(DIRECT_II),
    }


def quotient_support(alpha: int, beta: int) -> set[int]:
    support = {0}
    for atom, count in ((1, alpha), (5, beta)):
        for _ in range(count):
            support = (
                support
                | {(x + atom) % 6 for x in support}
                | {(x - atom) % 6 for x in support}
            )
    return support


def thin_packet(alpha: int, beta: int) -> dict[str, Any]:
    if alpha < 0 or beta < 0 or alpha + beta > 2:
        raise ValueError("thin packet requires alpha+beta<=2")
    support = quotient_support(alpha, beta)
    cbar = (alpha - beta) % 6
    type_ii = 3
    type_i = (1 - cbar) % 6
    hit_ii = type_ii in support
    hit_i = type_i in support
    if hit_ii:
        hit_class = "type-II-hit"
    elif hit_i:
        hit_class = "type-I-only"
    else:
        hit_class = "combined-miss"
    return {
        "alpha": alpha,
        "beta": beta,
        "cbar": cbar,
        "support": sorted(support),
        "type_II_target": type_ii,
        "type_I_target": type_i,
        "class": hit_class,
    }


def verify_thin_packets() -> list[dict[str, Any]]:
    rows = []
    for alpha in range(3):
        for beta in range(3 - alpha):
            row = thin_packet(alpha, beta)
            pair = (alpha, beta)
            if pair == (0, 0):
                expected = "combined-miss"
            elif pair in THIN_TYPE_I_ONLY:
                expected = "type-I-only"
            elif pair in THIN_COMBINED_MISS:
                expected = "combined-miss"
            else:
                raise SystemExit(f"unclassified thin packet {pair}")
            if row["class"] != expected:
                raise SystemExit(
                    f"thin packet {pair}: {row['class']} != {expected}"
                )
            if row["type_II_target"] in row["support"]:
                raise SystemExit(f"thin packet {pair} unexpectedly hits Type II")
            rows.append(row)

    if {
        (r["alpha"], r["beta"])
        for r in rows
        if r["class"] == "type-I-only"
    } != THIN_TYPE_I_ONLY:
        raise SystemExit("Type-I-only thin packet set changed")
    return rows


def classify_factorization(C19: int) -> dict[str, Any]:
    factors = cylinder.factorint(C19)
    residues = {q: q % 19 for q in factors}

    if all(r in QR19 for r in residues.values()):
        return {
            "branch": "pure-QR",
            "predicted_hit_class": "miss",
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    if any(r in DIRECT_II for r in residues.values()):
        return {
            "branch": "outside-TypeII-miss-normal-form",
            "predicted_hit_class": "Type-II-hit",
            "reason": "direct quotient-class-3 factor",
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    has_qr_outside = any(r in QR_OUTSIDE for r in residues.values())
    has_nr = any(r in NR19 for r in residues.values())
    if has_qr_outside and has_nr:
        return {
            "branch": "outside-TypeII-miss-normal-form",
            "predicted_hit_class": "Type-II-hit",
            "reason": "QR quotient saturation plus NR coset",
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    alpha = sum(e for q, e in factors.items() if q % 19 in P_PLUS)
    beta = sum(e for q, e in factors.items() if q % 19 in P_MINUS)
    if alpha + beta >= 3:
        return {
            "branch": "outside-TypeII-miss-normal-form",
            "predicted_hit_class": "Type-II-hit",
            "reason": "three signed +/-1 quotient atoms can sum to Type-II target 3",
            "alpha": alpha,
            "beta": beta,
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    # If an NR factor exists and none of the forcing conditions fired, every QR
    # residue must be in K and every NR residue must be in P+ or P-.
    if has_nr:
        if any(r not in K | P_PLUS | P_MINUS for r in residues.values()):
            raise SystemExit("thin classifier admitted forbidden residue")
        packet = thin_packet(alpha, beta)
        predicted = "type-I-only" if packet["class"] == "type-I-only" else "miss"
        return {
            "branch": "thin-NR",
            "predicted_hit_class": predicted,
            "alpha": alpha,
            "beta": beta,
            "packet": packet,
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    raise SystemExit("classifier reached impossible QR/non-QR partition state")


def verify_necessity_mechanisms() -> dict[str, Any]:
    # Starting from K quotient support {0}, an even outside-K QR atom has class
    # 2 or4 and fills the whole even subgroup {0,2,4}.
    even = {0, 2, 4}
    for a in (2, 4):
        support = {0, a % 6, (-a) % 6}
        if support != even:
            raise SystemExit(f"QR outside-K atom {a} does not fill even quotient")
        for odd in (1, 5):
            expanded = (
                support
                | {(x + odd) % 6 for x in support}
                | {(x - odd) % 6 for x in support}
            )
            if expanded != set(range(6)) or 3 not in expanded:
                raise SystemExit("QR saturation plus NR does not force Type II")

    # Any direct class3 factor hits Type II immediately.
    if 3 not in {0, 3, (-3) % 6}:
        raise SystemExit("quotient class3 does not directly hit Type II")

    # Any three P+/P- occurrences can each be signed to contribute +1, so 3 is
    # reachable regardless of their orientations.
    orientations = (1, 5)
    for a in orientations:
        for b in orientations:
            for c in orientations:
                chosen = [1 if x == 1 else (-x) % 6 for x in (a, b, c)]
                if sum(chosen) % 6 != 3:
                    raise SystemExit("three oriented NR atoms failed to force target3")

    return {
        "QR_outside_K_fills_even_quotient": True,
        "even_quotient_plus_any_allowed_NR_fills_Z6": True,
        "direct_class3_hits_Type_II": True,
        "three_P_plus_minus_occurrences_force_Type_II": True,
    }


def regression(p: int, expected: str) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: regression is not prime")
    if p % 840 != HARD:
        raise SystemExit(f"p={p}: not in h289")
    stage = ancestry.classify_stage(p, 19)
    if stage["hit_class"] != expected:
        raise SystemExit(f"p={p}: exact {stage['hit_class']} != {expected}")
    C19 = int(stage["C"])
    local = classify_factorization(C19)

    if expected in {"miss", "type-I-only"}:
        if local["predicted_hit_class"] != expected:
            raise SystemExit(
                f"p={p}: residue normal form predicts {local['predicted_hit_class']}"
            )
    elif expected == "type-II-only":
        if local["predicted_hit_class"] != "Type-II-hit":
            raise SystemExit(f"p={p}: residue normal form failed to force Type II")

    return {
        "p": p,
        "C19": C19,
        "exact_hit_class": stage["hit_class"],
        "normal_form": local,
    }


def verify() -> dict[str, Any]:
    partition = residue_partition()
    mechanisms = verify_necessity_mechanisms()
    packets = verify_thin_packets()
    regressions = [regression(p, cls) for p, cls in REGRESSIONS.items()]

    return {
        "verified": True,
        "mode": "h289-k19-residue-normal-form",
        "hard_class": HARD,
        "partition": partition,
        "necessity_mechanisms": mechanisms,
        "thin_packets": packets,
        "thin_type_I_only_packets": [list(x) for x in sorted(THIN_TYPE_I_ONLY)],
        "thin_combined_miss_packets": [list(x) for x in sorted(THIN_COMBINED_MISS)],
        "type_II_miss_normal_form": {
            "branch_A": "every prime divisor of C19 is QR modulo 19",
            "branch_B": (
                "all QR factors lie in {1,7,11}; all NR factors lie in "
                "P+={2,3,14} or P-={10,13,15}; alpha+beta<=2"
            ),
        },
        "regressions": regressions,
        "claim_boundary": (
            "Exact fixed-shift residue/valuation normal form for h289 k19.  It does "
            "not assert arithmetic realization after earlier ancestry or prove a "
            "global Lane-I ceiling or Erdos-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
