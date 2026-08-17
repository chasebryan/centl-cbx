#!/usr/bin/env python3
"""Verify the exact combined k=11 BREC obstruction normal form.

For Mordell-hard p and C11=(p+11)/4, the established Type-II classification
has a pure-QR branch and one thin primitive branch.  This verifier adds the
second exact Lane-I target and exhausts the thin branch.

The resulting combined classification is:

  A. pure QR:
       every prime divisor of C11 is QR modulo 11.
     This always misses both targets because p == 4*C11 (mod 11), hence p is
     QR as well and -p^-1 is NR.

  B. thin primitive:
       v3(C11)=1;
       every other QR prime divisor is 1 mod 11;
       primitive NR factors occur only in classes 2 and 6;
       total primitive-NR valuation <= 2.
     Among the six exponent states (a2,a6), Type I rescues only (2,0) and
     (0,2).  The mixed valuation-two state (1,1), valuation-one states, and
     empty packet miss both targets.

On the q23 Type-I-only branch C23=6*T this transports to C11=3*(2*T-1).

This is exact fixed-shift arithmetic.  It is not a bounded corridor theorem
and does not prove Erdős-Straus.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "kernel"
sys.path.insert(0, str(KERNEL))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze_brec_cylinder as cylinder  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402

HARD = (1, 121, 169, 289, 361, 529)
QR11 = {1, 3, 4, 5, 9}
NR11 = {2, 6, 7, 8, 10}
THIN_NR = {2, 6}
FORCING_NR = {7, 8, 10}
THIN_COMBINED_MISS = {(0, 0), (1, 0), (0, 1), (1, 1)}
THIN_TYPE_I_ONLY = {(2, 0), (0, 2)}


def signed_support(factors: dict[int, int], mod: int = 11) -> set[int]:
    support = {1}
    for residue, exponent in factors.items():
        residue %= mod
        if residue == 0:
            raise ValueError("signed support requires units")
        local = {pow(residue, z, mod) for z in range(-exponent, exponent + 1)}
        support = {(a * b) % mod for a in support for b in local}
    return support


def thin_state(a2: int, a6: int) -> dict[str, Any]:
    if a2 < 0 or a6 < 0 or a2 + a6 > 2:
        raise ValueError("thin q11 state requires a2+a6 <= 2")

    factors = {3: 1}
    if a2:
        factors[2] = a2
    if a6:
        factors[6] = a6
    support = signed_support(factors)

    C = (3 * pow(2, a2, 11) * pow(6, a6, 11)) % 11
    p = (4 * C) % 11
    type_ii = 10
    type_i = (-pow(p, -1, 11)) % 11
    hit_ii = type_ii in support
    hit_i = type_i in support

    if hit_i and hit_ii:
        hit_class = "both"
    elif hit_i:
        hit_class = "type-I-only"
    elif hit_ii:
        hit_class = "type-II-only"
    else:
        hit_class = "miss"

    return {
        "a2": a2,
        "a6": a6,
        "C_mod_11": C,
        "p_mod_11": p,
        "type_II_target": type_ii,
        "type_I_target": type_i,
        "support": sorted(support),
        "hit_type_II": hit_ii,
        "hit_type_I": hit_i,
        "hit_class": hit_class,
    }


def classify_factorization(C: int) -> dict[str, Any]:
    factors = cylinder.factorint(C)
    residues = {q: q % 11 for q in factors}

    if all(residue in QR11 for residue in residues.values()):
        return {
            "branch": "pure-QR",
            "combined_miss": True,
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    if factors.get(3, 0) != 1:
        return {
            "branch": "outside-TypeII-miss-normal-form",
            "combined_miss": False,
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    a2 = 0
    a6 = 0
    valid = True
    for q, exponent in factors.items():
        residue = q % 11
        if q == 3:
            continue
        if residue == 1:
            continue
        if residue == 2:
            a2 += exponent
            continue
        if residue == 6:
            a6 += exponent
            continue
        valid = False
        break

    if not valid or a2 + a6 > 2:
        return {
            "branch": "outside-TypeII-miss-normal-form",
            "combined_miss": False,
            "factorization": cylinder.factor_text(factors),
            "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        }

    state = thin_state(a2, a6)
    return {
        "branch": "thin-primitive",
        "combined_miss": state["hit_class"] == "miss",
        "packet": {"a2": a2, "a6": a6},
        "factorization": cylinder.factor_text(factors),
        "factor_residues": {str(q): residues[q] for q in sorted(residues)},
        "local_state": state,
    }


def verify_pure_qr_logic() -> dict[str, Any]:
    # 4 is QR mod 11.  Therefore p=4C has the same quadratic character as C.
    # If every prime factor of C is QR, C and p are QR, whereas -1 is NR.
    for c in QR11:
        p = 4 * c % 11
        if p not in QR11:
            raise SystemExit(f"pure-QR c={c}: p={p} is not QR")
        target = (-pow(p, -1, 11)) % 11
        if target not in NR11:
            raise SystemExit(f"pure-QR c={c}: Type-I target {target} is not NR")
    return {
        "C_character": "QR",
        "p_character": "QR",
        "type_I_target_character": "NR",
        "type_II_target_character": "NR",
        "combined_miss": True,
    }


def verify_thin_states() -> list[dict[str, Any]]:
    states = []
    for a2 in range(3):
        for a6 in range(3 - a2):
            state = thin_state(a2, a6)
            pair = (a2, a6)
            expected = "type-I-only" if pair in THIN_TYPE_I_ONLY else "miss"
            if state["hit_class"] != expected:
                raise SystemExit(
                    f"thin q11 state {pair}: {state['hit_class']} != {expected}"
                )
            if state["hit_type_II"]:
                raise SystemExit(f"thin q11 state {pair}: Type II unexpectedly hits")
            states.append(state)
    return states


def verify_hard_forcing() -> list[dict[str, int]]:
    rows = []
    for h in HARD:
        if h % 3 != 1:
            raise SystemExit(f"hard residue {h}: expected p=1 mod3")
        if h % 8 != 1:
            raise SystemExit(f"hard residue {h}: expected p=1 mod8")

        # C11 is checked on the actual congruence class modulo lcm(3,8)=24.
        # All hard residues are 1 mod24.
        if h % 24 != 1:
            raise SystemExit(f"hard residue {h}: expected p=1 mod24")
        c11_mod_6 = ((h % 24) + 11) // 4
        if c11_mod_6 % 3 != 0 or c11_mod_6 % 2 != 1:
            raise SystemExit(f"hard residue {h}: C11 is not forced odd and divisible by3")
        rows.append({"p_mod_840": h, "C11_mod_6": c11_mod_6 % 6})
    return rows


def verify_witness(p: int, expected_history: str, expected_branch: str) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: witness is not prime")
    early = [ancestry.classify_stage(p, k) for k in (3, 7, 11, 15, 19)]
    history = "".join(str(stage["sign"]) for stage in early)
    if history != expected_history:
        raise SystemExit(f"p={p}: history {history} != {expected_history}")

    stage11 = early[2]
    C11 = int(stage11["C"])
    local = classify_factorization(C11)
    if local["branch"] != expected_branch:
        raise SystemExit(
            f"p={p}: q11 branch {local['branch']} != {expected_branch}"
        )
    if (stage11["sign"] == "-") != bool(local["combined_miss"]):
        raise SystemExit(f"p={p}: q11 factor normal form disagrees with exact signed box")

    T = (p + 23) // 24
    if C11 != 3 * (2 * T - 1):
        raise SystemExit(f"p={p}: C11 != 3*(2T-1)")

    return {
        "p": p,
        "early_history": history,
        "T": T,
        "C11": C11,
        "branch": local["branch"],
        "local": local,
    }


def verify() -> dict[str, Any]:
    pure = verify_pure_qr_logic()
    thin = verify_thin_states()
    hard = verify_hard_forcing()

    states = {(row["a2"], row["a6"]): row for row in thin}
    if {pair for pair, row in states.items() if row["hit_class"] == "type-I-only"} != THIN_TYPE_I_ONLY:
        raise SystemExit("q11 Type-I-only state set mismatch")
    if {pair for pair, row in states.items() if row["hit_class"] == "miss"} != THIN_COMBINED_MISS:
        raise SystemExit("q11 combined-miss state set mismatch")

    witnesses = [
        verify_witness(8_243_281, "---++", "thin-primitive"),
        verify_witness(18_766_609, "-----", "pure-QR"),
        verify_witness(27_211_969, "-----", "pure-QR"),
    ]

    # A known non-miss at k=11 guards the other direction of the classifier.
    nonmiss = verify_witness(5_151_841, "-++-+", "outside-TypeII-miss-normal-form")
    if nonmiss["local"]["combined_miss"]:
        raise SystemExit("known k11 constructive witness was classified as a miss")

    return {
        "verified": True,
        "mode": "k11-brec-obstruction-normal-form",
        "hard_forcing": hard,
        "pure_QR_branch": pure,
        "thin_states": thin,
        "thin_combined_miss_packets": [list(x) for x in sorted(THIN_COMBINED_MISS)],
        "thin_type_I_only_packets": [list(x) for x in sorted(THIN_TYPE_I_ONLY)],
        "q23_rescue_translation": {
            "C23": "6*T",
            "C11": "3*(2*T-1)",
            "pure_QR_miss": "every prime divisor of 2*T-1 is QR mod 11",
            "thin_miss": (
                "v3(C11)=1; other QR primes are 1 mod11; primitive packet "
                "in {(1,0),(0,1),(1,1)} over residue classes (2,6)"
            ),
        },
        "witnesses": witnesses,
        "known_nonmiss": nonmiss,
        "claim_boundary": (
            "Exact fixed-shift combined-target classification only.  No bounded "
            "Lane-I ceiling, ancestry pruning theorem, or Erdős-Straus proof."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
