"""Power check at Stage 2's trial count: how often would the key effects be detected with n trials?

Reads a run_stage1.py results dir run with many trials (e.g. --R 200), repeatedly draws n trials per
policy without replacement, runs the comparison family per scenario with Holm correction, and reports
the fraction of repetitions where each comparison is significant (adjusted p < alpha) in each direction.

Usage:
  python power_check.py results/power --n 10 --reps 2000 --focus bmcs_cal_r
"""
import argparse
import os
import pickle

import numpy as np
from scipy.stats import mannwhitneyu

import bandit_sim as bs

HERE = os.path.dirname(os.path.abspath(__file__))


def family(focus):
    """Comparisons tested together (Holm) per scenario: the controller vs each fixed prior, plus transfer vs the priors."""
    return [(focus, "transfer"), (focus, "calib"), (focus, "fresh"), ("transfer", "calib"), ("transfer", "fresh")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir")
    ap.add_argument("--n", default="10", help="comma list of trials per policy")
    ap.add_argument("--reps", type=int, default=2000)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--at", default="1h")
    ap.add_argument("--N", type=int, default=5000)
    ap.add_argument("--focus", default="bmcs_cal")
    a = ap.parse_args()
    FAMILY = family(a.focus)
    with open(os.path.join(HERE, a.results_dir, "raw.pkl"), "rb") as fh:
        res = pickle.load(fh)
    rng = np.random.default_rng(0)
    scs = list(dict.fromkeys(k[0] for k in res))
    get = lambda sc, p: res[(sc, p, a.N, 0.98, 256)]["succ"][a.at]
    ns = [int(x) for x in a.n.split(",")]
    print(f"# Power check ({a.results_dir}, successes at {a.at}, N={a.N}, {a.reps} reps, Holm over "
          f"{len(FAMILY)} comparisons per scenario, alpha={a.alpha})\n")
    print("Full-sample A12 and MWU p use all trials. Detection columns: fraction of reps with Holm-adjusted "
          "p < alpha and A12 > 0.5 (x wins) / A12 < 0.5 (y wins).\n")
    print("| scenario | comparison | R | full A12 | full p | " + " | ".join(f"n={n}: x wins / y wins" for n in ns) + " |")
    print("|---|---|---|---|---|" + "---|" * len(ns))
    for sc in scs:
        rows = []
        for x, y in FAMILY:
            X, Y = get(sc, x), get(sc, y)
            rows.append([f"| {sc} | {x} vs {y} | {len(X)} | {bs.a12(X, Y):.2f} | {bs.mann_whitney(X, Y)[1]:.2g} |"])
        for n in ns:
            pv = np.zeros((a.reps, len(FAMILY)))
            sign = np.zeros((a.reps, len(FAMILY)))
            idx = {p: np.array([rng.choice(len(get(sc, p)), n, replace=False) for _ in range(a.reps)])
                   for p in {q for pair in FAMILY for q in pair}}
            for j, (x, y) in enumerate(FAMILY):
                X, Y = get(sc, x)[idx[x]], get(sc, y)[idx[y]]
                pv[:, j] = mannwhitneyu(X, Y, axis=1, method="asymptotic").pvalue
                sign[:, j] = np.sign((X[:, :, None] > Y[:, None, :]).mean((1, 2))
                                     + 0.5 * (X[:, :, None] == Y[:, None, :]).mean((1, 2)) - 0.5)
            adj = np.array([bs.holm(r) for r in pv])
            for j in range(len(FAMILY)):
                hit = adj[:, j] < a.alpha
                rows[j].append(f" {np.mean(hit & (sign[:, j] > 0)):.2f} / {np.mean(hit & (sign[:, j] < 0)):.2f} |")
        for r in rows:
            print("".join(r))


if __name__ == "__main__":
    main()
