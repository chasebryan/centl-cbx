#!/usr/bin/env python3
"""Trace exact fixed-shift Type-I/Type-II behavior through BREC ancestry.

This analyzer keeps one Lane-I target shift fixed (default k=23) while adding
increasing anchored all-negative BREC ancestry constraints:

    empty, -, --, ---, ...

For every selected prime it independently reconstructs the exact signed box at
the fixed target using analyze_brec_cylinder.make_record().  This distinguishes
four exact local states:

    both, Type-I-only, Type-II-only, miss.

That makes it possible to ask a theorem-oriented question that ordinary first-
hit statistics cannot express: after which exact obstruction ancestry, if any,
do the two target occupancies become identical?

For prime target moduli the analyzer also classifies the total exponents of
quadratic-nonresidue prime-factor classes of C=(p+k)/4.

Finite coincidence is evidence only.  It is not promoted to a theorem or a
pruning rule by this script.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from typing import Any

import analyze_brec_cylinder as cylinder


def load_rows(path: str, target_index: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"p", "spectrum", "history"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise SystemExit(f"{path}: not a cbx-brec-i history ledger")

        for raw in reader:
            history = raw["history"]
            if len(history) <= target_index:
                continue
            child = history[target_index]
            if child == "?":
                continue
            if child not in "+-":
                raise SystemExit(f"invalid BREC sign for p={raw['p']}: {child!r}")
            rows.append(
                {
                    "p": int(raw["p"]),
                    "spectrum": raw["spectrum"],
                    "history": history,
                    "child": child,
                }
            )
    return rows


def nonresidue_pattern(record: dict[str, Any], modulus: int) -> str | None:
    if not cylinder.is_prime64(modulus):
        return None

    nr: Counter[int] = Counter()
    factors: dict[int, int] = record["factors"]
    for q, exponent in factors.items():
        residue = q % modulus
        if residue == 0:
            raise SystemExit(
                f"factor {q} is non-invertible modulo prime target {modulus}"
            )
        symbol = pow(residue, (modulus - 1) // 2, modulus)
        if symbol == modulus - 1:
            nr[residue] += exponent
        elif symbol != 1:
            raise SystemExit(
                f"unexpected Euler criterion value {symbol} modulo {modulus}"
            )

    if not nr:
        return "QR"
    return "*".join(f"{residue}^{nr[residue]}" for residue in sorted(nr))


def compact_counter(counter: Counter[Any]) -> list[dict[str, Any]]:
    return [
        {"value": value, "count": count}
        for value, count in sorted(
            counter.items(), key=lambda item: (-item[1], str(item[0]))
        )
    ]


def summarize(records: list[dict[str, Any]], modulus: int) -> dict[str, Any]:
    hit_classes: Counter[str] = Counter()
    support_sizes: Counter[int] = Counter()
    nr_patterns: Counter[str] = Counter()
    type_ii_miss_patterns: Counter[str] = Counter()
    type_i_miss_patterns: Counter[str] = Counter()
    one_sided: list[dict[str, Any]] = []

    for record in records:
        hit_class = str(record["hit_class"])
        hit_classes[hit_class] += 1
        support_sizes[int(record["box_support_size"])] += 1
        pattern = nonresidue_pattern(record, modulus)
        if pattern is not None:
            nr_patterns[pattern] += 1

        if not record["hit_type_ii"] and pattern is not None:
            type_ii_miss_patterns[pattern] += 1
        if not record["hit_type_i"] and pattern is not None:
            type_i_miss_patterns[pattern] += 1

        if bool(record["hit_type_i"]) != bool(record["hit_type_ii"]):
            if len(one_sided) < 32:
                one_sided.append(
                    {
                        "p": record["p"],
                        "spectrum": record["spectrum"],
                        "history": record["history"],
                        "C": record["C"],
                        "factorization": record["factorization"],
                        "residue_signature": record["residue_signature"],
                        "box_support_size": record["box_support_size"],
                        "missing_unit_residues": record["missing_unit_residues"],
                        "target_type_i": record["target_type_i"],
                        "target_type_ii": record["target_type_ii"],
                        "hit_class": hit_class,
                        "nonresidue_pattern": pattern,
                    }
                )

    i_only = hit_classes.get("type-I-only", 0)
    ii_only = hit_classes.get("type-II-only", 0)
    both = hit_classes.get("both", 0)
    miss = hit_classes.get("miss", 0)
    type_ii_misses = i_only + miss
    type_i_misses = ii_only + miss

    return {
        "count": len(records),
        "hit_classes": compact_counter(hit_classes),
        "both": both,
        "miss": miss,
        "type_i_only": i_only,
        "type_ii_only": ii_only,
        "type_ii_misses": type_ii_misses,
        "type_i_rescues_of_type_ii_miss": i_only,
        "type_i_misses": type_i_misses,
        "type_ii_rescues_of_type_i_miss": ii_only,
        "two_target_coincidence": i_only == 0 and ii_only == 0,
        "box_support_sizes": compact_counter(support_sizes),
        "nonresidue_patterns": compact_counter(nr_patterns),
        "type_ii_miss_nonresidue_patterns": compact_counter(type_ii_miss_patterns),
        "type_i_miss_nonresidue_patterns": compact_counter(type_i_miss_patterns),
        "one_sided_examples": one_sided,
    }


def analyze(path: str, target_k: int, max_prefix_depth: int | None) -> dict[str, Any]:
    if target_k < 3 or target_k % 4 != 3:
        raise SystemExit("--target-k must be >=3 and congruent to 3 mod 4")
    target_index = (target_k - 3) // 4
    if target_index == 0:
        max_depth = 0
    else:
        max_depth = target_index if max_prefix_depth is None else max_prefix_depth
        if max_depth < 0 or max_depth > target_index:
            raise SystemExit(
                f"--max-prefix-depth must be in 0..{target_index} for k={target_k}"
            )

    source_rows = load_rows(path, target_index)
    exact_records = [cylinder.make_record(row, target_k) for row in source_rows]

    ancestry: list[dict[str, Any]] = []
    first_coincidence_depth: int | None = None
    for depth in range(max_depth + 1):
        prefix = "-" * depth
        selected = [r for r in exact_records if str(r["history"]).startswith(prefix)]
        summary = summarize(selected, target_k)
        row = {
            "prefix": prefix,
            "prefix_depth": depth,
            "prefix_last_k": None if depth == 0 else 3 + 4 * (depth - 1),
            **summary,
        }
        ancestry.append(row)
        if summary["two_target_coincidence"] and first_coincidence_depth is None:
            first_coincidence_depth = depth

    return {
        "mode": "analyze-brec-target",
        "application": "CBX-Lane-I-shift-history-v1",
        "target_k": target_k,
        "target_index": target_index,
        "target_modulus_prime": cylinder.is_prime64(target_k),
        "source_primes": len(exact_records),
        "max_prefix_depth": max_depth,
        "first_observed_two_target_coincidence_depth": first_coincidence_depth,
        "first_observed_two_target_coincidence_prefix": (
            None if first_coincidence_depth is None else "-" * first_coincidence_depth
        ),
        "ancestry": ancestry,
        "claim_boundary": (
            "Two-target coincidence and branch disappearance are exact only for the "
            "finite supplied corpus. They are theorem targets, not pruning authority."
        ),
    }


def self_test() -> int:
    # Known exact k=23 representatives.  The first two are finite Type-I-only
    # rescues; the latter two represent both and miss states respectively.
    cases = [
        (1544209, "+", "type-I-only"),
        (1911841, "+", "type-I-only"),
        (2521, "+", "both"),
        (397489, "-", "miss"),
    ]
    got: list[str] = []
    for p, child, expected in cases:
        record = cylinder.make_record(
            {"p": p, "spectrum": "?", "history": child, "child": child}, 23
        )
        got.append(str(record["hit_class"]))
        if record["hit_class"] != expected:
            raise SystemExit(
                f"target self-test failed for p={p}: {record['hit_class']} != {expected}"
            )

    if nonresidue_pattern(
        cylinder.make_record(
            {"p": 1544209, "spectrum": "?", "history": "+", "child": "+"},
            23,
        ),
        23,
    ) != "14^2":
        raise SystemExit("k23 nonresidue-pattern self-test failed")

    print(
        json.dumps(
            {"self_test": "ok", "mode": "analyze-brec-target", "classes": got},
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Trace a fixed Lane-I target through anchored BREC obstruction ancestry"
    )
    parser.add_argument("histories", nargs="?", help="cbx-brec-i TSV history ledger")
    parser.add_argument("--target-k", type=int, default=23, help="fixed Lane-I shift")
    parser.add_argument(
        "--max-prefix-depth",
        type=int,
        help="maximum all-negative anchored ancestry depth before the fixed target",
    )
    parser.add_argument("--json", action="store_true", help="emit compact JSON")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.histories:
        parser.error("histories ledger is required unless --self-test is used")

    result = analyze(args.histories, args.target_k, args.max_prefix_depth)
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
