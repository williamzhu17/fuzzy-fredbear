# Adaptive Policy Transfer for Cross-Version Fuzzing: Revised Project Plan (v3)

Oct 21, 2026 · @Someone

The previous version is kept in [`archive/PLAN_v2.md`](archive/PLAN_v2.md). This version was updated after Stage 1 runs 5–8.
Stage 1 evidence for every change below is in [`sim/README.md`](../sim/README.md) (run log) and the `sim/results/` directories.

## Summary

We ask whether a fuzzer can benefit from mutation-operator preferences learned on version v of a
program, while detecting when that experience has become misleading on version v+1.

A Bayesian model-comparison controller weighs two hypotheses about operator productivity on v+1:

- **Transfer:** the old operator ranking still holds.
- **Calibrated fresh:** rates are on the right scale but the old ranking carries no information.

Both hypotheses are scored on all evidence collected so far, and neither is penalised for being off by a
common scale factor. The controller follows each hypothesis with probability equal to its posterior
probability. The followed model, rescaled to the fitted scale, recommends the next mutation operator. We test the idea first in a
controlled simulation (Stage 1, done), then in real fuzzing campaigns across several version
transitions (Stage 2).

### Changes from the previous draft, driven by the Stage 1 simulation

- **New controller.** The two-level Thompson-sampling bandit over {fresh, transfer} is replaced by
  scale-invariant Bayesian model comparison (section 4).
  - The bandit credited only about one success per batch, and only to the chosen model. It could not
    tell the models apart before they converged.
  - It was statistically indistinguishable from a fixed 50/50 coin flip in 13 of 16 simulated
    configurations. It beat the coin flip only in three easy scenarios at N=5000, and it was
    significantly worse than transfer-only in several scenarios where transfer helps.
- **The controller's alternative hypothesis is calibrated fresh, not Beta(1,1).**
  - Against Beta(1,1), the transfer prior always wins the comparison on scale alone: Beta(1,1)
    predicts about a 50% success rate where real rates are about 10⁻³.
  - In the simulation, that comparison then behaved exactly like transfer-only, including the 50%
    collapse under a ranking reversal.
  - Fresh-only Beta(1,1) remains as the reset baseline.
- **Scale-invariant scoring.** Each hypothesis is "rates = c × prior means" with the scale c
  marginalised. Without this, a pure scale shift between versions made the controller reject a
  correct ranking. This is the realistic case of starting v+1 from an inherited corpus, where every
  operator succeeds less often. This replaces the rescaling sensitivity check from section 3 of the
  previous draft.
- **The followed model acts at the fitted scale.** Starting v+1 from an inherited corpus lowers
  every rate, so priors built on v are over-optimistic. Acting with them unscaled made the controller
  worse than Beta(1,1) under a reversal at 0.2× rates. Rescaling to the posterior-mean scale fixes
  this (sections 3–4). It costs 1–5% only when v+1 rates are *not* lower; the Stage 2 pilot measures
  which case holds.
- **N raised from 500 to 5000 (fixed).**
  - At N=500 the transferred evidence is overwritten within minutes, and no policy differs from any
    other by more than a few percent in any scenario.
  - A sweep over N ∈ {1000, 2000, 5000, 20000} put the controller at or near its best at 5000. The
    controller is insensitive to N; transfer-only gets both better and riskier as N grows.
- **About 20 trials per configuration** instead of 10 for the ranking question (section 7). A
  simulated power check found that 10 trials detect "the old ranking helps" only about half the time.
- **Discounting removed.** The controller no longer keeps reward counts. In the bandit design, γ had
  no useful effect: γ=1.0 was best or tied in 7 of 8 hard scenarios.
- **The 50/50 control now mixes the same two models as the controller.** Those are calibrated fresh
  and transfer.
- **Stage 1 expanded.** It now has 8 designed scenarios, a sweep over 168 random rank shifts, three
  inherited-corpus levels, an N sweep and a power check. Section 6 summarises them.

