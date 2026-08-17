#!/usr/bin/env python3
"""Verify exact finite state compression for the combined k=19 BREC coordinate.

For a Mordell-hard prime p, put C=(p+19)/4.  Since p != 19, every prime
factor of C is a unit modulo 19.  The unit group is cyclic of order 18 and 2
is a primitive root.  Write each prime factor residue as 2^a and expand
multiplicity into valuation atoms a_1,...,a_n.

The exact signed-box state is then

    c = sum a_i mod 18,
    S = sum_i {-a_i, 0, a_i}  subset Z/18Z.

Because p == 4C == 2^(c+2) mod 19, the two exact targets have exponents

    Type II : 9,
    Type I  : 7-c mod 18.

Thus combined miss is exactly

    9 not in S and 7-c not in S.

This verifier exhausts the finite closure of all possible (c,S) states under
all 18 residue atoms.  It proves by complete enumeration that:

  * only 439 distinct exact cyclic states are reachable;
  * every reachable state has a canonical representative of <=4 atoms;
  * the unique state needing 4 atoms has full support and is constructive;
  * exactly 136 reachable states are combined misses;
  * every combined-miss state has a canonical representative of <=3 atoms.

The canonical atom bound is a state-compression theorem, not a bound on the
number of prime factors of C.  Extra factors can collapse to the same cyclic
state.

The script also reconstructs several exact prime witnesses independently from
factorization and compares the compressed classification to the CBX signed-box
classifier.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "kernel"
sys.path.insert(0, str(KERNEL))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze_brec_cylinder as cylinder  # noqa: E402
import verify_k23_brec_ancestry_falsifiers as ancestry  # noqa: E402

MODULUS = 19
GROUP_ORDER = 18
GENERATOR = 2
TYPE_II_EXP = 9


def discrete_log_table() -> dict[int, int]:
    table: dict[int, int] = {}
    x = 1
    for a in range(GROUP_ORDER):
        if x in table:
            raise SystemExit("2 is not primitive modulo 19")
        table[x] = a
        x = (x * GENERATOR) % MODULUS
    if x != 1 or len(table) != GROUP_ORDER:
        raise SystemExit("failed to enumerate U(19) with generator 2")
    return table


DLOG = discrete_log_table()


def mask_values(mask: int) -> list[int]:
    return [x for x in range(GROUP_ORDER) if mask & (1 << x)]


def add_atom(mask: int, a: int) -> int:
    """Minkowski-add the signed valuation atom {-a,0,+a}."""
    out = 0
    a %= GROUP_ORDER
    for s in range(GROUP_ORDER):
        if not (mask & (1 << s)):
            continue
        out |= 1 << s
        out |= 1 << ((s + a) % GROUP_ORDER)
        out |= 1 << ((s - a) % GROUP_ORDER)
    return out


def is_combined_miss(c: int, mask: int) -> bool:
    type_i_exp = (7 - c) % GROUP_ORDER
    return not (mask & (1 << TYPE_II_EXP)) and not (mask & (1 << type_i_exp))


def closure() -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], tuple[tuple[int, int], int]]]:
    start = (0, 1 << 0)
    distance = {start: 0}
    predecessor: dict[tuple[int, int], tuple[tuple[int, int], int]] = {}
    queue: deque[tuple[int, int]] = deque([start])

    while queue:
        c, mask = queue.popleft()
        depth = distance[(c, mask)]
        for a in range(GROUP_ORDER):
            nxt = ((c + a) % GROUP_ORDER, add_atom(mask, a))
            if nxt in distance:
                continue
            distance[nxt] = depth + 1
            predecessor[nxt] = ((c, mask), a)
            queue.append(nxt)

    # Closure check: every state remains in the finite set under every atom.
    for c, mask in distance:
        for a in range(GROUP_ORDER):
            nxt = ((c + a) % GROUP_ORDER, add_atom(mask, a))
            if nxt not in distance:
                raise SystemExit("finite k19 state set is not closed")

    return distance, predecessor


def canonical_atoms(
    state: tuple[int, int],
    predecessor: dict[tuple[int, int], tuple[tuple[int, int], int]],
) -> list[int]:
    start = (0, 1)
    atoms: list[int] = []
    cur = state
    while cur != start:
        prev, atom = predecessor[cur]
        atoms.append(atom)
        cur = prev
    atoms.reverse()
    return atoms


def state_from_factorization(C: int) -> dict[str, Any]:
    factors = cylinder.factorint(C)
    c = 0
    mask = 1
    atoms: list[int] = []

    for q, exponent in sorted(factors.items()):
        residue = q % MODULUS
        if residue == 0:
            raise SystemExit(f"C={C}: factor 19 is not a unit")
        a = DLOG[residue]
        for _ in range(exponent):
            atoms.append(a)
            c = (c + a) % GROUP_ORDER
            mask = add_atom(mask, a)

    # Product exponent must agree with the actual C residue.
    if pow(GENERATOR, c, MODULUS) != C % MODULUS:
        raise SystemExit(f"C={C}: compressed product exponent mismatch")

    return {
        "C": C,
        "factorization": cylinder.factor_text(factors),
        "valuation_atoms": atoms,
        "c": c,
        "support_exponents": mask_values(mask),
        "support_size": mask.bit_count(),
        "type_II_exp": TYPE_II_EXP,
        "type_I_exp": (7 - c) % GROUP_ORDER,
        "combined_miss": is_combined_miss(c, mask),
        "state": (c, mask),
    }


def verify_prime_witness(
    p: int,
    expected_history: str,
    expected_miss: bool,
    expected_atoms: list[int] | None = None,
) -> dict[str, Any]:
    if not cylinder.is_prime64(p):
        raise SystemExit(f"p={p}: not prime")
    stage = ancestry.classify_stage(p, 19)
    if not stage["defined"]:
        raise SystemExit(f"p={p}: k19 unexpectedly undefined")

    early = [ancestry.classify_stage(p, k) for k in (3, 7, 11, 15, 19)]
    history = "".join(str(x["sign"]) for x in early)
    if history != expected_history:
        raise SystemExit(f"p={p}: history {history} != {expected_history}")

    C = int(stage["C"])
    compressed = state_from_factorization(C)
    if compressed["combined_miss"] != expected_miss:
        raise SystemExit(f"p={p}: compressed k19 classification mismatch")
    if (stage["sign"] == "-") != expected_miss:
        raise SystemExit(f"p={p}: compressed state disagrees with exact CBX stage")
    if expected_atoms is not None and compressed["valuation_atoms"] != expected_atoms:
        raise SystemExit(
            f"p={p}: atoms {compressed['valuation_atoms']} != {expected_atoms}"
        )

    support_residues = sorted(pow(GENERATOR, e, MODULUS) for e in compressed["support_exponents"])
    exact_support = sorted(cylinder.signed_box_support(cylinder.factorint(C), MODULUS)[0])
    if support_residues != exact_support:
        raise SystemExit(f"p={p}: exponent support does not match exact residue support")

    return {
        "p": p,
        "early_history": history,
        **{k: v for k, v in compressed.items() if k != "state"},
    }


def verify() -> dict[str, Any]:
    distance, predecessor = closure()
    states = list(distance)
    misses = [state for state in states if is_combined_miss(*state)]

    if len(states) != 439:
        raise SystemExit(f"reachable state count {len(states)} != 439")
    if len(misses) != 136:
        raise SystemExit(f"combined-miss state count {len(misses)} != 136")

    max_depth = max(distance.values())
    max_miss_depth = max(distance[state] for state in misses)
    if max_depth != 4:
        raise SystemExit(f"maximum canonical state depth {max_depth} != 4")
    if max_miss_depth != 3:
        raise SystemExit(f"maximum canonical miss depth {max_miss_depth} != 3")

    depth4 = [state for state, depth in distance.items() if depth == 4]
    if len(depth4) != 1:
        raise SystemExit(f"expected one depth-4 state, got {len(depth4)}")
    c4, mask4 = depth4[0]
    if c4 != 0 or mask4 != (1 << GROUP_ORDER) - 1:
        raise SystemExit("unique depth-4 state is not c=0 with full support")
    if is_combined_miss(c4, mask4):
        raise SystemExit("full-support depth-4 state cannot be a miss")

    state_depth_hist = Counter(distance.values())
    miss_depth_hist = Counter(distance[state] for state in misses)
    miss_support_hist = Counter(state[1].bit_count() for state in misses)

    # Every support is symmetric and contains exponent zero by construction.
    for _, mask in states:
        if not (mask & 1):
            raise SystemExit("reachable signed support lost zero")
        for e in mask_values(mask):
            if not (mask & (1 << ((-e) % GROUP_ORDER))):
                raise SystemExit("reachable signed support lost inversion symmetry")

    # Freeze the unique largest miss support.  It misses only exponent 9, so
    # combined failure forces the Type-I exponent to coincide with 9.
    largest_miss_size = max(state[1].bit_count() for state in misses)
    largest = [state for state in misses if state[1].bit_count() == largest_miss_size]
    if largest_miss_size != 17 or len(largest) != 1:
        raise SystemExit("unexpected largest k19 miss state")
    lc, lm = largest[0]
    if lc != 16 or mask_values(((1 << GROUP_ORDER) - 1) ^ lm) != [9]:
        raise SystemExit("largest k19 miss is not the expected c=16 / missing{-1} state")

    witnesses = [
        verify_prime_witness(18_766_609, "-----", True, [4, 10]),
        verify_prime_witness(27_211_969, "-----", True, [8]),
        verify_prime_witness(8_243_281, "---++", False, [16, 16, 5, 10, 15]),
        verify_prime_witness(5_151_841, "-++-+", False, [16, 6, 6, 6, 17]),
    ]

    canonical_miss_examples = []
    for state in sorted(misses, key=lambda s: (distance[s], s[0], s[1])):
        c, mask = state
        canonical_miss_examples.append(
            {
                "c": c,
                "support_size": mask.bit_count(),
                "type_I_exp": (7 - c) % GROUP_ORDER,
                "canonical_atoms": canonical_atoms(state, predecessor),
            }
        )

    return {
        "verified": True,
        "mode": "k19-brec-cyclic-state-compression",
        "modulus": MODULUS,
        "generator": GENERATOR,
        "group_order": GROUP_ORDER,
        "target_exponents": {"type_II": 9, "type_I": "7-c mod 18"},
        "reachable_states": len(states),
        "combined_miss_states": len(misses),
        "max_canonical_atoms_all_states": max_depth,
        "max_canonical_atoms_combined_miss": max_miss_depth,
        "state_depth_histogram": {str(k): state_depth_hist[k] for k in sorted(state_depth_hist)},
        "miss_depth_histogram": {str(k): miss_depth_hist[k] for k in sorted(miss_depth_hist)},
        "miss_support_size_histogram": {str(k): miss_support_hist[k] for k in sorted(miss_support_hist)},
        "unique_depth4_state": {
            "c": c4,
            "support_size": mask4.bit_count(),
            "constructive": True,
        },
        "largest_combined_miss_state": {
            "c": lc,
            "support_size": lm.bit_count(),
            "missing_exponents": mask_values(((1 << GROUP_ORDER) - 1) ^ lm),
            "canonical_atoms": canonical_atoms(largest[0], predecessor),
        },
        "witnesses": witnesses,
        "canonical_miss_states": canonical_miss_examples,
        "claim_boundary": (
            "Exact finite cyclic-state compression at fixed k=19 only. The atom bound "
            "is not a bound on Omega(C19), does not create pruning authority, and does "
            "not prove a bounded Lane-I corridor or Erdős-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
