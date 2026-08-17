#!/usr/bin/env python3
"""Verify the exact h169 k11-phase-5 -> k35 branch collapse.

On h169 write T=(p+23)/24=8+35t.  The class-conditioned k11 theorem says
that a k11 combined miss is pure QR modulo 11, so its allowed T phases are
{1,2,3,5,8} mod11.

On the phase T=5 mod11,

    C35 = 6T+3 = 3F,
    F   = 2T+1,

and therefore 11|F.  The complete h169 k35 theorem is

    k35 miss iff J35(F) or S7(F).

But S7 requires every prime-factor occurrence of F except one distinguished
3-mod7 occurrence to be 1 mod7.  Literal prime 11 is 4 mod7, so the forced
factor 11 excludes S7 identically.  Since 11 itself lies in H35, J35 remains
possible.

Hence on h169 + T=5 mod11:

    k35 miss iff J35(F).

The k11 miss hypothesis is what places phase 5 inside the exact predecessor
state grammar; the branch-collapse implication itself follows from the phase.
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
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402
import verify_k35_two_branch_survivor_theorem as k35  # noqa: E402

HARD = 169
PHASE_T11 = 5
QR11 = {1, 3, 4, 5, 9}
H35 = set(k35.h35())

REGRESSIONS = {
    # k11 miss + T=5 mod11 + k35 miss through J35
    3_529: {"k35_miss": True, "J35": True},
    31_249: {"k35_miss": True, "J35": True},
    # same h169/k11/phase state, but k35 constructs because J35 fails
    179_089: {"k35_miss": False, "J35": False},
}


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def J35(F: int) -> bool:
    return all(q % 35 in H35 for q in cylinder.factorint(F))


def S7(F: int) -> bool:
    factors = cylinder.factorint(F)
    special_occurrences = sum(
        exponent for q, exponent in factors.items() if q % 7 == 3
    )
    return (
        special_occurrences == 1
        and all(q % 7 in {1, 3} for q in factors)
        and all(exponent == 1 for q, exponent in factors.items() if q % 7 == 3)
    )


def exact_k35_state(F: int) -> dict[str, Any]:
    state = k35.seed_state()  # consumes the mandatory factor 3 in C35=3F
    for q, exponent in sorted(cylinder.factorint(F).items()):
        residue = q % 35
        if residue not in k35.UNITS:
            raise SystemExit(f"F={F}: non-unit q35 factor {q}")
        for _ in range(exponent):
            state = k35.transition35(state, residue)
    hit_i, hit_ii = k35.status35(state)
    if state[1] != k35.FINAL_CENTER:
        raise SystemExit(f"F={F}: final center {state[1]} != 16")
    return {
        "mask": sorted(state[0]),
        "center": state[1],
        "hit_type_I": hit_i,
        "hit_type_II": hit_ii,
        "miss": not (hit_i or hit_ii),
    }


def verify_phase_arithmetic() -> dict[str, Any]:
    # h169: p=169+840t and T=(p+23)/24=8+35t.
    # T=5 mod11 <=> t=4 mod11.
    solutions = []
    for t11 in range(11):
        T11 = (8 + 35 * t11) % 11
        if T11 == PHASE_T11:
            solutions.append(t11)
    if solutions != [4]:
        raise SystemExit(f"h169 phase T11=5 gives t11={solutions}, expected [4]")

    # F=2T+1, so the selected phase forces literal prime 11.
    if (2 * PHASE_T11 + 1) % 11 != 0:
        raise SystemExit("T=5 mod11 no longer forces 11|F")

    # The complete h169 k35 branches treat factor11 asymmetrically.
    if 11 % 7 != 4:
        raise SystemExit("11 mod7 changed")
    if 11 % 35 not in H35:
        raise SystemExit("11 is no longer in H35")
    if legendre(11, 5) * legendre(11, 7) != 1:
        raise SystemExit("11 no longer has J35 character +1")

    return {
        "p_mod_840": HARD,
        "T_mod_11": PHASE_T11,
        "equivalent_t_mod_11": 4,
        "F": "2T+1",
        "forced_prime": 11,
        "forced_prime_mod_7": 4,
        "forced_prime_in_H35": True,
        "consequence": "S7 impossible; J35 remains admissible",
    }


def regression(p: int, expected: dict[str, bool]) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: regression is not prime")
    if p % 840 != HARD:
        raise SystemExit(f"p={p}: hard class {p % 840} !=169")

    T = (p + 23) // 24
    if T % 11 != PHASE_T11:
        raise SystemExit(f"p={p}: T mod11={T % 11} !=5")

    stage11 = ancestry.classify_stage(p, 11)
    if stage11["sign"] != "-":
        raise SystemExit(f"p={p}: expected k11 combined miss")
    C11 = int(stage11["C"])
    if not all(q % 11 in QR11 for q in cylinder.factorint(C11)):
        raise SystemExit(f"p={p}: h169 k11 miss is not pure QR")

    F = 2 * T + 1
    C35 = 3 * F
    if C35 != (p + 35) // 4:
        raise SystemExit(f"p={p}: C35 affine identity failed")
    if F % 11:
        raise SystemExit(f"p={p}: forced factor11 missing from F")

    j = J35(F)
    s = S7(F)
    if s:
        raise SystemExit(f"p={p}: S7 survived despite forced factor11")
    if j != expected["J35"]:
        raise SystemExit(f"p={p}: J35={j} != {expected['J35']}")

    state = exact_k35_state(F)
    if state["miss"] != expected["k35_miss"]:
        raise SystemExit(
            f"p={p}: exact k35 miss={state['miss']} != {expected['k35_miss']}"
        )
    if state["miss"] != j:
        raise SystemExit(f"p={p}: exact k35 state disagrees with J35-only theorem")

    return {
        "p": p,
        "T": T,
        "T_mod_11": T % 11,
        "C11": C11,
        "F": F,
        "F_factorization": cylinder.factor_text(cylinder.factorint(F)),
        "J35": j,
        "S7": s,
        "k35": state,
    }


def verify() -> dict[str, Any]:
    phase = verify_phase_arithmetic()
    rows = [regression(p, expected) for p, expected in REGRESSIONS.items()]

    return {
        "verified": True,
        "mode": "h169-k11-phase5-k35-branch-collapse",
        "phase": phase,
        "theorem": (
            "For h169 on T=5 mod11, literal prime11 divides F=C35/3 and excludes "
            "the S7 branch. Therefore exact k35 miss iff J35(F)."
        ),
        "k11_context": (
            "A h169 k11 combined miss is pure QR and allows T mod11 in "
            "{1,2,3,5,8}; this theorem resolves the phase-5 child."
        ),
        "regressions": rows,
        "claim_boundary": (
            "Exact phase-conditioned h169 k35 branch collapse.  It does not force "
            "T=5 from k11 miss, eliminate J35, establish a finite Lane-I ceiling, "
            "or prove Erdos-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
