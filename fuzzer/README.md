# Stage 2 fuzzer (`fredbear`)

A LibAFL (0.16.1) fuzzer where an operator-family policy picks the mutation for each execution
(PLAN section 2, "What one action is"). The policies port the simulator's controller exactly; see
the cross-check below.

**Status (Nov 13, 2026):** works end to end on libpng (four versions built on macOS; 1.6.45 and 1.6.46 also built and run on FarmShare's Linux compute nodes, see [`docs/SLURM.md`](../docs/SLURM.md)).
No pilot yet. Next steps are at the bottom.

## Setup

```bash
brew install rustup && export PATH="/opt/homebrew/opt/rustup/bin:$PATH" && rustup default stable
cd fuzzer
cargo build --release
cargo test --release
```

## Running a transition

```bash
B=target/release/fredbear
# 1. Base run on version v with uniform family choice. Saves the corpus and per-batch family counts.
$B --target toy-v1 --policy uniform --dict dicts/toy.dict --secs 3600 --out runs/base1
# 2. A trial on v+1 from the inherited corpus. Priors come from the base run's first --base-cutoff seconds.
$B --target toy-v2 --policy adaptive --base-log runs/base1/batches.jsonl \
   --corpus runs/base1/queue --dict dicts/toy.dict --secs 3600 --seed 1 --out runs/v2-adaptive-1
```

**Several base runs.** `--base-log` and `--corpus` each take one or more paths, for example
`--base-log runs/base-1.6.45-{1,2,3}/batches.jsonl --corpus runs/base-1.6.45-{1,2,3}/queue`.
- Base logs are pooled by summing each family's counts. The cutoff applies to each run's own
  clock. The prior's weight is still capped at `--cap-n` per family, so pooling sharpens the
  rates without strengthening the prior.
- Corpus directories are loaded in the order given. An input that adds no coverage over those
  loaded before it is kept as disabled (stored but never mutated), so this is a one-pass merge,
  not a full minimization. List the directories in the same order for every trial.
- Every input loaded, disabled ones included, is written to the trial's own `queue/`. Three
  merged libpng queues are about 60 MB per trial.

`--out` must not exist yet. Outputs:

| File | Contents |
|---|---|
| `coverage.csv` | `t,execs,corpus,edges` about once a second. The `t=0` row is the inherited corpus's own coverage. |
| `batches.jsonl` | One line per batch of 256 executions: followed model, P(H_T\|D), fitted log c, executions and successes per family. |
| `queue/`, `crashes/` | Corpus (the inherited corpus for the next version) and crashing inputs. |

## libxml2

```bash
./targets/libxml2/build.sh 2.14.6   # clones libxml2 into targets/libxml2/repo on first use
```

This writes `targets/libxml2/build/2.14.6/`: `fredbear`, `xml.dict` and `seeds/`. The build:
- uses libxml2's own OSS-Fuzz `xml` target (`fuzz/xml.c` plus `fuzz/fuzz.c`);
- configures the library as the tag's `fuzz/oss-fuzz-build.sh` does (static, no HTTP or Python,
  with zlib), except `--without-lzma` because FarmShare has no liblzma headers;
- instruments the library and the harness with SanitizerCoverage;
- generates seeds with the tag's own `fuzz/genSeed` from its test files, using the
  `XML_SEED_CORPUS_SRC` list in `fuzz/Makefile.am`, as OSS-Fuzz does (366 seeds for 2.14.6 and
  2.15.0).

It needs autotools, clang and zlib, and takes about 40 s on 8 CPUs.

Things to know about this harness:
- **Inputs are not plain XML.** `genSeed` writes a small serialized format: 4-byte parser
  options, a 4-byte allocation-failure position and a 4-byte push-parser chunk size, followed by
  the document and any entities it loads. So the input chooses parser modes, and also when a
  `malloc` should fail.
- **`LLVMFuzzerInitialize` must run first.** fredbear calls it through
  `targets/harness_shim.c`, which every `libharness.a` now includes; libpng's build adds it too.
- **The harness's custom mutator is not used.** libFuzzer would use `LLVMFuzzerCustomMutator`,
  which mutates the 4-byte header fields separately. fredbear uses its own 9 families for every
  target, so the shim just stubs the `LLVMFuzzerMutate` symbol that the custom mutator needs to
  link.

**Transitions with an identical harness.** `fuzz/xml.c`, `fuzz/fuzz.c`, `fuzz/fuzz.h` and
`fuzz/xml.dict` change only at the minor releases 2.11.0, 2.12.0, 2.13.0 and 2.14.0, and not at
2.15.0. Changed lines below are all library `.c` changes, unfiltered:

| Transition | Changed `.c` lines |
|---|---|
| 2.14.4 → 2.14.5 | 139 |
| 2.14.2 → 2.14.3 | 328 |
| 2.15.1 → 2.15.2 | 682 |
| 2.14.6 → 2.15.0 | about 46,600 |

