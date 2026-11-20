# Stage 2 Results Log

Results from real fuzzing of libpng and libxml2 on FarmShare. Newest findings first in the summary; experiments
are in the order they ran. Every run used the fuzzer in `fuzzer/`, on FarmShare `iron` nodes
through Slurm (see [`SLURM.md`](SLURM.md)). Raw outputs are in `fuzzer/runs/` on FarmShare. That
directory is git-ignored, so the numbers below are the record.

## Summary (updated Nov 18, 2026)

**libxml2 (section 5), added Nov 17:**
- **libxml2 has the headroom libpng lacks.** Base runs on 2.14.6 were still gaining 33–70 edges
  in their last 15 minutes.
- **On 2.14.6 → 2.15.0, every policy keeps finding edges for the whole 15 minutes**: +28 to +55.
  Libpng found almost all of its few new edges in the first minute.
- **A trial yields about 190–240 successes,** against 20–60 on libpng.
- **Family success rates are 1e-4 to 1e-3,** about 100× libpng's and in the simulation's range,
  so N = 10⁴ gives a few pseudo-successes per family.
- **First hint of an effect:** adaptive's successes (209–242) all beat uniform's (188–208) in
  this probe: A12 = 1.00, exact Mann–Whitney p = 0.029, with 4 trials each.
  - This is one comparison out of six possible between the four policies and is uncorrected.
  - Edge gains overlap across all policies.
  - Treat it as a reason to run the full design, not a result.

**libxml2 main run (section 6), Nov 17:** 5 policies × 20 trials × 15 min on 2.14.6 → 2.15.0.
**No planned comparison is significant on any of the three outcomes** (independent branch
coverage, edges, new inputs).
- adaptive vs transfer: A12 = 0.41 on branches.
- The probe's adaptive-vs-uniform hint shrank from A12 = 1.00 (n = 4) to 0.66 (n = 20).
- transfer has the highest mean on every outcome, but only by about 0.5 sd.
- fresh learns the same family mix as transfer within the 15 minutes, so the transferred prior
  has little to add on this transition.

**libxml2 small transition (section 7), Nov 18:** same design on 2.14.5 → 2.14.6 (89 changed
library lines). **Transfer is significantly worse than fresh** on the primary outcome (A12 = 0.28,
Holm p = 0.046) and on inputs. The prior was learned from seed-started base runs, which rank
splice at the top; trials starting from the merged corpus favour copy_swap instead. Adaptive
recovers to fresh's level and beats transfer on inputs (Holm p = 0.014). Within-campaign learning
beats uniform here, unlike on the big transition.

**libpng (sections 1–4):**

1. **libpng is saturated in our setup.** The merged corpus inherited from the old version already
   reaches almost all edges the harness can reach. With the stock dictionary, edge coverage on
   1.6.46 did not move at all in 30 minutes under any policy. With mDCV/cLLI added to the
   dictionary, every policy finds the same 14 new edges within the first minute. After that, only
   0–12 more edges turn up in the next 14 minutes, so there is too little left for a scheduler to
   win.
2. **The original prior weight N = 5,000 could not test transfer at all.** Real success rates are
   about 10⁻⁶ to 10⁻⁵ per execution, 100× lower than in simulation. At N = 5,000 every family's
   prior is about Beta(1.0, 5000): the "+1" swamps the measured rates, the transfer and calibrated
   priors are nearly identical, and the controller's P(H_T | D) stays at 0.50. N = 10⁶ gives
   about 1–12 pseudo-successes per family, so the old ranking is visible.
3. **With N = 10⁶ the priors and controller behave as designed, but no policy does better.** The
   transfer prior visibly steers mutations, and adaptive's P(H_T | D) rises to 0.70–0.76. Edge
   counts and successes still overlap completely across uniform, fresh, transfer and adaptive.
   This shows only that the method is no longer disabled, not that it helps.
4. **The real evidence budget is small.** A 15-minute trial yields about 20–60 successes, against
   thousands per campaign in simulation.
5. **The fitted scale c is stable at about 0.12–0.22** on both 1.6.46 and 1.6.47. That is the
   simulation's L ≈ 0.2 regime, so rescaling the prior is the right variant.
6. **The best-vs-median gate check fails narrowly:** best family / median family = 1.9 on 1.6.45
   and 1.7 on 1.6.46, against the required 2. `delete` is about 20× below the rest; the other
   families are close together.
