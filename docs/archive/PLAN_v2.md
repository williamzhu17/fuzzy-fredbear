Adaptive Policy Transfer for Cross-Version Fuzzing: Revised Project Plan
Oct 21, 2026 · @Someone
Summary
We ask whether a fuzzer can benefit from mutation-operator preferences learned on version v of a program, while detecting when that experience has become misleading on version v+1.
A two-level Thompson sampler chooses between a transfer model, seeded with capped evidence from version v, and a fresh model with no history. The chosen model then recommends the next mutation operator. We test the idea first in a controlled simulation, then in real fuzzing campaigns across several version transitions.
Changes from the first draft:
• The transfer prior is capped at a fixed effective sample size, so old evidence cannot swamp new observations.
• The prior is built from three uniform-choice base runs, using only their first hour, to avoid sampling bias and saturation.
• Two new controls, calibrated fresh and shuffled transfer, test whether gains come from version-specific knowledge or just a better-scaled prior.
• The controller uses discounted updates, so credit earned in the easy early phase does not dominate later decisions.
• Decisions are made per batch of executions, and the unit of credit for stacked havoc mutations is defined explicitly.
• The reward, the wall-clock budget, and one primary outcome are fixed in advance.
• Fuzzer features that blur the operator signal are fixed or disabled, and runs are pinned and interleaved to limit machine noise.
• A simulation stage comes before real fuzzing, and the week-3 gate has a concrete criterion for whether operator families differ enough to study.
• The project is positioned against existing bandit-based mutation scheduling.
1. Problem and hypothesis
When software moves from version v to v+1, a fuzzer can either reuse the operator preferences it learned on v or reset and learn again. Reuse may speed up early exploration if the program behaves similarly. It may also impose outdated beliefs that suppress newly useful operators.
Hypothesis. An adaptive policy that chooses between transferred and fresh mutation models can approach the benefit of transfer when old knowledge stays useful, and reduce its cost when old knowledge misleads.
This splits into two empirical questions, and we do not assume either answer is yes:
1. Does previous-version experience predict mutation effectiveness on the new version, and for how long into the campaign?
2. When that usefulness varies across transitions, can a lightweight controller exploit the variation better than always transferring or always resetting?
If transfer almost always helps, the controller only adds wasted exploration. If transfer rarely helps, fresh-only is enough. Both are reportable outcomes.
Relation to prior work. Bandit-based mutation scheduling within a single campaign is established, for example Thompson sampling over operators (Karamcheti et al., 2018) and MOpt's operator scheduling (USENIX Security 2019). Our contribution is narrower: the cross-version question, and adaptive selection between inherited and fresh beliefs. In continuous fuzzing, the inherited corpus likely carries most transferred value. We therefore hold the corpus fixed across policies and isolate the effect of transferred operator preferences.
2. Actions, reward, and objective
The operator set is A = {a1, ..., aK}, grouped into families such as bit/byte flips, arithmetic, block insertion/deletion, interesting values, and dictionary insertion. We use roughly K = 6 to 10 families.
What one action is. Stock havoc stacks several randomly chosen operators per execution, which makes credit ambiguous. We replace that choice with a single selected family: one execution applies a random stack depth of mutations, all from family a_t. Credit is then unambiguous, and stacking behaviour is preserved.
Reward. Each execution yields a binary reward:
r_t = \begin{cases} 1 & \text{if the execution finds coverage unseen by the whole campaign} \\ 0 & \text{otherwise} \end{cases}
"Unseen" is campaign-wide, regardless of which model recommended the mutation, so both models pursue the same objective. We also log the number of new edges per success, for evaluation only.
Exact definition of a success. AFL-style fuzzers count an input as interesting if it reaches a new edge or a new hit-count bucket on a known edge. We set r_t = 1 exactly when the fuzzer would add the input to its corpus on either ground. The same definition is used in the simulation, the controller, and the evaluation. New edges alone are logged separately for the coverage metrics.
Statistical model. Each operator has an unknown success probability, r_t | a_t = a ~ Bernoulli(theta_a). This is an approximation: real productivity depends on the seed and on coverage already found, and it falls over time.
Objective. Maximise coverage-expanding executions within a fixed wall-clock budget. The controller adds per-execution sampling overhead, so policies will not run equal numbers of executions; wall-clock time is what a fuzzing user pays for, and we report executions per second for every policy. In the simplified model, with T executions:
\max_{\pi} \; \mathbb{E}_{\pi}\left[\sum_{t=1}^{T} r_t\right]
Total edge coverage is evaluated separately, since one success may find one edge or many. Bugs are the ultimate motivation but too sparse to be the learning signal; we report them where they occur.
3. Fresh and transfer models
Each model m in {F, T} keeps a Beta belief over each operator's success probability, theta_{m,a} ~ Beta(alpha_{m,a}, beta_{m,a}). Its mean is alpha / (alpha + beta); a larger alpha + beta at the same mean means more confidence.
Fresh model. Every operator starts at a common baseline, Beta(alpha_0, beta_0), with alpha_0 = beta_0 = 1. This uniform prior expresses ignorance, not a belief that half of mutations succeed.
Transfer model with a capped prior. On version v, operator a recorded s_a successes and f_a failures, with n_a = s_a + f_a. Fuzzers run thousands of executions per second, so n_a can reach millions. Adding those counts directly would freeze the transfer model. We keep the old mean but cap its weight at an effective sample size N:
\hat p_a = \frac{s_a + \alpha_0}{n_a + \alpha_0 + \beta_0}, \qquad N_a = \min(N, n_a)
\theta_{T,a} \sim \operatorname{Beta}\big(\alpha_0 + N_a \hat p_a,\; \beta_0 + N_a (1 - \hat p_a)\big)
N has a direct reading: old evidence is worth N new observations of that operator. The default is N = 500; the simulation confirms or adjusts it before any real runs. A sensitivity analysis uses N in {50, 500, 5000}; N = 0 makes the two models identical and serves as a sanity check.
One caveat: old rates come from a mature campaign, so they understate early success on the new version. The prior encodes the ranking of operators better than their scale. A sensitivity check rescales the p-hat values so their mean matches the fresh model's early-campaign rate.
Building an unbiased prior. If the version-v campaign used Thompson sampling, it would rarely try operators that looked bad early, leaving their estimates thin and possibly wrong. We therefore collect the old counts under uniform random operator choice, so every family gets comparable evidence. Only the first hour of each base run feeds the prior, so saturated late-campaign rates do not dominate.
We make three independent base runs per transition. Each trial on v+1 draws its prior from one of them in rotation, so the randomness of the base campaign shows up in trial-to-trial variance.
Two controls for what the prior carries. A transfer win could come from version-specific knowledge or merely from a better-calibrated scale than Beta(1, 1). Two extra baselines separate these explanations:
• Calibrated fresh: every operator gets the same prior, centred on the mean old success rate with weight N. It has the right scale but no ranking.
• Shuffled transfer: the real old rates, randomly reassigned to operators, with weight N. It has the right scale and spread but the wrong ranking.
Transfer is credited with version-specific knowledge only if it beats both controls.
4. Two-level Thompson sampling controller
The outer controller picks which model to follow for the next batch; the chosen model picks an operator for each execution in that batch.
Batching. Success rates per execution may be near 10^-3 or lower, so per-execution model choices would learn very slowly and add overhead. The controller decides once per batch of B = 256 executions. A sensitivity check uses B in {64, 1024}.
Controller belief. Let q_m be the success rate of following model m. The controller keeps q_m ~ Beta(u_m, v_m), with u_m = v_m = 1 initially for both models.
At the start of batch k, it samples one value per model and follows the larger:
\tilde q_m \sim \operatorname{Beta}(u_m, v_m), \qquad m_k = \arg\max_{m \in \{F,T\}} \tilde q_m
For each execution in the batch, model m_k samples every operator's success probability and recommends the largest:
\tilde\theta_a \sim \operatorname{Beta}(\alpha_{m_k,a}, \beta_{m_k,a}), \qquad a_t = \arg\max_{a \in \mathcal{A}} \tilde\theta_a
Discounting. Reward rates fall sharply as easy coverage is used up. Without discounting, whichever model happened to be chosen early keeps credit from that easy phase. After each batch, both models' controller counts decay toward the prior with factor gamma:
u_m \leftarrow 1 + \gamma (u_m - 1), \qquad v_m \leftarrow 1 + \gamma (v_m - 1)
The main setting is gamma = 0.98, an effective memory of about 50 batches. Sensitivity uses gamma in {1.0, 0.95}; gamma = 1.0 recovers the undiscounted design from the first draft.
5. Learning updates and model convergence
There are two updates, at different levels and with different recipients.
Level
What it estimates
Who is updated
When
Operator models
Productivity of operator a on version v+1
Both F and T, for the executed operator
After every execution
Controller
Productivity of following model m
Only the model chosen for the batch
After every batch, then discounted
Operator level. For the executed operator a_t, both models add r_t to alpha and 1 - r_t to beta. They see identical evidence and differ only in their priors.
Controller level. If batch k produced S_k successes, the chosen model gets u += S_k and v += B - S_k. The other model's counterfactual reward is unobserved, so it gets no credit.
The models converge, and we measure it. Shared updates dilute the transfer prior over time. After roughly N executions of an operator, the two models' beliefs about it are close, so the controller's choice matters mostly early in a campaign.
We log the total-variation distance between the two models' recommendation distributions at regular intervals. This tells us how long transfer has a distinct effect, and frames the early-campaign focus of the evaluation.
One consequence: the fresh model inside the adaptive policy also learns from transfer-chosen actions. It is therefore not identical to the fresh-only baseline, which we state when interpreting results.
6. Stage 1: simulation study
Before real fuzzing, we run all policies on a synthetic K-armed Bernoulli bandit where we control the shift between versions. This verifies the implementation and gives a noise-free answer to question 2.
Each simulated "version" assigns success rates to K = 8 operators, at fuzzing-like magnitudes (10^-4 to 10^-2). Rates decay over the campaign to mimic coverage saturation. The transfer prior is built from a simulated campaign on the old rates.
Scenario
Shift from old to new version
Expected best fixed policy
No shift
Identical rates
Transfer-only
Mild shift
Best operator unchanged; others perturbed
Transfer-only, narrowly
Reversal
Old best becomes weak; a weak operator becomes best
Fresh-only
Saturation only
Same rates, but the new campaign starts with lower rates overall
Unclear; mirrors the same-version restart control
We measure cumulative successes, regret against an oracle that knows the true rates, the share of batches given to the transfer model over time, and the time to recover after a reversal.
The simulation also runs the sensitivity grids for N, gamma, and B, which are too expensive to sweep fully in real fuzzing. We then fix their values for Stage 2 before any real runs.
The simulation includes the calibrated-fresh and shuffled-transfer controls from section 3. In the "no shift" scenario, real transfer should beat both; if it does not, the prior construction needs fixing before Stage 2.
7. Stage 2: real fuzzing experiments
Implementation. We implement the policies as a scheduler in LibAFL, whose modular mutator and scheduler design makes the swap straightforward. An AFL++ custom mutator is the fallback.
Targets. Three programs with real version histories, for example libpng, libxml2, and libtiff, with two transitions each. For each program we pick one small transition (few changed functions) and one large transition (substantial parsing changes), measured by the diff. Six transitions in total.
Protocol per transition.
1. Run three independent 6-hour campaigns on version v with uniform random operator choice. Save each corpus and the per-operator counts from its first hour.
2. Build the transfer, calibrated-fresh, and shuffled-transfer priors from those counts, as in section 3.
3. Run each policy on version v+1 for 4 hours of wall-clock time, 10 independent trials, all starting from the same inherited corpus. Trials rotate through the three base-run priors.
4. Replay the corpus at the start and record its coverage separately, so only discoveries from new mutations are credited to a policy.
Policies.
Policy
Behaviour
Purpose
Fresh-only
Always follow F, prior Beta(1, 1)
Reset baseline
Calibrated fresh
Always follow F, uniform prior at the old mean rate
Is any well-scaled prior enough?
Shuffled transfer
Always follow T, old rates reassigned at random
Does the old ranking matter?
Transfer-only
Always follow T
Reuse baseline
Adaptive
Discounted two-level Thompson sampling
The proposed method
Fixed 50/50
Pick F or T at random per batch, same updates
Does learning the choice add value beyond mixing?
Stock havoc was dropped as a reference point to pay for the two new controls. It can return as a single 10-trial run per transition if compute allows.
Same-version restart control. We also restart fresh-only, transfer-only, and adaptive on version v itself, from the saved corpus. If transfer loses value here too, the cause is corpus maturity rather than the software change.
Primary outcome, fixed in advance. Edge coverage at 1 hour, adaptive versus transfer-only, across all six transitions. A pre-specified secondary analysis splits transitions by whether transfer-only beat fresh-only. Every other metric and comparison below is secondary and reported as such. This limits false positives from the many metric, time point, policy, and transition combinations.
Metrics. Edge coverage at 15 minutes, 1 hour, and 4 hours; area under the coverage curve; coverage-expanding executions; the share of batches given to T over time; model divergence over time; and any unique crashes, deduplicated by stack hash.
Statistics. Following Klees et al. ("Evaluating Fuzz Testing," CCS 2018), we report medians with interquartile ranges over 10 trials. Pairwise comparisons use the Mann-Whitney U test with Vargha-Delaney A12 effect sizes, corrected for multiple comparisons.
Fuzzer configuration. CmpLog/Redqueen, automatic dictionary extraction, and the corpus power schedule all change what an operator can achieve. Automatic dictionaries can also differ between versions, which would make "dictionary insertion" a different operator on v and v+1. We disable CmpLog and automatic dictionaries, use one fixed hand-written dictionary per program for both versions, and keep the same corpus scheduler for every policy. This trades some realism for a cleaner signal, which we state as a limitation.
Run hygiene. Each campaign is pinned to its own core, with CPU frequency scaling and turbo boost disabled where possible. Trials of every configuration are interleaved in the run order, so no policy consistently runs while the machine is busier.
8. Timeline and compute budget
The plan front-loads the simulation and a one-transition pilot, so the expensive main runs start only with settings already fixed.
The gate at the end of week 3 checks that the scheduler runs at normal speed, rewards are logged correctly, and operator families actually differ. Concretely, in the pilot's uniform-choice base runs, the best family's success rate should be at least twice the median family's. If all families perform alike, no policy can gain much, and a null result would say nothing about transfer. If any check fails, we adjust or cut scope before spending the main compute.
Item
Count
Transitions
6 (3 programs × 2)
Configurations per transition
9 (6 cross-version policies + 3 same-version controls)
Trials per configuration
10
Campaign length
4 hours
Main runs
about 2,160 core-hours
Base runs on version v
3 per transition × 6 hours = 108 core-hours
Total
about 2,270 core-hours
On a 32-core machine, that is about 3 days of wall-clock time. If compute is tighter, we cut to 4 transitions or 2-hour campaigns, not fewer trials. Early-campaign effects remain measurable either way.
9. Course connection, limitations, and what counts as a result
Course techniques. Bayesian inference represents uncertain operator and model productivity. Sequential decision-making and Thompson sampling balance exploration and exploitation at two levels. Transfer learning enters as prior information with a controlled strength. Model evaluation tests whether these approximations still support good decisions.
Limitations. The main one is nonstationarity: coverage is consumed, the corpus changes, and both operator models keep learning. So q_F, q_T, and theta_a are not fixed, and stationary-bandit guarantees do not apply. Discounting is a practical response, not a guarantee. Other limits are a small number of targets and transitions, coverage as a proxy for bugs, and 4-hour campaigns that say little about long-run behaviour.
What would establish a useful result.
• Strong: across most transitions, adaptive is statistically indistinguishable from transfer-only where transfer helps, and significantly better than transfer-only where it hurts. It should also beat the fixed 50/50 mix, and transfer-only should beat calibrated fresh and shuffled transfer, showing the benefit comes from version-specific knowledge.
• Partial: transfer clearly helps or hurts depending on the transition, but adaptive does not consistently capture the better side. This still answers question 1 and shows where the controller fails.
• Null: transfer has no measurable effect beyond the shared corpus. This is a useful negative finding about cross-version operator-preference transfer.
Beating fresh-only on a single transition is not enough to claim the controller is useful, since transfer-only might do just as well.
