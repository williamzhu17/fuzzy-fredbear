"""Stage 1 simulation: cross-version policy transfer on a synthetic K-armed Bernoulli bandit.

Implements sections 3-6 of the revised plan with numpy only.

Approximations (state these when reporting):
  * Within a batch of B executions, every execution samples from the operator posterior
    as it stood at the start of the batch (delayed feedback); counts are applied at batch end.
  * Rates follow a deterministic per-operator schedule (see `rates`):
        theta_a(t) = level * theta_a / (1 + t / tau_a) * exp(-S_a / pool_a)
    where tau_a is a fraction of the campaign length T and S_a is the number of successes
    operator a has found so far in this campaign (pool_a = inf disables depletion).
"""
import zlib

import numpy as np
from scipy.special import betaln, logsumexp, ndtri

K = 8
# Version-v ("old") per-execution success rates, fuzzing-like magnitudes.
OLD_RATES = np.array([1e-2, 5e-3, 3e-3, 2e-3, 1e-3, 5e-4, 2e-4, 1e-4])
# Harder scenarios: the top operators are close together.
CLOSE_RATES = np.array([4e-3, 3.5e-3, 3e-3, 2.5e-3, 1.5e-3, 1e-3, 5e-4, 2e-4])


# ---------------------------------------------------------------- scenarios
def spec(theta, tau=0.05, pool=np.inf, level=1.0):
    return dict(theta=np.asarray(theta, float), tau=np.broadcast_to(np.asarray(tau, float), (K,)).copy(),
                pool=np.broadcast_to(np.asarray(pool, float), (K,)).copy(), level=float(level))


def scenario_seed(name):
    """Seed derived from the scenario name, so a scenario reproduces whatever else is in the run."""
    return 1000 + zlib.crc32(name.encode()) % 1_000_000


def rank_rates(base, rho, draw):
    """Permute `base` so the new ranking has rank correlation ~rho with the old one (Gaussian copula).

    The set of rates is unchanged, so only the ranking shifts, not the scale. Draw d uses the same
    noise for every rho, so curves over rho are paired.
    """
    order = np.argsort(-base)  # old best first
    x = np.empty(K)
    x[order] = ndtri((K - np.arange(K) - 0.5) / K)  # normal scores, best operator highest
    eps = np.random.default_rng([draw, 7]).normal(size=K)
    y = rho * x + np.sqrt(max(0.0, 1 - rho ** 2)) * eps
    new = np.empty(K)
    new[np.argsort(-y)] = np.sort(base)[::-1]
    return new


def make_scenario(name, new_level=1.0, seed=12345):
    """Return (old_spec, new_spec); new_level multiplies v+1's rates (inherited-corpus start)."""
    old, new = _make_scenario(name, seed)
    new["level"] *= new_level
    return old, new


def _make_scenario(name, seed):
    rng = np.random.default_rng(seed)
    old = OLD_RATES.copy()
    if name == "no_shift":
        return spec(old), spec(old)
    if name == "mild_shift":
        new = old.copy()
        new[1:] = old[1:] * np.exp(rng.normal(0, 0.7, K - 1))
        new[1:] = np.minimum(new[1:], 0.8 * old[0])  # best operator unchanged
        return spec(old), spec(new)
    if name == "reversal":
        new = old.copy()
        new[0], new[6] = old[6], old[0]  # old best becomes weak, a weak one becomes best
        return spec(old), spec(new)
    if name == "saturation":
        return spec(old), spec(old, level=0.2)  # same rates, new campaign starts lower
    c = CLOSE_RATES.copy()
    if name == "close_no_shift":
        return spec(c), spec(c)
    if name == "close_reversal":
        new = c.copy()
        new[0], new[3], new[4] = c[4], c[0], c[3]  # old best drops to 5th, old 4th becomes best
        return spec(c), spec(new)
    if name == "late_riser":
        # Op 3 starts 5th on v+1 but decays 10x slower (new code keeps paying), overtaking op 0 at ~27 min.
        new = c.copy()
        new[3] = 1.5e-3
        tau = np.full(K, 0.05)
        tau[3] = 0.5
        return spec(c), spec(new, tau=tau)
    if name == "depletion":
        # Finite coverage pools on v+1; the inherited corpus already covers most of op 0's region.
        return spec(c), spec(c, pool=[30, 400, 400, 400, 300, 200, 100, 50])
    if name.startswith(("rank_", "rankc_")):
        # rank_<rho>_<draw> on OLD_RATES, rankc_<rho>_<draw> on CLOSE_RATES
        kind, rho, draw = name.split("_")
        base = OLD_RATES if kind == "rank" else CLOSE_RATES
        return spec(base), spec(rank_rates(base, float(rho), int(draw)))
    raise ValueError(name)


