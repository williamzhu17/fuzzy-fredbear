"""Rank-correlation sweep: where does transfer stop helping, and does bmcs_cal switch at the right point?

v+1 rates are a permutation of v's rates (bandit_sim.rank_rates), so only the ranking shifts.
Scenario names: rank_<rho>_<draw> (OLD_RATES) and rankc_<rho>_<draw> (CLOSE_RATES).

Usage:
  python rank_sweep.py --level 0.5 --N 5000 --draws 6 --out results/rank
Writes <out>/summary.md, <out>/raw.pkl, <out>/rank_sweep.png.
"""
import argparse
import os
import pickle
from multiprocessing import Pool

import numpy as np
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import bandit_sim as bs

HERE = os.path.dirname(os.path.abspath(__file__))


def job(args):
    key, kw = args
    return key, bs.run_policy(**kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=30)
    ap.add_argument("--T", type=int, default=1_000_000)
    ap.add_argument("--N", type=int, default=5000)
    ap.add_argument("--level", type=float, default=1.0)
    ap.add_argument("--rhos", default="1,0.8,0.5,0.2,0,-0.5,-1")
    ap.add_argument("--draws", type=int, default=6)
    ap.add_argument("--bases", default="rank,rankc")
    ap.add_argument("--policies", default="fresh,calib,transfer,mix50_cal,bmcs_cal")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", default="results/rank")
    ap.add_argument("--replot", action="store_true", help="redo summary and plot from <out>/raw.pkl")
    a = ap.parse_args()
    rhos = [float(r) for r in a.rhos.split(",")]
    pols = a.policies.split(",")
    bases = a.bases.split(",")
    out = os.path.join(HERE, a.out)
    os.makedirs(out, exist_ok=True)

    saved = None
    if a.replot:
        with open(os.path.join(out, "raw.pkl"), "rb") as fh:
            saved = pickle.load(fh)
        a = argparse.Namespace(**{**saved["args"], "out": a.out})
        rhos = [float(r) for r in a.rhos.split(",")]
        pols, bases = a.policies.split(","), a.bases.split(",")
    scen = {}  # name -> (base, rho, draw, realized spearman, old best still best?)
    for base in bases:
        for rho in rhos:
            for d in range(a.draws):
                name = f"{base}_{rho:g}_{d}"
                old, new = bs.make_scenario(name)
                scen[name] = (base, rho, d, spearmanr(old["theta"], new["theta"])[0],
                              int(np.argmax(new["theta"]) == np.argmax(old["theta"])))
    if saved is not None:
        res = saved["res"]
    else:
        res = run_all(a, scen, pols)
        with open(os.path.join(out, "raw.pkl"), "wb") as fh:
            pickle.dump(dict(res=res, scen=scen, args=vars(a)), fh)
    report(a, out, scen, res, rhos, pols, bases)


def run_all(a, scen, pols):
    jobs = [((sc, p), dict(policy=p, scenario=sc, R=a.R, T=a.T, N=a.N, seed=bs.scenario_seed(sc),
                           new_level=a.level)) for sc in scen for p in pols]
    with Pool(a.jobs) as pool:
        return dict(pool.map(job, jobs))


def report(a, out, scen, res, rhos, pols, bases):
    med = lambda sc, p: np.median(res[(sc, p)]["succ"]["1h"])
    lines = [f"# Rank-correlation sweep\n",
             f"R = {a.R}, T = {a.T:,}, N = {a.N}, v+1 level = {a.level}, {a.draws} draws per rho. "
             "Cells are successes at 1h.\n"]
    for base in bases:
        names = [n for n in scen if scen[n][0] == base]
        lines.append(f"\n## {base} ({'OLD_RATES' if base == 'rank' else 'CLOSE_RATES'})\n")
        lines.append("Per nominal rho: median over draws of each draw's median; realized Spearman range; "
                     "draws where the old best is still best.\n")
        lines.append("| rho | Spearman | old best kept | " + " | ".join(pols) + " | bmcs / max(T, C) | P(T) at 1h |")
        lines.append("|---|---|---|" + "---|" * len(pols) + "---|---|")
        for rho in rhos:
            ns = [n for n in names if scen[n][1] == rho]
            sp = [scen[n][3] for n in ns]
            cells = [f"{np.median([med(n, p) for n in ns]):.0f}" for p in pols]
            ratio = [med(n, "bmcs_cal") / max(med(n, "transfer"), med(n, "calib")) for n in ns]
            nb = res[(ns[0], "bmcs_cal")]["post_T"].shape[1]
            pt = np.mean([np.nanmean(res[(n, "bmcs_cal")]["post_T"][:, nb // 4 - 1]) for n in ns])
            lines.append(f"| {rho:g} | {min(sp):.2f} to {max(sp):.2f} | {sum(scen[n][4] for n in ns)}/{len(ns)} | "
                         + " | ".join(cells) + f" | {np.median(ratio):.2f} [{min(ratio):.2f}-{max(ratio):.2f}] | {pt:.2f} |")

        lines.append("\nPer draw, sorted by realized Spearman: transfer / calib ratio and bmcs_cal's A12 "
                     "(unadjusted MWU p<0.05 marked *) vs transfer and vs calib.\n")
        lines.append("| scenario | Spearman | best kept | T / C | bmcs vs T | bmcs vs C | P(T) at 1h |")
        lines.append("|---|---|---|---|---|---|---|")
        for n in sorted(names, key=lambda n: -scen[n][3]):
            x = res[(n, "bmcs_cal")]["succ"]["1h"]
            cells = []
            for o in ("transfer", "calib"):
                y = res[(n, o)]["succ"]["1h"]
                cells.append(f"{bs.a12(x, y):.2f}{'*' if bs.mann_whitney(x, y)[1] < 0.05 else ''}")
            nb = res[(n, "bmcs_cal")]["post_T"].shape[1]
            pt = np.nanmean(res[(n, "bmcs_cal")]["post_T"][:, nb // 4 - 1])
            lines.append(f"| {n} | {scen[n][3]:.2f} | {scen[n][4]} | {med(n, 'transfer') / med(n, 'calib'):.2f} | "
                         f"{cells[0]} | {cells[1]} | {pt:.2f} |")
    with open(os.path.join(out, "summary.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    fig, axes = plt.subplots(2, len(bases), figsize=(6 * len(bases), 8), squeeze=False)
    for i, base in enumerate(bases):
        names = sorted([n for n in scen if scen[n][0] == base], key=lambda n: scen[n][3])
        x = [scen[n][3] for n in names]
        for p in pols:
            if p == "calib":
                continue
            axes[0, i].plot(x, [med(n, p) / med(n, "calib") for n in names], "o", ms=4, label=p, alpha=0.8)
        axes[0, i].axhline(1, ls=":", c="gray")
        axes[0, i].set_title(f"{base}: 1h successes relative to calib (N={a.N}, level={a.level})", fontsize=9)
        axes[0, i].set_ylabel("median / calib median")
        nb = res[(names[0], "bmcs_cal")]["post_T"].shape[1]
        axes[1, i].plot(x, [np.nanmean(res[(n, "bmcs_cal")]["post_T"][:, nb // 4 - 1]) for n in names], "o", ms=4)
        axes[1, i].set_ylim(0, 1)
        axes[1, i].set_ylabel("bmcs_cal mean P(T) at 1h")
        axes[1, i].set_xlabel("realized Spearman(old, new)")
    axes[0, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "rank_sweep.png"), dpi=100)
    print(open(os.path.join(out, "summary.md")).read())


if __name__ == "__main__":
    main()
