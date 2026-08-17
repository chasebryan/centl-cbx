#!/usr/bin/env python3
"""Cross-coordinate obligation and contradiction-core analyzer for h169.

The landed h169 dependency grammar is fixed background proof data. This layer
tensors it with the exact k11 ancestry phase

    t11 = t mod11 in {0,2,3,4,8}

and then carries theorem-backed downstream obligations.

Two Boolean cross-coordinate theorem atoms are currently needed for exact
contradiction extraction:

  1. factor11_in_R iff t11 == 8 on either realized h169 pair route;
  2. factor11_in_R is incompatible with k19 BARE.

Other phase children carry richer exact resource certificates rather than
Boolean pruning atoms. In particular:

  * t11=2 imports the canonical k43 seeded-shell theorem;
  * t11=0 imports the canonical k51 Jacobi normal form, its persistent
    factor11 shield cycle, and exact residual support-isolation theorem.

For a contradictory partial state, the analyzer deletion-minimizes supplied
assumptions plus the cross theorem atoms. Minimality is relative to the fixed
landed base grammar.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Iterable

import propagate_h169_dependency_state as dep
import verify_h169_k11_t0_k51_jacobi_normal_form as k51normal
import verify_h169_k11_t0_k51_persistent_shield_cycle as k51cycle
import verify_h169_k11_t0_k51_residual_support_isolation as k51isolation
import verify_h169_k11_t2_k43_seeded_shell as k43shell
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
    # The realized route seeds 391 and1081 are coprime to11, hence 11|R.
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
    obj = k43shell.verify()
    phase = obj["phase"]
    generic = obj["q43_generic"]
    seeded = obj["q43_seed11"]
    shell = obj["seed_shell"]
    absorbers = obj["one_occurrence_absorbers"]
    contraction = obj["contraction"]

    if phase["t_mod_11"] != 2 or phase["T_mod_11"] != 1:
        raise AssertionError("canonical k43 phase bridge changed")
    if phase["forced_factor"] != 11:
        raise AssertionError("canonical k43 forced factor changed")
    if seeded["type_II_miss_states"] != 2317:
        raise AssertionError("canonical seed11 q43 closure changed")
    if seeded["max_NR_valuation"] != 14:
        raise AssertionError("canonical seed11 q43 NR budget changed")
    if shell["h169_new_excluded_t_mod_43"] != 9:
        raise AssertionError("canonical k43 t-phase exclusion changed")

    return {
        "source_theorem": obj["mode"],
        "literal_prime": 11,
        "destination_shift": 43,
        "phase": "t mod11=2",
        "forced_consequence": "11|C43",
        "forced_signed_support": shell["forced_signed_support"],
        "generic_TypeII_miss_states": generic["type_II_miss_states"],
        "seed11_TypeII_miss_states": seeded["type_II_miss_states"],
        "generic_combined_miss_states": generic["combined_miss_states"],
        "seed11_combined_miss_states": seeded["combined_miss_states"],
        "seed11_TypeI_only_states": seeded["type_I_only_states"],
        "generic_max_Omega_NR": generic["max_NR_valuation"],
        "seed11_max_Omega_NR": seeded["max_NR_valuation"],
        "positive_NR_edges_inside_seeded_SCCs": seeded[
            "positive_NR_edges_inside_SCCs"
        ],
        "additional_factor_residues_forcing_TypeII": absorbers[
            "additional_factor_residues_forcing_Type_II"
        ],
        "combined_miss_excluded_t_mod_43": shell[
            "h169_new_excluded_t_mod_43"
        ],
        "TypeII_miss_states_removed": contraction["Type_II_miss_states_removed"],
        "combined_miss_states_removed": contraction["combined_miss_states_removed"],
        "NR_valuation_budget_drop": contraction["NR_valuation_budget_drop"],
        "interpretation": (
            "exact canonical k43 seeded shell: early phase -> forced factor -> "
            "support absorbers + CRT phase deletion + valuation contraction"
        ),
    }


@lru_cache(maxsize=1)
def k51_normal_form_resource() -> dict[str, object]:
    obj = k51normal.verify()
    cycle = k51cycle.verify_cycle()
    isolation = k51isolation.verify()
    phase = obj["phase"]
    seed = obj["seed_geometry"]
    full = obj["full_seeded_Type_II_miss_closure"]
    sufficiency = obj["H51_sufficiency"]
    necessity = obj["outside_H51_necessity"]
    t17 = obj["t17_phase_consequence"]

    if phase["t_mod_11"] != 0 or phase["T_mod_11"] != 8:
        raise AssertionError("canonical k51 phase bridge changed")
    if phase["forced_factor_occurrences"] != [5, 11]:
        raise AssertionError("canonical k51 hard-class seed changed")
    if full["type_II_miss_states"] != 86 or full["combined_miss_states"] != 26:
        raise AssertionError("canonical seed55 k51 closure changed")
    if necessity["combined_miss_with_outside_H51_factor"] != 0:
        raise AssertionError("canonical k51 necessity theorem changed")
    if cycle["local_v11_ceiling"] is not None:
        raise AssertionError("persistent k51 local v11 ceiling unexpectedly became finite")
    if isolation["canonical_k51_normal_form"] != obj["mode"]:
        raise AssertionError("k51 support-isolation theorem lost canonical parent")
    if isolation["always_coprime_to_R"] != [3, 15, 19, 23, 27, 35, 39, 43, 47, 55]:
        raise AssertionError("k51 residual unconditional coprime window changed")

    return {
        "source_theorem": obj["mode"],
        "persistence_theorem": cycle["mode"],
        "support_isolation_theorem": isolation["mode"],
        "destination_shift": 51,
        "phase": "t mod11=0",
        "C51_identity": phase["C51_identity"],
        "forced_factor_occurrences": phase["forced_factor_occurrences"],
        "residual_name": phase["residual_name"],
        "H51": seed["H51"],
        "H51_order": seed["H51_size"],
        "seed55_center": seed["seed55_center"],
        "seed55_support": seed["seed55_support"],
        "seed55_TypeII_miss_states": full["type_II_miss_states"],
        "seed55_combined_miss_states": full["combined_miss_states"],
        "seed55_TypeI_only_states": full["type_I_only_states"],
        "H51_only_states": sufficiency["H51_only_states"],
        "H51_only_all_combined_miss": sufficiency[
            "all_H51_only_states_are_combined_misses"
        ],
        "combined_miss_with_outside_H51_factor": necessity[
            "combined_miss_with_outside_H51_factor"
        ],
        "word_level_consequence": necessity["word_level_consequence"],
        "combined_miss_allowed_t_mod_17": t17[
            "combined_miss_allowed_t_mod_17"
        ],
        "prime_admissible_phase_fraction_retained": t17[
            "prime_admissible_phase_fraction_retained"
        ],
        "additional_factor11_occurrences_to_saturate_H51": cycle[
            "additional_factor11_occurrences_to_saturate_H51"
        ],
        "total_v11_at_H51_saturation": cycle["total_v11_at_H51_saturation"],
        "persistent_cycle_length": cycle["exact_state_period_after_saturation"],
        "local_v11_ceiling": cycle["local_v11_ceiling"],
        "residual_always_coprime_companions_through_k55": isolation[
            "always_coprime_to_R"
        ],
        "residual_only_possible_shared_prime_support": isolation[
            "only_possible_shared_prime_support"
        ],
        "residual_exact_exception_gcds": isolation["exact_exception_gcds"],
        "residual_strong_support_consequence": isolation[
            "strong_support_consequence"
        ],
        "interpretation": (
            "exact k51 normal form plus explicit vertical escape carrier and "
            "support isolation: a combined miss is exactly residual H51 support; "
            "repeated factor11 reaches a period-16 H51 cycle; and every residual "
            "prime other than 5 or11 is private to C51 through k55.  Global "
            "ancestry must puncture the shield through character/phase coupling."
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
                {"field": field, "allowed": sorted(allowed, key=str)},
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
            raise AssertionError("seed11 q19 NR valuation budget changed")
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
            "forced signed support {1,4,11}",
            "Type-II miss excludes added residues {32,39,42} mod43",
            "combined miss excludes t mod43=9",
            "Type-II miss Omega_NR(C43)<=14",
        ]

    if forced.get("t_mod_11") == 0:
        out["k51_jacobi_obligation"] = k51_normal_form_resource()
        out["phase0_chain"] = [
            "t mod11=0",
            "write t=11u",
            "C51=55(1+42u)=55R",
            "forced seed [5,11]",
            "k51 combined miss iff every residual prime occurrence lies in H51",
            "H51=ker Jacobi(./51)=<11>",
            "combined miss -> t mod17 in {0,2,8,10,11,12,15,16}",
            "four further factor11 copies saturate H51 (total v11=5)",
            "saturated exact state cycles with period16",
            "local v11 has no finite ceiling",
            "R is coprime to C3,C15,C19,C23,C27,C35,C39,C43,C47,C55",
            "only residual overlap channels through k55 are 11 with C7 and 5 with C11/C31",
            "every residual prime q not in {5,11} is private to C51 through k55",
            "global simultaneous character/phase obligations must puncture H51",
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
        "analysis": "h169-cross-obligation-core-v5",
        "route": route,
        "input_constraints": {
            field: sorted(values, key=str)
            for field, values in constraints.items()
        },
        "base_surviving_formal_tuples": len(base_survivors(route)),
        "cross_surviving_formal_tuples": len(states),
        "contradiction": not states,
        "claim_boundary": (
            "Cross-coordinate explanation over the realized h169 pair-route grammar "
            "with inherited k11 miss. The landed base grammar is fixed background "
            "proof data; core minimality is relative to it. Imported local normal "
            "forms, support-isolation laws, resource bounds, and persistence cycles "
            "do not assert arithmetic realization by prime corridor candidates."
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
    obligations = live["obligations"]  # type: ignore[index]
    assert obligations["forced"]["t_mod_11"] == 8  # type: ignore[index]
    assert obligations["forced"]["factor11_in_R"] is True  # type: ignore[index]
    assert obligations["forced"]["k19_mode"] == "FULL_QR"  # type: ignore[index]
    assert obligations["factor11_obligation"]["k19_TypeII_miss_max_Omega_NR"] == 2  # type: ignore[index]

    k43 = analyze("A", parse_constraints({"t_mod_11": 2}))
    assert k43["contradiction"] is False
    obligations = k43["obligations"]  # type: ignore[index]
    resource = obligations["k43_seed_obligation"]  # type: ignore[index]
    assert resource["source_theorem"] == "h169-k11-t2-k43-seeded-shell"  # type: ignore[index]
    assert resource["seed11_TypeII_miss_states"] == 2317  # type: ignore[index]
    assert resource["seed11_combined_miss_states"] == 1217  # type: ignore[index]
    assert resource["seed11_max_Omega_NR"] == 14  # type: ignore[index]
    assert resource["additional_factor_residues_forcing_TypeII"] == [32, 39, 42]  # type: ignore[index]
    assert resource["combined_miss_excluded_t_mod_43"] == 9  # type: ignore[index]

    k51 = analyze("B", parse_constraints({"t_mod_11": 0}))
    assert k51["contradiction"] is False
    obligations = k51["obligations"]  # type: ignore[index]
    resource = obligations["k51_jacobi_obligation"]  # type: ignore[index]
    assert resource["source_theorem"] == "h169-k11-t0-k51-jacobi-normal-form"  # type: ignore[index]
    assert resource["persistence_theorem"] == "h169-k11-t0-k51-persistent-shield-cycle"  # type: ignore[index]
    assert resource["support_isolation_theorem"] == "h169-k11-t0-k51-residual-support-isolation"  # type: ignore[index]
    assert resource["forced_factor_occurrences"] == [5, 11]  # type: ignore[index]
    assert resource["seed55_TypeII_miss_states"] == 86  # type: ignore[index]
    assert resource["seed55_combined_miss_states"] == 26  # type: ignore[index]
    assert resource["combined_miss_with_outside_H51_factor"] == 0  # type: ignore[index]
    assert resource["combined_miss_allowed_t_mod_17"] == [0, 2, 8, 10, 11, 12, 15, 16]  # type: ignore[index]
    assert resource["additional_factor11_occurrences_to_saturate_H51"] == 4  # type: ignore[index]
    assert resource["total_v11_at_H51_saturation"] == 5  # type: ignore[index]
    assert resource["persistent_cycle_length"] == 16  # type: ignore[index]
    assert resource["local_v11_ceiling"] is None  # type: ignore[index]
    assert resource["residual_always_coprime_companions_through_k55"] == [3,15,19,23,27,35,39,43,47,55]  # type: ignore[index]
    assert resource["residual_only_possible_shared_prime_support"] == {"C7": [11], "C11": [5], "C31": [5]}  # type: ignore[index]

    other = analyze("B", parse_constraints({"t_mod_11": 4}))
    assert other["contradiction"] is False
    obligations = other["obligations"]  # type: ignore[index]
    assert obligations["forced"]["factor11_in_R"] is False  # type: ignore[index]
    assert "k43_seed_obligation" not in obligations
    assert "k51_jacobi_obligation" not in obligations
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
        print(json.dumps({"verified": True, "analysis": "h169-cross-obligation-core-v5"}))
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