**First numbers (Nov 17, 2026, a 60 s uniform run on 2.14.6):** edges 3,770 at t=0 (seeds) and
5,533 at 60 s, still climbing quickly. About 2.1k executions per second, roughly 25× slower per
execution than libpng.

## Measuring a main run

These scripts are used for the libxml2 main runs (`docs/RESULTS.md`, sections 6 and 7):

| Script | Does |
|---|---|
| `scripts/inherited.sh <old version>` | Lists the union of the three base runs' queues as `runs/xml/inherited-<old>.names` and `.paths` |
| `[OLD=2.14.5 NEW=2.14.6] scripts/xml-tasks.sh <root> <secs> "<seeds>" <policies...>` | Prints one trial command per line for the transition OLD → NEW (default 2.14.6 → 2.15.0), for `slurm/pack.sbatch` |
| `scripts/run-trial.sh <out> <inherited names> <fredbear command>` | Runs a trial in node-local `$TMPDIR`, then keeps only the results and the trial's new inputs (`new/`), with `/usr/bin/time -v` in `time.txt` |
| `targets/libxml2/build-cov.sh <version>` | Builds the same harness with Clang source coverage plus `targets/replay_main.c` into `build/<version>-cov/replay` |
| `scripts/coverage.py` | Replays inherited and new inputs on that build and writes branch, line, region and function coverage at chosen times (`coverage-llvm.csv`) |
| `scripts/analyze.py <root>` | Summarises branches, edges and new inputs per policy, with Mann–Whitney, A12 and Holm |

fredbear writes `start_epoch`, the wall-clock time when fuzzing starts after the corpus loads, so
new inputs can be placed on the same clock as `coverage.csv` by their mtimes.

## libpng

```bash
./targets/libpng/build.sh 1.6.45   # clones libpng into targets/libpng/repo on first use
```

This writes `targets/libpng/build/1.6.45/`: `fredbear` (the fuzzer for that version), `png.dict`
(OSS-Fuzz dictionary) and `seeds/` (PngSuite images). Run it with `--target harness`. The build
compiles libpng and its OSS-Fuzz harness with SanitizerCoverage, using OSS-Fuzz's configuration
(stdio and write support off), and links them into the fuzzer through `build.rs`.

| Transition | Size | Reachable changed lines | Library change |
|---|---|---|---|
| 1.6.39 → 1.6.40 | small | 48 | eXIf multiplicity and pCAL fixes |
| 1.6.45 → 1.6.46 | large | 315 | New mDCV and cLLI chunk parsing |
| 1.6.46 → 1.6.47 | very large | 2,633 | Colorspace precedence reworked; most `png_handle_*` chunk handlers rewritten |

Within each pair the OSS-Fuzz harness and dictionary are identical, so only the library differs.

**How these were picked** (survey of 1.6.30–1.6.59, Nov 15, 2026):
1. The harness (`contrib/oss-fuzz/libpng_read_fuzzer.cc`) and `png.dict` must be byte-identical
   within the pair. The harness changed at 13 of 29 releases, which rules those pairs out.
2. Size is measured as changed code the harness can reach: read-path library files only (`png.c`,
   `pngrutil.c`, `pngrtran.c`, `pngread.c`, `pngset.c`, `pngget.c`, `pngtrans.c`, `pngrio.c`,
   `pngmem.c`, `pngerror.c`), ignoring whitespace, comments, version strings and copyright lines.
   Write support and stdio are compiled out, and the harness never uses the progressive reader
   (`pngpread.c`), so those files are excluded.
3. Pairs from 1.6.52 on are avoided: the harness gains allocation-failure injection (`nalloc.h`).

To reproduce the numbers (from `targets/libpng/repo`; `a`/`b` are tags like `v1.6.45`):

```bash
git diff -U0 -w $a $b -- png.c pngrutil.c pngrtran.c pngread.c pngset.c pngtrans.c pngrio.c pngmem.c pngerror.c pngget.c | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' | grep -vE '1\.6\.[0-9]+|[Cc]opyright|^[+-][[:space:]]*(/?\*|//)|^[+-][[:space:]]*$' | wc -l
```

All five versions above build on macOS and Linux (FarmShare).

**First numbers (Nov 13, 2026, one 2-minute base run on 1.6.45; indicative only):**
- About 120k executions per second.
- Family success rates range from 2.5e-6 (delete) to 9.9e-5 (insert). Best/median is 2.1, so it
  just passes the PLAN's week-3 gate (≥ 2).
- On 1.6.46 the adaptive controller fits log c ≈ −1.8, so rates are about 6× lower than on v. This
  is the simulation's L ≈ 0.2 regime.

## Policies

