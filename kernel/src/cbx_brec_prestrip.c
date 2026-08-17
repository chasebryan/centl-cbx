/*
 * cbx_brec_prestrip.c — exact consecutive-cofactor small-prime prestrip prototype.
 *
 * Lane I obeys the affine recurrence
 *
 *     C_(j+1) = C_j + 1,
 *     k_(j+1) = k_j + 4,
 *     4*C_j - k_j = p.
 *
 * cbx_brec_i currently strips its fixed small-prime prefix independently for
 * each cofactor.  This prototype exploits the consecutive C block instead:
 * for each small prime q, compute the first divisible offset once and visit
 * only offsets separated by q.  Residuals are then handed to the exact shared
 * deterministic-MR/Pollard-rho factorizer.
 *
 * The tool is deliberately separate from production BREC until whole-block
 * factor equivalence and benchmark evidence justify promotion.
 */
#define _POSIX_C_SOURCE 200809L
#define main cbx_core_main
#include "cbx.c"
#undef main

#include <time.h>

static const uint32_t PRE_SMALL_PRIMES[] = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
    41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
};

typedef struct {
    uint64_t residual;
    fac_t small;
} pre_item_t;

typedef struct {
    uint64_t initial_mod_tests;
    uint64_t scheduled_offsets;
    uint64_t qadic_divisions;
} pre_stats_t;

static uint64_t parse_u64_pre(const char *name, const char *text) {
    errno = 0;
    char *end = NULL;
    unsigned long long v = strtoull(text, &end, 10);
    if (errno || !end || *end) die("invalid %s: %s", name, text);
    return (uint64_t)v;
}

static size_t fac_capacity_pre(const fac_t *f) {
    return sizeof(f->ps) / sizeof(f->ps[0]);
}

static void fac_append_pre(fac_t *f, uint64_t q, unsigned e) {
    if (!e) return;
    if ((size_t)f->n >= fac_capacity_pre(f)) die("prestrip factor capacity exceeded");
    f->ps[f->n] = q;
    f->es[f->n] = e;
    f->n++;
}

static void prestrip_block(uint64_t start, size_t count, pre_item_t *items,
                           pre_stats_t *stats) {
    memset(stats, 0, sizeof(*stats));
    for (size_t i = 0; i < count; i++) {
        if (start > UINT64_MAX - (uint64_t)i) die("prestrip block overflow");
        items[i].residual = start + (uint64_t)i;
        items[i].small.n = 0;
    }

    for (size_t qi = 0; qi < sizeof(PRE_SMALL_PRIMES) / sizeof(PRE_SMALL_PRIMES[0]); qi++) {
        uint64_t q = PRE_SMALL_PRIMES[qi];
        uint64_t rem = start % q;
        stats->initial_mod_tests++;
        uint64_t offset = rem ? q - rem : 0;
        if (offset >= count) continue;

        for (size_t i = (size_t)offset; i < count;) {
            stats->scheduled_offsets++;
            unsigned e = 0;
            while (items[i].residual % q == 0) {
                items[i].residual /= q;
                e++;
                stats->qadic_divisions++;
            }
            fac_append_pre(&items[i].small, q, e);
            if (i > SIZE_MAX - (size_t)q) break;
            i += (size_t)q;
        }
    }
}

static void finish_factor_pre(const pre_item_t *item, fac_t *out) {
    *out = item->small;
    uint64_t n = item->residual;
    if (n <= 1) return;

    uint64_t raw[64];
    int nr = 0;
    factor_rec(n, raw, &nr);
    sort_u64(raw, nr);

    for (int i = 0; i < nr;) {
        int j = i + 1;
        while (j < nr && raw[j] == raw[i]) j++;
        fac_append_pre(out, raw[i], (unsigned)(j - i));
        i = j;
    }
}

static int same_factor_pre(const fac_t *a, const fac_t *b) {
    if (a->n != b->n) return 0;
    for (int i = 0; i < a->n; i++)
        if (a->ps[i] != b->ps[i] || a->es[i] != b->es[i]) return 0;
    return 1;
}

static uint64_t factor_checksum_pre(const fac_t *f) {
    uint64_t h = 1469598103934665603ull;
    for (int i = 0; i < f->n; i++) {
        h ^= f->ps[i];
        h *= 1099511628211ull;
        h ^= f->es[i];
        h *= 1099511628211ull;
    }
    return h;
}

static double now_seconds_pre(void) {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) die("clock_gettime failed");
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static void verify_block_pre(uint64_t start, size_t count, pre_stats_t *stats,
                             uint64_t *checksum) {
    pre_item_t *items = calloc(count ? count : 1, sizeof(*items));
    if (!items) die("prestrip allocation failed");
    prestrip_block(start, count, items, stats);

    uint64_t h = 0;
    for (size_t i = 0; i < count; i++) {
        fac_t ref, got;
        factor64(start + (uint64_t)i, &ref);
        finish_factor_pre(&items[i], &got);
        if (!same_factor_pre(&ref, &got))
            die("prestrip factor mismatch at n=%" PRIu64, start + (uint64_t)i);
        h ^= factor_checksum_pre(&got) + 0x9e3779b97f4a7c15ull * (uint64_t)(i + 1);
    }
    free(items);
    if (checksum) *checksum = h;
}

