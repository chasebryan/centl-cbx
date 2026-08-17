#!/usr/bin/env python3
"""Theorem-backed obligation and contradiction-core analyzer for h169.

This tool sits *above* the exact h169 dependency propagator.  It does not add
new mathematical pruning rules.  Instead it turns the existing theorem grammar
into two research products:

1. for a surviving formal state, an explicit arithmetic obligation ledger;
2. for a contradictory partial state, an inclusion-minimal unsatisfiable core
   over the supplied assumptions and the already-landed theorem rules.

The core is irreducible under deletion, not claimed minimum-cardinality.  Its
scope is exactly the realized h169 Route-A/Route-B simultaneous-survivor
laboratory encoded by ``propagate_h169_dependency_state.py``.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Iterable

import propagate_h169_dependency_state as dep


ROUTE_SEED = {
    "A": {"S": 391, "factorization": "17*23"},
    "B": {"S": 1081, "factorization": "23*47"},
}

RESERVOIRS = ("R", "B", "E", "D", "F", "G", "H", "J", "K", "L")


@dataclass(frozen=True)
class Atom:
    kind: str
    key: str
    payload: object

    def public(self) -> dict[str, object]:
        if self.kind == "assumption":
            field, allowed = self.payload  # type: ignore[misc]
            return {
                "kind": "assumption",
                "field": field,
                "allowed": sorted(allowed, key=str),
            }
        rule = self.payload
        return {
            "kind": "theorem",
            "name": rule.name,
            "statement": rule.statement,
        }


def assumption_atoms(
    constraints: dict[str, frozenset[object]],
) -> list[Atom]:
    return [
        Atom("assumption", f"assumption:{field}", (field, allowed))
        for field, allowed in constraints.items()
    ]


def theorem_atoms() -> list[Atom]:
    return [
        Atom("theorem", f"theorem:{rule.name}", rule)
        for rule in dep.RULES
    ]


def state_satisfies_atoms(route: str, state: dep.State, atoms: Iterable[Atom]) -> bool:
    for atom in atoms:
        if atom.kind == "assumption":
            field, allowed = atom.payload  # type: ignore[misc]
            if getattr(state, field) not in allowed:
                return False
        else:
            rule = atom.payload
            if not rule.predicate(route, state):
                return False
    return True


def has_formal_state(route: str, atoms: Iterable[Atom]) -> bool:
    """Return as soon as one formal grammar state satisfies all atoms."""
    frozen = tuple(atoms)
    return any(
        state_satisfies_atoms(route, state, frozen)
        for state in dep.naive_states(route)
    )


def contradiction(route: str, atoms: Iterable[Atom]) -> bool:
    return not has_formal_state(route, atoms)


def irreducible_unsat_core(route: str, atoms: list[Atom]) -> list[Atom]:
    """Deletion-minimize an unsatisfiable atom set to a fixed point.

    The result is inclusion-minimal: deleting any one retained atom makes the
    formal grammar satisfiable.  No minimum-cardinality claim is made.
    """
    if not contradiction(route, atoms):
        raise ValueError("cannot extract an unsat core from a satisfiable atom set")

    core = list(atoms)
    changed = True
    while changed:
        changed = False
        for atom in tuple(core):
            trial = [candidate for candidate in core if candidate.key != atom.key]
            if contradiction(route, trial):
                core = trial
                changed = True

    # Guard the advertised irreducibility property directly.
    if not contradiction(route, core):
        raise AssertionError("core minimization lost contradiction")
    for atom in core:
        trial = [candidate for candidate in core if candidate.key != atom.key]
        if contradiction(route, trial):
            raise AssertionError(f"core atom is redundant: {atom.key}")
    return core


def affine_ledger(route: str) -> dict[str, object]:
    seed = ROUTE_SEED[route]
    S = int(seed["S"])
    return {
        "route": route,
        "C19_seed_S": S,
        "C19_seed_factorization": seed["factorization"],
        "consecutive_companion_block": [
            f"C19={S}*R",
            f"C23={S}*R+1=6B",
            f"C27={S}*R+2=7E",
            f"C31={S}*R+3=10D",
            f"C35={S}*R+4=3F",
            f"C39={S}*R+5=2G",
            f"C43={S}*R+6=H",
            f"C47={S}*R+7=6J",
            f"C51={S}*R+8=5K",
            f"C55={S}*R+9=14L",
        ],
        "odd_support_separation": (
            "odd parts of R,B,E,D,F,G,H,J,K,L are pairwise coprime"
        ),
        "only_support_recycling": [
            "gcd(B,G)=gcd(2,t)",
            "gcd(G,L)=gcd(2,t)",
            "gcd(D,J)=gcd(2,t+1)",
            "gcd(B,L)=gcd(4,t)",
        ],
    }


def obligation_ledger(route: str, propagated: dict[str, object]) -> dict[str, object]:
    domains = propagated.get("domains", {})
    forced = propagated.get("forced", {})
    derived = propagated.get("derived", {})
    trace = propagated.get("theorem_trace", [])
    supports = propagated.get("support_consequences", [])

    return {
        "scope": "realized h169 pair-route simultaneous-survivor grammar",
        "route": route,
        "phase_domains": {
            field: domains.get(field, [])
            for field in ("tau19", "tau31", "tau4", "tau9")
        },
        "mode_domains": {
            field: domains.get(field, [])
            for field in (
                "k19_mode",
                "k27_mode",
                "k31_mode",
                "k35_status",
                "k47_mode",
            )
        },
        "forced_coordinates": forced,
        "derived_valuation_and_seam": derived,
        "required_support_and_character_obligations": supports,
        "affine_and_support_obligations": affine_ledger(route),
        "theorem_rules_that_contracted_this_query": trace,
        "interpretation": (
            "Every surviving formal tuple must satisfy all listed obligations "
            "simultaneously.  The ledger does not assert that any formal tuple "
            "has an arithmetic realization."
        ),
    }


def analyze(
    route: str,
    constraints: dict[str, frozenset[object]],
) -> dict[str, object]:
    route = route.upper()
    if route not in {"A", "B"}:
        raise ValueError("route must be A or B")

    propagated = dep.propagate(route, constraints)
    atoms = assumption_atoms(constraints) + theorem_atoms()

    result: dict[str, object] = {
        "analysis": "h169-obligation-core-v1",
        "route": route,
        "input_constraints": {
            field: sorted(values, key=str)
            for field, values in constraints.items()
        },
        "contradiction": propagated["contradiction"],
        "claim_boundary": (
            "exact explanation layer over the landed realized-h169 dependency "
            "grammar; contradiction cores are formal theorem-grammar cores and "
            "are not universal statements outside that scope"
        ),
    }

    if propagated["contradiction"]:
        core = irreducible_unsat_core(route, atoms)
        result["contradiction_core"] = {
            "minimality": "inclusion-minimal under single-atom deletion",
            "minimum_cardinality_claimed": False,
            "uses_implicit_grammar_base_domains": True,
            "atoms": [atom.public() for atom in core],
            "atom_count": len(core),
            "each_retained_atom_is_necessary": True,
        }
        result["propagator_contradiction_source"] = propagated.get(
            "contradiction_source"
        )
        return result

    result["surviving_formal_tuples"] = propagated["surviving_formal_tuples"]
    result["obligations"] = obligation_ledger(route, propagated)
    return result


def parse_state_json(raw: str | None) -> dict[str, frozenset[object]]:
    if not raw:
        return {}
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("--state-json must decode to a JSON object")
    return dep.parse_constraints(obj)


def self_test() -> None:
    # The canonical two-rule contradiction:
    # Route-B BARE -> tau19=8 -> k27=Q, incompatible with k27=A.
    bad = analyze(
        "B",
        dep.parse_constraints({"k19_mode": "BARE", "k27_mode": "A"}),
    )
    assert bad["contradiction"] is True
    core = bad["contradiction_core"]  # type: ignore[index]
    public = core["atoms"]  # type: ignore[index]
    theorem_names = {
        atom["name"]
        for atom in public
        if atom["kind"] == "theorem"
    }
    assumption_fields = {
        atom["field"]
        for atom in public
        if atom["kind"] == "assumption"
    }
    assert theorem_names == {"k19-bare-phase", "k27-phase8-q-selector"}
    assert assumption_fields == {"k19_mode", "k27_mode"}
    assert core["atom_count"] == 4  # type: ignore[index]

    # A surviving state should expose the same forced chain as the base
    # dependency propagator, but now as an obligation ledger.
    live = analyze("B", dep.parse_constraints({"k19_mode": "BARE"}))
    assert live["contradiction"] is False
    obligations = live["obligations"]  # type: ignore[index]
    assert obligations["forced_coordinates"]["tau19"] == 8  # type: ignore[index]
    assert obligations["forced_coordinates"]["k27_mode"] == "Q"  # type: ignore[index]
    support = obligations["required_support_and_character_obligations"]  # type: ignore[index]
    assert "k27 Q: every prime factor of E is QR mod27" in support

    # A parity contradiction is also reducible to a small theorem core.
    odd_thin = analyze(
        "B",
        dep.parse_constraints({"tau4": 1, "k47_mode": "THIN"}),
    )
    assert odd_thin["contradiction"] is True
    odd_core = odd_thin["contradiction_core"]["atoms"]  # type: ignore[index]
    assert any(
        atom.get("name") in {
            "route-b-k47-thin-even",
            "route-b-odd-full-full",
        }
        for atom in odd_core
        if atom["kind"] == "theorem"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit theorem-backed obligations or an inclusion-minimal contradiction "
            "core for the realized h169 dependency grammar."
        )
    )
    parser.add_argument("--route", choices=("A", "B"))
    parser.add_argument(
        "--state-json",
        help="partial proof state as JSON; values may be scalars or allowed-value lists",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print(json.dumps({"verified": True, "analysis": "h169-obligation-core-v1"}))
        return 0

    if not args.route:
        parser.error("--route is required unless --self-test is used")

    result = analyze(args.route, parse_state_json(args.state_json))
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