7. **Speed is about 25k executions per second per trial** with 16 trials sharing a node, not the
   120k the plan assumed. It varies 2–3× between trials, with outliers down to 3k. Campaigns
   limited by time are therefore noisy, so compare at a fixed execution count.

**Open decisions:**
- Whether to build the prior from the same campaign phase it is used in (late base-run batches,
  or a short run on the merged corpus), since section 7 points to a phase mismatch.
- Why adaptive's family mix looks like fresh's although it follows the transfer model in 71% of
  batches (section 7).
- Fix N in the plan per target: 10⁶ for libpng, 10⁴ for libxml2.
- For libpng only: whether trials use the extended dictionary, and if so whether to redo the base
  runs with it.

## Setup common to all runs

- **Fuzzer:** `fredbear` (LibAFL 0.16.1), with one operator family chosen per execution from 9
  families and a batch size of 256. A success is an input added to the corpus.
- **Builds:** libpng 1.6.39, 1.6.40, 1.6.45, 1.6.46 and 1.6.47, each built with
  `targets/libpng/build.sh` and its own tag's OSS-Fuzz harness and `png.dict`. All five build on
  Linux.
- **Inherited corpus:** the three base runs' `queue/` folders, merged with
  `--corpus <q1> <q2> <q3>`. LibAFL keeps an input only if it adds coverage over those loaded
  before it.
