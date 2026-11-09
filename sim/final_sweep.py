"""Final Stage 1 sweep (README run 10): every Stage 2 policy on the designed scenarios and the
rank-correlation sweep, at several inherited-corpus levels. Analysis is in final_report.py.

Usage:
  python final_sweep.py --out results/final            # runs everything (resumes if raw.pkl exists)
Writes <out>/raw.pkl: {"res": {(scenario, level, policy): run_policy output}, "args": ...}.
Progress is saved every --save_every jobs, and finished jobs are skipped on restart.
"""
import argparse
import os
import pickle
import time
from multiprocessing import Pool

import bandit_sim as bs

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGNED = ["no_shift", "mild_shift", "reversal", "saturation", "close_no_shift", "close_reversal",
            "late_riser", "depletion"]
POLICIES = ["fresh", "calib", "shuffled", "transfer", "bmcs_cal", "bmcs_cal_r", "mix50_cal_r"]
SLIM = ("succ", "expected", "oracle", "post_T", "share_T")  # fields kept (per-batch best_share/tv dropped)


def job(args):
    key, kw = args
    r = bs.run_policy(**kw)
    out = {k: r[k] for k in SLIM}
    out["post_T_1h"] = r["post_T"][:, r["post_T"].shape[1] // 4 - 1]
    del out["post_T"]
    out["share_T"] = r["share_T"].mean(1)
    return key, out


def scenarios(rhos, draws):
    names = list(DESIGNED)
    for base in ("rank", "rankc"):
        names += [f"{base}_{rho:g}_{d}" for rho in rhos for d in range(draws)]
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=30)
    ap.add_argument("--T", type=int, default=1_000_000)
    ap.add_argument("--N", type=int, default=5000)
    ap.add_argument("--levels", default="1,0.5,0.2")
    ap.add_argument("--rhos", default="1,0.8,0.5,0.2,0,-0.5,-1")
    ap.add_argument("--draws", type=int, default=6)
    ap.add_argument("--policies", default=",".join(POLICIES))
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--save_every", type=int, default=100)
    ap.add_argument("--out", default="results/final")
    a = ap.parse_args()
    out = os.path.join(HERE, a.out)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "raw.pkl")
    res = {}
    if os.path.exists(path):
        with open(path, "rb") as fh:
            res = pickle.load(fh)["res"]
    levels = [float(x) for x in a.levels.split(",")]
    rhos = [float(x) for x in a.rhos.split(",")]
    jobs = [((sc, L, p), dict(policy=p, scenario=sc, R=a.R, T=a.T, N=a.N, seed=bs.scenario_seed(sc),
                              new_level=L, tv_every=10 ** 9))
            for L in levels for sc in scenarios(rhos, a.draws) for p in a.policies.split(",")]
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
                print(f"{i}/{len(todo)} done, {el / 60:.1f} min, ~{el / i * (len(todo) - i) / 60:.0f} min left", flush=True)
    save()
    print(f"done in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