| `--policy` | Simulator name | Behaviour |
|---|---|---|
| `uniform` | (base runs) | Uniform random family |
| `fresh` | `fresh` | Thompson sampling (TS) from Beta(1,1) |
| `calib` | `calib` | TS from calibrated fresh: old mean rate for every family |
| `shuffled` | `shuffled` | TS from the transfer prior with old rates shuffled across families |
| `transfer` | `transfer` | TS from the transfer prior |
| `adaptive` | `bmcs_cal_r` | Scale-invariant model comparison C vs T, acting at the fitted scale |
| `adaptive-unscaled` | `bmcs_cal` | Same comparison, acting with the unscaled prior |
| `mix50` | `mix50_cal_r` | Coin flip between C and T each batch, same rescaling |
| `dts` | not yet in the sim | Discounted TS (TA feedback): the transfer prior decays toward calib by `--gamma-prior` per batch; observed counts decay by `--gamma-data` (1 = off) |

`dts` decays toward calib, not Beta(1,1). Beta(1,1) expects about 50% success where real rates are
about 1e-3, so decaying toward it would force heavy exploration.

## Operator families

| Family | LibAFL mutators |
|---|---|
| bitflip | BitFlip, ByteFlip, ByteNeg |
| arith | ByteInc, ByteDec, ByteAdd, WordAdd, DwordAdd, QwordAdd |
| interesting | Byte/Word/DwordInteresting |
| random_bytes | ByteRand, BytesSet, BytesRandSet |
| delete | BytesDelete |
| insert | BytesExpand, BytesInsert, BytesRandInsert |
| copy_swap | BytesCopy, BytesInsertCopy, BytesSwap |
| splice | CrossoverInsert, CrossoverReplace |
| dictionary | TokenInsert, TokenReplace (needs `--dict`) |

Each execution applies a stack of 2^(1..7) mutations from one family, the same depth distribution as
LibAFL's stock havoc. Success (r_t = 1) means LibAFL added the input to the corpus, i.e. new
coverage including hit-count buckets, which is the PLAN's definition. If a family cannot mutate the
input (no tokens, a one-entry corpus for splice), no execution happens. The family is then not
counted, and another one is picked.

## Code

| File | Contents |
|---|---|
| `src/policy.rs` | Priors, model comparison and policies. No LibAFL types. |
| `src/mutator.rs` | Family table, the LibAFL `Mutator`, batch log, base-log reader |
| `src/main.rs` | Campaign runner (CLI) |
| `src/toy.rs` | Two-version toy target, for testing the pipeline only |
| `src/policy_ref.rs` | Reference values generated from `sim/bandit_sim.py` |

**Cross-check against the simulator.** The test `marginal_likelihood_matches_simulator` checks
P(D\|H) and the fitted log c for both hypotheses against `sim/bandit_sim.py`, to 1e-8. To regenerate
`policy_ref.rs` after changing the simulator's math (from `sim/`):

```python
import numpy as np
from bandit_sim import build_priors, log_marginal_scaled
pr = build_priors(np.array([60., 30, 20, 12, 8, 5, 3, 1]), np.full(8, 6000.), 5000, rng=np.random.default_rng(0))
s = np.array([5., 20, 4, 1, 2, 0, 3, 1])
for name, tag in (("transfer", "T"), ("calib", "C")):
    lml, logc = log_marginal_scaled(*pr[name], s, 2000 - s)
    print(f"const REF_LML_{tag}: f64 = {lml!r};\nconst REF_LOGC_{tag}: f64 = {logc!r};")
```

One deliberate difference from the simulator: counts update after every execution, not at batch
end. The hypothesis is still resampled once per batch.

## Next steps

1. **Calibrate N and γ to real execution rates.** The simulator treats 10⁶ executions as 4 hours;
   libpng runs about 4×10⁸ per hour, so N=5000 and a per-batch γ of 0.999 wash out in about a
   second. Pick N so the prior covers the same fraction of the campaign as in the simulation.
2. **Dictionary.** The OSS-Fuzz `png.dict` lacks chunk names added after it was written (e.g. mDCV,
   cLLI, new in 1.6.46). Decide whether to keep it as is (same for every version, as the PLAN says)
   or add them.
3. **MOpt baseline.** Add a `--policy mopt` that uses LibAFL's `StdMOptMutator` instead of
   `FamilyMutator`.
4. **Corpus scheduler.** `QueueScheduler` is a placeholder. Pick one scheduler and use it for every
   policy.
5. **Linux.** Builds and runs on FarmShare (Ubuntu 24.04, Nov 16). It needs rustc ≥ 1.93.1 and a `CPLUS_INCLUDE_PATH` fix for clang++; see [`docs/SLURM.md`](../docs/SLURM.md). No link-order changes were needed.
6. **Analysis script.** Coverage at 15 min / 1 h, Mann–Whitney + A12 (reuse `sim/bandit_sim.py`'s
   `mann_whitney`, `a12`, `holm`).
