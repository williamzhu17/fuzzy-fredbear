"""Analysis of the final sweep (README run 10). Reads <dir>/raw.pkl from final_sweep.py, writes <dir>/summary.md.

Usage:
  python final_report.py results/final [--reps 2000]

Sections:
  A. designed scenarios: medians and the adaptive controller's comparisons (Holm within each cell)
  B. every policy against the hindsight-best fixed prior, over all scenario x level cells
  C. rank-sweep cells split by whether transfer helps, is neutral, or hurts
  D. head-to-head counts for the adaptive controller
  E. prior check: does the old ranking itself matter (transfer vs calib and shuffled)?
  F. simulated Stage 2: power of per-transition and pooled tests over random transitions
"""
import argparse
import os
import pickle

import numpy as np
from scipy.stats import norm

import bandit_sim as bs

HERE = os.path.dirname(os.path.abspath(__file__))
ADAPT = "bmcs_cal_r"
FIXED = ("fresh", "calib", "transfer")  # candidates for the hindsight-best fixed prior
NAMES = {"fresh": "fresh", "calib": "calib", "shuffled": "shuffled", "transfer": "transfer",
         "bmcs_cal": "adaptive (unscaled)", "bmcs_cal_r": "adaptive", "mix50_cal_r": "50/50"}


def cmp(x, y):
    """(A12, two-sided MWU p)."""
    return bs.a12(x, y), bs.mann_whitney(x, y)[1]


def wtl(pairs, alpha=0.05):
    """Win / tie / loss counts from a list of (A12, p)."""
    w = sum(1 for a, p in pairs if p < alpha and a > 0.5)
    l = sum(1 for a, p in pairs if p < alpha and a < 0.5)
    return w, len(pairs) - w - l, l


