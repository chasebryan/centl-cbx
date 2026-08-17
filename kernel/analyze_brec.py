#!/usr/bin/env python3
"""Analyze exact finite CBX/BREC Lane-I histories.

The input is the JSON summary emitted by cbx-brec-i and, optionally, the TSV
history ledger emitted by --histories.  The analyzer exposes finite structural
signals that can guide theorem hunting without turning statistics into proof.

Key outputs:
  * every absent/present binary motif through the recorded order;
  * exact conditional next-sign counts for each observed prefix;
  * negative-run escape rates, e.g. P(+ next | --- suffix) in the finite corpus;
  * re-entrant motif counts (+-+ and -+-);
  * deepest first constructive shift and longest obstructive runs per prime;
  * spectrum-conditioned finite history summaries.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
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
        yield "".join("-" if (code >> (depth - 1 - i)) & 1 else "+" for i in range(depth))


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
            raise SystemExit(f"BREC summary: emitted motif {word!r} must have positive count")
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
        "right_plus_matches": require_int(cross, "right_plus", "cross") == count_of(motifs, "+"),
        "left_minus_matches": require_int(cross, "left_minus", "cross") == count_of(motifs, "-"),
        "up_plus_minus_matches": (
            order < 2
            or require_int(cross, "up_plus_minus", "cross") == count_of(motifs, "+-")
        ),
        "down_minus_plus_matches": (
            order < 2
            or require_int(cross, "down_minus_plus", "cross") == count_of(motifs, "-+")
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
                raise SystemExit(f"{path}: stage/history length mismatch for p={row['p']}")
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


def analyze_history_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
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
            "max_longest_negative_run": max(row["longest_negative_run"] for row in group),
            "mean_bias": mean([row["bias"] for row in group]),
        }

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
                "value": min(row["bias"] for row in rows),
                "primes": [
                    row["p"]
                    for row in rows
                    if row["bias"] == min(r["bias"] for r in rows)
                ][:32],
            }
            if rows
            else {"value": None, "primes": []}
        ),
        "spectrum": spectrum_summary,
    }


def analyze(summary: dict[str, Any], histories_path: str | None) -> dict[str, Any]:
    motifs = analyze_motifs(summary)
    result: dict[str, Any] = {
        "mode": "analyze-brec-I",
        "application": summary.get("application"),
        "lo": require_int(summary, "lo", "BREC summary"),
        "hi": require_int(summary, "hi", "BREC summary"),
        "i_max": require_int(summary, "i_max", "BREC summary"),
        "hard_primes": require_int(summary, "hard_primes", "BREC summary"),
        "motifs": motifs,
        "claim_boundary": (
            "Finite motif frequencies and absences are theorem-hunting signals only; "
            "they do not establish universal exclusions or pruning authority."
        ),
    }
    if histories_path:
        rows = load_histories(histories_path)
        if len(rows) != result["hard_primes"]:
            raise SystemExit(
                f"history ledger contains {len(rows)} primes; summary reports {result['hard_primes']}"
            )
        result["histories"] = analyze_history_rows(rows)
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
            {"history": "+", "depth": 1, "count": 3, "spectrum": {"A": 1, "B": 2, "C": 0}},
            {"history": "-", "depth": 1, "count": 5, "spectrum": {"A": 2, "B": 3, "C": 0}},
            {"history": "+-", "depth": 2, "count": 2, "spectrum": {"A": 1, "B": 1, "C": 0}},
            {"history": "-+", "depth": 2, "count": 1, "spectrum": {"A": 0, "B": 1, "C": 0}},
            {"history": "--", "depth": 2, "count": 3, "spectrum": {"A": 1, "B": 2, "C": 0}},
            {"history": "+--", "depth": 3, "count": 1, "spectrum": {"A": 1, "B": 0, "C": 0}},
            {"history": "-+-", "depth": 3, "count": 1, "spectrum": {"A": 0, "B": 1, "C": 0}},
            {"history": "--+", "depth": 3, "count": 1, "spectrum": {"A": 0, "B": 1, "C": 0}},
            {"history": "---", "depth": 3, "count": 1, "spectrum": {"A": 1, "B": 0, "C": 0}},
        ],
    }
    out = analyze_motifs(summary)
    if out["reentrant"]["-+-"] != 1:
        raise SystemExit("analyze_brec self-test: reentrant count")
    run2 = next(row for row in out["negative_run_escape"] if row["negative_run"] == 2)
    if run2["escape_to_plus"] != 1 or run2["continue_minus"] != 1:
        raise SystemExit("analyze_brec self-test: negative-run escape")
    if "+" in out["absent_by_depth"]["1"] or "+-+" not in out["absent_by_depth"]["3"]:
        raise SystemExit("analyze_brec self-test: absent motif census")
    puts = json.dumps({"self_test": "ok", "mode": "analyze-brec-I"}, sort_keys=True)
    print(puts)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze exact finite CBX/BREC Lane-I histories")
    parser.add_argument("summary", nargs="?", help="cbx-brec-i JSON summary")
    parser.add_argument("--histories", help="optional cbx-brec-i TSV history ledger")
    parser.add_argument("--json", action="store_true", help="emit compact JSON")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.summary:
        parser.error("summary is required unless --self-test is used")

    result = analyze(load_json(args.summary), args.histories)
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
