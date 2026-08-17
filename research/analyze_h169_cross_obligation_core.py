#!/usr/bin/env python3
"""Cross-coordinate obligation and contradiction-core analyzer for h169.

This is the next layer above ``propagate_h169_dependency_state.py``. The base
h169 dependency grammar is treated as a landed exact background relation. We
then tensor it with the k11 ancestry coordinate

    t11 = t mod11 in {0,2,3,4,8}

and one explicit derived obligation

    factor11_in_R.

Two exact cross-coordinate theorem atoms are compiled:

  1. factor11_in_R iff t11 == 8 on either realized h169 pair route;
  2. factor11_in_R is incompatible with k19 BARE, because BARE requires every
     prime divisor of R to be 1 mod19 while 11 mod19 is 11.

The other inherited k11 phases may carry theorem-verified local resource
certificates without becoming new Boolean grammar dimensions. In particular,
t11 == 2 forces literal factor11 at k43 and contracts the exact q43 miss
closure, while t11 == 0 forces literal factor11 at k51 and enters an exact
composite Jacobi shield.

For a contradictory partial state, the tool deletion-minimizes the supplied
assumptions plus the two cross theorem atoms. Minimality is relative to the
landed base grammar, which remains fixed background proof data.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Iterable

import propagate_h169_dependency_state as dep
import verify_h169_k11_phase_k43_seed as k43seed
import verify_h169_k11_phase_k51_composite_shield as k51shield
import verify_k19_nr_valuation_budget as nrbudget

T11_DOMAIN = (0, 2, 3, 4, 8)
CROSS_FIELDS = dep.FIELDS + ("t_mod_11", "factor11_in_R")


@dataclass(frozen=True)
class CrossState:
    base: dep.State
    t_mod_11: int
    factor11_in_R: bool

    def value(self, field: str) -> object:
        if field == "t_mod_11":
            return self.t_mod_11
        if field == "factor11_in_R":
            return self.factor11_in_R
        return getattr(self.base, field)


@dataclass(frozen=True)
class Atom:
    kind: str
    key: str
    predicate: Callable[[str, CrossState], bool]
    public_data: dict[str, object]

    def public(self) -> dict[str, object]:
        return {"kind": self.kind, **self.public_data}


def rule_phase_factor11(_route: str, s: CrossState) -> bool:
    # On h169, T=8+35t. Thus t=8 mod11 iff T=2 mod11 iff 11|C19.
    # The realized route seeds 391 and1081 are coprime to 11, hence 11|R.
    return s.factor11_in_R == (s.t_mod_11 == 8)


def rule_bare_excludes_11(_route: str, s: CrossState) -> bool:
    return not (s.factor11_in_R and s.base.k19_mode == "BARE")


CROSS_THEOREMS = (
    Atom(
        "theorem",
        "theorem:h169-k11-phase-factor11-in-R",
        rule_phase_factor11,
        {
            "name": "h169-k11-phase-factor11-in-R",
            "statement": (
                "On either realized h169 pair route under inherited k11 miss, "
                "factor11_in_R iff t mod11=8 (equiv. T mod11=2)."
            ),
        },
    ),
    Atom(
        "theorem",
        "theorem:k19-bare-excludes-factor11-in-R",
        rule_bare_excludes_11,
        {
            "name": "k19-bare-excludes-factor11-in-R",
            "statement": (
                "k19 BARE requires every q|R to be 1 mod19; literal q=11 is not, "
                "so factor11_in_R excludes BARE."
            ),
        },
    ),
)


@lru_cache(maxsize=2)
def base_survivors(route: str) -> tuple[dep.State, ...]:
    route = route.upper()
    return tuple(
        state
        for state in dep.naive_states(route)
        if all(rule.predicate(route, state) for rule in dep.RULES)
    )


@lru_cache(maxsize=1)
def k43_seed_resource() -> dict[str, object]:
    obj = k43seed.verify()
    phase = obj["phase"]
    generic = obj["generic_q43"]
    seeded = obj["seed11_q43"]
    contraction = obj["exact_contraction"]
    if phase["t_mod_11"] != 2 or phase["forced_shift"] != 43:
        raise AssertionError("k43 seed theorem phase changed")
    if phase["consequence"] != "11|C43":
        raise AssertionError("k43 seed theorem lost factor11 consequence")
    if seeded["TypeII_miss_states"] != 2317:
        raise AssertionError("seed11 q43 closure changed")
    if seeded["NR_budget"]["max_NR_valuation"] != 14:
        raise AssertionError("seed11 q43 NR budget changed")
    return {
        "literal_prime": 11,
        "destination_shift": 43,
        "phase": "t mod11=2",
        "forced_consequence": "11|C43",
        "generic_TypeII_miss_states": generic["TypeII_miss_states"],
        "seed11_TypeII_miss_states": seeded["TypeII_miss_states"],
        "seed11_combined_miss_states": seeded["combined_miss_states"],
        "seed11_TypeI_only_states": seeded["TypeI_only_states"],
        "generic_max_Omega_NR": generic["NR_budget"]["max_NR_valuation"],
        "seed11_max_Omega_NR": seeded["NR_budget"]["max_NR_valuation"],
        "positive_NR_edges_inside_seeded_SCCs": seeded["NR_budget"][
            "positive_NR_edges_inside_SCCs"
        ],
        "state_ratio": contraction["TypeII_miss_state_ratio"],
        "states_removed": contraction["states_removed"],
        "interpretation": (
            "exact local k43 resource contraction inherited from the k11 phase; "
            "this is not yet a branch-deletion theorem"
        ),
    }


@lru_cache(maxsize=1)
def k51_shield_resource() -> dict[str, object]:
    obj = k51shield.verify()
    phase = obj["phase"]
    generic = obj["generic_q51"]
    seeded = obj["seed11_q51"]
    contraction = obj["exact_contraction"]
    shield = obj["jacobi_shield"]
    cycle = obj["persistent_cycle"]
    if phase["t_mod_11"] != 0 or phase["forced_shift"] != 51:
        raise AssertionError("k51 shield theorem phase changed")
    if phase["consequence"] != "11|C51":
        raise AssertionError("k51 shield theorem lost factor11 consequence")
    if seeded["TypeII_miss_states"] != 636:
        raise AssertionError("seed11 q51 closure changed")
    if shield["H_order"] != 16 or shield["H_index"] != 2:
        raise AssertionError("k51 Jacobi shield changed")
    if cycle["local_factor11_multiplicity_ceiling"] is not None:
        raise AssertionError("k51 local factor11 ceiling unexpectedly became finite")
    return {
        "literal_prime": 11,
        "destination_shift": 51,
        "phase": "t mod11=0",
        "forced_consequence": "11|C51",
        "generic_TypeII_miss_states": generic["TypeII_miss_states"],
        "seed11_TypeII_miss_states": seeded["TypeII_miss_states"],
        "seed11_combined_miss_states": seeded["combined_miss_states"],
        "seed11_TypeI_only_states": seeded["TypeI_only_states"],
        "state_ratio": contraction["TypeII_miss_state_ratio"],
        "states_removed": contraction["states_removed"],
        "shield_group": shield["H"],
        "shield_order": shield["H_order"],
        "shield_index": shield["H_index"],
        "shield_characterization": shield["H_characterization"],
        "shield_generator_order": shield["generator_order"],
        "TypeII_target_outside_shield": shield["jacobi_TypeII_target"] == -1,
        "TypeI_base_outside_shield": shield["jacobi_TypeI_base"] == -1,
        "support_saturation_exponent": cycle["saturation_exponent"],
        "persistent_cycle_length": cycle["cycle_length"],
        "local_factor11_multiplicity_ceiling": cycle[
            "local_factor11_multiplicity_ceiling"
        ],
        "interpretation": (
            "exact local k51 state contraction plus a persistent index-two Jacobi "
            "combined-miss shield; simultaneous cofactor obligations must puncture "
            "the shield because local k51 geometry cannot"
        ),
    }


def cross_states(route: str) -> Iterable[CrossState]:
    for base in base_survivors(route):
        for t11 in T11_DOMAIN:
            for factor11 in (False, True):
                yield CrossState(base, t11, factor11)


def normalize_value(value: object) -> frozenset[object]:
    if isinstance(value, list):
        return frozenset(value)
    return frozenset({value})


def parse_constraints(raw: dict[str, object]) -> dict[str, frozenset[object]]:
    unknown = set(raw) - set(CROSS_FIELDS)
    if unknown:
        raise ValueError(f"unknown cross-state fields: {sorted(unknown)}")
    out = {field: normalize_value(value) for field, value in raw.items()}
    if "t_mod_11" in out and not out["t_mod_11"] <= set(T11_DOMAIN):
        raise ValueError(
            f"t_mod_11 is an inherited h169 k11-miss phase and must lie in {T11_DOMAIN}"
        )
    return out


def assumption_atoms(
    constraints: dict[str, frozenset[object]],
) -> list[Atom]:
    atoms = []
    for field, allowed in constraints.items():
        atoms.append(
            Atom(
                "assumption",
                f"assumption:{field}",
                lambda _route, s, f=field, a=allowed: s.value(f) in a,
                {
                    "field": field,
                    "allowed": sorted(allowed, key=str),
                },
            )
        )
    return atoms


def satisfies(route: str, state: CrossState, atoms: Iterable[Atom]) -> bool:
    return all(atom.predicate(route, state) for atom in atoms)


def has_state(route: str, atoms: Iterable[Atom]) -> bool:
    frozen = tuple(atoms)
    return any(satisfies(route, state, frozen) for state in cross_states(route))


def is_contradiction(route: str, atoms: Iterable[Atom]) -> bool:
    return not has_state(route, atoms)


def irreducible_core(route: str, atoms: list[Atom]) -> list[Atom]:
    if not is_contradiction(route, atoms):
        raise ValueError("cannot extract a contradiction core from a satisfiable state")

    core = list(atoms)
    changed = True
    while changed:
        changed = False
        for atom in tuple(core):
            trial = [x for x in core if x.key != atom.key]
            if is_contradiction(route, trial):
                core = trial
                changed = True

    if not is_contradiction(route, core):
        raise AssertionError("core minimization lost contradiction")
    for atom in core:
        trial = [x for x in core if x.key != atom.key]
        if is_contradiction(route, trial):
            raise AssertionError(f"retained atom is redundant: {atom.key}")
    return core


def projected_domains(states: list[CrossState]) -> dict[str, list[object]]:
    return {
        field: sorted({state.value(field) for state in states}, key=str)
        for field in CROSS_FIELDS
    }


def live_obligations(route: str, states: list[CrossState]) -> dict[str, object]:
    domains = projected_domains(states)
    forced = {
        field: values[0]
        for field, values in domains.items()
        if len(values) == 1
    }
    out: dict[str, object] = {
        "domains": domains,
        "forced": forced,
        "base_grammar": "landed h169 dependency relation v1",
        "cross_theorems": [atom.public() for atom in CROSS_THEOREMS],
    }

    if forced.get("factor11_in_R") is True:
        budget = nrbudget.weighted_budget((11,))
        if budget["max_NR_valuation"] != 2:
            raise AssertionError("seed11 NR valuation budget changed")
        out["factor11_obligation"] = {
            "literal_prime": 11,
            "reservoir": "R",
            "residue_mod_19": 11,
            "k19_BARE_compatible": False,
            "k19_TypeII_miss_max_Omega_NR": 2,
            "positive_NR_edges_inside_seeded_SCCs": budget[
                "positive_NR_edges_inside_SCCs"
            ],
        }

    if forced.get("t_mod_11") == 8:
        if forced.get("k19_mode") != "FULL_QR":
            raise AssertionError("t11=8 did not force k19 FULL_QR")
        out["phase8_chain"] = [
            "t mod11=8",
            "T mod11=2",
            "11|C19",
            "gcd(route seed,11)=1 -> 11|R",
            "BARE support(R) subset 1 mod19",
            "11 mod19 !=1 -> BARE contradiction",
            "k19 miss mode FULL_QR",
            "seed11 Type-II-miss Omega_NR budget <=2",
        ]

    if forced.get("t_mod_11") == 2:
        out["k43_seed_obligation"] = k43_seed_resource()
        out["phase2_chain"] = [
            "t mod11=2",
            "T mod11=1",
            "11|C43",
            "preload literal residue11 in q43 signed box",
            "conditional k43 Type-II miss -> exact seed11 closure size 2317",
            "conditional k43 Type-II miss -> Omega_NR(C43)<=14",
        ]

    if forced.get("t_mod_11") == 0:
        out["k51_composite_shield_obligation"] = k51_shield_resource()
        out["phase0_chain"] = [
            "t mod11=0",
            "T mod11=8",
            "11|C51",
            "preload literal residue11 in exact U(51) signed box",
            "conditional k51 Type-II miss -> exact seed11 closure size 636",
            "H51=<11>=ker Jacobi(./51) is an index-two combined-miss shield",
            "pure factor11 support saturates H51 at exponent8",
            "saturated state cycles with period16",
            "local factor11 multiplicity has no finite ceiling",
            "therefore simultaneous cofactor obligations must puncture H51",
        ]
    return out


def analyze(
    route: str,
    constraints: dict[str, frozenset[object]],
) -> dict[str, object]:
    route = route.upper()
    if route not in {"A", "B"}:
        raise ValueError("route must be A or B")
    if route == "A" and "k47_mode" in constraints and constraints["k47_mode"] != {"NA"}:
        raise ValueError("Route A uses k47_mode=NA")

    assumptions = assumption_atoms(constraints)
    atoms = assumptions + list(CROSS_THEOREMS)
    states = [state for state in cross_states(route) if satisfies(route, state, atoms)]

    result: dict[str, object] = {
        "verified_background": True,
        "analysis": "h169-cross-obligation-core-v3",
        "route": route,
        "input_constraints": {
            field: sorted(values, key=str)
            for field, values in constraints.items()
        },
        "base_surviving_formal_tuples": len(base_survivors(route)),
        "cross_surviving_formal_tuples": len(states),
        "contradiction": not states,
        "claim_boundary": (
            "cross-coordinate explanation over the realized h169 pair-route "
            "grammar with inherited k11 miss. The landed base grammar is fixed "
            "background proof data; core minimality is relative to it. Local "
            "resource certificates and persistent residue cycles do not assert "
            "arithmetic realization by prime corridor candidates."
        ),
    }

    if not states:
        core = irreducible_core(route, atoms)
        result["contradiction_core"] = {
            "minimality": "inclusion-minimal under single-atom deletion",
            "relative_to_fixed_background": "landed h169 dependency grammar v1",
            "minimum_cardinality_claimed": False,
            "atoms": [atom.public() for atom in core],
            "atom_count": len(core),
            "each_retained_atom_is_necessary": True,
        }
    else:
        result["obligations"] = live_obligations(route, states)
    return result


def self_test() -> None:
    a = analyze("A", {})
    b = analyze("B", {})
    assert a["base_surviving_formal_tuples"] == 105_600
    assert b["base_surviving_formal_tuples"] == 147_900
    assert a["cross_surviving_formal_tuples"] == 516_450
    assert b["cross_surviving_formal_tuples"] == 736_950

    bad = analyze("B", parse_constraints({"t_mod_11": 8, "k19_mode": "BARE"}))
    assert bad["contradiction"] is True
    core = bad["contradiction_core"]  # type: ignore[index]
    assert core["atom_count"] == 4  # type: ignore[index]
    public = core["atoms"]  # type: ignore[index]
    assert {
        atom["field"] for atom in public if atom["kind"] == "assumption"
    } == {"t_mod_11", "k19_mode"}
    assert {
        atom["name"] for atom in public if atom["kind"] == "theorem"
    } == {
        "h169-k11-phase-factor11-in-R",
        "k19-bare-excludes-factor11-in-R",
    }

    live = analyze("A", parse_constraints({"t_mod_11": 8}))
    assert live["contradiction"] is False
    obligations = live["obligations"]  # type: ignore[index]
    assert obligations["forced"]["t_mod_11"] == 8  # type: ignore[index]
    assert obligations["forced"]["factor11_in_R"] is True  # type: ignore[index]
    assert obligations["forced"]["k19_mode"] == "FULL_QR"  # type: ignore[index]
    assert obligations["factor11_obligation"]["k19_TypeII_miss_max_Omega_NR"] == 2  # type: ignore[index]

    k43 = analyze("A", parse_constraints({"t_mod_11": 2}))
    assert k43["contradiction"] is False
    obligations = k43["obligations"]  # type: ignore[index]
    resource = obligations["k43_seed_obligation"]  # type: ignore[index]
    assert resource["literal_prime"] == 11  # type: ignore[index]
    assert resource["destination_shift"] == 43  # type: ignore[index]
    assert resource["generic_TypeII_miss_states"] == 18_048  # type: ignore[index]
    assert resource["seed11_TypeII_miss_states"] == 2_317  # type: ignore[index]
    assert resource["generic_max_Omega_NR"] == 20  # type: ignore[index]
    assert resource["seed11_max_Omega_NR"] == 14  # type: ignore[index]
    assert resource["positive_NR_edges_inside_seeded_SCCs"] == 0  # type: ignore[index]

    k51 = analyze("B", parse_constraints({"t_mod_11": 0}))
    assert k51["contradiction"] is False
    obligations = k51["obligations"]  # type: ignore[index]
    resource = obligations["k51_composite_shield_obligation"]  # type: ignore[index]
    assert resource["literal_prime"] == 11  # type: ignore[index]
    assert resource["destination_shift"] == 51  # type: ignore[index]
    assert resource["generic_TypeII_miss_states"] == 3337  # type: ignore[index]
    assert resource["seed11_TypeII_miss_states"] == 636  # type: ignore[index]
    assert resource["shield_order"] == 16  # type: ignore[index]
    assert resource["shield_index"] == 2  # type: ignore[index]
    assert resource["support_saturation_exponent"] == 8  # type: ignore[index]
    assert resource["persistent_cycle_length"] == 16  # type: ignore[index]
    assert resource["local_factor11_multiplicity_ceiling"] is None  # type: ignore[index]

    other = analyze("B", parse_constraints({"t_mod_11": 4}))
    assert other["contradiction"] is False
    obligations = other["obligations"]  # type: ignore[index]
    assert obligations["forced"]["factor11_in_R"] is False  # type: ignore[index]
    assert "k43_seed_obligation" not in obligations
    assert "k51_composite_shield_obligation" not in obligations
    assert set(obligations["domains"]["k19_mode"]) == {"BARE", "FULL_QR"}  # type: ignore[index]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Propagate the h169 k11 t-mod11 ancestry coordinate into the landed "
            "pair-route grammar and emit obligations or an irreducible core."
        )
    )
    parser.add_argument("--route", choices=("A", "B"))
    parser.add_argument(
        "--state-json",
        help=(
            "partial cross state as JSON; accepts base h169 fields plus "
            "t_mod_11 and factor11_in_R"
        ),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print(json.dumps({"verified": True, "analysis": "h169-cross-obligation-core-v3"}))
        return 0
    if not args.route:
        parser.error("--route is required unless --self-test is used")

    raw = json.loads(args.state_json) if args.state_json else {}
    if not isinstance(raw, dict):
        raise SystemExit("--state-json must decode to a JSON object")
    result = analyze(args.route, parse_constraints(raw))
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
