"""Stage 1 driver: scenario x policy grid at one or more N, plus N / gamma / B sensitivity for adaptive.

Usage:
  python run_stage1.py                                   # original 4 scenarios, all sweeps
  python run_stage1.py --scenarios close_no_shift,close_reversal,late_riser,depletion \
      --Ns 500,5000 --sweeps gamma --out results/hard
Writes <out>/summary.md, <out>/raw.pkl and <out>/*.png.
"""
import argparse
import os
import pickle
from multiprocessing import Pool

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import bandit_sim as bs

POLICIES = ["fresh", "calib", "shuffled", "transfer", "adaptive", "mix50"]
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = dict(N=500, gamma=0.98, B=256)
SWEEPS = {"N": [0, 50, 500, 5000], "gamma": [1.0, 0.98, 0.95], "B": [64, 256, 1024]}


def job(args):
    key, kw = args
    return key, bs.run_policy(**kw)


def med_iqr(x):
    q1, m, q3 = np.percentile(x, [25, 50, 75])
    return f"{m:.0f} [{q1:.0f}-{q3:.0f}]"


def windows(x):
    """Mean of a (R, nb) per-batch series over 0-15m / 15m-1h / 1h-4h."""
    nb = x.shape[1]
    m = x.mean(0)
    return " / ".join(f"{m[lo:hi].mean():.2f}" for lo, hi in [(0, nb // 16), (nb // 16, nb // 4), (nb // 4, nb)])


def recovery_minutes(best_share, win=20, thresh=0.5):
    """Minutes (of a 240-min campaign) until the rolling best-operator share first reaches thresh."""
    nb = best_share.shape[1]
    ker = np.ones(win) / win
    res = []
    for row in best_share:
        roll = np.convolve(row, ker, mode="valid")
        hit = np.nonzero(roll >= thresh)[0]
        res.append((hit[0] + win) * 240 / nb if len(hit) else np.inf)
    return np.array(res)


def fmt_spec(sp):
    s = f"theta: {np.array2string(sp['theta'] * sp['level'], precision=5)}"
    if not np.allclose(sp["tau"], 0.05):
        s += f"  \ntau (fraction of T): {np.array2string(sp['tau'], precision=3)}"
    if np.isfinite(sp["pool"]).any():
        s += f"  \npool (successes): {np.array2string(sp['pool'], precision=0)}"
    return s


def compare(lines, res, key, x_pol, others, title):
    x = res[key(x_pol)]["succ"]["1h"]
    lines.append(f"\n{title}\n")
    lines.append(f"| comparison | A12 | p (Holm) |\n|---|---|---|")
    ys = [res[key(o)]["succ"]["1h"] for o in others]
    ps = [bs.mann_whitney(x, y)[1] for y in ys]
    for o, y, padj in zip(others, ys, bs.holm(ps)):
        lines.append(f"| {x_pol} vs {o} | {bs.a12(x, y):.2f} | {padj:.3g} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=30)
    ap.add_argument("--T", type=int, default=1_000_000)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--scenarios", default="no_shift,mild_shift,reversal,saturation")
    ap.add_argument("--Ns", default="500", help="N values for the full policy grid")
    ap.add_argument("--sweeps", default="N,gamma,B", help="comma list of N,gamma,B ('' for none)")
    ap.add_argument("--out", default="results/original")
    ap.add_argument("--policies", default=",".join(POLICIES))
    ap.add_argument("--focus", default="adaptive", help="policies compared against all others")
    ap.add_argument("--level", type=float, default=1.0, help="multiplier on v+1 rates (inherited-corpus start)")
    a = ap.parse_args()
    POLICIES[:] = a.policies.split(",")
    focus = a.focus.split(",")
    scenarios = a.scenarios.split(",")
    Ns = [int(n) for n in a.Ns.split(",")]
    sweeps = [s for s in a.sweeps.split(",") if s]
    out = os.path.join(HERE, a.out)
    os.makedirs(out, exist_ok=True)

    # Every run is keyed by (scenario, policy, N, gamma, B); duplicates are run once.
    # Same seed per scenario across policies -> same base runs (common random numbers).
    # The seed comes from the scenario name (runs 1-4 used 1000 + list position instead).
    jobs = {}

    def add(i, sc, pol, **kw):
        p = {**DEFAULTS, **kw}
        key = (sc, pol, p["N"], p["gamma"], p["B"])
        jobs[key] = (key, dict(policy=pol, scenario=sc, R=a.R, T=a.T, seed=bs.scenario_seed(sc),
                                    new_level=a.level, **p))

    for i, sc in enumerate(scenarios):
        for N in Ns:
            for pol in POLICIES:
                add(i, sc, pol, N=N)
            for param in sweeps:
                if param == "N":
                    continue
                for val in SWEEPS[param]:
                    add(i, sc, "adaptive", N=N, **{param: val})
        if "N" in sweeps:
            for val in SWEEPS["N"]:
                for pol in ("adaptive", "transfer"):
                    add(i, sc, pol, N=val)

    with Pool(a.jobs) as p:
        res = dict(p.map(job, list(jobs.values())))
    with open(os.path.join(out, "raw.pkl"), "wb") as fh:
        pickle.dump(res, fh)

    lines = [f"# Stage 1 simulation results\n",
             f"R = {a.R} trials, T = {a.T:,} executions (= '4h'), K = {bs.K}, defaults gamma=0.98, B=256, "
             f"v+1 level multiplier = {a.level}.\n",
             "Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected "
             "successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.\n"]
    for sc in scenarios:
        old, new = bs.make_scenario(sc, a.level)
        lines.append(f"\n## {sc}\n")
        lines.append(f"**old** {fmt_spec(old)}  \n**new** {fmt_spec(new)}\n")
        for N in Ns:
            key = lambda pol: (sc, pol, N, DEFAULTS["gamma"], DEFAULTS["B"])
            lines.append(f"\n### N = {N}\n")
            lines.append("| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) "
                         "| share T (same windows) | TV C vs T after batch 1 / 15m / 1h |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for pol in POLICIES:
                r = res[key(pol)]
                tvm, tt = r["tv"].mean(0), r["tv_t"]
                tvs = " / ".join(f"{tvm[np.searchsorted(tt, x)]:.2f}" for x in [0, a.T // 16, a.T // 4])
                reg = r["oracle"]["4h"] - r["expected"]["4h"]
                lines.append(f"| {pol} | {med_iqr(r['succ']['15m'])} | {med_iqr(r['succ']['1h'])} "
                             f"| {med_iqr(r['succ']['4h'])} | {med_iqr(reg)} | {windows(r['best_share'])} "
                             f"| {windows(r['share_T'])} | {tvs} |")
            for fp in focus:
                compare(lines, res, key, fp, [p for p in POLICIES if p != fp],
                        f"{fp} vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P({fp} > other)):")
            ctl = [p for p in ("calib", "shuffled", "fresh") if p in POLICIES]
            if "transfer" in POLICIES and ctl:
                compare(lines, res, key, "transfer", ctl,
                        "Transfer vs prior controls at 1h (does the old *ranking* matter?):")
            if "reversal" in sc:
                lines.append("\nRecovery: minutes until the 20-batch rolling best-op share reaches 50% "
                             "(median [IQR]; never = count of trials that never do):\n")
                for pol in POLICIES:
                    rec = recovery_minutes(res[key(pol)]["best_share"])
                    q = np.percentile(np.minimum(rec, 240), [25, 50, 75])  # never -> 240 for quantiles
                    lines.append(f"- {pol}: {q[1]:.1f} [{q[0]:.1f}-{q[2]:.1f}], never: {np.isinf(rec).sum()}/{len(rec)}")

    if sweeps:
        lines.append("\n# Sensitivity (median successes at 1h / 4h)\n")
    for param in sweeps:
        vals = SWEEPS[param]
        lines.append(f"\n## {param}\n")
        lines.append("| scenario | policy | " + " | ".join(f"{param}={v}" for v in vals) + " |")
        lines.append("|---|---|" + "---|" * len(vals))
        for sc in scenarios:
            rows = [(pol, None) for pol in ("adaptive", "transfer")] if param == "N" else [("adaptive", N) for N in Ns]
            for pol, N in rows:
                cells = []
                for v in vals:
                    p = {**DEFAULTS, **({"N": N} if N is not None else {}), param: v}
                    r = res[(sc, pol, p["N"], p["gamma"], p["B"])]
                    cells.append(f"{np.median(r['succ']['1h']):.0f} / {np.median(r['succ']['4h']):.0f}")
                label = pol if N is None else f"{pol} (N={N})"
                lines.append(f"| {sc} | {label} | " + " | ".join(cells) + " |")
    with open(os.path.join(out, "summary.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    # Plots per N: adaptive's share to T, best-op share for key policies, F-vs-T divergence.
    n = len(scenarios)
    for N in Ns:
        key = lambda sc, pol: (sc, pol, N, DEFAULTS["gamma"], DEFAULTS["B"])
        fig, axes = plt.subplots(3, n, figsize=(4 * n, 10), sharex=True, squeeze=False)
        w = 20
        smooth = lambda y: np.convolve(y, np.ones(w) / w, mode="valid")
        for i, sc in enumerate(scenarios):
            nb = res[key(sc, focus[0])]["share_T"].shape[1]
            tmin = (np.arange(nb - w + 1) + w / 2) * 240 / nb
            for fp in focus:
                axes[0, i].plot(tmin, smooth(res[key(sc, fp)]["share_T"].mean(0)), label=fp)
            axes[0, i].axhline(0.5, ls=":", c="gray")
            axes[0, i].set_ylim(0, 1)
            axes[0, i].set_title(f"{sc} (N={N})")
            for pol in [p for p in ["fresh", "transfer"] if p in POLICIES] + focus:
                rr = res[key(sc, pol)]
                axes[1, i].plot(tmin, smooth(rr["best_share"].mean(0)), label=pol)
                axes[2, i].plot(rr["tv_t"] * 240 / a.T, rr["tv"].mean(0), label=pol)
            axes[1, i].set_ylim(0, 1)
            axes[2, i].set_xlabel("minutes")
        axes[0, 0].set_ylabel("share of batches / execs to T")
        axes[0, 0].legend()
        axes[1, 0].set_ylabel("share of execs on current best op")
        axes[2, 0].set_ylabel("TV(C, T) recommendation")
        axes[1, 0].legend()
        fig.tight_layout()
        fig.savefig(os.path.join(out, f"timeseries_N{N}.png"), dpi=100)
        plt.close(fig)

        fig, axes = plt.subplots(1, n, figsize=(4 * n, 4), squeeze=False)
        for i, sc in enumerate(scenarios):
            axes[0, i].boxplot([res[key(sc, p)]["succ"]["1h"] for p in POLICIES], tick_labels=POLICIES)
            axes[0, i].set_title(f"{sc}: successes at 1h (N={N})", fontsize=9)
            axes[0, i].tick_params(axis="x", rotation=45)
        fig.tight_layout()
        fig.savefig(os.path.join(out, f"successes_1h_N{N}.png"), dpi=100)
        plt.close(fig)
    print(open(os.path.join(out, "summary.md")).read())


if __name__ == "__main__":
    main()
