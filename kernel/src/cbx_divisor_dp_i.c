/*
 * cbx_divisor_dp_i.c — exact divisor-square residue DP prototype for Lane I.
 *
 * For gcd(C,k)=1, the signed box
 *
 *   B_k(C) = { product q_i^z_i : -e_i <= z_i <= e_i }
 *
 * is exactly
 *
 *   { C * D^-1 mod k : D | C^2 }.
 *
 * Therefore the two Lane-I targets {-1,-p^-1}, with p=4C mod k, are hit iff
 * the divisor residues of C^2 contain either
 *
 *   -C mod k          (Type II)
 *   -4^-1 mod k       (Type I, via inversion symmetry of the signed box).
 *
 * This prototype enumerates distinct divisor residues of C^2 with a sparse
 * residue DP.  The state size is at most k, independent of the formal box
 * size product(2e_i+1).  It remains separate from cbx-brec-i until finite
 * equivalence and benchmark evidence justify a hybrid or replacement path.
 */
#define _POSIX_C_SOURCE 200809L
#define main cbx_core_main
#include "cbx.c"
#undef main

#include <time.h>

typedef struct {
    uint64_t reachable;
    uint64_t generated;
    uint64_t deduplicated;
    uint64_t early_target_hits;
} dp_stats_t;

static uint64_t parse_u64_dp(const char *name, const char *text) {
    errno = 0;
    char *end = NULL;
    unsigned long long v = strtoull(text, &end, 10);
    if (errno || !end || *end) die("invalid %s: %s", name, text);
    return (uint64_t)v;
}

static double now_seconds_dp(void) {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) die("clock_gettime failed");
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static int divisor_dp_delta_zero(const fac_t *f, uint64_t C, uint64_t k,
                                 dp_stats_t *stats) {
    if (stats) memset(stats, 0, sizeof(*stats));
    if (k < 3 || !(k & 1)) return 0;
    if (gcd64(C, k) != 1) return 0;
    if (k > SIZE_MAX / sizeof(uint64_t)) die("DP modulus too large");

    uint64_t inv4 = inv_mod(4 % k, k);
    if (!inv4) return 0;
    uint64_t target_ii = (k - (C % k)) % k;
    uint64_t target_i = (k - inv4) % k;

    size_t cap = (size_t)k;
    uint64_t *cur = malloc(cap * sizeof(*cur));
    uint64_t *next = malloc(cap * sizeof(*next));
    uint32_t *marks = calloc(cap, sizeof(*marks));
    if (!cur || !next || !marks) die("divisor DP allocation failed");

    size_t ncur = 1;
    cur[0] = 1 % k;
    uint32_t generation = 1;
    marks[cur[0]] = generation;

    if (cur[0] == target_ii || cur[0] == target_i) {
        if (stats) {
            stats->reachable = 1;
            stats->early_target_hits = 1;
        }
        free(marks); free(next); free(cur);
        return 1;
    }

    for (int fi = 0; fi < f->n; fi++) {
        uint64_t q = f->ps[fi] % k;
        unsigned max_power = 2u * f->es[fi];

        generation++;
        if (generation == 0) {
            memset(marks, 0, cap * sizeof(*marks));
            generation = 1;
        }

        size_t nnext = 0;
        for (size_t ri = 0; ri < ncur; ri++) {
            uint64_t residue = cur[ri];
            uint64_t power = 1 % k;
            for (unsigned e = 0; e <= max_power; e++) {
                uint64_t out = mul_mod(residue, power, k);
                if (stats) stats->generated++;
                if (marks[out] != generation) {
                    marks[out] = generation;
                    if (nnext >= cap) die("divisor DP reachable-set overflow");
                    next[nnext++] = out;
                    if (out == target_ii || out == target_i) {
                        if (stats) {
                            stats->reachable = nnext;
                            stats->early_target_hits++;
                        }
                        free(marks); free(next); free(cur);
                        return 1;
                    }
                } else if (stats) {
                    stats->deduplicated++;
                }
                power = mul_mod(power, q, k);
            }
        }

        uint64_t *tmp = cur;
        cur = next;
        next = tmp;
        ncur = nnext;
    }

    if (stats) stats->reachable = ncur;
    free(marks); free(next); free(cur);
    return 0;
}

static int verify_prime_dp(uint64_t p, uint64_t K, uint64_t *checked,
                           uint64_t *hits, uint64_t *dp_reachable_sum) {
    if (!is_prime64(p)) die("DP verify target must be prime");
    if ((p & 3) != 1) die("DP verify target must be 1 mod4");

    uint64_t local_checked = 0;
    uint64_t local_hits = 0;
    uint64_t local_reachable = 0;

    for (uint64_t k = 3; k <= K; k += 4) {
        if (gcd64(k, p) != 1) continue;
        if (p > UINT64_MAX - k) break;
        uint64_t C = (p + k) / 4;
        fac_t f;
        factor64(C, &f);
        int ref = delta_zero(&f, C, k);
        dp_stats_t st;
        int got = divisor_dp_delta_zero(&f, C, k, &st);
        if (ref != got)
            die("divisor DP mismatch at p=%" PRIu64 " k=%" PRIu64, p, k);
        local_checked++;
        local_hits += (uint64_t)got;
        local_reachable += st.reachable;
        if (k > UINT64_MAX - 4) break;
    }

    if (checked) *checked += local_checked;
    if (hits) *hits += local_hits;
    if (dp_reachable_sum) *dp_reachable_sum += local_reachable;
    return 0;
}

