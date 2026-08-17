#!/usr/bin/env python3
"""Verify the h169 k11 phase child that forces factor11 at k=51.

Unlike k=43, the Lane-I modulus 51 is composite.  The correct local state space
is therefore the unit group U(51), not a cyclic prime-field exponent model.

For h169 write

    p = 169 + 840 t,
    T = (p+23)/24 = 8 + 35 t.

The landed k11 combined-miss theorem restricts

    t mod11 in {0,2,3,4,8}.

On t=0 mod11,

    C51 = (p+51)/4 = 6T+7 = 55+210t

is divisible by 11.  This verifier preloads one literal residue11 occurrence in
an exact signed-box automaton on U(51).

The important result is two-sided:

  * the seed contracts the complete local Type-II-miss closure;
  * but it also lies in an exact index-two Jacobi shield H=<11> of order16.

Every factorization supported entirely in H misses both Lane-I targets modulo
51.  Repeated residue11 reaches the full H support after eight occurrences and
then runs around an exact 16-state combined-miss cycle.  Thus local k51
geometry alone cannot bound the multiplicity of the forced factor11.
"""

from __future__ import annotations

import json
from collections import Counter, deque
from math import gcd
from pathlib import Path
from typing import Any
import sys

RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(RESEARCH))

import verify_h169_k11_future_factor_partition as future  # noqa: E402

MODULUS = 51
FORCED_FACTOR = 11
SELECTED_T11 = 0
EXPECTED = {
    "generic_states": 3337,
    "generic_combined": 1626,
    "generic_type_i_only": 1711,
    "seed_states": 636,
    "seed_combined": 268,
    "seed_type_i_only": 368,
    "shield_order": 16,
    "shield_saturation_exponent": 8,
    "shield_cycle_length": 16,
}


