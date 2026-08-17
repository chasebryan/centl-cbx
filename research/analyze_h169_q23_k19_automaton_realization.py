#!/usr/bin/env python3
"""Map the h169 q23 Type-I rescue frontier into the exact q=19 residue automaton.

The unseeded q=19 signed-box residue automaton exhausts every abstract local
factor-residue/multiplicity state that can still miss Type II.  This analyzer
then asks which of those exact local states are actually realized by the much
smaller arithmetic family

    p = 24M - 23,
    p == 169 (mod 840),
    q23 Type-I-only defect 5^2 or 14^2,

optionally after a required anchored early BREC prefix (default '----').

This creates a clean separation:

  local possibility  = exact finite q19 automaton,
  arithmetic reality = q23 rescue branch + earlier exact BREC constraints.

Finite non-realization is not promoted to a theorem.  Exact automaton
non-reachability is a genuine local impossibility.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parent
KERNEL = RESEARCH.parent / "kernel"
sys.path.insert(0, str(RESEARCH))
sys.path.insert(0, str(KERNEL))

import analyze_brec_cylinder as cylinder  # noqa: E402
import classify_signed_box_residue_automaton as auto  # noqa: E402
import search_q23_typei_rescue_branch as rescue  # noqa: E402

Q = 19
HARD_CLASS = 169
HARD_M_CLASS = 8


def build_q19_typeii_miss_closure() -> tuple[
    set[auto.State],
    dict[auto.State, tuple[auto.State, int] | None],
    dict[auto.State, int],
    dict[int, int],
    int,
    int,
]:
    g = auto.primitive_root(Q)
    logs = auto.log_table(Q, g)
    n = Q - 1
    log_minus_one = logs[Q - 1]

    start = auto.State(0, 1)
    queue: deque[auto.State] = deque([start])
    seen = {start}
    parent: dict[auto.State, tuple[auto.State, int] | None] = {start: None}
    depth = {start: 0}

    while queue:
        state = queue.popleft()
        for a in range(1, n):
            nxt = auto.transition(state, a, n)
            if auto.contains(nxt.support, log_minus_one):
                continue
            if nxt in seen:
                continue
            seen.add(nxt)
            parent[nxt] = (state, a)
            depth[nxt] = depth[state] + 1
            queue.append(nxt)

    return seen, parent, depth, logs, g, log_minus_one


def factorization_state(C: int, logs: dict[int, int]) -> auto.State:
    state = auto.State(0, 1)
    n = Q - 1
    factors = cylinder.factorint(C)
    for prime, exponent in sorted(factors.items()):
        residue = prime % Q
        if residue == 0:
            raise ValueError(f"C={C}: factor 19 makes Lane-I stage undefined")
        a = logs[residue]
        for _ in range(exponent):
            state = auto.transition(state, a, n)
    return state


def state_id(state: auto.State) -> str:
    return f"A{state.c_exp}:S{state.support:x}"


def type_i_target_exp(state: auto.State, logs: dict[int, int]) -> int:
    return (logs[Q - 1] - logs[4] - state.c_exp) % (Q - 1)


def state_class(state: auto.State, logs: dict[int, int]) -> str:
    if auto.contains(state.support, logs[Q - 1]):
        return "type-II-hit"
    target_i = type_i_target_exp(state, logs)
    if auto.contains(state.support, target_i):
        return "type-I-only"
    return "combined-miss"


def representative_added_residues(
    state: auto.State,
    parent: dict[auto.State, tuple[auto.State, int] | None],
    g: int,
) -> list[int]:
    exps: list[int] = []
    cur = state
    while parent[cur] is not None:
        prev, a = parent[cur]  # type: ignore[misc]
        exps.append(a)
        cur = prev
    exps.reverse()
    return [pow(g, a, Q) for a in exps]


def describe_state(
    state: auto.State,
    logs: dict[int, int],
    g: int,
    parent: dict[auto.State, tuple[auto.State, int] | None],
    depth: dict[auto.State, int],
) -> dict[str, Any]:
    target_i_exp = type_i_target_exp(state, logs)
    support_exps = auto.exponents(state.support, Q - 1)
    return {
        "state_id": state_id(state),
        "class": state_class(state, logs),
        "minimal_abstract_factor_occurrences": depth.get(state),
        "minimal_abstract_residue_word": representative_added_residues(state, parent, g)
        if state in parent
        else None,
        "C_mod_19": pow(g, state.c_exp, Q),
        "p_mod_19": (4 * pow(g, state.c_exp, Q)) % Q,
        "support_size": state.support.bit_count(),
        "support_exponents": support_exps,
        "support_residues": sorted(pow(g, e, Q) for e in support_exps),
        "type_II_target": 18,
        "type_I_target": pow(g, target_i_exp, Q),
    }


def analyze(p_hi: int, prefix: str, max_results: int) -> dict[str, Any]:
    if any(ch not in "+-" for ch in prefix) or len(prefix) > 5:
        raise SystemExit("--prefix must be a +/- word of length at most 5")

    closure, parent, depth, logs, g, _ = build_q19_typeii_miss_closure()
    abstract_classes = Counter(state_class(state, logs) for state in closure)

    # The exact hard-class map p=169 mod840 <=> M=8 mod35 lets us scan only
    # the h169 arithmetic progression in M rather than all six hard classes.
    m_hi = (p_hi + 23) // 24
    stats: Counter[str] = Counter()
    realized: Counter[str] = Counter()
    realized_states: dict[str, dict[str, Any]] = {}
    examples: dict[str, list[dict[str, Any]]] = {
        "combined-miss": [],
        "type-I-only": [],
        "type-II-hit": [],
    }

    emitted = 0
    first = 1 + ((HARD_M_CLASS - 1) % 35)
    if first < 1:
        first += 35

    for M in range(first, m_hi + 1, 35):
        stats["M_h169_class"] += 1
        if M % 6 == 0 or M % 23 == 0:
            stats["small_factor_skip"] += 1
            continue
        p = 24 * M - 23
        if p > p_hi:
            break
        if not cylinder.is_prime64(p):
            stats["p_composite"] += 1
            continue
        if p % 840 != HARD_CLASS:
            raise RuntimeError(f"M={M}: expected h169, got p mod840={p % 840}")
        stats["p_prime"] += 1

        branch = rescue.q23_branch(M)
        if branch is None:
            stats["q23_branch_reject"] += 1
            continue
        stats[f"q23_D_{branch['D_class_mod_23']}"] += 1

        stage23 = rescue.exact_stage(p, 23)
        if stage23["hit_class"] != "type-I-only":
            raise RuntimeError(f"p={p}: q23 branch did not verify as Type-I-only")

        history, stages = rescue.fast_early_history(M, p)
        if not history.startswith(prefix):
            stats["prefix_reject"] += 1
            continue
        stats["prefix_accept"] += 1

        stage19 = stages[4]["exact"]
        C19 = 6 * M - 1
        if int(stage19["C"]) != C19:
            raise RuntimeError(f"p={p}: C19 affine identity failed")

        state = factorization_state(C19, logs)
        cls = state_class(state, logs)
        if stage19["hit_class"] == "miss" and cls != "combined-miss":
            raise RuntimeError(f"p={p}: automaton/exact combined-miss disagreement")
        if stage19["hit_class"] == "type-I-only" and cls != "type-I-only":
            raise RuntimeError(f"p={p}: automaton/exact Type-I-only disagreement")
        if stage19["hit_class"] in {"type-II-only", "both"} and cls != "type-II-hit":
            raise RuntimeError(f"p={p}: automaton/exact Type-II-hit disagreement")

        if cls != "type-II-hit" and state not in closure:
            raise RuntimeError(f"p={p}: exact Type-II-miss state absent from automaton closure")

        sid = state_id(state)
        realized[cls] += 1
        if sid not in realized_states:
            desc = describe_state(state, logs, g, parent, depth)
            desc["realized_class"] = cls
            desc["first_realized_p"] = p
            desc["first_realized_M"] = M
            desc["first_q23_D_class"] = branch["D_class_mod_23"]
            desc["first_early_history"] = history
            realized_states[sid] = desc

        if len(examples[cls]) < 20:
            examples[cls].append(
                {
                    "p": p,
                    "M": M,
                    "q23_D_class": branch["D_class_mod_23"],
                    "early_history": history,
                    "C19": C19,
                    "C19_factorization": stage19["factorization"],
                    "k19_hit_class": stage19["hit_class"],
                    "automaton_state": describe_state(state, logs, g, parent, depth)
                    if cls != "type-II-hit"
                    else {
                        "state_id": sid,
                        "class": cls,
                        "support_size": state.support.bit_count(),
                    },
                }
            )

        emitted += 1
        if max_results and emitted >= max_results:
            break

    abstract_combined_ids = {
        state_id(state) for state in closure if state_class(state, logs) == "combined-miss"
    }
    abstract_i_ids = {
        state_id(state) for state in closure if state_class(state, logs) == "type-I-only"
    }
    realized_combined_ids = {
        sid for sid, row in realized_states.items() if row["realized_class"] == "combined-miss"
    }
    realized_i_ids = {
        sid for sid, row in realized_states.items() if row["realized_class"] == "type-I-only"
    }

    return {
        "mode": "analyze-h169-q23-k19-automaton-realization",
        "p_hi": p_hi,
        "hard_class_mod_840": HARD_CLASS,
        "M_mod_35": HARD_M_CLASS,
        "required_prefix": prefix,
        "q19_automaton": {
            "type_II_miss_states": len(closure),
            "abstract_classes": dict(sorted(abstract_classes.items())),
            "combined_miss_state_count": len(abstract_combined_ids),
            "type_I_only_state_count": len(abstract_i_ids),
        },
        "arithmetic_scan_stats": dict(sorted(stats.items())),
        "realized_candidate_classes": dict(sorted(realized.items())),
        "realized_distinct_type_II_miss_states": len(
            realized_combined_ids | realized_i_ids
        ),
        "realized_distinct_combined_miss_states": len(realized_combined_ids),
        "realized_distinct_type_I_only_states": len(realized_i_ids),
        "finite_unrealized_abstract_combined_states": len(
            abstract_combined_ids - realized_combined_ids
        ),
        "finite_unrealized_abstract_type_I_only_states": len(
            abstract_i_ids - realized_i_ids
        ),
        "realized_states": sorted(
            realized_states.values(),
            key=lambda row: (
                row["realized_class"],
                row.get("support_size", 0),
                row["state_id"],
            ),
        ),
        "examples": examples,
        "claim_boundary": (
            "Automaton non-reachability is an exact local impossibility.  A state "
            "that is abstractly reachable but absent from this finite h169 q23 scan "
            "is only finitely unrealized and may appear at larger scale."
        ),
    }


def self_test() -> int:
    result = analyze(30_000_000, "----", 0)
    known = {18_766_609, 27_211_969}
    found = {
        row["p"]
        for row in result["examples"].get("combined-miss", [])
        if row["p"] in known
    }
    # Examples are capped, so independently verify known full ----- states.
    closure, _, _, logs, _, _ = build_q19_typeii_miss_closure()
    for p in known:
        M = (p + 23) // 24
        history, stages = rescue.fast_early_history(M, p)
        if history != "-----":
            raise SystemExit(f"p={p}: expected -----, got {history}")
        C19 = 6 * M - 1
        state = factorization_state(C19, logs)
        if state not in closure or state_class(state, logs) != "combined-miss":
            raise SystemExit(f"p={p}: known k19 miss not represented by exact closure")
    if result["realized_candidate_classes"].get("combined-miss", 0) < 2:
        raise SystemExit("30M h169 scan failed to recover at least two k19 misses")
    print(
        json.dumps(
            {
                "self_test": "ok",
                "known_examples_visible": sorted(found),
                "q19_type_II_miss_states": result["q19_automaton"]["type_II_miss_states"],
            },
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Map h169 q23 rescue candidates into the exact q19 residue automaton"
    )
    parser.add_argument("--p-hi", type=int, default=30_000_000)
    parser.add_argument("--prefix", default="----")
    parser.add_argument("--max-results", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    result = analyze(args.p_hi, args.prefix, args.max_results)
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
