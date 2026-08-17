#!/usr/bin/env python3
"""Verify exact support isolation of the k51 residual on h169, t mod11=0.

The canonical k51 Jacobi normal form writes

    p = 169 + 840 t,
    t = 11 u,
    C51 = 55 R,
    R = 1 + 42 u.

For every other Lane-I companion C_k=(p+k)/4 through k=55 we write

    C_k = a_k + 2310 u,
    a_k = (169+k)/4.

Any common divisor of R and C_k divides

    2310 R - 42 C_k = 2310 - 42 a_k.

Since R is always odd and R == 1 mod3 and mod7, the determinant table kills
all possible common factors except:

  * rational prime 11 at k=7;
  * rational prime 5 at k=11 and k=31.

Moreover these exceptions are exact:

    gcd(R,C7)=11 iff u=6 mod11, otherwise1;
    gcd(R,C11)=gcd(R,C31)=5 iff u=2 mod5, otherwise1.

Thus every prime q>11 in the k51 residual R is absent from every other
companion C_k with k=3,7,...,55, k!=51. In fact every q>5 is absent except
that q=11 may overlap C7. This is a simultaneous support-isolation theorem,
not a termination theorem.
"""

from __future__ import annotations

import json
import math
from typing import Any

import verify_h169_k11_t0_k51_jacobi_normal_form as k51

SHIFTS = tuple(range(3, 56, 4))
OTHER_SHIFTS = tuple(k for k in SHIFTS if k != 51)
EXPECTED_EXCEPTION_SUPPORT = {
    7: {11},
    11: {5},
    31: {5},
}
EXPECTED_CANONICAL_C51_IDENTITY = "if t=11u then C51=55(1+42u)"


def factorint(n: int) -> dict[int, int]:
    n = abs(n)
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def companion_constant(k: int) -> int:
    if k not in SHIFTS:
        raise ValueError(f"unsupported Lane-I shift: {k}")
    return (169 + k) // 4


def determinant(k: int) -> int:
    a = companion_constant(k)
    return 2310 - 42 * a


def possible_common_primes(k: int) -> set[int]:
    d = determinant(k)
    primes = set(factorint(d))
    # R=1+42u is odd, 1 mod3, and 1 mod7 for every integer u.
    primes -= {2, 3, 7}
    return primes


def exact_gcd(u: int, k: int) -> int:
    R = 1 + 42 * u
    C = companion_constant(k) + 2310 * u
    return math.gcd(R, C)


def verify_symbolic_table() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    observed_exceptions: dict[int, set[int]] = {}

    for k in OTHER_SHIFTS:
        a = companion_constant(k)
        d = determinant(k)
        possible = possible_common_primes(k)
        if possible:
            observed_exceptions[k] = possible
        rows.append(
            {
                "k": k,
                "Ck": f"{a}+2310u",
                "determinant_2310R_minus_42Ck": d,
                "determinant_factorization": factorint(d),
                "possible_common_primes_after_R_mod_2_3_7": sorted(possible),
            }
        )

    if observed_exceptions != EXPECTED_EXCEPTION_SUPPORT:
        raise SystemExit(
            f"residual support exception table changed: {observed_exceptions}"
        )
    return rows


def verify_exact_exceptions() -> dict[str, Any]:
    # mod11: 42=9, so R=0 iff u=6.
    for u in range(11):
        want = 11 if u == 6 else 1
        got = exact_gcd(u, 7)
        if got != want:
            raise SystemExit(f"k7 exact gcd failed at u={u}: {got} != {want}")

    # mod5: 42=2, so R=0 iff u=2. Both C11 and C31 have a
    # permanent factor5, while the determinant has only one factor5.
    for k in (11, 31):
        for u in range(5):
            want = 5 if u == 2 else 1
            got = exact_gcd(u, k)
            if got != want:
                raise SystemExit(
                    f"k{k} exact gcd failed at u={u}: {got} != {want}"
                )

    # All other shifts are symbolically coprime for every u. A full residue
    # sweep modulo the determinant radical is a regression check; the theorem
    # itself is the Euclidean identity plus R mod2,3,7.
    for k in OTHER_SHIFTS:
        if k in EXPECTED_EXCEPTION_SUPPORT:
            continue
        d = abs(determinant(k))
        modulus = max(1, math.prod(factorint(d).keys()))
        for u in range(modulus):
            got = exact_gcd(u, k)
            if got != 1:
                raise SystemExit(
                    f"unexpected overlap at k={k}, u={u}: gcd={got}"
                )

    return {
        "k7": "gcd(R,C7)=11 iff u mod11=6; otherwise1",
        "k11": "gcd(R,C11)=5 iff u mod5=2; otherwise1",
        "k31": "gcd(R,C31)=5 iff u mod5=2; otherwise1",
    }


