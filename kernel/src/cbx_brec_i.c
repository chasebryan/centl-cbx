/*
 * cbx_brec_i.c — Bryan Recursive Entanglement Calculus telemetry for Lane I.
 *
 * This is an exact finite research profiler.  For each Mordell-hard prime p
 * and each admissible Lane-I shift k = 3 (mod 4), it evaluates
 *
 *     C = (p + k) / 4,
 *     +  iff delta_k(C) = 0,
 *     -  iff delta_k(C) != 0.
 *
 * The resulting +/- word is a CBX application of BREC v1.0.  Undefined
 * stages (for example gcd(k,p) != 1) are written as '?' and break recursive
 * motif continuity; they are never silently coerced to a negative stage.
 *
 * The Cross and Compass are finite projections.  This engine streams every
 * observed contiguous binary motif through --order N, so depth 4 already
 * goes strictly beyond the eight-ray projection without materializing an
 * exponential search tree per target.
 *
 * Research only.  BREC annotations do not alter W -> I -> N -> L verdicts,
 * do not grant pruning permission, and do not prove Erdős–Straus.
 */
#define main cbx_core_main
#include "cbx.c"
#undef main

typedef unsigned __int128 brec_u128;

static const uint64_t BREC_HARD[6] = {1, 121, 169, 289, 361, 529};
static const uint32_t BREC_SMALL_PRIMES[] = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
    41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
};

typedef struct {
    brec_u128 count;
    brec_u128 spectrum[3];
} brec_motif_t;

typedef struct {
    brec_u128 hard_primes;
    brec_u128 stages;
    brec_u128 defined;
    brec_u128 undefined;
    brec_u128 constructive;
    brec_u128 obstructive;
    brec_u128 up_plus_minus;
    brec_u128 down_minus_plus;
} brec_totals_t;

static uint64_t brec_parse_u64(const char *name, const char *text) {
    errno = 0;
    char *end = NULL;
    unsigned long long v = strtoull(text, &end, 10);
    if (errno || !end || *end) die("invalid %s: %s", name, text);
    return (uint64_t)v;
}

static uint64_t brec_first_congruent(uint64_t lo, uint64_t mod, uint64_t residue) {
    uint64_t rem = lo % mod;
    uint64_t add = (residue + mod - rem) % mod;
    if (lo > UINT64_MAX - add) return UINT64_MAX;
    return lo + add;
}

static void brec_u128_decimal(brec_u128 x, char out[64]) {
    char rev[64];
    size_t n = 0;
    if (!x) {
        strcpy(out, "0");
        return;
    }
    while (x) {
        rev[n++] = (char)('0' + (unsigned)(x % 10));
        x /= 10;
    }
    for (size_t i = 0; i < n; i++) out[i] = rev[n - 1 - i];
    out[n] = 0;
}

/*
 * BREC-local factorizer optimization.
 *
 * The shared core's factor_rec is exact, but composites with small factors
 * otherwise reach Pollard-rho.  Lane-I walks consecutive C values for each
 * target, where small factors are common.  Strip a fixed exact prefix first,
 * then hand only the residual to the deterministic-MR/Pollard-rho core.
 */
static int brec_factor64(uint64_t n, fac_t *f) {
    f->n = 0;
    if (n < 2) return 0;

    uint64_t raw[64];
    int nr = 0;

    for (size_t i = 0; i < sizeof(BREC_SMALL_PRIMES) / sizeof(BREC_SMALL_PRIMES[0]); i++) {
        uint64_t q = BREC_SMALL_PRIMES[i];
        while (n % q == 0) {
            if (nr >= 64) die("BREC factor stack overflow");
            raw[nr++] = q;
            n /= q;
        }
        if (n == 1) break;
        if (q > n / q) {
            if (nr >= 64) die("BREC factor stack overflow");
            raw[nr++] = n;
            n = 1;
            break;
        }
    }

    if (n > 1) factor_rec(n, raw, &nr);
    sort_u64(raw, nr);

    for (int i = 0; i < nr;) {
        int j = i + 1;
        while (j < nr && raw[j] == raw[i]) j++;
        f->ps[f->n] = raw[i];
        f->es[f->n] = (unsigned)(j - i);
        f->n++;
        i = j;
    }
    return f->n;
}