def legendre(a: int, prime: int) -> int:
    x = pow(a % prime, (prime - 1) // 2, prime)
    if x == 1:
        return 1
    if x == prime - 1:
        return -1
    return 0


def jacobi_51(a: int) -> int:
    if gcd(a, MODULUS) != 1:
        return 0
    return legendre(a, 3) * legendre(a, 17)


def units() -> tuple[int, ...]:
    return tuple(a for a in range(1, MODULUS) if gcd(a, MODULUS) == 1)


UNITS = units()
INDEX = {a: i for i, a in enumerate(UNITS)}
TARGET_II = MODULUS - 1
TARGET_II_INDEX = INDEX[TARGET_II]
ALPHABET = tuple(a for a in UNITS if a != 1)
INVERSES = {a: pow(a, -1, MODULUS) for a in UNITS}
PERM = {
    a: tuple(INDEX[(u * a) % MODULUS] for u in UNITS)
    for a in UNITS
}


def permute(mask: int, permutation: tuple[int, ...]) -> int:
    out = 0
    work = mask
    while work:
        bit = work & -work
        i = bit.bit_length() - 1
        out |= 1 << permutation[i]
        work -= bit
    return out


def transition(state: tuple[int, int], residue: int) -> tuple[int, int]:
    C, support = state
    plus = permute(support, PERM[residue])
    minus = permute(support, PERM[INVERSES[residue]])
    return ((C * residue) % MODULUS, support | plus | minus)


def contains(mask: int, residue: int) -> bool:
    return bool(mask & (1 << INDEX[residue]))


def support_residues(mask: int) -> set[int]:
    return {u for u in UNITS if contains(mask, u)}


def type_i_target(C: int) -> int:
    # p == 4C (mod51), so the Type-I target is -p^{-1}.
    return (-pow((4 * C) % MODULUS, -1, MODULUS)) % MODULUS


def state_class(state: tuple[int, int]) -> str:
    C, support = state
    if contains(support, TARGET_II):
        return "type-II-hit"
    if contains(support, type_i_target(C)):
        return "type-I-only"
    return "combined-miss"


def apply_seed(seed_residues: tuple[int, ...]) -> tuple[int, int]:
    state = (1, 1 << INDEX[1])
    for residue in seed_residues:
        if residue not in INDEX:
            raise ValueError(f"seed residue {residue} is not a unit modulo51")
        state = transition(state, residue)
    return state


def closure(seed_residues: tuple[int, ...]) -> dict[str, Any]:
    seed = apply_seed(seed_residues)
    if contains(seed[1], TARGET_II):
        raise SystemExit("forced seed already hits Type II")

    queue: deque[tuple[int, int]] = deque([seed])
    seen = {seed}
    depth = {seed: 0}
    pruned_type_ii = 0
    transitions_considered = 0

    while queue:
        state = queue.popleft()
        for residue in ALPHABET:
            transitions_considered += 1
            nxt = transition(state, residue)
            if contains(nxt[1], TARGET_II):
                pruned_type_ii += 1
                continue
            if nxt in seen:
                continue
            seen.add(nxt)
            depth[nxt] = depth[state] + 1
            queue.append(nxt)

    classes = Counter(state_class(state) for state in seen)
    support_sizes = Counter(state[1].bit_count() for state in seen)
    return {
        "seed_residues": list(seed_residues),
        "seed_state": seed,
        "TypeII_miss_states": len(seen),
        "combined_miss_states": classes["combined-miss"],
        "TypeI_only_states": classes["type-I-only"],
        "max_factor_occurrence_depth": max(depth.values()),
        "support_size_distribution": dict(sorted(support_sizes.items())),
        "transitions_considered": transitions_considered,
        "transitions_pruned_after_TypeII_hit": pruned_type_ii,
    }


def multiplicative_order(a: int) -> int:
    x = 1
    for n in range(1, 1000):
        x = x * a % MODULUS
        if x == 1:
            return n
    raise RuntimeError("multiplicative order not found")


def verify_phase() -> dict[str, Any]:
    obj = future.verify()
    allowed = obj["k11_combined_miss_implies_t_mod_11"]
    if allowed != [0, 2, 3, 4, 8]:
        raise SystemExit(f"h169 k11 phase domain changed: {allowed}")
    rows = [row for row in obj["partition"] if row["t_mod_11"] == SELECTED_T11]
    if len(rows) != 1:
        raise SystemExit("future factor partition lost t=0 mod11")
    row = rows[0]
    if row["shift_k"] != 51:
        raise SystemExit(f"t=0 mod11 no longer maps to k51: {row}")

    t11 = SELECTED_T11
    T11 = (8 + 35 * t11) % 11
    C51_11 = (6 * T11 + 7) % 11
    direct = (55 + 210 * t11) % 11
    if T11 != 8 or C51_11 != 0 or direct != 0:
        raise SystemExit(
            f"k51 phase algebra changed: T11={T11}, C51={C51_11}, direct={direct}"
        )

    return {
        "t_mod_11": t11,
        "T_mod_11": T11,
        "p_mod_11": row["p_mod_11"],
        "forced_factor": FORCED_FACTOR,
        "forced_shift": row["shift_k"],
        "forced_coordinate": "C51=(p+51)/4=6T+7=55+210t",
        "consequence": "11|C51",
    }


def verify_jacobi_shield() -> dict[str, Any]:
    if len(UNITS) != 32:
        raise SystemExit(f"phi(51) changed unexpectedly: {len(UNITS)}")
    order = multiplicative_order(FORCED_FACTOR)
    if order != EXPECTED["shield_order"]:
        raise SystemExit(f"ord_51(11) changed: {order}")

    H = {pow(FORCED_FACTOR, e, MODULUS) for e in range(order)}
    jacobi_plus = {u for u in UNITS if jacobi_51(u) == 1}
    if H != jacobi_plus:
        raise SystemExit("<11> is no longer the Jacobi +1 subgroup modulo51")

    minus_one = TARGET_II
    type_i_base = (-pow(4, -1, MODULUS)) % MODULUS
    if minus_one in H:
        raise SystemExit("-1 entered the shield subgroup")
    if type_i_base in H:
        raise SystemExit("-4^{-1} entered the shield subgroup")
    if jacobi_51(minus_one) != -1 or jacobi_51(type_i_base) != -1:
        raise SystemExit("target cosets lost negative Jacobi character")

    # Verify the general shield implication directly on every possible C in H:
    # a support subset of H can contain neither target.
    for C in H:
        target_i = type_i_target(C)
        if target_i in H:
            raise SystemExit(f"Type-I target entered H for C={C}")

    return {
        "unit_group_order": len(UNITS),
        "generator": FORCED_FACTOR,
        "generator_order": order,
        "H": sorted(H),
        "H_order": len(H),
        "H_index": len(UNITS) // len(H),
        "H_characterization": "kernel of Jacobi symbol (./51)",
        "jacobi_11": jacobi_51(FORCED_FACTOR),
        "TypeII_target": minus_one,
        "jacobi_TypeII_target": jacobi_51(minus_one),
        "TypeI_base_minus_inverse4": type_i_base,
        "jacobi_TypeI_base": jacobi_51(type_i_base),
        "shield_theorem": (
            "If every prime-factor residue of C lies in H=<11>=ker Jacobi(./51), "
            "then the signed-box support is contained in H, while -1 and "
            "-4^{-1}C^{-1} lie in the opposite coset; hence both Lane-I targets miss."
        ),
    }


def verify_repeated_11_cycle(shield: dict[str, Any]) -> dict[str, Any]:
    H = set(shield["H"])
    state = (1, 1 << INDEX[1])
    rows = []
    state_at: dict[int, tuple[int, int]] = {0: state}

    for exponent in range(1, 25):
        state = transition(state, FORCED_FACTOR)
        state_at[exponent] = state
        cls = state_class(state)
        if cls != "combined-miss":
            raise SystemExit(
                f"pure 11^{exponent} left combined-miss class: {cls}"
            )
        rows.append(
            {
                "exponent": exponent,
                "C_mod_51": state[0],
                "support_size": state[1].bit_count(),
                "class": cls,
            }
        )

    saturation = EXPECTED["shield_saturation_exponent"]
    saturated = state_at[saturation]
    if support_residues(saturated[1]) != H:
        raise SystemExit("eight factor11 occurrences no longer saturate H")
    cycle_length = EXPECTED["shield_cycle_length"]
    if state_at[saturation + cycle_length] != saturated:
        raise SystemExit("pure factor11 shield no longer has 16-state cycle")

    # Once H is saturated, another 11 only rotates C inside H and leaves the
    # full support H fixed.  Thus arbitrary further multiplicity is locally safe.
    return {
        "saturation_exponent": saturation,
        "support_at_saturation": sorted(H),
        "support_size_at_saturation": len(H),
        "cycle_length": cycle_length,
        "cycle_start_exponent": saturation,
        "cycle_return_exponent": saturation + cycle_length,
        "all_checked_states_combined_miss": True,
        "local_factor11_multiplicity_ceiling": None,
        "interpretation": (
            "repeated factor11 alone can remain a combined miss indefinitely modulo51; "
            "local k51 signed-box geometry supplies no factor11 valuation ceiling"
        ),
        "prefix": rows,
    }


def verify() -> dict[str, Any]:
    phase = verify_phase()
    generic = closure(())
    seeded = closure((FORCED_FACTOR,))

    if generic["TypeII_miss_states"] != EXPECTED["generic_states"]:
        raise SystemExit("generic q51 Type-II-miss closure changed")
    if generic["combined_miss_states"] != EXPECTED["generic_combined"]:
        raise SystemExit("generic q51 combined-miss count changed")
    if generic["TypeI_only_states"] != EXPECTED["generic_type_i_only"]:
        raise SystemExit("generic q51 Type-I-only count changed")
    if seeded["TypeII_miss_states"] != EXPECTED["seed_states"]:
        raise SystemExit("seed11 q51 Type-II-miss closure changed")
    if seeded["combined_miss_states"] != EXPECTED["seed_combined"]:
        raise SystemExit("seed11 q51 combined-miss count changed")
    if seeded["TypeI_only_states"] != EXPECTED["seed_type_i_only"]:
        raise SystemExit("seed11 q51 Type-I-only count changed")

    shield = verify_jacobi_shield()
    cycle = verify_repeated_11_cycle(shield)

    return {
        "verified": True,
        "mode": "h169-k11-phase-k51-composite-shield",
        "phase": phase,
        "unit_group": {
            "modulus": MODULUS,
            "order": len(UNITS),
            "structure": "U(51) via exact residue multiplication; no prime-field cyclic assumption",
        },
        "generic_q51": {
            k: v for k, v in generic.items() if k != "seed_state"
        },
        "seed11_q51": {
            k: v for k, v in seeded.items() if k != "seed_state"
        },
        "exact_contraction": {
            "TypeII_miss_state_ratio": (
                f"{seeded['TypeII_miss_states']}/{generic['TypeII_miss_states']}"
            ),
            "states_removed": (
                generic["TypeII_miss_states"] - seeded["TypeII_miss_states"]
            ),
        },
        "jacobi_shield": shield,
        "persistent_cycle": cycle,
        "theorem": (
            "For h169 under an inherited k11 combined miss, the child t=0 mod11 "
            "forces 11|C51.  The seed11 exact U(51) Type-II-miss closure has 636 "
            "states versus 3337 unseeded, but H=<11>=ker Jacobi(./51) is an "
            "index-two combined-miss shield.  Pure factor11 support saturates H "
            "after eight occurrences and then cycles with period16, so local k51 "
            "geometry cannot impose a finite factor11 multiplicity ceiling."
        ),
        "claim_boundary": (
            "Exact composite-modulus local theorem conditional on the inherited "
            "h169 k11 phase.  It does not assert t=0 is forced, that k51 is reached, "
            "that actual corridor candidates realize arbitrary factor11 valuations, "
            "or that a persistent local shield survives the full simultaneous "
            "cofactor ancestry."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
