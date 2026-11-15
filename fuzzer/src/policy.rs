//! Operator-family scheduling policies. A port of `sim/bandit_sim.py` (PLAN sections 3-4),
//! plus discounted Thompson sampling. No LibAFL types here, so it can be tested on its own.
//!
//! One deliberate difference from the simulator: counts update after every execution instead of
//! at batch end. The hypothesis (C or T) is still resampled once per batch.

use rand::rngs::StdRng;
use rand::{RngExt, SeedableRng};
use rand_distr::{Beta, Distribution};
use serde::{Deserialize, Serialize};

fn ln_beta(a: f64, b: f64) -> f64 {
    libm::lgamma(a) + libm::lgamma(b) - libm::lgamma(a + b)
}

/// Grid over log c (sim: `LOGC`): 61 points on [1/30, 30], uniform prior.
fn logc_grid() -> Vec<f64> {
    let (lo, hi) = ((1.0f64 / 30.0).ln(), 30.0f64.ln());
    (0..61).map(|i| lo + (hi - lo) * i as f64 / 60.0).collect()
}

#[derive(Clone, Debug)]
pub struct BetaPrior {
    pub a: Vec<f64>,
    pub b: Vec<f64>,
}

impl BetaPrior {
    /// Same weight a + b, mean multiplied by exp(logc), capped at 0.5 (sim: `scaled_prior`).
    fn scaled(&self, logc: f64) -> BetaPrior {
        let mut out = self.clone();
        for i in 0..self.a.len() {
            let w = self.a[i] + self.b[i];
            let m = (logc.exp() * self.a[i] / w).min(0.5);
            out.a[i] = w * m;
            out.b[i] = w * (1.0 - m);
        }
        out
    }

    /// Beta-Binomial log marginal likelihood, summed over families (sim: `log_marginal`).
    fn log_marginal(&self, s: &[f64], f: &[f64]) -> f64 {
        (0..self.a.len())
            .map(|i| ln_beta(self.a[i] + s[i], self.b[i] + f[i]) - ln_beta(self.a[i], self.b[i]))
            .sum()
    }

    /// Log marginal likelihood with log c integrated out over the grid, and the posterior mean
    /// of log c (sim: `log_marginal_scaled`).
    fn log_marginal_scaled(&self, s: &[f64], f: &[f64]) -> (f64, f64) {
        let grid = logc_grid();
        let ll: Vec<f64> = grid.iter().map(|&lc| self.scaled(lc).log_marginal(s, f)).collect();
        let max = ll.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let lse = max + ll.iter().map(|l| (l - max).exp()).sum::<f64>().ln();
        let mean_logc = ll.iter().zip(&grid).map(|(l, lc)| (l - lse).exp() * lc).sum();
        (lse - (grid.len() as f64).ln(), mean_logc)
    }
}

/// Per-family successes `s` out of `n` executions from uniform-choice base runs on version v.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct BaseCounts {
    pub families: Vec<String>,
    pub s: Vec<f64>,
    pub n: Vec<f64>,
}

impl BaseCounts {
    pub fn validate(&self, families: &[&str]) -> Result<(), String> {
        if self.families != families {
            return Err(format!("base counts are for families {:?}, expected {:?}", self.families, families));
        }
        if self.s.len() != families.len() || self.n.len() != families.len() {
            return Err("base counts: s and n must have one entry per family".into());
        }
        if self.s.iter().zip(&self.n).any(|(s, n)| *s < 0.0 || s > n) {
            return Err("base counts: need 0 <= s <= n for every family".into());
        }
        Ok(())
    }
}

/// The priors of PLAN section 3 (sim: `build_priors`).
#[derive(Clone, Debug)]
pub struct PriorSet {
    pub fresh: BetaPrior,
    pub calib: BetaPrior,
    pub transfer: BetaPrior,
    pub shuffled: BetaPrior,
}

