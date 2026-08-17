CC ?= cc
CFLAGS ?= -O3 -std=c11 -Wall -Wextra
LDFLAGS ?=
LDLIBS ?= -lm
PYTHON ?= python3

.PHONY: all clean check

all: cbx cbx-inverse cbx-forward-i cbx-shift-i cbx-profile-i cbx-standalone-i cbx-brec-i
	mkdir -p state observations letters

cbx: src/cbx_runtime.c src/cbx.c
	$(CC) $(CFLAGS) -o $@ src/cbx_runtime.c $(LDFLAGS) $(LDLIBS)
	mkdir -p state observations letters

cbx-inverse: src/cbx_inverse.c src/cbx.c
	$(CC) $(CFLAGS) -o $@ src/cbx_inverse.c $(LDFLAGS) $(LDLIBS)

cbx-forward-i: src/cbx_forward_i.c src/cbx.c
	$(CC) $(CFLAGS) -o $@ src/cbx_forward_i.c $(LDFLAGS) $(LDLIBS)

cbx-shift-i: src/cbx_shift_i.c src/cbx.c
	$(CC) $(CFLAGS) -o $@ src/cbx_shift_i.c $(LDFLAGS) $(LDLIBS)

cbx-profile-i: src/cbx_profile_i.c src/cbx.c
	$(CC) $(CFLAGS) -o $@ src/cbx_profile_i.c $(LDFLAGS) $(LDLIBS)

cbx-standalone-i: src/cbx_standalone_i.c src/cbx.c
	$(CC) $(CFLAGS) -o $@ src/cbx_standalone_i.c $(LDFLAGS) $(LDLIBS)

cbx-brec-i: src/cbx_brec_i.c src/cbx.c
	$(CC) $(CFLAGS) -o $@ src/cbx_brec_i.c $(LDFLAGS) $(LDLIBS)

