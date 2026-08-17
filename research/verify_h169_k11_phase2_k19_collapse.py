#!/usr/bin/env python3
"""Verify the h169 k11-phase-2 -> k19 mode/valuation collapse.

Scope: the realized h169 Route-A / Route-B simultaneous-survivor laboratory.

Write

    p = 169 + 840 t,
    T = (p+23)/24 = 8 + 35 t.

The landed h169 k11 theorem says a combined miss is pure QR modulo 11 and
therefore restricts t mod11 to {0,2,3,4,8}.  On t=8 mod11 we have
T=2 mod11, hence

    11 | C19 = 6T-1.

On the two realized q23/k19 pair routes,

    Route A: C19 = 391 R = 17*23*R,
    Route B: C19 = 1081 R = 23*47*R.

Neither route seed is divisible by 11, so the forced literal factor 11 lies in
R.  The landed k19 BARE normal form requires every prime divisor of R to be
1 mod19.  But 11 mod19 = 11 != 1.  Therefore BARE is impossible.

Thus, conditional on k19 also being a miss,

    h169 + k11 miss + t=8 mod11 -> k19 mode FULL_QR.

The same phase also preloads residue 11 into the exact q19 signed-box state.
The landed weighted automaton gives the stronger vertical resource bound

    Omega_NR(C19) <= 2

for every k19 Type-II miss on this phase, instead of the generic h169 bound 8.

This module composes already-landed exact theorems and verifies the algebraic
bridge between them.  It does not claim the phase is forced by k11 miss.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(RESEARCH))

import propagate_h169_dependency_state as dep  # noqa: E402
import verify_h169_k11_future_factor_partition as future  # noqa: E402
import verify_k19_nr_valuation_budget as nrbudget  # noqa: E402

HARD = 169
SELECTED_t11 = 8
SELECTED_T11 = 2
ROUTE_SEEDS = {
    "A": {"S": 391, "factors": {17: 1, 23: 1}},
    "B": {"S": 1081, "factors": {23: 1, 47: 1}},
}


def factor_small(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def verify_phase() -> dict[str, Any]:
    partition = future.verify()
    allowed = partition["k11_combined_miss_implies_t_mod_11"]
    if allowed != [0, 2, 3, 4, 8]:
        raise SystemExit(f"h169 k11 phase domain changed: {allowed}")
    if SELECTED_t11 not in allowed:
        raise SystemExit("selected t mod11 phase is no longer k11-admissible")

    T11 = (8 + 35 * SELECTED_t11) % 11
    if T11 != SELECTED_T11:
        raise SystemExit(f"t11=8 gives T11={T11}, expected 2")
    if (6 * T11 - 1) % 11 != 0:
        raise SystemExit("T11=2 no longer forces 11|C19")

    selected = [
        row
        for row in partition["partition"]
        if row["t_mod_11"] == SELECTED_t11
    ]
    if len(selected) != 1:
        raise SystemExit("future factor partition lost the selected h169 row")
    row = selected[0]
    if row["T_mod_11"] != 2 or row["p_mod_11"] != 3:
        raise SystemExit(f"selected h169 phase row changed: {row}")

    return {
        "t_mod_11": SELECTED_t11,
        "T_mod_11": T11,
        "p_mod_11": row["p_mod_11"],
        "forced_factor": 11,
        "forced_coordinate": "C19=6T-1",
        "next_post_k23_reentry_shift": row["shift_k"],
    }


def verify_route(route: str) -> dict[str, Any]:
    spec = ROUTE_SEEDS[route]
    S = int(spec["S"])
    factors = factor_small(S)
    if factors != spec["factors"]:
        raise SystemExit(f"Route {route}: seed factorization changed: {factors}")
    if S % 11 == 0:
        raise SystemExit(f"Route {route}: seed unexpectedly absorbs factor11")

    # The exact dependency grammar exposes the already-landed BARE support law.
    state = dep.propagate(route, {"k19_mode": frozenset({"BARE"})})
    if state["contradiction"]:
        raise SystemExit(f"Route {route}: BARE vanished from the base grammar")
    support = state["support_consequences"]
    bare_law = "k19 BARE: residual R has only 1-mod19 prime support"
    if bare_law not in support:
        raise SystemExit(f"Route {route}: BARE residual-support theorem unavailable")
    if set(state["domains"]["k19_mode"]) != {"BARE"}:
        raise SystemExit(f"Route {route}: BARE projection was not exact")

    # Because gcd(S,11)=1, 11|C19=S*R forces 11|R.  That violates the BARE
    # requirement q=1 mod19 for every prime divisor q of R.
    if 11 % 19 == 1:
        raise SystemExit("11 unexpectedly became 1 mod19")
    if dep.M19 != ("BARE", "FULL_QR"):
        raise SystemExit(f"k19 mode domain changed: {dep.M19}")

    return {
        "route": route,
        "C19_form": f"{S}*R",
        "route_seed": S,
        "route_seed_factorization": "*".join(
            str(p) if e == 1 else f"{p}^{e}" for p, e in sorted(factors.items())
        ),
        "gcd_route_seed_11": 1,
        "forced_consequence": "11|R",
        "bare_support_law": bare_law,
        "11_mod_19": 11,
        "bare_compatible": False,
        "only_surviving_k19_miss_mode": "FULL_QR",
    }


def verify_valuation_contraction() -> dict[str, Any]:
    seeded = nrbudget.weighted_budget((11,))
    generic = nrbudget.weighted_budget(())
    if generic["max_NR_valuation"] != 8:
        raise SystemExit("generic q19 NR valuation bound changed")
    if seeded["max_NR_valuation"] != 2:
        raise SystemExit("seed11 q19 NR valuation bound changed")
    if seeded["positive_NR_edges_inside_SCCs"] != 0:
        raise SystemExit("seed11 Type-II-miss graph gained a positive NR cycle")

    return {
        "generic_h169_TypeII_miss_max_Omega_NR": 8,
        "phase_seed": [11],
        "phase_TypeII_miss_max_Omega_NR": 2,
        "resource_drop": 6,
        "positive_NR_edges_inside_seeded_SCCs": 0,
        "interpretation": (
            "the same ancestry phase that deletes BARE also reduces the exact "
            "remaining nonresidue-valuation budget from 8 to 2"
        ),
    }


def verify() -> dict[str, Any]:
    phase = verify_phase()
    routes = [verify_route(route) for route in ("A", "B")]
    valuation = verify_valuation_contraction()

    return {
        "verified": True,
        "mode": "h169-k11-phase2-k19-collapse",
        "scope": "realized h169 Route-A/Route-B simultaneous-survivor grammar",
        "phase": phase,
        "routes": routes,
        "horizontal_mode_theorem": (
            "If h169 is on a realized pair route, k11 misses, t=8 mod11, and "
            "k19 also misses, then k19 BARE is impossible and the k19 survivor "
            "mode is FULL_QR."
        ),
        "vertical_resource_theorem": valuation,
        "obligation_chain": [
            "k11 miss -> t mod11 in {0,2,3,4,8}",
            "t=8 mod11 -> T=2 mod11",
            "T=2 mod11 -> 11|C19",
            "C19=S*R with gcd(S,11)=1 -> 11|R",
            "k19 BARE -> every prime divisor of R is 1 mod19",
            "11 mod19=11 -> BARE contradiction",
            "therefore a k19 miss is FULL_QR",
            "seed11 q19 Type-II-miss graph -> Omega_NR(C19)<=2",
        ],
        "claim_boundary": (
            "Exact theorem composition inside the realized h169 pair-route "
            "laboratory.  k11 miss does not force t=8 mod11; the other four "
            "k11 phases remain.  No finite Lane-I ceiling or Erdos-Straus proof "
            "is claimed."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
