#!/usr/bin/env python3
"""Analyze k=19 on the forward q23 Type-I rescue branch.

The first four BREC obstruction coordinates have exact normal forms.  This tool
selects exact q23 Type-I-only candidates satisfying an anchored prefix through
k=15, then projects their k19 signed-box state into the exhaustive cyclic-state
model from verify_k19_brec_state_compression.py.

This lets a finite frontier row carry both its ordinary factor/residue signature
and the exact compressed state (c,S), including a canonical <=4-atom history.
For miss states the canonical representative is always <=3 atoms by the
independently verified k19 state theorem.

The output remains finite structural evidence only.  Frequencies or observed
absences do not become pruning rules or universal theorems.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parent
KERNEL = RESEARCH.parent / "kernel"
sys.path.insert(0, str(RESEARCH))
sys.path.insert(0, str(KERNEL))

import analyze_brec_cylinder as cylinder  # noqa: E402
import search_q23_typei_rescue_branch as rescue  # noqa: E402
import verify_k19_brec_state_compression as k19state  # noqa: E402


def factor_character_signature(C: int) -> dict[str, Any]:
    factors = cylinder.factorint(C)
    residues: Counter[int] = Counter()
    qr_omega = 0
    nr_omega = 0
    zero_omega = 0
    for q, exponent in factors.items():
        r = q % 19
        residues[r] += exponent
        symbol = rescue.legendre_prime(r, 19)
        if symbol == 1:
            qr_omega += exponent
        elif symbol == -1:
            nr_omega += exponent
        else:
            zero_omega += exponent

    return {
        "factorization": cylinder.factor_text(factors),
        "residue_valuations_mod_19": {
            str(r): e for r, e in sorted(residues.items())
        },
        "qr_Omega": qr_omega,
        "nr_Omega": nr_omega,
        "zero_Omega": zero_omega,
        "omega": len(factors),
        "Omega": sum(factors.values()),
    }


def cyclic_signature(
    C: int,
    distance: dict[tuple[int, int], int],
    predecessor: dict[tuple[int, int], tuple[tuple[int, int], int]],
) -> dict[str, Any]:
    raw = k19state.state_from_factorization(C)
    state = raw["state"]
    c, mask = state
    if state not in distance:
        raise RuntimeError(f"C19={C}: exact cyclic state escaped exhaustive closure")

    canonical_atoms = k19state.canonical_atoms(state, predecessor)
    canonical_depth = distance[state]
    if bool(raw["combined_miss"]) and canonical_depth > 3:
        raise RuntimeError(f"C19={C}: miss state exceeds proved canonical depth 3")

    return {
        "state_key": f"{c}:{mask:05x}",
        "c": c,
        "support_exponents": raw["support_exponents"],
        "support_size": raw["support_size"],
        "type_II_exp": raw["type_II_exp"],
        "type_I_exp": raw["type_I_exp"],
        "combined_miss": raw["combined_miss"],
        "canonical_depth": canonical_depth,
        "canonical_atoms": canonical_atoms,
    }


def analyze(
    p_hi: int,
    required_prefix: str,
    branch_class: int | None,
    max_candidates: int,
) -> dict[str, Any]:
    if len(required_prefix) > 4:
        raise SystemExit("k19 frontier parent prefix must stop at or before k=15")
    if not required_prefix:
        required_prefix = "----"

    m_hi = (p_hi + 23) // 24
    search_result = rescue.search(
        1,
        m_hi,
        required_prefix,
        branch_class,
        max_candidates,
    )

    distance, predecessor = k19state.closure()

    hit_counts: Counter[str] = Counter()
    support_counts: Counter[int] = Counter()
    branch_counts: Counter[int] = Counter()
    nr_omega_counts: Counter[int] = Counter()
    p19_counts: Counter[int] = Counter()
    residue_pattern_counts: Counter[str] = Counter()
    cyclic_state_counts: Counter[str] = Counter()
    cyclic_depth_counts: Counter[int] = Counter()
    canonical_atom_counts: Counter[str] = Counter()
    miss_state_counts: Counter[str] = Counter()
    examples: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in search_result["results"]:
        p = int(row["p"])
        M = int(row["M"])
        stage = row["early_stages"][4]["exact"]
        if stage["k"] != 19:
            raise RuntimeError("forward search did not place k19 at coordinate five")
        C19 = 6 * M - 1
        if int(stage["C"]) != C19:
            raise RuntimeError(f"p={p}: C19 affine recurrence mismatch")

        factor_sig = factor_character_signature(C19)
        cyclic = cyclic_signature(C19, distance, predecessor)
        hit_class = str(stage["hit_class"])
        exact_miss = hit_class == "miss"
        if bool(cyclic["combined_miss"]) != exact_miss:
            raise RuntimeError(f"p={p}: cyclic state disagrees with exact k19 hit class")
        if int(stage["support_size"]) != int(cyclic["support_size"]):
            raise RuntimeError(f"p={p}: cyclic support size disagrees with exact stage")

        hit_counts[hit_class] += 1
        support_counts[int(stage["support_size"])] += 1
        branch_counts[int(row["D_class_mod_23"])] += 1
        nr_omega_counts[int(factor_sig["nr_Omega"])] += 1
        p19_counts[p % 19] += 1
        cyclic_state_counts[str(cyclic["state_key"])] += 1
        cyclic_depth_counts[int(cyclic["canonical_depth"])] += 1
        atom_key = ",".join(str(a) for a in cyclic["canonical_atoms"])
        canonical_atom_counts[atom_key] += 1
        if exact_miss:
            miss_state_counts[str(cyclic["state_key"])] += 1

        pattern_key = ",".join(
            f"{r}^{e}"
            for r, e in sorted(
                (int(r), int(e))
                for r, e in factor_sig["residue_valuations_mod_19"].items()
            )
        )
        residue_pattern_counts[pattern_key] += 1

        if len(examples[hit_class]) < 12:
            examples[hit_class].append(
                {
                    "p": p,
                    "M": M,
                    "p_mod_840": p % 840,
                    "p_mod_19": p % 19,
                    "q23_D_class": row["D_class_mod_23"],
                    "early_history": row["early_history"],
                    "C19": C19,
                    "k19": stage,
                    "factor_character": factor_sig,
                    "cyclic_state": cyclic,
                }
            )

    misses = hit_counts.get("miss", 0)
    total = len(search_result["results"])
    return {
        "mode": "analyze-q23-rescue-k19-frontier",
        "p_hi": p_hi,
        "required_parent_prefix": required_prefix,
        "q23_branch_class": branch_class,
        "candidates": total,
        "k19_misses": misses,
        "k19_constructive": total - misses,
        "k19_hit_classes": dict(sorted(hit_counts.items())),
        "k19_support_sizes": {
            str(k): v for k, v in sorted(support_counts.items())
        },
        "q23_D_class_counts": {
            str(k): v for k, v in sorted(branch_counts.items())
        },
        "k19_NR_Omega_counts": {
            str(k): v for k, v in sorted(nr_omega_counts.items())
        },
        "p_mod_19_counts": {
            str(k): v for k, v in sorted(p19_counts.items())
        },
        "k19_cyclic_state_counts": dict(sorted(cyclic_state_counts.items())),
        "k19_miss_cyclic_state_counts": dict(sorted(miss_state_counts.items())),
        "k19_canonical_depth_counts": {
            str(k): v for k, v in sorted(cyclic_depth_counts.items())
        },
        "top_k19_canonical_atom_patterns": [
            {"atoms": pattern, "count": count}
            for pattern, count in canonical_atom_counts.most_common(40)
        ],
        "top_factor_residue_patterns": [
            {"pattern": pattern, "count": count}
            for pattern, count in residue_pattern_counts.most_common(40)
        ],
        "examples_by_hit_class": dict(examples),
        "forward_search_stats": search_result["stats"],
        "k19_state_theorem": {
            "reachable_states": len(distance),
            "combined_miss_states": sum(
                k19state.is_combined_miss(*state) for state in distance
            ),
            "max_canonical_miss_atoms": max(
                distance[state]
                for state in distance
                if k19state.is_combined_miss(*state)
            ),
        },
        "claim_boundary": (
            "All rows are exact finite q23 Type-I-only branch candidates.  The "
            "cyclic-state projection is exact, but finite frontier frequencies and "
            "absences remain theorem-hunting evidence only."
        ),
    }


def self_test() -> int:
    result = analyze(30_000_000, "----", None, 0)
    misses = {
        row["p"]
        for row in result["examples_by_hit_class"].get("miss", [])
    }
    for p in (18_766_609, 27_211_969):
        M = (p + 23) // 24
        branch = rescue.q23_branch(M)
        if branch is None:
            raise SystemExit(f"known p={p}: q23 branch missing")
        history, stages = rescue.fast_early_history(M, p)
        if history != "-----":
            raise SystemExit(f"known p={p}: {history} != -----")
        if stages[4]["exact"]["hit_class"] != "miss":
            raise SystemExit(f"known p={p}: k19 is not an exact miss")
    if result["k19_misses"] < 2:
        raise SystemExit("30M frontier failed to recover at least two k19 misses")
    if result["k19_state_theorem"] != {
        "reachable_states": 439,
        "combined_miss_states": 136,
        "max_canonical_miss_atoms": 3,
    }:
        raise SystemExit("k19 exhaustive state theorem metadata changed")
    print(
        json.dumps(
            {
                "self_test": "ok",
                "k19_misses": result["k19_misses"],
                "example_misses": sorted(misses),
                "cyclic_states": result["k19_cyclic_state_counts"],
            }
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze k19 on the exact q23 Type-I rescue branch"
    )
    parser.add_argument("--p-hi", type=int, required=False, default=30_000_000)
    parser.add_argument("--prefix", default="----")
    parser.add_argument("--branch-class", type=int, choices=(5, 14))
    parser.add_argument("--max-candidates", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    result = analyze(args.p_hi, args.prefix, args.branch_class, args.max_candidates)
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
