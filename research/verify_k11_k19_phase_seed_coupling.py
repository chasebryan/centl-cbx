#!/usr/bin/env python3
"""Verify an exact k11 -> k19 cross-coordinate seed coupling.

In hard classes 169, 289, and 529, the class-conditioned k11 theorem says a
combined miss is pure quadratic-residue splitting modulo 11.  On the q23
parameter T=(p+23)/24,

    C11 = 3*(2*T-1).

Since 3 is QR modulo 11, k11 miss forces 2*T-1 to be QR modulo 11.  Therefore

    T mod11 in {1,2,3,5,8}.

On the phase T==2 mod11,

    C19 = 6*T-1 == 0 mod11,

so literal prime 11 is forced into C19.  Modulo 19, 11 has order 3 and
log_2(11)=12, hence one occurrence supplies exponent subgroup

    K={0,6,12}.

This is the same K-periodic k19 seed used by the h289 forced factor 7.  Exact
Type-II-miss behavior therefore factors through Z/18Z/K ~= Z/6Z and has the
same 9-state quotient (6 combined misses, 3 Type-I-only).

The result is especially useful for h169 and h529, whose hard class alone has
no forced 5/7 k19 seed.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, deque
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

QR11 = {1, 3, 4, 5, 9}
HARD_CLASSES = {169, 289, 529}
ALLOWED_T11 = {1, 2, 3, 5, 8}
K19 = {0, 6, 12}

REGRESSIONS = {
    53_089: "both",
    71_569: "type-II-only",
    80_809: "miss",
    5_569: "miss",
}


def derive_allowed_t11() -> list[int]:
    inv2 = pow(2, -1, 11)
    allowed = sorted(((r + 1) * inv2) % 11 for r in QR11)
    if set(allowed) != ALLOWED_T11:
        raise SystemExit(f"allowed T mod11 set changed: {allowed}")
    for t in range(11):
        condition = (2 * t - 1) % 11 in QR11
        if condition != (t in ALLOWED_T11):
            raise SystemExit(f"T={t}: phase selector equivalence failed")
    return allowed


def multiplicative_order(a: int, q: int) -> int:
    x = 1
    for n in range(1, q):
        x = x * a % q
        if x == 1:
            return n
    raise RuntimeError("multiplicative order not found")


def mask_values(mask: int, n: int) -> set[int]:
    return {x for x in range(n) if mask & (1 << x)}


def quotient_projection(state: auto.State) -> tuple[int, frozenset[int]]:
    return (
        state.c_exp % 6,
        frozenset(x % 6 for x in mask_values(state.support, 18)),
    )


def quotient_class(projected: tuple[int, frozenset[int]]) -> str:
    cbar, support = projected
    if 3 in support:
        return "type-II-hit"
    target_i = (1 - cbar) % 6
    return "type-I-only" if target_i in support else "combined-miss"


def seeded_full_closure(seed_residue: int) -> dict[auto.State, int]:
    g = auto.primitive_root(19)
    logs = auto.log_table(19, g)
    seed, _ = auto.apply_seed(19, logs, [seed_residue])
    if mask_values(seed.support, 18) != K19:
        raise SystemExit(
            f"seed {seed_residue}: support is not order-three subgroup K"
        )

    log_minus_one = logs[18]
    queue: deque[auto.State] = deque([seed])
    depth = {seed: 0}
    while queue:
        state = queue.popleft()
        for a in range(1, 18):
            nxt = auto.transition(state, a, 18)
            if auto.contains(nxt.support, log_minus_one):
                continue
            if nxt in depth:
                continue
            depth[nxt] = depth[state] + 1
            queue.append(nxt)
    return depth


def verify_order_three_seed_equivalence() -> dict[str, Any]:
    g = auto.primitive_root(19)
    logs = auto.log_table(19, g)
    if g != 2:
        raise SystemExit(f"q19 primitive root changed from 2 to {g}")
    if logs[7] != 6 or logs[11] != 12:
        raise SystemExit(
            f"unexpected q19 logs: log2(7)={logs[7]}, log2(11)={logs[11]}"
        )
    if multiplicative_order(7, 19) != 3 or multiplicative_order(11, 19) != 3:
        raise SystemExit("7 or 11 lost order three modulo 19")

    closures = {r: seeded_full_closure(r) for r in (7, 11)}
    summaries = {}
    projected_sets = {}
    for residue, depth in closures.items():
        if len(depth) != 27:
            raise SystemExit(f"seed {residue}: full Type-II-miss closure !=27")
        projected = {quotient_projection(state) for state in depth}
        if len(projected) != 9:
            raise SystemExit(f"seed {residue}: quotient closure !=9")
        counts = Counter(quotient_class(state) for state in projected)
        if counts != Counter({"combined-miss": 6, "type-I-only": 3}):
            raise SystemExit(f"seed {residue}: quotient split changed: {counts}")
        full_counts = Counter(
            quotient_class(quotient_projection(state)) for state in depth
        )
        if full_counts != Counter({"combined-miss": 18, "type-I-only": 9}):
            raise SystemExit(f"seed {residue}: full split changed: {full_counts}")
        projected_sets[residue] = projected
        summaries[residue] = {
            "full_states": len(depth),
            "quotient_states": len(projected),
            "quotient_combined_miss": counts["combined-miss"],
            "quotient_type_I_only": counts["type-I-only"],
            "full_combined_miss": full_counts["combined-miss"],
            "full_type_I_only": full_counts["type-I-only"],
        }

    if projected_sets[7] != projected_sets[11]:
        raise SystemExit("seed7 and seed11 quotient state identities differ")

    public11 = auto.classify(19, [11], 500_000, 16)
    if (
        public11["type_II_miss_states"],
        public11["combined_miss_states"],
        public11["type_I_only_states"],
    ) != (27, 18, 9):
        raise SystemExit("generic seed11 automaton disagrees")

    table = []
    for cbar, support in sorted(
        projected_sets[11], key=lambda s: (s[0], tuple(sorted(s[1])))
    ):
        table.append(
            {
                "cbar": cbar,
                "support": sorted(support),
                "type_I_target": (1 - cbar) % 6,
                "class": quotient_class((cbar, support)),
            }
        )

    return {
        "primitive_root": g,
        "log2_7": logs[7],
        "log2_11": logs[11],
        "K": sorted(K19),
        "seed7": summaries[7],
        "seed11": summaries[11],
        "quotient_state_identities_equal": True,
        "quotient_table": table,
    }


def regression(p: int, expected_hit_class: str) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: regression witness is not prime")
    hard = p % 840
    if hard not in HARD_CLASSES:
        raise SystemExit(f"p={p}: hard class {hard} outside theorem domain")
    T = (p + 23) // 24
    if T % 11 != 2:
        raise SystemExit(f"p={p}: T mod11={T % 11} !=2")

    stage11 = ancestry.classify_stage(p, 11)
    if stage11["sign"] != "-":
        raise SystemExit(f"p={p}: k11 is not a combined miss")
    C11 = int(stage11["C"])
    if not all(q % 11 in QR11 for q in cylinder.factorint(C11)):
        raise SystemExit(f"p={p}: class-conditioned k11 miss is not pure QR")

    stage19 = ancestry.classify_stage(p, 19)
    if stage19["hit_class"] != expected_hit_class:
        raise SystemExit(
            f"p={p}: k19 class {stage19['hit_class']} != {expected_hit_class}"
        )
    C19 = int(stage19["C"])
    if C19 % 11:
        raise SystemExit(f"p={p}: phase T=2 mod11 did not force 11|C19")

    return {
        "p": p,
        "p_mod_840": hard,
        "T_mod_11": T % 11,
        "C11": C11,
        "C19": C19,
        "C19_factorization": cylinder.factor_text(cylinder.factorint(C19)),
        "k19_hit_class": stage19["hit_class"],
    }


def verify() -> dict[str, Any]:
    allowed = derive_allowed_t11()

    # On the selected phase, literal prime 11 enters C19.
    if (6 * 2 - 1) % 11 != 0:
        raise SystemExit("T=2 mod11 no longer forces 11|C19")

    seed = verify_order_three_seed_equivalence()
    regressions = [regression(p, cls) for p, cls in REGRESSIONS.items()]

    return {
        "verified": True,
        "mode": "k11-k19-phase-seed-coupling",
        "hard_classes": sorted(HARD_CLASSES),
        "k11_miss_forces_T_mod11": allowed,
        "selected_phase": 2,
        "selected_phase_consequence": "11 | C19=6T-1",
        "k19_order_three_seed": seed,
        "theorem": (
            "For hard classes 169,289,529, k11 miss forces T mod11 into "
            "{1,2,3,5,8}.  On phase T=2 mod11, literal factor11 enters C19 and "
            "forces the same exact 9-state Z/6 quotient as the h289 factor7 seed."
        ),
        "regressions": regressions,
        "claim_boundary": (
            "Exact cross-coordinate phase/seed implication.  It does not assert that "
            "the selected phase is forced by k11 miss, nor that all quotient states "
            "are realized after full ancestry, nor prove Erdos-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