/* One signed-box traversal for both exact delta targets. */
static int brec_dfs_box_two(const fac_t *f, int i, uint64_t val, uint64_t mod,
                            uint64_t target_a, uint64_t target_b) {
    if (i == f->n) return val == target_a || val == target_b;
    uint64_t p = f->ps[i] % mod;
    uint64_t pinv = inv_mod(p, mod);
    if (!pinv) return 0;
    unsigned e = f->es[i];
    uint64_t cur = 1 % mod;
    for (unsigned j = 0; j < e; j++) cur = mul_mod(cur, pinv, mod);
    for (unsigned z = 0; z <= 2 * e; z++) {
        if (brec_dfs_box_two(f, i + 1, mul_mod(val, cur, mod), mod,
                             target_a, target_b))
            return 1;
        cur = mul_mod(cur, p, mod);
    }
    return 0;
}

static int brec_delta_zero(const fac_t *f, uint64_t C, uint64_t k) {
    if (k < 2 || gcd64(C, k) != 1) return 0;
    uint64_t cinv = inv_mod(C % k, k);
    uint64_t four_inv = inv_mod(4 % k, k);
    if (!cinv || !four_inv) return 0;
    uint64_t target_a = k - 1;
    uint64_t target_b = (k - mul_mod(four_inv, cinv, k)) % k;
    return brec_dfs_box_two(f, 0, 1 % k, k, target_a, target_b);
}

static int brec_same_fac(const fac_t *a, const fac_t *b) {
    if (a->n != b->n) return 0;
    for (int i = 0; i < a->n; i++)
        if (a->ps[i] != b->ps[i] || a->es[i] != b->es[i]) return 0;
    return 1;
}

static size_t brec_offset(unsigned depth) {
    return (((size_t)1) << depth) - 2;
}

static void brec_word_from_code(unsigned depth, size_t code, char *out) {
    for (unsigned i = 0; i < depth; i++) {
        unsigned shift = depth - 1 - i;
        out[i] = ((code >> shift) & 1u) ? '-' : '+';
    }
    out[depth] = 0;
}

static void brec_record_symbol(brec_motif_t *motifs, unsigned order,
                               uint64_t *rolling, unsigned *run_depth,
                               int minus, int spectrum) {
    uint64_t mask = order == 64 ? UINT64_MAX : ((((uint64_t)1) << order) - 1);
    *rolling = ((*rolling << 1) | (uint64_t)(minus ? 1 : 0)) & mask;
    if (*run_depth < order) (*run_depth)++;

    for (unsigned depth = 1; depth <= *run_depth; depth++) {
        size_t code_mask = (((size_t)1) << depth) - 1;
        size_t code = (size_t)(*rolling) & code_mask;
        size_t idx = brec_offset(depth) + code;
        motifs[idx].count++;
        if (spectrum >= 0 && spectrum < 3) motifs[idx].spectrum[spectrum]++;
    }
}

