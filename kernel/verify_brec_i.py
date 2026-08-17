#!/usr/bin/env python3
"""Exact finite equivalence checks for CBX Lane-I BREC telemetry.

This verifier compares the optimized cbx-brec-i census against the existing
standalone Lane-I reference census on the same finite domain.

It checks only identities that must hold exactly. It does not infer a theorem
from finite data and does not grant pruning authority to BREC telemetry.
"""

from __future__ import annotations

import argparse
import json
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        obj = json.load(fh)
    if not isinstance(obj, dict):
        raise SystemExit(f"{path}: expected a JSON object")
    return obj


def as_int(obj: dict[str, Any], key: str, where: str) -> int:
    if key not in obj:
        raise SystemExit(f"{where}: missing {key!r}")
    value = obj[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise SystemExit(f"{where}: {key!r} must be an integer")
    return value


def motif_map(brec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = brec.get("motifs")
    if not isinstance(raw, list):
        raise SystemExit("BREC summary: motifs must be a list")
    out: dict[str, dict[str, Any]] = {}
    for item in raw:
        if not isinstance(item, dict):
            raise SystemExit("BREC summary: motif entry must be an object")
        history = item.get("history")
        if not isinstance(history, str):
            raise SystemExit("BREC summary: motif history must be a string")
        if history in out:
            raise SystemExit(f"BREC summary: duplicate motif {history!r}")
        out[history] = item
    return out


def verify(standalone: dict[str, Any], brec: dict[str, Any]) -> dict[str, Any]:
    if standalone.get("mode") != "standalone-I":
        raise SystemExit("reference summary is not mode=standalone-I")
    if brec.get("mode") != "brec-I":
        raise SystemExit("candidate summary is not mode=brec-I")
    if brec.get("application") != "CBX-Lane-I-shift-history-v1":
        raise SystemExit("candidate summary has an unexpected BREC application id")

    for key in ("lo", "hi", "i_max"):
        if as_int(standalone, key, "standalone") != as_int(brec, key, "BREC"):
            raise SystemExit(f"domain mismatch for {key}")

    hard_ref = as_int(standalone, "hard_primes", "standalone")
    hard_brec = as_int(brec, "hard_primes", "BREC")
    if hard_ref != hard_brec:
        raise SystemExit(
            f"hard-prime mismatch: standalone={hard_ref} BREC={hard_brec}"
        )

    shifts = standalone.get("shifts")
    if not isinstance(shifts, list) or not shifts:
        raise SystemExit("standalone summary: shifts must be a non-empty list")

    total_visits = 0
    total_skips = 0
    total_factorizations = 0
    total_hits = 0
    spectrum_hits = {"A": 0, "B": 0, "C": 0}

    expected_k = 3
    for row in shifts:
        if not isinstance(row, dict):
            raise SystemExit("standalone summary: shift entry must be an object")
        k = as_int(row, "k", "standalone shift")
        if k != expected_k:
            raise SystemExit(
                f"standalone shift sequence mismatch: expected k={expected_k}, got {k}"
            )
        expected_k += 4

        total_visits += as_int(row, "target_visits", f"standalone k={k}")
        total_skips += as_int(row, "coprime_skips", f"standalone k={k}")
        total_factorizations += as_int(row, "factorizations", f"standalone k={k}")
        total_hits += as_int(row, "hits", f"standalone k={k}")

        spec = row.get("spectrum_hits")
        if not isinstance(spec, dict):
            raise SystemExit(f"standalone k={k}: spectrum_hits must be an object")
        for name in spectrum_hits:
            spectrum_hits[name] += as_int(spec, name, f"standalone k={k} spectrum")

    brec_stages = as_int(brec, "stages", "BREC")
    brec_defined = as_int(brec, "defined_stages", "BREC")
    brec_undefined = as_int(brec, "undefined_stages", "BREC")
    brec_plus = as_int(brec, "constructive", "BREC")
    brec_minus = as_int(brec, "obstructive", "BREC")

    checks = {
        "target_visits_equal_stages": total_visits == brec_stages,
        "coprime_skips_equal_undefined": total_skips == brec_undefined,
        "factorizations_equal_defined": total_factorizations == brec_defined,
        "hits_equal_constructive": total_hits == brec_plus,
        "defined_partition": brec_plus + brec_minus == brec_defined,
        "stage_partition": brec_defined + brec_undefined == brec_stages,
    }

    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        details = {
            "standalone": {
                "visits": total_visits,
                "skips": total_skips,
                "factorizations": total_factorizations,
                "hits": total_hits,
            },
            "brec": {
                "stages": brec_stages,
                "undefined": brec_undefined,
                "defined": brec_defined,
                "constructive": brec_plus,
                "obstructive": brec_minus,
            },
        }
        raise SystemExit(f"BREC equivalence failed: {failed}; {details}")

    motifs = motif_map(brec)
    plus = motifs.get("+")
    minus = motifs.get("-")
    if plus is None or minus is None:
        raise SystemExit("BREC summary must contain depth-1 '+' and '-' motifs")
    if as_int(plus, "count", "BREC '+' motif") != brec_plus:
        raise SystemExit("BREC '+' motif count disagrees with constructive total")
    if as_int(minus, "count", "BREC '-' motif") != brec_minus:
        raise SystemExit("BREC '-' motif count disagrees with obstructive total")

    plus_spec = plus.get("spectrum")
    if not isinstance(plus_spec, dict):
        raise SystemExit("BREC '+' motif spectrum must be an object")
    for name, expected in spectrum_hits.items():
        got = as_int(plus_spec, name, "BREC '+' spectrum")
        if got != expected:
            raise SystemExit(
                f"constructive spectrum mismatch for {name}: standalone={expected} BREC={got}"
            )

    cross = brec.get("cross")
    if not isinstance(cross, dict):
        raise SystemExit("BREC summary: cross must be an object")
    if as_int(cross, "right_plus", "BREC cross") != brec_plus:
        raise SystemExit("BREC Cross right/+ total mismatch")
    if as_int(cross, "left_minus", "BREC cross") != brec_minus:
        raise SystemExit("BREC Cross left/- total mismatch")

    optimization = brec.get("optimization")
    if not isinstance(optimization, dict):
        raise SystemExit("BREC summary: optimization must be an object")
    shortcuts = as_int(
        optimization, "prime_coprime_shortcuts", "BREC optimization"
    )
    mod_checks = as_int(optimization, "prime_mod_checks", "BREC optimization")
    if optimization.get("targets") != "-1,-p^-1":
        raise SystemExit("BREC optimization: collapsed target identity mismatch")
    traversals = as_int(
        optimization,
        "signed_box_traversals_per_defined_stage",
        "BREC optimization",
    )
    if traversals != 1:
        raise SystemExit(
            "BREC optimization: expected one signed-box traversal per defined stage"
        )

    # On ordinary finite research domains p+k cannot approach uint64 overflow.
    # Then every stage takes exactly one admissibility path: automatic p>K
    # shortcut or prime-modulus k%p check.
    if as_int(brec, "hi", "BREC") <= (1 << 63):
        if shortcuts + mod_checks != brec_stages:
            raise SystemExit(
                "BREC optimization accounting mismatch: "
                f"shortcuts({shortcuts}) + mod_checks({mod_checks}) "
                f"!= stages({brec_stages})"
            )

    return {
        "verified": True,
        "application": brec["application"],
        "lo": brec["lo"],
        "hi": brec["hi"],
        "i_max": brec["i_max"],
        "hard_primes": hard_brec,
        "shifts": len(shifts),
        "stages": brec_stages,
        "defined_stages": brec_defined,
        "undefined_stages": brec_undefined,
        "constructive": brec_plus,
        "obstructive": brec_minus,
        "constructive_spectrum": spectrum_hits,
        "optimization": {
            "prime_coprime_shortcuts": shortcuts,
            "prime_mod_checks": mod_checks,
            "targets": optimization["targets"],
            "signed_box_traversals_per_defined_stage": traversals,
        },
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify exact finite equivalence of cbx-brec-i and cbx-standalone-i"
    )
    parser.add_argument("standalone", help="standalone-I JSON summary")
    parser.add_argument("brec", help="brec-I JSON summary")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    result = verify(load_json(args.standalone), load_json(args.brec))
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        opt = result["optimization"]
        print(
            "BREC exact finite equivalence OK: "
            f"hard={result['hard_primes']} shifts={result['shifts']} "
            f"stages={result['stages']} +={result['constructive']} "
            f"-={result['obstructive']} ?={result['undefined_stages']} "
            f"coprime-shortcuts={opt['prime_coprime_shortcuts']} "
            f"mod-checks={opt['prime_mod_checks']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
