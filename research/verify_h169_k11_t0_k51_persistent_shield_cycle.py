#!/usr/bin/env python3
"""Verify the persistent factor-11 cycle inside the exact h169 k51 Jacobi normal form.

The canonical t11=0 theorem proves that, after stripping the forced factors
5 and 11 from C51=55R, a k51 combined miss is equivalent to every residual
prime-factor occurrence lying in

    H51 = ker Jacobi(./51) = <11>, |H51|=16.

This companion verifier asks what happens if the residual factorization keeps
spending valuation on the already-forced rational prime 11.  Starting from the
canonical seed [5,11], it repeatedly applies residue 11 in the exact U(51)
signed-box transition system.

The support saturates H51 after four *additional* occurrences of 11, i.e. when
the total 11-adic exponent has reached five including the forced seed copy.
Thereafter support remains exactly H51 while the center rotates through H51.
Since ord_51(11)=16, the exact state has period 16.  Every state on the cycle
is a combined miss by the canonical H51 normal form.

Thus local k51 residue geometry has no finite ceiling on v_11(C51).  Any global
termination proof must kill this escape through simultaneous cofactor/ancestry
constraints rather than a local k51 valuation argument.
"""

from __future__ import annotations

import json
from typing import Any

import verify_h169_k11_t0_k51_jacobi_normal_form as k51

FORCED_SEED = (5, 11)
REPEATED_FACTOR = 11
EXPECTED_ADDITIONAL_SATURATION = 4
EXPECTED_TOTAL_V11_SATURATION = 5
EXPECTED_PERIOD = 16


def verify_cycle() -> dict[str, Any]:
    canonical = k51.verify()
    H = frozenset(canonical["seed_geometry"]["H51"])
    if len(H) != 16:
        raise SystemExit("canonical H51 order changed")

    state = k51.seed_state(FORCED_SEED)
    if k51.state_class(state) != "miss":
        raise SystemExit("canonical [5,11] seed is no longer a combined miss")

    states: dict[int, k51.State] = {0: state}
    classes: dict[int, str] = {0: k51.state_class(state)}
    supports: dict[int, frozenset[int]] = {0: k51.support_values(state)}

    # Two periods are enough to prove the stated finite-state cycle identity.
    for additional in range(1, EXPECTED_ADDITIONAL_SATURATION + 2 * EXPECTED_PERIOD + 1):
        state = k51.transition(state, REPEATED_FACTOR)
        states[additional] = state
        classes[additional] = k51.state_class(state)
        supports[additional] = k51.support_values(state)

    saturation_candidates = [
        i for i, support in supports.items() if support == H
    ]
    if not saturation_candidates:
        raise SystemExit("repeated factor11 never saturated H51")
    first_saturation = min(saturation_candidates)
    if first_saturation != EXPECTED_ADDITIONAL_SATURATION:
        raise SystemExit(
            f"H51 saturation moved: additional={first_saturation} "
            f"!= {EXPECTED_ADDITIONAL_SATURATION}"
        )

    # Before saturation the support must be a proper subset; after saturation
    # it remains exactly H51 because multiplication by 11 permutes H51.
    for i in range(first_saturation):
        if supports[i] == H:
            raise SystemExit("H51 saturated earlier than claimed")
    for i in range(first_saturation, max(states) + 1):
        if supports[i] != H:
            raise SystemExit(f"support escaped H51 after saturation at step {i}")
        if classes[i] != "miss":
            raise SystemExit(f"persistent H51 state at step {i} is not a combined miss")

    if states[first_saturation + EXPECTED_PERIOD] != states[first_saturation]:
        raise SystemExit("exact state failed to return after 16 repeated factor11 transitions")

    # Verify that no shorter positive period closes the saturated exact state.
    shorter = [
        period
        for period in range(1, EXPECTED_PERIOD)
        if states[first_saturation + period] == states[first_saturation]
    ]
    if shorter:
        raise SystemExit(f"k51 shield cycle has unexpected shorter period(s): {shorter}")

    # ord_51(11)=16 is independently frozen by the canonical theorem.  The
    # state-period proof above includes both center and support, so it is the
    # exact signed-box period, not merely a group-order observation.
    generator_order = 1
    x = REPEATED_FACTOR % k51.K
    while x != 1:
        x = x * REPEATED_FACTOR % k51.K
        generator_order += 1
        if generator_order > 100:
            raise SystemExit("failed to recover ord_51(11)")
    if generator_order != EXPECTED_PERIOD:
        raise SystemExit(f"ord_51(11) changed: {generator_order}")

    prefix = []
    for additional in range(0, first_saturation + EXPECTED_PERIOD + 1):
        st = states[additional]
        prefix.append(
            {
                "additional_factor11_occurrences": additional,
                "total_v11_including_forced_copy": additional + 1,
                "center_mod_51": st.center,
                "support_size": len(supports[additional]),
                "support_is_H51": supports[additional] == H,
                "class": classes[additional],
            }
        )

    return {
        "verified": True,
        "mode": "h169-k11-t0-k51-persistent-shield-cycle",
        "canonical_normal_form": canonical["mode"],
        "seed": list(FORCED_SEED),
        "repeated_factor": REPEATED_FACTOR,
        "H51": sorted(H),
        "H51_order": len(H),
        "additional_factor11_occurrences_to_saturate_H51": first_saturation,
        "total_v11_at_H51_saturation": EXPECTED_TOTAL_V11_SATURATION,
        "exact_state_period_after_saturation": EXPECTED_PERIOD,
        "cycle_start_additional_occurrences": first_saturation,
        "cycle_return_additional_occurrences": first_saturation + EXPECTED_PERIOD,
        "cycle_start_total_v11": first_saturation + 1,
        "cycle_return_total_v11": first_saturation + EXPECTED_PERIOD + 1,
        "all_saturated_cycle_states_are_combined_misses": True,
        "local_v11_ceiling": None,
        "prefix_and_one_cycle": prefix,
        "theorem": (
            "Inside the exact h169 t11=0 k51 Jacobi normal form, starting from "
            "the forced seed [5,11], four further factor11 occurrences saturate "
            "H51=<11>.  The exact combined-miss signed-box state then has period16 "
            "under further factor11 occurrences.  Hence local k51 geometry imposes "
            "no finite ceiling on v_11(C51)."
        ),
        "claim_boundary": (
            "This is an exact local residue-state persistence theorem.  It does not "
            "assert that h169 prime corridor candidates realize arbitrarily large "
            "v_11(C51); a global ancestry or neighboring-cofactor theorem may still "
            "forbid the persistent local cycle."
        ),
    }


def main() -> int:
    print(json.dumps(verify_cycle(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
