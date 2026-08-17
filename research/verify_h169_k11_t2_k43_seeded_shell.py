#!/usr/bin/env python3
"""Verify the exact h169 k11 t=2 mod11 -> seeded k43 shell.

For h169 write p=169+840t and T=(p+23)/24=8+35t.  The exact h169
k11 combined-miss theorem restricts

    t mod11 in {0,2,3,4,8}.

On the child t=2 mod11 we have T=1 mod11.  Since

    C43 = (p+43)/4 = 6T+5,

literal prime11 divides C43.

Modulo43, primitive root 3 gives log_3(11)=30 and ord_43(11)=7.  One
forced occurrence of factor11 therefore preloads signed support

    {1, 11, 11^(-1)} = {1,11,4}.

This verifier exhausts the exact q43 Type-II-miss signed-box automaton from
that seed and compares it with the unseeded local universe.  It also weights
quadratic-nonresidue factor occurrences by one and proves, via SCC
condensation, an exact finite NR-valuation budget.

Seed11 consequences verified here:

  * Type-II-miss states: 18048 -> 2317
  * combined-miss states: 7740 -> 1217
  * max NR valuation under Type-II miss: 20 -> 14
  * no positive-NR edge occurs inside an SCC
  * any additional factor occurrence congruent to 32,39,42 mod43 hits Type II
  * combined miss excludes C43 == 8 mod43 in addition to the two generic
    impossible C residues 32 and42
  * on h169, C43==8 is p==32 and t==9 mod43, so this phase is excluded.

The automaton is a local exact residue/multiplicity theorem.  It does not
assert that every abstract state is arithmetically realized by an h169 prime.
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
import verify_h169_k11_future_factor_partition as future  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402

Q = 43
N = 42
SEED = (11,)
HARD = 169
SELECTED_t11 = 2
SELECTED_T11 = 1
EXPECTED = {
    (): {
        "type_II_miss_states": 18_048,
        "combined_miss_states": 7_740,
        "type_I_only_states": 10_308,
        "max_depth": 5,
        "max_NR_valuation": 20,
    },
    SEED: {
        "type_II_miss_states": 2_317,
        "combined_miss_states": 1_217,
        "type_I_only_states": 1_100,
        "max_depth": 4,
        "max_NR_valuation": 14,
    },
}

REGRESSIONS = {
    48_049: "miss",
    177_409: "type-II-only",
    583_969: "both",
    1_498_729: "type-I-only",
}


def multiplicative_order(a: int, q: int) -> int:
    x = 1
    for n in range(1, q):
        x = x * a % q
        if x == 1:
            return n
    raise RuntimeError("multiplicative order not found")


def type_targets(state: auto.State, logs: dict[int, int]) -> tuple[int, int]:
    log_minus_one = logs[Q - 1]
    log_four = logs[4]
    target_i = (log_minus_one - log_four - state.c_exp) % N
    return target_i, log_minus_one


def state_class(state: auto.State, logs: dict[int, int]) -> str:
    target_i, target_ii = type_targets(state, logs)
    hit_i = auto.contains(state.support, target_i)
    hit_ii = auto.contains(state.support, target_ii)
    if hit_i and hit_ii:
        return "both"
    if hit_i:
        return "type-I-only"
    if hit_ii:
        return "type-II-only"
    return "miss"


def build_type_ii_miss_graph(seed_residues: tuple[int, ...]) -> dict[str, Any]:
    g = auto.primitive_root(Q)
    logs = auto.log_table(Q, g)
    start, seed_exps = auto.apply_seed(Q, logs, list(seed_residues))
    target_ii = logs[Q - 1]
    if auto.contains(start.support, target_ii):
        raise SystemExit(f"seed {seed_residues} already hits Type II")

    queue: deque[auto.State] = deque([start])
    seen = {start}
    depth = {start: 0}
    edges: dict[auto.State, list[tuple[auto.State, int]]] = defaultdict(list)

    for_state_atoms = range(1, N)  # exponent0 / residue1 is inert
    while queue:
        state = queue.popleft()
        for atom in for_state_atoms:
            nxt = auto.transition(state, atom, N)
            if auto.contains(nxt.support, target_ii):
                continue
            # primitive-root exponent parity is exactly QR/NR character
            edges[state].append((nxt, atom & 1))
            if nxt not in seen:
                seen.add(nxt)
                depth[nxt] = depth[state] + 1
                queue.append(nxt)

    combined = 0
    type_i_only = 0
    c_combined: set[int] = set()
    for state in seen:
        cls = state_class(state, logs)
        if cls == "miss":
            combined += 1
            c_combined.add(pow(g, state.c_exp, Q))
        elif cls == "type-I-only":
            type_i_only += 1
        else:
            raise SystemExit("Type-II-miss graph contains a Type-II hit")

    expected = EXPECTED[seed_residues]
    observed = {
        "type_II_miss_states": len(seen),
        "combined_miss_states": combined,
        "type_I_only_states": type_i_only,
        "max_depth": max(depth.values()),
    }
    for key, value in observed.items():
        if value != expected[key]:
            raise SystemExit(
                f"seed {seed_residues}: {key}={value} != {expected[key]}"
            )

    return {
        "g": g,
        "logs": logs,
        "start": start,
        "seed_exponents": seed_exps,
        "states": seen,
        "depth": depth,
        "edges": edges,
        "combined_C_residues": c_combined,
        **observed,
    }


def tarjan_scc(
    states: set[auto.State],
    edges: dict[auto.State, list[tuple[auto.State, int]]],
) -> tuple[list[list[auto.State]], dict[auto.State, int]]:
    index = 0
    indices: dict[auto.State, int] = {}
    low: dict[auto.State, int] = {}
    stack: list[auto.State] = []
    on_stack: set[auto.State] = set()
    components: list[list[auto.State]] = []

    sys.setrecursionlimit(max(100_000, 4 * len(states) + 100))

    def visit(v: auto.State) -> None:
        nonlocal index
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w, _ in edges.get(v, []):
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


def nr_valuation_budget(graph: dict[str, Any]) -> dict[str, int]:
    states = graph["states"]
    edges = graph["edges"]
    start = graph["start"]
    components, component_of = tarjan_scc(states, edges)

    positive_internal = 0
    dag_weight: dict[tuple[int, int], int] = {}
    for src in states:
        for dst, weight in edges.get(src, []):
            u = component_of[src]
            v = component_of[dst]
            if u == v:
                positive_internal += weight
                continue
            key = (u, v)
            dag_weight[key] = max(weight, dag_weight.get(key, -1))

    if positive_internal:
        raise SystemExit(
            f"positive-NR transition occurs inside SCC: total={positive_internal}"
        )

    dag: dict[int, list[tuple[int, int]]] = defaultdict(list)
    indegree = [0] * len(components)
    for (u, v), weight in dag_weight.items():
        dag[u].append((v, weight))
        indegree[v] += 1

    queue: deque[int] = deque(i for i, degree in enumerate(indegree) if degree == 0)
    topo: list[int] = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v, _ in dag.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(topo) != len(components):
        raise SystemExit("SCC condensation graph is not acyclic")

    neg = -10**9
    best = [neg] * len(components)
    best[component_of[start]] = 0
    for u in topo:
        if best[u] == neg:
            continue
        for v, weight in dag.get(u, []):
            best[v] = max(best[v], best[u] + weight)

    maximum = max(best)
    return {
        "scc_count": len(components),
        "positive_NR_edges_inside_SCCs": positive_internal,
        "max_NR_valuation": maximum,
    }


def one_occurrence_absorbers(seed_graph: dict[str, Any]) -> dict[str, Any]:
    g = seed_graph["g"]
    logs = seed_graph["logs"]
    start = seed_graph["start"]
    target_ii = logs[Q - 1]

    type_ii = []
    classes: Counter[str] = Counter()
    for residue in range(2, Q):
        nxt = auto.transition(start, logs[residue], N)
        cls = state_class(nxt, logs)
        classes[cls] += 1
        if auto.contains(nxt.support, target_ii):
            type_ii.append(residue)

    if type_ii != [32, 39, 42]:
        raise SystemExit(f"seed11 one-occurrence Type-II absorbers changed: {type_ii}")
    if classes != Counter({"miss": 38, "both": 3}):
        raise SystemExit(f"seed11 one-occurrence class split changed: {classes}")

    return {
        "additional_factor_residues_forcing_Type_II": type_ii,
        "one_occurrence_class_split": dict(sorted(classes.items())),
        "support_consequence": (
            "If Type II misses after the forced factor11, no additional prime-factor "
            "occurrence may be congruent to 32,39,or42 modulo43."
        ),
    }


def seed_shell(seed_graph: dict[str, Any], generic_graph: dict[str, Any]) -> dict[str, Any]:
    g = seed_graph["g"]
    logs = seed_graph["logs"]
    start = seed_graph["start"]
    seed_support = sorted(
        pow(g, e, Q) for e in auto.exponents(start.support, N)
    )
    if g != 3 or logs[11] != 30:
        raise SystemExit(f"unexpected q43 primitive-root data g={g}, log11={logs[11]}")
    if multiplicative_order(11, Q) != 7:
        raise SystemExit("ord_43(11) changed")
    if seed_support != [1, 4, 11]:
        raise SystemExit(f"seed11 signed support changed: {seed_support}")

    generic_missing = sorted(set(range(1, Q)) - generic_graph["combined_C_residues"])
    seeded_missing = sorted(set(range(1, Q)) - seed_graph["combined_C_residues"])
    if generic_missing != [32, 42]:
        raise SystemExit(f"generic combined-miss C exclusions changed: {generic_missing}")
    if seeded_missing != [8, 32, 42]:
        raise SystemExit(f"seed11 combined-miss C exclusions changed: {seeded_missing}")

    # Human-readable reason for the new C=8 exclusion.
    # If C=8 then p=4C=32 and the Type-I target -p^{-1} is 4, which is already
    # in the forced factor11 signed support {1,4,11}.
    C = 8
    p_residue = 4 * C % Q
    type_i_target = (-pow(p_residue, -1, Q)) % Q
    if (p_residue, type_i_target) != (32, 4):
        raise SystemExit("C=8 Type-I shell calculation changed")
    if type_i_target not in seed_support:
        raise SystemExit("forced seed no longer contains C=8 Type-I target")

    # In h169, p=169+840t = 40+23t mod43.  The new p=32 exclusion is exactly
    # t=9 mod43.
    excluded_t43 = [t for t in range(Q) if (169 + 840 * t) % Q == p_residue]
    if excluded_t43 != [9]:
        raise SystemExit(f"h169 C=8 phase exclusion changed: {excluded_t43}")

    return {
        "primitive_root": g,
        "log_3_11": logs[11],
        "order_43_11": 7,
        "forced_signed_support": seed_support,
        "generic_combined_miss_C_exclusions": generic_missing,
        "seed11_combined_miss_C_exclusions": seeded_missing,
        "new_seeded_C_exclusion": 8,
        "new_seeded_p_exclusion": p_residue,
        "new_seeded_Type_I_target": type_i_target,
        "h169_new_excluded_t_mod_43": 9,
    }


def nr_omega(factors: dict[int, int]) -> int:
    qr = {pow(x, 2, Q) for x in range(1, Q)}
    return sum(
        exponent
        for prime, exponent in factors.items()
        if prime % Q not in qr
    )


def factorization_state(C: int, logs: dict[int, int]) -> auto.State:
    state = auto.State(0, 1)
    for prime, exponent in sorted(cylinder.factorint(C).items()):
        residue = prime % Q
        if residue == 0:
            raise SystemExit(f"C={C}: factor43 makes q43 state undefined")
        atom = logs[residue]
        for _ in range(exponent):
            state = auto.transition(state, atom, N)
    return state


def regression(p: int, expected_class: str, seed_graph: dict[str, Any]) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: regression witness is not prime")
    if p % 840 != HARD:
        raise SystemExit(f"p={p}: hard class {p % 840} !=169")
    t = (p - 169) // 840
    if t % 11 != SELECTED_t11:
        raise SystemExit(f"p={p}: t mod11={t % 11} !=2")

    stage11 = ancestry.classify_stage(p, 11)
    if stage11["hit_class"] != "miss":
        raise SystemExit(f"p={p}: k11 class {stage11['hit_class']} !=miss")

    stage43 = ancestry.classify_stage(p, 43)
    if stage43["hit_class"] != expected_class:
        raise SystemExit(
            f"p={p}: k43 class {stage43['hit_class']} !={expected_class}"
        )
    C43 = int(stage43["C"])
    if C43 % 11:
        raise SystemExit(f"p={p}: selected k11 phase failed to force 11|C43")

    factors = cylinder.factorint(C43)
    state = factorization_state(C43, seed_graph["logs"])
    if state_class(state, seed_graph["logs"]) != expected_class:
        raise SystemExit(f"p={p}: factorization state disagrees with exact stage")

    return {
        "p": p,
        "t_mod_11": t % 11,
        "p_mod_43": p % 43,
        "C43": C43,
        "C43_mod_43": C43 % 43,
        "factorization": cylinder.factor_text(factors),
        "Omega_NR_mod43": nr_omega(factors),
        "k11_hit_class": stage11["hit_class"],
        "k43_hit_class": stage43["hit_class"],
    }


def verify_phase() -> dict[str, Any]:
    partition = future.verify()
    if partition["k11_combined_miss_implies_t_mod_11"] != [0, 2, 3, 4, 8]:
        raise SystemExit("h169 k11 phase domain changed")
    rows = [
        row for row in partition["partition"]
        if row["t_mod_11"] == SELECTED_t11
    ]
    if len(rows) != 1:
        raise SystemExit("selected t11 phase missing from future factor partition")
    row = rows[0]
    if row["T_mod_11"] != SELECTED_T11 or row["shift_k"] != 43:
        raise SystemExit(f"selected t11=2 calendar row changed: {row}")
    if (6 * SELECTED_T11 + 5) % 11:
        raise SystemExit("T11=1 no longer forces factor11 into C43")
    return {
        "t_mod_11": SELECTED_t11,
        "T_mod_11": SELECTED_T11,
        "forced_factor": 11,
        "forced_coordinate": "C43=6T+5",
    }


def compact_graph_report(
    seed_residues: tuple[int, ...], graph: dict[str, Any], budget: dict[str, int]
) -> dict[str, Any]:
    return {
        "seed_residues": list(seed_residues),
        "seed_exponents": graph["seed_exponents"],
        "type_II_miss_states": graph["type_II_miss_states"],
        "combined_miss_states": graph["combined_miss_states"],
        "type_I_only_states": graph["type_I_only_states"],
        "max_minimal_depth": graph["max_depth"],
        **budget,
    }


def verify() -> dict[str, Any]:
    phase = verify_phase()

    generic = build_type_ii_miss_graph(())
    seeded = build_type_ii_miss_graph(SEED)
    generic_budget = nr_valuation_budget(generic)
    seeded_budget = nr_valuation_budget(seeded)
    if generic_budget["max_NR_valuation"] != EXPECTED[()]["max_NR_valuation"]:
        raise SystemExit("generic q43 NR budget changed")
    if seeded_budget["max_NR_valuation"] != EXPECTED[SEED]["max_NR_valuation"]:
        raise SystemExit("seed11 q43 NR budget changed")

    # Cross-check the closure counts against the independent public classifier.
    for seed_residues, graph in (((), generic), (SEED, seeded)):
        public = auto.classify(Q, list(seed_residues), 100_000, 4)
        for key in (
            "type_II_miss_states",
            "combined_miss_states",
            "type_I_only_states",
        ):
            if public[key] != graph[key]:
                raise SystemExit(
                    f"seed {seed_residues}: public classifier {key} disagreement"
                )

    shell = seed_shell(seeded, generic)
    absorbers = one_occurrence_absorbers(seeded)
    witnesses = [
        regression(p, cls, seeded)
        for p, cls in REGRESSIONS.items()
    ]

    generic_report = compact_graph_report((), generic, generic_budget)
    seeded_report = compact_graph_report(SEED, seeded, seeded_budget)

    return {
        "verified": True,
        "mode": "h169-k11-t2-k43-seeded-shell",
        "phase": phase,
        "q43_generic": generic_report,
        "q43_seed11": seeded_report,
        "contraction": {
            "Type_II_miss_states_removed": (
                generic_report["type_II_miss_states"]
                - seeded_report["type_II_miss_states"]
            ),
            "combined_miss_states_removed": (
                generic_report["combined_miss_states"]
                - seeded_report["combined_miss_states"]
            ),
            "NR_valuation_budget_drop": (
                generic_report["max_NR_valuation"]
                - seeded_report["max_NR_valuation"]
            ),
        },
        "seed_shell": shell,
        "one_occurrence_absorbers": absorbers,
        "regressions": witnesses,
        "theorem": (
            "For h169 under inherited k11 miss on t=2 mod11, literal factor11 "
            "enters C43.  The exact seeded q43 Type-II-miss closure has 2317 "
            "states (1217 combined misses), forbids additional factor residues "
            "32,39,42 mod43, excludes t=9 mod43 from a combined miss, and has "
            "Omega_NR(C43)<=14 instead of the generic local bound20."
        ),
        "claim_boundary": (
            "Exact local seeded signed-box theorem plus exact h169 phase bridge. "
            "It does not assert every abstract state or phase is arithmetically "
            "realized, does not force a k43 hit, and does not prove Erdos-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
