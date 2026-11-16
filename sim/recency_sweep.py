"""Recency-weighted prior sweep (README run 11).

Builds the v-derived priors (transfer, calib, shuffled) from recency-weighted base-run counts
(bandit_sim.base_run_counts, half_life in base-run executions) and compares each policy against
itself with the usual full-run prior. Two variants per half-life:
  decay  - recency-weighted counts for both the mean and the weight cap min(N, n);
  weight - full-run mean, weight capped at the recency-weighted count. Separates "more recent"
           from "weaker" (a short memory also means fewer effective executions).

Usage:
  python recency_sweep.py --out results/recency            # run (resumes if raw.pkl exists)
  python recency_sweep.py --out results/recency --report   # summary.md from raw.pkl only
"""
import argparse
import os
import pickle
import time
from multiprocessing import Pool

import numpy as np
from scipy.stats import spearmanr

import bandit_sim as bs

HERE = os.path.dirname(os.path.abspath(__file__))
DRIFT = ["drift_swap_late", "drift_swap_early", "drift_geom_late", "drift_geom_early"]
CONTROL = ["no_shift", "mild_shift", "reversal", "close_no_shift", "close_reversal"]
RANK = [f"{b}_{rho:g}_{d}" for b in ("rank", "rankc") for rho in (1, 0.5, 0, -1) for d in (0, 1)]
POLICIES = ["transfer", "bmcs_cal_r", "mix50_cal_r"]
REFERENCE = ["fresh", "calib"]  # full-run prior only, for context
HALF_LIVES = [64000, 16000, 4000]
SLIM = ("succ", "expected", "oracle", "share_T")


def variants():
    return [(None, "decay")] + [(h, m) for m in ("decay", "weight") for h in HALF_LIVES]


def vname(h, m):
    return "full" if h is None else f"{m[0]}{h // 1000}k"


def job(args):
    key, kw = args
    r = bs.run_policy(**kw)
    out = {k: r[k] for k in SLIM}
    out["share_T"] = r["share_T"].mean(1)
    return key, out


def make_jobs(a):
    jobs = []
    for L in a.levels:
        for sc in a.scenarios:
            for p in a.policies + REFERENCE:
                for h, m in (variants() if p in a.policies else [(None, "decay")]):
                    kw = dict(policy=p, scenario=sc, R=a.R, T=a.T, N=a.N, seed=bs.scenario_seed(sc),
                              new_level=L, tv_every=10 ** 9, half_life=h, recency=m)
                    jobs.append(((sc, L, p, vname(h, m)), kw))
    return jobs