static int brec_self_test(void) {
    static const uint64_t samples[] = {
        1, 2, 3, 4, 5, 12, 97, 98, 99, 100,
        1000003ull, 1000003ull * 1000033ull, 9658489ull
    };
    for (size_t i = 0; i < sizeof(samples) / sizeof(samples[0]); i++) {
        fac_t a, b;
        factor64(samples[i], &a);
        brec_factor64(samples[i], &b);
        if (!brec_same_fac(&a, &b)) die("BREC factor equivalence self-test failed at %" PRIu64, samples[i]);
    }

    static const uint64_t ps[] = {1009, 2521, 9658489};
    for (size_t pi = 0; pi < sizeof(ps) / sizeof(ps[0]); pi++) {
        uint64_t p = ps[pi];
        for (uint64_t k = 3; k <= 79; k += 4) {
            if (gcd64(k, p) != 1 || p > UINT64_MAX - k) continue;
            uint64_t C = (p + k) / 4;
            fac_t a, b;
            factor64(C, &a);
            brec_factor64(C, &b);
            if (!brec_same_fac(&a, &b)) die("BREC Lane-I factor self-test failed");
            if (delta_zero(&a, C, k) != brec_delta_zero(&b, C, k))
                die("BREC dual-target delta self-test failed at p=%" PRIu64 " k=%" PRIu64, p, k);
        }
    }

    brec_motif_t motifs[30];
    memset(motifs, 0, sizeof(motifs));
    uint64_t rolling = 0;
    unsigned run_depth = 0;
    const char *word = "+--+";
    for (const char *s = word; *s; s++)
        brec_record_symbol(motifs, 4, &rolling, &run_depth, *s == '-', 1);
    size_t idx_pm = brec_offset(2) + 1; /* +- => binary 01 */
    size_t idx_mp = brec_offset(2) + 2; /* -+ => binary 10 */
    if (motifs[idx_pm].count != 1 || motifs[idx_mp].count != 1)
        die("BREC motif recurrence self-test failed");

    puts("cbx-brec-i self-test OK");
    return 0;
}

static void brec_usage(void) {
    fprintf(stderr,
            "cbx-brec-i — exact recursive BREC Lane-I profiler\n"
            "  cbx-brec-i --hi X [--lo L] [--i-max K] [--order N] [--segment N]\n"
            "             [--histories FILE]\n"
            "  cbx-brec-i --self-test\n\n"
            "BREC application: + iff delta_k((p+k)/4)=0, - iff exact miss.\n"
            "Undefined stages are '?', break motif continuity, and are never counted as '-'.\n"
            "Default order is 4; supported order is 1..16.\n");
}