static int self_test_pre(void) {
    static const struct { uint64_t start; size_t count; } cases[] = {
        {1, 256},
        {253, 128},
        {2414623, 128},
        {1287961, 128},
        {4691653, 128},
    };
    for (size_t i = 0; i < sizeof(cases) / sizeof(cases[0]); i++) {
        pre_stats_t stats;
        uint64_t checksum;
        verify_block_pre(cases[i].start, cases[i].count, &stats, &checksum);
        if (!stats.initial_mod_tests || !checksum)
            die("prestrip self-test accounting failure");
    }
    puts("cbx-brec-prestrip self-test OK");
    return 0;
}

static void usage_pre(void) {
    fprintf(stderr,
            "cbx-brec-prestrip — consecutive-cofactor factorization prototype\n"
            "  cbx-brec-prestrip --start C --count N [--repeat R]\n"
            "  cbx-brec-prestrip --prime P --i-max K [--repeat R]\n"
            "  cbx-brec-prestrip --self-test\n");
}

int main(int argc, char **argv) {
    uint64_t start = 0;
    uint64_t count64 = 0;
    uint64_t prime = 0;
    uint64_t i_max = 0;
    uint64_t repeat = 1;
    int self_test = 0;

    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--start") && i + 1 < argc) start = parse_u64_pre("start", argv[++i]);
        else if (!strcmp(argv[i], "--count") && i + 1 < argc) count64 = parse_u64_pre("count", argv[++i]);
        else if (!strcmp(argv[i], "--prime") && i + 1 < argc) prime = parse_u64_pre("prime", argv[++i]);
        else if (!strcmp(argv[i], "--i-max") && i + 1 < argc) i_max = parse_u64_pre("i-max", argv[++i]);
        else if (!strcmp(argv[i], "--repeat") && i + 1 < argc) repeat = parse_u64_pre("repeat", argv[++i]);
        else if (!strcmp(argv[i], "--self-test")) self_test = 1;
        else if (!strcmp(argv[i], "--help") || !strcmp(argv[i], "-h")) { usage_pre(); return 0; }
        else { usage_pre(); return 2; }
    }

    if (self_test) return self_test_pre();
    if (!repeat) die("--repeat must be >=1");

    if (prime) {
        if (start || count64) die("use either --prime/--i-max or --start/--count");
        if ((prime & 3) != 1) die("--prime must be 1 mod4 for the Lane-I cofactor walk");
        if (i_max < 3) die("--i-max must be >=3");
        if (prime > UINT64_MAX - 3) die("prime too large for C0");
        start = (prime + 3) / 4;
        count64 = (i_max - 3) / 4 + 1;
    }

    if (!start || !count64) die("provide a positive block with --start/--count");
    if (count64 > SIZE_MAX / sizeof(pre_item_t)) die("block too large");
    if (start > UINT64_MAX - (count64 - 1)) die("block overflows uint64");
    size_t count = (size_t)count64;

    pre_stats_t verified_stats;
    uint64_t verified_checksum = 0;
    verify_block_pre(start, count, &verified_stats, &verified_checksum);

    double scalar_start = now_seconds_pre();
    uint64_t scalar_checksum = 0;
    for (uint64_t r = 0; r < repeat; r++) {
        uint64_t h = 0;
        for (size_t i = 0; i < count; i++) {
            fac_t f;
            factor64(start + (uint64_t)i, &f);
            h ^= factor_checksum_pre(&f) + 0x9e3779b97f4a7c15ull * (uint64_t)(i + 1);
        }
        scalar_checksum ^= h + r;
    }
    double scalar_seconds = now_seconds_pre() - scalar_start;

    double block_start = now_seconds_pre();
    uint64_t block_checksum = 0;
    pre_stats_t last_stats;
    for (uint64_t r = 0; r < repeat; r++) {
        pre_item_t *items = calloc(count, sizeof(*items));
        if (!items) die("prestrip benchmark allocation failed");
        prestrip_block(start, count, items, &last_stats);
        uint64_t h = 0;
        for (size_t i = 0; i < count; i++) {
            fac_t f;
            finish_factor_pre(&items[i], &f);
            h ^= factor_checksum_pre(&f) + 0x9e3779b97f4a7c15ull * (uint64_t)(i + 1);
        }
        block_checksum ^= h + r;
        free(items);
    }
    double block_seconds = now_seconds_pre() - block_start;

    if (scalar_checksum != block_checksum)
        die("benchmark checksum disagreement between scalar and block factorization");

    uint64_t scalar_small_mods = count64 *
        (uint64_t)(sizeof(PRE_SMALL_PRIMES) / sizeof(PRE_SMALL_PRIMES[0]));
    double speedup = block_seconds > 0.0 ? scalar_seconds / block_seconds : 0.0;

    printf("{\"kernel\":\"cbx.kernel\",\"mode\":\"brec-prestrip-benchmark\","
           "\"start\":%" PRIu64 ",\"count\":%" PRIu64 ",\"repeat\":%" PRIu64
           ",\"verified\":true,\"checksum\":%" PRIu64
           ",\"small_primes\":%zu,\"scalar_small_prime_mod_tests\":%" PRIu64
           ",\"block_initial_mod_tests\":%" PRIu64
           ",\"block_scheduled_offsets\":%" PRIu64
           ",\"block_qadic_divisions\":%" PRIu64
           ",\"scalar_seconds\":%.9f,\"block_seconds\":%.9f,\"speedup\":%.6f}\n",
           start, count64, repeat, verified_checksum,
           sizeof(PRE_SMALL_PRIMES) / sizeof(PRE_SMALL_PRIMES[0]),
           scalar_small_mods, verified_stats.initial_mod_tests,
           verified_stats.scheduled_offsets, verified_stats.qadic_divisions,
           scalar_seconds, block_seconds, speedup);
    return 0;
}
