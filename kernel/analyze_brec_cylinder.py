#!/usr/bin/env python3
"""Exact arithmetic comparison of the two children of a BREC prefix cylinder.

Given a cbx-brec-i history ledger and an anchored binary prefix such as
"-----", select the primes whose Lane-I history begins with that prefix, then
split them by the immediately following sign.  For each child, factor

    C = (p + k_next) / 4,
    k_next = 3 + 4 * len(prefix),

and compare exact factor/residue structure modulo k_next.

This is a theorem-hunting tool.  A finite common factor, residue support, or
missing child is evidence to investigate, not a universal theorem.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from functools import reduce
from typing import Any

UINT64_MAX = (1 << 64) - 1
MR_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def is_prime64(n: int) -> bool:
    if n < 2:
        return False
    for q in SMALL_PRIMES:
        if n == q:
            return True
        if n % q == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in MR_BASES_64:
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    if n % 5 == 0:
        return 5

    # Deterministic sequence of polynomial constants.  This is analysis-side
    # exact factorization, not a cryptographic RNG requirement.
    for c in range(1, 128, 2):
        x = 2 + (c % max(1, n - 3))
        y = x
        d = 1
        for _ in range(1_000_000):
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            if d == 1:
                continue
            if d != n:
                return d
            break
    raise RuntimeError(f"Pollard-rho failed to split {n}")


def factor_list(n: int, out: list[int]) -> None:
    if n == 1:
        return
    if is_prime64(n):
        out.append(n)
        return
    d = pollard_rho(n)
    factor_list(d, out)
    factor_list(n // d, out)


def factorint(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("factorint requires n >= 1")
    if n == 1:
        return {}
    raw: list[int] = []
    factor_list(n, raw)
    raw.sort()
    return dict(Counter(raw))


def factor_text(factors: dict[int, int]) -> str:
    if not factors:
        return "1"
    return "*".join(f"{q}^{e}" if e != 1 else str(q) for q, e in sorted(factors.items()))


def residue_signature(factors: dict[int, int], modulus: int) -> str:
    return ",".join(
        f"{q % modulus}^{e}" for q, e in sorted(factors.items(), key=lambda item: (item[0] % modulus, item[0]))
    ) or "1"


def residue_set_signature(factors: dict[int, int], modulus: int) -> str:
    return ",".join(str(r) for r in sorted({q % modulus for q in factors})) or "1"


def load_selected(path: str, prefix: str) -> tuple[list[dict[str, Any]], dict[str, int]]:
    rows: list[dict[str, Any]] = []
    stats = {
        "ledger_rows": 0,
        "prefix_matches": 0,
        "short_history": 0,
        "undefined_child": 0,
    }
    depth = len(prefix)

    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"p", "spectrum", "history"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise SystemExit(f"{path}: not a cbx-brec-i history ledger")

        for raw in reader:
            stats["ledger_rows"] += 1
            history = raw["history"]
            if not history.startswith(prefix):
                continue
            stats["prefix_matches"] += 1
            if len(history) <= depth:
                stats["short_history"] += 1
                continue
            child = history[depth]
            if child == "?":
                stats["undefined_child"] += 1
                continue
            if child not in "+-":
                raise SystemExit(f"invalid child sign for p={raw['p']}: {child!r}")
            rows.append(
                {
                    "p": int(raw["p"]),
                    "spectrum": raw["spectrum"],
                    "history": history,
                    "child": child,
                }
            )
    return rows, stats


def make_record(row: dict[str, Any], next_k: int) -> dict[str, Any]:
    p = int(row["p"])
    if (p + next_k) % 4:
        raise SystemExit(f"p={p}: p+k is not divisible by 4 at k={next_k}")
    if math.gcd(p, next_k) != 1:
        raise SystemExit(f"p={p}: history marks defined child but gcd(p,{next_k}) != 1")

    C = (p + next_k) // 4
    if C > UINT64_MAX:
        raise SystemExit(f"p={p}: C exceeds uint64 analysis contract")
    factors = factorint(C)
    reconstructed = 1
    for q, e in factors.items():
        reconstructed *= q**e
    if reconstructed != C:
        raise SystemExit(f"p={p}: factorization reconstruction failed")
    if any(not is_prime64(q) for q in factors):
        raise SystemExit(f"p={p}: non-prime factor emitted")

    residues = {q: q % next_k for q in factors}
    return {
        **row,
        "next_k": next_k,
        "C": C,
        "factors": factors,
        "factorization": factor_text(factors),
        "omega": len(factors),
        "Omega": sum(factors.values()),
        "largest_prime_factor": max(factors, default=1),
        "residues": residues,
        "residue_signature": residue_signature(factors, next_k),
        "residue_set": residue_set_signature(factors, next_k),
    }


def gcd_all(values: list[int]) -> int:
    return 0 if not values else reduce(math.gcd, values)


def summarize_child(records: list[dict[str, Any]], modulus: int) -> dict[str, Any]:
    if not records:
        return {
            "count": 0,
            "spectra": {},
            "gcd_C": 0,
            "gcd_C_factorization": "0",
            "common_factor_primes": [],
            "common_residue_support": [],
            "omega": {},
            "Omega": {},
            "residue_sets": [],
            "residue_signatures": [],
            "prime_residue_occurrences": {},
            "examples": [],
        }

    spectra = Counter(str(r["spectrum"]) for r in records)
    omega = Counter(int(r["omega"]) for r in records)
    big_omega = Counter(int(r["Omega"]) for r in records)
    residue_sets = Counter(str(r["residue_set"]) for r in records)
    residue_signatures = Counter(str(r["residue_signature"]) for r in records)

    prime_residue_occurrences: Counter[int] = Counter()
    exponent_residue_mass: Counter[int] = Counter()
    factor_sets: list[set[int]] = []
    residue_supports: list[set[int]] = []
    for rec in records:
        factors: dict[int, int] = rec["factors"]
        factor_sets.append(set(factors))
        support = set()
        for q, e in factors.items():
            residue = q % modulus
            support.add(residue)
            prime_residue_occurrences[residue] += 1
            exponent_residue_mass[residue] += e
        residue_supports.append(support)

    common_factor_primes = sorted(set.intersection(*factor_sets)) if factor_sets else []
    common_residue_support = sorted(set.intersection(*residue_supports)) if residue_supports else []
    g = gcd_all([int(r["C"]) for r in records])
    gfac = factorint(g) if g > 1 else {}

    def top(counter: Counter[Any], limit: int = 20) -> list[dict[str, Any]]:
        return [
            {"value": value, "count": count}
            for value, count in counter.most_common(limit)
        ]

    examples = [
        {
            "p": r["p"],
            "spectrum": r["spectrum"],
            "C": r["C"],
            "factorization": r["factorization"],
            "residue_set": r["residue_set"],
            "residue_signature": r["residue_signature"],
        }
        for r in records[:24]
    ]

    return {
        "count": len(records),
        "spectra": dict(sorted(spectra.items())),
        "gcd_C": g,
        "gcd_C_factorization": factor_text(gfac) if g else "0",
        "common_factor_primes": common_factor_primes,
        "common_residue_support": common_residue_support,
        "omega": top(omega),
        "Omega": top(big_omega),
        "residue_sets": top(residue_sets),
        "residue_signatures": top(residue_signatures),
        "prime_residue_occurrences": dict(sorted(prime_residue_occurrences.items())),
        "exponent_residue_mass": dict(sorted(exponent_residue_mass.items())),
        "examples": examples,
    }


def analyze(path: str, prefix: str) -> dict[str, Any]:
    if not prefix or any(ch not in "+-" for ch in prefix):
        raise SystemExit("--prefix must be a non-empty binary +/- word")
    next_k = 3 + 4 * len(prefix)
    rows, ledger_stats = load_selected(path, prefix)
    records = [make_record(row, next_k) for row in rows]
    plus = [r for r in records if r["child"] == "+"]
    minus = [r for r in records if r["child"] == "-"]

    return {
        "mode": "analyze-brec-cylinder",
        "application": "CBX-Lane-I-shift-history-v1",
        "prefix": prefix,
        "prefix_depth": len(prefix),
        "next_k": next_k,
        "ledger": ledger_stats,
        "binary_children": len(records),
        "constructive_child": summarize_child(plus, next_k),
        "obstructive_child": summarize_child(minus, next_k),
        "claim_boundary": (
            "All arithmetic summaries are exact for this finite selected corpus. "
            "Common or absent structures are candidate theorem signals only."
        ),
    }


def self_test() -> int:
    for n, expected in (
        (1, {}),
        (2**4 * 3**2 * 5, {2: 4, 3: 2, 5: 1}),
        (1000003 * 1000033, {1000003: 1, 1000033: 1}),
        (9658489, {9658489: 1}),
    ):
        got = factorint(n)
        if got != expected:
            raise SystemExit(f"factor self-test failed for {n}: {got} != {expected}")

    sample = [
        make_record(
            {"p": 1009, "spectrum": "A", "history": "--+", "child": "+"},
            11,
        ),
        make_record(
            {"p": 2521, "spectrum": "B", "history": "---", "child": "-"},
            11,
        ),
    ]
    if sample[0]["C"] != 255 or sample[1]["C"] != 633:
        raise SystemExit("C-state self-test failed")
    if sample[0]["factorization"] != "3*5*17":
        raise SystemExit("factor formatting self-test failed")

    print(json.dumps({"self_test": "ok", "mode": "analyze-brec-cylinder"}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare exact arithmetic of the +/- children of a BREC prefix cylinder"
    )
    parser.add_argument("histories", nargs="?", help="cbx-brec-i TSV history ledger")
    parser.add_argument(
        "--prefix",
        default="-----",
        help="anchored binary parent prefix (default: -----, so next k=23)",
    )
    parser.add_argument("--json", action="store_true", help="emit compact JSON")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.histories:
        parser.error("histories ledger is required unless --self-test is used")

    result = analyze(args.histories, args.prefix)
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