impl PriorSet {
    /// `cap_n` is N: old evidence is worth at most N new observations per family.
    pub fn build(base: &BaseCounts, cap_n: f64, shuffle_seed: u64) -> PriorSet {
        let k = base.s.len();
        let p_hat: Vec<f64> = (0..k).map(|i| (base.s[i] + 1.0) / (base.n[i] + 2.0)).collect();
        let p_mean = p_hat.iter().sum::<f64>() / k as f64;
        let mut perm: Vec<usize> = (0..k).collect();
        let mut rng = StdRng::seed_from_u64(shuffle_seed);
        for i in (1..k).rev() {
            perm.swap(i, rng.random_range(0..=i));
        }
        let prior = |p: Vec<f64>| BetaPrior {
            a: (0..k).map(|i| 1.0 + base.n[i].min(cap_n) * p[i]).collect(),
            b: (0..k).map(|i| 1.0 + base.n[i].min(cap_n) * (1.0 - p[i])).collect(),
        };
        PriorSet {
            fresh: BetaPrior { a: vec![1.0; k], b: vec![1.0; k] },
            calib: prior(vec![p_mean; k]),
            shuffled: prior(perm.iter().map(|&j| p_hat[j]).collect()),
            transfer: prior(p_hat),
        }
    }

    /// For policies that use no prior (uniform, fresh).
    pub fn flat(k: usize) -> PriorSet {
        let p = BetaPrior { a: vec![1.0; k], b: vec![1.0; k] };
        PriorSet { fresh: p.clone(), calib: p.clone(), transfer: p.clone(), shuffled: p }
    }
}

/// Simulator names in brackets.
#[derive(Clone, Copy, Debug, PartialEq, clap::ValueEnum)]
pub enum PolicyKind {
    /// Uniform random family; used for base runs on version v.
    Uniform,
    /// Thompson sampling from Beta(1,1) [fresh].
    Fresh,
    /// Calibrated fresh: old mean rate for every family [calib].
    Calib,
    /// Transfer prior with the old rates shuffled across families [shuffled].
    Shuffled,
    /// Transfer prior [transfer].
    Transfer,
    /// Scale-invariant model comparison C vs T, acting at the fitted scale [bmcs_cal_r].
    Adaptive,
    /// Same comparison, acting with the unscaled prior [bmcs_cal].
    AdaptiveUnscaled,
    /// Coin flip between C and T each batch, same rescaling [mix50_cal_r].
    Mix50,
    /// Discounted Thompson sampling: the transfer prior decays toward calib by gamma_prior per
    /// batch, and observed counts decay by gamma_data per batch. Not in the simulator yet.
    Dts,
}

pub struct PolicyConfig {
    pub kind: PolicyKind,
    pub batch: u64,
    pub gamma_prior: f64,
    pub gamma_data: f64,
}

/// One line of the per-batch log.
#[derive(Clone, Debug, Serialize)]
pub struct BatchRecord {
    pub batch: u64,
    /// "calib", "transfer" or "" (single-prior policies).
    pub followed: &'static str,
    /// P(H_T | D) at batch start, for the model-comparison policies.
    pub post_t: Option<f64>,
    /// Posterior mean of log c under the followed hypothesis, for the rescaled policies.
    pub logc: Option<f64>,
    /// Executions and successes per family in this batch.
    pub n: Vec<u64>,
    pub s: Vec<u64>,
}

pub struct Policy {
    cfg: PolicyConfig,
    priors: PriorSet,
    rng: StdRng,
    /// Counts on this version. For DTS they are discounted; all other policies never discount.
    s: Vec<f64>,
    f: Vec<f64>,
    /// DTS: remaining weight of the transfer prior's offset from calib.
    prior_w: f64,
    /// Beta parameters (before counts) that the current batch samples from.
    act: BetaPrior,
    rec: BatchRecord,
}

impl Policy {
    pub fn new(cfg: PolicyConfig, priors: PriorSet, seed: u64) -> Policy {
        let k = priors.fresh.a.len();
        let mut policy = Policy {
            cfg,
            act: priors.fresh.clone(),
            priors,
            rng: StdRng::seed_from_u64(seed),
            s: vec![0.0; k],
            f: vec![0.0; k],
            prior_w: 1.0,
            rec: BatchRecord { batch: 0, followed: "", post_t: None, logc: None, n: vec![0; k], s: vec![0; k] },
        };
        policy.start_batch(0);
        policy
    }