static int self_test_dp(void) {
    static const uint64_t ps[] = {
        1009ull,
        2521ull,
        9658489ull,
        5151841ull,
        8243281ull,
        18766609ull,
        27211969ull
    };

    uint64_t checked = 0, hits = 0, reachable = 0;
    for (size_t i = 0; i < sizeof(ps) / sizeof(ps[0]); i++)
        verify_prime_dp(ps[i], 400, &checked, &hits, &reachable);

    if (!checked || !reachable) die("divisor DP self-test accounting failure");
    printf("cbx-divisor-dp-i self-test OK checked=%" PRIu64 " hits=%" PRIu64 "\n",
           checked, hits);
    return 0;
}

static uint64_t evaluate_reference_all(uint64_t p, uint64_t K) {
    uint64_t checksum = 0;
    uint64_t index = 0;
    for (uint64_t k = 3; k <= K; k += 4) {
        if (gcd64(k, p) != 1) continue;
        uint64_t C = (p + k) / 4;
        fac_t f;
        factor64(C, &f);
        int hit = delta_zero(&f, C, k);
        checksum ^= ((uint64_t)hit + 0x9e3779b97f4a7c15ull) * (++index);
        if (k > UINT64_MAX - 4) break;
    }
    return checksum;
}

static uint64_t evaluate_dp_all(uint64_t p, uint64_t K, dp_stats_t *aggregate) {
    memset(aggregate, 0, sizeof(*aggregate));
    uint64_t checksum = 0;
    uint64_t index = 0;
    for (uint64_t k = 3; k <= K; k += 4) {
        if (gcd64(k, p) != 1) continue;
        uint64_t C = (p + k) / 4;
        fac_t f;
        factor64(C, &f);
        dp_stats_t st;
        int hit = divisor_dp_delta_zero(&f, C, k, &st);
        aggregate->reachable += st.reachable;
        aggregate->generated += st.generated;
        aggregate->deduplicated += st.deduplicated;
        aggregate->early_target_hits += st.early_target_hits;
        checksum ^= ((uint64_t)hit + 0x9e3779b97f4a7c15ull) * (++index);
        if (k > UINT64_MAX - 4) break;
    }
    return checksum;
}

static void usage_dp(void) {
    fprintf(stderr,
            "cbx-divisor-dp-i — exact divisor-square Lane-I DP prototype\n"
            "  cbx-divisor-dp-i --prime P [--i-max K] [--repeat R]\n"
            "  cbx-divisor-dp-i --self-test\n");
}

int main(int argc, char **argv) {
    uint64_t p = 0;
    uint64_t K = 400;
    uint64_t repeat = 1;
    int self_test = 0;

    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--prime") && i + 1 < argc)
            p = parse_u64_dp("prime", argv[++i]);
        else if (!strcmp(argv[i], "--i-max") && i + 1 < argc)
            K = parse_u64_dp("i-max", argv[++i]);
        else if (!strcmp(argv[i], "--repeat") && i + 1 < argc)
            repeat = parse_u64_dp("repeat", argv[++i]);
        else if (!strcmp(argv[i], "--self-test")) self_test = 1;
        else if (!strcmp(argv[i], "--help") || !strcmp(argv[i], "-h")) {
            usage_dp(); return 0;
        } else {
            usage_dp(); return 2;
        }
    }

    if (self_test) return self_test_dp();
    if (!p || !is_prime64(p) || (p & 3) != 1)
        die("--prime must be a prime congruent to 1 mod4");
    if (K < 3 || !repeat) die("invalid --i-max or --repeat");

    uint64_t ref_checksum = 0;
    double t0 = now_seconds_dp();
    for (uint64_t r = 0; r < repeat; r++)
        ref_checksum ^= evaluate_reference_all(p, K) + r;
    double ref_seconds = now_seconds_dp() - t0;

    uint64_t dp_checksum = 0;
    dp_stats_t last = {0};
    double t1 = now_seconds_dp();
    for (uint64_t r = 0; r < repeat; r++) {
        dp_stats_t st;
        dp_checksum ^= evaluate_dp_all(p, K, &st) + r;
        last = st;
    }
    double dp_seconds = now_seconds_dp() - t1;

    if (ref_checksum != dp_checksum)
        die("reference and divisor-DP checksums disagree");

    double speedup = dp_seconds > 0.0 ? ref_seconds / dp_seconds : 0.0;
    printf("{\"kernel\":\"cbx.kernel\",\"mode\":\"divisor-dp-I-benchmark\","
           "\"prime\":%" PRIu64 ",\"i_max\":%" PRIu64 ",\"repeat\":%" PRIu64
           ",\"verified\":true,\"checksum\":%" PRIu64
           ",\"dp_reachable_sum\":%" PRIu64 ",\"dp_generated\":%" PRIu64
           ",\"dp_deduplicated\":%" PRIu64 ",\"dp_early_target_hits\":%" PRIu64
           ",\"reference_seconds\":%.9f,\"dp_seconds\":%.9f,\"speedup\":%.6f}\n",
           p, K, repeat, ref_checksum, last.reachable, last.generated,
           last.deduplicated, last.early_target_hits,
           ref_seconds, dp_seconds, speedup);
    return 0;
}