## 1. Problem and hypothesis

When software moves from version v to v+1, a fuzzer can either reuse the operator preferences it
learned on v or reset and learn again. Reuse may speed up early exploration if the program behaves
similarly. It may also impose outdated beliefs that suppress newly useful operators.

**Hypothesis.** An adaptive policy that weighs transferred against fresh mutation models can approach
the benefit of transfer when old knowledge stays useful, and reduce its cost when old knowledge
misleads.

This splits into two empirical questions, and we do not assume either answer is yes:

1. Does previous-version experience predict mutation effectiveness on the new version, and for how
   long into the campaign?
2. When that usefulness varies across transitions, can a lightweight controller exploit the variation
   better than always transferring or always resetting?

If transfer almost always helps, the controller only adds wasted exploration. If transfer rarely
helps, fresh-only is enough. Both are reportable outcomes.

**Relation to prior work.** Bandit-based mutation scheduling within a single campaign is established,
for example Thompson sampling over operators (Karamcheti et al., 2018) and MOpt's operator scheduling
(USENIX Security 2019). Our contribution is narrower: the cross-version question, and principled
selection between inherited and fresh beliefs. In continuous fuzzing, the inherited corpus likely
carries most transferred value. We therefore hold the corpus fixed across policies and isolate the
effect of transferred operator preferences.

## 2. Actions, reward, and objective

*Unchanged from the previous draft.*

The operator set is A = {a₁, …, a_K}, grouped into families such as bit/byte flips, arithmetic, block
insertion/deletion, interesting values, and dictionary insertion. We use roughly K = 6 to 10
families.

**What one action is.** Stock havoc stacks several randomly chosen operators per execution, which
makes credit ambiguous. We replace that choice with a single selected family: one execution applies a
random stack depth of mutations, all from family a_t. Credit is then unambiguous, and stacking
behaviour is preserved.

**Reward.** Each execution yields a binary reward:

$$
r_t = \begin{cases} 1 & \text{if the execution finds coverage unseen by the whole campaign} \\ 0 & \text{otherwise} \end{cases}
$$

"Unseen" is campaign-wide, regardless of which model recommended the mutation, so both models pursue
the same objective. We also log the number of new edges per success, for evaluation only.

**Exact definition of a success.** AFL-style fuzzers count an input as interesting if it reaches a
new edge or a new hit-count bucket on a known edge. We set r_t = 1 exactly when the fuzzer would add
the input to its corpus on either ground. The same definition is used in the simulation, the
controller, and the evaluation. New edges alone are logged separately for the coverage metrics.

**Statistical model.** Each operator has an unknown success probability,
r_t | a_t = a ~ Bernoulli(θ_a). This is an approximation: real productivity depends on the seed and on
coverage already found, and it falls over time.

**Objective.** Maximise coverage-expanding executions within a fixed wall-clock budget. The
controller adds per-execution sampling overhead, so policies will not run equal numbers of
executions. Wall-clock time is what a fuzzing user pays for, and we report executions per second for
every policy. In the simplified model, with T executions:

$$
\max_{\pi} \; \mathbb{E}_{\pi}\left[\sum_{t=1}^{T} r_t\right]
$$

Total edge coverage is evaluated separately, since one success may find one edge or many. Bugs are
the ultimate motivation but too sparse to be the learning signal; we report them where they occur.

## 3. Priors: fresh, calibrated fresh, and transfer

Each model m keeps a Beta belief over each operator's success probability,
θ_{m,a} ~ Beta(α_{m,a}, β_{m,a}). Its mean is α/(α+β); a larger α+β at the same mean means more
confidence.

**Fresh model (reset baseline only).** Every operator starts at Beta(α₀, β₀), with α₀ = β₀ = 1.
Stage 1 showed that this prior is badly miscalibrated for fuzzing: it predicts about a 50% success
rate where real rates are around 10⁻³. It is therefore used only as the fresh-only baseline, not
inside the controller.