def verify_harmless_overlap_characters() -> dict[str, Any]:
    # These facts do not prove simultaneous survival; they only explain why the
    # three exceptional small overlaps do not immediately contradict the known
    # local miss support laws at k7/k11/k31.
    qr7 = {pow(x, 2, 7) for x in range(1, 7)}
    qr11 = {pow(x, 2, 11) for x in range(1, 11)}
    H31 = {1, 5, 25}
    if 11 % 7 not in qr7:
        raise SystemExit("11 ceased to be QR mod7")
    if 5 % 11 not in qr11:
        raise SystemExit("5 ceased to be QR mod11")
    if 5 % 31 not in H31:
        raise SystemExit("5 left the landed k31 BARE subgroup H31")
    return {
        "11_mod_7": 11 % 7,
        "11_is_QR_mod_7": True,
        "5_mod_11": 5,
        "5_is_QR_mod_11": True,
        "5_mod_31": 5,
        "5_in_H31": True,
        "interpretation": (
            "the only permitted residual overlaps are small factors already "
            "compatible with the corresponding landed local miss shields"
        ),
    }


def verify() -> dict[str, Any]:
    canonical = k51.verify()
    phase = canonical["phase"]
    if phase["t_mod_11"] != 0:
        raise SystemExit("canonical k51 t11 phase changed")
    if phase["C51_identity"] != EXPECTED_CANONICAL_C51_IDENTITY:
        raise SystemExit(
            f"canonical k51 residual identity changed: {phase['C51_identity']}"
        )
    if phase["forced_factor_occurrences"] != [5, 11]:
        raise SystemExit("canonical k51 hard-class seed changed")

    table = verify_symbolic_table()
    exceptions = verify_exact_exceptions()
    character_check = verify_harmless_overlap_characters()

    coprime_shifts = [
        row["k"]
        for row in table
        if not row["possible_common_primes_after_R_mod_2_3_7"]
    ]
    if coprime_shifts != [3, 15, 19, 23, 27, 35, 39, 43, 47, 55]:
        raise SystemExit(f"coprime shift list changed: {coprime_shifts}")

    return {
        "verified": True,
        "mode": "h169-k11-t0-k51-residual-support-isolation",
        "canonical_k51_normal_form": canonical["mode"],
        "canonical_C51_identity": phase["C51_identity"],
        "parameterization": {
            "t": "11u",
            "R": "1+42u",
            "C51": "55R",
            "R_mod_2": 1,
            "R_mod_3": 1,
            "R_mod_7": 1,
        },
        "companion_window": list(SHIFTS),
        "symbolic_table": table,
        "exact_exception_gcds": exceptions,
        "always_coprime_to_R": coprime_shifts,
        "only_possible_shared_prime_support": {
            "C7": [11],
            "C11": [5],
            "C31": [5],
        },
        "character_compatibility_of_exceptions": character_check,
        "strong_support_consequence": (
            "Every prime q>11 dividing the k51 residual R is absent from every "
            "other Lane-I companion C_k for k=3,7,...,55, k!=51. More sharply, "
            "the only shared residual prime support anywhere in that window is "
            "11 with C7 and 5 with C11/C31, under their stated exact u phases."
        ),
        "theorem": (
            "On the h169 inherited-k11 child t=0 mod11, with t=11u and C51=55R, "
            "the residual R is coprime to C3,C15,C19,C23,C27,C35,C39,C43,C47,C55; "
            "gcd(R,C7) is 11 exactly when u=6 mod11; and gcd(R,C11)=gcd(R,C31) "
            "is 5 exactly when u=2 mod5. No other prime support can be shared "
            "between R and the Lane-I companion window through k55."
        ),
        "claim_boundary": (
            "Exact Euclidean support-isolation theorem. It does not force an "
            "outside-H51 factor into R and therefore does not kill the persistent "
            "k51 Jacobi shield by itself. It proves that any large-prime H51 escape "
            "support in R is private to C51 within the early companion window."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