def rates(sp, t, T, S):
    """Current true success rate of each operator; S has shape (..., K)."""
    r = sp["level"] * sp["theta"] / (1.0 + t / (sp["tau"] * T)) * np.exp(-S / sp["pool"])
    return np.minimum(r, 1.0)


# ---------------------------------------------------------------- base runs and priors
def base_run_counts(rng, sp, n_exec, B, T):
    """Uniform-random operator choice; returns (s, n) per operator for the first n_exec executions."""
    s = np.zeros(K)
    n = np.zeros(K)
    for k in range(n_exec // B):
        nk = rng.multinomial(B, np.full(K, 1.0 / K))
        s += rng.binomial(nk, rates(sp, k * B, T, s))
        n += nk
    return s, n


def build_priors(s, n, N, a0=1.0, b0=1.0, rng=None):
    """Capped transfer prior plus the calibrated-fresh and shuffled-transfer controls."""
    p_hat = (s + a0) / (n + a0 + b0)
    Na = np.minimum(N, n)
    transfer = (a0 + Na * p_hat, b0 + Na * (1 - p_hat))
    pm = p_hat.mean()
    calib = (a0 + Na * pm, b0 + Na * (1 - pm))
    Nw = np.minimum(50, n)  # weakly calibrated: right scale, little confidence
    calib_weak = (a0 + Nw * pm, b0 + Nw * (1 - pm))
    perm = rng.permutation(K)
    shuffled = (a0 + Na * p_hat[perm], b0 + Na * (1 - p_hat[perm]))
    fresh = (np.full(K, a0), np.full(K, b0))
    return dict(fresh=fresh, transfer=transfer, calib=calib, calib_weak=calib_weak, shuffled=shuffled)


# ---------------------------------------------------------------- campaign
POLICIES = {
    # name: (models, chooser)
    "fresh":    (("fresh",), "fixed"),
    "calib":    (("calib",), "fixed"),
    "shuffled": (("shuffled",), "fixed"),
    "transfer": (("transfer",), "fixed"),
    "adaptive": (("fresh", "transfer"), "ts"),
    "mix50":    (("fresh", "transfer"), "random"),
    "mix50_cal": (("calib", "transfer"), "random"),  # matched coin-flip control for bmc*_cal
    # Bayesian model comparison: P(T | data) from each prior's Beta-Binomial marginal likelihood
    # on all shared evidence. bmc samples a model per batch; bma samples a mixture component per execution.
    "bmc":      (("fresh", "transfer"), "bmc"),
    "bma":      (("fresh", "transfer"), "bma"),
    # Same, but the competing hypothesis is a scale-matched prior with no ranking, so the
    # comparison measures whether the old *ranking* holds rather than whether Beta(1,1) is miscalibrated.
    "bmc_cal":  (("calib", "transfer"), "bmc"),
    "bma_cal":  (("calib", "transfer"), "bma"),
    "bmc_calw": (("calib_weak", "transfer"), "bmc"),
    "bma_calw": (("calib_weak", "transfer"), "bma"),
    # Scale-invariant comparison: each hypothesis is "rates = c * prior mean" with c unknown and
    # marginalised, so only the ranking/shape is tested. _r also acts with the prior rescaled to its fitted c.
    "bmcs_cal":   (("calib", "transfer"), "bmc_si"),
    "bmcs_cal_r": (("calib", "transfer"), "bmc_si_r"),
    # Same comparison (calib vs transfer, scale-invariant), but when T is not chosen act with Beta(1,1)
    # instead of calib, whose old-version scale is too optimistic when v+1 starts lower.
    "bmcs_cf":    (("calib", "transfer", "fresh"), "bmc_si_f"),
    # Matched control for bmcs_cal_r: same rescaling to the fitted c, but C or T chosen by coin flip.
    "mix50_cal_r": (("calib", "transfer"), "random_si_r"),
}


def log_marginal(a0, b0, s, f):
    """Beta-Binomial log marginal likelihood of per-operator counts, summed over operators."""
    return (betaln(a0 + s, b0 + f) - betaln(a0, b0)).sum(-1)


LOGC = np.linspace(np.log(1 / 30), np.log(30), 61)  # global scale grid, uniform prior on log c


def scaled_prior(a0, b0, logc):
    """Prior with the same weight W = a0 + b0 but mean multiplied by exp(logc) (capped at 0.5)."""
    W = a0 + b0
    m = np.minimum(np.exp(logc) * a0 / W, 0.5)
    return W * m, W * (1 - m)


def log_marginal_scaled(a0, b0, s, f):
    """Scale-invariant log marginal likelihood: integrate log c over LOGC.

    Returns (log ML, posterior mean of log c), each with the leading shape of a0 minus the operator axis.
    """
    lc = LOGC.reshape((-1,) + (1,) * a0.ndim)
    a, b = scaled_prior(a0[None], b0[None], lc)
    ll = log_marginal(a, b, s, f)  # (G, ...)
    lml = logsumexp(ll, axis=0) - np.log(len(LOGC))
    post = np.exp(ll - logsumexp(ll, axis=0, keepdims=True))
    return lml, (post * LOGC.reshape((-1,) + (1,) * (ll.ndim - 1))).sum(0)


def run_policy(policy, scenario, R=30, T=1_000_000, B=256, N=500, gamma=0.98,
               n_base=3, seed=0, tv_every=50, tv_draws=1000, new_level=1.0, tv_pair=("calib", "transfer")):
    """Run R independent trials of one policy on one scenario. Returns a dict of arrays.

    tv_pair: the two priors whose posterior recommendation distributions are compared for "tv".
    """
    rng = np.random.default_rng(seed)
    old, new = make_scenario(scenario, new_level)

    # Three uniform-choice base runs on the old version, first "hour" (= T/4) only.
    base = [base_run_counts(rng, old, T // 4, B, T) for _ in range(n_base)]
    priors = [build_priors(s, n, N, rng=rng) for s, n in base]
    # Shuffled control: fresh permutation per trial (rebuild from its base run).
    model_names, chooser = POLICIES[policy]
    M = len(model_names)
    pa = np.zeros((M, R, K))
    pb = np.zeros((M, R, K))
    tva = np.zeros((2, R, K))  # tv_pair priors, for divergence logging
    tvb = np.zeros((2, R, K))
    for r in range(R):
        s, n = base[r % n_base]
        pr = build_priors(s, n, N, rng=rng) if "shuffled" in model_names else priors[r % n_base]
        for m, name in enumerate(model_names):
            pa[m, r], pb[m, r] = pr[name]
        for j, name in enumerate(tv_pair):
            tva[j, r], tvb[j, r] = pr[name]

    s = np.zeros((R, K))  # shared operator evidence on v+1
    f = np.zeros((R, K))
    u = np.ones((M, R))   # controller beliefs
    v = np.ones((M, R))
    nb = T // B
    checkpoints = {max(1, nb // 16): "15m", max(1, nb // 4): "1h", nb: "4h"}
    succ_cum = np.zeros(R)
    exp_cum = np.zeros(R)
    oracle_cum = 0.0
    oS = np.zeros(K)      # greedy oracle's own campaign state (matters only with depletion)
    out = {k: {} for k in ("succ", "expected", "oracle")}
    share_T = np.zeros((R, nb))
    post_T = np.full((R, nb), np.nan)  # P(T | data) at the start of each batch (bmc / bma only)
    best_share = np.zeros((R, nb))
    tv_t, tv = [], []
    ridx = np.arange(R)

    for k in range(nb):
        t = k * B
        rt = rates(new, t, T, s)  # (R, K): depends on each trial's own successes under depletion
        # Outer controller
        if chooser == "fixed":
            mk = np.zeros(R, dtype=int)
        elif chooser == "random":
            mk = rng.integers(0, M, R)
        elif chooser == "ts":
            mk = np.argmax(rng.beta(u, v), axis=0)
        else:
            if chooser in ("bmc", "bma"):
                lml = log_marginal(pa, pb, s, f)  # (M, R)
            else:
                lml, mlogc = log_marginal_scaled(pa[:2], pb[:2], s, f)
            wT = 1.0 / (1.0 + np.exp(np.clip(lml[0] - lml[1], -700, 700)))
            post_T[:, k] = wT  # for random_si_r: what the evidence says, not what is followed
            mk = (rng.random(R) < (0.5 if chooser == "random_si_r" else wT)).astype(int)
        if chooser == "bma":
            comp = rng.random((R, B)) < wT[:, None]
            dF = rng.beta((pa[0] + s)[:, None, :], (pb[0] + f)[:, None, :], size=(R, B, K))
            dT = rng.beta((pa[1] + s)[:, None, :], (pb[1] + f)[:, None, :], size=(R, B, K))
            draws = np.where(comp[:, :, None], dT, dF)
        elif chooser in ("bmc_si_r", "random_si_r"):
            sa, sb = scaled_prior(pa, pb, mlogc[..., None])
            alpha = sa[mk, ridx] + s
            beta = sb[mk, ridx] + f
            draws = rng.beta(alpha[:, None, :], beta[:, None, :], size=(R, B, K))
        else:
            act = np.where(mk == 1, 1, 2) if chooser == "bmc_si_f" else mk
            alpha = pa[act, ridx] + s
            beta = pb[act, ridx] + f
            draws = rng.beta(alpha[:, None, :], beta[:, None, :], size=(R, B, K))
        acts = draws.argmax(axis=2)
        n_k = np.stack([(acts == a).sum(1) for a in range(K)], axis=1)
        succ = rng.binomial(n_k, rt)
        s += succ
        f += n_k - succ
        S = succ.sum(1)
        # Controller update for the chosen model only, then discount both toward the prior.
        if chooser == "ts":
            u[mk, ridx] += S
            v[mk, ridx] += B - S
            u = 1 + gamma * (u - 1)
            v = 1 + gamma * (v - 1)
        succ_cum += S
        exp_cum += (n_k * rt).sum(1)
        ort = rates(new, t, T, oS)
        oracle_cum += B * ort.max()
        oS[ort.argmax()] += B * ort.max()
        if chooser == "bma":
            share_T[:, k] = comp.mean(1)
        elif M >= 2:
            share_T[:, k] = mk == 1
        elif model_names[0] == "transfer":
            share_T[:, k] = 1
        best_share[:, k] = n_k[ridx, rt.argmax(1)] / B
        if k + 1 in checkpoints:
            c = checkpoints[k + 1]
            out["succ"][c] = succ_cum.copy()
            out["expected"][c] = exp_cum.copy()
            out["oracle"][c] = oracle_cum
        if k % tv_every == 0:
            rec = []
            for j in range(2):
                d = rng.beta((tva[j] + s)[:, None, :], (tvb[j] + f)[:, None, :], size=(R, tv_draws, K))
                a = d.argmax(2)
                rec.append(np.stack([(a == i).mean(1) for i in range(K)], axis=1))
            tv_t.append(t)
            tv.append(0.5 * np.abs(rec[0] - rec[1]).sum(1))

    out["share_T"] = share_T
    out["post_T"] = post_T
    out["best_share"] = best_share
    out["tv_t"] = np.array(tv_t)
    out["tv"] = np.array(tv).T  # (R, n_tv)
    out["B"] = B
    return out


# ---------------------------------------------------------------- statistics
def mann_whitney(x, y):
    """Two-sided Mann-Whitney U (normal approximation with tie correction). Returns (U, p)."""
    from math import erfc, sqrt
    x, y = np.asarray(x, float), np.asarray(y, float)
    n1, n2 = len(x), len(y)
    allv = np.concatenate([x, y])
    order = allv.argsort(kind="mergesort")
    ranks = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    U = ranks[:n1].sum() - n1 * (n1 + 1) / 2
    _, cnt = np.unique(allv, return_counts=True)
    n = n1 + n2
    var = n1 * n2 / 12 * ((n + 1) - (cnt ** 3 - cnt).sum() / (n * (n - 1)))
    if var == 0:
        return U, 1.0
    z = (U - n1 * n2 / 2) / sqrt(var)
    return U, erfc(abs(z) / sqrt(2))


def a12(x, y):
    """Vargha-Delaney A12: P(X > Y) + 0.5 P(X = Y)."""
    x, y = np.asarray(x)[:, None], np.asarray(y)[None, :]
    return float((x > y).mean() + 0.5 * (x == y).mean())


def holm(pvals):
    p = np.asarray(pvals)
    order = p.argsort()
    adj = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = running
    return adj
