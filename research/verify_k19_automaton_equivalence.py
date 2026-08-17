#!/usr/bin/env python3
"""Cross-verify the two independently written exact k=19 state automata.

The repository now contains two complementary implementations of the same
local signed-box geometry:

1. verify_k19_brec_state_compression.py enumerates the full exact (c,S)
   closure, including states that already hit Type II.
2. classify_signed_box_residue_automaton.py enumerates only the Type-II-miss
   closure, pruning a transition permanently once exponent 9 (-1) appears.

For q=19 both choose primitive root 2, so their state coordinates should agree
bit-for-bit.  This verifier reconstructs the second closure directly from its
public transition functions and compares it to the Type-II-miss subset of the
first closure.

Exact result:

    full closure                         439 states
    Type-II-miss closure                 254 states
      combined miss                      136 states
      Type-I-only                        118 states

The canonical/minimal state depths also agree state-by-state.  This is an
implementation equivalence check, not a new Erdős-Straus coverage theorem.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(RESEARCH))

import classify_signed_box_residue_automaton as generic  # noqa: E402
import verify_k19_brec_state_compression as full  # noqa: E402

Q = 19
N = 18
TYPE_II_EXP = 9


def generic_closure() -> tuple[dict[tuple[int, int], int], int, dict[int, int]]:
    g = generic.primitive_root(Q)
    if g != 2:
        raise SystemExit(f"generic q19 primitive root changed: {g}")
    logs = generic.log_table(Q, g)
    if logs[Q - 1] != TYPE_II_EXP:
        raise SystemExit("generic q19 log(-1) is not exponent 9")

    start = generic.State(0, 1)
    queue: deque[generic.State] = deque([start])
    depth: dict[generic.State, int] = {start: 0}

    while queue:
        state = queue.popleft()
        for a in range(1, N):
            nxt = generic.transition(state, a, N)
            if generic.contains(nxt.support, TYPE_II_EXP):
                continue
            if nxt in depth:
                continue
            depth[nxt] = depth[state] + 1
            queue.append(nxt)

    return (
        {(s.c_exp, s.support): d for s, d in depth.items()},
        g,
        logs,
    )


def classify_type_i(c: int, mask: int) -> str:
    # At q=19 with g=2: log(-1)=9, log(4)=2, so Type-I exponent is 7-c.
    target_i = (7 - c) % N
    if mask & (1 << target_i):
        return "type-I-only"
    return "combined-miss"


def verify() -> dict[str, Any]:
    full_depth, _ = full.closure()
    if len(full_depth) != 439:
        raise SystemExit(f"full k19 closure changed: {len(full_depth)} != 439")

    filtered = {
        (c, mask): depth
        for (c, mask), depth in full_depth.items()
        if not (mask & (1 << TYPE_II_EXP))
    }
    generic_depth, generator, logs = generic_closure()

    full_keys = set(filtered)
    generic_keys = set(generic_depth)
    if full_keys != generic_keys:
        only_full = sorted(full_keys - generic_keys)[:20]
        only_generic = sorted(generic_keys - full_keys)[:20]
        raise SystemExit(
            "q19 automaton state-set mismatch: "
            f"only_full={only_full} only_generic={only_generic}"
        )

    depth_mismatches = [
        {
            "c": c,
            "support": mask,
            "full_depth": filtered[(c, mask)],
            "generic_depth": generic_depth[(c, mask)],
        }
        for c, mask in sorted(full_keys)
        if filtered[(c, mask)] != generic_depth[(c, mask)]
    ]
    if depth_mismatches:
        raise SystemExit(f"q19 canonical-depth mismatch: {depth_mismatches[:10]}")

    classes = Counter(classify_type_i(c, mask) for c, mask in full_keys)
    if classes != Counter({"combined-miss": 136, "type-I-only": 118}):
        raise SystemExit(f"unexpected q19 Type-II-miss class split: {classes}")

    generic_summary = generic.classify(19, [], 500_000, 8)
    if generic_summary["type_II_miss_states"] != len(generic_keys):
        raise SystemExit("generic public summary disagrees with reconstructed closure")
    if generic_summary["combined_miss_states"] != classes["combined-miss"]:
        raise SystemExit("generic public combined-miss count disagrees")
    if generic_summary["type_I_only_states"] != classes["type-I-only"]:
        raise SystemExit("generic public Type-I-only count disagrees")

    depth_hist = Counter(generic_depth.values())
    class_depth: dict[str, Counter[int]] = {
        "combined-miss": Counter(),
        "type-I-only": Counter(),
    }
    support_hist: dict[str, Counter[int]] = {
        "combined-miss": Counter(),
        "type-I-only": Counter(),
    }
    for (c, mask), depth in generic_depth.items():
        cls = classify_type_i(c, mask)
        class_depth[cls][depth] += 1
        support_hist[cls][mask.bit_count()] += 1

    # The full implementation's miss predicate must select exactly the same
    # 136 states, not merely the same count.
    full_combined = {
        (c, mask)
        for c, mask in full_keys
        if full.is_combined_miss(c, mask)
    }
    classified_combined = {
        (c, mask)
        for c, mask in full_keys
        if classify_type_i(c, mask) == "combined-miss"
    }
    if full_combined != classified_combined:
        raise SystemExit("independent combined-miss state identities disagree")

    return {
        "verified": True,
        "mode": "k19-automaton-equivalence",
        "modulus": Q,
        "primitive_root": generator,
        "group_order": N,
        "full_reachable_states": len(full_depth),
        "type_II_miss_states": len(generic_keys),
        "combined_miss_states": classes["combined-miss"],
        "type_I_only_states": classes["type-I-only"],
        "state_sets_identical": True,
        "minimal_depths_identical": True,
        "combined_miss_identities_identical": True,
        "type_II_miss_depth_distribution": {
            str(k): depth_hist[k] for k in sorted(depth_hist)
        },
        "combined_miss_depth_distribution": {
            str(k): class_depth["combined-miss"][k]
            for k in sorted(class_depth["combined-miss"])
        },
        "type_I_only_depth_distribution": {
            str(k): class_depth["type-I-only"][k]
            for k in sorted(class_depth["type-I-only"])
        },
        "combined_miss_support_distribution": {
            str(k): support_hist["combined-miss"][k]
            for k in sorted(support_hist["combined-miss"])
        },
        "type_I_only_support_distribution": {
            str(k): support_hist["type-I-only"][k]
            for k in sorted(support_hist["type-I-only"])
        },
        "generic_public_summary": {
            "type_II_miss_states": generic_summary["type_II_miss_states"],
            "combined_miss_states": generic_summary["combined_miss_states"],
            "type_I_only_states": generic_summary["type_I_only_states"],
        },
        "claim_boundary": (
            "Independent exact implementation equivalence for the local q=19 "
            "signed-box state space.  It does not assert arithmetic realization "
            "of every abstract state and does not prove Erdős-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