- **Prior:** the three base runs' `batches.jsonl` files, pooled with
  `--base-log <l1> <l2> <l3>` (counts summed over each run's first 3600 s).
- **Concurrency:** 9–16 single-CPU trials packed into one `interactive` job with
  `slurm/pack.sbatch`.

## 1. Base runs (Nov 16; job 1990785)

`uniform`, 1 h, starting from the 51 PngSuite seeds, 3 seeds × 3 versions.

| Version | Edges at 5 / 15 / 30 / 60 min | Executions in 1 h |
|---|---|---|
| 1.6.39 | 1160–1194 / 1181–1200 / 1182–1202 / 1186–1203 | 164M–248M |
| 1.6.45 | 1262–1373 / 1372–1383 / 1381–1389 / 1396–1397 | 175M–184M |
| 1.6.46 | 1277–1332 / 1291–1373 / 1299–1388 / 1380–1406 | 101M–142M |

- Coverage levels off within 5 minutes on 1.6.39 and by about 15 minutes on 1.6.45. On 1.6.46
  it still jumped late, by +80 to +90 edges between 15 and 60 minutes in two of the three runs.
- No crashes. Of the 51 seeds, 22–27 were kept at load time; the rest added no coverage.
- Each family was used about 20.4M times per run.
- Pooled success rates per family were 3e-7 (`delete`) to 1.1e-5 (`insert`) on 1.6.45, and
  5e-7 to 1.4e-5 on 1.6.46.

## 2. Pilot on 1.6.45 → 1.6.46 (Nov 16; job 1990986)

`uniform`, `fresh`, `transfer` and `adaptive`, 8 trials each, 30 min, stock dictionary, N = 5,000.

- **Edges:** all 32 trials started at 1,409 and ended at 1,409 or 1,410.
- **Corpus growth:**

  | Policy | Corpus at 30 min (from 550) | Mean growth |
  |---|---|---|
  | uniform | 570–577 | +23 |
  | transfer | 564–594 | +27 |
  | fresh | 565–592 | +29 |
  | adaptive | 565–594 | +29 |

  The gap is small compared with the spread across trials, and the N-check below does not
  reproduce it.
- **Why edges were flat:** no input in any base or pilot queue contains an `mDCV` or `cLLI` chunk.
  1.6.46's new chunk code was never reached, because `png.dict` lacks those names. The harness
  ignores chunk CRCs (`PNG_CRC_QUIET_USE`), so the chunk name is the only obstacle.
- **Speed:** 11–30k executions per second per trial.

## 3. Headroom probe (Nov 16; job 1991201)

`uniform` × 4 per arm, 15 min, N = 5,000. Arm B also ran `adaptive` × 4.
`png-plus.dict` is `png.dict` plus `section_mDCV="mDCV"` and `section_cLLI="cLLI"`.

| Arm | Transition | Dictionary | Edges at 0 / 1 / 5 / 15 min | Gain |
|---|---|---|---|---|
| A | 1.6.45 → 1.6.46 | plus | 1409 / 1422–1423 / 1423 / 1428–1435 | +19 to +26 |
| B | 1.6.46 → 1.6.47 | stock | 1210 / 1213–1217 / 1215–1217 / 1218–1220 | +8 to +10 |
| C | 1.6.46 → 1.6.47 | plus | 1210 / 1214–1218 / 1218–1220 / 1220–1232 | +10 to +22 |

- **The dictionary works.** Every arm A and C trial has 5–20 queue inputs containing mDCV or
  cLLI chunks, and the arm B trials have none.
- **Most gains come in the first minute**, which is easy coverage every policy gets.
- **Edge counts on 1.6.47 are not comparable with 1.6.46's,** because the instrumented code
  differs. We have no 1.6.47 run from the seeds, so its ceiling is unknown.
- **Adaptive on arm B:** P(H_T | D) stayed at 0.49–0.51 for 15 minutes, following each model about
  half the time. c = 0.12–0.20.
- **The family ranking shifts.** On arm A (uniform), `dictionary` becomes the best family
  (5.4e-6) and `insert` drops to mid-table (2.2e-6). In the 1.6.45 base runs `insert` was the
  best (1.1e-5). Part of this shift comes from the dictionary change, not the code change.

## 4. Prior weight N (Nov 17; job 1993505)

Same setup as arm A (1.6.46, `png-plus.dict`), 15 min.

What the prior looks like at each N, from the pooled 1.6.45 counts. The prior for each family is
Beta(a, b) with a = 1 + min(n, N)·p̂:

| Family | p̂ | a at N = 5e3 | a at N = 1e5 | a at N = 1e6 |
|---|---|---|---|---|
| bitflip | 3.6e-6 | 1.02 | 1.36 | 4.6 |
| arith | 5.7e-6 | 1.03 | 1.57 | 6.7 |
| interesting | 5.9e-6 | 1.03 | 1.59 | 6.9 |
| random_bytes | 3.4e-6 | 1.02 | 1.34 | 4.4 |
| delete | 3.3e-7 | 1.00 | 1.03 | 1.3 |
| insert | 1.1e-5 | 1.06 | 2.12 | 12.2 |
| copy_swap | 3.0e-6 | 1.02 | 1.30 | 4.0 |
| splice | 7.9e-6 | 1.04 | 1.79 | 8.9 |
| dictionary | 7.4e-6 | 1.04 | 1.74 | 8.4 |

Results:

| Policy | Trials | Successes per trial | Mean | Edges at 15 min | Adaptive P(H_T \| D) at end |
|---|---|---|---|---|---|
| uniform (arm A above) | 4 | 25–46 | 35 | 1428–1435 | |
| fresh | 4 | 23–43 | 29 | 1423–1433 | |
| transfer, N = 1e5 | 3 | 12–34 | 22 | 1423 | |
| transfer, N = 1e6 | 3 | 24–37 | 29 | 1423–1435 | |
| adaptive, N = 1e5 | 3 | 28–58 | 43 | 1428–1435 | 0.56–0.62 |
| adaptive, N = 1e6 | 3 | 33–40 | 38 | 1423–1429 | 0.70–0.76 |

- **What the transfer prior does to the family mix.** At N = 1e6, transfer uses `delete` for
  0.3–0.8% of mutations, against about 5% at N = 1e5, and gives more to `insert` and `splice`. At
  N = 1e5 its family mix looks much like fresh's.
- **What adaptive does at N = 1e6.** It follows the transfer model in 66–73% of batches, with
  c = 0.14–0.22. P(H_T | D) moving shows only that the controller responds to evidence. Whether
  favouring the transfer model was correct has not been checked.
- **Outcomes overlap across all policies.** Two transfer N = 1e5 trials ran at 3k and 11k
  executions per second, against about 25k for the rest, and have the lowest success counts.

## 5. libxml2 (Nov 17; jobs 1993978, 1994110)

Setup: libxml2's own OSS-Fuzz `xml` harness, built with `fuzzer/targets/libxml2/build.sh` (see
`fuzzer/README.md`). The harness, `fuzz.c` and `xml.dict` are identical in 2.14.6 and 2.15.0;
about 46,600 library `.c` lines changed between them.

### Base runs (job 1993978)

`uniform`, 1 h, from the 366 genSeed seeds, 3 seeds per version.

