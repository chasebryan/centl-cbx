#!/usr/bin/env python3
"""Verify the generic Lane-I prime-relative quadratic-reciprocity bridge.

Let p be an odd prime with p == 1 (mod 4), let k > 0 satisfy k == 3
(mod 4), and set C_k=(p+k)/4. For every odd prime q|C_k with gcd(q,k)=1,

    (q/p) = (q/k),

where the left symbol is Legendre and the right symbol is Jacobi.

Proof:

    p == -k (mod q)
    (q/p) = (p/q)                  because p == 1 (mod 4)
            = (-k/q)
            = (-1/q)(k/q)
            = (-1/q)^2 (q/k)       because k == 3 (mod 4)
            = (q/k).

The final reciprocity step is the Jacobi version of quadratic reciprocity.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from typing import Any


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


def factorint(n: int) -> dict[int, int]:
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


def jacobi(a: int, n: int) -> int:
    if n <= 0 or n % 2 == 0:
        raise ValueError("Jacobi denominator must be positive odd")
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def bridge_value(p: int, k: int, q: int) -> dict[str, int]:
    if not is_prime(p) or p % 4 != 1:
        raise ValueError("p must be prime and 1 mod4")
    if k <= 0 or k % 4 != 3:
        raise ValueError("k must be positive and 3 mod4")
    C = (p + k) // 4
    if 4 * C != p + k:
        raise ValueError("C_k is not integral")
    if not is_prime(q) or q == 2 or C % q:
        raise ValueError("q must be an odd prime divisor of C_k")
    if math.gcd(q, k) != 1:
        raise ValueError("bridge excludes q|k")

    q_over_p = legendre(q, p)
    p_over_q = legendre(p, q)
    minus_k_over_q = legendre(-k, q)
    q_over_k = jacobi(q, k)
    if not (q_over_p == p_over_q == minus_k_over_q == q_over_k):
        raise AssertionError(
            f"bridge failed p={p}, k={k}, q={q}: "
            f"(q/p)={q_over_p}, (p/q)={p_over_q}, "
            f"(-k/q)={minus_k_over_q}, (q/k)={q_over_k}"
        )
    return {
        "q_over_p": q_over_p,
        "p_over_q": p_over_q,
        "minus_k_over_q": minus_k_over_q,
        "q_over_k": q_over_k,
    }


def verify_sign_identity() -> dict[str, Any]:
    rows = []
    for q_mod4 in (1, 3):
        minus_one = 1 if q_mod4 == 1 else -1
        reciprocity_sign = minus_one
        product = minus_one * reciprocity_sign
        if product != 1:
            raise SystemExit(f"sign cancellation failed for q mod4={q_mod4}")
        rows.append(
            {
                "q_mod_4": q_mod4,
                "minus_one_over_q": minus_one,
                "k_q_reciprocity_sign_for_k_mod4_3": reciprocity_sign,
                "product": product,
            }
        )
    return {
        "rows": rows,
        "identity": "(-k/q)=(q/k) for odd gcd(q,k)=1 and k=3 mod4",
    }


def verify_regression() -> dict[str, Any]:
    counts: Counter[str] = Counter()
    examples: list[dict[str, Any]] = []
    specialized: dict[int, Counter[int]] = {
        k: Counter() for k in (3, 7, 11, 19, 23, 31, 43, 51)
    }

    # Complete finite regression over these explicit p/k bounds. This is not
    # the proof; it guards the symbol implementation and composite-k cases.
    for p in range(5, 10_000, 4):
        if not is_prime(p):
            continue
        for k in range(3, 100, 4):
            C = (p + k) // 4
            if 4 * C != p + k:
                raise SystemExit("Lane-I integrality regression failed")
            for q in factorint(C):
                if q == 2 or not is_prime(q):
                    continue
                if math.gcd(q, k) != 1:
                    counts["excluded_q_divides_k"] += 1
                    continue
                values = bridge_value(p, k, q)
                char = values["q_over_p"]
                counts["checked_distinct_prime_divisor_instances"] += 1
                counts["QR" if char == 1 else "NR"] += 1
                if k in specialized:
                    specialized[k][char] += 1
                if len(examples) < 24:
                    examples.append(
                        {
                            "p": p,
                            "k": k,
                            "C_k": C,
                            "q": q,
                            "character": char,
                        }
                    )

    # The exact current finite rectangle contains 26k+ checked instances.  Keep
    # the floor conservative so harmless changes in factor enumeration do not
    # masquerade as a theorem failure.
    if counts["checked_distinct_prime_divisor_instances"] < 20_000:
        raise SystemExit(f"regression unexpectedly small: {counts}")
    if counts["QR"] == 0 or counts["NR"] == 0:
        raise SystemExit("regression failed to exercise both character signs")
    if not specialized[51][1] or not specialized[51][-1]:
        raise SystemExit("composite k=51 regression did not exercise both signs")

    return {
        "counts": dict(sorted(counts.items())),
        "sample_examples": examples,
        "selected_shift_character_counts": {
            str(k): {str(sign): count for sign, count in sorted(rows.items())}
            for k, rows in specialized.items()
        },
    }


def verify_h169_selected_examples() -> dict[str, Any]:
    rows = []
    checked = 0
    for p in range(169, 2_000_000, 840):
        if not is_prime(p):
            continue
        for k in (7, 11, 19, 23, 31, 43, 51):
            C = (p + k) // 4
            for q in factorint(C):
                if q == 2 or math.gcd(q, k) != 1:
                    continue
                values = bridge_value(p, k, q)
                checked += 1
                if len(rows) < 28:
                    rows.append(
                        {
                            "p": p,
                            "p_mod_840": p % 840,
                            "k": k,
                            "C_k": C,
                            "q": q,
                            "q_over_p": values["q_over_p"],
                            "q_over_k": values["q_over_k"],
                        }
                    )
        if checked >= 4_000:
            break
    if checked < 4_000:
        raise SystemExit(f"h169 regression unexpectedly small: {checked}")
    return {"checked_instances": checked, "samples": rows}


def verify() -> dict[str, Any]:
    sign = verify_sign_identity()
    regression = verify_regression()
    h169 = verify_h169_selected_examples()
    return {
        "verified": True,
        "mode": "lane-i-prime-relative-reciprocity",
        "domain": {
            "p": "odd prime, p=1 mod4",
            "k": "positive odd integer, k=3 mod4",
            "C_k": "(p+k)/4",
            "q": "odd prime divisor of C_k with gcd(q,k)=1",
        },
        "identity": "Legendre(q/p)=Jacobi(q/k)",
        "proof_chain": [
            "q|C_k -> p=-k mod q",
            "p=1 mod4 -> (q/p)=(p/q)",
            "p=-k modq -> (p/q)=(-k/q)",
            "k=3 mod4 -> (-k/q)=(q/k)",
        ],
        "sign_cancellation": sign,
        "finite_regression": regression,
        "h169_regression": h169,
        "corollary": (
            "Any Lane-I local support law stated as Jacobi(q/k)=+1 for every "
            "prime q|C_k is equivalently a global law saying every such q is a "
            "quadratic residue modulo the original prime p."
        ),
        "theorem": (
            "Let p be prime with p=1 mod4, k>0 with k=3 mod4, and "
            "C_k=(p+k)/4. For every odd prime q|C_k with q not dividing k, "
            "Legendre(q/p)=Jacobi(q/k)."
        ),
        "claim_boundary": (
            "Exact quadratic-character identity. It does not assert that any "
            "particular Lane-I stage is a miss, does not cover q|k, and does not "
            "by itself force a QR or NR divisor or prove Erdős-Straus."
        ),
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