    /// Pick the family for the next execution, skipping families in `exclude`.
    /// Returns None if every family is excluded.
    pub fn choose(&mut self, exclude: &[usize]) -> Option<usize> {
        let allowed: Vec<usize> = (0..self.s.len()).filter(|a| !exclude.contains(a)).collect();
        if allowed.is_empty() {
            return None;
        }
        if self.cfg.kind == PolicyKind::Uniform {
            return Some(allowed[self.rng.random_range(0..allowed.len())]);
        }
        let mut best = (allowed[0], f64::NEG_INFINITY);
        for &a in &allowed {
            let draw = Beta::new(self.act.a[a] + self.s[a], self.act.b[a] + self.f[a])
                .expect("Beta parameters are positive")
                .sample(&mut self.rng);
            if draw > best.1 {
                best = (a, draw);
            }
        }
        Some(best.0)
    }

    /// Record one execution of family `a`. Returns the batch record when a batch completes.
    pub fn record(&mut self, a: usize, success: bool) -> Option<BatchRecord> {
        self.s[a] += success as u8 as f64;
        self.f[a] += !success as u8 as f64;
        self.rec.n[a] += 1;
        self.rec.s[a] += success as u64;
        if self.rec.n.iter().sum::<u64>() < self.cfg.batch {
            return None;
        }
        let done = self.rec.clone();
        if self.cfg.kind == PolicyKind::Dts {
            self.prior_w *= self.cfg.gamma_prior;
            for i in 0..self.s.len() {
                self.s[i] *= self.cfg.gamma_data;
                self.f[i] *= self.cfg.gamma_data;
            }
        }
        self.start_batch(done.batch + 1);
        Some(done)
    }

    fn start_batch(&mut self, batch: u64) {
        let k = self.s.len();
        let (mut followed, mut post_t, mut logc) = ("", None, None);
        self.act = match self.cfg.kind {
            PolicyKind::Uniform | PolicyKind::Fresh => self.priors.fresh.clone(),
            PolicyKind::Calib => self.priors.calib.clone(),
            PolicyKind::Shuffled => self.priors.shuffled.clone(),
            PolicyKind::Transfer => self.priors.transfer.clone(),
            PolicyKind::Dts => {
                // Decay toward calib, not Beta(1,1): Beta(1,1) expects ~50% success where real
                // rates are ~1e-3, so decaying toward it would force heavy exploration.
                let (c, t, w) = (&self.priors.calib, &self.priors.transfer, self.prior_w);
                BetaPrior {
                    a: (0..k).map(|i| c.a[i] + w * (t.a[i] - c.a[i])).collect(),
                    b: (0..k).map(|i| c.b[i] + w * (t.b[i] - c.b[i])).collect(),
                }
            }
            PolicyKind::Adaptive | PolicyKind::AdaptiveUnscaled | PolicyKind::Mix50 => {
                let (lml_c, logc_c) = self.priors.calib.log_marginal_scaled(&self.s, &self.f);
                let (lml_t, logc_t) = self.priors.transfer.log_marginal_scaled(&self.s, &self.f);
                let w_t = 1.0 / (1.0 + (lml_c - lml_t).clamp(-700.0, 700.0).exp());
                let p_follow_t = if self.cfg.kind == PolicyKind::Mix50 { 0.5 } else { w_t };
                let (prior, lc) = if self.rng.random::<f64>() < p_follow_t {
                    followed = "transfer";
                    (&self.priors.transfer, logc_t)
                } else {
                    followed = "calib";
                    (&self.priors.calib, logc_c)
                };
                post_t = Some(w_t);
                if self.cfg.kind == PolicyKind::AdaptiveUnscaled {
                    prior.clone()
                } else {
                    logc = Some(lc);
                    prior.scaled(lc)
                }
            }
        };
        self.rec = BatchRecord { batch, followed, post_t, logc, n: vec![0; k], s: vec![0; k] };
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    include!("policy_ref.rs");

    fn base() -> BaseCounts {
        BaseCounts {
            families: (0..8).map(|i| format!("f{i}")).collect(),
            s: vec![60.0, 30.0, 20.0, 12.0, 8.0, 5.0, 3.0, 1.0],
            n: vec![6000.0; 8],
        }
    }

    fn policy(kind: PolicyKind, batch: u64, gamma_prior: f64) -> Policy {
        let cfg = PolicyConfig { kind, batch, gamma_prior, gamma_data: 1.0 };
        Policy::new(cfg, PriorSet::build(&base(), 5000.0, 0), 1)
    }

    /// Run `execs` Bernoulli executions at the given true rates; return the last batch record.
    fn run(pol: &mut Policy, rates: &[f64], execs: usize) -> BatchRecord {
        let mut rng = StdRng::seed_from_u64(7);
        let mut last = None;
        for _ in 0..execs {
            let a = pol.choose(&[]).unwrap();
            last = pol.record(a, rng.random::<f64>() < rates[a]).or(last);
        }
        last.unwrap()
    }

    #[test]
    fn marginal_likelihood_matches_simulator() {
        let p = PriorSet::build(&base(), 5000.0, 0);
        let s = [5.0, 20.0, 4.0, 1.0, 2.0, 0.0, 3.0, 1.0];
        let f: Vec<f64> = s.iter().map(|x| 2000.0 - x).collect();
        let (lml_t, logc_t) = p.transfer.log_marginal_scaled(&s, &f);
        let (lml_c, logc_c) = p.calib.log_marginal_scaled(&s, &f);
        for (got, want) in [(lml_t, REF_LML_T), (logc_t, REF_LOGC_T), (lml_c, REF_LML_C), (logc_c, REF_LOGC_C)] {
            assert!((got - want).abs() < 1e-8 * want.abs().max(1.0), "{got} vs {want}");
        }
    }

    #[test]
    fn adaptive_rejects_reversed_ranking() {
        let rates = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 3e-3, 5e-3, 1e-2];
        let rec = run(&mut policy(PolicyKind::Adaptive, 256, 1.0), &rates, 200_000);
        assert!(rec.post_t.unwrap() < 0.05, "P(H_T|D) = {:?}", rec.post_t);
    }