| Version | Edges at 0 / 5 / 15 / 30 / 45 / 60 min | Executions in 1 h | Corpus at 1 h |
|---|---|---|---|
| 2.14.6 | 3770 / 5984–6046 / 6231–6245 / 6322–6408 / 6387–6477 / 6443–6534 | 5.8M–6.9M | 4321–4417 |
| 2.15.0 | 3680 / 5569–5653 / 5823–5872 / 5943–6051 / 5993–6121 / 6022–6171 | 2.4M–3.9M | 3346–3740 |

- **Still climbing at 60 minutes,** by +33 to +70 edges between 45 and 60 minutes.
- **No crashes.**
- **Speed:** about 1.6–1.9k executions per second on 2.14.6 and 0.7–1.1k on 2.15.0.
- **Each base queue is about 95 MB** (2.14.6) or 120–150 MB (2.15.0).
- **Pooled family success rates on 2.14.6:** `delete` 9.7e-5, `interesting` 4.6e-4, `bitflip`
  4.9e-4, `copy_swap` 5.9e-4, `arith` 6.6e-4, `random_bytes` 6.8e-4, `dictionary` 7.2e-4, `insert`
  1.0e-3, `splice` 1.1e-3.
- **Best / median = 1.65** (2.14.6) and 1.80 (2.15.0), so the gate check fails narrowly, as on
  libpng.

### Probe on 2.14.6 → 2.15.0 (job 1994110)

uniform, fresh, transfer and adaptive, 4 trials each, 15 min, N = 10⁴. Every trial starts from
the three merged 2.14.6 queues (13,547 inputs loaded, about 2,535 kept) and the pooled prior.

- **The inherited corpus starts above 2.15.0's own ceiling.** On 2.15.0 it starts at 6,454–6,458
  edges, higher than any 2.15.0 run from the seeds reached in an hour (6,022–6,171).
- **Starting points differ slightly between trials** (corpus kept 2,528–2,542), even though every
  trial loads the same folders in the same order. libxml2 is not fully deterministic between
  processes, probably because of its randomized hash seeds.

| Policy | Edges gained in 15 min | Mean | Successes (corpus growth) | Mean | Executions per second |
|---|---|---|---|---|---|
| uniform | 28–49 | 36.5 | 188–208 | 196.5 | 1.21k–1.32k |
| fresh | 37–39 | 38.0 | 185–215 | 193.8 | 0.96k–1.12k |
| transfer | 29–55 | 40.0 | 186–236 | 213.2 | 1.00k–1.15k |
| adaptive | 29–44 | 38.2 | 209–242 | 225.5 | 1.04k–1.15k |

- **Edges keep coming throughout the campaign.** Edges at 1 / 5 / 10 / 15 min for uniform-1 were
  6466 / 6480 / 6497 / 6506, not a single early jump as on libpng.
- **Adaptive vs uniform on successes:** all 4 adaptive trials beat all 4 uniform trials, A12 = 1.00,
  exact two-sided Mann–Whitney p = 0.029.
  - Transfer vs uniform: A12 = 0.69, p = 0.49.
  - These are uncorrected; after a Holm correction across the six pairwise comparisons,
    adaptive vs uniform would not be significant.
  - Edge gains, including edges at a fixed 900k executions, overlap across all policies.
- **Adaptive's controller.** P(H_T | D) was 0.73–0.84 at the end, and adaptive followed the
  transfer model in 66–82% of batches. Fitted c = 0.19–0.24, so on libxml2 too the new version's
  rates are about a fifth of the old ones.
- **Learned policies run about 15% slower than uniform** (about 1.05–1.10k against 1.27k
  executions per second). They favour `insert` and `splice`, which make inputs longer. So they
  found more per execution than the per-time numbers suggest.
- **Disk:** the 16 trial folders took 4.5 GB, mostly copies of the 280 MB inherited corpus. Their
  `queue/` folders were deleted afterwards.

## 6. Main run on libxml2 2.14.6 → 2.15.0 (Nov 17; jobs 1994460, 1994461)

**Design, fixed before the results were looked at:**
- **Policies:** uniform, fresh, transfer, adaptive and dts.
- **Trials:** 20 per policy (seeds 1–20), 15 min each, limited by wall-clock time.
- **Settings:** N = 10⁴, dts at its defaults (γ_prior = 0.999 and γ_data = 1 per batch).
- **Inputs:** every trial starts from the merged 2.14.6 base queues and the pooled prior.
- **Scheduling:** 16 trials at a time, seeds in the outer loop so every wave mixes all policies.
- **How each trial runs:** through `scripts/run-trial.sh`, in node-local `/tmp`. The inherited
  corpus copy never touches NFS. Only `coverage.csv`, `batches.jsonl`, `start_epoch`, `crashes/`,
  `time.txt` and the trial's new inputs (`new/`) are kept.