def prior_rank_corr(sc, h, m, T, B=256, n_base=3):
    """Spearman correlation of the transfer prior's mean with v+1's starting rates, per base run.

    Replays run_policy's base runs exactly (same seed, same draw order).
    """
    old, new = bs.make_scenario(sc)
    rng = np.random.default_rng(bs.scenario_seed(sc))
    out = []
    for _ in range(n_base):
        if h is None:
            s, n = bs.base_run_counts(rng, old, T // 4, B, T)
        else:
            s, n, sr, nr = bs.base_run_counts(rng, old, T // 4, B, T, h)
            if m == "decay":
                s, n = sr, nr
        p = (s + 1) / (n + 2)
        out.append(spearmanr(p, new["theta"])[0])
    return np.mean(out), np.mean(n)


def report(res, a, out):
    vs = [vname(h, m) for h, m in variants()][1:]
    L_ = []
    w = L_.append
    w("# Run 11: recency-weighted priors\n")
    w(f"R={a.R}, T={a.T}, N={a.N}, levels {a.levels}. Half-lives are in base-run executions "
      f"(all operators; the base run is {a.T // 4} executions, ~{a.T // 4 // bs.K} per operator).\n")
    w("Variants: `full` = current prior (all base-run counts). `d<h>` = recency-weighted counts for mean and "
      "weight. `w<h>` = full-run mean, weight capped at the recency-weighted count (\"weaker, not more recent\").\n")
    w("Cells: median successes at 1h for `full`; for the others, median ratio to `full` for the same policy. "
      "`*` marks Mann-Whitney p < 0.05 after Holm across the 6 variants in that row.\n")

    w("\n## Prior quality\n")
    w("Spearman correlation between the transfer prior's mean and v+1's starting rates (mean of the 3 base "
      "runs), and effective executions per operator.\n")
    hdr = ["full"] + [f"d{h // 1000}k" for h in HALF_LIVES]
    w("| scenario | " + " | ".join(hdr) + " |\n|---|" + "---|" * len(hdr))
    for sc in a.scenarios:
        cells = []
        for h in [None] + HALF_LIVES:
            r, n = prior_rank_corr(sc, h, "decay", a.T)
            cells.append(f"{r:.2f} (n≈{n:.0f})")
        w(f"| {sc} | " + " | ".join(cells) + " |")

    groups = [("drift", [s for s in a.scenarios if s in DRIFT]),
              ("controls (uniform decay on v)", [s for s in a.scenarios if s not in DRIFT])]
    for c in ("1h", "4h"):
        for L in a.levels:
            for p in a.policies:
                w(f"\n## {p}, L={L:g}, {c}\n")
                w("| scenario | full | " + " | ".join(vs) + " |\n|---|---|" + "---|" * len(vs))
                for gname, scs in groups:
                    w(f"| *{gname}* |" + " |" * (len(vs) + 1))
                    for sc in scs:
                        base = res[(sc, L, p, "full")]["succ"][c]
                        ys = [res[(sc, L, p, v)]["succ"][c] for v in vs]
                        ps = bs.holm([bs.mann_whitney(y, base)[1] for y in ys])
                        cells = [f"{np.median(y) / np.median(base):.2f}{'*' if q < 0.05 else ''}"
                                 for y, q in zip(ys, ps)]
                        w(f"| {sc} | {np.median(base):.0f} | " + " | ".join(cells) + " |")
            if c == "4h":
                break  # 4h tables only for the first level, to keep the summary short
    w("\n## Reference: fixed priors at 1h (full-run prior)\n")
    w("| scenario | L | fresh | calib | transfer | bmcs_cal_r | mix50_cal_r |\n|---|---|---|---|---|---|---|")
    for L in a.levels:
        for sc in a.scenarios:
            cells = [f"{np.median(res[(sc, L, p, 'full')]['succ']['1h']):.0f}" for p in REFERENCE + a.policies]
            w(f"| {sc} | {L:g} | " + " | ".join(cells) + " |")
    with open(os.path.join(out, "summary.md"), "w") as fh:
        fh.write("\n".join(L_) + "\n")
    print(f"wrote {os.path.join(out, 'summary.md')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=30)
    ap.add_argument("--T", type=int, default=1_000_000)
    ap.add_argument("--N", type=int, default=5000)
    ap.add_argument("--levels", default="1,0.2")
    ap.add_argument("--scenarios", default=",".join(DRIFT + CONTROL + RANK))
    ap.add_argument("--policies", default=",".join(POLICIES))
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--save_every", type=int, default=50)
    ap.add_argument("--out", default="results/recency")
    ap.add_argument("--report", action="store_true", help="only write summary.md from raw.pkl")
    a = ap.parse_args()
    a.levels = [float(x) for x in a.levels.split(",")]
    a.scenarios = a.scenarios.split(",")
    a.policies = a.policies.split(",")
    out = os.path.join(HERE, a.out)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "raw.pkl")
    res = {}
    if os.path.exists(path):
        with open(path, "rb") as fh:
            res = pickle.load(fh)["res"]
    if not a.report:
        jobs = make_jobs(a)
        todo = [j for j in jobs if j[0] not in res]
        print(f"{len(jobs)} jobs, {len(todo)} to run", flush=True)
        save = lambda: pickle.dump(dict(res=res, args=vars(a)), open(path, "wb"))
        t0 = time.time()
        with Pool(a.jobs) as pool:
            for i, (key, r) in enumerate(pool.imap_unordered(job, todo, chunksize=2), 1):
                res[key] = r
                if i % a.save_every == 0:
                    save()
                    el = time.time() - t0
                    print(f"{i}/{len(todo)} done, {el / 60:.1f} min, ~{el / i * (len(todo) - i) / 60:.0f} min left",
                          flush=True)
        save()
        print(f"done in {(time.time() - t0) / 60:.1f} min", flush=True)
    report(res, a, out)


if __name__ == "__main__":
    main()
