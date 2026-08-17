#!/usr/bin/env python3
"""Verify the h169 k11-phase child that forces literal factor 11 at k=43.

Scope: exact Lane-I signed-box residue geometry, with the h169 k11 ancestry
phase supplied by verify_h169_k11_future_factor_partition.py.

Write

    p = 169 + 840 t,
    T = (p+23)/24 = 8 + 35 t.

The landed h169 k11 theorem restricts a combined miss to

    t mod 11 in {0,2,3,4,8}.

On the child t=2 mod11,

    T = 1 mod11,
    C43 = (p+43)/4 = 6T+5 = 0 mod11.

Hence literal prime 11 is forced into C43.  This verifier asks what that one
forced factor does to the complete exact q=43 signed-box Type-II-miss state
space.  It proves a finite local contraction and an exact nonresidue-valuation
budget.  It does not assert that k43 must be reached or must miss.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(RESEARCH))

import classify_signed_box_residue_automaton as auto  # noqa: E402
import verify_h169_k11_future_factor_partition as future  # noqa: E402

Q = 43
SELECTED_T11_PHASE = 2
FORCED_FACTOR = 11
EXPECTED = {
    "generic_states": 18_048,
    "generic_combined": 7_740,
    "generic_type_i_only": 10_308,
    "generic_max_nr": 20,
    "seed_states": 2_317,
    "seed_combined": 1_217,
    "seed_type_i_only": 1_100,
    "seed_max_nr": 14,
}


def multiplicative_order(a: int, q: int) -> int:
    x = 1
    for n in range(1, q):
        x = x * a % q
        if x == 1:
            return n
    raise RuntimeError("multiplicative order not found")


def verify_phase() -> dict[str, Any]:
    obj = future.verify()
    allowed = obj["k11_combined_miss_implies_t_mod_11"]
    if allowed != [0, 2, 3, 4, 8]:
        raise SystemExit(f"h169 k11 phase domain changed: {allowed}")
    if SELECTED_T11_PHASE not in allowed:
        raise SystemExit("selected t mod11 phase is no longer admissible")

    rows = [
        row
        for row in obj["partition"]
        if row["t_mod_11"] == SELECTED_T11_PHASE
    ]
    if len(rows) != 1:
        raise SystemExit("future factor partition lost the t=2 mod11 row")
    row = rows[0]
    if row["shift_k"] != 43:
        raise SystemExit(f"t=2 mod11 no longer maps to k43: {row}")

    t11 = SELECTED_T11_PHASE
    T11 = (8 + 35 * t11) % 11
    C43_11 = (6 * T11 + 5) % 11
    direct_C43_11 = (53 + 210 * t11) % 11
    if T11 != 1 or C43_11 != 0 or direct_C43_11 != 0:
        raise SystemExit(
            f"phase algebra changed: T11={T11}, C43={C43_11}, direct={direct_C43_11}"
        )

    return {
        "t_mod_11": t11,
        "T_mod_11": T11,
        "p_mod_11": row["p_mod_11"],
        "forced_factor": FORCED_FACTOR,
        "forced_coordinate": "C43=(p+43)/4=6T+5=53+210t",
        "forced_shift": row["shift_k"],
        "consequence": "11|C43",
    }


def build_closure(seed_residues: tuple[int, ...]) -> dict[str, Any]:
    g = auto.primitive_root(Q)
    logs = auto.log_table(Q, g)
    n = Q - 1
    log_minus_one = logs[Q - 1]
    log_four = logs[4]
    seed, seed_exps = auto.apply_seed(Q, logs, list(seed_residues))

    if auto.contains(seed.support, log_minus_one):
        raise SystemExit("forced seed already hits Type II")

    queue: deque[auto.State] = deque([seed])
    seen = {seed}
    depth = {seed: 0}
    while queue:
        state = queue.popleft()
        for a in range(1, n):
            nxt = auto.transition(state, a, n)
            if auto.contains(nxt.support, log_minus_one):
                continue
            if nxt in seen:
                continue
            seen.add(nxt)
            depth[nxt] = depth[state] + 1
            queue.append(nxt)

    combined = 0
    type_i_only = 0
    support_sizes: Counter[int] = Counter()
    for state in seen:
        target_i = (log_minus_one - log_four - state.c_exp) % n
        if auto.contains(state.support, target_i):
            type_i_only += 1
        else:
            combined += 1
        support_sizes[state.support.bit_count()] += 1

    states = list(seen)
    index = {state: i for i, state in enumerate(states)}
    adjacency: list[list[tuple[int, int]]] = [[] for _ in states]
    for state in states:
        src = index[state]
        for a in range(1, n):
            nxt = auto.transition(state, a, n)
            if auto.contains(nxt.support, log_minus_one):
                continue
            # For a primitive root, odd exponent means nonresidue.
            adjacency[src].append((index[nxt], a & 1))

    return {
        "primitive_root": g,
        "logs": logs,
        "seed": seed,
        "seed_exponents": seed_exps,
        "states": states,
        "index": index,
        "adjacency": adjacency,
        "combined": combined,
        "type_i_only": type_i_only,
        "support_sizes": dict(sorted(support_sizes.items())),
        "max_depth": max(depth.values()),
    }


def tarjan(adjacency: list[list[tuple[int, int]]]) -> tuple[list[list[int]], list[int]]:
    sys.setrecursionlimit(max(100_000, 4 * len(adjacency)))
    serial = 0
    stack: list[int] = []
    on_stack = [False] * len(adjacency)
    index = [-1] * len(adjacency)
    low = [0] * len(adjacency)
    components: list[list[int]] = []

    def visit(v: int) -> None:
        nonlocal serial
        index[v] = serial
        low[v] = serial
        serial += 1
        stack.append(v)
        on_stack[v] = True

        for w, _weight in adjacency[v]:
            if index[w] == -1:
                visit(w)
                low[v] = min(low[v], low[w])
            elif on_stack[w]:
                low[v] = min(low[v], index[w])

        if low[v] == index[v]:
            comp: list[int] = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                comp.append(w)
                if w == v:
                    break
            components.append(comp)

    for v in range(len(adjacency)):
        if index[v] == -1:
            visit(v)

    component_of = [-1] * len(adjacency)
    for cid, comp in enumerate(components):
        for v in comp:
            component_of[v] = cid
    return components, component_of


def nr_budget(closure: dict[str, Any]) -> dict[str, Any]:
    adjacency: list[list[tuple[int, int]]] = closure["adjacency"]
    components, component_of = tarjan(adjacency)

    positive_inside = 0
    for v, edges in enumerate(adjacency):
        for w, weight in edges:
            if component_of[v] == component_of[w] and weight > 0:
                positive_inside += 1
    if positive_inside:
        raise SystemExit(
            "Type-II-miss graph contains a positive nonresidue cycle; budget is not finite"
        )

    dag: list[dict[int, int]] = [dict() for _ in components]
    for v, edges in enumerate(adjacency):
        cv = component_of[v]
        for w, weight in edges:
            cw = component_of[w]
            if cv == cw:
                continue
            old = dag[cv].get(cw)
            if old is None or weight > old:
                dag[cv][cw] = weight

    seed_index = closure["index"][closure["seed"]]
    start = component_of[seed_index]
    reachable = {start}
    queue: deque[int] = deque([start])
    while queue:
        c = queue.popleft()
        for d in dag[c]:
            if d not in reachable:
                reachable.add(d)
                queue.append(d)

    indegree = {c: 0 for c in reachable}
    for c in reachable:
        for d in dag[c]:
            if d in reachable:
                indegree[d] += 1
    queue = deque(c for c in reachable if indegree[c] == 0)
    topo: list[int] = []
    while queue:
        c = queue.popleft()
        topo.append(c)
        for d in dag[c]:
            if d not in reachable:
                continue
            indegree[d] -= 1
            if indegree[d] == 0:
                queue.append(d)
    if len(topo) != len(reachable):
        raise SystemExit("condensation graph unexpectedly contains a cycle")

    minus_inf = -10**9
    dist = {c: minus_inf for c in reachable}
    dist[start] = 0
    for c in topo:
        if dist[c] == minus_inf:
            continue
        for d, weight in dag[c].items():
            if d not in reachable:
                continue
            dist[d] = max(dist[d], dist[c] + weight)

    return {
        "max_NR_valuation": max(dist.values()),
        "positive_NR_edges_inside_SCCs": positive_inside,
        "SCC_count": len(components),
        "largest_SCC": max(len(comp) for comp in components),
        "reachable_SCC_count": len(reachable),
    }


def summarize(seed_residues: tuple[int, ...]) -> dict[str, Any]:
    closure = build_closure(seed_residues)
    budget = nr_budget(closure)
    return {
        "seed_residues": list(seed_residues),
        "seed_exponents": closure["seed_exponents"],
        "seed_support_size": closure["seed"].support.bit_count(),
        "TypeII_miss_states": len(closure["states"]),
        "combined_miss_states": closure["combined"],
        "TypeI_only_states": closure["type_i_only"],
        "max_factor_occurrence_depth": closure["max_depth"],
        "support_size_distribution": closure["support_sizes"],
        "NR_budget": budget,
    }


def verify() -> dict[str, Any]:
    phase = verify_phase()
    generic = summarize(())
    seeded = summarize((FORCED_FACTOR,))

    if generic["TypeII_miss_states"] != EXPECTED["generic_states"]:
        raise SystemExit("generic q43 Type-II-miss state count changed")
    if generic["combined_miss_states"] != EXPECTED["generic_combined"]:
        raise SystemExit("generic q43 combined-miss count changed")
    if generic["TypeI_only_states"] != EXPECTED["generic_type_i_only"]:
        raise SystemExit("generic q43 Type-I-only count changed")
    if generic["NR_budget"]["max_NR_valuation"] != EXPECTED["generic_max_nr"]:
        raise SystemExit("generic q43 NR valuation budget changed")

    if seeded["TypeII_miss_states"] != EXPECTED["seed_states"]:
        raise SystemExit("seed11 q43 Type-II-miss state count changed")
    if seeded["combined_miss_states"] != EXPECTED["seed_combined"]:
        raise SystemExit("seed11 q43 combined-miss count changed")
    if seeded["TypeI_only_states"] != EXPECTED["seed_type_i_only"]:
        raise SystemExit("seed11 q43 Type-I-only count changed")
    if seeded["NR_budget"]["max_NR_valuation"] != EXPECTED["seed_max_nr"]:
        raise SystemExit("seed11 q43 NR valuation budget changed")

    g = auto.primitive_root(Q)
    logs = auto.log_table(Q, g)
    if g != 3:
        raise SystemExit(f"q43 primitive root changed: {g}")
    if logs[FORCED_FACTOR] != 30:
        raise SystemExit(f"log_3(11) mod43 changed: {logs[FORCED_FACTOR]}")
    if multiplicative_order(FORCED_FACTOR, Q) != 7:
        raise SystemExit("11 no longer has order 7 modulo43")
    if pow(FORCED_FACTOR, (Q - 1) // 2, Q) != 1:
        raise SystemExit("11 is no longer quadratic-residue support modulo43")

    if generic["NR_budget"]["positive_NR_edges_inside_SCCs"] != 0:
        raise SystemExit("generic q43 miss graph gained a positive NR cycle")
    if seeded["NR_budget"]["positive_NR_edges_inside_SCCs"] != 0:
        raise SystemExit("seed11 q43 miss graph gained a positive NR cycle")

    reduction_num = seeded["TypeII_miss_states"]
    reduction_den = generic["TypeII_miss_states"]
    if math.gcd(reduction_num, reduction_den) != 1:
        raise SystemExit("unexpected q43 closure-ratio simplification changed")

    return {
        "verified": True,
        "mode": "h169-k11-phase-k43-seed-contraction",
        "phase": phase,
        "q43_seed": {
            "primitive_root": g,
            "log_g_11": logs[FORCED_FACTOR],
            "ord_43_11": multiplicative_order(FORCED_FACTOR, Q),
            "11_is_QR_mod_43": True,
        },
        "generic_q43": generic,
        "seed11_q43": seeded,
        "exact_contraction": {
            "TypeII_miss_state_ratio": f"{reduction_num}/{reduction_den}",
            "states_removed": reduction_den - reduction_num,
            "NR_valuation_budget": f"{EXPECTED['generic_max_nr']}->{EXPECTED['seed_max_nr']}",
            "NR_budget_drop": EXPECTED["generic_max_nr"] - EXPECTED["seed_max_nr"],
        },
        "theorem": (
            "For h169 under an inherited k11 combined miss, the child t=2 mod11 "
            "forces 11|C43.  Conditional on k43 Type-II miss, the complete exact "
            "q43 signed-box state lies in the 2317-state seed11 closure and "
            "Omega_NR(C43)<=14; the unseeded local bounds are 18048 states and 20."
        ),
        "claim_boundary": (
            "Exact local consequence of one admissible h169 k11 phase.  It does not "
            "assert that t=2 is forced, that k43 is reached, that k43 misses, or that "
            "every abstract seed11 state is arithmetically realized."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