**Outcomes, each the gain over the trial's own t = 0 at 15 minutes:**
1. **Branches (primary):** independent branch coverage. `scripts/coverage.py` replays the
   inherited corpus plus the trial's new inputs on a Clang source-coverage build of 2.15.0
   (`targets/libxml2/build-cov.sh`), excluding harness files. Out of 55,204 branches.
2. **Edges:** fredbear's own edge count.
3. **Inputs:** new corpus inputs, the policies' reward.

**Comparisons:** adaptive vs transfer, adaptive vs uniform and transfer vs fresh. Each uses a
two-sided Mann–Whitney test and A12, Holm-corrected across the three within each outcome
(`scripts/analyze.py`). Every other pair is exploratory and uncorrected.

**Smoke tests before launch** (jobs 1994439, 1994452):
- **I/O stall, found and fixed.** With trials writing to NFS, a 90 s trial took 4 min 20 s, mostly
  spent writing its 280 MB inherited-corpus copy. In local `/tmp`, 15 concurrent 120 s trials
  took 177 s each. The remaining 54 s is executing the 13,547 inherited inputs once at startup,
  which is not counted in the time budget.
- **Memory:** 0.6 GB peak per trial (`time.txt`), so 16 trials need about 10 GB. The job requests
  32 GB.
- **Disk:** 2–4 MB per trial.
- **The three outcomes are consistent.** The new-input count equals corpus growth in every trial,
  and branch coverage starts at the same 10,161 in every trial and rises over time.

**Results** (job 1994460: 100 of 100 trials completed, 1 h 50 min; coverage scored by job
1994461):

| Policy | Branches gained (primary) | Edges gained | New inputs | Executions per second |
|---|---|---|---|---|
| uniform | 45.5 ± 7.9 (33–62) | 36.9 ± 5.3 | 201.2 ± 17.8 | 1,292 |
| fresh | 47.2 ± 8.8 (35–64) | 38.8 ± 7.0 | 210.2 ± 23.9 | 1,074 |
| transfer | 49.6 ± 9.1 (38–67) | 40.6 ± 7.4 | 215.6 ± 15.0 | 1,058 |
| adaptive | 46.2 ± 7.6 (32–63) | 38.2 ± 6.7 | 210.9 ± 17.8 | 1,061 |
| dts | 47.1 ± 9.9 (31–69) | 38.2 ± 9.2 | 207.3 ± 23.7 | 1,119 |

Each cell is mean ± sd over 20 trials (range in brackets), as the gain at 15 minutes over 10,161
branches, about 6,456 edges and about 2,535 inputs at t = 0.

**Planned comparisons** (Holm-corrected within each outcome):

| Comparison | Branches: A12, p, Holm p | Edges: A12, Holm p | New inputs: A12, p, Holm p |
|---|---|---|---|
| adaptive vs transfer | 0.41, 0.32, 0.97 | 0.43, 1.00 | 0.44, 0.50, 0.87 |
| adaptive vs uniform | 0.55, 0.59, 0.97 | 0.56, 1.00 | 0.66, 0.086, 0.26 |
| transfer vs fresh | 0.58, 0.42, 0.97 | 0.56, 1.00 | 0.57, 0.43, 0.87 |

**Findings:**
- **No planned comparison is significant on any outcome.** The primary result is null: on this
  transition, adaptive does not beat transfer (it is slightly behind, A12 = 0.41), and neither
  learned prior separates from its baseline.
- **The probe's hint did not replicate.** The probe had adaptive above uniform on new inputs with
  A12 = 1.00 and 4 trials each. With 20 each it shrank to A12 = 0.66 (Holm p = 0.26). That is the
  expected regression of a small-sample extreme.
- **The direction is consistent but small.** transfer has the highest mean on all three outcomes
  and uniform the lowest. The gaps are about 4 branches, or about 0.5 sd. The largest
  exploratory difference, transfer vs uniform on new inputs (A12 = 0.72, uncorrected p = 0.018),
  is one of 21 exploratory tests across the three outcomes, so it is not evidence by itself.
