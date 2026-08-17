#!/usr/bin/env python3
"""Analyze the exact k=19 state on the forward q23 Type-I rescue branch.

The first four BREC obstruction coordinates now have exact normal forms on
M=HD.  This tool uses the forward rescue-branch search to select candidates
that satisfy an anchored prefix through k=15 (default '----'), then studies
the still-exact signed-box state at k=19 where C19=6M-1.

The output is finite structural evidence only.  It is designed to expose the
next residue/character normal-form candidate and to preserve immediate
counterexamples rather than promote an observed absence to a theorem.
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

    state_counts: Counter[str] = Counter()
    support_counts: Counter[int] = Counter()
    spectrum_counts: Counter[int] = Counter()
    branch_counts: Counter[int] = Counter()
    nr_omega_counts: Counter[int] = Counter()
    p19_counts: Counter[int] = Counter()
    residue_pattern_counts: Counter[str] = Counter()
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

        sig = factor_character_signature(C19)
        hit_class = stage["hit_class"]
        state_counts[hit_class] += 1
        support_counts[int(stage["support_size"])] += 1
        branch_counts[int(row["D_class_mod_23"])] += 1
        nr_omega_counts[int(sig["nr_Omega"])] += 1
        p19_counts[p % 19] += 1

        pattern_key = ",".join(
            f"{r}^{e}"
            for r, e in sorted(
                (int(r), int(e))
                for r, e in sig["residue_valuations_mod_19"].items()
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
                    "factor_character": sig,
                }
            )

    misses = state_counts.get("miss", 0)
    total = len(search_result["results"])
    return {
        "mode": "analyze-q23-rescue-k19-frontier",
        "p_hi": p_hi,
        "required_parent_prefix": required_prefix,
        "q23_branch_class": branch_class,
        "candidates": total,
        "k19_misses": misses,
        "k19_constructive": total - misses,
        "k19_hit_classes": dict(sorted(state_counts.items())),
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
        "top_factor_residue_patterns": [
            {"pattern": pattern, "count": count}
            for pattern, count in residue_pattern_counts.most_common(40)
        ],
        "examples_by_hit_class": dict(examples),
        "forward_search_stats": search_result["stats"],
        "claim_boundary": (
            "All rows are exact finite q23 Type-I-only branch candidates.  Any "
            "observed k19 pattern is a theorem candidate only until separately "
            "proved; counterexamples must be preserved."
        ),
    }


def self_test() -> int:
    # The 30M grade must include the two known full ----- q23 Type-I-only
    # witnesses, one from each q23 rescue class.
    result = analyze(30_000_000, "----", None, 0)
    misses = {
        row["p"]
        for row in result["examples_by_hit_class"].get("miss", [])
    }
    # Examples are capped, so verify by a direct exact known-witness path too.
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
    print(json.dumps({"self_test": "ok", "k19_misses": result["k19_misses"], "example_misses": sorted(misses)}))
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