check: cbx cbx-inverse cbx-forward-i cbx-shift-i cbx-profile-i cbx-standalone-i cbx-brec-i
	./cbx self-test
	./cbx-brec-i --self-test
	./cbx probe 1009
	./cbx probe 2521
	./cbx probe 9658489
	./cbx-inverse --hi 100000 --i-max 80 --segment 25000 --verify
	./cbx-forward-i --hi 100000 --i-max 80
	./cbx-shift-i --hi 100000 --i-max 80 --segment 25000 --verify
	./cbx-profile-i --hi 100000 --i-max 80 --segment 25000 > /tmp/cbx-check-profile.json
	./cbx-standalone-i --hi 20000 --i-max 40 --segment 10000 --sets /tmp/cbx-check-sets.tsv > /tmp/cbx-check-standalone.json
	./cbx-brec-i --hi 20000 --i-max 40 --order 8 --segment 10000 --histories /tmp/cbx-check-brec.tsv > /tmp/cbx-check-brec.json
	grep -q '"mode":"brec-I"' /tmp/cbx-check-brec.json
	grep -q 'CBX-Lane-I-shift-history-v1' /tmp/cbx-check-brec.json
	$(PYTHON) -m py_compile analyze.py analyze_geometry.py analyze_layers.py analyze_profile.py analyze_standalone.py analyze_overlap.py analyze_spectrum_overlap.py analyze_brec.py analyze_brec_cylinder.py analyze_brec_target.py bench_i.py plan_hybrid.py certify_i.py verify_brec_i.py ../research/verify_k3_brec_obstruction_normal_form.py ../research/verify_k23_typei_companion_patterns.py ../research/verify_k23_brec_ancestry_falsifiers.py
	$(PYTHON) verify_brec_i.py /tmp/cbx-check-standalone.json /tmp/cbx-check-brec.json --json > /tmp/cbx-check-brec-verify.json
	$(PYTHON) analyze_brec.py --self-test >/dev/null
	$(PYTHON) analyze_brec.py /tmp/cbx-check-brec.json --histories /tmp/cbx-check-brec.tsv --prefix-depth 6 --json > /tmp/cbx-check-brec-analysis.json
	grep -q '"prefix_cylinders"' /tmp/cbx-check-brec-analysis.json
	grep -q '"next_k":23' /tmp/cbx-check-brec-analysis.json
	$(PYTHON) analyze_brec_cylinder.py --self-test >/dev/null
	$(PYTHON) analyze_brec_cylinder.py /tmp/cbx-check-brec.tsv --prefix='-----' --json > /tmp/cbx-check-brec-k23-cylinder.json
	grep -q '"mode":"analyze-brec-cylinder"' /tmp/cbx-check-brec-k23-cylinder.json
	grep -q '"next_k":23' /tmp/cbx-check-brec-k23-cylinder.json
	$(PYTHON) analyze_brec_target.py --self-test >/dev/null
	$(PYTHON) analyze_brec_target.py /tmp/cbx-check-brec.tsv --target-k 23 --max-prefix-depth 5 --json > /tmp/cbx-check-brec-k23-target.json
	grep -q '"mode":"analyze-brec-target"' /tmp/cbx-check-brec-k23-target.json
	grep -q '"target_k":23' /tmp/cbx-check-brec-k23-target.json
	$(PYTHON) ../research/verify_k3_brec_obstruction_normal_form.py > /tmp/cbx-check-k3-obstruction-normal-form.json
	grep -q '"verified": true' /tmp/cbx-check-k3-obstruction-normal-form.json
	$(PYTHON) ../research/verify_k23_typei_companion_patterns.py > /tmp/cbx-check-k23-companion-patterns.json
	grep -q '"verified": true' /tmp/cbx-check-k23-companion-patterns.json
	$(PYTHON) ../research/verify_k23_brec_ancestry_falsifiers.py > /tmp/cbx-check-k23-ancestry-falsifiers.json
	grep -q '"verified": true' /tmp/cbx-check-k23-ancestry-falsifiers.json
	grep -q '18766609' /tmp/cbx-check-k23-ancestry-falsifiers.json
	$(PYTHON) analyze_geometry.py --self-test
	./cbx-inverse --hi 20000 --i-max 40 --segment 10000 --layers /tmp/cbx-check-layers.tsv >/dev/null
	$(PYTHON) analyze_layers.py /tmp/cbx-check-layers.tsv --json >/dev/null
	$(PYTHON) analyze_profile.py /tmp/cbx-check-profile.json --json > /tmp/cbx-check-profile-analysis.json
	$(PYTHON) analyze_standalone.py /tmp/cbx-check-standalone.json --json >/dev/null
	$(PYTHON) analyze_overlap.py /tmp/cbx-check-sets.tsv --json >/dev/null
	$(PYTHON) analyze_spectrum_overlap.py /tmp/cbx-check-sets.tsv --json >/dev/null
	$(PYTHON) plan_hybrid.py /tmp/cbx-check-profile-analysis.json --json >/dev/null
	$(PYTHON) plan_hybrid.py /tmp/cbx-check-profile-analysis.json --c-retention 0.10 --json >/dev/null
	$(PYTHON) bench_i.py --hi 20000 --i-max 40 --repeat 1 --no-verify --json >/dev/null
	$(PYTHON) certify_i.py --hi 20000 --i-max 80 --segment 10000 --json >/dev/null
	rm -f /tmp/cbx-check-layers.tsv /tmp/cbx-check-profile.json /tmp/cbx-check-profile-analysis.json /tmp/cbx-check-standalone.json /tmp/cbx-check-sets.tsv /tmp/cbx-check-brec.json /tmp/cbx-check-brec.tsv /tmp/cbx-check-brec-verify.json /tmp/cbx-check-brec-analysis.json /tmp/cbx-check-brec-k23-cylinder.json /tmp/cbx-check-brec-k23-target.json /tmp/cbx-check-k3-obstruction-normal-form.json /tmp/cbx-check-k23-companion-patterns.json /tmp/cbx-check-k23-ancestry-falsifiers.json
	rm -f state/check.seed observations/check.jsonl
	./cbx go --run check --step 1000 --iterations 2 --sweep-only
	test "$$(sed -n 's/^sweep=//p' state/check.seed)" = "2000"
	rm -f state/check.seed observations/check.jsonl

clean:
	rm -f cbx cbx-inverse cbx-forward-i cbx-shift-i cbx-profile-i cbx-standalone-i cbx-brec-i
	rm -rf __pycache__
