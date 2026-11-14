# Stage 2 fuzzer (`fredbear`)

A LibAFL (0.16.1) fuzzer where an operator-family policy picks the mutation for each execution
(PLAN section 2, "What one action is"). The policies port the simulator's controller exactly; see
the cross-check below.

**Status (Nov 13, 2026):** works end to end on libpng (four versions built, macOS only so far).
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

`--out` must not exist yet. Outputs:

| File | Contents |
|---|---|
| `coverage.csv` | `t,execs,corpus,edges` about once a second. The `t=0` row is the inherited corpus's own coverage. |
| `batches.jsonl` | One line per batch of 256 executions: followed model, P(H_T\|D), fitted log c, executions and successes per family. |
| `queue/`, `crashes/` | Corpus (the inherited corpus for the next version) and crashing inputs. |

## libpng

```bash
./targets/libpng/build.sh 1.6.45   # clones libpng into targets/libpng/repo on first use
```

This writes `targets/libpng/build/1.6.45/`: `fredbear` (the fuzzer for that version), `png.dict`
(OSS-Fuzz dictionary) and `seeds/` (PngSuite images). Run it with `--target harness`. The build
compiles libpng and its OSS-Fuzz harness with SanitizerCoverage, using OSS-Fuzz's configuration
(stdio and write support off), and links them into the fuzzer through `build.rs`.

| Transition | Size | Library change |
|---|---|---|
| 1.6.39 → 1.6.40 | small | ~50 lines: eXIf and pCAL fixes |
| 1.6.45 → 1.6.46 | large | ~590 lines: new mDCV and cLLI chunk parsing |

Within each pair the OSS-Fuzz harness and dictionary are identical, so only the library differs.

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
5. **Linux.** Only built on macOS. On Linux, link order with GNU ld may need fixing in `build.rs`.
6. **Analysis script.** Coverage at 15 min / 1 h, Mann–Whitney + A12 (reuse `sim/bandit_sim.py`'s
   `mann_whitney`, `a12`, `holm`).