- **Over time:** branch gains at 5 and 10 minutes show the same picture. Every planned Holm p is
  at least 0.83, and uniform even has the highest mean at 5 minutes.

**Why the policies end up close:**
- **Fresh learns the old ranking quickly.** With about 200 successes per trial, fresh puts about
  50% of its mutations into `insert` and `splice` by the end, the same as transfer (51%). Every
  learned policy gives `delete` only 1–4%. So transfer's head start is worth little after the
  first minutes.
- **The controller acts as designed.** adaptive ended at P(H_T | D) = 0.74 (0.49–0.86), followed
  the transfer model in 71% of batches, and fitted c = 0.26 (0.18–0.30). Following the transfer
  model is reasonable here, but it can only be as good as transfer, which itself barely beats
  fresh.
- **Learned policies are about 18% slower** (1,058–1,119 against 1,292 executions per second for
  uniform), because they favour `insert` and `splice`, which make inputs longer. Under a
  wall-clock budget this costs them about a sixth of their executions, which offsets part of
  their gain per execution.

**Other checks:** no crashes in any trial. Peak memory was 0.61–0.64 GB per trial. The 100 trial
folders take 1.2 GB.

## 7. Small transition: libxml2 2.14.5 → 2.14.6 (Nov 18; jobs 1995251–1995253, 1995322, 1995323)

**Question:** the plan predicts that transfer helps most when old and new versions are close.
Section 6 used a large transition (44 changed library files, about 44,600 changed lines) and
found nothing. This run repeats it on the smallest available step with the same harness:
2.14.5 → 2.14.6, 7 library files and 89 changed lines (`fuzz/xml.c`, `fuzz/fuzz.c`, `fuzz/fuzz.h`
unchanged).

**Design, fixed before any data was collected:** identical to section 6 except for the versions.
- **Base runs:** three 60 min uniform runs on 2.14.5 from its own genSeed seeds
  (`runs/xml/small/base-tasks.txt`). Their merged queues are the inherited corpus
  (`scripts/inherited.sh 2.14.5`) and their pooled logs the prior.
- **Main run:** uniform, fresh, transfer, adaptive and dts; 20 trials per policy (seeds 1–20),
  15 min each, wall-clock bound; N = 10⁴; dts at its defaults; 16 trials at a time through
  `scripts/run-trial.sh` (tasks from `OLD=2.14.5 NEW=2.14.6 scripts/xml-tasks.sh`).
- **Outcomes:** gains at 15 min in branches (primary, replayed on a source-coverage build of
  2.14.6), edges and inputs.
- **Comparisons:** adaptive vs transfer, adaptive vs uniform, transfer vs fresh; two-sided
  Mann–Whitney and A12, Holm-corrected within each outcome (`scripts/analyze.py`). Everything
  else is exploratory.
- **Expectation if the plan is right:** transfer and adaptive beat fresh and uniform by more than
  in section 6.

**Base runs** (job 1995252): 4,321–4,573 inputs and 6,465–6,520 edges after 60 min, close to
2.14.6's 6,443–6,534. The merged queues hold 13,019 unique inputs.

**Smoke test** (job 1995253; one 120 s trial per policy): all five completed; peak memory
0.64 GB per trial. Coverage starts at 10,764 of 57,870 branches in every trial. **Headroom is much
smaller than on the big transition.** At 120 s the trials gained 16–19 inputs, 1–5 edges and 0–2
branches, against about 50 inputs, about 14 edges and 4–28 branches in section 6's smoke test.
The merged 2.14.5 corpus already reaches nearly everything 2.14.6 can, so expect small 15-minute
gains, many ties, and less power than in section 6.

**Results** (job 1995322: 100 of 100 trials completed, 1 h 50 min; coverage scored by job
1995323). Gains at 15 min, mean ± sd over 20 trials:

| Policy | Branches (primary) | Edges | Inputs | Exec/s |
|---|---|---|---|---|
| uniform | 12.6 ± 4.2 | 16.9 ± 3.6 | 114.5 ± 9.7 | 858 |
| fresh | 18.2 ± 8.1 | 17.6 ± 4.9 | 157.3 ± 21.0 | 873 |
| transfer | 12.7 ± 6.1 | 15.8 ± 4.7 | 142.2 ± 21.3 | 793 |
| adaptive | 19.4 ± 10.2 | 18.9 ± 6.0 | 162.1 ± 17.5 | 814 |
| dts | 14.7 ± 4.2 | 16.8 ± 4.3 | 152.6 ± 18.6 | 876 |

