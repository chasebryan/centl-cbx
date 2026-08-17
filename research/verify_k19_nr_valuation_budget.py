#!/usr/bin/env python3
"""Verify exact quadratic-nonresidue valuation budgets at k=19.

Each prime-factor valuation occurrence of C19 contributes one discrete-log atom
in Z/18Z.  With primitive root 2, an occurrence is QR iff its atom exponent is
even and NR iff the exponent is odd.

Restrict the exact signed-box transition graph to states that still miss the
Type-II target exponent 9.  Give every QR transition weight 0 and every NR
transition weight 1.  The graph is finite.  For each exact seed used by the
hard-class/phase grammar, this verifier:

  * exhausts the complete Type-II-miss state closure;
  * computes strongly connected components;
  * proves no SCC contains a positive-weight (NR) edge;
  * contracts to a DAG and computes the longest NR-weighted path.

Therefore the longest path is a genuine upper bound on total NR valuation,
not merely a canonical-state complexity bound.

Exact budgets:

  unseeded []       : Omega_NR <= 8
  seed [5]          : Omega_NR <= 6
  seed [7]          : Omega_NR <= 2
  seed [5,7]        : Omega_NR <= 0
  seed [11]         : Omega_NR <= 2
  seed [7,11]       : Omega_NR <= 2

The first four induce the hard-class atlas:

  h1,h361   <= 6
  h121       = 0
  h169,h529 <= 8
  h289      <= 2.

On the exact k11-selected phase T=2 mod11 in h169/h529, factor 11 is forced
into C19 and the budget drops from 8 to 2.  In h289 the additional factor 11
leaves the existing bound 2 unchanged.
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
GENERATOR = 2
TYPE_II_EXP = 9

EXPECTED = {
    (): (254, 8),
    (5,): (64, 6),
    (7,): (27, 2),
    (5, 7): (9, 0),
    (11,): (27, 2),
    (7, 11): (27, 2),
}

HARD_ATLAS = {
    1: ((5,), 6),
    121: ((5, 7), 0),
    169: ((), 8),
    289: ((7,), 2),
    361: ((5,), 6),
    529: ((), 8),
}

# Exact arithmetic sharpness/regression witnesses.  The first two prove that
# the unseeded and seed-[5] graph bounds are attained by actual prime k19
# states.  h289 and h121 guard the exact class-conditioned endpoints.  The
# phase witnesses show the seed-[11] budget 2 is also arithmetically attained
# on both previously unseeded hard lanes.
WITNESSES = [
    {
        "p": 108_013,
        "expected_hard": None,
        "expected_seed": (),
        "expected_nr": 8,
        "expected_hit": "type-I-only",
    },
    {
        "p": 11_896_466_401,
        "expected_hard": 1,
        "expected_seed": (5,),
        "expected_nr": 6,
        "expected_hit": "type-I-only",
    },
    {
        "p": 93_529,
        "expected_hard": 289,
        "expected_seed": (7,),
        "expected_nr": 2,
        "expected_hit": "miss",
    },
    {
        "p": 6_841,
        "expected_hard": 121,
        "expected_seed": (5, 7),
        "expected_nr": 0,
        "expected_hit": "miss",
    },
    {
        "p": 1_023_289,
        "expected_hard": 169,
        "expected_seed": (11,),
        "expected_nr": 2,
        "expected_hit": "type-I-only",
        "require_k11_phase": True,
    },
    {
        "p": 670_849,
        "expected_hard": 529,
        "expected_seed": (11,),
        "expected_nr": 2,
        "expected_hit": "type-I-only",
        "require_k11_phase": True,
    },
]


def mask_values(mask: int) -> list[int]:
    return [x for x in range(N) if mask & (1 << x)]


def seed_state(seed_residues: tuple[int, ...]) -> tuple[auto.State, dict[int, int]]:
    g = auto.primitive_root(Q)
    if g != GENERATOR:
        raise SystemExit(f"q19 primitive root changed: {g}")
    logs = auto.log_table(Q, g)
    state, _ = auto.apply_seed(Q, logs, list(seed_residues))
    if auto.contains(state.support, TYPE_II_EXP):
        raise SystemExit(f"seed {seed_residues} already hits Type II")
    for residue in seed_residues:
        if logs[residue] % 2:
            raise SystemExit(f"seed {residue} is NR; atlas assumes QR-only seeds")
    return state, logs


def type_ii_miss_graph(
    seed_residues: tuple[int, ...],
) -> tuple[
    auto.State,
    dict[auto.State, list[tuple[auto.State, int, int]]],
    dict[int, int],
]:
    start, logs = seed_state(seed_residues)
    queue: deque[auto.State] = deque([start])
    seen = {start}
    edges: dict[auto.State, list[tuple[auto.State, int, int]]] = defaultdict(list)

    # Exponent 0 is an inert residue-1 occurrence.  It is QR, adds no NR
    # valuation, and does not affect any state, so it is omitted from the graph.
    for_state_atoms = range(1, N)

    while queue:
        state = queue.popleft()
        for atom in for_state_atoms:
            nxt = auto.transition(state, atom, N)
            if auto.contains(nxt.support, TYPE_II_EXP):
                continue
            weight = atom & 1
            edges[state].append((nxt, weight, atom))
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)

    # Exact closure guard.
    for state in list(seen):
        for atom in for_state_atoms:
            nxt = auto.transition(state, atom, N)
            if not auto.contains(nxt.support, TYPE_II_EXP) and nxt not in seen:
                raise SystemExit("Type-II-miss graph is not transition-closed")

    return start, edges, logs


def tarjan_scc(
    states: set[auto.State],
    edges: dict[auto.State, list[tuple[auto.State, int, int]]],
) -> tuple[list[list[auto.State]], dict[auto.State, int]]:
    index = 0
    indices: dict[auto.State, int] = {}
    low: dict[auto.State, int] = {}
    stack: list[auto.State] = []
    on_stack: set[auto.State] = set()
    components: list[list[auto.State]] = []

    sys.setrecursionlimit(max(10_000, 4 * len(states) + 100))

    def visit(v: auto.State) -> None:
        nonlocal index
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w, _, _ in edges.get(v, []):
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])

        if low[v] == indices[v]:
            comp: list[auto.State] = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            components.append(comp)

    for state in states:
        if state not in indices:
            visit(state)

    component_of = {
        state: cid
        for cid, comp in enumerate(components)
        for state in comp
    }
    return components, component_of


def weighted_budget(seed_residues: tuple[int, ...]) -> dict[str, Any]:
    start, edges, logs = type_ii_miss_graph(seed_residues)
    states = {start}
    for src, outgoing in edges.items():
        states.add(src)
        states.update(dst for dst, _, _ in outgoing)

    components, component_of = tarjan_scc(states, edges)

    positive_internal: list[dict[str, int]] = []
    dag_edge_weight: dict[tuple[int, int], int] = {}
    dag_edge_atom: dict[tuple[int, int], int] = {}

    for src in states:
        for dst, weight, atom in edges.get(src, []):
            u = component_of[src]
            v = component_of[dst]
            if u == v:
                if weight:
                    positive_internal.append(
                        {"component": u, "atom": atom, "weight": weight}
                    )
                continue
            key = (u, v)
            if weight > dag_edge_weight.get(key, -1):
                dag_edge_weight[key] = weight
                dag_edge_atom[key] = atom

    if positive_internal:
        raise SystemExit(
            f"seed {seed_residues}: positive-NR cycle exists: {positive_internal[:5]}"
        )

    dag: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    indegree = [0] * len(components)
    for (u, v), weight in dag_edge_weight.items():
        dag[u].append((v, weight, dag_edge_atom[(u, v)]))
        indegree[v] += 1

    queue: deque[int] = deque(i for i, d in enumerate(indegree) if d == 0)
    topo: list[int] = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v, _, _ in dag.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(topo) != len(components):
        raise SystemExit("SCC condensation is not acyclic")

    neg = -10**9
    best = [neg] * len(components)
    best[component_of[start]] = 0
    for u in topo:
        if best[u] == neg:
            continue
        for v, weight, _ in dag.get(u, []):
            best[v] = max(best[v], best[u] + weight)

    maximum = max(best)
    expected_states, expected_max = EXPECTED[seed_residues]
    if len(states) != expected_states:
        raise SystemExit(
            f"seed {seed_residues}: state count {len(states)} != {expected_states}"
        )
    if maximum != expected_max:
        raise SystemExit(
            f"seed {seed_residues}: NR budget {maximum} != {expected_max}"
        )

    # A simple explicit abstract path reaches every stated maximum: append
    # `maximum` copies of atom exponent 1 (residue 2 mod19).  This is not the
    # upper-bound proof, but guards sharpness of the finite-state budget.
    state = start
    for _ in range(maximum):
        state = auto.transition(state, 1, N)
        if auto.contains(state.support, TYPE_II_EXP):
            raise SystemExit(
                f"seed {seed_residues}: repeated atom1 hits Type II before budget"
            )
    if maximum:
        one_more = auto.transition(state, 1, N)
        # The next repeated atom need not be the only way to exceed the bound;
        # the SCC/DAG proof above establishes impossibility globally.  For the
        # chosen sharp path it should hit Type II at the next step.
        if not auto.contains(one_more.support, TYPE_II_EXP):
            raise SystemExit(
                f"seed {seed_residues}: repeated atom1 path exceeds claimed budget"
            )

    public = auto.classify(Q, list(seed_residues), 500_000, 8)
    if public["type_II_miss_states"] != len(states):
        raise SystemExit(
            f"seed {seed_residues}: graph closure disagrees with public automaton"
        )

    return {
        "seed_residues": list(seed_residues),
        "seed_exponents": [logs[r] for r in seed_residues],
        "type_II_miss_states": len(states),
        "scc_count": len(components),
        "positive_NR_edges_inside_SCCs": 0,
        "max_NR_valuation": maximum,
        "abstract_sharp_path_atoms": [1] * maximum,
        "abstract_sharp_path_residues": [2] * maximum,
        "abstract_sharp_endpoint_support_size": state.support.bit_count(),
    }


def nr_omega(factors: dict[int, int]) -> int:
    Q19 = {pow(x, 2, Q) for x in range(1, Q)}
    return sum(
        exponent
        for prime, exponent in factors.items()
        if prime % Q not in Q19
    )


def verify_witness(spec: dict[str, Any]) -> dict[str, Any]:
    p = int(spec["p"])
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: sharpness witness is not prime")
    if spec["expected_hard"] is not None and p % 840 != spec["expected_hard"]:
        raise SystemExit(
            f"p={p}: hard class {p % 840} != {spec['expected_hard']}"
        )

    stage = ancestry.classify_stage(p, 19)
    if stage["hit_class"] != spec["expected_hit"]:
        raise SystemExit(
            f"p={p}: k19 class {stage['hit_class']} != {spec['expected_hit']}"
        )
    if stage["hit_type_II"]:
        raise SystemExit(f"p={p}: witness does not miss Type II")

    C19 = int(stage["C"])
    factors = cylinder.factorint(C19)
    omega_nr = nr_omega(factors)
    if omega_nr != spec["expected_nr"]:
        raise SystemExit(
            f"p={p}: Omega_NR={omega_nr} != {spec['expected_nr']}"
        )

    expected_seed = tuple(spec["expected_seed"])
    for residue in expected_seed:
        if not any(prime % Q == residue % Q for prime in factors):
            raise SystemExit(
                f"p={p}: expected seed residue {residue} absent from factorization"
            )

    if spec.get("require_k11_phase"):
        T = (p + 23) // 24
        if T % 11 != 2:
            raise SystemExit(f"p={p}: T mod11={T % 11} !=2")
        stage11 = ancestry.classify_stage(p, 11)
        if stage11["sign"] != "-":
            raise SystemExit(f"p={p}: phase witness is not a k11 miss")
        if C19 % 11:
            raise SystemExit(f"p={p}: phase witness lacks forced factor11")

    return {
        "p": p,
        "p_mod_840": p % 840,
        "C19": C19,
        "factorization": cylinder.factor_text(factors),
        "Omega_NR": omega_nr,
        "k19_hit_class": stage["hit_class"],
        "seed": list(expected_seed),
    }


def verify() -> dict[str, Any]:
    budgets = {
        seed: weighted_budget(seed)
        for seed in EXPECTED
    }

    atlas = []
    for hard, (seed, bound) in HARD_ATLAS.items():
        if budgets[seed]["max_NR_valuation"] != bound:
            raise SystemExit(f"hard={hard}: atlas budget mismatch")
        atlas.append(
            {
                "p_mod_840": hard,
                "forced_k19_seed": list(seed),
                "Type_II_miss_max_Omega_NR": bound,
            }
        )

    # The k11-selected phase T=2 mod11 forces seed11 in h169/h529 and seed
    # [7,11] in h289.  Both exact budgets are 2.
    phase = {
        "T_mod_11": 2,
        "forced_factor": 11,
        "h169_seed": [11],
        "h169_max_Omega_NR": budgets[(11,)]["max_NR_valuation"],
        "h529_seed": [11],
        "h529_max_Omega_NR": budgets[(11,)]["max_NR_valuation"],
        "h289_seed": [7, 11],
        "h289_max_Omega_NR": budgets[(7, 11)]["max_NR_valuation"],
    }
    if {
        phase["h169_max_Omega_NR"],
        phase["h529_max_Omega_NR"],
        phase["h289_max_Omega_NR"],
    } != {2}:
        raise SystemExit("phase-seeded NR budget is not uniformly two")

    witnesses = [verify_witness(spec) for spec in WITNESSES]

    return {
        "verified": True,
        "mode": "k19-nr-valuation-budget",
        "global_theorem": (
            "If the exact k19 Type-II target misses, then the total valuation of "
            "quadratic-nonresidue prime factors of C19 is at most 8."
        ),
        "global_bound": 8,
        "global_bound_arithmetically_sharp": True,
        "budgets": [budgets[seed] for seed in EXPECTED],
        "hard_class_atlas": atlas,
        "k11_phase_T2_mod11": phase,
        "sharpness_and_regression_witnesses": witnesses,
        "proof_method": (
            "Exhaust the exact Type-II-miss transition graph; weight NR atom "
            "transitions by one; prove every SCC has only weight-zero internal "
            "edges; compute the longest path on the SCC condensation DAG."
        ),
        "claim_boundary": (
            "Exact fixed-shift q19 valuation theorem.  Bounds on hard lanes are "
            "theorem-safe consequences of forced QR seeds; not every hard-lane "
            "bound is claimed arithmetically sharp.  No Lane-I ceiling or "
            "Erdos-Straus proof follows by itself."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
