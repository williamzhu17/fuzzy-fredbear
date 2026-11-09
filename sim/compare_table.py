"""Compact cross-scenario tables from a run_stage1.py results directory (reads <dir>/raw.pkl).

Prints median successes at 1h and 4h for each scenario x N x policy, and for one focus policy
the A12 / unadjusted MWU p against selected baselines at 1h plus mean P(T) over time.

Usage:
  python compare_table.py results/bmcs --focus bmcs_cal --against transfer,calib,fresh,bmc_cal
"""
import argparse
import os
import pickle

import numpy as np

import bandit_sim as bs

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir")
    ap.add_argument("--focus", default=None, help="policy for the A12 / P(T) table")
    ap.add_argument("--against", default="transfer,calib,fresh")
    ap.add_argument("--gamma", type=float, default=0.98)
    ap.add_argument("--B", type=int, default=256)
    a = ap.parse_args()
    with open(os.path.join(HERE, a.results_dir, "raw.pkl"), "rb") as fh:
        res = pickle.load(fh)
    keys = [k for k in res if k[3] == a.gamma and k[4] == a.B]
    scs = list(dict.fromkeys(k[0] for k in keys))
    pols = list(dict.fromkeys(k[1] for k in keys))
    Ns = sorted(set(k[2] for k in keys))
    get = lambda sc, p, N: res.get((sc, p, N, a.gamma, a.B))

    for t in ("1h", "4h"):
        print(f"\nmedian successes at {t}")
        print(f"{'scenario':15s} {'N':>5s} " + " ".join(f"{p:>10s}" for p in pols))
        for N in Ns:
            for sc in scs:
                cells = [f"{np.median(get(sc, p, N)['succ'][t]):10.0f}" if get(sc, p, N) else f"{'-':>10s}" for p in pols]
                print(f"{sc:15s} {N:5d} " + " ".join(cells))

    if a.focus:
        against = a.against.split(",")
        print(f"\n{a.focus} at 1h: A12 / unadjusted p vs {', '.join(against)};  mean P(T) at 1, 15, 60, 239 min")
        for N in Ns:
            for sc in scs:
                x = get(sc, a.focus, N)
                if x is None:
                    continue
                cells = []
                for o in against:
                    y = get(sc, o, N)["succ"]["1h"]
                    cells.append(f"{bs.a12(x['succ']['1h'], y):.2f}/{bs.mann_whitney(x['succ']['1h'], y)[1]:.3f}")
                line = f"{sc:15s} {N:5d} " + "  ".join(cells)
                if not np.isnan(x["post_T"]).all():
                    nb = x["post_T"].shape[1]
                    pt = np.nanmean(x["post_T"], 0)
                    line += "   P(T): " + " ".join(f"{pt[min(nb - 1, int(m / 240 * nb))]:.2f}" for m in (1, 15, 60, 239))
                print(line)


if __name__ == "__main__":
    main()
