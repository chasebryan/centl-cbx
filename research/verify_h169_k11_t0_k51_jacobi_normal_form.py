#!/usr/bin/env python3
"""Verify the exact h169 k11 t=0 mod11 -> k51 Jacobi normal form.

For h169,

    p = 169 + 840 t,
    C51 = (p+51)/4 = 55 + 210 t.

The exact h169 k11 miss theorem restricts t mod11 to {0,2,3,4,8}.  On the
child t=0 mod11, write t=11u.  Then

    C51 = 55(1+42u),

so literal factors 5 and11 are simultaneously forced into C51.

Let H51 be the index-two Jacobi kernel

    H51 = {r in U(51) : (r/3)(r/17)=+1}.

After stripping one forced occurrence of 5 and one of11, write

    C51 = 55 R.

This verifier proves by exact finite signed-box automaton that

    k51 combined miss  <=>  every prime-factor occurrence of R lies in H51.

The proof is word-level, not only state-level.  The Type-II-miss automaton
seeded by [5,11] has exactly 86 states.  Augmenting every state by a flag that
records whether any residual factor outside H51 has appeared gives:

    26 states with outside_used=False, all combined misses;
    60 states with outside_used=True,  all Type-I-only.

Any word that hits Type II is safely pruned because signed support is monotone.
Therefore no factorization containing an outside-H51 residual occurrence can
return to a combined miss.

The normal form also forces (p/17)=+1 on an h169 k51 miss, hence

    t mod17 in {0,2,8,10,11,12,15,16}.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "kernel"
RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(KERNEL))
sys.path.insert(0, str(RESEARCH))

import analyze_brec_cylinder as cylinder  # noqa: E402
import verify_h169_k11_future_factor_partition as future  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402

K = 51
HARD = 169
SELECTED_t11 = 0
UNITS = tuple(r for r in range(1, K) if math.gcd(r, K) == 1)

EXPECTED_H51 = frozenset(
    {1, 4, 5, 11, 13, 14, 16, 19, 20, 23, 25, 29, 41, 43, 44, 49}
)
EXPECTED_SEED_SUPPORT = frozenset({1, 4, 5, 11, 13, 14, 19, 41, 43})
EXPECTED_OUTSIDE_ONE_STEP = frozenset(
    {2, 7, 8, 10, 22, 26, 28, 31, 32, 35, 37, 38, 40, 46, 47, 50}
)
EXPECTED_ALLOWED_t17 = [0, 2, 8, 10, 11, 12, 15, 16]

REGRESSIONS = {
    55_609: "miss",
    64_849: "both",
    231_169: "type-I-only",
    379_009: "type-II-only",
}


@dataclass(frozen=True)
class State:
    center: int
    support: int


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def jacobi51(r: int) -> int:
    if math.gcd(r, K) != 1:
        raise ValueError(f"Jacobi character requires a unit mod51: {r}")
    return legendre(r, 3) * legendre(r, 17)


def h51() -> frozenset[int]:
    H = frozenset(r for r in UNITS if jacobi51(r) == 1)
    if H != EXPECTED_H51:
        raise SystemExit(f"H51 changed: {sorted(H)}")
    if len(H) != 16:
        raise SystemExit("H51 is not index two in U(51)")
    if not all(a * b % K in H for a in H for b in H):
        raise SystemExit("H51 is not multiplicatively closed")
    if not all(pow(a, -1, K) in H for a in H):
        raise SystemExit("H51 is not inverse closed")
    return H


def multiply_mask(mask: int, r: int) -> int:
    out = 0
    for x in range(K):
        if mask & (1 << x):
            out |= 1 << ((x * r) % K)
    return out


def transition(state: State, r: int) -> State:
    if math.gcd(r, K) != 1:
        raise ValueError(f"transition residue is not a unit mod51: {r}")
    inv = pow(r, -1, K)
    support = (
        state.support
        | multiply_mask(state.support, r)
        | multiply_mask(state.support, inv)
    )
    return State(state.center * r % K, support)


def seed_state(residues: tuple[int, ...]) -> State:
    state = State(1, 1 << 1)
    for residue in residues:
        state = transition(state, residue % K)
    return state


def support_values(state: State) -> frozenset[int]:
    return frozenset(x for x in range(K) if state.support & (1 << x))


def targets(state: State) -> tuple[int, int]:
    p_residue = 4 * state.center % K
    if math.gcd(p_residue, K) != 1:
        raise SystemExit(f"non-unit p residue in exact k51 state: {p_residue}")
    type_i = (-pow(p_residue, -1, K)) % K
    type_ii = K - 1
    return type_i, type_ii


def state_class(state: State) -> str:
    type_i, type_ii = targets(state)
    hit_i = bool(state.support & (1 << type_i))
    hit_ii = bool(state.support & (1 << type_ii))
    if hit_i and hit_ii:
        return "both"
    if hit_i:
        return "type-I-only"
    if hit_ii:
        return "type-II-only"
    return "miss"


def type_ii_miss_closure(
    seed_residues: tuple[int, ...],
    alphabet: tuple[int, ...] = UNITS,
) -> tuple[set[State], dict[State, int]]:
    start = seed_state(seed_residues)
    if state_class(start) in {"type-II-only", "both"}:
        raise SystemExit(f"seed {seed_residues} already hits Type II")

    queue: deque[State] = deque([start])
    seen = {start}
    depth = {start: 0}
    for_alphabet = tuple(r for r in alphabet if r != 1)

    while queue:
        state = queue.popleft()
        for r in for_alphabet:
            nxt = transition(state, r)
            if nxt.support & (1 << (K - 1)):
                continue
            if nxt in seen:
                continue
            seen.add(nxt)
            depth[nxt] = depth[state] + 1
            queue.append(nxt)
    return seen, depth


def verify_seed_geometry() -> dict[str, Any]:
    H = h51()
    seed5 = seed_state((5,))
    seed11 = seed_state((11,))
    seed55 = seed_state((5, 11))

    if support_values(seed5) != frozenset({1, 5, 41}):
        raise SystemExit("factor5 seed support changed")
    if support_values(seed11) != frozenset({1, 11, 14}):
        raise SystemExit("factor11 seed support changed")
    if seed55.center != 4:
        raise SystemExit(f"seed55 center {seed55.center} !=4 mod51")
    if support_values(seed55) != EXPECTED_SEED_SUPPORT:
        raise SystemExit(f"seed55 support changed: {sorted(support_values(seed55))}")
    if not support_values(seed55).issubset(H):
        raise SystemExit("seed55 support escaped H51")
    if 50 in H:
        raise SystemExit("Type-II target unexpectedly lies in H51")

    # For H-supported residual factors, center remains in H, hence p=4C is in
    # H because 4 is in H.  The Type-I target -p^-1 is therefore outside H.
    if 4 not in H or jacobi51(50) != -1:
        raise SystemExit("H51 target-character setup changed")

    return {
        "H51": sorted(H),
        "H51_size": len(H),
        "seed5_support": sorted(support_values(seed5)),
        "seed11_support": sorted(support_values(seed11)),
        "seed55_center": seed55.center,
        "seed55_support": sorted(support_values(seed55)),
        "Type_II_target": 50,
        "Jacobi_Type_II_target": jacobi51(50),
    }


def verify_full_seeded_closure() -> dict[str, Any]:
    states, depth = type_ii_miss_closure((5, 11))
    classes = Counter(state_class(state) for state in states)
    if len(states) != 86:
        raise SystemExit(f"seed55 Type-II-miss closure {len(states)} !=86")
    if classes != Counter({"type-I-only": 60, "miss": 26}):
        raise SystemExit(f"seed55 class split changed: {classes}")
    if max(depth.values()) != 3:
        raise SystemExit(f"seed55 max minimal depth {max(depth.values())} !=3")

    combined_centers = {state.center for state in states if state_class(state) == "miss"}
    if combined_centers != set(EXPECTED_H51):
        raise SystemExit(
            f"seed55 combined centers are not exactly H51: {sorted(combined_centers)}"
        )

    return {
        "type_II_miss_states": len(states),
        "combined_miss_states": classes["miss"],
        "type_I_only_states": classes["type-I-only"],
        "max_minimal_residual_factor_occurrences": max(depth.values()),
        "combined_center_residues": sorted(combined_centers),
    }


def verify_h_only_sufficiency() -> dict[str, Any]:
    H = h51()
    states, depth = type_ii_miss_closure((5, 11), tuple(sorted(H)))
    classes = Counter(state_class(state) for state in states)
    if len(states) != 26 or classes != Counter({"miss": 26}):
        raise SystemExit(f"H51-only closure changed: states={len(states)}, classes={classes}")
    for state in states:
        if not support_values(state).issubset(H):
            raise SystemExit("H51-only transition escaped H51 support")
        type_i, type_ii = targets(state)
        if type_i in H or type_ii in H:
            raise SystemExit("H51-only state has a target inside H51")

    return {
        "H51_only_states": len(states),
        "all_H51_only_states_are_combined_misses": True,
        "max_minimal_residual_factor_occurrences": max(depth.values()),
        "reason": (
            "seed support lies in H51; H51 is a subgroup; both targets lie in "
            "the opposite Jacobi coset whenever the residual support stays in H51"
        ),
    }


def verify_outside_h_necessity() -> dict[str, Any]:
    H = h51()
    start = seed_state((5, 11))
    queue: deque[tuple[State, bool]] = deque([(start, False)])
    seen = {(start, False)}
    class_flag: Counter[tuple[str, bool]] = Counter()

    while queue:
        state, outside_used = queue.popleft()
        class_flag[(state_class(state), outside_used)] += 1
        for r in UNITS:
            if r == 1:
                continue
            nxt = transition(state, r)
            # Type II is monotone in signed support, so once hit it can never
            # return to a combined miss.  Pruning is theorem-safe.
            if nxt.support & (1 << (K - 1)):
                continue
            flagged = outside_used or (r not in H)
            item = (nxt, flagged)
            if item in seen:
                continue
            seen.add(item)
            queue.append(item)

    expected = Counter({("miss", False): 26, ("type-I-only", True): 60})
    if class_flag != expected:
        raise SystemExit(f"outside-H flagged closure changed: {class_flag}")
    if len(seen) != 86:
        raise SystemExit(f"flagged closure {len(seen)} !=86")

    # Freeze the immediate shell as a human-readable first obstruction layer.
    start = seed_state((5, 11))
    one_step: Counter[str] = Counter()
    outside_nonmiss: set[int] = set()
    for r in UNITS:
        if r == 1:
            continue
        cls = state_class(transition(start, r))
        one_step[cls] += 1
        if r not in H and cls != "miss":
            outside_nonmiss.add(r)
    if outside_nonmiss != set(EXPECTED_OUTSIDE_ONE_STEP):
        raise SystemExit(f"outside-H one-step shell changed: {sorted(outside_nonmiss)}")
    if one_step != Counter(
        {"miss": 15, "type-I-only": 7, "type-II-only": 7, "both": 2}
    ):
        raise SystemExit(f"seed55 one-step class split changed: {one_step}")

    return {
        "flagged_Type_II_miss_states": len(seen),
        "combined_miss_with_no_outside_H51_factor": 26,
        "combined_miss_with_outside_H51_factor": 0,
        "type_I_only_with_outside_H51_factor": 60,
        "one_step_class_split": dict(sorted(one_step.items())),
        "one_step_outside_H51_residues": sorted(outside_nonmiss),
        "word_level_consequence": (
            "Within the complete Type-II-miss automaton, every word that ever uses "
            "a residual factor outside H51 ends Type-I-only; no such word reaches "
            "a combined miss."
        ),
    }


def verify_phase_bridge() -> dict[str, Any]:
    partition = future.verify()
    if partition["k11_combined_miss_implies_t_mod_11"] != [0, 2, 3, 4, 8]:
        raise SystemExit("h169 k11 t mod11 phase domain changed")
    row = next(
        row for row in partition["partition"]
        if row["t_mod_11"] == SELECTED_t11
    )
    if row["T_mod_11"] != 8 or row["shift_k"] != 51:
        raise SystemExit(f"selected t11=0 future row changed: {row}")

    # Direct h169 arithmetic is stronger than the generic factor11 calendar:
    # C51=55+210t, and t=11u makes C51=55(1+42u).
    for u in range(17 * 11):
        t = 11 * u
        p = 169 + 840 * t
        C51 = (p + 51) // 4
        if C51 != 55 * (1 + 42 * u):
            raise SystemExit("h169 t11=0 C51 factorization identity failed")

    return {
        "t_mod_11": 0,
        "T_mod_11": 8,
        "C51_identity": "if t=11u then C51=55(1+42u)",
        "forced_factor_occurrences": [5, 11],
        "residual_name": "R=C51/55=1+42u",
    }


def verify_t17_phase_consequence() -> dict[str, Any]:
    H = h51()
    qr17 = {pow(x, 2, 17) for x in range(1, 17)}

    # p=169+840t is always 1 mod3.  If k51 misses, center C51 lies in H51 and
    # therefore p=4C51 lies in H51.  Since (p/3)=+1, this means (p/17)=+1.
    if 169 % 3 != 1 or 840 % 3 != 0:
        raise SystemExit("h169 p mod3 setup changed")
    if 4 not in H:
        raise SystemExit("multiplier4 left H51")

    allowed = [
        t for t in range(17)
        if (169 + 840 * t) % 17 in qr17
    ]
    zero = [
        t for t in range(17)
        if (169 + 840 * t) % 17 == 0
    ]
    if allowed != EXPECTED_ALLOWED_t17:
        raise SystemExit(f"h169 k51 Jacobi t17 phases changed: {allowed}")
    if zero != [5]:
        raise SystemExit(f"h169 p divisible17 phase changed: {zero}")

    return {
        "combined_miss_implies_Legendre_p_mod_17": 1,
        "combined_miss_allowed_t_mod_17": allowed,
        "prime_forbidden_p_divisible_17_t_mod_17": 5,
        "prime_admissible_t17_phases_before_k51_character": 16,
        "t17_phases_after_k51_combined_miss": len(allowed),
        "prime_admissible_phase_fraction_retained": "1/2",
    }


def residual_all_h51(C51: int) -> tuple[int, bool, str]:
    if C51 % 55:
        raise SystemExit(f"C51={C51}: expected seed55 divisibility")
    residual = C51 // 55
    factors = cylinder.factorint(residual)
    all_h = all(prime % K in EXPECTED_H51 for prime in factors)
    return residual, all_h, cylinder.factor_text(factors)


def regression(p: int, expected_class: str) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: regression witness is not prime")
    if p % 840 != HARD:
        raise SystemExit(f"p={p}: hard class {p % 840} !=169")
    t = (p - 169) // 840
    if t % 11 != 0:
        raise SystemExit(f"p={p}: t mod11={t % 11} !=0")

    stage11 = ancestry.classify_stage(p, 11)
    if stage11["hit_class"] != "miss":
        raise SystemExit(f"p={p}: k11 class {stage11['hit_class']} !=miss")
    stage51 = ancestry.classify_stage(p, 51)
    if stage51["hit_class"] != expected_class:
        raise SystemExit(
            f"p={p}: k51 class {stage51['hit_class']} !={expected_class}"
        )

    C51 = int(stage51["C"])
    residual, all_h, residual_factorization = residual_all_h51(C51)
    if (expected_class == "miss") != all_h:
        raise SystemExit(
            f"p={p}: arithmetic regression violates exact H51 support normal form"
        )

    return {
        "p": p,
        "t_mod_11": t % 11,
        "t_mod_17": t % 17,
        "p_mod_17": p % 17,
        "C51": C51,
        "C51_factorization": stage51["factorization"],
        "R": residual,
        "R_factorization": residual_factorization,
        "all_residual_prime_support_in_H51": all_h,
        "k11_hit_class": stage11["hit_class"],
        "k51_hit_class": stage51["hit_class"],
    }


def verify() -> dict[str, Any]:
    phase = verify_phase_bridge()
    seed = verify_seed_geometry()
    full = verify_full_seeded_closure()
    sufficiency = verify_h_only_sufficiency()
    necessity = verify_outside_h_necessity()
    t17 = verify_t17_phase_consequence()
    witnesses = [regression(p, cls) for p, cls in REGRESSIONS.items()]

    return {
        "verified": True,
        "mode": "h169-k11-t0-k51-jacobi-normal-form",
        "phase": phase,
        "seed_geometry": seed,
        "full_seeded_Type_II_miss_closure": full,
        "H51_sufficiency": sufficiency,
        "outside_H51_necessity": necessity,
        "t17_phase_consequence": t17,
        "regressions": witnesses,
        "theorem": (
            "For h169 under inherited k11 miss on t=0 mod11, write C51=55R. "
            "Then k51 is a combined miss iff every prime-factor occurrence of R "
            "lies in H51={r in U(51):(r/3)(r/17)=+1}.  Consequently any such "
            "miss has (p/17)=+1 and t mod17 in {0,2,8,10,11,12,15,16}."
        ),
        "claim_boundary": (
            "Exact phase-conditioned k51 normal form.  It does not say k11 miss "
            "forces t=0 mod11, does not eliminate the H51 support branch, does not "
            "establish a finite Lane-I ceiling, and does not prove Erdos-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
