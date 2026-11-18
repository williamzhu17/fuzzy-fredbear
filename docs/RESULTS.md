# Stage 2 Results Log

Results from real libpng fuzzing on FarmShare. Newest findings first in the summary; experiments
are in the order they ran. Every run used the fuzzer in `fuzzer/`, on FarmShare `iron` nodes
through Slurm (see [`SLURM.md`](SLURM.md)). Raw outputs are in `fuzzer/runs/` on FarmShare. That
directory is git-ignored, so the numbers below are the record.

## Summary (Nov 17, 2026)

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
- Add a target with more headroom (libxml2 or libtiff, both in PLAN v3 before the Stage 2 cut).
- Change the main outcome to something that still moves on a plateau: time to reach changed
  code, or coverage features.
- Fix N = 10⁶ in the plan.
- Decide whether trials on the new version use the extended dictionary, and if so whether to
  redo the base runs with it.

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

## Reproducing

All commands run from `fuzzer/` on FarmShare. The task files list every trial's exact command:
- `runs/base-tasks.txt` (base runs)
- `runs/pilot-1.6.46/tasks.txt` (pilot)
- `runs/probe/tasks.txt` (headroom probe; also holds `png-plus.dict`)
- `runs/ncheck/tasks.txt` (prior weight N)
- `runs/xml/base-tasks.txt` and `runs/xml/probe/tasks.txt` (libxml2)

Submit a task file with
`slurm/fresh sbatch -c 16 --mem=60G -t <time> slurm/pack.sbatch <tasks file>`. Each trial's
outputs (`coverage.csv`, `batches.jsonl`, `queue/`) are in the `--out` folder named in its command.