def signed_z(X, Y):
    """MWU z statistic (normal approximation, no tie correction) for each row of X (reps, n) vs Y (reps, m)."""
    n, m = X.shape[1], Y.shape[1]
    U = ((X[:, :, None] > Y[:, None, :]) + 0.5 * (X[:, :, None] == Y[:, None, :])).sum((1, 2))
    return (U - n * m / 2) / np.sqrt(n * m * (n + m + 1) / 12)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir")
    ap.add_argument("--reps", type=int, default=2000)
    ap.add_argument("--transitions", type=int, default=6)
    ap.add_argument("--at", default="1h")
    a = ap.parse_args()
    d = pickle.load(open(os.path.join(HERE, a.results_dir, "raw.pkl"), "rb"))
    res, args = d["res"], d["args"]
    levels = sorted({k[1] for k in res}, reverse=True)
    pols = [p for p in args["policies"].split(",")]
    scs = list(dict.fromkeys(k[0] for k in res))
    designed = [s for s in scs if not s.startswith("rank")]
    ranked = [s for s in scs if s.startswith("rank")]
    g = lambda sc, L, p, t=a.at: res[(sc, L, p)]["succ"][t]
    med = lambda sc, L, p, t=a.at: float(np.median(g(sc, L, p, t)))
    old_best_kept = {s: int(np.argmax(bs.make_scenario(s)[1]["theta"]) == 0) for s in scs}

    L_ = []
    L_.append("# Final Stage 1 sweep\n")
    L_.append(f"R = {args['R']} trials per cell, T = {args['T']:,}, N = {args['N']}, levels {levels}, "
              f"{len(designed)} designed scenarios + {len(ranked)} rank-sweep transitions "
              f"({args['draws']} draws per rho, rho in {args['rhos']}). Outcome: successes at {a.at} unless noted. "
              f"'adaptive' = {ADAPT}, '50/50' = mix50_cal_r, 'adaptive (unscaled)' = bmcs_cal. "
              "Significance is two-sided MWU at 0.05; 'unadj.' marks counts without multiplicity correction.\n")

    # ---------------------------------------------------------------- A
    L_.append("\n## A. Designed scenarios\n")
    L_.append("Median successes. The last column is the adaptive controller vs transfer / calib / fresh / 50/50 "
              "(A12; * = significant after Holm over these 4 comparisons in the cell).\n")
    L_.append("| L | scenario | " + " | ".join(NAMES[p] for p in pols) + " | adaptive vs T / C / F / 50/50 |")
    L_.append("|---|---|" + "---|" * len(pols) + "---|")
    for L in levels:
        for sc in designed:
            others = ["transfer", "calib", "fresh", "mix50_cal_r"]
            cs = [cmp(g(sc, L, ADAPT), g(sc, L, o)) for o in others]
            adj = bs.holm(np.array([p for _, p in cs]))
            cell = " / ".join(f"{A:.2f}{'*' if q < 0.05 else ''}" for (A, _), q in zip(cs, adj))
            L_.append(f"| {L:g} | {sc} | " + " | ".join(f"{med(sc, L, p):.0f}" for p in pols) + f" | {cell} |")

    # ---------------------------------------------------------------- B
    L_.append("\n## B. Every policy against the hindsight-best fixed prior\n")
    L_.append("For each scenario x level cell, the best fixed prior is whichever of fresh / calib / transfer has the "
              "highest median in that cell (chosen in hindsight, so no real policy can beat it on average). "
              "Ratio = policy median / best-fixed median. 'within 5%' = share of cells with ratio >= 0.95. "
              "worse / better = cells where the policy is significantly below / above the best fixed prior (unadj.).\n")
    for group, cells in (("all cells", scs), ("designed only", designed), ("rank sweep only", ranked)):
        L_.append(f"\n**{group}**\n")
        L_.append("| L | policy | median ratio | 10th pct | worst | within 5% | worse / better | 4h median ratio |")
        L_.append("|---|---|---|---|---|---|---|---|")
        for L in levels:
            for p in pols:
                r, r4, pv = [], [], []
                for sc in cells:
                    best = max(FIXED, key=lambda q: med(sc, L, q))
                    best4 = max(FIXED, key=lambda q: med(sc, L, q, "4h"))
                    r.append(med(sc, L, p) / max(med(sc, L, best), 1e-9))
                    r4.append(med(sc, L, p, "4h") / max(med(sc, L, best4, "4h"), 1e-9))
                    pv.append(cmp(g(sc, L, p), g(sc, L, best)))
                w, _, l = wtl(pv)
                r = np.array(r)
                L_.append(f"| {L:g} | {NAMES[p]} | {np.median(r):.3f} | {np.percentile(r, 10):.3f} | {r.min():.3f} | "
                          f"{(r >= 0.95).mean():.0%} | {l} / {w} | {np.median(r4):.3f} |")

    # ---------------------------------------------------------------- C
    L_.append("\n## C. Rank sweep split by whether transfer helps\n")
    L_.append("Regime from the transfer / calib median ratio in the cell: helps > 1.05, neutral 0.95-1.05, hurts < 0.95. "
              "Cells show the median over cells of each policy's median relative to calib; then the adaptive "
              "controller's win / tie / loss counts (unadj.) against 50/50 and against transfer, and its mean P(T) at 1h.\n")
    show = [p for p in ("fresh", "shuffled", "transfer", "bmcs_cal", ADAPT, "mix50_cal_r") if p in pols]
    L_.append("| L | regime | cells | " + " | ".join(NAMES[p] for p in show) + " | adaptive vs 50/50 W/T/L | adaptive vs transfer W/T/L | P(T) 1h |")
    L_.append("|---|---|---|" + "---|" * len(show) + "---|---|---|")
    for L in levels:
        ratio = {sc: med(sc, L, "transfer") / med(sc, L, "calib") for sc in ranked}
        for name, lo, hi in (("helps", 1.05, np.inf), ("neutral", 0.95, 1.05), ("hurts", -np.inf, 0.95)):
            cells = [sc for sc in ranked if lo <= ratio[sc] < hi]
            if not cells:
                continue
            rel = [f"{np.median([med(sc, L, p) / med(sc, L, 'calib') for sc in cells]):.2f}" for p in show]
            vs50 = wtl([cmp(g(sc, L, ADAPT), g(sc, L, "mix50_cal_r")) for sc in cells])
            vsT = wtl([cmp(g(sc, L, ADAPT), g(sc, L, "transfer")) for sc in cells])
            pt = np.mean([res[(sc, L, ADAPT)]["post_T_1h"].mean() for sc in cells])
            L_.append(f"| {L:g} | {name} | {len(cells)} | " + " | ".join(rel)
                      + f" | {'/'.join(map(str, vs50))} | {'/'.join(map(str, vsT))} | {pt:.2f} |")

    # ---------------------------------------------------------------- D
    L_.append("\n## D. Adaptive controller head-to-head, all cells\n")
    L_.append("Win / tie / loss (significant unadj.), median of per-cell median ratios, and the range of that ratio.\n")
    L_.append("| L | adaptive vs | W / T / L | median ratio | range |")
    L_.append("|---|---|---|---|---|")
    for L in levels:
        for o in [p for p in pols if p != ADAPT]:
            pairs = [cmp(g(sc, L, ADAPT), g(sc, L, o)) for sc in scs]
            rr = np.array([med(sc, L, ADAPT) / max(med(sc, L, o), 1e-9) for sc in scs])
            L_.append(f"| {L:g} | {NAMES[o]} | {' / '.join(map(str, wtl(pairs)))} | {np.median(rr):.3f} | "
                      f"{rr.min():.2f}-{rr.max():.2f} |")

    # ---------------------------------------------------------------- E
    L_.append("\n## E. Prior check: does the old ranking itself matter?\n")
    L_.append("Transfer against calib (right scale, no ranking) and shuffled (right scale and spread, wrong ranking), "
              "in rank-sweep cells where the old best operator is still best vs where it is not.\n")
    L_.append("| L | old best kept? | cells | transfer vs calib W/T/L | transfer vs shuffled W/T/L | median T / C |")
    L_.append("|---|---|---|---|---|---|")
    for L in levels:
        for kept in (1, 0):
            cells = [sc for sc in ranked if old_best_kept[sc] == kept]
            if not cells:
                continue
            vc = wtl([cmp(g(sc, L, "transfer"), g(sc, L, "calib")) for sc in cells])
            vs = wtl([cmp(g(sc, L, "transfer"), g(sc, L, "shuffled")) for sc in cells]) if "shuffled" in pols else ("-",)
            tc = np.median([med(sc, L, "transfer") / med(sc, L, "calib") for sc in cells])
            L_.append(f"| {L:g} | {'yes' if kept else 'no'} | {len(cells)} | {'/'.join(map(str, vc))} | "
                      f"{'/'.join(map(str, vs))} | {tc:.2f} |")

    # ---------------------------------------------------------------- F
    k = a.transitions
    L_.append(f"\n## F. Simulated Stage 2: {k} random transitions, n trials per policy\n")
    L_.append(f"Each repetition ({a.reps}) draws {k} distinct transitions from the rank sweep at one level and, for each, "
              "n trials per policy resampled with replacement from that cell's 30. Detection rates:\n\n"
              f"- **per-transition**: mean share of the {k} transitions where the comparison is significant in the "
              "stated direction after Holm over the 5-comparison family (adaptive vs transfer, calib, fresh; "
              "transfer vs calib, fresh) plus adaptive vs 50/50, i.e. 6 tests;\n"
              f"- **pooled**: share of repetitions where a Stouffer combination of the {k} signed MWU z-scores is "
              "significant (two-sided 0.05) in the stated direction.\n\n"
              "'Population effect' is the mean A12 over all rank cells at that level (what the pooled test estimates). "
              "Resampling from 30 trials understates real variability; treat these as upper bounds.\n")
    comps = [(ADAPT, "mix50_cal_r", "adaptive > 50/50"), (ADAPT, "transfer", "adaptive > transfer"),
             (ADAPT, "calib", "adaptive > calib"), (ADAPT, "fresh", "adaptive > fresh"),
             ("transfer", "calib", "transfer > calib"), ("transfer", "fresh", "transfer > fresh")]
    rng = np.random.default_rng(0)
    L_.append("| L | comparison | population A12 | n=10 per-transition | n=10 pooled | n=20 per-transition | n=20 pooled |")
    L_.append("|---|---|---|---|---|---|---|")
    for L in levels:
        pop = {c: np.mean([bs.a12(g(sc, L, c[0]), g(sc, L, c[1])) for sc in ranked]) for c in comps}
        det = {}
        for n in (10, 20):
            picks = np.array([rng.choice(len(ranked), k, replace=False) for _ in range(a.reps)])  # (reps, k)
            Z = np.zeros((len(comps), a.reps, k))
            for j in range(k):
                samp = {}
                for p in {q for c in comps for q in c[:2]}:
                    data = np.stack([g(ranked[i], L, p) for i in picks[:, j]])  # (reps, 30)
                    idx = rng.integers(0, data.shape[1], (a.reps, n))
                    samp[p] = np.take_along_axis(data, idx, 1)
                for ci, (x, y, _) in enumerate(comps):
                    Z[ci, :, j] = signed_z(samp[x], samp[y])
            P = 2 * norm.sf(np.abs(Z))  # (C, reps, k)
            adj = np.stack([np.stack([bs.holm(P[:, r, j]) for j in range(k)], 1) for r in range(a.reps)], 1)
            per = ((adj < 0.05) & (Z > 0)).mean((1, 2))
            pooled_z = Z.sum(2) / np.sqrt(k)
            pooled = (pooled_z > norm.isf(0.025)).mean(1)
            det[n] = (per, pooled)
        for ci, c in enumerate(comps):
            L_.append(f"| {L:g} | {c[2]} | {pop[c]:.2f} | {det[10][0][ci]:.2f} | {det[10][1][ci]:.2f} | "
                      f"{det[20][0][ci]:.2f} | {det[20][1][ci]:.2f} |")

    out = os.path.join(HERE, a.results_dir, "summary.md")
    with open(out, "w") as fh:
        fh.write("\n".join(L_) + "\n")
    print("\n".join(L_))


if __name__ == "__main__":
    main()