**Planned comparisons** (Holm-corrected within each outcome):

| Comparison | Branches A12 (Holm p) | Edges A12 (Holm p) | Inputs A12 (Holm p) |
|---|---|---|---|
| adaptive vs transfer | 0.69 (0.076) | 0.65 (0.31) | 0.75 (0.014) |
| adaptive vs uniform | 0.68 (0.076) | 0.59 (0.40) | 1.00 (< 10⁻⁴) |
| transfer vs fresh | **0.28** (0.046) | 0.38 (0.40) | **0.31** (0.044) |

**Findings:**
1. **Transfer is worse than fresh**, the opposite of the plan's prediction: significant on the
   primary outcome (A12 = 0.28, Holm p = 0.046) and on inputs (A12 = 0.31, Holm p = 0.044), same
   direction but not significant on edges. Transfer is no better than uniform on branches
   (12.7 vs 12.6).
2. **Adaptive recovers.** It beats transfer on inputs (Holm p = 0.014) and is ahead on branches
   and edges (A12 0.69 and 0.65, not significant). It ties fresh (exploratory A12 = 0.52 on
   branches, 0.53 on inputs).
3. **Learning within the campaign helps here, unlike section 6.** Every learned policy beats
   uniform on inputs (A12 0.87–1.00); fresh beats uniform on branches (exploratory A12 = 0.71,
   p = 0.025). In section 6, fresh and uniform were close.
4. **At 5 and 10 min** the same pattern holds but weaker: adaptive vs uniform on inputs is
   significant at both (Holm p ≤ 0.0012); no planned branch comparison is.

**Why transfer hurts:** the 2.14.5 base runs ranked the families in a different regime. They
started from 366 seeds; the main trials start from the merged 13,019-input corpus. Per-execution
success rates (×10⁻⁴):

| | insert | copy_swap | splice | rest (range) |
|---|---|---|---|---|
| 2.14.5 base runs (the prior) | 11.2 | 6.2 | 11.4 | 1.0–7.6 |
| 2.14.6 trials, all policies pooled | about 2.8 | about 2.5 | about 1.8 | 0.1–1.5 |

In the base runs splice ties insert for the top and copy_swap is mid-table; in the trials,
copy_swap is second and splice has fallen behind it. Transfer therefore spends 14.6% of its
mutations on splice and 16.7% on copy_swap; fresh, learning from the trial alone, spends 7.8% and
23.4%. In section 6 splice stayed strong in the trials (2.5–2.8), so the same mismatch did not
arise. The base-run rates are also 4–7× higher than in-trial rates for every family, so the prior
is overconfident in absolute terms, not just in ranking.

**Controller:** adaptive ended at P(T) = 0.74 on average (range 0.23–0.87) and followed the
transfer model in 71% of batches, yet its mix (51% insert, 17.5% copy_swap, 11.1% splice) is not
transfer's, and it outperformed transfer. Why it ends up near fresh while nominally following
transfer has not been checked.

**Speed** differs less than in section 6: 793–876 executions per second for all policies.

**Other checks:** no crashes; peak memory 0.64–0.68 GB per trial; 513 MB on disk.

## Reproducing

All commands run from `fuzzer/` on FarmShare. The task files list every trial's exact command:
- `runs/base-tasks.txt` (base runs)
- `runs/pilot-1.6.46/tasks.txt` (pilot)
- `runs/probe/tasks.txt` (headroom probe; also holds `png-plus.dict`)
- `runs/ncheck/tasks.txt` (prior weight N)
- `runs/xml/base-tasks.txt`, `runs/xml/probe/tasks.txt` and `runs/xml/main/tasks.txt` (libxml2;
  the main run's tasks were generated by `scripts/xml-tasks.sh`)
- `runs/xml/small/` (section 7: `build.sbatch`, `base-tasks.txt`, `smoke.sbatch`, `main/tasks.txt`,
  `main/coverage.sbatch`)

Submit a task file with
`slurm/fresh sbatch -c 16 --mem=60G -t <time> slurm/pack.sbatch <tasks file>`. Each trial's
outputs (`coverage.csv`, `batches.jsonl`, `queue/`) are in the `--out` folder named in its command.
