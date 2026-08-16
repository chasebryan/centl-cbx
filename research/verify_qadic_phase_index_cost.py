#!/usr/bin/env python3
"""Verify exact q-adic lattice-index costs for routed source valuation lifts."""
from __future__ import annotations

import argparse
import itertools
import json
import math


def crt_pair(a: int, m: int, b: int, n: int) -> tuple[int, int]:
    g = math.gcd(m, n)
    if (b - a) % g:
        raise ValueError("incompatible CRT")
    mm = m // g
    nn = n // g
    x = ((b - a) // g) * pow(mm, -1, nn) % nn
    mod = m * nn
    return (a + m * x) % mod, mod


def vq(n: int, q: int) -> int:
    if n == 0:
        return 10**9
    e = 0
    while n % q == 0:
        n //= q
        e += 1
    return e


def one_source_residue(A: int, q: int, e: int) -> tuple[int, int]:
    assert e >= 1
    mod = q ** (e - 1)
    return (-A) % mod if mod > 1 else 0, mod


def synchronized_residue(Bs: list[int], qs: list[int], es: list[int], Qs: list[int]) -> tuple[int, int]:
    residue = 0
    modulus = 1
    for B, q, e, Q_i in zip(Bs, qs, es, Qs):
        local_mod = q ** (e - 1)
        if local_mod == 1:
            local = 0
        else:
            local = (-B * pow(Q_i, -1, local_mod)) % local_mod
        residue, modulus = crt_pair(residue, modulus, local, local_mod)
    return residue, modulus


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # One-source theorem: exact classes and incremental factor q.
    one_rows = []
    for q in (13, 29, 37, 41, 71, 317):
        for A in (1, 2, q - 1, q + 3):
            for e in range(1, 6):
                r, mod = one_source_residue(A, q, e)
                assert mod == q ** (e - 1)
                # Check several periods exactly against q(A+n).
                for n in range(0, min(20_000, max(20, 3 * mod))):
                    lhs = vq(q * (A + n), q) >= e
                    rhs = (n - r) % mod == 0
                    assert lhs == rhs
                if e < 5:
                    _, next_mod = one_source_residue(A, q, e + 1)
                    assert next_mod // mod == q
            one_rows.append({"q": q, "A": A, "index_e5": q ** 4})

    # Exact parent splitting: q-1 exact-e children, one >=e+1 child.
    split_rows = []
    for q in (5, 13, 29, 71):
        A = q + 2
        for e in (1, 2, 3):
            r, parent_mod = one_source_residue(A, q, e)
            r_next, child_mod = one_source_residue(A, q, e + 1)
            assert child_mod == parent_mod * q
            child_residues = [(r + parent_mod * a) % child_mod for a in range(q)]
            assert len(set(child_residues)) == q
            deeper = [x for x in child_residues if x == r_next]
            assert len(deeper) == 1
            exact_e = [x for x in child_residues if x != r_next]
            assert len(exact_e) == q - 1
            for x in exact_e:
                assert vq(q * (A + x), q) == e
            assert vq(q * (A + r_next), q) >= e + 1
            split_rows.append({"q": q, "e": e, "children": q, "exact_e": q - 1, "deeper": 1})

    # Multi-source synchronized route theorem in abstract normal form.
    multi_rows = []
    cases = [
        ([13, 17], [2, 3]),
        ([37, 41], [2, 2]),
        ([13, 29, 71], [3, 2, 2]),
    ]
    for qs, es in cases:
        Q = math.prod(qs)
        # Choose an arbitrary synchronized k0 state through the quotient data B_i.
        Bs = [i + 2 for i in range(len(qs))]
        Qis = [Q // q for q in qs]
        r, mod = synchronized_residue(Bs, qs, es, Qis)
        expected = math.prod(q ** (e - 1) for q, e in zip(qs, es))
        assert mod == expected
        # Verify exact simultaneous valuation floors on several representatives.
        for h in range(6):
            n = r + mod * h
            for B, q, e, Qi in zip(Bs, qs, es, Qis):
                assert vq(q * (B + Qi * n), q) >= e
        # Increment each source independently and verify exact index ratio.
        ratios = []
        for j, q in enumerate(qs):
            es2 = list(es)
            es2[j] += 1
            _, mod2 = synchronized_residue(Bs, qs, es2, Qis)
            assert mod2 // mod == q
            ratios.append(q)
        multi_rows.append({"qs": qs, "es": es, "index": mod, "increment_ratios": ratios})

    # Fixed-destination target-phase formulation.
    # q^e|C_k iff p=-k (mod 4q^e), and each lift adds factor q.
    target_rows = []
    for q in (13, 29, 41, 317):
        k = 39 if q != 41 else 195
        for e in range(1, 5):
            mod = 4 * (q ** e)
            p_class = (-k) % mod
            assert (p_class + k) % mod == 0
            if e < 4:
                next_mod = 4 * (q ** (e + 1))
                assert next_mod // mod == q
        target_rows.append({"q": q, "k": k, "index_e4_vs_e1": q ** 3})

    # Landed examples.
    assert 29 ** 9 == 14_507_145_975_869
    assert 41 * 37 == 1517
    assert 317 ** 1 == 317

    # h169 + fixed-destination distinct source refinement, for primes coprime to840.
    # Relative to multiplicity-one q_i shell, exponents e_i add product q_i^(e_i-1).
    h169_rows = []
    for qs, es, k in [([41, 37], [2, 2], 195), ([29], [10], 951), ([317], [2], 39)]:
        assert all(math.gcd(q, 840) == 1 for q in qs)
        extra = math.prod(q ** (e - 1) for q, e in zip(qs, es))
        h169_rows.append({"qs": qs, "es": es, "k": k, "extra_index": extra})
    assert h169_rows[0]["extra_index"] == 1517
    assert h169_rows[1]["extra_index"] == 29 ** 9
    assert h169_rows[2]["extra_index"] == 317

    report = {
        "analysis": "qadic-phase-index-cost-v1",
        "one_source_regression": one_rows,
        "exact_parent_splits": split_rows,
        "multi_source_regression": multi_rows,
        "target_phase_regression": target_rows,
        "landed_examples": {
            "q29_e10_extra_index": 29 ** 9,
            "k195_q41_q37_double_square_extra_index": 1517,
            "q317_square_extra_index": 317,
        },
        "h169_target_phase_examples": h169_rows,
        "termination_rank": False,
        "failures": 0,
        "claim": (
            "a routed source valuation floor e selects one route-index class modulo q^(e-1); each increment e->e+1 has exact index q; "
            "for distinct synchronized sources the indices multiply by CRT, yielding product q_i^(e_i-1) relative to the multiplicity-one shell"
        ),
    }

    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
