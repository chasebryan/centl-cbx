#!/usr/bin/env python3
"""Verify a prime-relative reformulation of the h169 k51 Jacobi normal form.

On the selected h169 k11 child t=0 mod11,

    t=11u,
    C51=55R,
    R=1+42u,
    p=220R-51.

The canonical k51 theorem says a combined miss is equivalent to every residual
prime factor q|R lying in

    H51 = ker Jacobi(./51).

For every odd prime q not dividing51, quadratic reciprocity gives

    (-51/q) = (q/3)(q/17) = Jacobi(q/51).

If q|R then p == -51 (mod q), so

    (p/q) = Jacobi(q/51).

Since every h169 prime p is 1 mod4,

    (q/p) = (p/q).

Therefore q lies in H51 iff q is a quadratic residue modulo p.  The forced
factors 5 and11 are also QR modulo p on t11=0.  Hence the selected k51 combined
miss has the exact global reformulation

    k51 combined miss
    iff
    every prime divisor of C51 is QR modulo p.

This is a bridge from the composite local shield to the global prime p.
"""

from __future__ import annotations

import json
from typing import Any

import verify_h169_k11_t0_k51_jacobi_normal_form as k51

REGRESSION_EXAMPLES = (
    (6, 55_609, 253, (11, 23)),
    (10, 92_569, 421, (421,)),
    (20, 184_969, 841, (29,)),
    (34, 314_329, 1429, (1429,)),
    (37, 342_049, 1555, (5, 311)),
)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def legendre(a: int, q: int) -> int:
    if not is_prime(q) or q == 2:
        raise ValueError(f"Legendre denominator must be an odd prime: {q}")
    a %= q
    if a == 0:
        return 0
    x = pow(a, (q - 1) // 2, q)
    if x == 1:
        return 1
    if x == q - 1:
        return -1
    raise RuntimeError(f"Euler criterion failed for a={a}, q={q}")


def jacobi51_prime(q: int) -> int:
    if q in (3, 17):
        return 0
    return legendre(q, 3) * legendre(q, 17)


def verify_reciprocity_character() -> dict[str, Any]:
    checked = 0
    by_h = {True: 0, False: 0}
    H = k51.h51()

    # Regression over many rational primes. The theorem itself is the exact
    # reciprocity identity documented below; this loop freezes implementation.
    for q in range(5, 20_000, 2):
        if q in (17,) or not is_prime(q):
            continue
        lhs = legendre(-51, q)
        rhs = jacobi51_prime(q)
        if lhs != rhs:
            raise SystemExit(
                f"reciprocity character failed at q={q}: (-51/q)={lhs}, J51={rhs}"
            )
        in_h = q % 51 in H
        if (rhs == 1) != in_h:
            raise SystemExit(
                f"H51 character mismatch at q={q}, residue={q % 51}, rhs={rhs}"
            )
        by_h[in_h] += 1
        checked += 1

    return {
        "checked_primes": checked,
        "checked_H51_primes": by_h[True],
        "checked_outside_H51_primes": by_h[False],
        "identity": "(-51/q)=(q/3)(q/17)=Jacobi(q/51)",
        "exact_reason": (
            "(-1/q) and the reciprocity sign in (3/q) cancel; 17 is 1 mod4"
        ),
    }


def verify_fixed_seed_qr() -> dict[str, Any]:
    # On t=11u, p=169+9240u, so p=4 mod5 and p=4 mod11, while p=1 mod4.
    # Quadratic reciprocity therefore makes both fixed factors QR modulo p.
    if 169 % 5 != 4 or 9240 % 5 != 0:
        raise SystemExit("p mod5 phase changed")
    if 169 % 11 != 4 or 9240 % 11 != 0:
        raise SystemExit("p mod11 phase changed")
    if 169 % 4 != 1 or 9240 % 4 != 0:
        raise SystemExit("p mod4 phase changed")
    if legendre(4, 5) != 1 or legendre(4, 11) != 1:
        raise SystemExit("4 lost QR status modulo5 or11")
    return {
        "p_mod_4": 1,
        "p_mod_5": 4,
        "p_mod_11": 4,
        "5_is_QR_mod_p": True,
        "11_is_QR_mod_p": True,
        "reason": (
            "p=1 mod4, so reciprocity has no p-side sign; p=4 is QR modulo5 and11"
        ),
    }


def verify_prime_relative_bridge() -> dict[str, Any]:
    H = k51.h51()
    checked = 0
    for u, p, R, residual_primes in REGRESSION_EXAMPLES:
        if p != 169 + 9240 * u:
            raise SystemExit(f"regression p identity failed at u={u}")
        if R != 1 + 42 * u:
            raise SystemExit(f"regression R identity failed at u={u}")
        if not is_prime(p):
            raise SystemExit(f"regression p is not prime: {p}")
        if p != 220 * R - 51:
            raise SystemExit(f"p=220R-51 failed at p={p}")

        product = 1
        for q in residual_primes:
            product *= q
            if R % q:
                raise SystemExit(f"q={q} does not divide R={R}")
            if q % 51 not in H:
                raise SystemExit(f"regression residual q={q} is outside H51")
            if p % q != (-51) % q:
                raise SystemExit(f"p!=-51 mod q for p={p}, q={q}")
            if legendre(p, q) != 1:
                raise SystemExit(f"p is not QR mod residual q={q}")
            if legendre(q, p) != 1:
                raise SystemExit(f"residual q={q} is not QR mod p={p}")
            checked += 1
        if R % product:
            raise SystemExit(f"listed residual primes do not divide R={R}")

    return {
        "regression_examples": len(REGRESSION_EXAMPLES),
        "residual_prime_checks": checked,
        "bridge": (
            "q|R and q in H51 -> p=-51 mod q -> (p/q)=+1 -> (q/p)=+1"
        ),
    }


def verify() -> dict[str, Any]:
    canonical = k51.verify()
    phase = canonical["phase"]
    necessity = canonical["outside_H51_necessity"]
    H = canonical["seed_geometry"]["H51"]

    if phase["t_mod_11"] != 0:
        raise SystemExit("canonical k51 selected phase changed")
    if phase["residual_name"] != "R=C51/55=1+42u":
        raise SystemExit("canonical k51 residual coordinate changed")
    if necessity["combined_miss_with_outside_H51_factor"] != 0:
        raise SystemExit("canonical H51 necessity theorem changed")

    reciprocity = verify_reciprocity_character()
    fixed = verify_fixed_seed_qr()
    bridge = verify_prime_relative_bridge()

    return {
        "verified": True,
        "mode": "h169-k11-t0-k51-reciprocal-shield",
        "canonical_parent": canonical["mode"],
        "parameterization": {
            "t": "11u",
            "R": "1+42u",
            "C51": "55R",
            "p": "220R-51",
        },
        "H51": H,
        "reciprocity_character": reciprocity,
        "fixed_seed_character": fixed,
        "prime_relative_bridge": bridge,
        "residual_equivalence": (
            "for every residual prime q|R: q in H51 iff (p/q)=+1 iff (q/p)=+1"
        ),
        "global_normal_form": (
            "k51 combined miss iff every prime divisor of C51 is a quadratic residue modulo p"
        ),
        "theorem": (
            "For an h169 prime p on the inherited k11 phase t=0 mod11, write "
            "C51=55R and p=220R-51.  The canonical k51 combined-miss condition "
            "is equivalent to every residual q|R satisfying (q/p)=+1.  Since the "
            "forced factors5 and11 are also QR modulo p, k51 is a combined miss "
            "if and only if every prime divisor of C51 is QR modulo p."
        ),
        "claim_boundary": (
            "Exact quadratic-reciprocity reformulation of the landed k51 Jacobi "
            "normal form.  It does not by itself force an NR prime divisor of C51 "
            "and therefore does not eliminate the selected phase or prove ES."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
