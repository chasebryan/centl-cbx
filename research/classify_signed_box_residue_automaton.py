#!/usr/bin/env python3
"""Exact finite automaton for prime-modulus signed-box residue states.

For an odd prime modulus q, choose a primitive root g and encode every unit
residue as an exponent in Z/(q-1)Z.  If

    C = product r_i

where prime-factor occurrences are counted with multiplicity, then its signed
box has exponent support

    S = sum_i { -a_i, 0, +a_i },

with r_i = g^a_i.  Treating a prime power q0^e as e repeated occurrences is
exact because the e-fold sum of {-a,0,+a} is {-ea,...,+ea}.

Adding one factor occurrence of exponent a therefore performs the exact state
transition

    A' = A + a,
    S' = S union (S+a) union (S-a),

where A is the exponent of C itself.

For Lane I, p == 4C (mod q).  The two targets are

    Type II: -1,
    Type I : -p^(-1).

Once Type II is present in S it can never disappear because every transition
contains the old support S.  Hence all possible Type-II-miss residue states can
be enumerated by a finite BFS that prunes only Type-II hits.  Type-I-only and
combined-miss states are then classified inside that exact finite closure.

The tool supports forced factor occurrences as a seed.  For k=23 on
Mordell-hard primes, seed residues 2,3 reproduce the known q23 thin-defect
companion classification.  For h121 at k=19, seed residues 5,7 reproduce the
forced QR-saturation theorem.  With no seed at q=19 it exposes the complete
local residue-state universe needed for the harder h169 lane.

This automaton classifies residue support only.  Arithmetic existence of a
particular state for a prime/corridor branch is a separate question.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class State:
    c_exp: int
    support: int


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def prime_factors(n: int) -> set[int]:
    out: set[int] = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def primitive_root(q: int) -> int:
    if not is_prime(q) or q == 2:
        raise ValueError("modulus must be an odd prime")
    phi = q - 1
    factors = prime_factors(phi)
    for g in range(2, q):
        if all(pow(g, phi // r, q) != 1 for r in factors):
            return g
    raise RuntimeError(f"no primitive root found modulo {q}")


def log_table(q: int, g: int) -> dict[int, int]:
    table: dict[int, int] = {}
    x = 1
    for e in range(q - 1):
        if x in table:
            raise RuntimeError("primitive-root cycle repeated early")
        table[x] = e
        x = (x * g) % q
    if len(table) != q - 1:
        raise RuntimeError("incomplete discrete-log table")
    return table


def rotate(mask: int, shift: int, n: int) -> int:
    shift %= n
    full = (1 << n) - 1
    if shift == 0:
        return mask & full
    return ((mask << shift) | (mask >> (n - shift))) & full


def transition(state: State, factor_exp: int, n: int) -> State:
    a = factor_exp % n
    support = (
        state.support
        | rotate(state.support, a, n)
        | rotate(state.support, -a, n)
    )
    return State((state.c_exp + a) % n, support)


def contains(mask: int, exponent: int) -> bool:
    return bool(mask & (1 << exponent))


def exponents(mask: int, n: int) -> list[int]:
    return [e for e in range(n) if contains(mask, e)]


def apply_seed(
    q: int,
    logs: dict[int, int],
    residues: list[int],
) -> tuple[State, list[int]]:
    n = q - 1
    state = State(0, 1)
    seed_exps: list[int] = []
    for residue in residues:
        r = residue % q
        if r == 0:
            raise ValueError(f"forced residue {residue} is not a unit modulo {q}")
        a = logs[r]
        seed_exps.append(a)
        state = transition(state, a, n)
    return state, seed_exps


def representative_path(
    state: State,
    parent: dict[State, tuple[State, int] | None],
    q: int,
    g: int,
) -> list[int]:
    exps: list[int] = []
    cur = state
    while parent[cur] is not None:
        prev, a = parent[cur]  # type: ignore[misc]
        exps.append(a)
        cur = prev
    exps.reverse()
    return [pow(g, a, q) for a in exps]


def classify(
    q: int,
    seed_residues: list[int],
    max_states: int,
    example_limit: int,
) -> dict[str, Any]:
    g = primitive_root(q)
    logs = log_table(q, g)
    n = q - 1
    log_minus_one = logs[q - 1]
    log_four = logs[4 % q]

    seed, seed_exps = apply_seed(q, logs, seed_residues)
    if contains(seed.support, log_minus_one):
        raise SystemExit("forced seed already hits Type II; no Type-II-miss closure exists")

    # Factor residue 1 is exponent zero and is exactly inert, so it is omitted
    # from the transition alphabet.  Every other unit residue is available as
    # a possible prime-factor residue class.
    alphabet = [a for a in range(1, n)]

    queue: deque[State] = deque([seed])
    seen: set[State] = {seed}
    parent: dict[State, tuple[State, int] | None] = {seed: None}
    depth: dict[State, int] = {seed: 0}

    pruned_type_ii = 0
    transitions_considered = 0
    while queue:
        state = queue.popleft()
        for a in alphabet:
            transitions_considered += 1
            nxt = transition(state, a, n)
            if contains(nxt.support, log_minus_one):
                pruned_type_ii += 1
                continue
            if nxt in seen:
                continue
            seen.add(nxt)
            parent[nxt] = (state, a)
            depth[nxt] = depth[state] + 1
            queue.append(nxt)
            if len(seen) > max_states:
                raise SystemExit(
                    f"state closure exceeded --max-states={max_states}; "
                    "increase the explicit safety bound"
                )

    combined: list[State] = []
    type_i_only: list[State] = []
    support_sizes: Counter[int] = Counter()
    combined_support_sizes: Counter[int] = Counter()
    type_i_support_sizes: Counter[int] = Counter()
    depth_counts: Counter[int] = Counter()
    c_residue_counts: Counter[int] = Counter()
    qr_only_combined = 0
    qr_exponents = set(range(0, n, 2))

    for state in seen:
        support_size = state.support.bit_count()
        support_sizes[support_size] += 1
        depth_counts[depth[state]] += 1

        # p = 4C, so log(p)=log(4)+A.  Multiplying by -1 and inverting
        # gives Type-I target exponent log(-1)-log(4)-A.
        target_i = (log_minus_one - log_four - state.c_exp) % n
        if contains(state.support, target_i):
            type_i_only.append(state)
            type_i_support_sizes[support_size] += 1
        else:
            combined.append(state)
            combined_support_sizes[support_size] += 1
            c_residue_counts[pow(g, state.c_exp, q)] += 1
            if set(exponents(state.support, n)).issubset(qr_exponents):
                qr_only_combined += 1

    def describe(state: State) -> dict[str, Any]:
        A = state.c_exp
        C = pow(g, A, q)
        p = (4 * C) % q
        target_i = (log_minus_one - log_four - A) % n
        path = representative_path(state, parent, q, g)
        return {
            "minimal_added_factor_occurrences": depth[state],
            "representative_added_residues": path,
            "C_mod_q": C,
            "p_mod_q": p,
            "C_exponent": A,
            "support_size": state.support.bit_count(),
            "support_exponents": exponents(state.support, n),
            "support_residues": sorted(pow(g, e, q) for e in exponents(state.support, n)),
            "type_II_target": q - 1,
            "type_I_target": pow(g, target_i, q),
            "type_I_target_exponent": target_i,
        }

    type_i_examples = sorted(
        type_i_only,
        key=lambda s: (depth[s], s.support.bit_count(), s.c_exp, s.support),
    )[:example_limit]
    combined_examples = sorted(
        combined,
        key=lambda s: (depth[s], s.support.bit_count(), s.c_exp, s.support),
    )[:example_limit]

    return {
        "verified": True,
        "mode": "signed-box-residue-automaton",
        "modulus": q,
        "primitive_root": g,
        "group_order": n,
        "log_minus_one": log_minus_one,
        "log_four": log_four,
        "seed_residues": seed_residues,
        "seed_exponents": seed_exps,
        "seed_support_size": seed.support.bit_count(),
        "type_II_miss_states": len(seen),
        "combined_miss_states": len(combined),
        "type_I_only_states": len(type_i_only),
        "qr_only_combined_miss_states": qr_only_combined,
        "transitions_considered": transitions_considered,
        "transitions_pruned_after_type_II_hit": pruned_type_ii,
        "support_size_distribution": dict(sorted(support_sizes.items())),
        "combined_support_size_distribution": dict(sorted(combined_support_sizes.items())),
        "type_I_only_support_size_distribution": dict(sorted(type_i_support_sizes.items())),
        "minimal_depth_distribution": dict(sorted(depth_counts.items())),
        "combined_C_residue_distribution": dict(sorted(c_residue_counts.items())),
        "type_I_only_examples": [describe(s) for s in type_i_examples],
        "combined_miss_examples": [describe(s) for s in combined_examples],
        "claim_boundary": (
            "The automaton exhausts abstract prime-factor residue/multiplicity states "
            "modulo q reachable from the supplied seed while Type II remains absent. "
            "It does not assert arithmetic realization by a prime corridor candidate."
        ),
    }


def self_test() -> int:
    # q=7 with forced factor 2: Type-II misses are exactly QR-support states;
    # Type-I and Type-II coincide for the Mordell-hard application seed.
    q7 = classify(7, [2], 10000, 8)
    if q7["type_I_only_states"] != 0:
        raise SystemExit("q7 seed unexpectedly admits Type-I-only state")

    # q=23 with forced 2,3 must contain Type-I-only residue states.  The exact
    # companion verifier separately identifies their 5^2/14^2 normal forms.
    q23 = classify(23, [2, 3], 200000, 16)
    if q23["type_I_only_states"] < 2:
        raise SystemExit("q23 seed failed to recover Type-I-only residue states")

    # h121 k19 forced 5,7 fill QR19.  Any NR occurrence hits Type II, so no
    # Type-I-only state can remain in the Type-II-miss closure.
    q19_h121 = classify(19, [5, 7], 100000, 8)
    if q19_h121["type_I_only_states"] != 0:
        raise SystemExit("h121 q19 seed unexpectedly admits Type-I-only state")

    print(
        json.dumps(
            {
                "self_test": "ok",
                "q7_states": q7["type_II_miss_states"],
                "q23_states": q23["type_II_miss_states"],
                "q19_h121_states": q19_h121["type_II_miss_states"],
            },
            sort_keys=True,
        )
    )
    return 0


def parse_seed(text: str) -> list[int]:
    if not text.strip():
        return []
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enumerate exact prime-modulus signed-box residue states"
    )
    parser.add_argument("--modulus", type=int, default=19)
    parser.add_argument(
        "--seed",
        default="",
        help="comma-separated forced factor residues, counted with multiplicity",
    )
    parser.add_argument("--max-states", type=int, default=500000)
    parser.add_argument("--example-limit", type=int, default=32)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    result = classify(
        args.modulus,
        parse_seed(args.seed),
        args.max_states,
        args.example_limit,
    )
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
