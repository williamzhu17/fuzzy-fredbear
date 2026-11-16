# Stage 1 simulation: cross-version operator-preference transfer

Synthetic K=8-armed Bernoulli bandit standing in for mutation-operator families
(plan sections 3–6). There is no fuzzer and no corpus: only per-operator success rates that differ
between "version v" and "version v+1".

- **Plan:** [`../docs/PLAN.md`](../docs/PLAN.md) is the current plan (v3), revised from these results.
  [`../docs/archive/PLAN_v2.md`](../docs/archive/PLAN_v2.md) is the version that existed before the simulation.
- **Short version of the findings:** see [Bottom line](#bottom-line) below, then
  [Overall conclusions](#overall-conclusions) and [Proposed next steps](#proposed-next-steps).

## Bottom line

From the consolidated run 10: 276 transition × level cells, 7 policies, 30 trials each
(`results/final/summary.md`).

1. **Transfer on its own is a gamble.** When the old best operator is still best in v+1, transfer
   beats calibrated fresh in 71 of 78 cells. The gain is 4–33% at 1h, and the ranking itself matters:
   transfer beats a shuffled prior in 76 of 78. When the old best is not still best, transfer is worse
   than calib in 124 of 174 cells, with a median of 0.73–0.80× calib. Its worst cell is 0.29× the
   best fixed prior.
2. **The rescaled adaptive controller (`bmcs_cal_r`) removes that downside.**
   - Its worst cell over all 276 is 0.88× the hindsight-best of fresh / calib / transfer. Transfer's
     worst is 0.29×, and calib's and fresh's are 0.54× and 0.59×.
   - Its median is 0.96× at L=1, 0.995× at L=0.5 and 1.09× at L=0.2. It beats every fixed prior at
     L=0.2, because none of them are at the right scale.
   - No other policy has a worst case above 0.84×.
3. **The inherited-corpus scale (L) matters as much as the ranking.** Rescaling turns the unscaled
   controller's 0.89× median at L=0.2 into 1.09×. At L=1 it costs about 2%: the unscaled
   `bmcs_cal` is better there (0.985×) and loses to the rescaled controller in only 2 of 92 cells.
   Because L is unknown before a campaign, the rescaled controller is the robust choice.
4. **The adaptive controller is only slightly better than a rescaled 50/50 coin flip between calib
   and transfer.**
   - It is significantly better in 45 of 276 cells and worse in 1.
   - The median gain is +2.0% at L=1, +1.5% at L=0.5 and +0.9% at L=0.2.
   - Most of the robustness comes from rescaling plus hedging between C and T. Weighing the
     evidence adds a small, consistent edge, mostly at L=1 and where transfer hurts.
5. **What Stage 2 can show.** Simulated Stage 2 uses 6 random transitions and a pooled test (run 10,
   F). It detects "adaptive beats transfer" and "adaptive beats fresh" 62–99% of the time with 10–20
   trials. It detects "adaptive beats 50/50" only 9–65% of the time, depending on L (best at L=1).
   This holds before real-fuzzing noise. "Beats 50/50" cannot be a primary claim at this scale.

## Setup

From the repo root (see the top-level `README.md`):

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cd sim
../.venv/bin/python <script> ...
```

All scripts resolve `--out` / results-dir arguments relative to `sim/`, so run them from anywhere.
The venv has numpy 1.26.4, scipy 1.17.1 and matplotlib 3.11.2 (pinned in `requirements.txt`).
The commands in the run log below assume you are in `sim/`.

## Files

| file | purpose |
|---|---|
| `bandit_sim.py` | Simulator: scenarios, base runs and priors, all policies, statistics (MWU, A12, Holm) |
| `run_stage1.py` | Full grid driver: scenarios × policies × N (+ optional N/γ/B sweeps) → `<out>/summary.md`, `raw.pkl`, PNGs |
| `compare_table.py` | Compact cross-scenario tables (1h/4h medians, A12/p for one focus policy, P(T)) from a results dir |
| `rank_sweep.py` | Rank-correlation sweep (run 6): permuted v+1 rates over ρ and random draws → `summary.md`, `rank_sweep.png`; `--replot` redraws from `raw.pkl` |
| `power_check.py` | Power at Stage 2 trial counts (run 8): subsamples n trials from a large-R results dir, Holm per scenario |
| `run_next.sh` | Commands for runs 6–10 |
| `final_sweep.py` | Consolidated sweep (run 10): 7 policies × (8 designed + 84 rank) scenarios × L ∈ {1, 0.5, 0.2}; resumable, slim `raw.pkl` |
| `final_report.py` | Analysis of run 10 → `results/final/summary.md` (sections A–F, including simulated Stage 2) |
| `recency_sweep.py` | Recency-weighted prior sweep (run 11): decay vs weight-only variants at several half-lives, including the drift scenarios; resumable, `--report` rewrites `summary.md` |
| `results/<run>/` | One directory per full run (see run log). Each has `summary.md` (all tables), plus `raw.pkl` and plots when generated locally |

Only `summary.md` is committed. `raw.pkl` (about 1.2 GB in total), the plots (`*.png`) and the
run logs (`*.log`) are git-ignored, so the results can be read without regenerating anything. To rerun an analysis script (`compare_table.py`,
`power_check.py`, `final_report.py`, `rank_sweep.py --replot`) you need the `raw.pkl` for that run:
regenerate it with the run's command below or get a copy from a teammate.

Result files written before the reorganisation may still name their directory the old way, e.g.
`results_power_L0.5` means `results/power_L0.5/`.

## Model

- **Rates:** θ_a(t) = level · θ_a / (1 + t/τ_a) · exp(−S_a/pool_a).
  - τ_a is a fraction of the campaign length T (default 0.05).
  - S_a is the number of successes operator a has found in this campaign.
  - Time decay stands in for coverage saturation; the pools (default ∞) model depletion.
- **Campaign length:** T = 1,000,000 executions is called "4h", so T/16 is "15m" and T/4 is "1h".
- **Base runs:** three per scenario on the old version, with uniform operator choice, first "hour" only.
  Each trial takes its prior from one of them in rotation.
- **Priors:**
  - capped transfer prior: mean p̂_a, weight min(N, n_a);
  - calibrated fresh: all operators at the mean of p̂, weight N;
  - shuffled transfer: p̂ permuted per trial;
  - fresh Beta(1,1).
- **Batching:** within a batch of B executions, every execution samples from the posterior as it stood
  at the start of the batch.
- **Regret:** measured against a greedy oracle that plays the operator with the highest current true
  rate, simulated as its own campaign.
- **Metrics:**
  - successes at 15m/1h/4h;
  - regret;
  - best-operator share (fraction of executions on the currently best operator);
  - share of batches to T;
  - P(T | data) for model-comparison policies;
  - total-variation distance between two posteriors' recommendation distributions. Runs 1–4 compared
    **Beta(1,1) fresh vs transfer**; from run 5 on it compares **calib vs transfer**, the pair the
    controller weighs (`tv_pair` in `run_policy`).
- **Inherited-corpus level (run 5+):** `--level L` multiplies every v+1 rate by L, on top of any
  scenario-specific level (saturation's 0.2). It stands in for starting v+1 from an inherited corpus,
  where everything succeeds less often. Runs 1–4 used L = 1.
- **Seeds:** from run 5 on, seed = `bandit_sim.scenario_seed(name)` (CRC32 of the scenario name), so
  a scenario reproduces whatever else is in the run. Runs 1–4 used 1000 + the scenario's *position in
  the `--scenarios` list*, which is why, for example, close_no_shift numbers differ slightly between
  run 2 and runs 3–4, and why run 5's level-1 numbers differ slightly from run 4. Within a run, all
  policies on a scenario share base runs (common random numbers).

## Policies (`bandit_sim.POLICIES`)

| name | models | how the model is chosen |
|---|---|---|
| `fresh`, `calib`, `shuffled`, `transfer` | one | fixed |
| `adaptive` | fresh, transfer | previous plan's two-level Thompson sampling; only the chosen model gets credit; discounted (γ) |
| `mix50` | fresh, transfer | coin flip per batch |
| `mix50_cal` | calib, transfer | coin flip per batch: the matched control for `bmcs_cal` (run 5+) |
| `mix50_cal_r` | calib, transfer | coin flip per batch, acting with the prior rescaled to the fitted c: the matched control for `bmcs_cal_r` (run 9). P(T) is still computed and logged, but not used |
| `bmc` / `bma` | fresh Beta(1,1), transfer | posterior model probability from the Beta-Binomial marginal likelihood on all shared evidence; bmc samples a model per batch, bma a mixture component per execution |
| `bmc_cal` / `bma_cal` | calib, transfer | same, but the competing hypothesis has the right scale and no ranking |
| `bmc_calw` / `bma_calw` | calib with weight 50, transfer | weak-calibrated variant (worse in a quick check; dropped) |
| **`bmcs_cal`** | calib, transfer | **scale-invariant** comparison: each hypothesis is "rates = c × prior mean", with log c marginalised on 61 grid points over [1/30, 30]. **This is the plan's new controller.** |
| **`bmcs_cal_r`** | calib, transfer | as `bmcs_cal`, and the chosen model also *acts* with its prior rescaled to the posterior-mean c under that hypothesis (empirical Bayes). Rejected in run 4 at level 1; **the recommended controller from runs 5–7**, when v+1 starts lower than v |
| `bmcs_cf` | calib, transfer (+ fresh) | as `bmcs_cal`, but when T is not chosen it acts with Beta(1,1) instead of calib (run 5; dropped) |

## Scenarios (`bandit_sim.make_scenario`)

| name | old rates | shift to new version |
|---|---|---|
| `no_shift` | 1e-2, 5e-3, 3e-3, 2e-3, 1e-3, 5e-4, 2e-4, 1e-4 | identical |
| `mild_shift` | same | best unchanged; others × lognormal(0, 0.7), capped below the best |
| `reversal` | same | old best ↔ 7th (1e-2 ↔ 2e-4) |
| `saturation` | same | same ranking, all rates × 0.2 (stand-in for starting from an inherited corpus) |
| `close_no_shift` | 4e-3, 3.5e-3, 3e-3, 2.5e-3, 1.5e-3, 1e-3, 5e-4, 2e-4 | identical |
| `close_reversal` | same (close) | old best drops to 5th, old 4th becomes best (the new best was already in the old top 4) |
| `late_riser` | same (close) | op 3 starts at 1.5e-3 but decays 10× slower (τ = 0.5); it overtakes op 0 at ~28 min |
| `depletion` | same (close) | finite coverage pools on v+1: [30, 400, 400, 400, 300, 200, 100, 50] successes |
| `rank_<ρ>_<d>` | OLD_RATES | v+1 rates are a permutation of the old ones with rank correlation ≈ ρ (Gaussian copula on normal scores, draw d; same noise for every ρ). Only the ranking changes, not the set of rates (run 6) |
| `rankc_<ρ>_<d>` | CLOSE_RATES | same on the close rates |
| `drift_<swap\|geom>_<late\|early>` | OLD_RATES, per-operator τ on v (`DRIFT_TAU`) | v's ranking changes during the base run. v+1 (uniform τ) is a permutation of OLD_RATES ranked like v at the end of the base run (`late`) or at its start (`early`) (run 11) |

## Sanity checks

- **N = 0:** transfer and fresh produce identical results with the same seed.
- **Statistics:** the hand-written Mann–Whitney U matches `scipy.stats.mannwhitneyu` (asymptotic, no
  continuity correction) to about 15 decimal places.
- **Regression:** after generalising the rate model for runs 2+, `no_shift` reproduced run 1 exactly
  (fresh 811.5, transfer 853.5 median at 1h).
- **Prior check (plan section 6):** under no shift, transfer must beat both controls. It does at
  N=500 in run 1 (vs calib A12 0.71, p=0.009; vs shuffled A12 0.67, p=0.02) and at N=5000 in run 2.

## Run log

All cells are median successes over 30 trials unless noted. A12 = P(row policy > other); p is the
two-sided Mann–Whitney U, Holm-corrected within a table in `summary.md` and **unadjusted** where
marked. Full tables (IQRs, 15m/4h, regret, best-op share, share to T, divergence) are in each
`summary.md`.

### Run 1: previous plan, original scenarios (`results/original/`)

```
../.venv/bin/python run_stage1.py --R 30 --T 1000000
```

This ran 4 scenarios × 6 policies at N=500, plus sweeps of N ∈ {0, 50, 500, 5000} (adaptive and
transfer), γ ∈ {1, 0.98, 0.95} and B ∈ {64, 256, 1024} (adaptive). Run time 3m40s.

Successes at 1h, N=500:

| scenario | fresh | calib | shuffled | transfer | adaptive | mix50 |
|---|---|---|---|---|---|---|
| no_shift | 812 | 822 | 836 | 854 | 834 | 822 |
| mild_shift | 804 | 850 | 843 | 851 | 830 | 816 |
| reversal | 822 | 830 | 836 | 821 | 819 | 810 |
| saturation | 133 | 125 | 118 | 135 | 128 | 132 |

N sweep, successes at 1h (adaptive / transfer):

| scenario | N=0 | N=50 | N=500 | N=5000 |
|---|---|---|---|---|
| no_shift | 816 / 806 | 806 / 820 | 834 / 854 | 846 / 892 |
| mild_shift | 823 / 802 | 809 / 824 | 830 / 851 | 866 / 898 |
| reversal | 820 / 809 | 812 / 814 | 819 / 821 | **821 / 419** |
| saturation | 124 / 132 | 127 / 130 | 128 / 135 | 146 / 154 |

Findings:

- **N=500 is too weak to matter.** All policies are within ~5% of each other. Under reversal even
  transfer recovers in ~1.5 min: every policy reaches a 50% best-op share in 1.3–1.7 min.
- **The bandit doesn't learn.** `adaptive` loses to `transfer` under no shift (A12 0.28, p=0.019) and
  mild shift (A12 0.29, p=0.029). Its share of batches to T is 0.78 at first, falling to 0.5 within
  an hour. The two models' recommendation distributions converge (TV < 0.1 by 15–50 min).
- **N=5000 reveals the hypothesis.**
  - Transfer gains about 10% when the ranking holds and collapses under reversal (419 vs fresh 810).
  - Adaptive avoids the collapse (821, A12 1.00 vs transfer). Its early share to T drops to 0.42.
  - But adaptive captures only about a third of the upside in no shift and mild shift
    (A12 0.13 and 0.23 vs transfer).
- **γ and B have little effect.** γ=1.0 is slightly best everywhere, and B=64/256/1024 are within
  noise.

### Run 2: harder scenarios (`results/hard/`)

```
../.venv/bin/python run_stage1.py --R 30 --T 1000000 --scenarios close_no_shift,close_reversal,late_riser,depletion \
    --Ns 500,5000 --sweeps gamma --out results/hard
```

Run time 2m31s.

Successes at 1h:

| scenario | N | fresh | calib | shuffled | transfer | adaptive | mix50 |
|---|---|---|---|---|---|---|---|
| close_no_shift | 500 | 290 | 295 | 288 | 296 | 300 | 295 |
| close_reversal | 500 | 274 | 288 | 290 | 294 | 286 | 284 |
| late_riser | 500 | 302 | 303 | 306 | 299 | 302 | 306 |
| depletion | 500 | 223 | 216 | 216 | 222 | 220 | 226 |
| close_no_shift | 5000 | 282 | 304 | 304 | **330** | 312 | 303 |
| close_reversal | 5000 | 278 | 301 | 288 | **313** | 300 | 296 |
| late_riser | 5000 | 301 | 305 | 316 | **342** | 310 | 304 |
| depletion | 5000 | 218 | 216 | 209 | **232** | 210 | 217 |

Findings:

- **At N=500, nothing differs significantly**, in any scenario or comparison.
- **At N=5000, transfer is best or tied-best in all 4 scenarios.** It beats shuffled transfer
  everywhere (A12 0.72–0.80, p ≤ 0.006), so the old ranking carries real information.
- **The bandit is never better than transfer, and is significantly worse in two scenarios:**
  late_riser (A12 0.21, p < 0.001) and depletion (A12 0.28, p = 0.014). It is never different from
  mix50. Its share to T is 0.75–0.8 for the first 15 min, then 0.5.
- **Diagnosis:** there's about one success per 256-execution batch, credited only to the chosen
  model. Telling a 10–30% rate difference apart needs ~100 batches per model (~10+ min), and by then
  the models have converged on shared evidence.
- **close_reversal is benign.** The new best was already in the old top 4 and the bottom 4 stay bad,
  so the old ranking is still mostly right. Transfer even recovers fastest: a median of 3.6 min to
  reach 50% best-op share, vs fresh 9.0, at N=5000.
- **late_riser hurts everyone.** At the overtaking point (~28 min), best-op share drops to about 0.05
  for all policies. Fresh adapts fastest and transfer slowest, so transfer's 1h lead (342 vs 301) is
  gone by 4h (634 vs 631). This is operator-level staleness in the shared counts, which no prior
  choice fixes.
- **Discounting doesn't help.** γ=1.0 is best or tied in 7 of 8 configurations, even in late_riser.

### Run 3: Bayesian model comparison (`results/bmc/`)

```
../.venv/bin/python run_stage1.py --R 30 --T 1000000 \
    --scenarios no_shift,mild_shift,reversal,saturation,close_no_shift,close_reversal,late_riser,depletion \
    --Ns 500,5000 --sweeps "" --policies fresh,calib,shuffled,transfer,adaptive,mix50,bmc,bmc_cal,bma_cal \
    --focus bmc_cal,bma_cal,adaptive --out results/bmc
../.venv/bin/python compare_table.py results/bmc --focus bmc_cal --against transfer,calib,fresh,adaptive
```

Run time 6m39s. It was preceded by a one-off quick check (20 trials, T=400k, N=5000). In that check:
- `bmc` with Beta(1,1) was confident in T after 10 batches even under reversal (P(T)=0.999), and
  collapsed like transfer (58 vs fresh 123).
- Calibrated alternatives fixed this; the weak-calibrated one (`*_calw`) was worse under reversal
  (247–257 vs 328–338).

Successes at 1h, N=5000:

| scenario | fresh | calib | shuffled | transfer | adaptive | mix50 | bmc | bmc_cal | bma_cal |
|---|---|---|---|---|---|---|---|---|---|
| no_shift | 817 | 892 | 635 | 892 | 846 | 840 | 888 | 896 | 892 |
| mild_shift | 812 | 866 | 748 | 898 | 866 | 820 | 896 | 901 | 896 |
| reversal | 810 | 882 | 467 | **419** | 821 | 798 | **406** | 876 | 884 |
| saturation | 128 | 103 | 80 | 154 | 146 | 128 | 154 | **119** | 125 |
| close_no_shift | 285 | 306 | 292 | 325 | 317 | 306 | 334 | 328 | 320 |
| close_reversal | 288 | 318 | 296 | 302 | 294 | 288 | 298 | 306 | 300 |
| late_riser | 300 | 308 | 297 | 332 | 314 | 310 | 327 | 329 | 332 |
| depletion | 217 | 218 | 216 | 230 | 225 | 220 | 223 | 228 | 220 |

Shuffled transfer at N=5000 is much worse than everything else in the original scenarios (no_shift
635, saturation 80): a strong prior with the wrong ranking is actively harmful. At N=500 all policies are within a few percent (see
`compare_table.py results/bmc`).

Findings:

- **`bmc` (alternative = Beta(1,1)) is just transfer.** It matches transfer-only everywhere,
  including the reversal collapse (406). Beta(1,1) predicts ~50% success, so every failure counts
  heavily against it and T wins the comparison on scale alone.
- **`bmc_cal` (alternative = calibrated fresh) works except under pure scale shift.**
  - At N=5000 it matches transfer in 6 of 8 scenarios (A12 0.47–0.51).
  - Reversal: 876 vs 419 (A12 1.00); P(T) falls to 0.04 within 1 min and 0 by 1h.
  - It beats `adaptive` in 5 of 8 (p ≤ 0.005).
- **Failure: saturation.** bmc_cal scores 119 vs transfer 154 (A12 0.06, p < 0.001); P(T) falls to
  ~0.2.
  - Cause: the ranking is unchanged but all rates are 5× lower. T predicts ~0.0036 for the most-played
    operator, while calib predicts ~0.0010 against an actual ~0.0007.
  - So calib is "more accurate" while knowing nothing about the ranking. Accurate isn't the same as
    useful.
- **The scale prior does much of the work.** Calib alone gets most of the gain over Beta(1,1) fresh
  (892 vs 817 under no shift). Transfer's extra gain from the ranking is about 0–8% at 1h.
- **Late drift.** Under no shift P(T) slides back to ~0.5 by 4h, because the first-hour rates
  gradually stop matching the decaying rates. By then the models have converged, so it costs
  nothing.
- **Correction to an earlier claim.** Here `adaptive` beats `mix50` in 3 of 16 configurations:
  mild_shift, reversal and saturation at N=5000 (A12 0.70–0.75, p ≤ 0.006). The earlier "never
  different from mix50" holds only for the 12 configurations of runs 1–2.

### Run 4: scale-invariant model comparison (`results/bmcs/`)

```
../.venv/bin/python run_stage1.py --R 30 --T 1000000 \
    --scenarios no_shift,mild_shift,reversal,saturation,close_no_shift,close_reversal,late_riser,depletion \
    --Ns 500,5000 --sweeps "" --policies fresh,calib,transfer,adaptive,bmc_cal,bmcs_cal,bmcs_cal_r \
    --focus bmcs_cal,bmcs_cal_r --out results/bmcs
../.venv/bin/python compare_table.py results/bmcs --focus bmcs_cal --against transfer,calib,fresh,bmc_cal,adaptive
```

Run time 6m02s. It was preceded by a one-off quick check (20 trials, T=400k, N=5000). That check
showed saturation fixed (P(T) → 0.93) and reversal still caught (340 vs transfer 158), with
`bmcs_cal_r` hurting both reversals.

Successes at 1h:

| scenario | N | fresh | calib | transfer | adaptive | bmc_cal | **bmcs_cal** | bmcs_cal_r |
|---|---|---|---|---|---|---|---|---|
| no_shift | 500 | 812 | 822 | 854 | 834 | 849 | 849 | 871 |
| mild_shift | 500 | 804 | 850 | 851 | 830 | 850 | 844 | 852 |
| reversal | 500 | 822 | 830 | 821 | 819 | 834 | 834 | 842 |
| saturation | 500 | 133 | 125 | 135 | 128 | 131 | 127 | 151 |
| close_no_shift | 500 | 296 | 300 | 300 | 290 | 291 | 294 | 304 |
| close_reversal | 500 | 296 | 286 | 290 | 286 | 299 | 304 | 305 |
| late_riser | 500 | 294 | 302 | 303 | 288 | 296 | 306 | 309 |
| depletion | 500 | 215 | 216 | 224 | 221 | 218 | 224 | 228 |
| no_shift | 5000 | 817 | 892 | 892 | 846 | 896 | 886 | 876 |
| mild_shift | 5000 | 812 | 866 | 898 | 866 | 901 | 900 | 884 |
| reversal | 5000 | 810 | 882 | **419** | 821 | 876 | **870** | 822 |
| saturation | 5000 | 128 | 103 | 154 | 146 | **119** | **147** | 162 |
| close_no_shift | 5000 | 285 | 306 | 325 | 317 | 328 | 335 | 320 |
| close_reversal | 5000 | 288 | 318 | 302 | 294 | 306 | 308 | 290 |
| late_riser | 5000 | 300 | 308 | 332 | 314 | 329 | 334 | 320 |
| depletion | 5000 | 217 | 218 | 230 | 225 | 228 | 224 | 223 |

`bmcs_cal` at N=5000, 1h (A12 / unadjusted p), and mean P(T) at 1 / 15 / 60 / 239 min:

| scenario | vs transfer | vs calib | vs fresh | vs bmc_cal | vs adaptive | P(T) |
|---|---|---|---|---|---|---|
| no_shift | 0.51 / 0.93 | 0.57 / 0.36 | 0.94 / <0.001 | 0.49 / 0.87 | 0.86 / <0.001 | 0.78 0.66 0.59 0.97 |
| mild_shift | 0.51 / 0.86 | 0.76 / 0.001 | 0.98 / <0.001 | 0.52 / 0.77 | 0.82 / <0.001 | 0.76 0.66 0.64 0.97 |
| reversal | 1.00 / <0.001 | 0.47 / 0.70 | 0.87 / <0.001 | 0.45 / 0.54 | 0.86 / <0.001 | 0.02 0.00 0.00 0.02 |
| saturation | 0.35 / 0.044 | 0.97 / <0.001 | 0.78 / <0.001 | 0.89 / <0.001 | 0.53 / 0.67 | 0.68 0.94 0.95 0.93 |
| close_no_shift | 0.49 / 0.90 | 0.72 / 0.003 | 0.91 / <0.001 | 0.52 / 0.80 | 0.75 / 0.001 | 0.67 0.73 0.90 0.93 |
| close_reversal | 0.57 / 0.35 | 0.47 / 0.67 | 0.71 / 0.005 | 0.57 / 0.37 | 0.67 / 0.021 | 0.47 0.54 0.74 0.80 |
| late_riser | 0.47 / 0.64 | 0.73 / 0.002 | 0.79 / <0.001 | 0.49 / 0.85 | 0.68 / 0.019 | 0.60 0.66 0.88 0.94 |
| depletion | 0.47 / 0.71 | 0.62 / 0.098 | 0.62 / 0.12 | 0.45 / 0.50 | 0.51 / 0.87 | 0.68 0.69 0.89 0.88 |

Findings:

- **`bmcs_cal` at N=5000 is the best controller so far.**
  - It ties transfer in 7 of 8 scenarios (A12 0.47–0.57).
  - It avoids the reversal collapse (870 vs 419); P(T) is 0.02 within 1 min.
  - Saturation is mostly fixed: 147 vs transfer 154 (A12 0.35, p=0.044 unadjusted, wouldn't survive
    correction), up from bmc_cal's 119. P(T) rises to 0.94 by 15 min.
  - It is never significantly worse than `bmc_cal`, and beats `adaptive` in 6 of 8.
- **It is less decisive mid-campaign.** Without scale to separate the priors, P(T) under no shift
  sits at 0.59–0.66 mid-campaign, vs 1.00 for bmc_cal, with no measurable cost in successes.
- **`bmcs_cal_r` (acting with a rescaled prior) is mixed.**
  - At N=500 it's the best policy, significantly beating transfer in saturation (151 vs 135,
    A12 0.76) and reversal (A12 0.72). Rescaling corrects the optimism of a too-high prior.
  - At N=5000 it's significantly worse than transfer and bmcs_cal in several scenarios
    (A12 0.31–0.36): rescaling a strong prior dilutes the ranking advantage.
  - Not adopted.
- **At N=500 all policies remain within noise**, apart from `bmcs_cal_r`.

### Run 5: inherited-corpus level (`results/level1/`, `results/level0.5/`, `results/level0.2/`)

```
for L in 1 0.5 0.2; do
  ../.venv/bin/python run_stage1.py --R 30 \
      --scenarios no_shift,mild_shift,reversal,saturation,close_no_shift,close_reversal,late_riser,depletion \
      --Ns 5000 --sweeps "" --policies fresh,calib,transfer,mix50_cal,bmcs_cal,bmcs_cf,bmcs_cal_r \
      --focus bmcs_cal,bmcs_cf --level $L --out results/level$L
done
../.venv/bin/python compare_table.py results/level0.5 --focus bmcs_cf --against transfer,calib,fresh,bmcs_cal,bmcs_cal_r
```

This is next step 2 from the previous list, run together with steps 4 (`mix50_cal`), 5 (C-vs-T
divergence) and 7 (name seeds). Every v+1 rate is multiplied by L. In saturation the multiplier
stacks on its own 0.2, so saturation at L = 0.2 starts at 0.04 × the old rates. It was run twice: first
without `bmcs_cf` / `bmcs_cal_r`, then with them. The policies common to both runs reproduced
exactly, as name seeds should.

Successes at 1h, N=5000:

| L | scenario | fresh | calib | transfer | mix50_cal | bmcs_cal | bmcs_cf | **bmcs_cal_r** |
|---|---|---|---|---|---|---|---|---|
| 1 | no_shift | 828 | 864 | 898 | 889 | 886 | 874 | 888 |
| 1 | mild_shift | 805 | 858 | 894 | 897 | 888 | 880 | 894 |
| 1 | reversal | 822 | 872 | 410 | 819 | 867 | 818 | 846 |
| 1 | saturation | 133 | 106 | 147 | 124 | 148 | 146 | 163 |
| 1 | close_no_shift | 288 | 300 | 345 | 324 | 336 | 327 | 320 |
| 1 | close_reversal | 296 | 309 | 300 | 298 | 318 | 296 | 301 |
| 1 | late_riser | 300 | 323 | 336 | 325 | 322 | 326 | 319 |
| 1 | depletion | 210 | 224 | 238 | 222 | 232 | 226 | 225 |
| 0.5 | no_shift | 368 | 416 | 438 | 428 | 428 | 420 | 434 |
| 0.5 | mild_shift | 379 | 404 | 440 | 426 | 443 | 428 | 425 |
| 0.5 | reversal | 375 | 402 | 189 | 357 | 402 | 378 | 408 |
| 0.5 | saturation | 50 | 39 | 64 | 49 | 61 | 60 | 78 |
| 0.5 | close_no_shift | 136 | 128 | 153 | 131 | 138 | 146 | 148 |
| 0.5 | close_reversal | 138 | 125 | 143 | 137 | 136 | 136 | 143 |
| 0.5 | late_riser | 140 | 138 | 159 | 146 | 152 | 150 | 152 |
| 0.5 | depletion | 110 | 106 | 122 | 112 | 116 | 113 | 118 |
| 0.2 | no_shift | 126 | 108 | 150 | 131 | 144 | 147 | 164 |
| 0.2 | mild_shift | 130 | 116 | 156 | 132 | 148 | 144 | 165 |
| 0.2 | reversal | 125 | 110 | 62 | 81 | 104 | 118 | 148 |
| 0.2 | saturation | 18 | 12 | 23 | 18 | 21 | 19 | 25 |
| 0.2 | close_no_shift | 48 | 42 | 54 | 46 | 50 | 51 | 52 |
| 0.2 | close_reversal | 46 | 41 | 54 | 46 | 46 | 49 | 54 |
| 0.2 | late_riser | 53 | 46 | 58 | 50 | 55 | 50 | 62 |
| 0.2 | depletion | 44 | 38 | 50 | 42 | 44 | 45 | 47 |

`bmcs_cal` at 1h vs transfer / calib / fresh (A12, unadjusted p<0.05 marked *), from the first pass:

| scenario | L=1 | L=0.5 | L=0.2 |
|---|---|---|---|
| no_shift | 0.39 / 0.71* / 0.91* | 0.34* / 0.64 / 0.99* | 0.40 / 0.93* / 0.83* |
| reversal | 1.00* / 0.47 / 0.81* | 1.00* / 0.40 / 0.72* | 0.95* / 0.41 / **0.25*** |
| saturation | 0.43 / 0.88* / 0.74* | 0.40 / 0.92* / 0.70* | 0.38 / 0.86* / 0.71* |
| close_no_shift | 0.35* / 0.74* / 0.92* | **0.27*** / 0.69* / 0.57 | 0.38 / 0.74* / 0.61 |
| close_reversal | 0.63 / 0.58 / 0.77* | **0.30*** / 0.66* / 0.44 | **0.28*** / 0.59 / 0.46 |
| late_riser | 0.32* / 0.51 / 0.78* | 0.39 / 0.77* / 0.73* | 0.42 / 0.75* / 0.55 |

Findings:

- **Calibrated fresh is the wrong fallback once v+1 starts lower.** Calib keeps the *old* scale with
  weight N. When every rate drops, it is over-optimistic about every operator and spends a long time
  pulling them down. At L=0.2 calib is below Beta(1,1) fresh in every scenario: no_shift 108 vs 126,
  reversal 110 vs 125.
- **The comparison still works, but the action under it suffers.** `bmcs_cal`'s P(T) still drops to
  ≈0.05 under reversal at every level. The scale-invariant evidence doesn't care about the level. But
  when it rejects T it acts with the miscalibrated calib prior, so at L=0.2 under reversal it gets 104,
  significantly below fresh's 125 (A12 0.25).
- **Transfer is also miscalibrated, but its ranking still pays.** At low levels transfer beats calib
  even in close_reversal (L=0.5: 143 vs 125, A12 0.73 in run 8). There, the new best was already in
  the old top 4. Run 4's "close_reversal: transfer ≈ calib" held only at L=1.
- **`bmcs_cf` (act with Beta(1,1) when T is rejected) doesn't fix it.** It recovers some reversal
  ground at L=0.2 (118), but it is significantly below `bmcs_cal` under reversal at L=1 and L=0.5
  (A12 0.17 and 0.32), and never significantly better than `bmcs_cal_r`. Dropped.
- **`bmcs_cal_r` (act with the prior rescaled to the fitted c) is the best controller at L ≤ 0.5.**
  - At L ≤ 0.5 it is never significantly worse than any fixed prior in any scenario.
  - It is significantly better than the best fixed prior in no_shift and reversal at L=0.2
    (A12 0.77 and 0.70), and in saturation at L=0.5 (78 vs transfer 64, A12 0.81). Under reversal at
    L=0.2 it gets 148 vs fresh 125, calib 110 and transfer 62.
  - At L=1 it is significantly below transfer in close_no_shift, late_riser and depletion
    (A12 0.25–0.32), and below calib under reversal (0.27). It is 1–5% below `bmcs_cal` in five of
    eight scenarios, as in run 4. The exception is saturation, an effective level of 0.2, where it is
    best.
- **`mix50_cal` is a weak control.**
  - Under reversal it is below `bmcs_cal` at every level (A12 0.77–0.82).
  - At L=0.2 it is also below in no_shift, mild_shift and close_no_shift (A12 0.74–0.76). Elsewhere
    it ties.
  - `bmcs_cal_r` beats it significantly in 12 of 24 scenario × level cells.
  - Evidence-weighing therefore adds value over mixing mainly by avoiding the bad model.
  - **Run 9 qualifies this:** much of `bmcs_cal_r`'s margin over `mix50_cal` comes from rescaling,
    not from evidence-weighing.

### Run 6: rank-correlation sweep (`results/rank_L0.5/`, `results/rank_L1/`, `results/rank_L0.2/`)

```
../.venv/bin/python rank_sweep.py --level 0.5 --draws 6 --policies fresh,calib,transfer,bmcs_cal,bmcs_cal_r --out results/rank_L0.5
../.venv/bin/python rank_sweep.py --level 1   --draws 3 --policies fresh,calib,transfer,bmcs_cal,bmcs_cal_r --out results/rank_L1
../.venv/bin/python rank_sweep.py --level 0.2 --draws 3 --policies fresh,calib,transfer,bmcs_cal,bmcs_cal_r --out results/rank_L0.2
```

**Design.**
- ρ ∈ {1, 0.8, 0.5, 0.2, 0, −0.5, −1}, on both OLD_RATES (`rank_`) and CLOSE_RATES (`rankc_`).
- That gives 84 scenarios at L=0.5 (6 draws per ρ) and 42 at each of L=1 and L=0.2 (3 draws), each
  with 30 trials at N=5000.
- Run time: about 50 minutes for all three.
- With K=8 the realised Spearman correlation spreads widely around the nominal ρ. Nominal 0.5 gave
  −0.43 to 0.81. `summary.md` therefore also lists every draw sorted by realised Spearman, and
  `rank_sweep.png` plots against it.

Per-ρ medians at L=0.5 (successes at 1h; "kept" = draws where the old best operator is still best):

| set | ρ | kept | fresh | calib | transfer | bmcs_cal | bmcs_cal_r | bmcs_cal P(T) at 1h |
|---|---|---|---|---|---|---|---|---|
| rank | 1 | 6/6 | 380 | 403 | 440 | 430 | 434 | 0.96 |
| rank | 0.8 | 3/6 | 380 | 406 | 404 | 414 | 420 | 0.67 |
| rank | 0.5 | 1/6 | 382 | 407 | 378 | 399 | 405 | 0.49 |
| rank | 0.2 | 1/6 | 376 | 407 | 402 | 398 | 406 | 0.37 |
| rank | 0 | 1/6 | 380 | 409 | 281 | 399 | 409 | 0.26 |
| rank | −0.5 | 1/6 | 378 | 402 | 265 | 402 | 411 | 0.14 |
| rank | −1 | 0/6 | 383 | 412 | 255 | 412 | 406 | 0.00 |
| rankc | 1 | 6/6 | 136 | 132 | 153 | 144 | 155 | 0.89 |
| rankc | 0.8 | 3/6 | 132 | 131 | 150 | 140 | 148 | 0.74 |
| rankc | 0.5 | 1/6 | 134 | 129 | 147 | 137 | 144 | 0.57 |
| rankc | 0.2 | 1/6 | 135 | 132 | 135 | 134 | 142 | 0.35 |
| rankc | 0 | 1/6 | 132 | 129 | 130 | 129 | 142 | 0.30 |
| rankc | −0.5 | 1/6 | 133 | 132 | 110 | 126 | 140 | 0.07 |
| rankc | −1 | 0/6 | 135 | 131 | 94 | 130 | 137 | 0.01 |

Each controller against the best *fixed* prior for each draw, chosen in hindsight from transfer,
calib and fresh. Columns: ratio of medians, median [min]; then draws where the controller is
significantly worse / better (unadjusted MWU p<0.05):

| L | set | bmcs_cal ratio | worse / better | bmcs_cal_r ratio | worse / better |
|---|---|---|---|---|---|
| 1 | rank (21 draws) | 1.00 [0.83] | 2 / 0 | 0.97 [0.85] | 14 / 0 |
| 1 | rankc (21) | 0.98 [0.91] | 4 / 0 | 0.95 [0.86] | 13 / 0 |
| 0.5 | rank (42) | 0.98 [0.92] | 10 / 0 | 0.99 [0.92] | 4 / 1 |
| 0.5 | rankc (42) | 0.94 [0.87] | 12 / 0 | 1.01 [0.95] | 0 / 5 |
| 0.2 | rank (21) | 0.89 [0.75] | 16 / 0 | **1.10 [0.99]** | 0 / 16 |
| 0.2 | rankc (21) | 0.91 [0.80] | 9 / 0 | **1.05 [0.94]** | 0 / 6 |

Findings:

- **What matters is whether the old top operators stay on top, not the overall rank correlation.**
  - Wide rates (`rank`, L=0.5): transfer is +6–10% over calib whenever the old best stays best. It
    is −25% to −50% when the old best falls to the bottom half, even at Spearman 0.3–0.55 (for
    example rank_0.8_4 at Spearman 0.55: T/C = 0.51). The in-between draws, where the old best drops
    but stays near the top, give T/C ≈ 0.92–0.99.
  - Close rates (`rankc`): transfer still helps (T/C 1.09–1.22) down to Spearman ≈ 0.4, and hurts only
    below about −0.4, by at most −33%.
- **The comparison switches at the right place.** `bmcs_cal`'s P(T) at 1h tracks the realised
  correlation: ≈0.9–0.96 at Spearman 1.
  - At L=0.5, in every draw where transfer loses more than 25% to calib, P(T) ≤ 0.25, and below 0.1 in all but
    two.
  - `bmcs_cal` beats transfer there with A12 0.91–1.00.
- **Where it goes wrong is mild.** Take the wide-rate draws where the old best drops but stays near
  the top (T/C ≈ 0.92–0.99). There P(T) stays 0.4–0.86, and `bmcs_cal` loses to calib (A12
  0.30–0.34), by at most 8%.
- **Under an inherited corpus, `bmcs_cal_r` is the one to use.** Across 84 draws at L=0.5 it is
  within 1% of the hindsight-best fixed prior in median. It is significantly worse in only 4 and
  better in 6. At L=0.2 it is never worse and better in 22 of 42. `bmcs_cal` falls 9–11% short at
  L=0.2. At L=1 the order flips: `bmcs_cal_r` is 3–5% below and significantly worse in 27 of 42.

### Run 7: finer N sweep (`results/nsweep_L1/`, `results/nsweep_L0.5/`, `results/nsweep_L0.2/`)

```
for L in 1 0.5 0.2; do
  ../.venv/bin/python run_stage1.py --scenarios no_shift,mild_shift,reversal,saturation,close_no_shift,close_reversal,late_riser,depletion \
      --Ns 1000,2000,5000,20000 --sweeps "" --policies calib,transfer,bmcs_cal,bmcs_cal_r --focus bmcs_cal_r \
      --level $L --out results/nsweep_L$L
done
```

The first attempt crashed in plotting because `fresh` was not among the policies. That is fixed in
`run_stage1.py`. Runs 7 and 8 together took about 30 minutes.

Successes at 1h, L=0.5 (calib / transfer / bmcs_cal / **bmcs_cal_r**):

| scenario | N=1000 | N=2000 | N=5000 | N=20000 |
|---|---|---|---|---|
| no_shift | 396 / 412 / 407 / **422** | 396 / 426 / 414 / **431** | 416 / 438 / 428 / **434** | 414 / 440 / 438 / **430** |
| mild_shift | 380 / 410 / 404 / **414** | 407 / 428 / 422 / **421** | 404 / 440 / 443 / **425** | 417 / 444 / 431 / **438** |
| reversal | 390 / 378 / 382 / **396** | 388 / 308 / 396 / **404** | 402 / 189 / 402 / **408** | 410 / 143 / 404 / **390** |
| saturation | 46 / 61 / 54 / **70** | 44 / 62 / 52 / **71** | 39 / 64 / 61 / **78** | 31 / 75 / 70 / **80** |
| close_no_shift | 134 / 136 / 140 / **146** | 133 / 146 / 139 / **146** | 128 / 153 / 138 / **148** | 126 / 154 / 158 / **152** |
| close_reversal | 136 / 130 / 140 / **141** | 138 / 140 / 136 / **144** | 125 / 143 / 136 / **143** | 125 / 134 / 122 / **132** |
| late_riser | 144 / 146 / 146 / **154** | 140 / 148 / 150 / **146** | 138 / 159 / 152 / **152** | 127 / 166 / 165 / **158** |
| depletion | 112 / 108 / 114 / **117** | 110 / 117 / 108 / **118** | 106 / 122 / 116 / **118** | 104 / 121 / 120 / **116** |

Transfer's reversal collapse vs N (successes at 1h, transfer / bmcs_cal_r):

| L | N=1000 | N=2000 | N=5000 | N=20000 |
|---|---|---|---|---|
| 1 | 824 / 846 | 540 / 856 | 410 / 846 | 366 / 819 |
| 0.5 | 378 / 396 | 308 / 404 | 189 / 408 | 143 / 390 |
| 0.2 | 114 / 138 | 93 / 146 | 62 / 148 | 40 / 144 |

Findings:

- **Transfer's gain and its risk both grow with N.** Where the ranking holds, transfer keeps gaining
  up to N=20000: saturation at L=0.5 goes 61 → 75, late_riser 146 → 166. Its reversal collapse
  deepens over the same range, at L=0.5 from 378 to 143.
- **The controller makes N much less critical.**
  - At L=0.5, `bmcs_cal_r` stays within about ±5% across N=1000–20000 in every scenario except
    saturation (70–80).
  - At N=20000 it loses a little under reversal (390) and close_reversal (132), where the stronger
    wrong prior takes longer to undo.
  - The L=1 and L=0.2 tables in `summary.md` show the same shape.
- **N=5000 is fixed for Stage 2.** It is at or near the best N for `bmcs_cal_r` at every level.
  N=20000 helps it slightly in some no-shift-like scenarios but costs under reversal. Most of the
  extra gain above 5000 goes to transfer-only.

### Run 8: power check (`results/power_L0.5/`)

```
../.venv/bin/python run_stage1.py --R 200 --scenarios no_shift,reversal,saturation,close_no_shift,close_reversal \
    --Ns 5000 --sweeps "" --policies fresh,calib,transfer,bmcs_cal,bmcs_cal_r --focus bmcs_cal_r --level 0.5 --out results/power_L0.5
../.venv/bin/python power_check.py results/power_L0.5 --n 10,20,30 --reps 2000 --focus bmcs_cal_r > results/power_L0.5/power_bmcs_cal_r.md
../.venv/bin/python power_check.py results/power_L0.5 --n 10 --reps 2000 --focus bmcs_cal > results/power_L0.5/power_bmcs_cal.md
```

**Method.**
- 200 trials per policy on five key scenarios at L=0.5, N=5000.
- Then 2000 repetitions of drawing n trials per policy without replacement.
- Each repetition runs the Stage 2 comparison family per scenario with Holm correction (5 tests):
  controller vs transfer, calib and fresh; transfer vs calib and fresh.
- Detection means Holm-adjusted p < 0.05 in the stated direction.

Detection rate (`bmcs_cal_r` as controller; full-sample A12 from 200 trials):

| scenario | comparison | full A12 | n=10 | n=20 | n=30 |
|---|---|---|---|---|---|
| reversal | controller > transfer | 0.99 | 1.00 | 1.00 | 1.00 |
| reversal | transfer < calib | 0.00 | 1.00 | 1.00 | 1.00 |
| reversal | controller > fresh | 0.71 | 0.22 | 0.50 | 0.72 |
| no_shift | transfer > calib (ranking matters) | 0.85 | 0.68 | 0.98 | 1.00 |
| no_shift | controller > calib | 0.82 | 0.58 | 0.95 | 1.00 |
| no_shift | controller vs transfer: false "worse" | 0.44 | 0.04 | 0.07 | 0.09 |
| saturation | controller > transfer | 0.67 | 0.17 | 0.46 | 0.61 |
| close_no_shift | transfer > calib | 0.81 | 0.48 | 0.93 | 0.99 |
| close_reversal | transfer > calib | 0.73 | 0.14 | 0.48 | 0.73 |
| close_reversal | controller vs transfer: any difference | 0.50 | 0.01 | 0.00 | 0.02 |

Findings:

- **10 trials detect the headline effect.** Under a damaging shift, the controller beats transfer in
  100% of repetitions.
- **10 trials are not enough for the ranking question.** "Transfer beats calibrated fresh", the core
  of question 1, is detected only 48–68% of the time at A12 ≈ 0.8. At A12 ≈ 0.7 it drops to 14%.
  With 20 trials those rates become 93–98% and 48%.
- **"Indistinguishable from transfer" needs a pre-set equivalence margin.** With 10 trials, a
  non-significant test is the expected outcome even when the controller is slightly worse: no_shift
  A12 0.44 is flagged worse only 4% of the time. The "strong" criterion should state a margin, for
  example A12 ≥ 0.36 or median ratio ≥ 0.95, rather than rely on non-significance.
- **Caveat.** These are simulated variances. Real fuzzing trials are likely noisier, which lowers
  power further.

### Run 9: matched 50/50 control for the rescaled controller (`results/mix_L1/`, `results/mix_L0.5/`, `results/mix_L0.2/`)

```
for L in 1 0.5 0.2; do
  ../.venv/bin/python run_stage1.py --R 30 \
      --scenarios no_shift,mild_shift,reversal,saturation,close_no_shift,close_reversal,late_riser,depletion \
      --Ns 5000 --sweeps "" --policies fresh,calib,transfer,mix50_cal,mix50_cal_r,bmcs_cal_r \
      --focus bmcs_cal_r --level $L --out results/mix_L$L
done
../.venv/bin/python compare_table.py results/mix_L0.5 --focus bmcs_cal_r --against mix50_cal_r,mix50_cal,transfer,calib
```

`mix50_cal_r` is `bmcs_cal_r` with the choice between C and T replaced by a coin flip. Rescaling,
the fitted c and the shared counts are all the same. So the gap between the two measures only what
evidence-weighing adds. Run time 8m50s. The common policies reproduce run 5 exactly.

Successes at 1h; the last column is `bmcs_cal_r` vs `mix50_cal_r` (A12, unadjusted p, and
Holm-adjusted p within each level's 8 scenarios):

| L | scenario | transfer | calib | mix50_cal | **mix50_cal_r** | bmcs_cal_r | bmcs_cal_r vs mix50_cal_r |
|---|---|---|---|---|---|---|---|
| 1 | no_shift | 898 | 864 | 889 | 863 | 888 | 0.71, p=0.005, **Holm 0.038** |
| 1 | mild_shift | 894 | 858 | 897 | 876 | 894 | 0.69, p=0.010, Holm 0.059 |
| 1 | reversal | 410 | 872 | 819 | 800 | 846 | 0.73, p=0.002, **Holm 0.018** |
| 1 | saturation | 147 | 106 | 124 | 162 | 163 | 0.48 |
| 1 | close_no_shift | 345 | 300 | 324 | 309 | 320 | 0.63 |
| 1 | close_reversal | 300 | 309 | 298 | 294 | 301 | 0.52 |
| 1 | late_riser | 336 | 323 | 325 | 315 | 319 | 0.55 |
| 1 | depletion | 238 | 224 | 222 | 229 | 225 | 0.40 |
| 0.5 | no_shift | 438 | 416 | 428 | 424 | 434 | 0.59 |
| 0.5 | mild_shift | 440 | 404 | 426 | 420 | 425 | 0.58 |
| 0.5 | reversal | 189 | 402 | 357 | 384 | 408 | 0.72, p=0.004, **Holm 0.029** |
| 0.5 | saturation | 64 | 39 | 49 | 72 | 78 | 0.66, p=0.029, Holm 0.20 |
| 0.5 | close_no_shift | 153 | 128 | 131 | 146 | 148 | 0.57 |
| 0.5 | close_reversal | 143 | 125 | 137 | 137 | 143 | 0.58 |
| 0.5 | late_riser | 159 | 138 | 146 | 154 | 152 | 0.53 |
| 0.5 | depletion | 122 | 106 | 112 | 120 | 118 | 0.49 |
| 0.2 | no_shift | 150 | 108 | 131 | 158 | 164 | 0.54 |
| 0.2 | mild_shift | 156 | 116 | 132 | 161 | 165 | 0.57 |
| 0.2 | reversal | 62 | 110 | 81 | 142 | 148 | 0.55 |
| 0.2 | saturation | 23 | 12 | 18 | 19 | 25 | 0.65, p=0.049, Holm 0.34 |
| 0.2 | close_no_shift | 54 | 42 | 46 | 55 | 52 | 0.48 |
| 0.2 | close_reversal | 54 | 41 | 46 | 53 | 54 | 0.56 |
| 0.2 | late_riser | 58 | 46 | 50 | 55 | 62 | 0.70, p=0.009, Holm 0.073 |
| 0.2 | depletion | 50 | 38 | 42 | 46 | 47 | 0.54 |

Findings:

- **Evidence-weighing adds a small, consistent edge.** `bmcs_cal_r` is never significantly worse
  than the matched coin flip. Its median is +2% across the 24 cells (range −4.5% to +13%, ignoring
  saturation at L=0.2, where the counts are tiny). It is significantly better in 7 of 24 cells
  unadjusted, and in 3 after Holm within each level.
- **The edge is largest where the old ranking is wrong and v+1 rates aren't much lower.** Under
  reversal it is +6% at L=1 and L=0.5 (846 vs 800, 408 vs 384). At L=1 it is also +2–3% under no
  shift and mild shift.
- **At L=0.2 the coin flip almost catches up, even under reversal (142 vs 148).** At a low fitted
  c, the rescaled transfer prior has a small mean at the same weight W, so it carries little
  confidence in its ranking and is quickly overruled by data. Rescaling therefore both corrects the
  scale and defuses a wrong ranking, and leaves little for the comparison to add. This is also the
  likely reason rescaling costs a little at L=1 (next step 4).
- **Rescaling alone explains most of the gain over the unscaled coin flip.** `mix50_cal_r` beats
  `mix50_cal` significantly in 8 of 24 cells, strongly at L=0.2: A12 0.82–0.91 in no_shift,
  mild_shift, reversal and close_no_shift. It is worse in 3 cells at L=1 (no_shift, mild_shift,
  close_no_shift; A12 0.26–0.31), the same L=1 rescaling cost. Run 5's "`bmcs_cal_r` beats `mix50_cal` in 12 of 24 cells" mostly measured
  rescaling.
- **Stage 2 will have trouble showing "beats 50/50".** The effect size is A12 ≈ 0.7 where it exists.
  Run 8 puts detection for A12 ≈ 0.73 at 14% with 10 trials and 48% with 20, per transition, before
  real-fuzzing noise. A per-transition "adaptive beats 50/50" is therefore unlikely to be shown.
  A pre-registered pooled test across transitions is the realistic way to test it.

### Run 10: consolidated final sweep (`results/final/`)

**Command:**
`final_sweep.py --out results/final`, which takes about 87 minutes on 8 processes. Then
`final_report.py results/final --reps 2000`.

**Grid:**
- 7 policies: fresh, calib, shuffled, transfer, `bmcs_cal`, `bmcs_cal_r` and `mix50_cal_r`.
- 92 transitions per level: the 8 designed scenarios, plus rank and rankc × 7 ρ × 6 draws.
- 3 levels: L ∈ {1, 0.5, 0.2}.
- R=30, N=5000, giving 1,932 cells in all.

**RNG note.** TV logging is off (`tv_every=10**9`). The TV draws share the policy RNG, so trials here
are a fresh realisation of runs 5–9, not a copy, and medians differ by a few percent. For example,
L=1 reversal is adaptive 834 vs 50/50 806, against 846 vs 800 in run 9. The conclusions agree, so
this run also serves as a replication.

**Hindsight-best fixed prior, all 92 cells per level** (median ratio / worst ratio / share within
5% / cells significantly worse–better, unadjusted):

| policy | L=1 | L=0.5 | L=0.2 |
|---|---|---|---|
| fresh | 0.92 / 0.82 / 8% / 86–0 | 0.93 / 0.83 / 29% / 68–0 | 1.00 / 0.59 / 61% / 28–0 |
| calib | 1.00 / 0.70 / 78% / 34–0 | 0.96 / 0.54 / 51% / 40–0 | 0.86 / 0.55 / 7% / 75–0 |
| shuffled | 0.85 / 0.48 / 12% / 72–0 | 0.85 / 0.57 / 15% / 73–0 | 0.78 / 0.46 / 5% / 78–0 |
| transfer | 0.94 / 0.29 / 48% / 49–0 | 0.99 / 0.45 / 52% / 44–0 | 0.97 / 0.36 / 53% / 38–0 |
| adaptive, unscaled (`bmcs_cal`) | 0.985 / 0.74 / 82% / 21–0 | 0.97 / 0.86 / 71% / 28–1 | 0.89 / 0.74 / 22% / 58–0 |
| **adaptive (`bmcs_cal_r`)** | 0.96 / **0.88** / 68% / 53–1 | **0.995 / 0.91 / 97% / 6–5** | **1.09 / 0.91 / 96% / 0–47** |
| 50/50, rescaled (`mix50_cal_r`) | 0.94 / 0.83 / 40% / 79–0 | 0.98 / 0.91 / 85% / 21–1 | 1.07 / 0.92 / 97% / 0–37 |

The best fixed prior is chosen per cell in hindsight from fresh, calib and transfer, all at the old
scale. A rescaled policy can therefore beat it, which is what happens at L=0.2.

Pooled over all 276 cells, the worst / 10th-percentile / median ratios are:

| policy | worst | 10th pct | median |
|---|---|---|---|
| `bmcs_cal_r` | 0.88 | 0.94 | 0.99 |
| `mix50_cal_r` | 0.83 | 0.92 | 0.98 |
| `bmcs_cal` | 0.74 | 0.86 | 0.96 |
| transfer | 0.29 | 0.51 | 0.96 |
| calib | 0.54 | 0.80 | 0.94 |
| fresh | 0.59 | 0.84 | 0.93 |

**Adaptive head-to-head** (W / T / L, significant unadjusted; median ratio):

| adaptive vs | L=1 | L=0.5 | L=0.2 |
|---|---|---|---|
| transfer | 41/27/24, 1.01 | 43/48/1, 1.04 | 68/24/0, 1.14 |
| calib | 13/48/31, 0.98 | 42/45/5, 1.05 | 87/5/0, 1.29 |
| fresh | 63/29/0, 1.05 | 67/25/0, 1.09 | 66/26/0, 1.16 |
| unscaled `bmcs_cal` | 2/68/22, 0.98 | 21/70/1, 1.02 | 81/11/0, 1.20 |
| rescaled 50/50 | 26/66/0, 1.020 | 13/79/0, 1.015 | 6/85/1, 1.009 |

The single loss to 50/50 is `rank_-1_0` at L=0.2 (143 vs 152). That is a full reversal, where the
coin flip follows calib half the time and the controller follows T for a while.

**By regime (rank sweep).** Cells are split by transfer / calib: helps > 1.05, hurts < 0.95. The
adaptive controller's wins over 50/50 come mostly from cells where transfer hurts: 13 at L=1, 5 at
L=0.5 and 2 at L=0.2. Mean P(T) at 1h is 0.66–0.75 where transfer helps and 0.09–0.12 where it hurts.

Where transfer helps, the controller trails transfer at L=1: 0 / 4 / 13, median 1.03× calib against
transfer's 1.09×. This is the rescaling cost. At L ≤ 0.5 it ties or beats transfer.

**Does the ranking itself matter?** (rank sweep, transfer vs calib and vs shuffled)

| L | old best kept? | cells | transfer vs calib W/T/L | transfer vs shuffled W/T/L | median T / C |
|---|---|---|---|---|---|
| 1 | yes | 26 | 22/4/0 | 25/1/0 | 1.04 |
| 1 | no | 58 | 6/4/48 | 11/18/29 | 0.73 |
| 0.5 | yes | 26 | 25/1/0 | 26/0/0 | 1.09 |
| 0.5 | no | 58 | 5/12/41 | 14/14/30 | 0.77 |
| 0.2 | yes | 26 | 24/2/0 | 25/1/0 | 1.33 |
| 0.2 | no | 58 | 12/11/35 | 14/15/29 | 0.80 |

**Simulated Stage 2.**
- Setup:
  - Each repetition draws 6 random rank-sweep transitions and resamples n trials per policy.
  - Per transition, Holm is applied over 6 tests.
  - The pooled test is a Stouffer combination of the signed MWU z-scores.
- Detection rates (per-transition / pooled):

| L | comparison | pop. A12 | n=10 | n=20 |
|---|---|---|---|---|
| 1 | adaptive > 50/50 | 0.59 | 0.08 / 0.42 | 0.18 / 0.65 |
| 0.5 | adaptive > 50/50 | 0.55 | 0.04 / 0.20 | 0.10 / 0.31 |
| 0.2 | adaptive > 50/50 | 0.52 | 0.04 / 0.09 | 0.08 / 0.15 |
| 1 | adaptive > transfer | 0.64 | 0.42 / 0.62 | 0.46 / 0.72 |
| 0.5 | adaptive > transfer | 0.70 | 0.41 / 0.81 | 0.44 / 0.89 |
| 0.2 | adaptive > transfer | 0.78 | 0.47 / 0.99 | 0.62 / 0.99 |
| 0.5 | adaptive > fresh | 0.72 | 0.33 / 0.93 | 0.53 / 0.97 |

- Caveat: resampling from 30 trials understates variance, so these are upper bounds.
- The pooled test makes "adaptive beats transfer / fresh" a realistic primary claim. "Adaptive
  beats 50/50" stays out of reach unless L ≈ 1, and even then only with 20 trials.
- Random transitions are harder on transfer than the plan's real version pairs will probably be:
  in only 26 of 84 cells is the old best still best. Real per-transition rates depend on which
  pairs are chosen.

**Findings.**
- Every run 5–9 conclusion holds on the larger grid with a fresh realisation.
- `bmcs_cal_r` has the best worst case of any policy at every level, and the best median at
  L ≤ 0.5. It is the recommendation.
- Its L=1 cost is about 2% against `bmcs_cal` and 4% against the hindsight-best prior. It is the main
  weakness left (next step 4).

### Run 11: recency-weighted priors (`results/recency/`)

**Question.** Should the v-derived priors weight the end of the base run more, since v+1 starts
from the corpus inherited at the end of v?

**Command:**
`recency_sweep.py --out results/recency`, about 50 minutes on 8 processes (resumable;
`--report` rewrites `summary.md` from `raw.pkl`).

**What changed in the simulator.**
- `run_policy(..., half_life=h, recency="decay" | "weight")`. `base_run_counts` also returns counts
  where each batch is weighted by 0.5^(age / h), with age in base-run executions (all operators).
  Same random draws, so `half_life=None` is bit-identical to before (checked).
  - `decay` builds transfer, calib and shuffled from the weighted counts: recency-weighted mean,
    weight min(N, ñ).
  - `weight` keeps the full-run mean and only caps the weight at min(N, ñ). This is the control that
    separates "more recent" from "weaker": a short memory also means fewer effective executions.
- Four `drift_*` scenarios where v's ranking changes *during the base run* (per-operator τ on v, see
  `DRIFT_TAU`). v+1 is a permutation of OLD_RATES ranked like v at the end of the base run (`_late`,
  where recency should help) or at its start (`_early`, where it should hurt).

**Grid:**
- Policies: transfer, `bmcs_cal_r`, `mix50_cal_r`, each with 7 prior variants: full, decay and
  weight at h ∈ {64k, 16k, 4k}. Fresh and calib at full only, for reference.
- 25 scenarios: the 4 drift scenarios; no_shift, mild_shift, reversal, close_no_shift,
  close_reversal; rank and rankc at ρ ∈ {1, 0.5, 0, −1} × 2 draws.
- L ∈ {1, 0.2}, R=30, N=5000: 1,150 cells.
- Effective executions per operator: about 10.8k at h=64k, 2.9k at 16k and 740 at 4k (full run: 31k).
  So at h=64k the cap N=5000 still binds, and `w64k` is identical to `full` (checked). **`d64k` vs
  `full` is therefore the clean "more recent at the same weight" comparison.**

**Findings.**
- **Recency at the same weight does nothing for the controller.** `bmcs_cal_r` with `d64k`: median
  ratio to full 1.006 at L=1 and 1.000 at L=0.2, range 0.90–1.08, no significant cell after
  Bonferroni over 25 scenarios. Same for `mix50_cal_r`.
- **Shorter memories mostly just weaken the prior, and `weight` reproduces their effect.**
  - For transfer alone, d16k/d4k give big gains exactly where transfer is wrong (reversal 1.3–2.0×,
    rank ρ ≤ 0 up to 3.3×) and cost 5–22% where it is right (no_shift, rank ρ=1, close). The
    weight-only control gives nearly the same numbers (for example rank_0_0 at L=1: d4k 3.32,
    w4k 3.35; no_shift: 0.95 and 0.95). This is the familiar "smaller N is safer and weaker" trade
    from run 7, not a recency effect.
  - For `bmcs_cal_r`, which already protects against a wrong ranking, h=4k costs up to 7% where the
    ranking is right (close_no_shift 0.93–0.94, rankc_1_0 0.93, no_shift at L=0.2 0.94) and gains
    nothing significant elsewhere.
- **Why the drift scenarios show no recency gain.**
  - The late base-run window has very few successes. Rates decay to about 1/6 of their start by
    T/4, so a 16k half-life leaves 0–4 effective successes per operator. The transfer prior's rank
    correlation with v+1 drops from 0.52 (full) to 0.19 (d16k) and −0.06 (d4k) in drift_geom_late,
    and falls with h in every control scenario too (no_shift: 0.98 → 0.84 → 0.52).
  - Where the late leader is clear (drift_swap_late), the full-run average already ranks it in the
    top two (rank correlation 0.98), so there is little to gain.
  - Only `d64k` keeps enough data, and it moves rank correlation by at most ±0.1.
- **Side observation: transfer's unscaled prior gains a little from recency at L=0.2 (d64k median
  1.036).** Late rates are lower, so the recency-weighted mean is less over-optimistic: recency acts
  as a crude rescaling. The rescaled controller already does this properly, so it gains nothing.
- **The controller's edge over the matched coin flip is unchanged** (median `bmcs_cal_r` /
  `mix50_cal_r` 1.00–1.02 for every variant).

**Conclusion.** Keep the full-run prior. In this simulator a recency-weighted prior only helps
through the weaker weight it implies, which the controller makes unnecessary, and its noise costs
up to 7% where the old ranking holds. The caveat is the rate model: a real base run whose ranking
shifts sharply while still producing many late successes (slower decay than here) could change
this. The real base run's per-batch log can check that directly: if the family ranking in its last
quarter matches the full-run ranking, recency weighting cannot help.

## Overall conclusions

1. **Question 1 (does old experience help?).** Yes, when the old top operators stay near the top,
   and only with a strong prior (N in the thousands).
   - The gain over calibrated fresh is about +5–20% at 1h.
   - What decides it is whether the old *best* operators keep their place, not the overall rank
     correlation (run 6).
   - When the old best falls to the bottom half, transfer loses 25–50%, and more with larger N.
2. **The previous plan's bandit controller doesn't work.** It is mostly indistinguishable from a coin
   flip. The cause is structural: too little evidence per batch, credited to one model, before the
   models converge.
3. **Scale-invariant Bayesian model comparison picks the right hypothesis.**
   - P(T) tracks the true rank correlation across 168 random rank shifts.
   - It falls to ≤ 0.25, usually below 0.1, wherever transfer would lose more than 25%.
   - Its only systematic error is following T when the old best drops slightly (cost ≤ 8%).
4. **The controller must act at the fitted scale when v+1 starts lower.**
   - With an inherited corpus, every prior built from v is over-optimistic.
   - Acting with calibrated fresh at the old scale can then be worse than Beta(1,1).
   - Rescaling the followed prior to the posterior-mean c (`bmcs_cal_r`) fixes this.
     - It is never significantly worse than any fixed prior in the 16 designed scenario × level
       cells at L ≤ 0.5.
     - In the rank sweep it is within 1% of the hindsight-best fixed prior at L=0.5 and 5–10%
       above it at L=0.2.
   - It costs 3–5% when v+1 is *not* lower (L=1). `bmcs_cal` is better there.
   - Much of the robustness comes from rescaling plus hedging between C and T. A coin flip with
     the same rescaling (runs 9–10) is 1–2% behind in median. Across 276 cells it is
     significantly behind in 45 and ahead in 1. Evidence-weighing adds about +2–6% under reversal at
     L ≥ 0.5 (run 9 vs run 10) and almost nothing at L=0.2.
   - Across all 276 run-10 cells its worst ratio to the hindsight-best fixed prior is 0.88. No other
     policy's is above 0.84, and transfer's is 0.29.
   - Stage 2 starts from the inherited corpus, so `bmcs_cal_r` is the recommended controller. The
     pilot should measure the actual level (the fitted c) to confirm this.
5. **N=5000 is fixed.** With the controller, N matters little in 1000–20000. Transfer-only becomes
   both better and riskier as N grows.
6. **Stage 2 needs about 20 trials per configuration for question 1.**
   - 10 trials catch transfer's collapse every time, but detect "the ranking helps" only about half
     the time.
   - Equivalence claims need a margin, not a non-significant test.
7. **Open weaknesses.**
   - The cost of rescaling at L=1.
   - No answer to mid-campaign ranking changes (late_riser).
   - Late drift in P(T).
   - Simulated variance is probably optimistic.

## Proposed next steps

Status of the previous list:

| # | step | status |
|---|---|---|
| 1 | Rank-correlation sweep | done (run 6) |
| 2 | Inherited-corpus default | done (run 5); `--level` flag, every later run uses L ∈ {1, 0.5, 0.2} |
| 3 | Finer N sweep | done (run 7); N=5000 fixed |
| 4 | Calib/transfer 50/50 control | done (`mix50_cal`, run 5; rescaled `mix50_cal_r`, run 9) |
| 5 | Log calib-vs-transfer divergence | done (`tv_pair`, default calib vs transfer) |
| 6 | Power check | done (run 8) |
| 7 | Seed by scenario name | done (`scenario_seed`) |
| 8, 9 | Operator-level / evidence forgetting | not started (optional) |
| — | Consolidated sweep of everything | done (run 10) |

These are mirrored in `PLAN.md` section 6.

**Before Stage 2:**

1. **Decide the trial count.** Run 8 says about 20 trials per configuration for question 1. At the
   plan's 6 transitions × 9 configurations × 4h, that doubles compute to about 4,300 core-hours.
   Options, at roughly the original budget:
   - 20 trials on 3 transitions;
   - 20 trials with 2-hour campaigns;
   - 20 trials for the four core policies only, and 10 for the rest.
2. **Pre-register an equivalence margin** for "adaptive ≈ transfer where transfer helps", for example
   A12 ≥ 0.36 or median ratio ≥ 0.95.
3. **Decide how to test "adaptive beats 50/50".** Runs 9–10 show the edge over the matched coin flip
   is small: +1–2% median, population A12 0.52–0.59. Run 10's simulated Stage 2 detects it 4–18% of
   the time per transition. A pooled test over 6 transitions detects it 9–65% of the time, so even
   that is not enough.
   Options:
   - pre-register a pooled test across transitions, for example a stratified test on per-transition
     A12;
   - move "beats 50/50" from the strong criterion to a secondary analysis;
   - reframe the contribution as "rescaled hedging between C and T", with evidence-weighing as a
     measured refinement.

**Optional simulation work:**

4. **Rescaling cost at L=1.** A likely cause: shrinking the prior mean at fixed weight W lowers its
   relative precision, which dilutes the ranking. Test rescaling with W scaled by 1/c, which keeps
   relative precision, and see whether it removes the L=1 cost without losing the L ≤ 0.5 gains.
5. **Operator-level forgetting** (late_riser) and **evidence forgetting in P(T)** (late drift), as
   before.
6. **Recency-weighted priors: done, not adopted (run 11).** No gain at matched weight; shorter
   half-lives only weaken the prior. Revisit only if a real base run's late-quarter family ranking
   differs from its full-run ranking.

**Then Stage 2:** LibAFL scheduler and the one-transition pilot (week-3 gate). The pilot should log
the fitted scale c, the real counterpart of L, which decides between `bmcs_cal_r` and `bmcs_cal`.
