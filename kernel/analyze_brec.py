#!/usr/bin/env python3
"""Analyze exact finite CBX/BREC Lane-I histories.

The input is the JSON summary emitted by cbx-brec-i and, optionally, the TSV
history ledger emitted by --histories. The analyzer exposes finite structural
signals that can guide theorem hunting without turning statistics into proof.

Key outputs:
  * every absent/present contiguous binary motif through the recorded order;
  * exact conditional next-sign counts for each observed motif prefix;
  * negative-run escape rates for contiguous obstructive motifs;
  * exact start-of-corridor prefix cylinders from the per-prime history ledger;
  * re-entrant motif counts (+-+ and -+-);
  * deepest first constructive shift and longest obstructive runs per prime;
  * spectrum-conditioned finite history summaries.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from typing import Any, Iterable


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        obj = json.load(fh)
    if not isinstance(obj, dict):
        raise SystemExit(f"{path}: expected a JSON object")
    return obj


def require_int(obj: dict[str, Any], key: str, where: str) -> int:
    value = obj.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise SystemExit(f"{where}: {key!r} must be an integer")
    return value


def all_words(depth: int) -> Iterable[str]:
    for code in range(1 << depth):
        yield "".join(
            "-" if (code >> (depth - 1 - i)) & 1 else "+"
            for i in range(depth)
        )


def motif_index(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = summary.get("motifs")
    if not isinstance(raw, list):
        raise SystemExit("BREC summary: motifs must be a list")
    out: dict[str, dict[str, Any]] = {}
    for row in raw:
        if not isinstance(row, dict):
            raise SystemExit("BREC summary: motif entry must be an object")
        word = row.get("history")
        if not isinstance(word, str) or not word or any(ch not in "+-" for ch in word):
            raise SystemExit("BREC summary: invalid motif history")
        if word in out:
            raise SystemExit(f"BREC summary: duplicate motif {word!r}")
        count = require_int(row, "count", f"motif {word}")
        if count <= 0:
            raise SystemExit(
                f"BREC summary: emitted motif {word!r} must have positive count"
            )
        out[word] = row
    return out


def count_of(motifs: dict[str, dict[str, Any]], word: str) -> int:
    row = motifs.get(word)
    return 0 if row is None else require_int(row, "count", f"motif {word}")


def analyze_motifs(summary: dict[str, Any]) -> dict[str, Any]:
    if summary.get("mode") != "brec-I":
        raise SystemExit("summary is not mode=brec-I")
    order = require_int(summary, "order", "BREC summary")
    if order < 1:
        raise SystemExit("BREC summary: order must be positive")

    motifs = motif_index(summary)
    absent_by_depth: dict[str, list[str]] = {}
    present_by_depth: dict[str, int] = {}
    for depth in range(1, order + 1):
        words = list(all_words(depth))
        absent = [word for word in words if word not in motifs]
        absent_by_depth[str(depth)] = absent
        present_by_depth[str(depth)] = len(words) - len(absent)

    continuation: list[dict[str, Any]] = []
    if order >= 2:
        for depth in range(1, order):
            for prefix in all_words(depth):
                plus = count_of(motifs, prefix + "+")
                minus = count_of(motifs, prefix + "-")
                total = plus + minus
                if total == 0:
                    continue
                continuation.append(
                    {
                        "prefix": prefix,
                        "depth": depth,
                        "followed_by_plus": plus,
                        "followed_by_minus": minus,
                        "extensions": total,
                        "plus_rate": plus / total,
                    }
                )

    constructive_precursors = sorted(
        continuation,
        key=lambda row: (
            row["plus_rate"],
            row["extensions"],
            len(row["prefix"]),
            row["prefix"],
        ),
        reverse=True,
    )
    obstructive_precursors = sorted(
        continuation,
        key=lambda row: (
            1.0 - row["plus_rate"],
            row["extensions"],
            len(row["prefix"]),
            row["prefix"],
        ),
        reverse=True,
    )

    negative_run_escape: list[dict[str, Any]] = []
    for run in range(1, order):
        prefix = "-" * run
        plus = count_of(motifs, prefix + "+")
        minus = count_of(motifs, prefix + "-")
        extensions = plus + minus
        if extensions:
            negative_run_escape.append(
                {
                    "negative_run": run,
                    "prefix": prefix,
                    "escape_to_plus": plus,
                    "continue_minus": minus,
                    "extensions": extensions,
                    "escape_rate": plus / extensions,
                }
            )

    reentrant = {
        "+-+": count_of(motifs, "+-+") if order >= 3 else None,
        "-+-": count_of(motifs, "-+-") if order >= 3 else None,
    }

    cross = summary.get("cross")
    if not isinstance(cross, dict):
        raise SystemExit("BREC summary: cross must be an object")
    cross_check = {
        "right_plus_matches": require_int(cross, "right_plus", "cross")
        == count_of(motifs, "+"),
        "left_minus_matches": require_int(cross, "left_minus", "cross")
        == count_of(motifs, "-"),
        "up_plus_minus_matches": (
            order < 2
            or require_int(cross, "up_plus_minus", "cross")
            == count_of(motifs, "+-")
        ),
        "down_minus_plus_matches": (
            order < 2
            or require_int(cross, "down_minus_plus", "cross")
            == count_of(motifs, "-+")
        ),
    }
    if not all(cross_check.values()):
        raise SystemExit(f"BREC Cross/motif accounting mismatch: {cross_check}")

    return {
        "order": order,
        "present_by_depth": present_by_depth,
        "absent_by_depth": absent_by_depth,
        "all_depths_saturated": all(not xs for xs in absent_by_depth.values()),
        "continuation": continuation,
        "top_constructive_precursors": constructive_precursors[:12],
        "top_obstructive_precursors": obstructive_precursors[:12],
        "negative_run_escape": negative_run_escape,
        "reentrant": reentrant,
        "cross_check": cross_check,
        "interpretation": (
            "These motif counts are contiguous-window statistics anywhere in a Lane-I "
            "history. Use histories.prefix_cylinders for exact start-of-corridor "
            "prefix populations."
        ),
    }


def longest_run(history: str, symbol: str) -> int:
    best = 0
    cur = 0
    for ch in history:
        if ch == symbol:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def initial_negative_run(history: str) -> int:
    n = 0
    for ch in history:
        if ch != "-":
            break
        n += 1
    return n


def first_plus_k(history: str) -> int:
    idx = history.find("+")
    return 0 if idx < 0 else 3 + 4 * idx


def load_histories(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        expected = {
            "p",
            "spectrum",
            "stages",
            "defined",
            "undefined",
            "positive",
            "negative",
            "bias",
            "reversals",
            "parity",
            "initial",
            "terminal",
            "first_hit_k",
            "history",
        }
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            raise SystemExit(f"{path}: unexpected BREC history header")
        for raw in reader:
            history = raw["history"]
            if any(ch not in "+-?" for ch in history):
                raise SystemExit(f"{path}: invalid history for p={raw['p']}")
            row: dict[str, Any] = {
                "p": int(raw["p"]),
                "spectrum": raw["spectrum"],
                "stages": int(raw["stages"]),
                "defined": int(raw["defined"]),
                "undefined": int(raw["undefined"]),
                "positive": int(raw["positive"]),
                "negative": int(raw["negative"]),
                "bias": int(raw["bias"]),
                "reversals": int(raw["reversals"]),
                "parity": int(raw["parity"]),
                "initial": raw["initial"],
                "terminal": raw["terminal"],
                "first_hit_k": int(raw["first_hit_k"]),
                "history": history,
            }
            if len(history) != row["stages"]:
                raise SystemExit(
                    f"{path}: stage/history length mismatch for p={row['p']}"
                )
            if history.count("+") != row["positive"]:
                raise SystemExit(f"{path}: positive count mismatch for p={row['p']}")
            if history.count("-") != row["negative"]:
                raise SystemExit(f"{path}: negative count mismatch for p={row['p']}")
            if history.count("?") != row["undefined"]:
                raise SystemExit(f"{path}: undefined count mismatch for p={row['p']}")
            if row["defined"] + row["undefined"] != row["stages"]:
                raise SystemExit(f"{path}: stage partition mismatch for p={row['p']}")
            derived_first = first_plus_k(history)
            if derived_first != row["first_hit_k"]:
                raise SystemExit(
                    f"{path}: first_hit_k mismatch for p={row['p']}: "
                    f"ledger={row['first_hit_k']} derived={derived_first}"
                )
            row["longest_negative_run"] = longest_run(history, "-")
            row["longest_positive_run"] = longest_run(history, "+")
            row["initial_negative_run"] = initial_negative_run(history)
            rows.append(row)
    return rows


def compact_extrema(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    if not rows:
        return {"value": None, "primes": []}
    value = max(int(row[field]) for row in rows)
    primes = [row["p"] for row in rows if int(row[field]) == value]
    return {"value": value, "primes": primes[:32], "prime_count": len(primes)}


def mean(values: list[int]) -> float | None:
    return None if not values else sum(values) / len(values)


def analyze_prefix_cylinders(
    rows: list[dict[str, Any]], max_depth: int
) -> dict[str, Any]:
    if max_depth < 1:
        return {"max_depth": 0, "depths": {}}

    depths: dict[str, Any] = {}
    for depth in range(1, max_depth + 1):
        counts: dict[str, int] = defaultdict(int)
        spectrum_counts: dict[str, dict[str, int]] = defaultdict(
            lambda: {"A": 0, "B": 0, "C": 0, "?": 0}
        )
        excluded_undefined = 0

        for row in rows:
            history = str(row["history"])
            if len(history) < depth:
                continue
            prefix = history[:depth]
            if "?" in prefix:
                excluded_undefined += 1
                continue
            counts[prefix] += 1
            spectrum = str(row["spectrum"])
            spectrum_counts[prefix][
                spectrum if spectrum in {"A", "B", "C"} else "?"
            ] += 1

        entries = [
            {
                "prefix": prefix,
                "count": counts[prefix],
                "spectrum": spectrum_counts[prefix],
            }
            for prefix in sorted(counts)
        ]
        absent = [word for word in all_words(depth) if word not in counts]
        depths[str(depth)] = {
            "eligible_primes": sum(counts.values()),
            "excluded_undefined_prefix": excluded_undefined,
            "present": len(entries),
            "absent": absent,
            "cylinders": entries,
        }

    all_negative_splits: list[dict[str, Any]] = []
    for depth in range(1, max_depth):
        parent = "-" * depth
        child_plus = parent + "+"
        child_minus = parent + "-"
        next_depth = depths[str(depth + 1)]
        lookup = {row["prefix"]: row["count"] for row in next_depth["cylinders"]}
        plus = lookup.get(child_plus, 0)
        minus = lookup.get(child_minus, 0)
        total = plus + minus
        all_negative_splits.append(
            {
                "parent": parent,
                "next_k": 3 + 4 * depth,
                "constructive_child": child_plus,
                "obstructive_child": child_minus,
                "constructive_count": plus,
                "obstructive_count": minus,
                "children": total,
                "constructive_rate": None if total == 0 else plus / total,
            }
        )

    return {
        "max_depth": max_depth,
        "depths": depths,
        "all_negative_splits": all_negative_splits,
        "note": (
            "Prefix cylinders are anchored at k=3. Unlike motif continuation, "
            "they do not count the same sign word at later offsets."
        ),
    }


def analyze_history_rows(
    rows: list[dict[str, Any]], prefix_depth: int
) -> dict[str, Any]:
    by_spectrum: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_spectrum[str(row["spectrum"])].append(row)

    finite_letters = [row for row in rows if row["positive"] == 0]
    with_hit = [row for row in rows if row["first_hit_k"] > 0]
    max_first = compact_extrema(with_hit, "first_hit_k")

    spectrum_summary: dict[str, Any] = {}
    for spectrum, group in sorted(by_spectrum.items()):
        hits = [row["first_hit_k"] for row in group if row["first_hit_k"] > 0]
        spectrum_summary[spectrum] = {
            "primes": len(group),
            "no_constructive_stage": sum(row["positive"] == 0 for row in group),
            "mean_first_hit_k": mean(hits),
            "max_first_hit_k": max(hits) if hits else None,
            "mean_reversals": mean([row["reversals"] for row in group]),
            "max_longest_negative_run": max(
                row["longest_negative_run"] for row in group
            ),
            "mean_bias": mean([row["bias"] for row in group]),
        }

    min_bias = min((row["bias"] for row in rows), default=None)
    return {
        "primes": len(rows),
        "with_constructive_stage": len(with_hit),
        "no_constructive_stage": len(finite_letters),
        "no_constructive_primes": [row["p"] for row in finite_letters[:64]],
        "deepest_first_constructive": max_first,
        "longest_negative_run": compact_extrema(rows, "longest_negative_run"),
        "longest_positive_run": compact_extrema(rows, "longest_positive_run"),
        "longest_initial_obstruction": compact_extrema(rows, "initial_negative_run"),
        "most_reversals": compact_extrema(rows, "reversals"),
        "most_obstructive_bias": (
            {
                "value": min_bias,
                "primes": [row["p"] for row in rows if row["bias"] == min_bias][:32],
            }
            if min_bias is not None
            else {"value": None, "primes": []}
        ),
        "spectrum": spectrum_summary,
        "prefix_cylinders": analyze_prefix_cylinders(rows, prefix_depth),
    }


def analyze(
    summary: dict[str, Any], histories_path: str | None, prefix_depth: int | None
) -> dict[str, Any]:
    motifs = analyze_motifs(summary)
    order = motifs["order"]
    chosen_prefix_depth = order if prefix_depth is None else prefix_depth
    if chosen_prefix_depth < 1:
        raise SystemExit("--prefix-depth must be positive")

    result: dict[str, Any] = {
        "mode": "analyze-brec-I",
        "application": summary.get("application"),
        "lo": require_int(summary, "lo", "BREC summary"),
        "hi": require_int(summary, "hi", "BREC summary"),
        "i_max": require_int(summary, "i_max", "BREC summary"),
        "hard_primes": require_int(summary, "hard_primes", "BREC summary"),
        "motifs": motifs,
        "claim_boundary": (
            "Finite motif frequencies, prefix-cylinder frequencies, and absences are "
            "theorem-hunting signals only; they do not establish universal exclusions "
            "or pruning authority."
        ),
    }
    if histories_path:
        rows = load_histories(histories_path)
        if len(rows) != result["hard_primes"]:
            raise SystemExit(
                f"history ledger contains {len(rows)} primes; "
                f"summary reports {result['hard_primes']}"
            )
        if rows:
            chosen_prefix_depth = min(chosen_prefix_depth, rows[0]["stages"])
        result["histories"] = analyze_history_rows(rows, chosen_prefix_depth)
    elif prefix_depth is not None:
        raise SystemExit("--prefix-depth requires --histories")
    return result


def self_test() -> int:
    summary = {
        "mode": "brec-I",
        "application": "CBX-Lane-I-shift-history-v1",
        "lo": 2,
        "hi": 100,
        "i_max": 15,
        "order": 3,
        "hard_primes": 2,
        "cross": {
            "right_plus": 3,
            "left_minus": 5,
            "up_plus_minus": 2,
            "down_minus_plus": 1,
        },
        "motifs": [
            {
                "history": "+",
                "depth": 1,
                "count": 3,
                "spectrum": {"A": 1, "B": 2, "C": 0},
            },
            {
                "history": "-",
                "depth": 1,
                "count": 5,
                "spectrum": {"A": 2, "B": 3, "C": 0},
            },
            {
                "history": "+-",
                "depth": 2,
                "count": 2,
                "spectrum": {"A": 1, "B": 1, "C": 0},
            },
            {
                "history": "-+",
                "depth": 2,
                "count": 1,
                "spectrum": {"A": 0, "B": 1, "C": 0},
            },
            {
                "history": "--",
                "depth": 2,
                "count": 3,
                "spectrum": {"A": 1, "B": 2, "C": 0},
            },
            {
                "history": "+--",
                "depth": 3,
                "count": 1,
                "spectrum": {"A": 1, "B": 0, "C": 0},
            },
            {
                "history": "-+-",
                "depth": 3,
                "count": 1,
                "spectrum": {"A": 0, "B": 1, "C": 0},
            },
            {
                "history": "--+",
                "depth": 3,
                "count": 1,
                "spectrum": {"A": 0, "B": 1, "C": 0},
            },
            {
                "history": "---",
                "depth": 3,
                "count": 1,
                "spectrum": {"A": 1, "B": 0, "C": 0},
            },
        ],
    }
    out = analyze_motifs(summary)
    if out["reentrant"]["-+-"] != 1:
        raise SystemExit("analyze_brec self-test: reentrant count")
    run2 = next(
        row for row in out["negative_run_escape"] if row["negative_run"] == 2
    )
    if run2["escape_to_plus"] != 1 or run2["continue_minus"] != 1:
        raise SystemExit("analyze_brec self-test: negative-run escape")
    if "+" in out["absent_by_depth"]["1"] or "+-+" not in out["absent_by_depth"]["3"]:
        raise SystemExit("analyze_brec self-test: absent motif census")

    synthetic_rows = [
        {
            "p": 1009,
            "spectrum": "A",
            "stages": 4,
            "defined": 4,
            "undefined": 0,
            "positive": 1,
            "negative": 3,
            "bias": -2,
            "reversals": 1,
            "parity": -1,
            "initial": "-",
            "terminal": "+",
            "first_hit_k": 15,
            "history": "---+",
            "longest_negative_run": 3,
            "longest_positive_run": 1,
            "initial_negative_run": 3,
        },
        {
            "p": 2521,
            "spectrum": "B",
            "stages": 4,
            "defined": 4,
            "undefined": 0,
            "positive": 0,
            "negative": 4,
            "bias": -4,
            "reversals": 0,
            "parity": 1,
            "initial": "-",
            "terminal": "-",
            "first_hit_k": 0,
            "history": "----",
            "longest_negative_run": 4,
            "longest_positive_run": 0,
            "initial_negative_run": 4,
        },
    ]
    cylinders = analyze_prefix_cylinders(synthetic_rows, 4)
    split3 = next(
        row for row in cylinders["all_negative_splits"] if row["parent"] == "---"
    )
    if split3["constructive_count"] != 1 or split3["obstructive_count"] != 1:
        raise SystemExit("analyze_brec self-test: prefix-cylinder split")

    print(json.dumps({"self_test": "ok", "mode": "analyze-brec-I"}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze exact finite CBX/BREC Lane-I histories"
    )
    parser.add_argument("summary", nargs="?", help="cbx-brec-i JSON summary")
    parser.add_argument("--histories", help="optional cbx-brec-i TSV history ledger")
    parser.add_argument(
        "--prefix-depth",
        type=int,
        help="start-of-corridor prefix-cylinder depth (defaults to motif order)",
    )
    parser.add_argument("--json", action="store_true", help="emit compact JSON")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.summary:
        parser.error("summary is required unless --self-test is used")

    result = analyze(load_json(args.summary), args.histories, args.prefix_depth)
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
