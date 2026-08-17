#!/usr/bin/env python3
"""Verify the exact k=11 obstruction collapse in hard classes 169, 289, 529.

For the q23 parameter T=(p+23)/24, the three Mordell-hard classes

    p mod 840 in {169,289,529}

correspond to

    T mod 35 in {8,13,23}.

All three satisfy T == 3 (mod 5), hence

    5 | (2*T-1)

and therefore the literal prime 5 is forced into

    C11 = 3*(2*T-1).

The already-proved general k11 Type-II miss normal form has only two branches:

  A. every prime divisor of C11 is QR modulo 11; or
  B. the thin primitive branch, in which every QR prime divisor other than the
     forced prime 3 must be 1 modulo 11.

But 5 is QR modulo 11 and 5 != 1 modulo 11.  Thus the forced literal factor 5
kills branch B identically in these hard classes.  A Type-II miss can only be
pure QR, and the independently proved Type-I companion theorem says every pure
QR Type-II miss is also a Type-I miss.

Consequently, for p mod840 in {169,289,529},

    sigma_11(p) = -
    iff every prime divisor of C11=(p+11)/4 is QR modulo 11.

The verifier checks the congruence forcing, the general theorem interface, an
independent seeded residue automaton, and exact prime regression witnesses on
both sides of the equivalence for each hard class.
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
import classify_signed_box_residue_automaton as automaton  # noqa: E402
import verify_k11_brec_obstruction_normal_form as k11  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402

HARD_TO_T35 = {
    169: 8,
    289: 13,
    529: 23,
}
QR11 = {1, 3, 4, 5, 9}

# One exact miss and one exact construction in every class.  These are
# regression witnesses only; the theorem itself is the symbolic branch
# elimination above.
REGRESSIONS = {
    169: {"miss": 2_689, "constructive": 1_009},
    289: {"miss": 12_049, "constructive": 1_129},
    529: {"miss": 5_569, "constructive": 3_049},
}


def hard_class_row(hard: int, t35: int) -> dict[str, Any]:
    if t35 % 5 != 3:
        raise SystemExit(f"hard={hard}: T mod35={t35} is not 3 mod5")
    if (2 * t35 - 1) % 5 != 0:
        raise SystemExit(f"hard={hard}: 5 is not forced into 2T-1")

    # Work directly on the hard residue modulo 840.  Since h+11 is divisible
    # by four, C11 has a well-defined residue modulo 210.
    if (hard + 11) % 4:
        raise SystemExit(f"hard={hard}: C11 is not integral on the residue class")
    c11_mod_210 = ((hard + 11) // 4) % 210
    if c11_mod_210 % 5:
        raise SystemExit(f"hard={hard}: literal factor 5 is not forced in C11")
    if c11_mod_210 % 3:
        raise SystemExit(f"hard={hard}: forced factor 3 disappeared from C11")

    # 5 is a quadratic residue but is not the inert residue 1 modulo 11.
    if 5 not in QR11 or 5 % 11 == 1:
        raise SystemExit("q11 character classification of literal prime 5 changed")
    if pow(5, 5, 11) != 1:
        raise SystemExit("Euler criterion no longer identifies 5 as QR mod11")

    return {
        "p_mod_840": hard,
        "T_mod_35": t35,
        "T_mod_5": t35 % 5,
        "C11_mod_210": c11_mod_210,
        "forced_prime_factors": [3, 5],
        "five_mod_11": 5,
        "five_character_mod_11": "QR",
        "thin_branch_excluded_because": (
            "the thin q11 Type-II miss branch requires every QR prime divisor "
            "other than forced 3 to be 1 mod11, but literal prime 5 is forced"
        ),
    }


def exact_regression(p: int, hard: int, expected_miss: bool) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: regression witness is not prime")
    if p % 840 != hard:
        raise SystemExit(f"p={p}: hard class {p % 840} != {hard}")

    stage = ancestry.classify_stage(p, 11)
    if not stage["defined"]:
        raise SystemExit(f"p={p}: k11 unexpectedly undefined")
    C11 = int(stage["C"])
    factors = cylinder.factorint(C11)
    all_qr = all(q % 11 in QR11 for q in factors)
    exact_miss = stage["sign"] == "-"

    if all_qr != expected_miss:
        raise SystemExit(
            f"p={p}: factor criterion all_qr={all_qr} != expected {expected_miss}"
        )
    if exact_miss != expected_miss:
        raise SystemExit(
            f"p={p}: exact stage miss={exact_miss} != expected {expected_miss}"
        )

    local = k11.classify_factorization(C11)
    if bool(local["combined_miss"]) != expected_miss:
        raise SystemExit(f"p={p}: general k11 normal form disagrees")
    if expected_miss and local["branch"] != "pure-QR":
        raise SystemExit(
            f"p={p}: class-conditioned miss entered {local['branch']} instead of pure-QR"
        )
    if C11 % 5:
        raise SystemExit(f"p={p}: literal forced factor 5 missing")

    return {
        "p": p,
        "p_mod_840": hard,
        "C11": C11,
        "factorization": cylinder.factor_text(factors),
        "factor_residues_mod_11": {
            str(q): q % 11 for q in sorted(factors)
        },
        "all_prime_divisors_QR_mod_11": all_qr,
        "exact_hit_class": stage["hit_class"],
        "sign": stage["sign"],
        "general_k11_branch": local["branch"],
    }


def verify_seeded_automaton() -> dict[str, Any]:
    seeded = automaton.classify(11, [3, 5], 100_000, 16)
    if seeded["type_II_miss_states"] != 5:
        raise SystemExit("q11 [3,5] Type-II-miss closure changed")
    if seeded["combined_miss_states"] != 5:
        raise SystemExit("q11 [3,5] combined-miss count changed")
    if seeded["type_I_only_states"] != 0:
        raise SystemExit("q11 [3,5] unexpectedly admits Type-I-only state")
    if seeded["qr_only_combined_miss_states"] != 5:
        raise SystemExit("q11 [3,5] closure contains a non-QR combined miss")

    return {
        "seed_residues": seeded["seed_residues"],
        "seed_support_size": seeded["seed_support_size"],
        "type_II_miss_states": seeded["type_II_miss_states"],
        "combined_miss_states": seeded["combined_miss_states"],
        "type_I_only_states": seeded["type_I_only_states"],
        "qr_only_combined_miss_states": seeded[
            "qr_only_combined_miss_states"
        ],
        "minimal_depth_distribution": seeded["minimal_depth_distribution"],
    }


def verify() -> dict[str, Any]:
    rows = [hard_class_row(h, t35) for h, t35 in HARD_TO_T35.items()]
    seeded = verify_seeded_automaton()

    regressions: list[dict[str, Any]] = []
    for hard, witnesses in REGRESSIONS.items():
        regressions.append(
            exact_regression(witnesses["miss"], hard, True)
        )
        regressions.append(
            exact_regression(witnesses["constructive"], hard, False)
        )

    if {row["p_mod_840"] for row in rows} != {169, 289, 529}:
        raise SystemExit("class-conditioned theorem hard-class set changed")

    return {
        "verified": True,
        "mode": "h169-h289-h529-k11-brec-obstruction-normal-form",
        "hard_classes": [169, 289, 529],
        "hard_class_rows": rows,
        "seeded_q11_automaton": seeded,
        "theorem": (
            "For a Mordell-hard prime p with p mod840 in {169,289,529}, "
            "sigma_11(p)=- iff every prime divisor of C11=(p+11)/4 is a "
            "quadratic residue modulo 11."
        ),
        "type_II_companion_consequence": (
            "In these three hard classes, a k11 Type-II miss automatically "
            "implies a Type-I miss; the thin Type-I-only packets are impossible."
        ),
        "regressions": regressions,
        "claim_boundary": (
            "Exact class-conditioned fixed-shift theorem.  It does not classify "
            "the other hard classes at k11, create a Lane-I ceiling, or prove "
            "Erdos-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