int main(int argc, char **argv) {
    uint64_t lo = 2;
    uint64_t hi = 0;
    uint64_t K = DEFAULT_I_MAX;
    uint64_t segment = 1000000;
    unsigned order = 4;
    int self_test_only = 0;
    const char *histories_path = NULL;

    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--lo") && i + 1 < argc) lo = brec_parse_u64("lo", argv[++i]);
        else if (!strcmp(argv[i], "--hi") && i + 1 < argc) hi = brec_parse_u64("hi", argv[++i]);
        else if (!strcmp(argv[i], "--i-max") && i + 1 < argc) K = brec_parse_u64("i-max", argv[++i]);
        else if (!strcmp(argv[i], "--order") && i + 1 < argc) {
            uint64_t v = brec_parse_u64("order", argv[++i]);
            if (v < 1 || v > 16) die("--order must be in 1..16");
            order = (unsigned)v;
        }
        else if (!strcmp(argv[i], "--segment") && i + 1 < argc) segment = brec_parse_u64("segment", argv[++i]);
        else if (!strcmp(argv[i], "--histories") && i + 1 < argc) histories_path = argv[++i];
        else if (!strcmp(argv[i], "--self-test")) self_test_only = 1;
        else if (!strcmp(argv[i], "--help") || !strcmp(argv[i], "-h")) { brec_usage(); return 0; }
        else { brec_usage(); return 2; }
    }

    if (self_test_only) return brec_self_test();
    if (hi < 2 || hi < lo) die("--hi must be >= max(2,--lo)");
    if (K < 3) die("--i-max must be >= 3");
    if (!segment || segment > 100000000ull) die("--segment must be in 1..100000000");

    uint64_t nshifts64 = (K - 3) / 4 + 1;
    if (nshifts64 > SIZE_MAX - 1) die("too many BREC shifts");
    size_t nshifts = (size_t)nshifts64;

    size_t motif_count = (((size_t)1) << (order + 1)) - 2;
    brec_motif_t *motifs = calloc(motif_count, sizeof(*motifs));
    if (!motifs) die("BREC motif allocation failed");

    FILE *histories = NULL;
    if (histories_path) {
        histories = fopen(histories_path, "w");
        if (!histories) die("cannot open BREC history output: %s", strerror(errno));
        fputs("p\tspectrum\tstages\tdefined\tundefined\tpositive\tnegative\tbias\treversals\tparity\tinitial\tterminal\tfirst_hit_k\thistory\n", histories);
    }

    brec_totals_t total;
    memset(&total, 0, sizeof(total));

    for (uint64_t seg_lo = lo;;) {
        brec_u128 proposed = (brec_u128)seg_lo + segment - 1;
        uint64_t seg_hi = proposed > hi ? hi : (uint64_t)proposed;

        for (size_t r = 0; r < 6; r++) {
            uint64_t p = brec_first_congruent(seg_lo, 840, BREC_HARD[r]);
            if (p == UINT64_MAX) continue;
            while (p <= seg_hi) {
                if (p >= 2 && is_prime64(p)) {
                    int spectrum = spectrum_of(p);
                    total.hard_primes++;

                    char *history = NULL;
                    if (histories) {
                        if (nshifts > SIZE_MAX - 1) die("BREC history allocation overflow");
                        history = malloc(nshifts + 1);
                        if (!history) die("BREC history allocation failed");
                    }

                    size_t hp = 0;
                    uint64_t rolling = 0;
                    unsigned run_depth = 0;
                    int have_prev = 0;
                    int prev_minus = 0;
                    uint64_t first_hit_k = 0;
                    uint64_t defined = 0, undefined = 0, pos = 0, neg = 0, reversals = 0;
                    int initial_minus = 0, terminal_minus = 0;
                    int have_initial = 0;

                    for (uint64_t k = 3; k <= K; k += 4) {
                        total.stages++;
                        int stage_defined = 1;
                        if (gcd64(k, p) != 1 || p > UINT64_MAX - k) stage_defined = 0;

                        if (!stage_defined) {
                            total.undefined++;
                            undefined++;
                            rolling = 0;
                            run_depth = 0;
                            have_prev = 0;
                            if (history) history[hp++] = '?';
                        } else {
                            uint64_t C = (p + k) / 4;
                            fac_t f;
                            brec_factor64(C, &f);
                            int hit = brec_delta_zero(&f, C, k);
                            int minus = !hit;

                            total.defined++;
                            defined++;
                            if (hit) {
                                total.constructive++;
                                pos++;
                                if (!first_hit_k) first_hit_k = k;
                            } else {
                                total.obstructive++;
                                neg++;
                            }

                            if (!have_initial) {
                                initial_minus = minus;
                                have_initial = 1;
                            }
                            terminal_minus = minus;

                            if (have_prev) {
                                if (!prev_minus && minus) total.up_plus_minus++;
                                if (prev_minus && !minus) total.down_minus_plus++;
                                if (prev_minus != minus) reversals++;
                            }
                            prev_minus = minus;
                            have_prev = 1;

                            brec_record_symbol(motifs, order, &rolling, &run_depth, minus, spectrum);
                            if (history) history[hp++] = minus ? '-' : '+';
                        }

                        if (k > UINT64_MAX - 4) break;
                    }

                    if (history) {
                        history[hp] = 0;
                        const char *spec_name = spectrum >= 0 && spectrum < 3 ? SPEC_NAME[spectrum] : "?";
                        char initial = have_initial ? (initial_minus ? '-' : '+') : '?';
                        char terminal = have_initial ? (terminal_minus ? '-' : '+') : '?';
                        int parity = (neg & 1) ? -1 : 1;
                        int64_t bias = pos >= neg ? (int64_t)(pos - neg) : -(int64_t)(neg - pos);
                        if (fprintf(histories,
                                    "%" PRIu64 "\t%s\t%zu\t%" PRIu64 "\t%" PRIu64
                                    "\t%" PRIu64 "\t%" PRIu64 "\t%" PRId64 "\t%" PRIu64
                                    "\t%d\t%c\t%c\t%" PRIu64 "\t%s\n",
                                    p, spec_name, nshifts, defined, undefined, pos, neg, bias,
                                    reversals, parity, initial, terminal, first_hit_k, history) < 0)
                            die("cannot write BREC history output");
                        free(history);
                    }
                }
                if (p > UINT64_MAX - 840) break;
                p += 840;
            }
        }

        if (seg_hi == hi || seg_hi == UINT64_MAX) break;
        seg_lo = seg_hi + 1;
    }

    if (histories) {
        if (fflush(histories) != 0 || fsync(fileno(histories)) != 0)
            die("cannot flush BREC history output");
        fclose(histories);
    }

    char hard_s[64], stage_s[64], defined_s[64], undefined_s[64];
    char plus_s[64], minus_s[64], up_s[64], down_s[64];
    brec_u128_decimal(total.hard_primes, hard_s);
    brec_u128_decimal(total.stages, stage_s);
    brec_u128_decimal(total.defined, defined_s);
    brec_u128_decimal(total.undefined, undefined_s);
    brec_u128_decimal(total.constructive, plus_s);
    brec_u128_decimal(total.obstructive, minus_s);
    brec_u128_decimal(total.up_plus_minus, up_s);
    brec_u128_decimal(total.down_minus_plus, down_s);

    uint64_t formal_nonempty = (((uint64_t)1) << (order + 1)) - 2;
    uint64_t formal_with_epsilon = formal_nonempty + 1;

    printf("{\"kernel\":\"cbx.kernel\",\"version\":\"%s\","
           "\"mode\":\"brec-I\",\"brec_spec\":\"BREC-v1.0\","
           "\"application\":\"CBX-Lane-I-shift-history-v1\","
           "\"lo\":%" PRIu64 ",\"hi\":%" PRIu64 ",\"i_max\":%" PRIu64
           ",\"order\":%u,\"segment\":%" PRIu64 ","
           "\"formal_nonempty_histories_through_order\":%" PRIu64
           ",\"formal_histories_including_epsilon\":%" PRIu64
           ",\"hard_primes\":%s,\"stages\":%s,\"defined_stages\":%s,"
           "\"undefined_stages\":%s,\"constructive\":%s,\"obstructive\":%s,"
           "\"cross\":{\"right_plus\":%s,\"left_minus\":%s,"
           "\"up_plus_minus\":%s,\"down_minus_plus\":%s},"
           "\"histories_recorded\":%s,\"motifs\":[",
           VERSION, lo, hi, K, order, segment, formal_nonempty, formal_with_epsilon,
           hard_s, stage_s, defined_s, undefined_s, plus_s, minus_s,
           plus_s, minus_s, up_s, down_s, histories_path ? "true" : "false");

    int first = 1;
    char word[17];
    for (unsigned depth = 1; depth <= order; depth++) {
        size_t width = ((size_t)1) << depth;
        size_t off = brec_offset(depth);
        for (size_t code = 0; code < width; code++) {
            brec_motif_t *m = &motifs[off + code];
            if (!m->count) continue;
            char count_s[64], a_s[64], b_s[64], c_s[64];
            brec_u128_decimal(m->count, count_s);
            brec_u128_decimal(m->spectrum[0], a_s);
            brec_u128_decimal(m->spectrum[1], b_s);
            brec_u128_decimal(m->spectrum[2], c_s);
            brec_word_from_code(depth, code, word);
            if (!first) putchar(',');
            first = 0;
            printf("{\"history\":\"%s\",\"depth\":%u,\"count\":%s,"
                   "\"spectrum\":{\"A\":%s,\"B\":%s,\"C\":%s}}",
                   word, depth, count_s, a_s, b_s, c_s);
        }
    }
    puts("]}");

    free(motifs);
    return 0;
}
