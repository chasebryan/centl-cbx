#!/usr/bin/env python3
"""Verify the exact h289 k=19 quotient normal form.

For p == 289 (mod 840), C19=(p+19)/4 is always divisible by 7.  Modulo 19,
7 has discrete-log exponent 6 to primitive root 2 and order 3.  A single
valuation of 7 therefore contributes the complete subgroup

    K = {0,6,12} <= Z/18Z

in exponent support.  Higher 7-adic valuation does not enlarge that support.
Every later signed-box support is K-periodic, so exact target membership can be
quotiented by K:

    Z/18Z / K ~= Z/6Z.

Write cbar=c mod6 and Sbar=S mod6.  The exact targets become

    Type II: 3
    Type I : 1-cbar mod6.

The complete Type-II-miss quotient closure has only 9 states.  Six are
combined misses and three are Type-I-only.  The full seeded q19 closure has 27
states, exactly three lifts of each quotient state, split 18 combined / 9
Type-I-only.

This is an exact class-conditioned local state theorem.  It does not claim
that every abstract state is arithmetically realized in a deeper BREC corridor.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "kernel"
RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(KERNEL))
sys.path.insert(0, str(RESEARCH))

import analyze_brec_cylinder as cylinder  # noqa: E402
import classify_signed_box_residue_automaton as auto  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402

Q = 19
N = 18
QUOTIENT_N = 6
GENERATOR = 2
TYPE_II_EXP = 9
TYPE_II_QUOT = 3
HARD = 289
T35 = 13
K = {0, 6, 12}

EXPECTED_QUOTIENT_STATES = {
    # (cbar, support tuple): class
    (0, (0,)): "combined-miss",
    (1, (0, 1, 5)): "type-I-only",
    (2, (0, 2, 4)): "combined-miss",
    (4, (0, 2, 4)): "combined-miss",
    (5, (0, 1, 5)): "combined-miss",
    (0, (0, 1, 2, 4, 5)): "type-I-only",
    (0, (0, 2, 4)): "combined-miss",
    (2, (0, 1, 2, 4, 5)): "type-I-only",
    (4, (0, 1, 2, 4, 5)): "combined-miss",
}

REGRESSIONS = {
    1_129: "type-I-only",
    8_689: "miss",
    22_129: "type-II-only",
}


def mask_values(mask: int, n: int) -> set[int]:
    return {x for x in range(n) if mask & (1 << x)}


def quotient_support(mask: int) -> frozenset[int]:
    return frozenset(x % QUOTIENT_N for x in mask_values(mask, N))


def quotient_transition(
    state: tuple[int, frozenset[int]], atom: int
) -> tuple[int, frozenset[int]]:
    cbar, support = state
    a = atom % QUOTIENT_N
    out = set(support)
    out.update((x + a) % QUOTIENT_N for x in support)
    out.update((x - a) % QUOTIENT_N for x in support)
    return (cbar + a) % QUOTIENT_N, frozenset(out)


def quotient_class(state: tuple[int, frozenset[int]]) -> str:
    cbar, support = state
    if TYPE_II_QUOT in support:
        return "type-II-hit"
    type_i = (1 - cbar) % QUOTIENT_N
    return "type-I-only" if type_i in support else "combined-miss"


def quotient_closure() -> dict[tuple[int, frozenset[int]], int]:
    start = (0, frozenset({0}))
    depth = {start: 0}
    queue: deque[tuple[int, frozenset[int]]] = deque([start])

    while queue:
        state = queue.popleft()
        for a in range(QUOTIENT_N):
            nxt = quotient_transition(state, a)
            if TYPE_II_QUOT in nxt[1]:
                continue
            if nxt in depth:
                continue
            depth[nxt] = depth[state] + 1
            queue.append(nxt)

    for state in depth:
        for a in range(QUOTIENT_N):
            nxt = quotient_transition(state, a)
            if TYPE_II_QUOT not in nxt[1] and nxt not in depth:
                raise SystemExit("quotient closure is not transition-closed")
    return depth


def full_seeded_closure() -> dict[tuple[int, int], int]:
    g = auto.primitive_root(Q)
    if g != GENERATOR:
        raise SystemExit(f"q19 primitive root changed: {g}")
    logs = auto.log_table(Q, g)
    if logs[7] != 6:
        raise SystemExit(f"log_2(7)={logs[7]} != 6")

    seed, _ = auto.apply_seed(Q, logs, [7])
    if seed.c_exp != 6:
        raise SystemExit("seed product exponent is not 6")
    if mask_values(seed.support, N) != K:
        raise SystemExit("one forced factor 7 does not supply subgroup K")

    start = (seed.c_exp, seed.support)
    depth = {start: 0}
    queue: deque[tuple[int, int]] = deque([start])

    while queue:
        c, mask = queue.popleft()
        state = auto.State(c, mask)
        for a in range(1, N):
            nxt_obj = auto.transition(state, a, N)
            if auto.contains(nxt_obj.support, TYPE_II_EXP):
                continue
            nxt = (nxt_obj.c_exp, nxt_obj.support)
            if nxt in depth:
                continue
            depth[nxt] = depth[(c, mask)] + 1
            queue.append(nxt)
    return depth


def verify_hard_forcing() -> dict[str, Any]:
    if T35 != 13 or (6 * T35 - 1) % 7:
        raise SystemExit("h289 T mod35 no longer forces factor7 in C19")
    if (HARD + 19) % 4:
        raise SystemExit("h289 C19 is not integral on the residue class")
    c19_mod210 = ((HARD + 19) // 4) % 210
    if c19_mod210 % 7:
        raise SystemExit("h289 does not force literal factor7")

    order = 1
    x = 7 % Q
    while x != 1:
        x = x * 7 % Q
        order += 1
    if order != 3:
        raise SystemExit(f"ord_19(7)={order} != 3")

    return {
        "p_mod_840": HARD,
        "T_mod_35": T35,
        "C19_mod_210": c19_mod210,
        "forced_prime": 7,
        "log2_7_mod18": 6,
        "ord19_7": order,
        "forced_support_exponents": sorted(K),
        "quotient": "Z/18Z / <6> ~= Z/6Z",
    }


def verify_state_quotient() -> dict[str, Any]:
    qdepth = quotient_closure()
    if len(qdepth) != 9:
        raise SystemExit(f"quotient state count {len(qdepth)} != 9")

    observed = {
        (c, tuple(sorted(support))): quotient_class((c, support))
        for c, support in qdepth
    }
    if observed != EXPECTED_QUOTIENT_STATES:
        raise SystemExit(
            f"h289 quotient state table changed: observed={observed}"
        )

    full = full_seeded_closure()
    if len(full) != 27:
        raise SystemExit(f"full h289 seeded closure {len(full)} != 27")

    fibers: dict[tuple[int, frozenset[int]], list[tuple[int, int]]] = defaultdict(list)
    for (c, mask), depth in full.items():
        values = mask_values(mask, N)
        # K-periodicity is the algebraic reason the quotient is exact.
        for x in values:
            for k in K:
                if (x + k) % N not in values:
                    raise SystemExit("full seeded support lost K-periodicity")
        projected = (c % QUOTIENT_N, quotient_support(mask))
        if projected not in qdepth:
            raise SystemExit("full seeded state projected outside quotient closure")
        fibers[projected].append((c, depth))

    if set(fibers) != set(qdepth):
        raise SystemExit("quotient closure has a state with no full lift")
    if any(len(rows) != 3 for rows in fibers.values()):
        raise SystemExit("not every quotient state has exactly three full lifts")

    full_classes = Counter()
    for c, mask in full:
        proj = (c % QUOTIENT_N, quotient_support(mask))
        full_classes[quotient_class(proj)] += 1
    if full_classes != Counter({"combined-miss": 18, "type-I-only": 9}):
        raise SystemExit(f"full class split changed: {full_classes}")

    public = auto.classify(19, [7], 500_000, 16)
    if (
        public["type_II_miss_states"],
        public["combined_miss_states"],
        public["type_I_only_states"],
    ) != (27, 18, 9):
        raise SystemExit("generic seeded q19 automaton disagrees with quotient theorem")

    table = []
    for (cbar, support), depth in sorted(
        qdepth.items(), key=lambda item: (item[1], item[0][0], tuple(sorted(item[0][1])))
    ):
        table.append(
            {
                "cbar": cbar,
                "support": sorted(support),
                "type_II_target": TYPE_II_QUOT,
                "type_I_target": (1 - cbar) % QUOTIENT_N,
                "class": quotient_class((cbar, support)),
                "minimal_quotient_depth": depth,
                "full_lifts": sorted(c for c, _ in fibers[(cbar, support)]),
            }
        )

    return {
        "quotient_states": len(qdepth),
        "quotient_combined_miss_states": sum(
            quotient_class(state) == "combined-miss" for state in qdepth
        ),
        "quotient_type_I_only_states": sum(
            quotient_class(state) == "type-I-only" for state in qdepth
        ),
        "full_seeded_states": len(full),
        "full_combined_miss_states": full_classes["combined-miss"],
        "full_type_I_only_states": full_classes["type-I-only"],
        "fiber_size": 3,
        "table": table,
    }


def regression(p: int, expected: str) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: regression is not prime")
    if p % 840 != HARD:
        raise SystemExit(f"p={p}: not in hard class289")
    stage = ancestry.classify_stage(p, 19)
    if stage["hit_class"] != expected:
        raise SystemExit(
            f"p={p}: exact k19 class {stage['hit_class']} != {expected}"
        )
    C19 = int(stage["C"])
    if C19 % 7:
        raise SystemExit(f"p={p}: forced factor7 missing")

    factors = cylinder.factorint(C19)
    g = auto.primitive_root(Q)
    logs = auto.log_table(Q, g)
    state, _ = auto.apply_seed(Q, logs, [])
    for q, exponent in sorted(factors.items()):
        a = logs[q % Q]
        for _ in range(exponent):
            state = auto.transition(state, a, N)

    qstate = (state.c_exp % QUOTIENT_N, quotient_support(state.support))
    qclass = quotient_class(qstate)
    normalized = "miss" if qclass == "combined-miss" else qclass

    if expected in {"miss", "type-I-only"} and normalized != expected:
        raise SystemExit(
            f"p={p}: quotient class {normalized} != exact {expected}"
        )
    if expected == "type-II-only" and TYPE_II_QUOT not in qstate[1]:
        raise SystemExit(f"p={p}: Type-II construction not visible in quotient")

    return {
        "p": p,
        "C19": C19,
        "factorization": cylinder.factor_text(factors),
        "exact_hit_class": stage["hit_class"],
        "cbar": qstate[0],
        "support_quotient": sorted(qstate[1]),
        "quotient_class": qclass,
    }


def verify() -> dict[str, Any]:
    forcing = verify_hard_forcing()
    quotient = verify_state_quotient()
    regressions = [regression(p, expected) for p, expected in REGRESSIONS.items()]

    return {
        "verified": True,
        "mode": "h289-k19-quotient-normal-form",
        "hard_forcing": forcing,
        "quotient": quotient,
        "theorem": (
            "For p=289 mod840, the exact k19 Type-II-miss signed-box state factors "
            "through Z/18Z/<log_2(7)> ~= Z/6Z.  The quotient has 9 states: 6 "
            "combined misses and 3 Type-I-only; the full closure is their threefold "
            "lift with 18 combined and 9 Type-I-only states."
        ),
        "regressions": regressions,
        "claim_boundary": (
            "Exact hard-class-conditioned local state quotient.  It does not assert "
            "that every abstract quotient state is realized after earlier BREC "
            "ancestry, establish a finite Lane-I ceiling, or prove Erdos-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