    #[test]
    fn adaptive_keeps_ranking_at_lower_scale() {
        // Same ranking as the base counts, every rate 5x lower (inherited corpus).
        let rates = [2e-3, 1e-3, 6.7e-4, 4e-4, 2.7e-4, 1.7e-4, 1e-4, 3e-5];
        let rec = run(&mut policy(PolicyKind::Adaptive, 256, 1.0), &rates, 200_000);
        assert!(rec.post_t.unwrap() > 0.9, "P(H_T|D) = {:?}", rec.post_t);
        assert!(rec.logc.unwrap() < 0.0, "fitted log c = {:?}", rec.logc);
    }

    #[test]
    fn dts_prior_decays_to_calib() {
        let mut pol = policy(PolicyKind::Dts, 10, 0.5);
        for _ in 0..600 {
            pol.record(0, false);
        }
        let calib = PriorSet::build(&base(), 5000.0, 0).calib;
        for i in 0..8 {
            assert!((pol.act.a[i] - calib.a[i]).abs() < 1e-9);
        }
    }

    #[test]
    fn batch_record_counts_executions() {
        let mut pol = policy(PolicyKind::Transfer, 4, 1.0);
        assert!(pol.record(2, true).is_none());
        pol.record(2, false);
        pol.record(5, false);
        let rec = pol.record(2, false).unwrap();
        assert_eq!((rec.n[2], rec.s[2], rec.n[5]), (3, 1, 1));
        assert!(pol.record(0, false).is_none());
    }

    #[test]
    fn choose_respects_exclude() {
        let mut pol = policy(PolicyKind::Transfer, 256, 1.0);
        for _ in 0..100 {
            assert_ne!(pol.choose(&[0]), Some(0));
        }
        assert_eq!(pol.choose(&(0..8).collect::<Vec<_>>()), None);
    }

    #[test]
    fn validate_rejects_bad_base_counts() {
        let names: Vec<String> = (0..8).map(|i| format!("f{i}")).collect();
        let names: Vec<&str> = names.iter().map(|s| s.as_str()).collect();
        assert!(base().validate(&names).is_ok());
        assert!(base().validate(&names[..7]).is_err());
        let mut b = base();
        b.s[0] = 7000.0;
        assert!(b.validate(&names).is_err());
    }
}
