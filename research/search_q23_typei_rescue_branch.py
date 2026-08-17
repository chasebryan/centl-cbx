#!/usr/bin/env python3
"""Forward exact search on the q=23 Type-I-only rescue normal form.

Instead of scanning every hard prime and asking whether it lands in the q23
companion branch, this tool scans the integer parameter

    M = H*D,
    C23 = 6M,
    p   = 24M - 23,

subject to the exact q23 Type-I-only normal form:

  * p is a Mordell-hard prime;
  * every QR prime divisor of M is 1 mod 23;
  * the total NR valuation is exactly two;
  * both NR occurrences are in class 5 mod 23 or both are in class 14 mod 23.

It then applies the exact BREC obstruction normal forms already proved for
k=3,7,11,15 directly to M, and uses a full signed-box reconstruction for k=19.
Every fast normal-form decision is cross-checked against the generic exact
signed-box evaluator before a candidate is emitted.

This is a theorem/falsifier search tool, not a pruning theorem by itself.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

KERNEL = Path(__file__).resolve().parents[1] / "kernel"
sys.path.insert(0, str(KERNEL))

import analyze_brec_cylinder as cylinder  # noqa: E402

HARD_P_MOD_840 = {1, 121, 169, 289, 361, 529}
HARD_M_MOD_35 = (1, 6, 8, 13, 16, 23)
QR7 = {1, 2, 4}
QR11 = {1, 3, 4, 5, 9}
H15 = {1, 2, 4, 8}
EARLY_K = (3, 7, 11, 15, 19)


def legendre_prime(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    v = pow(a, (q - 1) // 2, q)
    if v == 1:
        return 1
    if v == q - 1:
        return -1
    raise RuntimeError(f"unexpected Euler value {v} mod {q}")


def iter_classes(lo: int, hi: int, modulus: int, residues: Iterable[int]) -> Iterable[int]:
    for residue in residues:
        first = lo + ((residue - lo) % modulus)
        for n in range(first, hi + 1, modulus):
            yield n


def exact_stage(p: int, k: int) -> dict[str, Any]:
    if math.gcd(p, k) != 1:
        return {"k": k, "defined": False, "sign": "?"}
    C = (p + k) // 4
    factors = cylinder.factorint(C)
    support, formal_size = cylinder.signed_box_support(factors, k)
    type_ii = (k - 1) % k
    type_i = (-pow(p % k, -1, k)) % k
    hit_ii = type_ii in support
    hit_i = type_i in support
    if hit_i and hit_ii:
        hit_class = "both"
    elif hit_i:
        hit_class = "type-I-only"
    elif hit_ii:
        hit_class = "type-II-only"
    else:
        hit_class = "miss"
    return {
        "k": k,
        "defined": True,
        "sign": "+" if (hit_i or hit_ii) else "-",
        "C": C,
        "factorization": cylinder.factor_text(factors),
        "support_size": len(support),
        "formal_size": formal_size,
        "type_II_target": type_ii,
        "type_I_target": type_i,
        "hit_class": hit_class,
    }


def q23_branch(M: int) -> dict[str, Any] | None:
    if M <= 0 or math.gcd(M, 6 * 23) != 1:
        return None
    factors = cylinder.factorint(M)
    H = 1
    D = 1
    nr_class: int | None = None
    nr_omega = 0

    for q, exponent in factors.items():
        residue = q % 23
        symbol = legendre_prime(residue, 23)
        if symbol == 1:
            if residue != 1:
                return None
            H *= q**exponent
        elif symbol == -1:
            if residue not in {5, 14}:
                return None
            if nr_class is None:
                nr_class = residue
            elif nr_class != residue:
                return None
            nr_omega += exponent
            D *= q**exponent
        else:
            return None

    if nr_class not in {5, 14} or nr_omega != 2:
        return None
    if H * D != M:
        raise RuntimeError("M != H*D after q23 branch classification")

    return {
        "M": M,
        "H": H,
        "D": D,
        "D_class_mod_23": nr_class,
        "D_Omega": nr_omega,
        "M_factorization": cylinder.factor_text(factors),
    }


def k3_miss(M: int) -> tuple[bool, dict[str, Any]]:
    n = 6 * M - 5
    factors = cylinder.factorint(n)
    miss = all(q % 3 == 1 for q in factors)
    return miss, {"value": n, "factorization": cylinder.factor_text(factors)}


def k7_miss(M: int) -> tuple[bool, dict[str, Any]]:
    n = 3 * M - 2
    factors = cylinder.factorint(n)
    miss = all(q % 7 in QR7 for q in factors)
    return miss, {"value": n, "factorization": cylinder.factor_text(factors)}


def k11_miss(M: int) -> tuple[bool, dict[str, Any]]:
    residual = 2 * M - 1
    factors = cylinder.factorint(residual)

    # QR branch: forced factor 3 is QR and every residual prime is QR.
    if all(legendre_prime(q, 11) == 1 for q in factors):
        return True, {
            "branch": "QR",
            "value": residual,
            "factorization": cylinder.factor_text(factors),
        }

    # Thin branch.
    if factors.get(3, 0):
        return False, {
            "branch": "nonmiss",
            "reason": "v3(C11)>=2",
            "value": residual,
            "factorization": cylinder.factor_text(factors),
        }

    a2 = 0
    a6 = 0
    for q, exponent in factors.items():
        r = q % 11
        symbol = legendre_prime(r, 11)
        if symbol == 1:
            if r != 1:
                return False, {
                    "branch": "nonmiss",
                    "reason": f"nontrivial QR residue {r}",
                    "value": residual,
                    "factorization": cylinder.factor_text(factors),
                }
        elif symbol == -1:
            if r == 2:
                a2 += exponent
            elif r == 6:
                a6 += exponent
            else:
                return False, {
                    "branch": "nonmiss",
                    "reason": f"Type-II-reaching NR residue {r}",
                    "value": residual,
                    "factorization": cylinder.factor_text(factors),
                }
        else:
            return False, {
                "branch": "nonmiss",
                "reason": "nonunit modulo 11",
                "value": residual,
                "factorization": cylinder.factor_text(factors),
            }

    pair = (a2, a6)
    miss = pair in {(1, 0), (0, 1), (1, 1)}
    return miss, {
        "branch": "thin" if miss else "nonmiss",
        "a2": a2,
        "a6": a6,
        "value": residual,
        "factorization": cylinder.factor_text(factors),
    }


def k15_miss(M: int) -> tuple[bool, dict[str, Any]]:
    residual = 3 * M - 1
    factors = cylinder.factorint(residual)
    miss = all(q % 15 in H15 for q in factors)
    return miss, {"value": residual, "factorization": cylinder.factor_text(factors)}


def fast_early_history(M: int, p: int) -> tuple[str, list[dict[str, Any]]]:
    fast = []
    history = []
    for k, predicate in (
        (3, k3_miss),
        (7, k7_miss),
        (11, k11_miss),
        (15, k15_miss),
    ):
        miss, detail = predicate(M)
        sign = "-" if miss else "+"
        exact = exact_stage(p, k)
        if exact["sign"] != sign:
            raise RuntimeError(
                f"normal-form disagreement p={p} k={k}: fast={sign} exact={exact['sign']}"
            )
        history.append(sign)
        fast.append({"k": k, "sign": sign, "normal_form": detail, "exact": exact})

    stage19 = exact_stage(p, 19)
    history.append(stage19["sign"])
    fast.append({"k": 19, "sign": stage19["sign"], "exact": stage19})
    return "".join(history), fast


def search(
    m_lo: int,
    m_hi: int,
    required_prefix: str,
    branch_class: int | None,
    max_results: int,
) -> dict[str, Any]:
    if m_lo < 1 or m_hi < m_lo:
        raise SystemExit("require 1 <= m_lo <= m_hi")
    if any(ch not in "+-" for ch in required_prefix) or len(required_prefix) > 5:
        raise SystemExit("--require-prefix must be a +/- word of length at most 5")
    if branch_class not in (None, 5, 14):
        raise SystemExit("--branch-class must be 5 or 14")

    stats: Counter[str] = Counter()
    depth_survivors = [0] * (len(required_prefix) + 1)
    results: list[dict[str, Any]] = []

    for M in iter_classes(m_lo, m_hi, 35, HARD_M_MOD_35):
        stats["M_hard_class"] += 1
        if math.gcd(M, 6 * 23) != 1:
            stats["M_small_factor_skip"] += 1
            continue

        p = 24 * M - 23
        if not cylinder.is_prime64(p):
            stats["p_composite"] += 1
            continue
        stats["p_prime"] += 1
        if p % 840 not in HARD_P_MOD_840:
            raise RuntimeError(f"M={M}: hard mod35 map produced non-hard p={p}")

        branch = q23_branch(M)
        if branch is None:
            stats["q23_branch_reject"] += 1
            continue
        if branch_class is not None and branch["D_class_mod_23"] != branch_class:
            stats["q23_other_branch"] += 1
            continue
        stats[f"q23_branch_{branch['D_class_mod_23']}"] += 1

        stage23 = exact_stage(p, 23)
        if stage23["hit_class"] != "type-I-only":
            raise RuntimeError(
                f"q23 branch normal form disagrees with exact stage for p={p}: "
                f"{stage23['hit_class']}"
            )

        history, stages = fast_early_history(M, p)
        depth_survivors[0] += 1
        matched = True
        for depth, expected in enumerate(required_prefix, start=1):
            if history[depth - 1] != expected:
                matched = False
                break
            depth_survivors[depth] += 1
        if not matched:
            stats["prefix_reject"] += 1
            continue

        results.append(
            {
                "p": p,
                "p_mod_840": p % 840,
                **branch,
                "early_history": history,
                "early_stages": stages,
                "k23": stage23,
            }
        )
        stats["emitted"] += 1
        if max_results and len(results) >= max_results:
            break

    return {
        "mode": "search-q23-typei-rescue-branch",
        "m_lo": m_lo,
        "m_hi": m_hi,
        "p_hi_approx": 24 * m_hi - 23,
        "required_prefix": required_prefix,
        "branch_class": branch_class,
        "hard_M_mod35": list(HARD_M_MOD_35),
        "stats": dict(sorted(stats.items())),
        "required_prefix_depth_survivors": depth_survivors,
        "results": results,
        "claim_boundary": (
            "Every emitted candidate is exact and cross-checked, but failure to emit "
            "a candidate in a finite M interval is not a theorem."
        ),
    }


def self_test() -> int:
    # Known q23 Type-I-only witnesses spanning both branches and different
    # ancestry depths.  Recover each directly from M=(p+23)/24.
    known = {
        5_151_841: ("5", "-++-+"),
        8_243_281: ("14", "---++"),
        18_766_609: ("14", "-----"),
        27_211_969: ("5", "-----"),
    }
    for p, (branch_name, expected_history) in known.items():
        if (p + 23) % 24:
            raise SystemExit(f"p={p}: q23 M is not integral")
        M = (p + 23) // 24
        branch = q23_branch(M)
        if branch is None or str(branch["D_class_mod_23"]) != branch_name:
            raise SystemExit(f"p={p}: q23 branch self-test failed: {branch}")
        history, _ = fast_early_history(M, p)
        if history != expected_history:
            raise SystemExit(f"p={p}: {history} != {expected_history}")
        if exact_stage(p, 23)["hit_class"] != "type-I-only":
            raise SystemExit(f"p={p}: k23 is not Type-I-only")

    print(json.dumps({"self_test": "ok", "mode": "search-q23-typei-rescue-branch"}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Forward-search the exact q23 Type-I-only rescue normal form"
    )
    parser.add_argument("--m-lo", type=int, default=1)
    parser.add_argument("--m-hi", type=int, help="highest M=HD to scan")
    parser.add_argument("--p-hi", type=int, help="alternative prime ceiling")
    parser.add_argument(
        "--require-prefix",
        default="",
        help="required anchored BREC prefix through k19, e.g. -----",
    )
    parser.add_argument("--branch-class", type=int, choices=(5, 14))
    parser.add_argument("--max-results", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.m_hi is None and args.p_hi is None:
        parser.error("provide --m-hi or --p-hi")
    if args.m_hi is not None and args.p_hi is not None:
        parser.error("provide only one of --m-hi or --p-hi")

    m_hi = args.m_hi
    if m_hi is None:
        if args.p_hi < 2:
            parser.error("--p-hi must be >=2")
        m_hi = (args.p_hi + 23) // 24

    result = search(
        args.m_lo,
        m_hi,
        args.require_prefix,
        args.branch_class,
        args.max_results,
    )
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