**Transfer model with a capped prior.** On version v, operator a recorded s_a successes and f_a
failures, with n_a = s_a + f_a. We keep the old mean but cap its weight at an effective sample size N:

$$
\hat p_a = \frac{s_a + \alpha_0}{n_a + \alpha_0 + \beta_0}, \qquad N_a = \min(N, n_a)
$$

$$
\theta_{T,a} \sim \operatorname{Beta}\big(\alpha_0 + N_a \hat p_a,\; \beta_0 + N_a (1 - \hat p_a)\big)
$$

N has a direct reading: old evidence is worth N new observations of that operator.

- **Default N = 5000 (fixed).**
  - In simulation, N=500 was washed out within a few simulated minutes and produced no measurable
    differences between any policies.
  - N=5000 produced large effects in both directions: about +5–10% for transfer when the ranking
    holds, and −50% when it reverses.
  - Over N ∈ {1000, 2000, 5000, 20000}, the controller stays within about ±5% and is at or near its
    best at 5000. Transfer-only's gain and its reversal collapse both keep growing with N.
- **N = 0** makes all priors identical and remains a sanity check. It passed in simulation.

**Calibrated-fresh model (the controller's alternative hypothesis, and a control).** Every operator
gets the same prior, centred on the mean old rate $\bar p = \frac{1}{K}\sum_a \hat p_a$, with weight
N_a. It has the right scale but no ranking.

**Shuffled transfer (control).** The real p̂ values, randomly reassigned to operators, with weight N.
It has the right scale and spread but the wrong ranking.

Transfer is credited with version-specific knowledge only if it beats both calibrated fresh and
shuffled transfer.
- **N=5000:** transfer beat shuffled transfer in every hard scenario where the ranking held
  (A12 0.72–0.80).
- **N=500:** the difference was detectable only in the easy no-shift scenario (A12 0.67).

**Scale caveat.** Old rates come from the early phase of a campaign started from scratch on v. The
campaign on v+1 starts from an inherited corpus, so every operator is likely to succeed less often.
The prior therefore encodes the ranking of operators better than their scale. The controller handles
this twice (section 4): its comparison ignores overall scale, and the followed model is rescaled to
the fitted scale before it acts.

- **Why rescaling is needed.** In simulation, v+1 rates were multiplied by L ∈ {1, 0.5, 0.2}.
  - At L=0.2 calibrated fresh at the old scale fell below Beta(1,1) in every scenario. A controller
    that acted with it lost to Beta(1,1) under reversal (104 vs 125 successes at 1h).
  - With rescaling, the controller was never significantly worse than any fixed prior at L ≤ 0.5.
    At L=0.2 it was 5–10% above the hindsight-best fixed prior across the rank sweep.
- **Cost.** At L=1 (no drop), rescaling is 1–5% below the unscaled version, and significantly below
  transfer-only in three of eight scenarios. This is why rescaling looked harmful in the first test,
  which ran only at L=1. The likely cause is that shrinking the prior mean at a fixed weight dilutes
  the ranking. Acting with the unscaled prior remains the fallback if the pilot shows no drop in
  rates.

**Building an unbiased prior.** *Unchanged.* Old counts are collected under uniform random operator
choice, so every family gets comparable evidence. Only the first hour of each base run feeds the
prior, so saturated late-campaign rates do not dominate. We make three independent base runs per
transition, and each trial on v+1 draws its prior from one of them in rotation.

## 4. Controller: scale-invariant Bayesian model comparison

**Why not a bandit over models.** The previous draft treated "follow F" and "follow T" as two bandit
arms. Stage 1 showed this cannot work at fuzzing success rates:

- **Weak signal:** each batch yields about one success, credited only to the chosen model.
- **Convergence:** the two models share all evidence, so they converge within 15–50 simulated
  minutes and the arms become identical.

It was indistinguishable from a 50/50 coin flip in 13 of 16 simulated configurations, and
significantly worse than transfer-only in several scenarios where transfer helps.

**Two hypotheses.** Both F and T see every execution, so they can be scored as competing hypotheses on
the same data, with no counterfactual problem. For m ∈ {C, T} (calibrated fresh, transfer), let
μ_{m,a} be the model's prior mean for operator a and W_a = α₀ + β₀ + N_a its prior weight. Hypothesis
H_m says the rates are the model's prior means up to an unknown global scale c:

$$
\theta_a \mid H_m, c \sim \operatorname{Beta}\big(W_a\, c\,\mu_{m,a},\; W_a\,(1 - c\,\mu_{m,a})\big)
$$

The scale c gets a uniform prior on log c over a grid G of 61 points spanning [1/30, 30], with c·μ
capped at 0.5. Both hypotheses share this prior, so neither is penalised for being off by a constant
factor. Only the shape of the ranking is tested.

**Evidence.** With s_a and f_a the successes and failures of operator a on v+1 so far, pooled across
all executions whichever model recommended them:

$$
P(D \mid H_m) = \frac{1}{|G|} \sum_{c \in G} \prod_{a} \frac{B\big(W_a c \mu_{m,a} + s_a,\; W_a (1 - c \mu_{m,a}) + f_a\big)}{B\big(W_a c \mu_{m,a},\; W_a (1 - c \mu_{m,a})\big)}
$$

$$
P(H_T \mid D) = \frac{P(D \mid H_T)}{P(D \mid H_T) + P(D \mid H_C)} \qquad \text{(equal prior odds)}
$$

Here B is the Beta function, and the operators are treated as independent given c. Operator choices
depend only on past data, so the adaptive way the data were collected does not bias this likelihood.

**Decision rule.**

- **Batch start:** at the start of batch k (B = 256 executions), the controller computes P(H_T | D)
  and follows T with that probability, otherwise C. This is Thompson sampling over hypotheses.
- **Operator choice:** within the batch, the followed model m_k is first rescaled to its fitted
  scale, the posterior mean of log c under H_{m_k}:

$$
\log \hat c_m = \sum_{c \in G} \log c \; P(c \mid D, H_m), \qquad
\alpha'_{m,a} = W_a \hat c_m \mu_{m,a}, \quad \beta'_{m,a} = W_a (1 - \hat c_m \mu_{m,a})
$$

  with ĉ_m μ_{m,a} capped at 0.5, as in the evidence.

  It then recommends operators by Thompson sampling from the rescaled prior plus the shared counts:

$$
\tilde\theta_a \sim \operatorname{Beta}(\alpha'_{m_k,a} + s_a,\; \beta'_{m_k,a} + f_a), \qquad a_t = \arg\max_a \tilde\theta_a
$$

  The posterior over c is a by-product of the evidence computation, so this costs nothing extra.
  Acting with the unscaled prior (α, β) is the variant to use if v+1 rates turn out not to be lower
  than v's.

- **Per-execution variant:** sampling the hypothesis per execution instead of per batch (Bayesian
  model averaging) performed the same in simulation.

**Batching.** With model comparison, B only sets how often the hypothesis is resampled; all
executions contribute evidence. B had little effect in the bandit design, and B = 256 is kept.

**Cost.** One evaluation per batch of 2 × |G| × K log-Beta functions, negligible next to execution
cost.

## 5. Learning updates and model convergence

| Level | What it estimates | Who is updated | When |
|---|---|---|---|
| Operator counts (s_a, f_a) | Productivity of operator a on v+1 | Shared by all models | After every execution |
| Hypothesis posterior P(H_T \| D) | Whether the old ranking holds on v+1 | Recomputed from the shared counts | Start of every batch |

**The models converge, and we measure it.** Shared updates dilute the transfer prior over time: after
roughly N executions of an operator, the models' beliefs about it are close. We log the total-variation
distance between the models' recommendation distributions and P(H_T | D) at regular intervals. The
simulation logs C vs T, the pair the controller compares. We also log the fitted scale ĉ, which
shows how far v+1 rates fell below v's.

**Late-campaign drift.** P(H_T | D) is cumulative. In simulation it sometimes slid back toward 0.5
late in the campaign, after the models had converged and the choice no longer mattered. We report it
over time rather than as a single number.

## 6. Stage 1: simulation study (complete)

All policies run on a synthetic K = 8-armed Bernoulli bandit where we control the shift between
versions. Code, run commands and full results are in `sim/` (see [`sim/README.md`](../sim/README.md), runs 1–10;
run 10 is the consolidated sweep and its "Bottom line" summarises everything).

- **Rates and decay:** rates are at fuzzing-like magnitudes (10⁻⁴ to 10⁻²) and decay over the
  campaign.
- **Campaign length:** T = 10⁶ executions stands in for 4 hours.
- **Priors:** the transfer prior comes from three simulated uniform-choice base runs on the old rates.
- **Inherited corpus:** v+1 rates are multiplied by a level L ∈ {1, 0.5, 0.2}. L < 1 stands in for
  starting from the inherited corpus.
- **Replication:** 30 trials per configuration; 200 for the power check.

**Designed scenarios** (N=5000, successes at 1h; "controller" is the rescaled scale-invariant
controller of section 4):

| Scenario | Shift from old to new version | Best fixed policy | Controller, L = 0.5 | Controller, L = 1 |
|---|---|---|---|---|
| No shift | Identical rates | Transfer | Ties transfer | Ties transfer |
| Mild shift | Best unchanged; others perturbed | Transfer | Ties transfer | Ties transfer |
| Reversal | Old best ↔ 7th | Calib (transfer −50%) | Ties calib, 2× transfer | 2× transfer; below calib (A12 0.27) |
| Saturation | Same ranking, rates × 0.2 | Transfer | Beats transfer (A12 0.81) | Beats transfer (A12 0.67) |
| Close, no shift | Top 4 within 1.6× | Transfer | Ties transfer | Below transfer (A12 0.25) |
| Close reversal | Old best to 5th; new best was old 4th | Transfer (L<1), calib (L=1) | Ties transfer | Ties both |
| Late riser | One operator decays 10× slower | Transfer | Ties transfer | Below transfer (A12 0.32) |
| Depletion | Old best has a tiny coverage pool | Transfer | Ties transfer | Below transfer (A12 0.30) |

At L=0.2 the controller is never significantly worse than any fixed policy. It is significantly
better than the best one under no shift and reversal.

**Random rank shifts.** There were 168 draws with rank correlation from 1 to −1, on wide-spread and
close-together rates.
- **Transfer's value depends on where the old best ends up.** It helps when the old best operator
  stays at or near the top. It loses 25–50% when the old best falls to the bottom half, even at
  moderate overall rank correlation (Spearman 0.3–0.55).
- **P(H_T | D) tracks the realised correlation.** It is ≈0.9 at identical ranking, and ≤0.25
  (usually <0.1) wherever transfer loses more than 25%.
- **Against the hindsight-best fixed prior,** the controller's median ratio is 0.99–1.01 at L=0.5
  and 1.05–1.10 at L=0.2.
- **Its systematic error is following T when the old best drops only slightly.** That costs at most
  8% against calib.

**Stage 1 conclusions.**

- **Question 1:** transfer helps when the old top operators stay on top and hurts badly when they
  don't, but only with a strong prior.
- **The previous bandit controller fails, for structural reasons.**
- **The controller reaches the "strong" pattern of section 9 in simulation, when v+1 starts lower
  than v.** Rescaling is what makes this work under an inherited corpus. Without a drop in rates,
  the unscaled version is better.
- **The scale prior does much of the work.** At L=1, calibrated fresh alone captures much of
  transfer's gain over Beta(1,1). At L<1 the old scale misleads, and the ranking's value over calib
  grows to about 5–20%.
- **The fixed 50/50 mix of C and T, with the same rescaling,** is close behind the controller.
  - It is never significantly better than the controller.
  - It is about 2% behind in median, and 6% behind under reversal at L ≥ 0.5 (A12 ≈ 0.72,
    significant after Holm).
  - At L=0.2 it nearly ties, even under reversal. A rescaled prior with a small fitted scale is
    weakly confident in its ranking, so a wrong one is overruled quickly.
  - So most of the robustness comes from rescaling plus hedging between C and T. Evidence-weighing
    adds a smaller, consistent edge.
- **Consolidated sweep (run 10).** 276 transition × level cells, 7 policies, fresh RNG realisation.
  All of the above held.
  - **Worst case.** The controller's worst ratio to the hindsight-best fixed prior is 0.88. The
    rescaled 50/50 mix's is 0.83, the unscaled controller's 0.74, and transfer's 0.29.
  - **Median.** The controller's median is 0.96 at L=1, 0.995 at L=0.5 and 1.09 at L=0.2.
  - **Against 50/50.** It is significantly better than the rescaled 50/50 in 45 of 276 cells and
    worse in 1. The median gain is +0.9–2.0%.
  - **Simulated Stage 2** (6 random transitions, pooled Stouffer test):
    - "Controller beats transfer" is detected 62–99% of the time with 10–20 trials.
    - "Controller beats fresh" is detected 89–99% of the time.
    - "Controller beats 50/50" is detected only 9–65% of the time.
- **Power:** see section 7.

**Remaining before Stage 2** (details in [`sim/README.md`](../sim/README.md), "Proposed next steps").

1. **Decide the trial count and budget** (section 8).
2. **Pre-register an equivalence margin** for "adaptive ≈ transfer where transfer helps", for example
   A12 ≥ 0.36 or median ratio ≥ 0.95. A non-significant test with 10–20 trials does not show
   equivalence.
3. **Decide how "adaptive beats 50/50" is tested.** The simulated edge (A12 ≈ 0.7 where present)
   would be detected per transition only 14–48% of the time with 10–20 trials. Run 10's pooled test
   over 6 random transitions reaches only 9–65%, depending on L. A pooled test helps but is not
   enough. Moving it to a secondary analysis is the safer option (section 9).
4. *Optional:* reduce rescaling's cost at L=1 by rescaling the prior weight as well. Also optional:
   operator-level forgetting (late riser) and evidence forgetting (late drift in P(H_T | D)).

The rule that real transfer must beat both controls under no shift was met at N=5000.

## 7. Stage 2: real fuzzing experiments

**Implementation, targets, fuzzer configuration and run hygiene.** *Unchanged from the previous
draft.*

- **Implementation:** a LibAFL scheduler, with an AFL++ custom mutator as the fallback.
- **Targets:** libpng, libxml2 and libtiff, with one small and one large transition each.
- **Configuration:** CmpLog and automatic dictionaries off, a fixed hand-written dictionary per
  program, and the same corpus scheduler for every policy.
- **Hygiene:** each campaign pinned to its own core, and configurations interleaved in the run order.

**Protocol per transition.** *Unchanged except the trial count (10 → 20).*

1. Run three independent 6-hour campaigns on version v with uniform random operator choice. Save each
   corpus and the per-operator counts from its first hour.
2. Build the transfer, calibrated-fresh and shuffled-transfer priors from those counts (section 3).
3. Run each policy on v+1 for 4 hours of wall-clock time, 20 independent trials, all starting from
   the same inherited corpus. Trials rotate through the three base-run priors.
4. Replay the corpus at the start and record its coverage separately, so only discoveries from new
   mutations are credited to a policy.

**Policies.**

| Policy | Behaviour | Purpose |
|---|---|---|
| Fresh-only | Always follow Beta(1,1) prior | Reset baseline |
| Calibrated fresh | Always follow C (uniform prior at the old mean, weight N) | Is a well-scaled prior enough? |
| Shuffled transfer | Always follow T with old rates reassigned at random | Does the old ranking matter? |
| Transfer-only | Always follow T | Reuse baseline |
| **Adaptive** | Scale-invariant model comparison between C and T, acting at the fitted scale (section 4) | The proposed method |
| Fixed 50/50 | Follow C or T at random per batch, same rescaling and shared updates | Does weighing the evidence add value beyond mixing? |

The original bandit controller is dropped from Stage 2. In simulation it was mostly
indistinguishable from 50/50 and consistently below the model-comparison controller. Stock havoc,
and adaptive acting with the unscaled prior, can return as single runs per transition if compute
allows.

**Same-version restart control.** Restart fresh-only, transfer-only and adaptive on version v itself,
from the saved corpus. If transfer loses value here too, the cause is corpus maturity rather than the
software change. In simulation, the analogous scenarios (no change in ranking, all rates lower) showed
transfer still helping once scale is ignored.

**Primary outcome, fixed in advance.** Edge coverage at 1 hour, adaptive versus transfer-only, across
all six transitions. A pre-specified secondary analysis splits transitions by whether transfer-only
beat fresh-only. Every other metric and comparison is secondary and reported as such.

**Metrics.**
- **Coverage:** edge coverage at 15 minutes, 1 hour and 4 hours; area under the coverage curve.
- **Controller behaviour:** coverage-expanding executions; P(H_T | D) over time; the share of batches
  given to T; model divergence over time; the fitted scale ĉ over time.
- **Crashes:** any unique crashes, deduplicated by stack hash.

**Statistics.** Following Klees et al. ("Evaluating Fuzz Testing," CCS 2018), we report medians with
interquartile ranges. Pairwise comparisons use the Mann–Whitney U test with Vargha–Delaney A12 effect
sizes, Holm-corrected within each transition. The family is 5 comparisons: adaptive vs transfer,
calib and fresh; transfer vs calib and fresh. The claim "adaptive matches transfer" uses a
pre-registered equivalence margin, not a non-significant test.

**Power (simulated, 200 trials subsampled).** Detection rates after Holm correction:

| Effect | A12 | 10 trials | 20 trials | 30 trials |
|---|---|---|---|---|
| Adaptive beats transfer under reversal | 0.99 | 100% | 100% | 100% |
| Transfer beats calib, no shift (ranking matters) | 0.85 | 68% | 98% | 100% |
| Transfer beats calib, close rates | 0.81 | 48% | 93% | 99% |
| Transfer beats calib, close reversal | 0.73 | 14% | 48% | 73% |
| Adaptive beats transfer under pure scale shift | 0.67 | 17% | 46% | 61% |

Ten trials are enough for the headline "adaptive avoids transfer's collapse", but not for question 1.
Real trials are likely noisier than simulated ones, so these rates are optimistic. **We plan 20
trials per configuration** (section 8).

## 8. Timeline and compute budget

The plan front-loads the simulation and a one-transition pilot, so the expensive main runs start only
with settings already fixed.

**Week-3 gate.** The gate checks six things before the main compute is spent:
- the scheduler runs at normal speed;
- rewards are logged correctly;
- operator families actually differ: in the pilot's uniform-choice base runs, the best family's
  success rate is at least twice the median family's;
- *(new)* the per-batch evidence computation adds negligible overhead;
- *(new)* the pilot's trial-to-trial variance is no larger than the simulation's. If it is larger,
  the power table is recomputed with the pilot's variance and the trial count adjusted;
- *(new)* the fitted scale ĉ on v+1 is below 1, confirming that the rescaled controller is the
  right variant. If ĉ ≈ 1, adaptive acts with the unscaled prior instead.

If any check fails, we adjust or cut scope first.

| Item | Count |
|---|---|
| Transitions | 6 (3 programs × 2) |
| Configurations per transition | 9 (6 cross-version policies + 3 same-version controls) |
| Trials per configuration | 20 (was 10; see the power table in section 7) |
| Campaign length | 4 hours |
| Main runs | about 4,320 core-hours |
| Base runs on version v | 3 per transition × 6 hours = 108 core-hours |
| Total | about 4,430 core-hours |

On a 32-core machine, that is about 6 days of wall-clock time, double the previous draft. **The
budget is an open decision.** If it has to stay near the previous 2,270 core-hours, the options are:

- **2-hour campaigns** (about 2,270 core-hours). The primary outcome is at 1 hour, so this loses only
  the 4-hour metrics.
- **3 transitions** (about 2,220 core-hours). This keeps everything per transition but weakens the
  cross-transition analysis.
- **20 trials for the core four policies, 10 for the rest:** adaptive, transfer-only, calibrated
  fresh and fresh-only get 20; shuffled transfer, 50/50 and the same-version controls get 10. That is
  about 3,230 core-hours.

We do not cut back to 10 trials: in simulation, 10 trials answer question 1 only about half the time.

## 9. Course connection, limitations, and what counts as a result

**Course techniques.**
- **Bayesian inference:** represents uncertain operator productivity.
- **Bayesian model comparison:** marginal likelihoods, posterior model probabilities, and a nuisance
  scale parameter integrated out. This decides how much to trust transferred knowledge.
- **Thompson sampling:** balances exploration and exploitation, over operators and over hypotheses.
- **Transfer learning:** enters as prior information with a controlled strength.
- **Model evaluation:** tests whether these approximations still support good decisions. The
  Beta(1,1) failure is a concrete example of a prior that is uninformative in name but badly
  miscalibrated in practice.

**Limitations.**
- **Nonstationarity.** Coverage is consumed, the corpus changes, and operator rates fall over time.
  The Bernoulli model with fixed θ_a is wrong, and P(H_T | D) accumulates evidence that can go stale,
  as in the late drift seen in simulation.
- **Mid-campaign ranking changes.** Changes such as the late-riser scenario hurt every policy,
  because the stale evidence sits in the shared operator counts. Neither prior choice fixes this;
  operator-level forgetting is future work.
- **Accuracy is not the same as usefulness.** Model comparison rewards the more accurate hypothesis,
  not the more useful one. Scale invariance removes the main known mismatch, a global scale shift,
  but not per-operator scale changes.
- **Narrow evidence base.** There are few targets and transitions, coverage is a proxy for bugs, and
  4-hour campaigns say little about long-run behaviour.
- **Simulated scenarios.** Stage 1 results depend on a simulator we designed. The rank-correlation
  sweep (168 random rank shifts) reduces the dependence on hand-picked shifts, but not on the model
  itself: independent operators, smooth decay, and a single global scale change between versions.
- **The controller variant depends on the level.** Acting at the fitted scale helps when v+1 rates
  are lower and costs a little when they are not. The pilot's ĉ decides which variant runs.

**What would establish a useful result.**

- **Strong:** across most transitions:
  - adaptive is within the pre-registered equivalence margin of transfer-only where transfer helps,
    and significantly better where it hurts;
  - it beats the fixed 50/50 mix, tested pooled across transitions (in simulation the edge is
    small, A12 ≈ 0.7, too small to detect per transition);
  - transfer-only beats calibrated fresh and shuffled transfer, showing the benefit comes from
    version-specific knowledge.

  Stage 1 reached this pattern in simulation when v+1 starts lower than v (L ≤ 0.5). At L=1 the
  rescaled controller fell short of transfer in three of eight scenarios. Its edge over the matched
  50/50 mix was significant only under reversal (L ≥ 0.5) and under no shift at L=1.
- **Partial:** transfer clearly helps or hurts depending on the transition, but adaptive does not
  consistently capture the better side. This still answers question 1 and shows where the controller
  fails.
- **Null:** transfer has no measurable effect beyond the shared corpus and a well-scaled prior. This
  is a useful negative finding about cross-version operator-preference transfer. Stage 1 suggests
  the ranking adds only about 0–8% over calibrated fresh when rates do not drop, and about 5–20%
  when they do, so this outcome is plausible.

Beating fresh-only on a single transition is not enough to claim the controller is useful, since
transfer-only, or merely a well-scaled prior, might do just as well.
